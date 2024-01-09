#!/bin/bash
python3 -m venv venv;
source venv\bin\activate;
mkdir temp temp_out videos_out;
pip install -r requirements.txt;
python app.py
