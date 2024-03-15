TeXInputs = TEXINPUTS=$(CURDIR):
MPLRC = MATPLOTLIBRC=$(CURDIR)/matplotlibrc

# add plots here
PLOTS := build/multi_messenger.pdf


all: $(PLOTS)

download: FORCE
	python download_files.py -i url_list.txt -o data/
	unzip -p data/20230424_Observation_of_High-Energy_Neutrinos_from_the_Galactic_Plane.zip \
		Public_Release/Fig4/ss_results.csv >data/ic_2023_gal_neutrinos.csv
	rm data/20230424_Observation_of_High-Energy_Neutrinos_from_the_Galactic_Plane.zip

build/multi_messenger.pdf: multi_messenger.py ./matplotlibrc ./header-matplotlib.tex | build
	$(TeXInputs) $(MPLRC) python $<

build:
	mkdir -p build/

clean:
	rm -rf build/

clean_data:
	rm -rf data/

FORCE:

.PHONY: all clean FORCE
