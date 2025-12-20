class Player:
    def __init__(self, row):
        self.name = row['Name']
        self.stats = row
        self.probs = self.calculate_probs()

    def calculate_probs(self):
        pa = float(self.stats['PA'])
        if pa == 0: return {'out': 1.0}

        h = int(self.stats['H'])
        doubles = int(self.stats['2B'])
        triples = int(self.stats['3B'])
        hr = int(self.stats['HR'])
        bb = int(self.stats['BB'])
        hbp = int(self.stats['HBP'])

        singles = h - doubles - triples - hr
        walks = bb + hbp
        outs = pa - (singles + doubles + triples + hr + walks)

        return {
            'single': singles / pa,
            'double': doubles / pa,
            'triple': triples / pa,
            'hr': hr / pa,
            'walk': walks / pa,
            'out': outs / pa
        }
