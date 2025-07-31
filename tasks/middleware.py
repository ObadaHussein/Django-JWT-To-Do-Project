import time
import logging
from django.utils.deprecation import MiddlewareMixin

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('task_requests.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class TaskLoggingMiddleware(MiddlewareMixin):
    """
    Custom middleware to log requests to task-related endpoints.
    Logs request path, method, username, and processing time.
    """
    
    def process_request(self, request):
        if request.path.startswith('/tasks/'):
            request.start_time = time.time()
    
    def process_response(self, request, response):
        if request.path.startswith('/tasks/') and hasattr(request, 'start_time'):
            processing_time = time.time() - request.start_time
            username = request.user.username if request.user.is_authenticated else 'Anonymous'
            
            logger.info(
                f"Path: {request.path} | Method: {request.method} | "
                f"User: {username} | Processing Time: {processing_time:.3f}s"
            )
        
        return response
    