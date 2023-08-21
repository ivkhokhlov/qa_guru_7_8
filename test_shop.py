"""
Протестируйте классы из модуля homework/models.py
"""
import pytest

from models import Product, Cart


@pytest.fixture
def product_book():
    return Product("book", 100, "This is a book", 1000)


@pytest.fixture
def product_phone():
    return Product('phone', 9000, 'This is a phone', 10)


@pytest.fixture
def empty_cart():
    return Cart()


@pytest.fixture
def filled_cart(product_book, product_phone):
    cart = Cart()
    cart.add_product(product_book)
    cart.add_product(product_phone)
    return cart


class TestProducts:
    """
    Тестовый класс - это способ группировки ваших тестов по какой-то тематике
    Например, текущий класс группирует тесты на класс Product
    """

    def test_product_check_quantity(self, product_book):
        # TODO напишите проверки на метод check_quantity
        assert product_book.check_quantity(999) is True
        assert product_book.check_quantity(1000) is True

    def test_product_check_quantity_negative(self, product_book):
        # TODO напишите проверки на метод check_quantity
        assert product_book.check_quantity(1001) is False

    def test_product_buy(self, product_book):
        # TODO напишите проверки на метод buy
        product_book.buy(100)
        assert product_book.quantity == 900

    def test_product_buy_more_than_available(self, product_book):
        # TODO напишите проверки на метод buy,
        #  которые ожидают ошибку ValueError при попытке купить больше, чем есть в наличии
        with pytest.raises(ValueError):
            product_book.buy(1001)
        assert product_book.quantity == 1000


class TestCart:
    """
    TODO Напишите тесты на методы класса Cart
        На каждый метод у вас должен получиться отдельный тест
        На некоторые методы у вас может быть несколько тестов.
        Например, негативные тесты, ожидающие ошибку (используйте pytest.raises, чтобы проверить это)
    """

    def test_add_product_default_buy_count(self, empty_cart, product_book):
        empty_cart.add_product(product_book)
        assert empty_cart.products[product_book] == 1

    def test_add_product_nonedefault_buy_count(self, empty_cart, product_book):
        empty_cart.add_product(product_book, buy_count=10)
        assert empty_cart.products[product_book] == 10

    def test_add_product_one_more(self, filled_cart, product_book):
        filled_cart.add_product(product_book)
        assert filled_cart.products[product_book] == 2

    def test_remove_product_same_quantity(self, filled_cart, product_book):
        filled_cart.remove_product(product_book)
        assert filled_cart.products.get(product_book) is None

    def test_remove_greter_then_added(self, empty_cart, product_book):
        empty_cart.add_product(product_book, 10)
        empty_cart.remove_product(product_book, 100)
        assert empty_cart.products.get(product_book) is None

    def test_remove_less_then_added(self, empty_cart, product_book):
        empty_cart.add_product(product_book, 10)
        empty_cart.remove_product(product_book, 5)
        assert empty_cart.products.get(product_book) == 5

    def test_remove_nonexisted_product(self, empty_cart, product_book):
        with pytest.raises(ValueError):
            empty_cart.remove_product(product_book)
        assert empty_cart.products == {}

    def test_clear_cart(self, filled_cart):
        filled_cart.clear()
        assert filled_cart.products == {}

    def test_get_total_price(self, filled_cart):
        assert filled_cart.get_total_price() == 9100

    def test_get_total_price_empty_cart(self, empty_cart):
        assert empty_cart.get_total_price() == 0

    def test_buy_valid(self, filled_cart):
        filled_cart.buy()
        assert filled_cart.products == {}

    def test_buy_empty_cart(self, empty_cart):
        with pytest.raises(Exception) as e:
            assert e == 'Корзина пуста'

    def test_buy_more_then_quantity(self, empty_cart, product_book):
        empty_cart.add_product(product_book, 10000)
        with pytest.raises(ValueError):
            empty_cart.buy()
        assert empty_cart.products != {}
        assert empty_cart.products[product_book] == 10000
