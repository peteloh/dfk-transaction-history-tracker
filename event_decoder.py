# Reference: //github.com/iamdefinitelyahuman/eth-event.git

import re
from typing import Dict, List
from eth_abi import decode_abi, decode_single
from eth_abi.exceptions import InsufficientDataBytes, NoEntriesFound, NonEmptyPaddingBytes
from eth_hash.auto import keccak
from eth_utils import to_checksum_address
from hexbytes import HexBytes


class ABIError(Exception):
    pass


class EventError(Exception):
    pass


class StructLogError(Exception):
    pass


class UnknownEvent(Exception):
    pass


def get_log_topic(event_abi: Dict) -> str:
    if not isinstance(event_abi, dict):
        raise TypeError("Must be a dictionary of the specific event's ABI")
    if event_abi.get("anonymous"):
        raise ABIError("Anonymous events do not have a topic")

    types = _params(event_abi["inputs"])
    key = f"{event_abi['name']}({','.join(types)})".encode()

    return "0x" + keccak(key).hex()


def get_topic_map(abi: List) -> Dict:
    try:
        events = [i for i in abi if i["type"] == "event" and not i.get("anonymous")]
        return {get_log_topic(i): {"name": i["name"], "inputs": i["inputs"]} for i in events}

    except (KeyError, TypeError):
        raise ABIError("Invalid ABI")


def decode_log(log: Dict, topic_map: Dict) -> Dict:
    if not log["topics"]:
        raise EventError("Cannot decode an anonymous event")

    key = HexBytes(log["topics"][0]).hex()
    if key not in topic_map:
        raise UnknownEvent("Event topic is not present in given ABI")
    abi = topic_map[key]

    try:
        return {
            "name": abi["name"],
            "data": _decode(abi["inputs"], log["topics"][1:], log["data"]),
            "decoded": True,
            "address": to_checksum_address(log["address"]),
        }
    except (KeyError, TypeError):
        raise EventError("Invalid event")

def _params(abi_params: List) -> List:
    types = []
    # regex with 2 capturing groups
    # first group captures whether this is an array tuple
    # second group captures the size if this is a fixed size tuple
    pattern = re.compile(r"tuple(\[(\d*)\])?")
    for i in abi_params:
        tuple_match = pattern.match(i["type"])
        if tuple_match:
            _array, _size = tuple_match.group(1, 2)  # unpack the captured info
            tuple_type_tail = f"[{_size}]" if _array is not None else ""
            types.append(f"({','.join(x for x in _params(i['components']))}){tuple_type_tail}")
            continue
        types.append(i["type"])

    return types

def _decode(inputs: List, topics: List, data: str) -> List:
    indexed_count = len([i for i in inputs if i["indexed"]])

    if indexed_count and not topics:
        # special case - if the ABI has indexed values but the log does not,
        # we should still be able to decode the data
        unindexed_types = inputs

    else:
        if indexed_count < len(topics):
            raise EventError(
                "Event log does not contain enough topics for the given ABI - this"
                " is usually because an event argument is not marked as indexed"
            )
        if indexed_count > len(topics):
            raise EventError(
                "Event log contains more topics than expected for the given ABI - this is"
                " usually because an event argument is incorrectly marked as indexed"
            )
        unindexed_types = [i for i in inputs if not i["indexed"]]

    # decode the unindexed event data
    try:
        unindexed_types = _params(unindexed_types)
    except (KeyError, TypeError):
        raise ABIError("Invalid ABI")

    if unindexed_types and data == "0x":
        length = len(unindexed_types) * 32
        data = f"0x{bytes(length).hex()}"

    try:
        decoded = list(decode_abi(unindexed_types, HexBytes(data)))[::-1]
    except InsufficientDataBytes:
        raise EventError("Event data has insufficient length")
    except NonEmptyPaddingBytes:
        raise EventError("Malformed data field in event log")
    except OverflowError:
        raise EventError("Cannot decode event due to overflow error")

    # decode the indexed event data and create the returned dict
    topics = topics[::-1]
    result = []
    for i in inputs:
        result.append({"name": i["name"], "type": i["type"]})

        if "components" in i:
            result[-1]["components"] = i["components"]

        if topics and i["indexed"]:
            encoded = HexBytes(topics.pop())
            try:
                value = decode_single(i["type"], encoded)
            except (InsufficientDataBytes, NoEntriesFound, OverflowError):
                # an array or other data type that uses multiple slots
                result[-1].update({"value": encoded.hex(), "decoded": False})
                continue
        else:
            value = decoded.pop()

        if isinstance(value, bytes):
            # converting to `HexBytes` first ensures the leading `0x`
            value = HexBytes(value).hex()
        result[-1].update({"value": value, "decoded": True})

    return result


