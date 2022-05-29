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


@dataclass
class Info:
    kernel_version: str
    uptime: int
    pkgs: Dict[str, str]


@dataclass
class Record:
    '''
    Not in use yet. But will replace info_to_triples()
    '''
    time: datetime
    info: Info
    message: List[str]


def info_to_triples(record_id: URIRef, info: Info) -> Iterable[T_ANY_TRIPLE]:
    now = Literal(pdl.now())
    yield (record_id, P_A, C_RECORD)
    yield (record_id, P_TIME, now)
    record_node = BNode()
    yield (record_id, P_INFO, record_node)
    yield (record_node, P_KERNEL_VER, Literal(info.kernel_version))
    yield (record_node, P_UPTIME, Literal(info.uptime))
    for pkg_name, pkg_version in info.pkgs.items():
        pkg_node = BNode()
        yield (pkg_node, P_NAME, Literal(pkg_name))
        yield (pkg_node, P_VERSION, Literal(pkg_version))
        yield (record_node, P_PKG, pkg_node)


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

    def add_record(self, record: dict, msg: str = None) -> None:
        '''
        TODO: deduplicate existing records
        '''
        record_id = URIRef('urn:uuid:' + str(uuid4()))
        for triple in info_to_triples(record_id, record):
            self._g.add(triple)
        if msg:
            self._g.add((record_id, P_MSG, Literal(msg)))

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


def get_record() -> Info:
    return Info(get_kernel_version(), get_uptime(), get_pkg_versions())


def add_new_record(msg: str = None):
    storage = Storage(STORAGE_LOCATION)
    record = get_record()
    storage.add_record(record, msg)
    storage.save()
