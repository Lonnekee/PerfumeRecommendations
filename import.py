import pandas as pd


def load_data(file):
    data = pd.read_csv(file)
    data = data.set_index('Handle')

    # Print full database
    print(data)

    # Get specific column
    print(data['Title'])

    # Search for all products with specific tag
    rows = data['Tags'].str.contains('ingr:amber') == True
    print(data[rows].index)

    # Updating truth-values of certain rows only
    truth_values = [0] * len(data.index)
    data['rank'] = truth_values
    data.loc[rows, ['rank']] += 1
    print(data.loc[:, ['rank']])

    # Selecting perfumes of or under a certain price
    budget = 100.0
    indices = data[data["Price"] > budget].index
    data.drop(labels=indices, inplace=True)
    print(data['Price'])


def main():
    data = load_data('filteredDatabase.csv')


if __name__ == "__main__":
    main()
