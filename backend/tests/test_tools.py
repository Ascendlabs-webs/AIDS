import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from diagram_tools import generate_diagram
from explanation_tools import explain_data


class TestDiagrams:
    def test_er_diagram(self):
        result = generate_diagram(
            "er",
            "Schema",
            "erDiagram\nCUSTOMER ||--o{ ORDER : places\n",
        )
        assert result["success"] is True
        assert result["diagram_type"] == "er"
        assert "erDiagram" in result["mermaid_code"]

    def test_flowchart_diagram(self):
        result = generate_diagram(
            "flowchart",
            "Orders",
            "flowchart TD\nA[Order placed] --> B[Packed]\n",
        )
        assert result["success"] is True
        assert "flowchart" in result["mermaid_code"]

    def test_lowercase_keyword_is_normalized(self):
        result = generate_diagram(
            "er",
            "Schema",
            "erdiagram\nCUSTOMER ||--o{ ORDER : places\n",
        )
        assert result["success"] is True
        assert result["mermaid_code"].startswith("erDiagram")

    def test_unknown_type_rejected(self):
        result = generate_diagram("pie", "x", "erDiagram\nx")
        assert result["success"] is False

    def test_wrong_keyword_rejected(self):
        result = generate_diagram(
            "er", "x", "flowchart TD\nA-->B\n"
        )
        assert result["success"] is False

    def test_empty_content_rejected(self):
        result = generate_diagram("er", "x", "   ")
        assert result["success"] is False


class TestExplanations:
    def test_explain_data_counts_and_stats(self):
        data = [
            {"city": "London", "revenue": 100},
            {"city": "Paris", "revenue": 200},
            {"city": "London", "revenue": 300},
        ]
        result = explain_data(data)
        assert result["success"] is True
        assert result["row_count"] == 3
        assert result["stats"]["revenue"]["sum"] == 600
        assert result["stats"]["revenue"]["avg"] == 200.0
        assert "London" in result["top_values"]["city"][0][0]

    def test_explain_data_empty(self):
        result = explain_data([])
        assert result["success"] is False

    def test_explain_data_non_numeric(self):
        result = explain_data([{"name": "apple"}, {"name": "banana"}])
        assert result["success"] is True
        assert result["row_count"] == 2
        assert "name" in result["columns"]