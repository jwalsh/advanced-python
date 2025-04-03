;;; Directory Local Variables
;;; For more information see (info "(emacs) Directory Variables")

((python-mode . ((python-shell-interpreter . "poetry")
                 (python-shell-interpreter-args . "run ipython")
                 (python-shell-prompt-regexp . "In \\[[0-9]+\\]: ")
                 (python-shell-prompt-output-regexp . "Out\\[[0-9]+\\]: ")
                 (python-shell-completion-setup-code . "from IPython.core.completerlib import module_completion")
                 (python-shell-completion-module-string-code . "';'.join(module_completion('''%s'''))")
                 (python-shell-completion-string-code . "';'.join(get_ipython().Completer.all_completions('''%s'''))")
                 (flycheck-python-pylint-executable . "poetry run pylint")
                 (flycheck-python-flake8-executable . "poetry run flake8")
                 (flycheck-python-mypy-executable . "poetry run mypy")
                 (lsp-python-ms-python-executable . "poetry run python")
                 (lsp-pyright-python-executable-cmd . "poetry run python")
                 (eval . (progn
                           (require 'lsp-pyright)
                           (lsp-deferred)))))

 (org-mode . ((eval . (org-babel-do-load-languages
                       'org-babel-load-languages
                       '((python . t)
                         (shell . t)
                         (emacs-lisp . t)))))))