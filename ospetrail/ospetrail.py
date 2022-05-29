'''

'''

import pendulum as pdl
from pendulum import datetime
from pathlib import Path
from rdflib import Graph, URIRef, Literal, BNode
from rdflib.namespace import RDF
from uuid import uuid4
from typing import Dict, Iterable, List, Tuple, Union
from dataclasses import dataclass
from pprint import pprint

import platform
import uptime
from pyalpm import Handle


alpm_handle = Handle('.', '/var/lib/pacman')
localdb = alpm_handle.get_localdb()


T_ANY_TRIPLE = Tuple[Union[str, URIRef], URIRef, Union[URIRef, Literal]]


STORAGE_LOCATION = Path.home() / 'logs/ospetrail'
DB_FILE = 'db.ttl'

PACKAGES = [
        'linux',
        'linux-lts',
        'mesa',
        'xf86-video-intel',
        'plasma-desktop',
        'xorg-server',
        'wayland',
        ]


def U(TERM):
    return URIRef(f"{NAMESPACE}#{TERM}")


P_A = RDF.type
NAMESPACE = 'urn:ryey:ospetrail'
P_MSG = U('message')
P_TIME = U('time')
P_INFO = U('info')
P_KERNEL_VER = U('kernel_version')
P_UPTIME = U('uptime')
P_PKG = U('package')
P_NAME = U('name')
P_VERSION = U('version')
C_RECORD = U('Record')


def one(result):
    lst = list(result)
    assert len(lst) == 1
    return lst[0]


def one_or_none(result):
    lst = list(result)
    if len(lst) == 0:
        return None
    elif len(lst) == 1:
        return lst[0]
    else:
        assert len(lst) in {0, 1}


@dataclass
class Info:
    '''
    An info represents the system and package information at the time of recording.
    '''
    kernel_version: str
    uptime: int
    pkgs: Dict[str, str]


@dataclass
class Record:
    '''
    A record represents a full record of a trail.
    '''
    record_id: URIRef
    time: datetime
    info: Info
    message: str

    def to_triples(self) -> Iterable[T_ANY_TRIPLE]:
        yield (self.record_id, P_A, C_RECORD)
        yield (self.record_id, P_TIME, Literal(self.time))
        record_node = BNode()
        yield (self.record_id, P_INFO, record_node)
        yield (record_node, P_KERNEL_VER, Literal(self.info.kernel_version))
        yield (record_node, P_UPTIME, Literal(self.info.uptime))
        for pkg_name, pkg_version in self.info.pkgs.items():
            pkg_node = BNode()
            yield (pkg_node, P_NAME, Literal(pkg_name))
            yield (pkg_node, P_VERSION, Literal(pkg_version))
            yield (record_node, P_PKG, pkg_node)
        yield (self.record_id, P_MSG, Literal(self.message))


class Storage:
    def __init__(self, location: str):
        p_loc = Path(location)
        if not p_loc.is_dir():
            if not p_loc.exists():
                p_loc.mkdir()
            else:
                print(f"Location {location} is not a directory")
                assert False
        self._location = location
        self._g = Graph()
        db_p = Path(location) / DB_FILE
        if db_p.exists():
            self._g.parse(db_p)

    def add_record(self, record: Record) -> None:
        '''
        TODO: deduplicate existing records
        '''
        for triple in record.to_triples():
            self._g.add(triple)

    def get_record(self, record_id: URIRef) -> Record:
        time = one(self._g.objects(record_id, P_TIME)).toPython()
        message = one(self._g.objects(record_id, P_MSG)).toPython()
        info_node = one(self._g.objects(record_id, P_INFO))
        kernel_ver = one(self._g.objects(info_node, P_KERNEL_VER)).toPython()
        uptime = one(self._g.objects(info_node, P_UPTIME)).toPython()
        pkgs = {}
        for pkg_node in self._g.objects(info_node, P_PKG):
            name = one(self._g.objects(pkg_node, P_NAME)).toPython()
            version = one(self._g.objects(pkg_node, P_VERSION)).toPython()
            pkgs[name] = version
        info = Info(kernel_version=kernel_ver, uptime=uptime, pkgs=pkgs)
        record = Record(record_id=record_id,
                        time=time, info=info, message=message)
        return record

    def list_records(self) -> List[Record]:
        return [self.get_record(record_id)
                for record_id in self._g.subjects(P_A, C_RECORD)]

    def save(self) -> None:
        db_p = Path(self._location) / DB_FILE
        self._g.serialize(db_p)


def get_kernel_version() -> str:
    '''
    Kernel version
    '''
    return platform.release()


def get_uptime() -> int:
    '''
    Uptime in seconds
    '''
    return int(uptime.uptime())


def get_pkg_versions() -> Dict[str, str]:
    '''
    All interested package versions
    See PACKAGES for the list of interested packages
    Only supports pacman (archlinux)
    '''
    ret = {}
    for pkg_name in PACKAGES:
        pkg = localdb.get_pkg(pkg_name)
        if pkg:
            version = pkg.version
            ret[pkg_name] = version
        else:
            print(f"Package {pkg_name} is not found in local database")
    return ret


def get_record(msg: str) -> Record:
    info = Info(get_kernel_version(), get_uptime(), get_pkg_versions())
    record_id = URIRef('urn:uuid:' + str(uuid4()))
    now = pdl.now()
    return Record(record_id=record_id,
                  time=now, info=info, message=msg)


def add_new_record(msg: str):
    storage = Storage(STORAGE_LOCATION)
    record = get_record(msg)
    storage.add_record(record)
    storage.save()


def list_records():
    storage = Storage(STORAGE_LOCATION)
    pprint(storage.list_records())
