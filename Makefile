all: install

install:
	./scripts/install.sh

clean:
	./scripts/clean.sh

test:
	./scripts/test.sh

lint:
	./scripts/lint.sh

typecheck:
	./scripts/typecheck.sh

check_format:
	./scripts/check_format.sh

format:
	./scripts/format.sh

quality:
	./scripts/quality.sh

.PHONY: install clean
