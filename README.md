# py4clj

a simple bridge to use python libs inside of clojure/babashka based on [pods](https://github.com/babashka/pods).

## Uses
- babashka
- python3 with the following libs
  - bcoding
  - edn_format

## Current stage
Playing around with moven json data to the python pod to create function calls there.

# Examples

``` clojure
(python-import "math" :as "mat")
(pyfn mat.sqrt :as pysqrt)
(pysqrt 42)
;; or
(python-call {:fn "mat.sqrt" :args [42]})
```
