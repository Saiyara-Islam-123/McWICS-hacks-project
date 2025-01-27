import datetime

dict_store = {"Zara" : 1, "Lululemon" : 2, "Hm" : 3, "Clubmonaco": 4, "Thereformation": 5, "Burberry": 6, "Nike": 7, "Maccosmetics": 8}

def encode_store(store):
    return dict_store[store]

class Encoder:

    def __init__(self):
        self.date_to_code = {}
        self.code_to_date = {}
        year = 2024
        start_date = datetime.date(year, 1, 1)
        end_date = datetime.date(year, 12, 31)

        current_date = start_date
        code = 1
        while current_date <= end_date:
            self.date_to_code[current_date.strftime("%m/%d").lstrip('0').replace("/0", "/")] = code
            self.code_to_date[code] = current_date.strftime("%m/%d").lstrip('0').replace("/0", "/")
            code += 1
            current_date += datetime.timedelta(days=1)

    def date_to_code(self, date):
        return self.date_to_code[date]

    def code_to_date(self, c):
        return self.code_to_date[c]