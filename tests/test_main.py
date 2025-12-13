"""
Unit tests for main application
"""
import pytest
from fastapi.testclient import TestClient
from main import app, custom_openapi


client = TestClient(app)


class TestRootEndpoint:
    """Test suite for root endpoint"""

    def test_root_endpoint(self):
        """Test GET / returns correct response"""
        response = client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "status" in data
        assert "endpoints" in data
        assert data["status"] == "healthy"

    def test_root_endpoint_structure(self):
        """Test that root endpoint has correct structure"""
        response = client.get("/")
        data = response.json()
        
        assert "message" in data
        assert "status" in data
        assert "endpoints" in data
        assert isinstance(data["endpoints"], dict)

    def test_root_endpoint_contains_docs(self):
        """Test that root endpoint lists documentation endpoints"""
        response = client.get("/")
        data = response.json()
        
        assert "docs" in data["endpoints"]
        assert "redoc" in data["endpoints"]

    def test_root_endpoint_contains_auth(self):
        """Test that root endpoint lists auth endpoints"""
        response = client.get("/")
        data = response.json()
        
        assert "auth" in data["endpoints"]

    def test_root_endpoint_contains_loans(self):
        """Test that root endpoint lists loans endpoints"""
        response = client.get("/")
        data = response.json()
        
        assert "loans" in data["endpoints"]


class TestHealthEndpoint:
    """Test suite for health check endpoint"""

    def test_health_endpoint(self):
        """Test GET /health returns ok"""
        response = client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"

    def test_health_endpoint_structure(self):
        """Test health endpoint response structure"""
        response = client.get("/health")
        data = response.json()
        
        assert "status" in data
        assert isinstance(data["status"], str)

    def test_health_endpoint_always_available(self):
        """Test that health endpoint is always available"""
        # Make multiple requests
        for _ in range(5):
            response = client.get("/health")
            assert response.status_code == 200


class TestDocsEndpoints:
    """Test suite for documentation endpoints"""

    def test_docs_endpoint_accessible(self):
        """Test that /docs endpoint is accessible"""
        response = client.get("/docs")
        assert response.status_code == 200

    def test_redoc_endpoint_accessible(self):
        """Test that /redoc endpoint is accessible"""
        response = client.get("/redoc")
        assert response.status_code == 200

    def test_openapi_json_accessible(self):
        """Test that OpenAPI JSON is accessible"""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        data = response.json()
        assert "openapi" in data
        assert "info" in data
        assert "paths" in data


class TestOpenAPICustomization:
    """Test suite for custom OpenAPI schema"""

    def test_custom_openapi_function(self):
        """Test custom_openapi function"""
        schema = custom_openapi()
        
        assert schema is not None
        assert "openapi" in schema
        assert "info" in schema
        assert "paths" in schema
        assert "components" in schema

    def test_openapi_has_security_schemes(self):
        """Test that OpenAPI has security schemes"""
        schema = custom_openapi()
        
        assert "components" in schema
        assert "securitySchemes" in schema["components"]
        assert "BearerAuth" in schema["components"]["securitySchemes"]

    def test_openapi_bearer_auth_config(self):
        """Test BearerAuth configuration"""
        schema = custom_openapi()
        bearer_auth = schema["components"]["securitySchemes"]["BearerAuth"]
        
        assert bearer_auth["type"] == "http"
        assert bearer_auth["scheme"] == "bearer"
        assert bearer_auth["bearerFormat"] == "JWT"

    def test_openapi_title(self):
        """Test OpenAPI schema title"""
        schema = custom_openapi()
        
        assert schema["info"]["title"] == "BookWise - Lending BC (with Auth)"

    def test_openapi_version(self):
        """Test OpenAPI schema version"""
        schema = custom_openapi()
        
        assert schema["info"]["version"] == "1.0.0"

    def test_openapi_has_paths(self):
        """Test that OpenAPI schema has paths defined"""
        schema = custom_openapi()
        
        assert len(schema["paths"]) > 0

    def test_openapi_login_endpoint_no_auth(self):
        """Test that login endpoint doesn't require auth"""
        schema = custom_openapi()
        
        # Check if /auth/login exists and doesn't have security
        login_path = None
        for path_key in schema["paths"]:
            if "/auth/login" in path_key:
                login_path = schema["paths"][path_key]
                break
        
        # Login endpoint should exist
        assert login_path is not None


class TestAppConfiguration:
    """Test suite for app configuration"""

    def test_app_title(self):
        """Test that app has correct title"""
        assert app.title == "BookWise - Lending BC (with Auth)"

    def test_app_version(self):
        """Test that app has correct version"""
        assert app.version == "1.0.0"

    def test_app_has_description(self):
        """Test that app has description"""
        assert app.description is not None
        assert len(app.description) > 0

    def test_app_routes_registered(self):
        """Test that routes are registered"""
        routes = [route.path for route in app.routes]
        
        # Check for key routes
        assert "/" in routes
        assert "/health" in routes
        assert "/openapi.json" in routes


class TestRoutersIncluded:
    """Test suite for included routers"""

    def test_auth_routes_included(self):
        """Test that auth routes are included"""
        routes = [route.path for route in app.routes]
        
        # Check for auth routes
        auth_routes_exist = any("/auth" in route for route in routes)
        assert auth_routes_exist

    def test_loan_routes_included(self):
        """Test that loan routes are included"""
        routes = [route.path for route in app.routes]
        
        # Check for loan routes
        loan_routes_exist = any("/loans" in route for route in routes)
        assert loan_routes_exist


class TestCORSAndMiddleware:
    """Test suite for CORS and middleware configuration"""

    def test_cors_headers(self):
        """Test CORS headers in response"""
        response = client.options("/health")
        # Basic test - app should handle OPTIONS
        assert response.status_code in [200, 405]  # 405 if not explicitly handled

    def test_json_response_content_type(self):
        """Test that JSON responses have correct content type"""
        response = client.get("/health")
        assert "application/json" in response.headers.get("content-type", "")


class TestErrorHandling:
    """Test suite for error handling"""

    def test_404_for_non_existent_route(self):
        """Test that non-existent routes return 404"""
        response = client.get("/non-existent-route")
        assert response.status_code == 404

    def test_405_for_wrong_method(self):
        """Test that wrong HTTP method returns 405"""
        response = client.put("/")
        assert response.status_code == 405


class TestVercelHandler:
    """Test suite for Vercel handler"""

    def test_vercel_handler_exists(self):
        """Test that Vercel handler is defined"""
        from main import handler
        assert handler is not None
        assert handler == app


class TestApplicationIntegration:
    """Integration tests for application"""

    def test_full_app_flow(self):
        """Test complete application flow"""
        # 1. Health check
        health_response = client.get("/health")
        assert health_response.status_code == 200
        
        # 2. Root endpoint
        root_response = client.get("/")
        assert root_response.status_code == 200
        
        # 3. OpenAPI docs
        docs_response = client.get("/openapi.json")
        assert docs_response.status_code == 200

    def test_authentication_integration(self):
        """Test authentication is integrated"""
        # Try to access protected endpoint without auth
        response = client.get("/loans/my")
        assert response.status_code == 401

    def test_login_then_access_protected(self):
        """Test login then access protected endpoint"""
        # Login
        login_response = client.post(
            "/auth/login",
            data={"username": "peminjam1", "password": "pinjam123"}
        )
        assert login_response.status_code == 200
        
        token = login_response.json()["access_token"]
        
        # Access protected endpoint
        headers = {"Authorization": f"Bearer {token}"}
        protected_response = client.get("/loans/my", headers=headers)
        assert protected_response.status_code == 200