class Bill:
    """
    object that represents a bill and is defined by a total amount
    in ($) and a specific period of time in (dd)
    """

    def __init__(self, amount, period):
        self.amount = amount
        self.period = period