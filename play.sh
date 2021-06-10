#!/usr/bin/env bash

ask() {
    local prompt default reply

    if [[ ${2:-} = 'Y' ]]; then
        prompt='Y/n'
        default='Y'
    elif [[ ${2:-} = 'N' ]]; then
        prompt='y/N'
        default='N'
    else
        prompt='y/n'
        default=''
    fi

    while true; do

        # Ask the question (not using "read -p" as it uses stderr not stdout)
        echo -n "$1 [$prompt] "

        # Read the answer (use /dev/tty in case stdin is redirected from somewhere else)
        read -r reply </dev/tty

        # Default?
        if [[ -z $reply ]]; then
            reply=$default
        fi

        # Check if the reply is valid
        case "$reply" in
            Y*|y*) return 0 ;;
            N*|n*) return 1 ;;
        esac

    done
}

if [ -z "$3" ]; then
    SEED=$(date +"%s")
else
    SEED=${3%\.dat}
    if [ -f "$SEED".dat ]; then
        echo Seed already in use: "$SEED"
        if ! ask "Are you continuing (y) or restarting (n)?" Y; then
            rm "$SEED".dat
            echo
        fi
    fi
fi

if [ ! -f "$SEED".dat ]; then
    echo New seed: "$SEED"
fi

while true; do
    "$1" > /dev/null 2>&1
    cp "$2" LBAL.save.bak
    # echo Original:
    # cat LBAL.save.bak
    # echo
    ./seed.py "$SEED" < LBAL.save.bak > "$2"
    # echo Modified:
    # cat "$2"
    # echo
#     read -s -n 1 -p "Press any key to continue . . ."
#     echo ""
done
