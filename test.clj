(require '[pod.m3tti.py4clj :as py4clj])

(py4clj/setf! "hello" "Hello, World")
(py4clj/py. "hello" '(split ",") 1)

(py4clj/require-python "math" :as "pymath")

(pymath/sin 180)
