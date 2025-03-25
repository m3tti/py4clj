#!/usr/bin/env python3

import json
import sys
import inspect
import importlib

from bcoding import bencode, bdecode


python_import = """
(defn python-import [lib & {:keys [as]}]
  (pod.m3tti.py4clj/exec!
    (if as
      (str "import " lib " as " as)
      (str "import " lib))))
"""

python_call = """
(require '[cheshire.core :as json])
(defn python-call [c]
  (->
   c
   json/encode
   pod.m3tti.py4clj/json-eval!
   json/decode))
"""

pyfn = """
(defmacro pyfn [fn-name & {:keys [as]}]
  (let [sym (if as
              as
              fn-name)]
    `(defn ~sym [& args]
       (python-call {:fn ~(str fn-name) :args args}))))
"""

eval_globals = {}
python_objects = {}


def cljfy_handle ():
    handle = next(python_handle)
    python_objects[handle] = obj
    return {"handle": handle}

def read():
    return dict(bdecode(sys.stdin.buffer))


def write(obj):
    sys.stdout.buffer.write(bencode(obj))
    sys.stdout.flush()


def debug(*msg):
    with open("/tmp/debug.log", "a") as f:
        f.write(str(msg) + "\n")


def fn_name(module):
    return [name for name, fn in inspect.getmembers(module, callable) if name[0] != '_']


def json_eval(jo):
    data = json.loads(jo)
    fn = data['fn']
    args = data['args']
    debug(f"{fn}(*{args})")
    call = f"{fn}(*{args})"

    return json.dumps(eval(call, eval_globals))


def main():
    while True:
        msg = read()
        debug("msg", msg)

        op = msg["op"]

        if op == "describe":
            write(
                {
                    "format": "json",
                    "namespaces": [
                        {"name": "pod.m3tti.py4clj",
                         "vars": [
                             {"name": "exec!"},
                             {"name": "eval!"},
                             {"name": "json-eval!"},
                             {"name": "python-import",
                              "code": python_import},
                             {"name": "python-call",
                              "code": python_call},
                             {"name": "pyfn",
                              "code": pyfn}
                         ]}
                    ]}
            )
        elif op == "invoke":
            var = msg["var"]
            id = msg["id"]
            args = json.loads(msg["args"])
            debug(args)

            if var == "pod.m3tti.py4clj/exec!":
                try:
                    exec(args[0], eval_globals)
                    result = True
                except:
                    result = False

            if var == "pod.m3tti.py4clj/eval!":
                result = eval(args[0], eval_globals)

            if var == "pod.m3tti.py4clj/json-eval!":
                try:
                    result = json_eval(args[0])
                except Exception as e:
                    issue = getattr(e, 'message', str(e))
                    debug(issue)
                    result = json.dumps({"error": issue})

            debug(result)
            value = json.dumps(result)
            debug("value", value)

            write({"value": value, "id": id, "status": ["done"]})

if __name__ == "__main__":
    main()
