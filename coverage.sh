#!/bin/bash
coverage erase
coverage run --source autobrightness -m unittest discover -s tests
coverage xml -i