"""Streaming SSE Event Parser & JSON Patch Reconstructor.
100% Python Standard Library.
"""

from typing import List, Dict, Any, Generator, Tuple
import json


class StreamingSSEParser:
    """Parses real-time Server-Sent Events (SSE) data streams and incrementally
    reconstructs JSON tool call arguments, thought reasoning deltas, and structured payloads."""

    @classmethod
    def parse_sse_lines(cls, sse_chunk: str) -> List[Dict[str, str]]:
        """Parses raw chunk of SSE text into discrete event objects containing 'event', 'data', 'id'."""
        events = []
        current_event = {}
        for line in sse_chunk.splitlines():
            line = line.strip()
            if not line:
                if current_event:
                    events.append(current_event)
                    current_event = {}
                continue
            if line.startswith("event:"):
                current_event["event"] = line[len("event:") :].strip()
            elif line.startswith("data:"):
                data_val = line[len("data:") :].strip()
                current_event["data"] = (
                    current_event.get("data", "") + ("\n" if "data" in current_event else "") + data_val
                )
            elif line.startswith("id:"):
                current_event["id"] = line[len("id:") :].strip()

        if current_event:
            events.append(current_event)
        return events

    @classmethod
    def reconstruct_streaming_tool_call(
        cls, argument_chunks: List[str]
    ) -> Dict[str, Any]:
        """Progressively stitches JSON argument fragments streamed across multiple deltas
        and attempts speculative lenient repair when streams are in-flight."""
        accumulated_text = "".join(argument_chunks)
        try:
            parsed = json.loads(accumulated_text)
            return {
                "complete": True,
                "raw_text": accumulated_text,
                "parsed_json": parsed,
                "error": None,
            }
        except json.JSONDecodeError as exc:
            # Attempt basic auto-close repair for in-flight inspection
            repaired_text = accumulated_text.strip()
            if repaired_text.startswith("{") and not repaired_text.endswith("}"):
                repaired_text += "}"
            elif repaired_text.startswith("[") and not repaired_text.endswith("]"):
                repaired_text += "]"

            try:
                speculative_parsed = json.loads(repaired_text)
                return {
                    "complete": False,
                    "raw_text": accumulated_text,
                    "speculative_json": speculative_parsed,
                    "error": str(exc),
                }
            except Exception:
                return {
                    "complete": False,
                    "raw_text": accumulated_text,
                    "speculative_json": None,
                    "error": str(exc),
                }
