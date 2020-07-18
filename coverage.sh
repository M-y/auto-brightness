#!/bin/bash
mv -f ~/.autobrightness ~/.autobrightness.backup
coverage erase
coverage run --source autobrightness -m unittest discover -s tests -v -f
coverage xml -i
mv -f ~/.autobrightness.backup ~/.autobrightness