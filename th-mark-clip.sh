#!/usr/bin/env bash
{
    now=$(date +"%Y-%m-%d") ;
    echo -e "<!-- Generated from $1 on $now -->" ;
    jupyter nbconvert $1 --to markdown --stdout;
    echo -e "\n\n\n" ;
    cat ./th-script-snippet.html ;
} | pbcopy
echo -e "Your clipboard is filled with delicious notebook markdown generated from $1"