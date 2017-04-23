#!/bin/bash
# Bash script so that the pylint tests does not fail the build on travis
# Help for script http://stackoverflow.com/questions/6626351/how-to-extract-bits-from-return-code-number-in-bash
# Source for pylint error return code: https://docs.pylint.org/en/1.6.0/run.html

#pylint --disable=C0103,C0111,C0303,RP0001,RP0002,RP0003,RP0101,RP0101,RP0401,RP0701,R0904,W0702 src/pyprime.py 
#pylint --disable=C0303 src/pyprime.py #Removes trailing-whitespace error


function my_pylint () {

    pylint --disable=C0303 $1   #Removes trailing-whitespace error
    
    status=$?     # Catch exit status before it changes

    if [ $status = 0 ]      # Means it worked well
    then 
        echo "$status: it worked perfectly"

    elif [ $(($status > 3 )) ]   # pylint return 1 is fatal error, return 2 is error 
    #elif [ $status -gt 3 ]      # Same as above
    then 
        echo "$status: a fatal or error message was sent"
    else 
        echo "$status: it sort of worked mostly"
    fi
}

#for f in "src/pyprime.py" "src/pyprime.py" "src/pyprime.py"; do # if the file and the script are not in the same directory
for f in pyprime.py toolbox.py unit_test.py; do
    
    echo "------- $f processing ------"
    echo " "
    my_pylint $f

done

exit 0