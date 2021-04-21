import datetime
from typing import Union, List, Sequence

import dateutil.parser
import attr
import threading
from . import batch

DEFAULT_HEADINGS = ('time', 'name', 'dob', 'nhs')


def convert_time(val):
    if isinstance(val, datetime.time):
        return val
    try:
        result = dateutil.parser.parse(val).time()
    except ValueError:
        result = datetime.time(0, 0)
    return result


def convert_dob(val):
    if isinstance(val, datetime.date):
        return val
    try:
        result = dateutil.parser.parse(val, dayfirst=True).date()
    except (ValueError, OverflowError):
        result = None
    return result


def convert_nhs(val):
    if isinstance(val, int):
        return val
    if isinstance(val, str):
        val = val.replace(" ", "")
    try:
        val = int(val)
    except (ValueError, TypeError):
        val = -1
    return val


def convert_name(val: str):
    return val.title()


def repr_nhs(val):
    if val == -1:
        return ""
    val = f"{val:010}"
    val = f"{val[0:3]} {val[3:6]} {val[6:10]}"
    return val


# noinspection PyUnresolvedReferences,PyUnusedLocal,PyClassHasNoInit
@attr.s(auto_attribs=True)
class Person:
    dob: datetime.date = attr.ib(converter=convert_dob, repr=lambda x: f"{x:%d-%m-%Y}")
    nhs: int = attr.ib(converter=convert_nhs, repr=repr_nhs)
    time: datetime.time = attr.ib(converter=convert_time, default="00:00", repr=lambda x: f"{x:%H:%M}")
    name: str = attr.ib(converter=convert_name, default="")
    status: str = "imported"
    error_type: str = ""
    image: bytes = attr.ib(default=b"", repr=lambda x: f"{x != b''}")
    vaccinator_initials: str = ""
    vaccinator: str = ""
    drawer: str = ""
    batch_no: batch.BatchInfo = None
    lock: threading.Lock = attr.ib(factory=threading.Lock, init=False)
    upload_attempts: int = 0

    @time.validator
    def _time_validator(self, attribute, value):
        if value is None:
            self.time = datetime.time(0, 0)
            self.set_error("Invalid Time read")

    @dob.validator
    def _dob_validator(self, attribute, value):
        if value is None:
            self.dob = datetime.date(1800, 1, 1)
            self.set_error("Invalid DOB read")

    @nhs.validator
    def _nhs_validator(self, attribute, value):
        if value >= 10000000000:
            self.set_error("Invalid NHS number")

    def set_error(self, reason):
        with self.lock:
            self.status = "error"
            self.error_type = reason

    def get_text(self, heading):
        with self.lock:
            field = getattr(attr.fields(type(self)), heading)
            var = getattr(self, heading)
            if isinstance(field.repr, bool):
                return str(var)
            else:
                return field.repr(var)

    def get_texts(self, headings: Sequence[str] = DEFAULT_HEADINGS):
        """Get a list of strings for each heading"""
        return [self.get_text(heading) for heading in headings]

    def name_match(self, search_name: str):
        with self.lock:
            name_lower_parts = self.name.lower().split()
            search_parts = search_name.strip().split()
            return all(any(n.startswith(part) for n in name_lower_parts) for part in search_parts)


class Everyone(list):
    def __init__(self):
        super().__init__()

    def filter(self, **kwargs) -> List[Person]:
        lst = sorted(self, key=lambda x: x.time)
        for key, value in kwargs.items():
            lst = [x for x in lst if getattr(x, key) == value]
        return lst

    def get_by_nhs(self, nhs: int) -> Union[None, Person]:
        results = self.filter(nhs=nhs)
        if len(results) >= 1:
            return results[0]
        else:
            return None

    def get_by_time_and_dob(self, time, dob) -> Union[None, Person]:
        if not isinstance(time, datetime.time):
            return None
        results = self.filter(time=time, dob=dob)
        if len(results) >= 1:
            return results[0]
        else:
            return None

    def append(self, person: Person):
        if person.nhs == -1:
            match = self.get_by_time_and_dob(person.time, person.dob)
            if match is not None:
                person.set_error("Duplicate time and dob")
        else:
            match = self.get_by_nhs(person.nhs)
            if match is not None:
                print(f"Duplicate found: {person}\n vs: {match}")
                person.set_error("Duplicate NHS number")
        super().append(person)

    def extend(self, lst: List[Person]):
        for p in lst:
            self.append(p)

    def update(self, person: Person):
        if person.nhs == -1:
            match = self.get_by_time_and_dob(person.time, person.dob)
        else:
            match = self.get_by_nhs(person.nhs)
        if match is None:
            person.set_error("Matching patient not found")
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

    def get_vaccinators(self):
        # noinspection PyTypeChecker
        return list({p.vaccinator for p in self if p.vaccinator})

    def get_name_matches(self, name, status="imported"):
        filtered = self.filter(status=status)
        if name:
            return [p for p in filtered if p.name_match(name.lower())]
        else:
            return filtered
