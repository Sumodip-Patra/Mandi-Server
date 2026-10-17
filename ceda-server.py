import os
from dotenv import load_dotenv
import httpx
from mcp.server.mcpserver import MCPServer
import logging

logging.basicConfig(level=logging.INFO)
log= logging.getLogger("ceda-server")

load_dotenv()
URL= "https://api.ceda.ashoka.edu.in/v1"
API_KEY= os.getenv("CEDA_API_KEY")

async def ceda_client(endpoint: str,params:dict | None = None) -> dict| list:
    """ "Call the CEDA API and return its JSON response"""
    if not API_KEY:
        raise ValueError("CEDA_API_KEY is not set in the environment variables.")

    header= {"Authorization": f"Bearer {API_KEY}",
                "content-type": "application/json"}

    try:
        async with httpx.AsyncClient(timeout=20) as client:
            response = await client.get(
                f"{URL}/{endpoint.lstrip('/')}",
                headers=header,
                params=params
            )
            response.raise_for_status()  # Raise an error for bad responses
            return response.json()
    except httpx.HTTPStatusError as e:
        return {"error": f"HTTP error occurred: {e.response.status_code} - {e.response.text}"}

    except httpx.TimeoutException:
        return {"error": "Request timed out. Please try again later."}

    except RuntimeError as e:
        return {"error": f"Runtime error occurred: {str(e)}"}

    except Exception as e:
        return {"error": f"An unexpected error occurred: {str(e)}"}


#mcp
mcp= MCPServer('ceda-client')

@mcp.tool()
async def get_cities()-> dict| list:
    """get the list of cites"""
    return await ceda_client("agmarknet/geographies")

@mcp.tool()
async def get_commodity()-> dict| list:
    """get the list of commodities"""
    return await ceda_client("agmarknet/commodities")

@mcp.tool()
async def get_mandi(census_state_id:int,census_district_id:int)-> dict | list:
    """get the list of mandis by state"""
    return await ceda_client("agmarknet/markets",params={"state":census_state_id,"district":census_district_id})

@mcp.tool()
async def get_price(commodity_id:int, census_state_id: int, census_district_id: int,from_date: str, to_date:str)-> dict | list:
    """get the list of prices by commodity, state and mandi"""
    return await ceda_client(
        "agmarknet/prices",
        params={"commodity":commodity_id,"state":census_state_id,"market":census_district_id,"from_date":from_date,"to_date":to_date}
    )


if __name__ == "__main__":
  

    log.info("Starting CEDA MCP server at http://127.0.0.1:8000/mcp")
    mcp.run(transport="streamable-http",host="127.0.0.1",port=8000)