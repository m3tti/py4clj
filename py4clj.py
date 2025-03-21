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


def execute(cmd):
    res = eval(cmd[0])
    debug(cmd[0])
    debug(res)
    return res


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
                                    "vars": [{"name": "execute!"},
                                             {"name": "wurst"}]}]}
            )
        elif op == "invoke":
            var = msg["var"]
            id = msg["id"]
            args = json.loads(msg["args"])
            debug(args)

            if var == "pod.m3tti.py4clj/execute!":
                result = execute(args)

            if var == "pod.m3tti.py4clj/wurst":
                result = {"echo":"wurst123"}


            value = json.dumps(result)
            debug("value", value)

            write({"value": value, "id": id, "status": ["done"]})

if __name__ == "__main__":
    main()
