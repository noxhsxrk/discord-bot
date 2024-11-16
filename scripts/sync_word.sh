#!/bin/bash

file1="src/bot_commands/insider/words.txt"
file2="src/bot_commands/just_one/words.txt"

lines_file1=$(wc -l <"$file1")
lines_file2=$(wc -l <"$file2")

print_unique_words() {
    sort "$1" | uniq >temp1.txt
    sort "$2" | uniq >temp2.txt
    comm -23 temp1.txt temp2.txt
    rm temp1.txt temp2.txt
}

if [ "$lines_file1" -gt "$lines_file2" ]; then
    echo "Synchronized words from $file1 to $file2:"
    print_unique_words "$file1" "$file2"
    cp "$file1" "$file2"
else
    echo "Synchronized words from $file2 to $file1:"
    print_unique_words "$file2" "$file1"
    cp "$file2" "$file1"
fi
