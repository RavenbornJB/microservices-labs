import sys
from typing import Union
from enum import Enum


class Services(Enum):
    FACADE = 0
    LOGGING = 1
    MESSAGES = 2


PORT_RANGES = {
    Services.FACADE: (8080, 8090),
    Services.LOGGING: (8090, 9000),
    Services.MESSAGES: (9000, 9010)
}


def validate_port(port_str, service):
    try:
        port = int(port_str)
    except ValueError:
        raise ValueError(f'`port` must be an integer (i.e. 8080), provided was {sys.argv[1]}')

    if not (PORT_RANGES[service][0] <= port < PORT_RANGES[service][1]):
        raise ValueError(f'`port` must be in the range [{PORT_RANGES[service][0]}, {PORT_RANGES[service][1]}),'
                         f' provided was {port}')

    return port


def parse_port(argv_order: int, service: int):
    """
    Parses a network port from argv
    :param argv_order: argument order (0-indexed, 0 is the program name)
    :param service: member of Services enum
    :return: port number
    """
    if len(sys.argv) < argv_order + 1:
        return PORT_RANGES[service][0]  # first available port

    port = validate_port(sys.argv[argv_order], service)
    return port


def parse_ports(argv_order: int, service: int):
    """
    Parses a network port from argv
    :param argv_order: argument order (0-indexed, 0 is the program name)
    :param service:  (0-indexed, 0 is the program name)
    :return: port numbers
    """
    if len(sys.argv) < argv_order + 1:
        return PORT_RANGES[service][0]  # first available port

    ports_str = sys.argv[argv_order].split(',')
    ports = [validate_port(port_str, service) for port_str in ports_str]
    return ports
