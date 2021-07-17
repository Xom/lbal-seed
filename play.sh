#!/usr/bin/env bash

# lbal-seed v20210716a

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
        rm -f "$SEED".dat "$SEED".save
        echo
    elif [ ! -f "$SEED".save ]; then
        if ! ask "Missing ${SEED}.save! Continue anyway (y) or stop (n)?" N; then
            exit
        fi
        if [ -f "$2" ]; then
            cp "$2" "$SEED".save # avoid killing LBAL when detecting previous save
        else
            echo "foo" > "$SEED".save
        fi
    fi
fi

if [ ! -f "$SEED".dat ]; then
    echo New seed: "$SEED"
    if [ -f "$2" ]; then
        cp "$2" "$SEED".save # avoid killing LBAL when detecting previous save
    else
        echo "foo" > "$SEED".save
    fi
fi

echo

cleanup() {
    kill "$!" 2> /dev/null
}

if [[ "$1" == *".exe" ]]; then
    echo "play.sh can't kill native Windows programs. You must manually close the game window at each roll."
    read -s -n 1 -p "Press any key to continue..."
    echo
    while true; do
        "$1" > /dev/null 2>&1
        # echo Original:
        # cat "$2"
        # echo
        ./seed.py "$SEED" < "$2" > "$SEED".save
        cp "$SEED".save "$2"
        # echo Modified:
        # cat "$SEED".save
        # echo
        # read -s -n 1 -p "Press any key to continue..."
        # echo
    done
else
    trap cleanup EXIT
    new=3 # counter to stop stringsearching for "rent_values":[25,5] after a few loops
    while true; do
        prev=$(tail -n 1 "$SEED".save)
        "$1" > /dev/null 2>&1 &
        while sleep 0.1; do
            { nextfull=$(<"$2"); } 2> /dev/null
            next=$(tail -n 1 <<< "$nextfull")
            if [ "$prev" != "$next" ] && [[ "$next" == *"\"saved_card_types\":[\""* ]] && [[ $(head -n 1 <<< "$nextfull") == *"\"adding\":false,"*"\"path\":\"/root/Main/Sums/Coin Sum\""* ]]; then
                if [ $new -eq 0 ]; then
                    break
                fi
                ((new--))
                if [[ "$next" != *"\"rent_values\":[25,5]"* ]]; then
                    break
                fi
                prev="$next"
            elif ! kill -0 "$!" 2> /dev/null; then
                exit
            fi
        done
        # if grep -q '"item_types":[^]]*"\(adoption_papers\|lunchbox\|booster_pack\|symbol_bomb\)' <<< "$nextfull"; then
        sleep 0.2
        # fi
        kill "$!" 2> /dev/null
        wait
        # echo Original:
        # cat "$2"
        # echo
        ./seed.py "$SEED" < "$2" > "$SEED".save
        cp "$SEED".save "$2"
        # echo Modified:
        # cat "$SEED".save
        # echo
        # read -s -n 1 -p "Press any key to continue..."
        # echo
    done
fi
