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

build:
	./scripts/build-package.sh

create-tag:
	./scripts/create-tag.sh

publish-test:
	./scripts/publish-test.sh

.PHONY: install clean
