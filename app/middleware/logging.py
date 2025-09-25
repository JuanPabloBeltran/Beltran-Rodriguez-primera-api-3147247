# Logging genérico de performance
import logging
import time
from fastapi import Request

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("performance")

async def log_request(request: Request):
	start_time = time.time()
	response = await request.app(request.scope, request.receive, request.send)
	process_time = time.time() - start_time
	logger.info(f"{request.method} {request.url.path} - {process_time:.4f}s")
	return response
