#!/usr/bin/env bash
{
    now=$(date +"%Y-%m-%d") ;
    echo -e "<!-- Generated from $1 on $now -->" ;
    echo -e '<span class="markdown--jupyter-notebook">\n' ;
    jupyter nbconvert $1 --to markdown --stdout;
    echo -e '</span>\n' ;
} | pbcopy
echo 'Your clipboard is filled with delicious notebook markdown'