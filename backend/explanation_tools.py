"""
Explanation tools: lightweight statistical summaries of query results.

The LLM provides the conversational explanation; this tool gives the
model (and the user) quick quantitative context about the data.
"""
from collections import Counter


def _numeric_columns(data):
    """Return the names of columns that look numeric."""
    numeric = set()
    for row in data:
        for key, value in row.items():
            if isinstance(value, (int, float)) and not isinstance(value, bool):
                numeric.add(key)
        if len(numeric) == len(row):
            break
    return sorted(numeric)


def explain_data(data, top_n=5):
    """
    Build a short statistical explanation of query results.

    Args:
        data: list of dictionaries (query results).
        top_n: how many top values to list for categorical columns.

    Returns:
        Dictionary with row counts, column stats and a ready-made
        natural-language summary.
    """
    if not data:
        return {
            "success": False,
            "explanation": "No data was found.",
        }

    try:
        rows = list(data)
        columns = list(rows[0].keys())
        numeric = _numeric_columns(rows)

        info = {
            "row_count": len(rows),
            "columns": columns,
            "numeric_columns": numeric,
            "stats": {},
            "explanation": "",
        }

        for column in numeric:
            values = [row[column] for row in rows
                      if isinstance(row.get(column), (int, float))]
            if not values:
                continue
            info["stats"][column] = {
                "min": min(values),
                "max": max(values),
                "avg": round(sum(values) / len(values), 2),
                "sum": round(sum(values), 2),
            }

        categorical = [c for c in columns if c not in numeric]
        if categorical:
            column = categorical[0]
            counts = Counter(
                str(row[column]) for row in rows if row.get(column) is not None
            )
            info["top_values"] = {
                column: counts.most_common(top_n)
            }

        parts = [
            f"The query returned {len(rows)} record(s)"
            f" with fields: {', '.join(columns)}."
        ]
        for column, stats in info["stats"].items():
            parts.append(
                f"'{column}' ranges from {stats['min']} to {stats['max']}"
                f" (average {stats['avg']}, total {stats['sum']})."
            )
        if "top_values" in info:
            for column, common in info["top_values"].items():
                listing = ", ".join(
                    f"{value} ({count})" for value, count in common[:3]
                )
                parts.append(
                    f"Most common values of '{column}': {listing}."
                )

        info["explanation"] = " ".join(parts)
        info["success"] = True
        return info

    except Exception as error:  # noqa: BLE001
        return {"success": False, "error": str(error)}


if __name__ == "__main__":
    print(explain_data([
        {"city": "London", "revenue": 100},
        {"city": "Paris", "revenue": 200},
    ]))