#!/usr/bin/env python3

import json
import sys
import itertools

from bcoding import bencode, bdecode


python_import = """
(defmacro require-python [lib & {:keys [as]}]
  (do (pod.m3tti.py4clj/exec!
       (if as
         (str "import " lib " as " as)
         (str "import " lib )))
      (let* [*namespace* (symbol (if as as lib))
             *cur-ns* *ns*
             functions (doall (map (fn [fun]
                                     `(pod.m3tti.py4clj/defpyfn
                                        ~(symbol (str *namespace* "." fun))
                                        :as ~(symbol fun)))
                                   (pod.m3tti.py4clj/fn-names (if as as lib))))]
        `(do
           (ns ~*namespace*)
           ~@functions
           (ns *cur-ns*)))))
"""

python_call = """
(require '[cheshire.core :as json])
(defn python-call [c]
  (->
   c
   json/encode
   json-eval!
   json/decode))
"""

pyfn = """
(defmacro defpyfn [fn-name & {:keys [as]}]
  (let [sym (if as
              as
              fn-name)]
    `(def ~sym (fn [& args]
       (python-call {:fn ~(str fn-name) :args args})))))
"""


setf = """
(defn setf! [var value]
  (exec! (str var "=" value)))
"""


fnNames = """
(defn fn-names [module]
  (pod.m3tti.py4clj/eval!
    (str
      "[name for name, fn in inspect.getmembers("
      module
      ", callable) if name[0] != '_']")))"""


eval_globals = {}
python_objects = {}
python_handle = itertools.count(0)

exec("import inspect", eval_globals)

def cljfy(obj):
    try:
        return json.dumps(obj)
    except:
        return cljfy_handle(obj)


def cljfy_handle(obj):
    handle = next(python_handle)
    python_objects[f"pyObj_{handle}"] = obj
    return cljfy(f"pyObj_{handle}")


def read():
    return dict(bdecode(sys.stdin.buffer))


def write(obj):
    sys.stdout.buffer.write(bencode(obj))
    sys.stdout.flush()


def debug(*msg):
    with open("/tmp/debug.log", "a") as f:
        f.write(str(msg) + "\n")

def py_eval(*msg):
    return eval(*msg, eval_globals)


def py_exec(*msg):
    return exec(*msg, eval_globals)


def json_eval(jo):
    data = json.loads(jo)
    fn = data['fn']
    args = data['args']

    function = py_eval(fn)

    if args != None:
        return cljfy(function(*args))
    else:
        return cljfy(function())


def describe():
    write({
        "format": "json",
        "namespaces": [
            {"name": "pod.m3tti.py4clj",
             "vars": [
                 {"name": "exec!"},
                 {"name": "eval!"},
                 {"name": "json-eval!"},
                 {"name": "defpyfn",
                  "code": pyfn},
                 {"name": "setf!",
                  "code": setf},
                 {"name": "fn-names",
                  "code": fnNames},
                 {"name": "python-call",
                  "code": python_call},
                 {"name": "require-python",
                  "code": python_import},
             ]}
        ]}
    )


def invoke(msg):
    var = msg["var"]
    id = msg["id"]
    args = json.loads(msg["args"])

    debug(args)

    if var == "pod.m3tti.py4clj/exec!":
        try:
            py_exec(args[0])
            result = True
        except Exception as e:
            issue = getattr(e, 'message', str(e))
            debug(issue)
            result = cljfy({"error": issue})

    if var == "pod.m3tti.py4clj/eval!":
        try:
            result = py_eval(args[0])
        except Exception as e:
            issue = getattr(e, 'message', str(e))
            debug(issue)
            result = cljfy({"error": issue})

    if var == "pod.m3tti.py4clj/json-eval!":
        try:
            result = json_eval(args[0])
        except Exception as e:
            issue = getattr(e, 'message', str(e))
            debug(issue)
            result = cljfy({"error": issue})

    debug(result)
    value = json.dumps(result)
    debug("value", value)

    write({"value": value, "id": id, "status": ["done"]})


def main():
    while True:
        python_handle = itertools.count(0)
        msg = read()
        debug("msg", msg)

        op = msg["op"]

        if op == "describe":
            describe()

        elif op == "invoke":
            invoke(msg)


if __name__ == "__main__":
    main()
