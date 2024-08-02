import matplotlib.pyplot as plt


def plot_expenses_by_category(transactions):
    categories = {}
    for transaction in transactions:
        if transaction.category in categories:
            categories[transaction.category] += transaction.amount
        else:
            categories[transaction.category] = transaction.amount

    plt.bar(list(categories.keys()), list(categories.values()))
    plt.xlabel('Category')
    plt.ylabel('Amount')
    plt.title('Expenses by Category')
    plt.show()