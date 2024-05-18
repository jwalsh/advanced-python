;; The Litter Schemer, Fourth Edition
;; page 41

(define member? (lambda (x lst)
  (cond
    ((null? lst) #f)
    ((eq? x (car lst)) #t)
    (else (member? x (cdr lst))))))

(define test-list '(1 2 3 4 5))

(member? 3 test-list) ; #t

(member? 6 test-list) ; #f
