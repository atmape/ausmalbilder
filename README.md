# Download von Ausmalbildern

Es werden verschiedene Seiten für Ausmalbildern mittels [`scrapy`](https://scrapy.org/) durchsucht und ein 
Download der Bilder (und falls notwendig in PDF umgewandelt) durchgeführt

## Setup

```
# Virtual Environment 
python3 -m venv venv
# aktivieren
. ./bin/activate
# Abhängigkeiten installieren
pip install -r requirements.txt
cd ausmalbilder
scrapy crawl <name>

```

## Aufrufe

| SCRAPY Aufruf | Dateityp | Anmerkung |
| --- | --- | --- |
| `scrapy crawl malvorlagen-bilder.de` | PDF | Direkt von Seite|
| `scrapy crawl ausmalbilder.org` | PDF | Bilder werden zu PDF umgewandelt - Viele Bilder!|