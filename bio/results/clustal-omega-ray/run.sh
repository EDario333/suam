#!/bin/bash

ray start --head --redis-port=6379
python ../../../vs-covid19.py -if ../sequences.fasta -fif fasta -t clustalo -v -ur