(require '[babashka.pods :as pods])

(pods/load-pod ["./py4clj.py"])

(python-call {:fn "len" :args [1 2 3 4]}) ;; error returns nil

(pyfn len :as pylen)
(pylen [1 2 2])

(pyfn json.dumps :as pyjd)
(pyjd {:a "b"})
