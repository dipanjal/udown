all: install

install:
	./scripts/install.sh

test:
	./scripts/test.sh

.PHONY: install
