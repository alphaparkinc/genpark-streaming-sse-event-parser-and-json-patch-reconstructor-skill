"""Example usage for Streaming SSE Parser."""
from client import StreamingSSEParser

if __name__ == "__main__":
    raw_sse = "event: message\ndata: {\"tool\": \"bash\"}\n\nevent: message\ndata: {\"tool\": \"python\"}\n\n"
    events = StreamingSSEParser.parse_sse_lines(raw_sse)
    print("Parsed SSE Events:", events)

    chunks = ['{"query": ', '"search for ', 'genpark skills"}']
    reconstructed = StreamingSSEParser.reconstruct_streaming_tool_call(chunks)
    print("Reconstructed Tool Call:", reconstructed)
