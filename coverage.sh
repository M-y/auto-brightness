#!/bin/bash
coverage erase
coverage run --source . -m unittest discover -s tests
coverage xml