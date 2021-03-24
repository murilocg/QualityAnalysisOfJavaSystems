#!/bin/bash

pip install pandas gitpython requests
rm -rf ck
git clone https://github.com/mauricioaniche/ck
cd ./ck
mvn clean compile assembly:single