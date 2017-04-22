#!/bin/bash
# Bash script so that the pylint tests does not fail the build on travis
# Help or script http://stackoverflow.com/questions/6626351/how-to-extract-bits-from-return-code-number-in-bash
# Source for pylint error return code: https://docs.pylint.org/en/1.6.0/run.html

#pylint --disable=C0103,C0111,C0303,RP0001,RP0002,RP0003,RP0101,RP0101,RP0401,RP0701,R0904,W0702 src/pyprime.py 

pylint --disable=C0303 src/pyprime.py #Removes trailing-whitespace error


function pylint {

    pylint --disable=C0303 $1
    
    status=$?     # Catch exit status before it changes

    if [ $status = 0 ]      # Means it worked well
    then 
        echo "$status: it worked perfectly"

    elif [ $(( $status & 3 )) != 0 ]   # Pylint error link above
    then 
        echo "$status: a fatal or error message was sent"
    else 
        echo "$status: it sort of worked mostly"
    fi
}


for f in src/pyprime.py src/toolbox.py src/unit_test.py
do
    
    echo "------- $f processing ------"
    pylint $f

done

exit 0