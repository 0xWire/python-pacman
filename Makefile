PYTHON ?= python
PYTEST = $(PYTHON) -m pytest
FLAKE8 = $(PYTHON) -m flake8
REPORTS_DIR = reports
PYTEST_REPORT = $(REPORTS_DIR)/pytest/report.html
FLAKE8_REPORT_DIR = $(REPORTS_DIR)/flake8

.PHONY: clean-reports test lint report ci

clean-reports:
	rm -rf $(REPORTS_DIR)

test:
	$(PYTEST)

lint:
	$(FLAKE8) .

report: clean-reports
	mkdir -p $(REPORTS_DIR)/pytest $(FLAKE8_REPORT_DIR)
	$(PYTEST) --html=$(PYTEST_REPORT) --self-contained-html
	$(FLAKE8) . --format=html --htmldir=$(FLAKE8_REPORT_DIR)

ci: lint test report
