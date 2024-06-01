from aiogram.fsm.state import State, StatesGroup


class TransactionsForm(StatesGroup):
    category = State()
    amount = State()
    type = State()


class BudgetsForm(StatesGroup):
    category = State()
    limit = State()
    type_limit = State()


class ApprovalForm(StatesGroup):
    category = State()
    approval = State()
