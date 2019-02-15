cat requirements.txt | \
while read line
do
	if [[ "$line" != "#"* ]];then
		if [[ "$line" != "django>=1.7" ]];then
			pip install $line
		#else
		#	pip3 install django>=1.7
		fi
	fi
done