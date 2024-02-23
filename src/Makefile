OS := $(shell uname)
ifeq $(OS) Windows_NT
	ACTIVATE := venv\Scripts\activate.bat
endif
ifeq $(OS) Linux
	ACTIVATE := source venv/bin/activate
endif
ifeq $(OS) Darwin
	ACTIVATE := source venv/bin/activate
endif

install:
	python3.11 -m venv venv
	$(ACTIVATE)
	docker-compose up
	deactivate

run:
	$(ACTIVATE) && cd server && python main.py && explorer "https://localhost:8080"
