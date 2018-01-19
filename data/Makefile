.PHONY: clean

all:
	@mkdir -p build/s_center
	@cd ../app; ./cli.py ../data/center Sweep ../data/build/s_center
	@cd ../texmap; ./texmap.py ../data/build/s_center/points ../data/build/s_center/paths ../data/build/s_center/map.tex
	@pdflatex -output-directory=build/s_center build/s_center/map.tex

	@mkdir -p build/ck_center
	@cd ../app; ./cli.py ../data/center ClarkeWright ../data/build/ck_center
	@cd ../texmap; ./texmap.py ../data/build/ck_center/points ../data/build/ck_center/paths ../data/build/ck_center/map.tex
	@pdflatex -output-directory=build/ck_center build/ck_center/map.tex

	@mkdir -p build/s_piastow
	@cd ../app; ./cli.py ../data/piastow Sweep ../data/build/s_piastow
	@cd ../texmap; ./texmap.py ../data/build/s_piastow/points ../data/build/s_piastow/paths ../data/build/s_piastow/map.tex
	@pdflatex -output-directory=build/s_piastow build/s_piastow/map.tex

	@mkdir -p build/ck_piastow
	@cd ../app; ./cli.py ../data/piastow ClarkeWright ../data/build/ck_piastow
	@cd ../texmap; ./texmap.py ../data/build/ck_piastow/points ../data/build/ck_piastow/paths ../data/build/ck_piastow/map.tex
	@pdflatex -output-directory=build/ck_piastow build/ck_piastow/map.tex

clean:
	@rm -rf build
