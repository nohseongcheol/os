"""Read ip.conf without executing it; shared by builders and QEMU networking."""
import argparse
import ipaddress
import json
import os
from pathlib import Path
import re

DEFAULTS = {'IP': '192.168.0.100', 'NETMASK': '255.255.255.0',
            'GATEWAY': '192.168.0.1', 'DNS': '1.1.1.1'}


def config_path(start):
    explicit = os.environ.get('IP_CONFIG')
    if explicit:
        path = Path(explicit).expanduser().resolve()
        if not path.is_file():
            raise ValueError('IP_CONFIG file does not exist: ' + str(path))
        return path
    start = Path(start).resolve()
    # A country/language may override the shared WorldOS configuration.
    for parent in (start,) + tuple(start.parents):
        if (parent / 'ip.conf').is_file() and ((parent / 'native.json').is_file() or
                (parent / 'native/generate.py').is_file()):
            return parent / 'ip.conf'
    for parent in (start,) + tuple(start.parents):
        if (parent / 'ip.conf').is_file():
            return parent / 'ip.conf'
    return None


def read_config(start, path=None):
    path = Path(path) if path is not None else config_path(start)
    values = dict(DEFAULTS)
    seen = set()
    if path is not None:
        for number, line in enumerate(path.read_text(encoding='utf-8').splitlines(), 1):
            line = line.split('#', 1)[0].strip()
            if not line:
                continue
            key, separator, value = line.partition('=')
            key, value = key.strip(), value.strip()
            if not separator or key not in values or key in seen:
                raise ValueError('{}:{}: unknown/duplicate key or invalid KEY=IPv4'.format(path, number))
            values[key] = str(ipaddress.IPv4Address(value))
            seen.add(key)
    interface = ipaddress.IPv4Interface(values['IP'] + '/' + values['NETMASK'])
    if str(interface.netmask) != values['NETMASK']:
        raise ValueError('NETMASK must be a contiguous IPv4 netmask')
    address, network = interface.ip, interface.network
    if address.is_multicast or address.is_loopback or address.is_unspecified or address in (network.network_address, network.broadcast_address) or int(address) >> 24 >= 240:
        raise ValueError('IP must be a usable unicast host address')
    gateway = ipaddress.IPv4Address(values['GATEWAY'])
    if int(gateway) and (gateway not in network or gateway == address or gateway in (network.network_address, network.broadcast_address) or gateway.is_multicast):
        raise ValueError('GATEWAY must be another host in the subnet, or 0.0.0.0')
    dns = ipaddress.IPv4Address(values['DNS'])
    if dns.is_multicast or dns.is_unspecified or int(dns) == 0xffffffff:
        raise ValueError('DNS must be a unicast IPv4 address')
    values.update(network=str(network), prefix=network.prefixlen,
                  path=str(path) if path is not None else None)
    return values


def qemu_network(config, guest=None):
    """NAT and the guest must agree on the subnet, gateway and forwarding IP."""
    network = ipaddress.IPv4Network(config['network'])
    # libslirp reserves subnet-relative host/DNS addresses; keep them distinct.
    gateway = ipaddress.IPv4Address(config['GATEWAY'])
    if not int(gateway):
        gateway = network.network_address + 2
    dns = network.network_address + 3
    address = ipaddress.IPv4Address(guest or config['IP'])
    if network.prefixlen > 29 or gateway in (network.network_address, network.broadcast_address, dns) or address not in network or address in (network.network_address, network.broadcast_address, gateway, dns):
        raise ValueError('QEMU NAT requires /29 or wider and distinct guest, gateway and DNS host addresses')
    return 'net={},host={},dns={}'.format(network, gateway, dns)


def write_header(start, destination):
    config = read_config(start)
    lines = ['/* Generated from ip.conf; do not edit. */']
    for key in ('IP', 'NETMASK', 'GATEWAY'):
        lines.append('#define IP_CONFIG_{} 0x{:08x}u'.format(key, int(ipaddress.IPv4Address(config[key]))))
    Path(destination).write_text('\n'.join(lines) + '\n', encoding='utf-8')
    return config


def configure_java(source, destination, config):
    text = Path(source).read_text(encoding='utf-8')
    for key in ('IP', 'NETMASK', 'GATEWAY'):
        pattern = r'0x[0-9a-fA-F]+(?=; /\* ip.conf:' + key + r' \*/)'
        text, count = re.subn(pattern, '0x{:08x}'.format(int(ipaddress.IPv4Address(config[key]))), text)
        if count != 1:
            raise ValueError('Missing Java ip.conf marker: ' + key)
    text = re.sub(r'NET RTL8139 [^"\\]+ UDP', 'NET RTL8139 {}/{} gateway {} UDP'.format(config['IP'], config['prefix'], config['GATEWAY']), text)
    target = Path(destination)
    target.parent.mkdir(parents=True, exist_ok=True)
    if not target.is_file() or target.read_text(encoding='utf-8') != text:
        target.write_text(text, encoding='utf-8')


def configure_guest_text(text, config):
    """Keep bundled QEMU host examples/package helpers on the selected gateway."""
    return text.replace('10.0.2.2', config['GATEWAY']).replace(
        '0x0a000202', '0x{:08x}'.format(int(ipaddress.IPv4Address(config['GATEWAY']))))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[3])
    parser.add_argument('--java', nargs=2, metavar=('SOURCE', 'DESTINATION'))
    parser.add_argument('--qemu', action='store_true')
    args = parser.parse_args()
    config = read_config(args.root)
    if args.java:
        configure_java(*args.java, config=config)
    elif args.qemu:
        print(qemu_network(config))
    else:
        print(json.dumps(config, sort_keys=True))


if __name__ == '__main__':
    main()
