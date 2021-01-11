import urllib.request
from pathlib import Path
import pandas as pd
from PIL import Image, ImageTk
import io

base_path = Path(__file__).parent
database_path = (base_path / "data/filteredDatabase.csv").resolve()
recommendations = pd.read_csv(open(database_path, encoding="utf-8"))

for index in range(len(recommendations.index)):
    print(recommendations.iloc[index])
    print(index)
    row = recommendations.iloc[index]
    url = row['Image']
    print(url)
    raw_data = urllib.request.urlopen(url).read()
    im = Image.open(io.BytesIO(raw_data))
