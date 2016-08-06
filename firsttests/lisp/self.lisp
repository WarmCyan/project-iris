(defparameter *self* "thing")
(defparameter *approval* "thing2")

(defun self-existence ()
  (mutate *self*)
  (approve? *self*)
  (remember *self* *approval*)
  (values))

(defun mutate (thing)
  (format t "Mutating...~%"))

(defun approve? (thing)
  (format t "Do you approve of me?~%"))

(defun remember (thing1 thing2)
  (format t "Trying to remember self...~%"))
