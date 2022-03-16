#!/bin/bash

# shellcheck disable=SC1091
source reglages || exit 1
awk -F'\t' '{ printf("%04d: #%03d %-10s %-20s %-20s %14s %14s %06s\n",FNR-1,$5,$6,$1,$2,$7,$3,$4)}' <"${FICHIER_POUR_FRANCK}" | tail -30
