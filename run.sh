#!/bin/bash

NUM_WORKERS=5
FILE="additional_config.txt"

function test_update() {
    update_variable=$1
    update_value=$2
    python3 test.py --key $update_variable --value $update_value --num-workers $NUM_WORKERS
}

function test_signal_handling() {
    update_variable=$1
    update_value=$2
    date=$(date)
    echo  "$update_value:$date" > $FILE
    python3 test.py --key $update_variable --value $update_value --num-workers $NUM_WORKERS
}

function run_app() {
    python3 app.py --num-workers $NUM_WORKERS
}

function main() {
    if [ "$#" -eq 0 ]; then 
        if [ -f $FILE ]; then
            rm $FILE
        fi
        echo "Init" > $FILE
        run_app
    else
        action=$1; shift
        case $action in
            test_global_variable)
                test_update "global_data" "new_data"
                ;;
            test_mp_value)
                test_update "multiprocess_value" 1
                ;;
            test_mp_array)
                test_update "multiprocess_array" 100
                ;;
            test_mp_manager)
                test_update "multiprocess_manager" "new_manager_data"
                ;;
            test_signal_handling)
                test_signal_handling "sighup_data" "new_sighup_data"
                ;;
            *)
                echo "Wrong option"
                exit 1
                ;;
        esac
    fi
}

program_name=$0
main "$@"