VENVDIR = venv

gantt.pdf: venv
	( \
		source $(VENVDIR)/bin/activate; \
		python milestones.py standalone --gantt gantt.tex; \
		xelatex gantt.tex; \
		xelatex gantt.tex; \
		xelatex gantt.tex; \
	)

venv:
	python -m venv $(VENVDIR)
	( \
		source $(VENVDIR)/bin/activate; \
		pip install -r requirements.txt; \
	)

.PHONY: jira
jira: venv
	( \
		source $(VENVDIR)/bin/activate; \
		python milestones.py standalone --jira; \
	)

.PHONY: clean
clean:
	rm -rf $(VENVDIR)
