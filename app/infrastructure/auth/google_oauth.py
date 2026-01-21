"""
Infrastructure - Google OAuth

Google OAuth orqali autentifikatsiya.
"""

import httpx
from typing import Optional, Dict, Any

from app.infrastructure.db.database import settings


class GoogleOAuthClient:
    """Google OAuth client."""
    
    def __init__(self):
        self.client_id = settings.google_client_id
        self.client_secret = settings.google_client_secret
        self.redirect_uri = settings.google_redirect_uri
        self.token_url = "https://oauth2.googleapis.com/token"
        self.userinfo_url = "https://www.googleapis.com/oauth2/v2/userinfo"
    
    def get_authorization_url(self) -> str:
        """
        Google OAuth authorization URL yaratish.
        
        Returns:
            Authorization URL
        """
        base_url = "https://accounts.google.com/o/oauth2/v2/auth"
        params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "response_type": "code",
            "scope": "openid email profile",
            "access_type": "offline",
            "prompt": "consent"
        }
        
        query_string = "&".join([f"{k}={v}" for k, v in params.items()])
        return f"{base_url}?{query_string}"
    
    async def exchange_code_for_token(self, code: str) -> Optional[Dict[str, Any]]:
        """
        Authorization code'ni access token'ga almashtirish.
        
        Args:
            code: Authorization code
            
        Returns:
            Token ma'lumotlari yoki None
        """
        payload = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": self.redirect_uri
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(self.token_url, data=payload)
                response.raise_for_status()
                return response.json()
        except Exception as e:
            print(f"Token almashinuv xatosi: {str(e)}")
            return None
    
    async def get_user_info(self, access_token: str) -> Optional[Dict[str, Any]]:
        """
        Access token orqali foydalanuvchi ma'lumotlarini olish.
        
        Args:
            access_token: Google access token
            
        Returns:
            Foydalanuvchi ma'lumotlari yoki None
        """
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(self.userinfo_url, headers=headers)
                response.raise_for_status()
                return response.json()
        except Exception as e:
            print(f"User info xatosi: {str(e)}")
            return None


# Global instance
google_oauth_client = GoogleOAuthClient()
