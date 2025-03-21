(require '[babashka.pods :as pods])

(pods/load-pod ["./main.py"])

(pod.m3tti.py4clj/execute! "'bla bla'.split(' ')")
