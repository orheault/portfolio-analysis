class SecurityFormatter:
    def __init__(self):
        self.rows = []

    def __call__(self, line):
        row_content_split = line.split('|')
        self.rows.append(row_content_split)
