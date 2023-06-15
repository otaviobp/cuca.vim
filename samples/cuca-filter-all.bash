#!/bin/bash
# Sample filter hook that doesn't filter any item

for x in $@; do
    echo $x
done
