VENVDIR = venv

gantt.pdf: venv
	( \
		source $(VENVDIR)/bin/activate; \
		python milestones.py gantt --output=gantt.tex; \
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

milestones.csv: venv
	( \
		source $(VENVDIR)/bin/activate; \
		python milestones.py csv; \
	)


.PHONY: jira
jira: venv
	( \
		source $(VENVDIR)/bin/activate; \
		python milestones.py jira; \
	)

.PHONY: clean
clean:
	rm -rf $(VENVDIR)
