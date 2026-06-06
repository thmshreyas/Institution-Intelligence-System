from datetime import datetime


class AgeVerifier:

    def verify(self, establishment_year):

        if establishment_year is None:

            return {
                "passed": False,
                "age": None,
            }

        current_year = datetime.now().year

        age = current_year - establishment_year

        return {"passed": age >= 50, "age": age, "year": establishment_year}
