# DataPilot

Demo Flask per controllare la qualità di file CSV: celle vuote, righe duplicate, intestazioni duplicate, spazi superflui e righe con un numero inatteso di colonne.

## Avvio

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python app.py
```

Apri http://127.0.0.1:5000.

## Test

```powershell
python -m unittest discover -s tests -v
```

Prototipo didattico per la sfida Big Data Developer - Sfida 2. Non è una piattaforma Big Data pronta per la produzione.