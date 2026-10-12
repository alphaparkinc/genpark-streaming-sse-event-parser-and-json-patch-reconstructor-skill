# genpark-streaming-sse-event-parser-and-json-patch-reconstructor-skill

Parses streaming Server-Sent Events (SSE) deltas and reconstructs structured JSON tool arguments, thought blocks, and multi-part content streams in real time.

100% Python Standard Library implementation with zero external dependencies.

## Key Capabilities
- **W3C Compliant SSE Frame Parsing**: Accurately handles multi-line `event:`, `data:`, and `id:` boundaries across streaming chunk buffers.
- **Incremental Tool Call Reconstruction**: Stitches in-flight streaming JSON parameter fragments into validated dictionary objects with speculative repair.
- **Thought Stream Disassembly**: Separates internal chain-of-thought blocks from structured tool invocation arguments in real-time pipelines.
- **Zero Dependencies**: Pure standard library execution with sub-millisecond parsing latency.

## Architecture

```
[Raw SSE Network Stream]
           │
           ▼
┌──────────────────────────────────────────────┐
│  StreamingSSEParser                          │
│  ├─ Frame Boundary Normalizer (event/data/id)│
│  ├─ JSON Delta Reconstructor                 │
│  └─ In-Flight Speculative Synthesizer        │
└──────────────────────────────────────────────┘
           │
    ┌──────┴────────────────────────┐
    ▼                               ▼
[Parsed Discrete Events]     [Validated Tool Arguments]
```

## MCP Server Integration

Run standard MCP stdio server:
```bash
python mcp_server.py
```

Exposed Tools:
- `parse_sse_events`: Parses raw SSE chunk lines into discrete structured event objects.
- `reconstruct_tool_arguments`: Stitches JSON fragments with spec-compliant validation and in-flight repair.

## Quickstart

```python
from client import StreamingSSEParser

# 1. Parse raw SSE frame
raw_sse = "event: delta\ndata: {\"query\": \"search genpark\"}\n\n"
events = StreamingSSEParser.parse_sse_lines(raw_sse)
print(events)

# 2. Reconstruct streaming JSON arguments
chunks = ['{"tool": ', '"weather", ', '"city": "Tokyo"}']
reconstructed = StreamingSSEParser.reconstruct_streaming_tool_call(chunks)
print(reconstructed["parsed_json"])
```

---

## GenPark Ecosystem

- **Official Website**: [https://www.genpark.ai](https://www.genpark.ai)
- **LinkedIn Page**: [https://www.linkedin.com/company/92955550](https://www.linkedin.com/company/92955550)
