#!/bin/bash
install -Dm755 src/ana.py /usr/local/bin/ana
install -Dm644 packaging/ana.desktop /usr/share/applications/ana.desktop
cp -r content /usr/share/ana/
