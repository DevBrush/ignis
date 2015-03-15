#!/bin/sh
python3 setup.py install
cp docs/ignis.1.gz /usr/share/man/man1/
mkdir -p /etc/ignis/
cp -r docs/example/ /etc/ignis/
