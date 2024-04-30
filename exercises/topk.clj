(ns topk
  (:require [clojure.string :as str]))

(defn top-k [sku-list k]
  (->> sku-list
       (frequencies)
       (sort-by val >)
       (take k)
       (map first)))

(defrecord TestCase [sku-list k expected comment])

(def test-cases
  [(TestCase. [] 100 [] "Empty list with k=100")
   (TestCase. ["a" "b" "c" "d" "e" "a" "b" "e" "e"] 3 ["e" "a" "b"])
   (TestCase. ["a" "b" "c" "d" "e" "a" "b" "e" "e"] 2 ["e" "a"])
   (TestCase. ["a" "b" "c" "d" "e" "a" "b" "e" "e"] 1 ["e"])
   (TestCase. ["a" "b" "c" "d" "e" "a" "b" "e" "e"] 4 ["e" "a" "b" "c"])])


(def -main
  (doseq [tc test-cases]
    (let [actual (top-k (:sku-list tc) (:k tc))]
      (if (= actual (:expected tc))
        (println "Test passed" tc "Actual:" actual)
        (println "Test failed" tc "Expected:" (:expected tc) "Actual:" actual)))))
  
