for file in $(ls $1);
do
./create_hit.py -p -i $1/$file -t template.html
done
