#!/bin/sh

alembic upgrade head
python -m fastapi run main.py --host 0.0.0.0
