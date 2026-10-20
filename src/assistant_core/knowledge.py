class OfficeDirectory:
    @classmethod
    def from_csv(cls, path):
        # Trả về một object rỗng tạm thời để test không bị crash
        return cls()


class Handbook:
    @classmethod
    def from_json(cls, path):
        return cls()
