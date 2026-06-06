import re


class AddressCollector:

    def collect(
        self,
        text
    ):

        pin = re.search(
            r"\b\d{6}\b",
            text
        )

        if pin:

            return pin.group()

        return None