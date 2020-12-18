import datetime
from typing import Union, List

import dateutil.parser
import attr

DEFAULT_HEADINGS = ('time', 'name', 'dob', 'nhs')


def convert_time(val):
    if isinstance(val, datetime.time):
        return val
    try:
        result = dateutil.parser.parse(val).time()
    except ValueError:
        result = None
    return result


def convert_dob(val):
    if isinstance(val, datetime.date):
        return val
    try:
        result = dateutil.parser.parse(val, dayfirst=True).date()
    except ValueError:
        result = None
    return result


def convert_nhs(val):
    if isinstance(val, int):
        return val
    if isinstance(val, str):
        val = val.replace(" ", "")
    try:
        val = int(val)
    except ValueError:
        val = -1
    return val

def repr_nhs(val):
    val = f"{val:010}"
    val = f"{val[0:3]} {val[3:6]} {val[6:10]}"
    return val


@attr.s(auto_attribs=True)
class Person:
    dob: datetime.date = attr.ib(converter=convert_dob, repr=lambda x: f"{x:%d-%m-%Y}")
    nhs: int = attr.ib(converter=convert_nhs, repr=repr_nhs)
    time: datetime.time = attr.ib(converter=convert_time, default="00:00", repr=lambda x: f"{x:%H:%M}")
    name: str = ""
    status: str = "imported"
    error_type: str = ""
    image: bytes = attr.ib(default=b"", repr= lambda x: f"{x != b''}")
    vaccinator_initials: str = ""
    vaccinator: str = ""

    @time.validator
    def _time_validator(self, attribute, value):
        if value is None:
            self.set_error("Invalid Time read")

    @dob.validator
    def _dob_validator(self, attribute, value):
        if value is None:
            self.set_error("Invalid DOB read")

    @nhs.validator
    def _nhs_validator(self, attribute, value):
        if value <= 0:
            self.set_error("Invalid NHS number")
        if value >= 10000000000:
            self.set_error("Invalid NHS number")

    def set_error(self, reason):
        self.status = "error"
        self.error_type = reason


    def get_text(self, heading):
        field = getattr(attr.fields(type(self)),heading)
        var = getattr(self, heading)
        if isinstance(field.repr, bool):
            return str(var)
        else:
            return field.repr(var)

    def get_texts(self, headings = DEFAULT_HEADINGS):
        """Get a list of strings for each heading"""
        return[self.get_text(heading) for heading in headings]


class Everyone(list):
    def __init__(self):
        super().__init__()

    def filter(self, **kwargs) -> List[Person]:
        lst = self
        for key, value in kwargs.items():
            lst = [x for x in lst if getattr(x, key) == value]
        return lst

    def get_by_nhs(self, nhs: int) -> Union[None, Person]:
        results = self.filter(nhs=nhs)
        if len(results) >= 1:
            return results[0]
        else:
            return None

    def append(self, person: Person):
        match = self.get_by_nhs(person.nhs)
        if match is not None:
            person.set_error("Duplicate NHS number")
        super().append(person)

    def extend(self, lst: List[Person]):
        for p in lst:
            self.append(p)

    def update(self, person: Person):
        match = self.get_by_nhs(person.nhs)
        if match is None:
            person.set_error("NHS number not found")
            self.append(person)
            return
        if match.dob != person.dob:
            print(f"dob mismatch {match.dob} {person.dob}", type(match.dob), type(person.dob))
            person.set_error(f"DOB mismatch: {match.dob} vs {person.dob}")
            self.append(person)
            return
        match.status = person.status
        match.vaccinator_initials = person.vaccinator_initials
        match.vaccinator = person.vaccinator
        match.image = person.image
        match.error_type = person.error_type

