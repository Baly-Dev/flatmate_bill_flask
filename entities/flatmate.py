class Flatmate:
    """
    object that rappresents the user - flatmate - and defines in 
    which quantity a flatmate should pay the bill for the days 
    spent in the house
    """

    def __init__(self, name, days_in_house):
        self.name = name
        self.days_in_house = days_in_house

    def pays(self, bill, flatmate):
        weight = round(self.days_in_house / (self.days_in_house + flatmate.days_in_house), 1)
        return bill.amount * weight
