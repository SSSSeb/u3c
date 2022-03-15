#!/bin/bash

cat resultats.txt | awk -F'\t' '{ printf("%-10s %-10s %-20s %-20s %14s %14s %06s\n",$5,$6,$1,$2,$7,$3,$4)}' | tail -30
