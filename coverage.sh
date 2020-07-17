#!/bin/bash
mv -f ~/.autobrightness ~/.autobrightness.backup
coverage erase
coverage run --source autobrightness -m unittest discover -s tests
coverage xml -i
mv -f ~/.autobrightness.backup ~/.autobrightness