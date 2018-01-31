#!/usr/bin/env bash

rm .git/hooks/*
echo "Symlinking new hooks..."
ln -s ../../test.sh .git/hooks/pre-commit
echo "Done."
