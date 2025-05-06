class Assignment:
    def __init__(self, title, description, price, get_order_button):
        self.title = title
        self.description = description
        self.price = price
        self.get_order_button = get_order_button

    @staticmethod
    def standarize_price(price_element):
        value = ".".join(price_element.text.replace("$", "").split("\n"))
        return float(value)
    
    def should_click_on_order_button(self, checkers):
        print("Processing assignment:", self.__repr__())
        for checker in checkers:
            if checker.check(self):
                return True
        return False

    def __repr__(self):
        return f'<Assignment title="{self.title}" description="{self.description}" price="$ {self.price}">'


