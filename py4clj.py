#!/usr/bin/env python3

import json
import sys

from bcoding import bencode, bdecode


def read():
    return dict(bdecode(sys.stdin.buffer))


def write(obj):
    sys.stdout.buffer.write(bencode(obj))
    sys.stdout.flush()


def debug(*msg):
    with open("/tmp/debug.log", "a") as f:
        f.write(str(msg) + "\n")


def main():
    while True:
        msg = read()
        debug("msg", msg)

        op = msg["op"]

        if op == "describe":
            write(
                {
                    "format": "json",
                    "namespaces": [{"name": "pod.m3tti.py4clj",
                                    "vars": [{"name": "exec!"},
                                             {"name": "eval!"}]}]}
            )
        elif op == "invoke":
            var = msg["var"]
            id = msg["id"]
            args = json.loads(msg["args"])
            debug(args)

            if var == "pod.m3tti.py4clj/exec!":
                exec(args[0])
                result = True

            if var == "pod.m3tti.py4clj/eval!":
                result = eval(args[0])

            debug(result)
            value = json.dumps(result)
            debug("value", value)

            write({"value": value, "id": id, "status": ["done"]})

if __name__ == "__main__":
    main()
