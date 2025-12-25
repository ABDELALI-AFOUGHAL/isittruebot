# -*- coding: utf-8 -*-
"""
Gemini AI Service Module
Senior Python Developer - Robust API Integration
"""

import logging
import time
from typing import Optional
import google.generativeai as genai
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type
)

logger = logging.getLogger(__name__)


class GeminiService:
    """Professional Gemini API integration with retry logic"""
    
    def __init__(self, api_key: str, model: str = 'gemini-2.5-flash'):
        """
        Initialize Gemini service
        
        Args:
            api_key: Google API key
            model: Model name to use
        """
        if not api_key or api_key == "YOUR_API_KEY_HERE":
            raise ValueError("CRITICAL: Gemini API key not configured in .env")
        
        self.api_key = api_key
        self.model_name = model
        
        # Configure API
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model)
        
        logger.info(f"[OK] Gemini service initialized with model: {model}")
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type(Exception),
        reraise=True
    )
    def generate_response(
        self,
        prompt: str,
        system_prompt: str = None,
        temperature: float = 0.7,
        max_tokens: int = 1000
    ) -> str:
        """
        Generate response from Gemini with retry logic
        
        Args:
            prompt: User prompt/input
            system_prompt: System prompt for context
            temperature: Response creativity (0.0-1.0)
            max_tokens: Maximum response length
            
        Returns:
            Generated response text
            
        Raises:
            Exception: If generation fails after retries
        """
        try:
            # Combine prompts
            full_prompt = prompt
            if system_prompt:
                full_prompt = f"{system_prompt}\n\nUser Input:\n{prompt}"
            
            # Configure generation
            generation_config = genai.types.GenerationConfig(
                temperature=temperature,
                top_p=0.95,
                top_k=40,
                max_output_tokens=max_tokens,
                candidate_count=1,
            )
            
            # Generate content
            logger.debug(f"Sending request to Gemini: {full_prompt[:100]}...")
            response = self.model.generate_content(
                full_prompt,
                generation_config=generation_config,
                safety_settings={
                    "HARM_CATEGORY_UNSPECIFIED": "BLOCK_NONE",
                    "HARM_CATEGORY_DEROGATORY": "BLOCK_ONLY_HIGH",
                    "HARM_CATEGORY_VIOLENCE": "BLOCK_ONLY_HIGH",
                    "HARM_CATEGORY_SEXUAL": "BLOCK_ONLY_HIGH",
                    "HARM_CATEGORY_MEDICAL": "BLOCK_ONLY_HIGH",
                    "HARM_CATEGORY_DANGEROUS": "BLOCK_ONLY_HIGH",
                }
            )
            
            result = response.text if response.text else "No response generated"
            logger.info(f"[OK] Response generated successfully ({len(result)} chars)")
            
            return result
        
        except genai.types.BlockedPromptException as e:
            logger.warning(f"[WARNING] Blocked by safety filter: {e}")
            raise ValueError("Content blocked by safety filter")
        
        except genai.types.StopCandidateException as e:
            logger.warning(f"[WARNING] Generation stopped: {e}")
            raise ValueError("Generation stopped - please rephrase")
        
        except genai.types.InvalidArgument as e:
            logger.error(f"[ERROR] Invalid argument: {e}")
            raise ValueError(f"Invalid request: {str(e)[:100]}")
        
        except Exception as e:
            logger.error(f"[ERROR] Gemini API error: {e}", exc_info=True)
            raise
    
    async def generate_response_async(
        self,
        prompt: str,
        system_prompt: str = None
    ) -> str:
        """
        Async wrapper for generate_response
        
        Args:
            prompt: User prompt
            system_prompt: System prompt
            
        Returns:
            Generated response
        """
        # Note: Gemini SDK doesn't have true async, so we run in executor
        # In production, consider using aiohttp with REST API
        return self.generate_response(prompt, system_prompt)
    
    def health_check(self) -> bool:
        """
        Check if Gemini service is available
        
        Returns:
            True if service is healthy
        """
        try:
            response = self.model.generate_content("test")
            return bool(response.text)
        except Exception as e:
            logger.error(f"[ERROR] Health check failed: {e}")
            return False


class AIResponseFormatter:
    """Format AI responses consistently"""
    
    @staticmethod
    def format_fact_check(response: str) -> str:
        """Format fact-check response"""
        return response
    
    @staticmethod
    def format_ai_detection(response: str) -> str:
        """Format AI detection response"""
        return response
    
    @staticmethod
    def format_general_chat(response: str) -> str:
        """Format general chat response"""
        return response
