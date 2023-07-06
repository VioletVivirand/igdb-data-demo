import httpx
import asyncio
from functools import partial
import aiometer

class IGDBWrapper:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
    
    def _fetch(self, request):
        endpoint = request["endpoint"]
        body = request["body"]
        headers = {
            "Client-ID": self.client_id,
            "Authorization": f"Bearer {self.__access_token}",
            "Accept": "application/json",
        }

        with httpx.Client(base_url="https://api.igdb.com/v4") as client:
            response = client.post(url=f"/{endpoint}", data=body, headers=headers)
        
        return response.json()
    

    async def _fetch_async(self, request):
        endpoint = request["endpoint"]
        body = request["body"]
        headers = {
            "Client-ID": self.client_id,
            "Authorization": f"Bearer {self.__access_token}",
            "Accept": "application/json",
        }

        async with httpx.AsyncClient(base_url="https://api.igdb.com/v4") as client:
            response = await client.post(url=f"/{endpoint}", data=body, headers=headers)

        return response.json()
    
    def get_token(self):
        body = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "client_credentials",
        }
        response = httpx.post(url="https://id.twitch.tv/oauth2/token", data=body)
        self.__access_token = response.json()["access_token"]
        return response.json()
    
    async def get_games(self, query):
        # Get counts
        request_count = {
            "endpoint": "games/count",
            "body": query,
        }

        response_count = self._fetch(request=request_count)
        count = response_count["count"]

        # Get games
        # [NOTE]
        # (1) 假設 Count（遊戲數量）= 1735，無法被 500 整除，
        # 查詢的 Body 要加上 "offset x;", x = 0, 500, 1000, 1500
        # 想像 pages = 1735 // 500 + 1 = 4，用 List compregension 產生 0, 500, 1000, 1500
        # (2) 假設 Count（遊戲數量）= 1500，可以 500 整除，
        # 查詢的 Body 要加上 "offset x;", x = 0, 500, 1000
        # 想像 pages = 1500 / 500 = 3，用 List compregension 產生 0, 500, 1000
        if count > 500:
            # Async fetch
            if count % 500:
                pages = count // 500 + 1
            else:
                pages = count / 500
            
            bodies = [query + f"offset {500*page};" for page in range(pages)]
            requests = [{"endpoint": "games", "body": body} for body in bodies]
            
            # Method 1
            result = []
            async with aiometer.amap(
                self._fetch_async,
                requests,
                max_per_second=4,  # Limit request rate to not overload the server.
            ) as responses:
                async for response in responses:
                    result += response
            
            # Method 2
            # responses = await aiometer.run_all([partial(self._fetch_async, request) for request in requests], max_per_second=4)
            # result = []
            # for response in responses:
            #     result += response
            
            return result

        else:
            # Sync fetch
            request = {"endpoint": "games", "body": query}
            response = self._fetch(request=request)

            return response
