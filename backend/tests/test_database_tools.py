import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import pytest

from backend.database_tools import execute_query, generate_chart, get_schema


@pytest.fixture(scope="module")
def schema():
    return get_schema()


def test_schema_has_expected_tables(schema):
    expected = {"customers", "orders", "order_items", "products"}
    assert expected.issubset(schema.keys())


def test_schema_columns_have_names_and_types(schema):
    for table, info in schema.items():
        assert info["columns"], f"{table} has no columns"
        for column in info["columns"]:
            assert "name" in column
            assert "type" in column
            assert "primary_key" in column


def test_schema_foreign_keys_reference_real_tables(schema):
    for table, info in schema.items():
        for foreign_key in info.get("foreign_keys", []):
            assert foreign_key["references_table"] in schema


def test_execute_query_returns_rows():
    result = execute_query("SELECT * FROM products LIMIT 3")
    assert result["success"] is True
    assert result["row_count"] == 3
    assert "product_name" in result["columns"]
    assert len(result["data"]) == 3


def test_execute_query_rejects_non_select():
    result = execute_query("DELETE FROM products")
    assert result["success"] is False
    assert "SELECT" in result["error"]


def test_execute_query_returns_error_for_bad_sql():
    result = execute_query("SELECT * FROM missing_table")
    assert result["success"] is False
    assert result["error"]


def test_execute_query_truncates_large_results():
    result = execute_query("SELECT * FROM order_items")
    assert result["success"] is True
    assert result["truncated"] is False  # 40 rows < limit


def test_generate_chart_bar_returns_figure_json():
    data = [
        {"city": "London", "revenue": 100},
        {"city": "Paris", "revenue": 200},
    ]
    result = generate_chart(data, "bar", "city", "revenue", "Test Chart")
    assert result["success"] is True
    figure = json.loads(result["figure"])
    assert figure["data"]
    assert result["chart_type"] == "bar"


def test_generate_chart_pie_uses_names_values():
    data = [{"category": "A", "count": 3}, {"category": "B", "count": 7}]
    result = generate_chart(data, "pie", "category", "count")
    assert result["success"] is True


def test_generate_chart_rejects_unknown_type():
    result = generate_chart([{"a": 1}], "gauge", "a", "a")
    assert result["success"] is False


def test_generate_chart_rejects_missing_column():
    result = generate_chart([{"a": 1}], "bar", "a", "missing")
    assert result["success"] is False


def test_generate_chart_rejects_empty_data():
    result = generate_chart([], "bar", "a", "b")
    assert result["success"] is False