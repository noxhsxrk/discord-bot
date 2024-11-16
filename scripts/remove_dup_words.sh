#!/bin/bash

file1="src/bot_commands/insider/words.txt"
file2="src/bot_commands/just_one/words.txt"

remove_duplicates() {
    local file="$1"
    sort "$file" | uniq >temp_file && mv temp_file "$file"
    echo "Duplicates removed in the file: $file"
}

remove_duplicates "$file1"
remove_duplicates "$file2"
