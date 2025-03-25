(require '[babashka.pods :as pods])

(pods/load-pod ["./py4clj.py"])

(require '[pod.m3tti.py4clj :as py4clj])

(python-call {:fn "len" :args [1 2 3 4]}) ;; error returns nil

(pyfn len :as pylen)
(pylen [1 2 2])

(pyfn json.dumps :as pyjd)
(pyjd {:a "b"})

(py4clj/python-import "sqlite")
(py4clj/exec! "con = sqlite.connect(\"tutorial.db\")")
(py4clj/eval! "con.execute(\"select * from bla\")")

(py4clj/python-call {:fn ".dumps" :args [{:a "b"}]})

(py4clj/python-import "math" :as "m")
(py4clj/python-call {:fn "m.sqrt" :args [42]})
