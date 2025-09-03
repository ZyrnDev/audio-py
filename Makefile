SHELL := /bin/bash

.PHONY: clean default

FILE := output.wav

default: $(FILE)
	@echo "Running default target, generated $(FILE)"

%.wav: .venv
	source .venv/bin/activate
	python3 main.py $@

%.mp4: %.wav
	ffmpeg -f lavfi -i color=c=black:s=1920x1080:r=5 -i $< -c:a aac -b:a 128k -shortest -max_interleave_delta 200M -fflags +shortest $@

.venv:
	python3 -m venv .venv
	source .venv/bin/activate && pip3 install -r requirements.txt

clean:
	rm -rf .venv
	rm -f *.wav
	rm -f *.mp4
