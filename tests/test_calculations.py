import pytest
from app.calculations import add, subtract, multiply, divide, BankAccount, InsufficientFunds

# pytest -v -s -x
# -v: increase verbosity, print more informmation
# -- disable warnings
# -x: stop at first failure

# fixtures used to avoid repetition of code
# fixtures really shine by when saving the developer time to initialise a db or email service for example

@pytest.fixture # create empty bank account
def zero_bank_account():
    return BankAccount()

@pytest.fixture
def bank_account():
    return BankAccount(50)

# to automate repeate testing with multiple values 
@pytest.mark.parametrize("num1, num2, expected", [
    (3, 2, 5), 
    (4, 3, 7), 
    (12, 4, 16)
])
def test_add(num1, num2, expected):
    print("testing add function")
    assert add(num1, num2) == expected

def test_subtract():
    print("testing subtract function")
    assert subtract(45,5) == 40

def test_multiply():
    assert multiply (8, 8) == 64

def test_divide():
    assert divide (44, 11) == 4  



def test_bank_set_initial_amount(bank_account):
    # checks if an account is created with specified balance
    assert bank_account.balance == 50

def test_bank_default_amount(zero_bank_account):
    # checks if an account is created with default balance of 0
    assert zero_bank_account.balance == 0

def test_withdraw(bank_account):
    bank_account.withdraw(20)
    assert bank_account.balance == 30

def test_deposit(bank_account):
    bank_account.deposit(20)
    assert bank_account.balance == 70

def test_collect_interest(bank_account):
    bank_account.collect_interest()
    assert round(bank_account.balance, 6) == 55

@pytest.mark.parametrize("deposited, withdrew, expected", [
    (200, 100, 100), 
    (50, 10, 40), 
    (1200, 200, 1000),
])
def test_bank_transaction(zero_bank_account, deposited, withdrew, expected):
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdrew)
    assert zero_bank_account.balance == expected

def test_insufficient_funds(bank_account):
    with pytest.raises(InsufficientFunds):
        bank_account.withdraw(200)

