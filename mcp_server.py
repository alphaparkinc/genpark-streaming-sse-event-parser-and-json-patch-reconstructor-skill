"""MCP server for Streaming SSE Event Parser & JSON Patch Reconstructor."""
import sys
import json
from client import StreamingSSEParser


def handle_request(req):
    method = req.get("method")
    if method == "tools/list":
        return {
            "tools": [
                {
                    "name": "parse_sse_events",
                    "description": "Parses raw streaming SSE line chunks into discrete structured events (event, data, id)",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "sse_text": {"type": "string", "description": "Raw SSE stream text payload"}
                        },
                        "required": ["sse_text"],
                    },
                },
                {
                    "name": "reconstruct_tool_arguments",
                    "description": "Reconstructs streamed JSON tool call parameter fragments and performs in-flight speculative repair",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "argument_chunks": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Array of string deltas received from streaming LLM output",
                            }
                        },
                        "required": ["argument_chunks"],
                    },
                },
            ]
        }
    elif method == "tools/call":
        params = req.get("params", {})
        tool_name = params.get("name")
        args = params.get("arguments", {})
        if tool_name == "parse_sse_events":
            res = StreamingSSEParser.parse_sse_lines(args.get("sse_text", ""))
            return {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
        elif tool_name == "reconstruct_tool_arguments":
            res = StreamingSSEParser.reconstruct_streaming_tool_call(args.get("argument_chunks", []))
            return {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
    return {"error": "Method not found"}


if __name__ == "__main__":
    for line in sys.stdin:
        if line.strip():
            print(json.dumps(handle_request(json.loads(line))))
            sys.stdout.flush()
