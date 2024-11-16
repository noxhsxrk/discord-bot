#!/bin/bash

file1="src/bot_commands/insider/words.txt"
file2="src/bot_commands/just_one/words.txt"

remove_duplicates() {
    local file="$1"
    local temp_file="temp_file"
    local original_sorted="original_sorted.txt"

    sort "$file" >"$original_sorted"
    sort "$file" | uniq >"$temp_file"

    comm -23 "$original_sorted" "$temp_file" >removed_words.txt

    if [ -s removed_words.txt ]; then
        echo "Removed words:"
        cat removed_words.txt
        echo "Duplicates removed in the file: $file"
    else
        echo "No words were removed from the file: $file"
    fi

    mv "$temp_file" "$file"
    rm "$original_sorted"
    rm removed_words.txt
}

remove_duplicates "$file1"
remove_duplicates "$file2"
