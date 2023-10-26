import re

class ProductName:
    def __init__(self, full_name):
        # Initialize
        self.full_name = full_name
        self.name = full_name

        # Extract formula
        self.get_formula()
        if self.formula != None:
            self.name = self.name.replace(self.formula, '')

        # Keep alphanumeric and add space after numeric
        self.name = re.sub(r'[^a-zA-Z0-9% ]', '', self.name)
        self.name = self.name.replace(r'(?<=[0-9])(?=[a-zA-Z])', ' ')

        # Extract metrics
        self.get_metrics()
        if self.metrics != None:
            self.name = self.name.replace(self.metrics, '')

    def get_formula(self):
        # Extract formula
        pattern_formula = r'(\d+-?\d+-\d+(?:-\d+-\d+)?)(?=\+|\s|[A-Za-z]|$)'
        self.formula = re.search(pattern_formula, self.full_name)
        if self.formula != None:
            self.formula = self.formula.group()

        return self.formula
    
    def get_metrics(self):
        # Extract metrics
        pattern_metrics = r'(\d+\s*[A-Za-z]+\s*|\d+\s*%\s*|\d+[A-Za-z]+\s*)$'
        self.metrics = re.search(pattern_metrics, self.name)
        if self.metrics != None:
            self.metrics = self.metrics.group()
            # Revise metrics
            pattern_pesticide = r'EC|SC|SL|AS|F|FW|FS|D|GR|B|RB|RMB|BB|WG|WDG|SG|WP|SP|SD|MC|PA|LT|CS|OD|DF|ULV|LV'
            if re.search(rf'(?i)\d+\s({pattern_pesticide})\s*$', self.metrics):
                self.metrics = None

        return self.metrics


product = ProductName('Extra One 680 SC @ 500 ml 12-0-15')
print(product.full_name)
print(product.name)
print(product.formula)
print(product.metrics)
