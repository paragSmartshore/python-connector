from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    get_remote_address,
    default_limits=["10 per minute"]  # Global rate limit of 10 requests per minute
)

def init_limiter(app):
    limiter.init_app(app)
