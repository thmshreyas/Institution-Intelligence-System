class ConfidenceScorer:

    def score(self, row):

        score = 0

        if row["website"]:
            score += 20

        if row["established_year"]:
            score += 15

        if row["engineering"]:
            score += 15

        if row["mba"]:
            score += 15

        if row["phd"]:
            score += 15

        if row["vice_chancellor"]:
            score += 10

        if row["address"]:
            score += 10

        return min(score, 100)