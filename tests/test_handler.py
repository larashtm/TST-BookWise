"""
Test for Vercel handler
"""
import pytest
from main import app, handler


class TestVercelHandler:
    """Test suite for Vercel handler"""
    
    def test_handler_is_app(self):
        """Test that handler is the FastAPI app"""
        assert handler == app
    
    def test_handler_has_routes(self):
        """Test that handler has routes registered"""
        assert len(handler.routes) > 0
    
    def test_handler_callable(self):
        """Test that handler is callable (ASGI app)"""
        assert callable(handler)


class TestFaviconEndpoints:
    """Test suite for favicon endpoints"""
    
    def test_favicon_ico(self):
        """Test favicon.ico returns 204"""
        from fastapi.testclient import TestClient
        client = TestClient(app)
        response = client.get("/favicon.ico")
        assert response.status_code == 204
    
    def test_favicon_png(self):
        """Test favicon.png returns 204"""
        from fastapi.testclient import TestClient
        client = TestClient(app)
        response = client.get("/favicon.png")
        assert response.status_code == 204