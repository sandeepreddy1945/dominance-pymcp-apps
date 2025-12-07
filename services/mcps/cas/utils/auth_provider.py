from pydantic.networks import AnyUrl
from fastmcp.server.auth.providers.introspection import IntrospectionTokenVerifier
from dotenv import load_dotenv
import os
from fastmcp.server.auth.providers.jwt import JWTVerifier

load_dotenv()

verifier = IntrospectionTokenVerifier(
    introspection_url=os.getenv("KEYCLOAK_INTROSPECTION_URL"),
    client_id=os.getenv("KEYCLOAK_CLIENT_ID"),
    client_secret=os.getenv("KEYCLOAK_CLIENT_SECRET"),
    timeout_seconds=60,
)


jwt_verifier = JWTVerifier(
    jwks_uri=os.getenv("KEYCLOAK_JWKS_URI"),
    issuer=os.getenv("KEYCLOAK_ISSUER"),
    audience=os.getenv("KEYCLOAK_AUDIENCE"),
    algorithm="RS256",
)
