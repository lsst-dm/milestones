VENVDIR = venv

celeb: venv
	( \
		source $(VENVDIR)/bin/activate; \
		python milestones.py  celeb; \
	)
burndown.png: venv
	( \
		source $(VENVDIR)/bin/activate; \
		python milestones.py  burndown; \
	)
fcast_burndown.png: venv
	( \
		source $(VENVDIR)/bin/activate; \
		python milestones.py --forecast burndown; \
	)

fcast_gantt.pdf: venv
	( \
		source $(VENVDIR)/bin/activate; \
		python milestones.py --forecast gantt --output=gantt.tex; \
		xelatex fcast_gantt.tex; \
	)

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
