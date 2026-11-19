# AutoScout24 scraping

Collects used-car listings from the French AutoScout24 site and stores them as CSV files. `scripts/main.py` drives Chrome with Selenium, walks brand and model pages, and writes one CSV per model. `scripts/concatenation.py` stacks those files into a single table.

The checked-in data is the output of that run: per-model files in `separated-results/` and the merged file `final-result/autoscout-brut-data.csv` (about 37,500 rows).

## What it collects

Each listing row has these columns:

| Column | Source on the listing card |
| --- | --- |
| `model_name` | First line of the `h2` title |
| `extended_name` | Version text (`ListItem_version`) |
| `price` | Current price |
| `price_judgement` | Price label, such as “Pas d'information” |
| `kilometers` | Mileage (`VehicleDetails-mileage_road`) |
| `transmission` | Gearbox (`VehicleDetails-transmission`) |
| `release_date` | Registration date (`VehicleDetails-calendar`) |
| `fuel` | Fuel type (`VehicleDetails-gas_pump`) |
| `power` | Power (`VehicleDetails-speedometer`) |
| `owner` | Present in the header, never filled |
| `owner_adress` | Present in the header, never filled |

Missing fields stay empty. The scraper does not open the listing detail page.

## How the scraper walks the site

`scripts/main.py` opens Chrome, then visits each brand URL in `companies_urls`. The list in the script is the French brand pages for Audi, BMW, Citroën, Dacia, Ferrari, Ford, Morgan, Peugeot, Porsche, Renault, Tesla, and Toyota.

On each brand page it:

1. Clicks **Accepter tout** when the cookie banner is there.
2. Clicks **Afficher tout** so the full model list is visible.
3. Opens a top-model tile (`TopModels_model`), then **Afficher toutes les annonces**.
4. Reads every listing card on the page.
5. Clicks **Aller à la page suivante** until that button is gone, reading listings on each page.
6. Returns to the brand page and writes `brand-index.csv` in the current working directory. The brand name is taken from the URL (`audi-0.csv`, `bmw-1.csv`, and so on). The dataframe is cleared before the next model.

`separated-results/` also contains files for brands that are not in the current URL list, including Mercedes-Benz, Volkswagen, Volvo, Škoda, Opel, Hyundai, Mazda, Nissan, Mitsubishi, and Suzuki. Those files come from an earlier run.

## Merge script

`scripts/concatenation.py` is meant to be run from the `scripts/` directory. It reads every CSV in `../separated-results/` and writes `../final-result/autoscout-brut-data.csv` without adding a new index. The merged file still has an `Unnamed: 0` column because `main.py` saves the pandas index.

## Requirements

- Python with `selenium`, `webdriver-manager`, `pandas`, and `numpy` (`numpy` and `webdriver-manager` are imported but not used)
- Google Chrome
- A ChromeDriver executable

There is no `requirements.txt`. Install the libraries the scripts import:

```bash
pip install selenium webdriver-manager pandas numpy
```

## Run

The driver path is hardcoded for a Windows machine:

```text
C:\Users\windows\Desktop\chromedriver-win64\chromedriver.exe
```

Change `path` in `scripts/main.py` before starting. Chrome is left open after the script finishes (`detach`).

```bash
cd autoscout24-scraping/scripts
python main.py
```

Move the new `brand-index.csv` files into `separated-results/`, then merge them:

```bash
cd autoscout24-scraping/scripts
python concatenation.py
```

## Layout

| Path | Role |
| --- | --- |
| `scripts/main.py` | Selenium scraper and per-model CSV writer |
| `scripts/concatenation.py` | Concatenates every file in `separated-results/` |
| `separated-results/` | One CSV per brand and model index |
| `final-result/autoscout-brut-data.csv` | All of those rows in one file |
