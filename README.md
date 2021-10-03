# FR Political dataset generator 🇫🇷
This is a CLI for political corpus generation. It collects political speeches of French politicians from 1974 to nowadays with the help of [vie-publique.fr](https://www.vie-publique.fr/). It feeds this information with the various political parties identified by [politologue.com](https://www.politologue.com).

The result is a folder named `generated` containing speeches corpus with the path `generated/{path}/{party}/{year}/{speaker}/{speech_name}`.

# Prerequisites
Install packages with pip:
```
pip install -r requirements.txt
```

# Generate parties CSV
First you need to generate the parties file with the CLI:
```
python3 cli.py parties
```
It has the following options:
```
Usage: cli.py parties [OPTIONS]

Options:
  --verbose BOOLEAN  Default false
  --help             Show this message and exit.
```

The resulting file has the following form:
```csv
name, party
Emmanuel Macron,En Marche
...
```

# Generate speeches corpus
You need the parties CSV file to generate the corpus, which can be created with the command `cli.py parties`, or directly using the `--create-parties` flag.

Retrieve speeches using the CLI:
```
python3 cli.py speeches
```
It has the following options:
```
Usage: cli.py speeches [OPTIONS]

Options:
  --verbose BOOLEAN    Default false
  --from-page INTEGER  Page to start from. Start at 0 (inclusive)
  --to-page INTEGER    Page to end at (exclusive). Default stops when there
                       are no more speeches.
  --create-parties     Create parties file directly
  --help               Show this message and exit.
```
Note that each page has 12 different speeches, but we only retrieve speeches with only one speaker.

The content of speeches are written in files using the following path:
`generated/{path}/{party}/{year}/{speaker}/{speech_name}`
