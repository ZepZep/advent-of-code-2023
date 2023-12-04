

task_fname=`printf "py/task%02d.py" $1`

if test -f $task_fname; then
    echo file $task_fname already exists!
    kate $task_fname &&
    exit 0
fi

cat template.py | sed "s/TASK_NUM/$1/" > $task_fname

echo created $task_fname
kate $task_fname &&
exit 0
