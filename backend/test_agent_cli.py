import json
import sys
sys.path.insert(0, ".")

from agent import stream_chat

question = sys.argv[1] if len(sys.argv) > 1 else "List the top 5 products by revenue and show a bar chart"
print("QUESTION:", question)
print("=" * 60)
for item in stream_chat([{"role": "user", "content": question}]):
    t = item["type"]
    if t == "delta":
        print(item["text"], end="", flush=True)
    elif t == "sql":
        print(f"\n[SQL] {item['sql']}", flush=True)
    elif t == "tool":
        print(f"\n[TOOL] {item['name']} ...", flush=True)
    elif t == "tool_result":
        print(f"\n[RESULT] {item.get('summary','')} | keys: {list(item.keys())}", flush=True)
    elif t == "error":
        print("\n[ERROR]", item["message"], flush=True)
    else:
        print(f"\n[{t.upper()}] {json.dumps(item)[:120]}", flush=True)
print("\n" + "=" * 60)