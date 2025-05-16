import aiohttp

from frankfurter.exceptions import FrankfurterException
from fastapi import HTTPException


class RestAdapter:
    def __init__(self, hostname: str = 'api.frankfurter.dev', ver: str = 'v1'):
        self.hostname = hostname
        self.ver = ver

    async def get(self, url):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status >= 400:
                        error_text = await response.text()
                        raise HTTPException(status_code=response.status, detail=f"API request failed: {error_text}")
                    return await response.json()
        except aiohttp.ClientConnectionError as e:
            raise HTTPException(status_code=503, detail=f"Could not connect to the external currency service at {url}. Details: {str(e)}")
        
    async def get_currencies(self):
        try:
            url = f"https://{self.hostname}/{self.ver}/currencies"
            return await self.get(url=url)
        except HTTPException as e:
            raise FrankfurterException(f"Failed to get currencies: {str(e)}")

    async def get_currency_rates(self, base_currency: str, target_currency: str):
        try:
            url = f"https://{self.hostname}/{self.ver}/latest?base={base_currency}&symbols={target_currency}"
            return await self.get(url=url)
        except HTTPException as e:
            raise FrankfurterException(f"Failed to get currency rates: {str(e)}")

    async def get_historical_currency_rates(self, date: str, base_currency: str = None, target_currency: str = None):
        try:
            url = f"https://{self.hostname}/{self.ver}/{date}?base={base_currency}&symbols={target_currency}"
            return await self.get(url=url)
        except HTTPException as e:
            raise FrankfurterException(f"Failed to get historical currency rates: {str(e)}")