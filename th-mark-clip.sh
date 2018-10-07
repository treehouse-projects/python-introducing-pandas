#!/usr/bin/env bash
{
    now=$(date +"%Y-%m-%d") ;
    echo -e "<!-- Generated from $1 on $now -->" ;
    echo -e "[![Binder](https://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/treehouse-projects/python-introducing-pandas/master?filepath=$1)\n"
    jupyter nbconvert $1 --to markdown --stdout;
    echo -e "\n\n\n" ;
    cat ./th-script-snippet.html ;
} | pbcopy
echo -e "Your clipboard is filled with delicious notebook markdown generated from $1"