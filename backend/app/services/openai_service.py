import os
from openai import OpenAI
from typing import Optional, Dict, Any
import logging
import asyncio
import time
from functools import wraps
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class OpenAIService:
    """Service for handling OpenAI ChatGPT API interactions"""
    
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        
        # Initialize OpenAI client with the new SDK
        self.client = OpenAI(api_key=self.api_key)
        
        # Configuration
        self.model = "gpt-3.5-turbo"  # Using free tier compatible model
        self.max_tokens = 1000
        self.temperature = 0.7
        
        # System prompt for travel documentation assistant
        self.system_prompt = """
        You are an expert travel documentation assistant. When users ask about travel requirements, 
        provide comprehensive, accurate, and well-formatted information including:
        
        1. Required visa documentation
        2. Passport requirements
        3. Additional necessary documents
        4. Relevant travel advisories
        5. Processing times where applicable
        6. Important notes or tips
        
        Format your responses clearly with proper sections and bullet points.
        Always provide current and accurate information based on official sources.
        Be helpful, informative, and professional in your responses.
        """
    
    def _retry_on_failure(max_retries: int = 3, delay: float = 1.0):
        """Decorator to retry failed API calls"""
        def decorator(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                last_exception = None
                for attempt in range(max_retries):
                    try:
                        return await func(*args, **kwargs)
                    except Exception as e:
                        last_exception = e
                        if attempt < max_retries - 1:
                            logger.warning(f"API call failed (attempt {attempt + 1}): {e}")
                            await asyncio.sleep(delay * (2 ** attempt))  # Exponential backoff
                        else:
                            logger.error(f"API call failed after {max_retries} attempts: {e}")
                
                raise last_exception
            return wrapper
        return decorator
    
    @_retry_on_failure(max_retries=3)
    async def generate_response(self, user_query: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Generate a response using OpenAI ChatGPT API
        
        Args:
            user_query: The user's question
            context: Optional context for the query
            
        Returns:
            Dictionary containing response and metadata
        """
        start_time = time.time()
        
        try:
            # Prepare messages
            messages = [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": user_query}
            ]
            
            # Add context if provided
            if context:
                context_message = f"Additional context: {context}"
                messages.insert(-1, {"role": "system", "content": context_message})
            
            # Make API call using the new SDK
            response = await asyncio.to_thread(
                self.client.chat.completions.create,
                model=self.model,
                messages=messages,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                top_p=1,
                frequency_penalty=0.2,
                presence_penalty=0.1
            )
            
            # Extract response
            ai_response = response.choices[0].message.content.strip()
            
            # Calculate response time
            response_time = time.time() - start_time
            
            # Return structured response
            return {
                "response": ai_response,
                "success": True,
                "response_time": response_time,
                "tokens_used": response.usage.total_tokens,
                "model": self.model,
                "metadata": {
                    "completion_tokens": response.usage.completion_tokens,
                    "prompt_tokens": response.usage.prompt_tokens,
                    "finish_reason": response.choices[0].finish_reason
                }
            }
            
        except Exception as e:
            # Handle different types of OpenAI API errors
            error_message = str(e)
            
            if "authentication" in error_message.lower():
                logger.error("OpenAI API authentication failed")
                raise Exception("API authentication failed. Please check your API key.")
            elif "rate_limit" in error_message.lower() or "quota" in error_message.lower():
                logger.error("OpenAI API rate limit exceeded")
                raise Exception("API rate limit exceeded. Please try again later.")
            elif "connection" in error_message.lower() or "network" in error_message.lower():
                logger.error("OpenAI API connection failed")
                raise Exception("Failed to connect to OpenAI API. Please check your internet connection.")
            elif "invalid" in error_message.lower():
                logger.error(f"Invalid OpenAI API request: {e}")
                raise Exception(f"Invalid API request: {str(e)}")
            else:
                logger.error(f"Unexpected error in OpenAI service: {e}")
                raise Exception(f"An error occurred while processing your request: {str(e)}")
    
    async def validate_api_key(self) -> bool:
        """Validate the OpenAI API key"""
        try:
            # Make a simple API call to validate the key
            response = await asyncio.to_thread(
                self.client.chat.completions.create,
                model=self.model,
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=5
            )
            return True
        except Exception as e:
            logger.error(f"API key validation failed: {e}")
            return False
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the current model"""
        return {
            "model": self.model,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "provider": "OpenAI"
        }

# Global service instance
openai_service = OpenAIService()

async def generate_ai_response(query: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Generate AI response - main interface function"""
    return await openai_service.generate_response(query, context)