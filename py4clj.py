#!/usr/bin/env python3

import json
import sys
import edn_format
import inspect

from bcoding import bencode, bdecode


def read():
    return dict(bdecode(sys.stdin.buffer))


def write(obj):
    sys.stdout.buffer.write(bencode(obj))
    sys.stdout.flush()


def debug(*msg):
    with open("/tmp/debug.log", "a") as f:
        f.write(str(msg) + "\n")


def edn_eval(edn):
    data = edn_format.loads(edn)
    fn = data[edn_format.Keyword('fn')]
    args = data[edn_format.Keyword('args')]
    debug(f"{fn}({args})")
    call = f"{fn}({args})"

    return edn_format.dumps(eval(call))


def json_eval(jo):
    data = json.loads(jo)
    fn = data['fn']
    args = data['args']
    debug(f"{fn}(*{args})")
    call = f"{fn}(*{args})"

    return json.dumps(eval(call))


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
                                             {"name": "eval!"},
                                             {"name": "edn-eval!"},
                                             {"name": "json-eval!"}]}]}
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

            if var == "pod.m3tti.py4clj/edn-eval!":
                result = edn_eval(args[0])

            if var == "pod.m3tti.py4clj/json-eval!":
                try:
                    result = json_eval(args[0])
                except:
                    result = None

            debug(result)
            value = json.dumps(result)
            debug("value", value)

            write({"value": value, "id": id, "status": ["done"]})

if __name__ == "__main__":
    main()
