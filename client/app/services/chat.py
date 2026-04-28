import asyncio
from langchain_core.messages import HumanMessage, ToolMessage, SystemMessage
from ..core.mcp_client import PokedexMCPClient, ClientSession
from ..core.factory import get_model
from ..ui.formatter import print_tools_status, print_header, print_user_prompt, print_system_log, print_assistant

async def run_terminal_chat():
    mcp_helper = PokedexMCPClient()
    model = get_model()
    
    initial_state = {
        "messages": [
            SystemMessage(content="You are a Pokedex assistant. Use tools for Pokemon/move data.")
        ],
        "current_pokemon_context": None
    }

    async with mcp_helper.get_context() as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # Fetch tools from FastMCP server
            tools = await mcp_helper.fetch_tools(session)
            print_tools_status(tools)

            # Initialize Graph
            app = create_pokedex_graph(model, tools)
            print_header()

            state = initial_state
            
            while True:
                # Running input in a separate thread to avoid blocking the event loop
                user_input = await asyncio.to_thread(input, print_user_prompt())
                
                if user_input.lower() in ["quit", "exit", "q"]: 
                    break
                
                input_msg = HumanMessage(content=user_input)
                result = await app.ainvoke({"messages": [input_msg]}, config={"configurable": {"thread_id": "1"}})

                # Update local state and display only the final response
                state = result
                print_assistant(state["messages"][-1])