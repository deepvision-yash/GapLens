import asyncio
import httpx
import re
import structlog
import json
from typing import List, Dict, Any, Optional, Union
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
        """Search using the configured provider and normalize results for the pipeline."""
        if settings.SEARCH_PROVIDER.strip().lower() == "jina":
            return await jina_service.search(query=query, max_results=max_results)
        if settings.SEARCH_PROVIDER.strip().lower() != "tavily":
            raise RuntimeError("SEARCH_PROVIDER must be either 'tavily' or 'jina'.")
        if not self.api_key:
            raise RuntimeError("TAVILY_API_KEY is not configured.")
        
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
        except httpx.HTTPError as e:
            logger.error("Tavily search failed", error=str(e))
            raise RuntimeError(f"Tavily search failed: {e}") from e
    
    async def extract(self, urls: List[str]) -> Dict[str, Any]:
        """Extract full content from URLs."""
        if not self.api_key:
            raise RuntimeError("TAVILY_API_KEY is not configured.")
        
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
        except httpx.HTTPError as e:
            logger.error("Tavily extract failed", error=str(e))
            raise RuntimeError(f"Tavily extraction failed: {e}") from e
    
    async def close(self):
        await self.client.aclose()


class JinaReaderService:
    """Jina AI Reader service for content extraction."""
    
    BASE_URL = "https://r.jina.ai/"
    SEARCH_URL = "https://s.jina.ai/"
    
    def __init__(self):
        self.api_key = settings.JINA_API_KEY
        self.client = httpx.AsyncClient(timeout=60.0)
    
    async def extract(self, url: str) -> Dict[str, Any]:
        """Extract clean markdown content from URL."""
        # Jina Reader doesn't require API key for basic usage
        extract_url = f"{self.BASE_URL}{url}"
        
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
        except httpx.HTTPError as e:
            logger.error("Jina Reader extract failed", url=url, error=str(e))
            return {
                "url": url,
                "title": "Failed to extract",
                "content": "",
                "success": False,
                "error": str(e),
            }
    
    async def search(self, query: str, max_results: int = 10) -> Dict[str, Any]:
        """Search via Jina's JSON search API."""
        if not self.api_key:
            raise RuntimeError("JINA_API_KEY is required when SEARCH_PROVIDER=jina.")
        headers = {"Authorization": f"Bearer {self.api_key}", "Accept": "application/json"}
        try:
            response = await self.client.post(
                f"{self.SEARCH_URL}search",
                headers=headers,
                json={"q": query, "num": max_results},
            )
            response.raise_for_status()
            data = response.json()
            items = data.get("data", data.get("results", []))
            if not isinstance(items, list):
                raise RuntimeError("Jina Search returned an unexpected response format.")
            results = []
            for item in items:
                if not isinstance(item, dict) or not item.get("url"):
                    continue
                try:
                    score = float(item.get("score", 0.0) or 0.0)
                except (TypeError, ValueError):
                    score = 0.0
                results.append({
                    "url": item["url"],
                    "title": item.get("title") or item.get("url"),
                    "content": item.get("content") or item.get("description"),
                    "score": score,
                    "published_date": item.get("publishedDate") or item.get("published_date") or item.get("publishedTime"),
                })
            return {"query": query, "results": results}
        except httpx.HTTPError as e:
            status = e.response.status_code if isinstance(e, httpx.HTTPStatusError) else None
            logger.error("Jina Search failed", status_code=status)
            raise RuntimeError(f"Jina Search failed{f' (HTTP {status})' if status else ''}.") from e
    
    async def embed(self, texts: List[str]) -> List[List[float]]:
        """Create Jina embeddings for a batch of source chunks."""
        if not self.api_key:
            raise RuntimeError("JINA_API_KEY is required for embeddings.")
        if not texts:
            return []
        try:
            response = await self.client.post(
                "https://api.jina.ai/v1/embeddings",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={
                    "model": settings.JINA_EMBEDDING_MODEL,
                    "input": texts,
                    "task": "retrieval.passage",
                    "dimensions": settings.EMBEDDING_DIM,
                    "embedding_type": "float",
                    "normalized": True,
                },
            )
            response.raise_for_status()
            data = response.json().get("data", [])
            ordered = sorted(data, key=lambda item: item.get("index", 0))
            vectors = [item.get("embedding") for item in ordered]
            if len(vectors) != len(texts) or any(not isinstance(vector, list) for vector in vectors):
                raise RuntimeError("Jina returned an invalid embedding response.")
            return vectors
        except (httpx.HTTPError, ValueError, KeyError) as exc:
            logger.error("Jina embeddings failed", error=str(exc))
            raise RuntimeError(f"Jina embeddings failed: {exc}") from exc

    async def close(self):
        await self.client.aclose()


class LLMService:
    """LLM service supporting Gemini and Groq."""
    
    def __init__(self):
        self.gemini_key = settings.GEMINI_API_KEY
        self.groq_key = settings.GROQ_API_KEY
        self.client = httpx.AsyncClient(timeout=60.0)

    async def _post_with_retry(self, url: str, *, headers: Dict[str, str], payload: Dict[str, Any], provider: str):
        """Retry one transient capacity/rate-limit response using the provider's wait hint."""
        for attempt in range(2):
            try:
                response = await self.client.post(url, headers=headers, json=payload)
                response.raise_for_status()
                return response
            except httpx.HTTPStatusError as exc:
                if exc.response.status_code not in (429, 500, 502, 503, 504) or attempt == 1:
                    raise
                retry_after = exc.response.headers.get("retry-after")
                match = re.search(r"try again in ([0-9]+(?:\.[0-9]+)?)\s*s", exc.response.text, re.IGNORECASE)
                if retry_after:
                    try:
                        delay = float(retry_after)
                    except ValueError:
                        delay = float(match.group(1)) if match else 2.0
                elif match:
                    delay = float(match.group(1))
                else:
                    delay = 2.0
                delay = min(60.0, max(1.0, delay))
                logger.warning("Provider capacity limit; retrying once", provider=provider, status_code=exc.response.status_code, retry_after_seconds=delay)
                await asyncio.sleep(delay)
    
    async def generate_structured(
        self,
        prompt: str,
        schema: Dict[str, Any],
        provider: Optional[str] = None,
        temperature: float = 0.1,
    ) -> Union[Dict[str, Any], List[Any]]:
        """Generate structured JSON output."""
        provider = (provider or settings.LLM_PROVIDER).strip().lower()
        if provider == "groq":
            if not self.groq_key:
                raise RuntimeError("GROQ_API_KEY is not configured.")
            return await self._groq_generate(prompt, schema, temperature)
        if provider != "gemini":
            raise RuntimeError("LLM_PROVIDER must be either 'gemini' or 'groq'.")
        if self.gemini_key:
            try:
                return await self._gemini_generate(prompt, schema, temperature)
            except Exception:
                if not self.groq_key:
                    raise
                logger.warning("Gemini request failed; trying configured Groq fallback")
        if self.groq_key:
            return await self._groq_generate(prompt, schema, temperature)
        raise RuntimeError("Configure GEMINI_API_KEY or GROQ_API_KEY to run research analysis.")
    
    async def _gemini_generate(
        self,
        prompt: str,
        schema: Dict[str, Any],
        temperature: float,
    ) -> Union[Dict[str, Any], List[Any]]:
        """Generate using Gemini API."""
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{settings.GEMINI_MODEL}:generateContent"
        
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": temperature,
                "responseMimeType": "application/json",
                "responseSchema": schema,
            },
        }
        
        try:
            response = await self._post_with_retry(url, headers={"x-goog-api-key": self.gemini_key}, payload=payload, provider="gemini")
            data = response.json()
            
            # Parse Gemini response
            text = data["candidates"][0]["content"]["parts"][0]["text"]
            import json
            return json.loads(text)
        except Exception as e:
            status = e.response.status_code if isinstance(e, httpx.HTTPStatusError) else None
            detail = e.response.text[:1200] if isinstance(e, httpx.HTTPStatusError) else str(e)
            logger.error("Gemini generation failed", status_code=status, detail=detail)
            raise RuntimeError(f"Gemini generation failed{f' (HTTP {status})' if status else ''}: {detail}") from e
    
    async def _groq_generate(
        self,
        prompt: str,
        schema: Dict[str, Any],
        temperature: float,
    ) -> Union[Dict[str, Any], List[Any]]:
        """Generate using Groq API."""
        url = "https://api.groq.com/openai/v1/chat/completions"
        
        headers = {
            "Authorization": f"Bearer {self.groq_key}",
            "Content-Type": "application/json",
        }
        
        instruction = "Return valid JSON only, as one object with a single 'result' property whose value matches the requested schema. Do not add prose."
        payload = {
            "model": settings.GROQ_MODEL,
            "messages": [
                {"role": "user", "content": f"{instruction}\n\n{prompt}\n\nSchema for result: {json.dumps(schema, ensure_ascii=False)}"},
            ],
            "temperature": temperature,
            # Groq defaults to 1024 completion tokens; reasoning plus JSON
            # output for scope/results can exceed that and produce truncated JSON.
            "max_completion_tokens": 4096,
            "response_format": {"type": "json_object"},
            "reasoning_format": "hidden",
            "reasoning_effort": "low",
        }
        
        try:
            response = await self._post_with_retry(url, headers=headers, payload=payload, provider="groq")
            data = response.json()
            
            parsed = json.loads(data["choices"][0]["message"]["content"])
            if isinstance(parsed, dict) and "result" in parsed:
                return parsed["result"]
            if schema.get("type") == "array":
                raise ValueError("Groq response did not include the required result array.")
            return parsed
        except Exception as e:
            detail = e.response.text[:1200] if isinstance(e, httpx.HTTPStatusError) else str(e)
            logger.error("Groq generation failed", detail=detail)
            raise RuntimeError(f"Groq generation failed: {detail}") from e
    
    async def close(self):
        await self.client.aclose()


# Global service instances
tavily_service = TavilyService()
jina_service = JinaReaderService()
llm_service = LLMService()
