import pandas as pd


def load_data(file):
    data = pd.read_csv(file)
    data = data.set_index('Handle')

    # Print full database
    print(data)

    # Get specific column
    print(data['Title'])

    # Search for all products with specific tag
    print(data[data['Tags'].str.contains('ingr:amber') == True].index)


def main():
    data = load_data('filteredDatabase.csv')


if __name__ == "__main__":
    main()
