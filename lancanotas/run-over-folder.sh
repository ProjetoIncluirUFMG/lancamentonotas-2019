#!/bin/bash

for filename in $1/*.{xlsx,xlsm} ; do
  python manage.py extractxls "$filename" >>"$filename.log" 2>&1
done