import os
from datetime import datetime

def save_graph_diagram(app):

    # Path logic to ensure logs go to cleint/graph/
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    GRAPH_DIR = os.path.join(BASE_DIR, "graphs")

    if not os.path.exists(GRAPH_DIR):
        os.makedirs(GRAPH_DIR)

    # Unique filename for each run: graph_20260426_1620.md
    run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    graph_file = os.path.join(GRAPH_DIR, f"graph_{run_id}.md")

    """Extracts the Mermaid representation and saves it to a file."""
    try:
        # Generate the Mermaid string
        mermaid_code = app.get_graph().draw_mermaid()
        
        # Wrap in markdown code blocks for easy viewing in IDEs
        content = f"```mermaid\n{mermaid_code}\n```"
        
        with open(graph_file, "w") as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"Failed to save diagram: {e}")
        return False