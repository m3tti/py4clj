(require '[babashka.pods :as pods])

(pods/load-pod ["./py4clj.py"])

(defn python-import [lib]
  (pod.m3tti.py4clj/exec! (str "import " lib)))

(defn pythonize [val]
  (condp instance? val
    java.lang.String val
    java.lang.Integer val
    clojure.lang.PersistentVector (str "[" (str/join ", " (map #'pythonize val))"]")
    clojure.lang.LazySeq (str "[" (str/join ", " (map #'pythonize val))"]")
    clojure.lang.Symbol (str val)
    (str val)))

(defn python-call [fn-name & args]
  (pod.m3tti.py4clj/eval!
   (str fn-name  "(" (str/join ", " (map #'pythonize args)) ")")))

(defmacro pyfn [fn-name & {:keys [as]}]
  (let [sym (if as
              as
              fn-name)]
    `(defn ~sym [& args]
       (apply #'python-call ~(str fn-name) (vec args)))))

(pyfn len :as pylen)
(pylen [1 2 3])

(pyfn "json.dumps" :as py-json-dumps)
(py-json-dumps [1 3 4])
