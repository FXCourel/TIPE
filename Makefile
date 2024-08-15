main:
	@python3 -B main.py

test:
	@python3 -B tests.py

perfs:
	@python3 -B perf.py

clean:
	find . | grep -E "(__pycache__|\.pyc$$)" | xargs rm -rf