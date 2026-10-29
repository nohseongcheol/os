import importlib.util
import gzip
import ipaddress
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'tools'))
import ip_config


class IPConfigTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='ip config ')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.path = self.root/'ip.conf'

    def read(self, text):
        self.path.write_text(text)
        return ip_config.read_config(self.root, self.path)

    def test_default_address_and_nat_agree(self):
        config = self.read('# defaults\n')
        self.assertEqual(config['IP'], '192.168.0.100')
        self.assertEqual(config['prefix'], 24)
        self.assertEqual(ip_config.qemu_network(config), 'net=192.168.0.0/24,host=192.168.0.1,dns=192.168.0.3')

    def test_custom_subnet_reaches_native_and_qemu(self):
        config = self.read('IP=172.20.16.88\nNETMASK=255.255.240.0\nGATEWAY=172.20.16.1\nDNS=8.8.8.8\n')
        self.assertEqual(config['prefix'], 20)
        self.assertEqual(ip_config.qemu_network(config), 'net=172.20.16.0/20,host=172.20.16.1,dns=172.20.16.3')
        with patch.dict(os.environ, {'IP_CONFIG': str(self.path)}):
            target = self.root/'generated.h'
            ip_config.write_header(self.root, target)
            self.assertIn('IP_CONFIG_IP 0xac141058u', target.read_text())

    def test_invalid_settings_fail_before_build(self):
        for text in ('IP=999.0.0.1', 'IP=127.0.0.1', 'IP=224.0.0.1',
                     'IP=192.168.0.0', 'IP=192.168.0.255',
                     'NETMASK=255.0.255.0', 'NETMASK=0.0.0.255',
                     'GATEWAY=10.0.0.1', 'GATEWAY=192.168.0.100',
                     'IP=192.168.0.101\nIP=192.168.0.102', 'BAD=hello',
                     'IP=$(touch /tmp/should-never-run)', 'DNS=224.0.0.1'):
            with self.subTest(text=text), self.assertRaises(ValueError):
                self.read(text)

    def test_default_route_optional(self):
        self.assertEqual(self.read('GATEWAY=0.0.0.0')['GATEWAY'], '0.0.0.0')

    def test_country_override_shared_and_standalone_precedence(self):
        world = self.root/'worldos'; edition = world/'country/CHN/khb'
        kernel = edition/'native-source/platforms/rpi4-native'
        kernel.mkdir(parents=True)
        (world/'native').mkdir(); (world/'native/generate.py').touch()
        (world/'ip.conf').write_text('IP=192.168.0.111\n')
        (edition/'native.json').write_text('{}')
        standalone = edition/'native-source/ip.conf'; standalone.write_text('IP=192.168.0.112\n')
        with patch.dict(os.environ, {}, clear=True):
            self.assertEqual(ip_config.read_config(kernel)['IP'], '192.168.0.111')
            (edition/'ip.conf').write_text('IP=192.168.0.113\n')
            self.assertEqual(ip_config.read_config(kernel)['IP'], '192.168.0.113')
            with patch.dict(os.environ, {'IP_CONFIG': str(standalone)}):
                self.assertEqual(ip_config.read_config(kernel)['IP'], '192.168.0.112')
            (edition/'ip.conf').unlink(); (world/'ip.conf').unlink()
            self.assertEqual(ip_config.read_config(kernel)['IP'], '192.168.0.112')

    def test_missing_explicit_file_is_error(self):
        with patch.dict(os.environ, {'IP_CONFIG': str(self.root/'missing')}):
            with self.assertRaises(ValueError):
                ip_config.read_config(self.root)

    def test_java_source_uses_config_and_retains_local_identifiers(self):
        import json
        spec = json.loads((ROOT/'native/inputs/ip-config-update.json').read_text())
        text = next(f['after_source'] for f in spec['files'] if f['path']=='os/원문/통신망.java')
        current = self.root/'통신망.java'; current.write_text(text)
        target = self.root/'java/통신망.java'
        config = self.read('IP=192.168.0.123\n')
        ip_config.configure_java(current, target, config)
        text = target.read_text()
        self.assertIn('내주소 = 0xc0a8007b;', text)
        self.assertIn('192.168.0.123/24 gateway 192.168.0.1', text)

    def test_forward_address_must_fit_configured_subnet(self):
        config = self.read('')
        for address in ('10.0.2.15', '192.168.0.0', '192.168.0.1', '192.168.0.3', '192.168.0.255'):
            with self.subTest(address=address), self.assertRaises(ValueError):
                ip_config.qemu_network(config, address)
        self.assertIn('net=192.168.0.0/24', ip_config.qemu_network(config, '192.168.0.120'))

    def test_migration_removes_old_address_guard_and_dhcp(self):
        from apply_ip_config import apply_edits
        text = 'before\nold NAT guard\ndhcp_start();\nafter\n'
        edits = [('old NAT guard\n',''), ('dhcp_start();\n','')]
        result = apply_edits(text, edits, 'test')
        self.assertEqual(result, 'before\nafter\n')
        self.assertEqual(apply_edits(result, edits, 'test'), result)

    def test_guest_examples_and_package_helpers_follow_gateway(self):
        config = self.read('IP=172.20.16.88\nNETMASK=255.255.240.0\nGATEWAY=172.20.16.1\n')
        text = 'Socket("10.0.2.2"); address=0x0a000202;'
        self.assertEqual(ip_config.configure_guest_text(text,config), 'Socket("172.20.16.1"); address=0xac141001;')

    def test_shared_config_change_invalidates_kernel_digest(self):
        from verify_country_boots import source_digest
        world=self.root/'worldos'; folder=world/'country/KOR'; source=folder/'source'
        (source/'kernel').mkdir(parents=True);(world/'native').mkdir()
        (world/'native/generate.py').touch();(source/'ip.conf').write_text('IP=192.168.0.100\n')
        (world/'ip.conf').write_text('IP=192.168.0.100\n')
        config={'owned_files':['ip.conf'],'source':'source','native':'kernel'}
        with patch.dict(os.environ, {}, clear=True):
            first=source_digest(folder,config)
            (world/'ip.conf').write_text('IP=192.168.0.123\n')
            self.assertNotEqual(first,source_digest(folder,config))
        self.assertEqual((source/'ip.conf').read_text(),'IP=192.168.0.100\n')

    def test_existing_linux_runtime_receives_validated_config(self):
        import json
        spec=importlib.util.spec_from_file_location('linux_edition',ROOT/'tools/edition.py')
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        folder=self.root/'edition';runtime=self.root/'runtime';folder.mkdir();runtime.mkdir()
        (folder/'build').mkdir();(folder/'examples').mkdir()
        for name in ('Source.java','messages.properties','posix.h'):(folder/name).touch()
        (folder/'build/edition.jar').write_bytes(b'test jar')
        (folder/'edition.json').write_text(json.dumps({'sources':['Source.java'],'messages':'messages.properties',
            'posix':'posix.h','examples':'examples','language':'en','country':'USA'}))
        (runtime/'worldos-init').write_text("#!/bin/sh\nip address add 10.0.2.15/24 dev eth0\nip route add default via 10.0.2.2\nprintf 'nameserver 10.0.2.3\\n' > /etc/resolv.conf\n")
        (runtime/'input-session.sh').touch();(runtime/'base.cpio.gz').write_bytes(gzip.compress(b''))
        self.path.write_text('IP=192.168.0.123\n')
        with patch.dict(os.environ,{'IP_CONFIG':str(self.path)}):module.prepare(folder,runtime)
        overlay=(folder/'build/edition.cpio').read_bytes()
        self.assertIn(b'IP=192.168.0.123\n',overlay)
        self.assertIn(b'. /opt/worldos/ip.conf',overlay)
        self.assertNotIn(b'ip address add 10.0.2.15/24',overlay)


if __name__ == '__main__':
    unittest.main()
