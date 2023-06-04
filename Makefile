VENVDIR = venv

report.csv: venv
	@( \
		. $(VENVDIR)/bin/activate; \
		python milestones.py report --output report.csv --prefix "SIT COM SUM" --months 2\
	)

blockschedule.pdf: venv
	@( \
		. $(VENVDIR)/bin/activate; \
		python milestones.py blockschedule --start-date -20 \
	)

burndown.png: venv
	( \
		. $(VENVDIR)/bin/activate; \
		python milestones.py  burndown; \
	)

gantt.pdf: venv
	( \
		. $(VENVDIR)/bin/activate; \
		python milestones.py gantt --output=gantt.tex; \
		xelatex gantt.tex; \
		xelatex gantt.tex; \
		xelatex gantt.tex; \
	)

venv:
	python -m venv $(VENVDIR)
	( \
		. $(VENVDIR)/bin/activate; \
		pip install -r requirements.txt; \
	)

milestones.csv: venv
	( \
		. $(VENVDIR)/bin/activate; \
		python milestones.py csv; \
	)

celeb: venv
	( \
		. $(VENVDIR)/bin/activate; \
		python milestones.py  celeb --inc=Y; \
	)

.PHONY: jira
jira: venv
	( \
		. $(VENVDIR)/bin/activate; \
		python milestones.py jira; \
	)

.PHONY: clean
clean:
	rm -rf $(VENVDIR)
