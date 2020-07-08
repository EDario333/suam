#!/bin/bash

ray start --head --redis-port=6379
python ../tests.py -if ../sequences.fasta -fif fasta -t clustalo -v -ur