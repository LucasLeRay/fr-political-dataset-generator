# Prerequisites
Install packages with pip:
```
pip install -r requirements.txt
```

# Generate parties CSV
Generate parties CSV from [politologue.com](https://www.politologue.com):
```
python3 generate_parties.py
```
The parties CSV has the following form:
```csv
name, parties
Emmanuel Macron,En Marche
...
```

# Generate speeches corpus
Once you've generated parties CSV, you can create corpus files for each speech from [vie-publique.fr](https://www.vie-publique.fr/):
```
python3 generate_speeches.py
```
The content of speeches are written in files using the following path:
`generated/{path}/{party}/{year}/{speaker}/{speech_name}`
