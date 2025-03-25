(require '[babashka.pods :as pods])

(pods/load-pod ["./py4clj.py"])

(require '[pod.m3tti.py4clj :as py4clj])

(py4clj/python-import 'math :as 'm)
(py4clj/pyfn m.sqrt :as pysqrt)
(pysqrt 42)

(py4clj/python-import 'uuid :as 'pyu)
(py4clj/pyfn pyu.uuid4 :as pyuuid)
(pyuuid)

(py4clj/setf! 'x 12)
(py4clj/eval! 'x)
