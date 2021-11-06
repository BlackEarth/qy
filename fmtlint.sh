#!/bin/bash
PATHS="qy"
isort -q -rc $PATHS
black -q $PATHS
flake8
