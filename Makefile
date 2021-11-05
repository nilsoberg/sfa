.DEFAULT_GOAL := help
.PHONY: help install

help:
	less -X README.md

install:
	./scripts/install.sh
