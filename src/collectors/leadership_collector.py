import re


class LeadershipCollector:

    def collect(
        self,
        text
    ):

        patterns = [

            r"Vice Chancellor[:\s]+([A-Za-z.\s]+)",

            r"Vice-Chancellor[:\s]+([A-Za-z.\s]+)",

            r"Chancellor[:\s]+([A-Za-z.\s]+)"

        ]

        for pattern in patterns:

            match = re.search(
                pattern,
                text,
                re.IGNORECASE
            )

            if match:

                return (
                    match.group(1)
                    .strip()
                )

        return None