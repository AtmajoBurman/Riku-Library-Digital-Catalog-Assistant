import os
import secrets
import logging

# Retrieve secret key from environment or fallback to a cryptographically secure random key.
# TODO(security): Ensure JWT_SECRET_KEY is configured in production environment variables.
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
if not SECRET_KEY:
    logging.warning("JWT_SECRET_KEY not set in environment. Generating an ephemeral secret key for this session.")
    SECRET_KEY = secrets.token_hex(32)

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
