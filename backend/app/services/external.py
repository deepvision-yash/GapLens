import httpx
import structlog
from typing import List, Dict, Any, Optional
from app.core.config import settings

logger = structlog.get_logger()


class TavilyService:
    """Tavily search and extract service."""
    
    BASE_URL = "https://api.tavily.com"
    
    def __init__(self):
        self.api_key = settings.TAVILY_API_KEY
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def search(
        self,
        query: str,
        max_results: int = 10,
        search_depth: str = "advanced",
        include_domains: Optional[List[str]] = None,
        exclude_domains: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Search web using Tavily."""
        if not self.api_key:
            logger.warning("Tavily API key not configured, returning mock results")
            return self._mock_search_results(query)
        
        payload = {
            "api_key": self.api_key,
            "query": query,
            "max_results": max_results,
            "search_depth": search_depth,
            "include_answer": False,
            "include_raw_content": True,
        }
        
        if include_domains:
            payload["include_domains"] = include_domains
        if exclude_domains:
            payload["exclude_domains"] = exclude_domains
        
        try:
            response = await self.client.post(
                f"{self.BASE_URL}/search",
                json=payload,
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error("Tavily search failed", error=str(e))
            return self._mock_search_results(query)
    
    async def extract(self, urls: List[str]) -> Dict[str, Any]:
        """Extract full content from URLs."""
        if not self.api_key:
            logger.warning("Tavily API key not configured, returning mock extraction")
            return {"results": []}
        
        payload = {
            "api_key": self.api_key,
            "urls": urls,
        }
        
        try:
            response = await self.client.post(
                f"{self.BASE_URL}/extract",
                json=payload,
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error("Tavily extract failed", error=str(e))
            return {"results": []}
    
    def _mock_search_results(self, query: str) -> Dict[str, Any]:
        """Return mock search results for development."""
        return {
            "query": query,
            "results": [
                {
                    "url": "https://example.gov.in/official-notification",
                    "title": f"Official Notification for {query}",
                    "content": f"This is mock content for {query}. Official source with detailed information.",
                    "score": 0.95,
                    "published_date": "2024-01-15",
                },
                {
                    "url": "https://news.example.com/article",
                    "title": f"News Article about {query}",
                    "content": f"News coverage of {query} with analysis and updates.",
                    "score": 0.85,
                    "published_date": "2024-02-20",
                },
            ],
        }
    
    async def close(self):
        await self.client.aclose()


class JinaReaderService:
    """Jina AI Reader service for content extraction."""
    
    BASE_URL = "https://r.jina.ai/http://"
    SEARCH_URL = "https://s.jina.ai/"
    
    def __init__(self):
        self.api_key = settings.JINA_API_KEY
        self.client = httpx.AsyncClient(timeout=60.0)
    
    async def extract(self, url: str) -> Dict[str, Any]:
        """Extract clean markdown content from URL."""
        # Jina Reader doesn't require API key for basic usage
        extract_url = f"https://r.jina.ai/http://{url.replace('https://', '').replace('http://', '')}"
        
        headers = {}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        
        try:
            response = await self.client.get(extract_url, headers=headers)
            response.raise_for_status()
            
            content = response.text
            
            # Parse title from content (first line usually)
            lines = content.strip().split('\n')
            title = lines[0].replace('#', '').strip() if lines else "Untitled"
            
            return {
                "url": url,
                "title": title,
                "content": content,
                "success": True,
            }
        except Exception as e:
            logger.error("Jina Reader extract failed", url=url, error=str(e))
            return {
                "url": url,
                "title": "Failed to extract",
                "content": "",
                "success": False,
                "error": str(e),
            }
    
    async def search(self, query: str, max_results: int = 10) -> Dict[str, Any]:
        """Search using Jina AI search endpoint."""
        search_url = f"{self.SEARCH_URL}{query}"
        
        headers = {}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        
        try:
            response = await self.client.get(search_url, headers=headers, params={"q": query})
            response.raise_for_status()
            
            # Parse results - Jina search returns markdown
            content = response.text
            return {"query": query, "content": content, "success": True}
        except Exception as e:
            logger.error("Jina search failed", error=str(e))
            return {"query": query, "content": "", "success": False, "error": str(e)}
    
    async def close(self):
        await self.client.aclose()


class LLMService:
    """LLM service supporting Gemini and Groq."""
    
    def __init__(self):
        self.gemini_key = settings.GEMINI_API_KEY
        self.groq_key = settings.GROQ_API_KEY
        self.client = httpx.AsyncClient(timeout=60.0)
    
    async def generate_structured(
        self,
        prompt: str,
        schema: Dict[str, Any],
        provider: str = "gemini",
        temperature: float = 0.1,
    ) -> Dict[str, Any]:
        """Generate structured JSON output."""
        if provider == "gemini" and self.gemini_key:
            return await self._gemini_generate(prompt, schema, temperature)
        elif provider == "groq" and self.groq_key:
            return await self._groq_generate(prompt, schema, temperature)
        else:
            logger.warning("No LLM provider configured, returning mock")
            return self._mock_response(schema)
    
    async def _gemini_generate(
        self,
        prompt: str,
        schema: Dict[str, Any],
        temperature: float,
    ) -> Dict[str, Any]:
        """Generate using Gemini API."""
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.gemini_key}"
        
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": temperature,
                "responseMimeType": "application/json",
                "responseSchema": schema,
            },
        }
        
        try:
            response = await self.client.post(url, json=payload)
            response.raise_for_status()
            data = response.json()
            
            # Parse Gemini response
            text = data["candidates"][0]["content"]["parts"][0]["text"]
            import json
            return json.loads(text)
        except Exception as e:
            logger.error("Gemini generation failed", error=str(e))
            return self._mock_response(schema)
    
    async def _groq_generate(
        self,
        prompt: str,
        schema: Dict[str, Any],
        temperature: float,
    ) -> Dict[str, Any]:
        """Generate using Groq API."""
        url = "https://api.groq.com/openai/v1/chat/completions"
        
        headers = {
            "Authorization": f"Bearer {self.groq_key}",
            "Content-Type": "application/json",
        }
        
        payload = {
            "model": "llama-3.1-8b-instant",
            "messages": [
                {"role": "system", "content": "You are a precise JSON generator. Output only valid JSON."},
                {"role": "user", "content": f"{prompt}\n\nOutput schema: {schema}"},
            ],
            "temperature": temperature,
            "response_format": {"type": "json_object"},
        }
        
        try:
            response = await self.client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            
            import json
            return json.loads(data["choices"][0]["message"]["content"])
        except Exception as e:
            logger.error("Groq generation failed", error=str(e))
            return self._mock_response(schema)
    
    def _mock_response(self, schema: Dict[str, Any]) -> Dict[str, Any]:
        """Generate mock response based on schema."""
        # Simple mock based on schema properties
        props = schema.get("properties", {})
        result = {}
        for key, prop in props.items():
            if prop.get("type") == "string":
                result[key] = f"mock_{key}"
            elif prop.get("type") == "array":
                result[key] = []
            elif prop.get("type") == "number":
                result[key] = 0
            elif prop.get("type") == "boolean":
                result[key] = True
            elif prop.get("type") == "object":
                result[key] = {}
        return result
    
    async def close(self):
        await self.client.aclose()


# Global service instances
tavily_service = TavilyService()
jina_service = JinaReaderService()
llm_service = LLMService()