import asyncio
from langchain_core.messages import HumanMessage, ToolMessage, SystemMessage
from ..core.mcp_client import PokedexMCPClient, ClientSession
from ..core.factory import get_model
from ..ui.formatter import print_tools_status, print_header, print_user_prompt, print_system_log, print_assistant

async def run_terminal_chat():
    mcp_helper = PokedexMCPClient()
    model = get_model()
    
    state = {
        "messages": [
            SystemMessage(
                content=(
                    "You are a Pokemon assistant with access to MCP tools.\n"
                    "Only call a tool when the user asks for specific Pokemon or Pokemon move data.\n"
                    "For greetings, introductions, or general conversation, respond directly."
                )
            )
        ]
    }
    
    async with mcp_helper.get_context() as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            tools = await mcp_helper.fetch_tools(session)
            print_tools_status(tools)
            
            model_with_tools = model.bind_tools(tools, tool_choice="auto")
            print_header()
            
            while True:
                # Running input in a separate thread to avoid blocking the event loop
                user_input = await asyncio.to_thread(input, print_user_prompt())
                
                if user_input.lower() in ["quit", "exit", "q"]: 
                    break
                
                state["messages"].append(HumanMessage(content=user_input))

                response = await model_with_tools.ainvoke(state["messages"])
                state["messages"].append(response)

                if response.tool_calls:
                    for tool_call in response.tool_calls:
                        print_system_log(f"Accessing Pokedex: {tool_call['name']}")
                        tool = next(t for t in tools if t.name == tool_call["name"])
                        result = await tool.ainvoke(tool_call["args"])
                        state["messages"].append(ToolMessage(content=str(result), tool_call_id=tool_call["id"]))
                    
                    final_response = await model_with_tools.ainvoke(state["messages"])
                    print_assistant(final_response)
                    state["messages"].append(final_response)
                else:
                    print_assistant(response)