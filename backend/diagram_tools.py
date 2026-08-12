"""
Diagram tools: Mermaid-powered ER diagrams and flowcharts.

The agent generates Mermaid source code; the frontend renders it
client-side with the mermaid.js library and we keep a copy on disk.
"""
import os

DIAGRAM_FOLDER = os.path.join(os.path.dirname(__file__), "diagrams")
os.makedirs(DIAGRAM_FOLDER, exist_ok=True)

SUPPORTED_TYPES = ("er", "flowchart", "mindmap", "graph")


def generate_diagram(diagram_type, title, content):
    """
    Generate a Mermaid diagram (ER, flowchart, mindmap or graph).

    Args:
        diagram_type: 'er', 'flowchart', 'mindmap' or 'graph'.
        title: human-readable title for the diagram.
        content: Mermaid diagram definition.

    Returns:
        Dictionary with 'mermaid_code' for the frontend renderer.
    """
    diagram_type = (diagram_type or "").strip().lower()

    if diagram_type not in SUPPORTED_TYPES:
        return {
            "success": False,
            "error": (
                "Unsupported diagram type. Use er, flowchart, "
                "mindmap or graph."
            ),
        }

    if not content or not str(content).strip():
        return {
            "success": False,
            "error": "Diagram content is empty.",
        }

    # Normalize the first declaration keyword (models often emit
    # lowercase keywords that Mermaid rejects).
    content = str(content).strip()
    lines = content.splitlines()
    first_line = lines[0].strip().strip("`")
    keyword_map = {
        "erdiagram": "erDiagram",
        "flowchart": "flowchart",
        "graph": "graph",
        "mindmap": "mindmap",
    }
    matched_keyword = None
    for keyword, canonical in keyword_map.items():
        if first_line.lower().startswith(keyword):
            matched_keyword = canonical
            break
    expected = {
        "er": "erDiagram",
        "flowchart": "flowchart",
        "graph": "graph",
        "mindmap": "mindmap",
    }[diagram_type]
    if not matched_keyword or matched_keyword != expected:
        return {
            "success": False,
            "error": (
                f"Diagram content must start with "
                f"'{expected}'. Got: '{first_line}'."
            ),
        }

    # Rewrite the first line with the canonical keyword
    lines[0] = matched_keyword + first_line[len(keyword):]
    content = "\n".join(lines)

    safe_name = "".join(
        ch for ch in str(title).lower() if ch.isalnum() or ch in " _-"
    ).strip().replace(" ", "_")[:40] or diagram_type

    filepath = os.path.join(
        DIAGRAM_FOLDER, f"{safe_name}_{diagram_type}.mmd"
    )
    with open(filepath, "w", encoding="utf-8") as file:
        file.write(content)

    return {
        "success": True,
        "diagram_type": diagram_type,
        "title": title,
        "mermaid_code": content,
        "file": filepath,
    }


if __name__ == "__main__":
    print(generate_diagram(
        "er",
        "Test",
        "erDiagram\nCUSTOMER ||--o{ ORDER : places\n",
    ))