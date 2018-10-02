{ echo '<span class="markdown--jupyter-notebook">\n' ; jupyter nbconvert $1 --to markdown --stdout; echo '</span>\n' ; } | pbcopy
echo 'Your clipboard is filled with delicious notebook markdown'