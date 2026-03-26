from dotenv import load_dotenv
import os
load_dotenv()
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
import time
import uuid
import asyncio

from .routing_model import RoutingModel
from .cache import CacheLayer
from .models import LLMManager
from .logger import LogManager

app = FastAPI(title="AI Gateway", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    prompt: str
    user_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    model_used: str
    routing_reason: str
    confidence_score: float
    latency_ms: float
    cache_hit: bool
    request_id: str

routing_model = RoutingModel()
cache = CacheLayer(similarity_threshold=0.85)
llm_manager = LLMManager()
log_manager = LogManager()

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    request_id = str(uuid.uuid4())
    start_time = time.time()
    
    try:
        await asyncio.sleep(0.01)
        
        cached_response, similarity = cache.get(request.prompt)
        if cached_response:
            latency_ms = (time.time() - start_time) * 1000
            log_manager.log_request(
                request_id=request_id,
                prompt=request.prompt,
                model_used=cached_response["model"],
                routing_reason="Cache hit",
                confidence_score=1.0,
                latency_ms=latency_ms,
                cache_hit=True,
                user_id=request.user_id
            )
            return ChatResponse(
                response=cached_response["text"],
                model_used=cached_response["model"],
                routing_reason="Cache hit",
                confidence_score=1.0,
                latency_ms=latency_ms,
                cache_hit=True,
                request_id=request_id
            )
        
        routing_decision = routing_model.route(request.prompt)
        model_used = routing_decision["model"]
        routing_reason = routing_decision["reason"]
        confidence = routing_decision["confidence"]
    
        response = await llm_manager.get_response(request.prompt, model_used)
        
        cache.set(request.prompt, {"text": response, "model": model_used})
        
        latency_ms = (time.time() - start_time) * 1000
        
        log_manager.log_request(
            request_id=request_id,
            prompt=request.prompt,
            model_used=model_used,
            routing_reason=routing_reason,
            confidence_score=confidence,
            latency_ms=latency_ms,
            cache_hit=False,
            user_id=request.user_id
        )
        
        return ChatResponse(
            response=response,
            model_used=model_used,
            routing_reason=routing_reason,
            confidence_score=confidence,
            latency_ms=latency_ms,
            cache_hit=False,
            request_id=request_id
        )
        
    except Exception as e:
        print(f"Error processing request {request_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/logs")
async def get_logs(limit: int = 100):
    return log_manager.get_logs(limit)

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "routing_model": routing_model.get_info(),
        "cache": cache.get_stats()
    }