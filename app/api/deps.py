import httpx

async def get_httpx_client():
	"""Функция создания асинхронного клиента"""
	async with httpx.AsyncClient(
			timeout=httpx.Timeout(60.0, connect=5.0),
			limits=httpx.Limits(max_keepalive_connections=5)
	) as client:
		yield client