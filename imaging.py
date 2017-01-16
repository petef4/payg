class Imaging:
    """Map the name of a logo file to its CSS offset in the sprite file.
    """
    def __init__(self):
        self.load()

    def load(self):
        """Read the conf file to get the logo filenames."""
        self.logo = []
        with open('logos.conf', encoding='UTF-8') as f:
            for line in f:
                record = line.strip()
                if record != '' and not record.startswith('#'):
                    self.logo.append(record)

    def add_logo_pos(self, data):
        """Update data to add logo_pos elements.

        data is modified.
        """
        for row in data:
            if 'operator.logo' in row:
                index = self.logo.index(row['operator.logo'])
                row['operator.logo_pos'] = index * -24 - 4
