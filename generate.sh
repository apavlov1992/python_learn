set -u # когда нет переменной баш вываливается(unset)
mkdir $1
for i in {1..10}; do
  mkdir -p $1/$i
for n in {1..1000}; do
    dd if=/dev/urandom of=$1/$i/file$( printf %03d "$n" ).bin bs=1 count=$(( RANDOM + 1024 ))
    openssl rand -base64 2048 > $1/$i/file$( printf %03d "$n" ).txt
done
done
