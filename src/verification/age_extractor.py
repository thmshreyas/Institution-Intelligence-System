import re


class AgeExtractor:

    def extract_year(self, search_result):

        text = ""

        if "knowledgeGraph" in search_result:

            kg = search_result["knowledgeGraph"]

            text += str(kg)

        for item in search_result.get("organic", []):

            text += " " + item.get("snippet", "")

        years = re.findall(r"(18\d{2}|19\d{2}|20\d{2})", text)

        if years:

            return int(years[0])

        return None
