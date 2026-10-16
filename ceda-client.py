import os
from urllib import response
import requests 
from dotenv import load_dotenv #type : ignore
load_dotenv()
from mcp.server.mcpserver import MCPServer
mcp= MCPServer("ceda-client")
API_KEY= os.getenv("CEDA_API_KEY")

URL= "https://api.ceda.ashoka.edu.in/v1"

headers= {"Authorization": f"Bearer {API_KEY}",
           "content-type": "application/json"}
@mcp.tool()
async def get_commodities():
    """ get the commodities"""
    url= f"{URL}/agmarknet/commodities"
    response = requests.get(url,headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Failed to fetch commodities. Status code: {response.status_code}"}

@mcp.tool()
async def get_states():
    """Get the states"""    
    url= f"{URL}/agmarknet/geographies"
    response = requests.get(url,headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Failed to fetch states. Status code: {response.status_code}"}

@mcp.tool()
async def get_mandis(state_id:int):
    """get the mandis by state"""
    url= f"{URL}/agmarknet/markets?state={state_id}"
    response = requests.get(url,headers=headers)
    if response.status_code == 200:
        return response.json()  
    else:
        return {"error": f"Failed to fetch mandis for state {state_id}. Status code: {response.status_code}"}

@mcp.tool()
async def get_commodity_prices(commodity_id:int, state_id:int,mandi_id:int):
    """get the commodity prices"""
    url= f"{URL}/agmarknet/prices?commodity={commodity_id}&state={state_id}&market={mandi_id}"
    response = requests.get(url,headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Failed to fetch prices for commodity {commodity_id} in state {state_id} and mandi {mandi_id}. Status code: {response.status_code}"}    



if __name__ == "__main__":
    import asyncio
    async def main():
        commodities= await get_commodities()
       # print("Commodities:", commodities)

        states= await get_states()
        print("States:", states)

        mandis= await get_mandis(27)
        #print("Mandis in Maharashtra:", mandis)

        prices= await get_commodity_prices(1, 27, 520)
        print("Prices for Wheat in Maharashtra, Pune:", prices)

    asyncio.run(main())   