import os
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
async def get_mandis(state:str):
    """get the mandis by state"""
    url= f"{URL}/agmarknet/markets?state={state}"
    response = requests.get(url,headers=headers)
    if response.status_code == 200:
        return response.json()  
    else:
        return {"error": f"Failed to fetch mandis for state {state}. Status code: {response.status_code}"}

@mcp.tool()
async def get_commodity_prices(commodity:str, state="Maharashtra",mandi:str=""):
    """get the commodity prices"""
    url= f"{URL}/agmarknet/prices?commodity={commodity}&state={state}&market={mandi}"
    response = requests.get(url,headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Failed to fetch prices for commodity {commodity} in state {state} and mandi {mandi}. Status code: {response.status_code}"}    



if __name__ == "__main__":
    import asyncio
    async def main():
        commodities= await get_commodities()
        print("Commodities:", commodities)

        states= await get_states()
        print("States:", states)

        mandis= await get_mandis("Maharashtra")
        print("Mandis in Maharashtra:", mandis)

        prices= await get_commodity_prices("Wheat", "Maharashtra", "Pune")
        print("Prices for Wheat in Maharashtra, Pune:", prices)

    asyncio.run(main())   