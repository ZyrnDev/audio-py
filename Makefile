SHELL := /bin/bash

.PHONY: clean

FILE := output.wav

all: .venv
	source .venv/bin/activate && python3 main.py $(FILE)

# ffmpeg -f lavfi -i color=c=black:s=1920x1080:r=5 -i output.wav -c:a aac -b:a 128k -shortest -max_interleave_delta 200M -fflags +shortest output.mp4

.venv:
	python3 -m venv .venv
	source .venv/bin/activate && pip3 install -r requirements.txt

clean:
	rm -rf .venv
