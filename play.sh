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

daily=$(date +"%Y%m%d")

if [ -z "$3" ]; then
    echo "Input a seed string, then press enter. For an auto-generated seed, input nothing. For the Seed of the Day, zz-${daily}, input a question mark."
    echo -n "Input: "
    IFS=$'\n' # don't split answer on spaces
    read -r SEED </dev/tty
    echo

    if [ -z "$SEED" ]; then
        b36="0123456789abcdefghijklmnopqrstuvwxyz"
        daily=$(date +"%s")
        SEED=""
        while true; do
            SEED=${b36:((daily%36)):1}${SEED}
            if [ $((daily=${daily}/36)) -eq 0 ]; then
                break
            fi
        done
        SEED="zz-$SEED"
    fi
else
    SEED="$3"
fi

SEED="${SEED%\.dat}"
if [[ "$SEED" == "?"* ]]; then
    SEED="zz-$SEED"
fi
SEED="${SEED//\?/$daily}"

if [ -f "$SEED".dat ]; then
    echo Seed already in use: "$SEED"
    if ! ask "Are you continuing (y) or restarting (n)?" Y; then
        rm "$SEED".dat
        echo
    fi
fi

if [ ! -f "$SEED".dat ]; then
    echo New seed: "$SEED"
fi

echo

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
