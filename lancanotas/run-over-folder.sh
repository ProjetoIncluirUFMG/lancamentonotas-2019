#!/bin/bash

for filename in $1/*.{xlsx,xlsm} ; do
  python manage.py extractxls "$filename"
done