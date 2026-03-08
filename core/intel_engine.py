import chromadb
from chromadb.utils import embedding_functions
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import time
from tavily import TavilyClient
load_dotenv()

class IntelEngine:
    def __init__(self):
        print(">> AI ENGINE STARTING...")
        # Database Setup
        self.client_db = chromadb.PersistentClient(path="D:/symbiote/core/vector_db")
        self.embed_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
        self.collection = self.client_db.get_or_create_collection(name="intel_reports", embedding_function=self.embed_fn)
        self.tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
        
        # New SDK Client
        api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        self.client_ai = genai.Client(api_key=api_key)
        self.model_id = 'gemini-2.0-flash'
        print(">> AI ENGINE INITIALIZED SUCCESSFULLY.")

    def ingest_report(self, report_id, file_path):
        """Reads TXT or PDF, chunks the text, and saves to ChromaDB."""
        try:
            content = ""
            # --- PDF HANDLING ---
            if file_path.lower().endswith(".pdf"):
                from pypdf import PdfReader
                reader = PdfReader(file_path)
                for page in reader.pages:
                    text = page.extract_text()
                    if text:
                        content += text + "\n"
            
            # --- TXT HANDLING ---
            else:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            
            if not content.strip():
                return f"SKIP: No readable text in {report_id}"

            # Create overlapping tactical chunks
            chunks = [content[i:i+600] for i in range(0, len(content), 450)]
            ids = [f"{report_id}_{i}" for i in range(len(chunks))]
            
            # Upsert into the private vector vault
            self.collection.upsert(
                documents=chunks,
                ids=ids,
                metadatas=[{"source": report_id}] * len(chunks)
            )
            return f"SUCCESS: Ingested {len(chunks)} nodes from {report_id}."
            
        except Exception as e:
            return f"ERROR during ingestion: {str(e)}"
        
    def query(self, question, n_results=3):
        results = self.collection.query(query_texts=[question], n_results=n_results)
        return results['documents'][0] if results['documents'] else []

    def synthesize(self, question, context_chunks):
        #1. search local first
        local_results = self.collection.query(query_texts=[question], n_results=5)
        local_context = '\n'.join(local_results['documents'][0])
        
        #2  if local memory is thin, go to Web 
        if not local_context or len(local_context) < 100:
            web_context = self.web_search(question) 
            final_context = f"LOCAL MEMORY:\n{local_context}\n\nWEB INTELLIGENCE:\n{web_context}"  
        else:
            final_context = local_context
        for attempt in range(3):
            try:
                response = self.client_ai.models.generate_content(
                    model=self.model_id,
                    contents=f"CONTEXT DATA:\n{context_text}\n\nUSER QUERY:\n{question}",
                    config=types.GenerateContentConfig(
                        system_instruction="You are the Symbiote OS Intelligence Core. Provide tactical, concise summaries."
                    )
                )
                return response.text
            except Exception as e:
                if "429" in str(e):
                    print(f">> QUOTA HIT. COOLING DOWN (Attempt {attempt+1}/3)...")
                    time.sleep(10) # Wait 10 seconds before trying again
                else:
                    return f"SYNTHESIS ERROR: {str(e)}"
        
        return "SYSTEM ERROR: API Quota exhausted after 3 attempts. Please wait 60 seconds."
    
    def web_search(self, query):
        """Fetches real time data from web"""
        print(f">> SCANNING GLOBAL NETWORKS FOR: {query}")
        try:
            # search and get text content not just links
            search_result = self.tavily.search(query=query, search_depth="advanced")
            context = ""
            for res in search_result['results']:
                context += f"Source: {res['url']}\nContent: {res['content']}\n---\n"
            return context
        except Exception as e:
            return f"WEB SEARCH ERROR: {str(e)}"
        
        response = self.client_ai.models.generate_content(
            model=self.model_id,
            contents=f"CONTEXT DATA:\n{context_text}\n\nUSER QUERY:\n{question}",
            config=types.GenerateContentConfig(
                system_instruction="You are the Symbiote OS Intelligence Core. Provide tactical, concise summaries."
            )
        )
        return response.text