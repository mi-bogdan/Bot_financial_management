from core.db.models import TransactionsType

category_list = [
    {"title": "Заработная плата", "transactions_type": TransactionsType.income},
    {"title": "Фриланс", "transactions_type": TransactionsType.income},
    {"title": "Инвестиции", "transactions_type": TransactionsType.income},
    {"title": "Подарки", "transactions_type": TransactionsType.income},
    {"title": "Пенсия", "transactions_type": TransactionsType.income},
    {"title": "Прочие доходы", "transactions_type": TransactionsType.income},
    {"title": "Продукты", "transactions_type": TransactionsType.expenses},
    {"title": "Коммунальные платежи", "transactions_type": TransactionsType.expenses},
    {"title": "Образование", "transactions_type": TransactionsType.expenses},
    {"title": "Здоровье", "transactions_type": TransactionsType.expenses},
    {"title": "Досуг и развлечения", "transactions_type": TransactionsType.expenses},
    {"title": "Одежда и аксессуары", "transactions_type": TransactionsType.expenses},
]
