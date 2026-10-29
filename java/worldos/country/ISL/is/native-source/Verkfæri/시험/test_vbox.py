import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import uuid

Skilgreining_VALUE = importlib.util.spec_from_file_location('jkoros_vbox', str(Path(__file__).resolve().parents[1] / '가상상자.py'))
eining_VALUE_6d2d8bf4 = importlib.util.module_from_spec(Skilgreining_VALUE)
Skilgreining_VALUE.loader.exec_module(eining_VALUE_6d2d8bf4)


class 가짜상자:
    def __init__(self, rót_VALUE):
        self.rót_VALUE = rót_VALUE
        self.명령들 = []
        self.가상기계들 = {}
        self.bilun_VALUE = None

    def __call__(self, Viðföng):
        Viðföng = list(map(str, Viðföng))
        self.명령들.append(Viðföng)
        if self.bilun_VALUE == Viðföng[1] or (Viðföng[0] == 'make' and self.bilun_VALUE == 'make'):
            self.bilun_VALUE = None
            raise eining_VALUE_6d2d8bf4.실행오류('시험용 bilun_VALUE')
        if Viðföng[0] == 'make':
            SLÓÐ = self.rót_VALUE / 'os/build/kernel.iso'
            SLÓÐ.parent.mkdir(parents=True, exist_ok=True)
            SLÓÐ.write_bytes(b'fake-iso-for-launcher-test')
            return 'build complete\n'
        Aðgerð = Viðföng[1]
        if Aðgerð == 'list':
            return '\n'.join('"{}" {{{}}}'.format(VALUE['name'], INDEX) for INDEX, VALUE in self.가상기계들.items())
        if Aðgerð == 'createvm':
            INDEX, Heiti = Viðföng[Viðföng.index('--uuid') + 1], Viðföng[Viðföng.index('--name') + 1]
            self.가상기계들[INDEX] = {'UUID': INDEX, 'name': Heiti, 'VMState': 'poweroff',
                'CfgFile': str(self.rót_VALUE / '.vbox/machines' / Heiti / (Heiti + '.vbox')), 'owner': None}
            return ''
        vél = self.가상기계들[Viðföng[2]]
        if Aðgerð == 'showvminfo':
            return '\n'.join('{}={}'.format(json.dumps(Heiti), json.dumps(VALUE)) for Heiti, VALUE in vél.items() if Heiti != 'owner')
        if Aðgerð == 'getextradata': return 'Value: ' + vél['owner'] if vél['owner'] else 'No value set!'
        if Aðgerð == 'setextradata': vél['owner'] = Viðföng[4]
        elif Aðgerð == 'storagectl': vél['storagecontrollername0'] = 'JKOROS IDE'
        elif Aðgerð == 'storageattach': vél['JKOROS IDE-0-0'] = Viðföng[Viðföng.index('--medium') + 1]
        elif Aðgerð == 'startvm': vél['VMState'] = 'running'
        elif Aðgerð == 'controlvm':
            assert Viðföng[3] == 'resume'
            vél['VMState'] = 'running'
        elif Aðgerð != 'modifyvm': raise AssertionError(Viðföng)
        return ''


class 실행시험(unittest.TestCase):
    def setUp(self):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-vbox-test-')
        self.addCleanup(self.임시.cleanup)
        self.rót_VALUE = Path(self.임시.name)
        (self.rót_VALUE / '.vbox').mkdir()
        self.상자 = 가짜상자(self.rót_VALUE)
        self.keyra_skipun = eining_VALUE_6d2d8bf4.forrit_ræsir(self.rót_VALUE, 'jkoros operating system', Skipun=self.상자)

    def stofna_færsla(self):
        NIÐURSTAÐA = self.keyra_skipun.keyra_skipun()
        self.상자.명령들.clear()
        return self.상자.가상기계들[NIÐURSTAÐA['uuid']]

    def 변경없음(self):
        self.assertTrue(all(Skipun[0] == 'VBoxManage' and Skipun[1] in ('list', 'showvminfo', 'getextradata') for Skipun in self.상자.명령들))

    def test_첫생성과광학부팅(self):
        NIÐURSTAÐA = self.keyra_skipun.keyra_skipun()
        self.assertEqual(NIÐURSTAÐA['state'], 'running')
        self.assertTrue(Path(NIÐURSTAÐA['iso']).is_file())
        self.assertTrue(any('--nic1' in Skipun and 'none' in Skipun for Skipun in self.상자.명령들))
        self.assertFalse(any('hdd' in Skipun or 'discardstate' in Skipun or 'createmedium' in Skipun for Skipun in self.상자.명령들))

    def test_실행중유지(self):
        self.stofna_færsla()
        self.assertEqual(self.keyra_skipun.keyra_skipun()['state'], 'running')
        self.변경없음()

    def test_저장상태재개와로그보존(self):
        vél = self.stofna_færsla()
        vél['VMState'] = 'saved'
        LOG_VALUE = self.keyra_skipun.SLÓÐ(self.keyra_skipun.Lestur()['serial_log'])
        LOG_VALUE.write_text('saved log')
        self.keyra_skipun.keyra_skipun()
        self.assertFalse(any(Skipun[0] == 'make' or Skipun[1] == 'modifyvm' for Skipun in self.상자.명령들))
        self.assertEqual([SLÓÐ.read_text() for SLÓÐ in LOG_VALUE.parent.glob('before-resume-*.log')], ['saved log'])

    def test_일시정지재개(self):
        self.stofna_færsla()['VMState'] = 'paused'
        self.keyra_skipun.keyra_skipun()
        self.assertTrue(any(Skipun[1] == 'controlvm' and Skipun[3] == 'resume' for Skipun in self.상자.명령들))
        self.assertFalse(any(Skipun[0] == 'make' for Skipun in self.상자.명령들))

    def test_다른VM이름충돌(self):
        self.상자.가상기계들[str(uuid.uuid4())] = {'name': 'jkoros operating system'}
        with self.assertRaises(eining_VALUE_6d2d8bf4.실행오류): self.keyra_skipun.keyra_skipun()
        self.변경없음()

    def test_소유표식거부(self):
        self.stofna_færsla()['owner'] = 'someone-else'
        with self.assertRaises(eining_VALUE_6d2d8bf4.실행오류): self.keyra_skipun.keyra_skipun()
        self.변경없음()

    def test_다른설정경로거부(self):
        self.stofna_færsla()['CfgFile'] = '/tmp/someone-else.vbox'
        with self.assertRaises(eining_VALUE_6d2d8bf4.실행오류): self.keyra_skipun.keyra_skipun()
        self.변경없음()

    def test_사용자추가디스크보존(self):
        vél = self.stofna_færsla()
        vél['VMState'] = 'poweroff'
        vél['JKOROS IDE-0-1'] = '/external/user.vdi'
        with self.assertRaises(eining_VALUE_6d2d8bf4.실행오류): self.keyra_skipun.keyra_skipun()
        self.변경없음()

    def test_전환중거부(self):
        self.stofna_færsla()['VMState'] = 'saving'
        with self.assertRaises(eining_VALUE_6d2d8bf4.실행오류): self.keyra_skipun.keyra_skipun()
        self.변경없음()

    def test_등록해제거부(self):
        self.stofna_færsla()
        self.상자.가상기계들.clear()
        with self.assertRaises(eining_VALUE_6d2d8bf4.실행오류): self.keyra_skipun.keyra_skipun()
        self.변경없음()

    def test_빌드실패시VM유지(self):
        vél = self.stofna_færsla()
        vél['VMState'] = 'poweroff'
        이전 = dict(vél)
        self.상자.bilun_VALUE = 'make'
        with self.assertRaises(eining_VALUE_6d2d8bf4.실행오류): self.keyra_skipun.keyra_skipun()
        self.assertEqual(vél, 이전)

    def test_중단된소유표식설정복구(self):
        self.상자.bilun_VALUE = 'setextradata'
        with self.assertRaises(eining_VALUE_6d2d8bf4.실행오류): self.keyra_skipun.keyra_skipun()
        self.상자.명령들.clear()
        self.assertEqual(self.keyra_skipun.keyra_skipun()['state'], 'running')
        self.assertFalse(any(Skipun[1] == 'createvm' for Skipun in self.상자.명령들))

    def test_보존ISO변조거부(self):
        vél = self.stofna_færsla()
        vél['VMState'] = 'poweroff'
        Path(vél['JKOROS IDE-0-0']).write_bytes(b'changed')
        with self.assertRaises(eining_VALUE_6d2d8bf4.실행오류): self.keyra_skipun.keyra_skipun()

    def test_상태미생성(self):
        self.assertEqual(self.keyra_skipun.sýna_staða()['state'], 'not-created')
        self.assertFalse(self.상자.명령들)

    def test_경로탈출거부(self):
        for SLÓÐ in ('../outside', '/tmp/outside'):
            with self.assertRaises(eining_VALUE_6d2d8bf4.실행오류): self.keyra_skipun.SLÓÐ(SLÓÐ)
        (self.rót_VALUE / '.vbox/media').symlink_to('/tmp')
        with self.assertRaises(eining_VALUE_6d2d8bf4.실행오류): self.keyra_skipun.SLÓÐ('media/kernel.iso')

    def test_VirtualBox52복합속성(self):
        NIÐURSTAÐA = eining_VALUE_6d2d8bf4.eigind_VALUE('VMState="running"\nVideoMode="720,400,0"@0,0 1\n"IDE-0-0"="/a b.iso"')
        self.assertEqual(NIÐURSTAÐA['VMState'], 'running')
        self.assertEqual(NIÐURSTAÐA['IDE-0-0'], '/a b.iso')


if __name__ == '__main__': unittest.main()
