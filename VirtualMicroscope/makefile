CC1=iverilog
CC3=emacs
TARGET1=bancoDePruebas.v cmos_cells.v sum_pipe.v
TARGET2=mux.vcd
run:
	python3 manage.py runserver

install: 
	sudo apt-get install python3.6
	sudo apt install -y zip unzip
	pip3 install Django==2.2.11
	pip3 install jsonfield
	pip3 install psycopg2-binary
	sudo apt-get install libvips
	sudo apt-get install libvips-dev
	sudo apt-get install libvips-tools


slide:
	wget ${ARGS} -O slide.svs
	vips dzsave slide.svs ./media/slides/${ARGS2}.zip  --background 0 --centre --layout google
	rm *.svs
	unzip ./media/slides/${ARGS2}.zip 
	unzip ./media/slides/${ARGS2}.zip -d ./media/slides/
	rm ./media/slides/*.zip