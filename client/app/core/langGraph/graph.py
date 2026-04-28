from langgraph.graph import StateGraph, END
from langchain_core.messages import ToolMessage
from .state import PokedexState
from ...ui.formatter import print_system_log

def create_pokedex_graph(model, tools):
    # Map for easy tool lookups and validation
    tool_map = {tool.name: tool for tool in tools}
    model_with_tools = model.bind_tools(tools)

    async def call_model(state: PokedexState):
        """Node: LLM processes history."""
        print_system_log("Agent is analyzing request...")
        response = await model_with_tools.ainvoke(state["messages"])
        return {"messages": [response]}

    async def execute_tools(state: PokedexState):
        """Node: Executes MCP tools with UI logging and hallucination guard."""
        last_message = state["messages"][-1]
        tool_outputs = []

        for tool_call in last_message.tool_calls:
            tool_name = tool_call["name"]
            
            # --- Hallucination Guard & Logging ---
            if tool_name not in tool_map:
                print_system_log(f"Hallucination Detected: {tool_name}")
                error_msg = f"Error: Tool '{tool_name}' does not exist."
                tool_outputs.append(ToolMessage(content=error_msg, tool_call_id=tool_call["id"]))
                continue

            # Log actual Pokedex access
            print_system_log(f"Accessing Pokedex: {tool_name}")
            
            # Execution
            result = await tool_map[tool_name].ainvoke(tool_call["args"])
            tool_outputs.append(ToolMessage(content=str(result), tool_call_id=tool_call["id"]))

        return {"messages": tool_outputs}

    def route_after_agent(state: PokedexState):
        """Routing logic."""
        last_message = state["messages"][-1]
        if last_message.tool_calls:
            return "tools"
        return END

    # Graph Construction
    workflow = StateGraph(PokedexState)
    workflow.add_node("agent", call_model)
    workflow.add_node("tools", execute_tools)

    workflow.set_entry_point("agent")

    # Explicit mapping tells the visualizer (and the engine) all possible routes
    workflow.add_conditional_edges(
        "agent", 
        route_after_agent, 
        {
            "tools": "tools",  # If function returns "tools", go to tools node
            END: END           # If function returns END, finish execution
        }
    )

    workflow.add_edge("tools", "agent")
    return workflow.compile()