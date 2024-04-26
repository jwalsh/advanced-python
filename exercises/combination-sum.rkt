(define/contract (combination-sum candidates target)
  (-> (listof exact-integer?) exact-integer? (listof (listof exact-integer?))))


(define (combination-sum candidates target)
  (define (helper candidates target)
    (cond
      [(= target 0) '()]
      [(= (length candidates) 0) '()]
      [else
       (append (helper (cdr candidates) (- target (car candidates)))
	       (map (lambda (x) (cons (car candidates) x))
		    (helper candidates (- target (car candidates)))))])))

