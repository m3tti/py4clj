(require '[babashka.pods :as pods])

(pods/load-pod ["./py4clj.py"])

(defn python-import [lib]
  (pod.m3tti.py4clj/exec! (str "import " lib)))

(defn python-call [c]
  (->
   c
   json/encode
   pod.m3tti.py4clj/json-eval!
   json/decode))

(defmacro pyfn [fn-name & {:keys [as]}]
  (let [sym (if as
              as
              fn-name)]
    `(defn ~sym [& args]
       (python-call {:fn ~(str fn-name) :args args}))))

(python-call {:fn "len" :args [1 2 3 4]}) ;; error returns nil

(pyfn len :as pylen)

(pylen [1 2 2])
