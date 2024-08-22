run:
	python src/bot.py

zip: 
	sh scripts/zip.sh
	mv archive.zip ~/Desktop 