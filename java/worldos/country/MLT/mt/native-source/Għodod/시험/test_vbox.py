import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import uuid

Definizzjoni_VALUE = importlib.util.spec_from_file_location('jkoros_vbox', str(Path(__file__).resolve().parents[1] / '가상상자.py'))
modulu_VALUE = importlib.util.module_from_spec(Definizzjoni_VALUE)
Definizzjoni_VALUE.loader.exec_module(modulu_VALUE)


class 가짜상자:
    def __init__(self, għerq_VALUE):
        self.għerq_VALUE = għerq_VALUE
        self.명령들 = []
        self.가상기계들 = {}
        self.żball_VALUE = None

    def __call__(self, 인수):
        인수 = list(map(str, 인수))
        self.명령들.append(인수)
        if self.żball_VALUE == 인수[1] or (인수[0] == 'make' and self.żball_VALUE == 'make'):
            self.żball_VALUE = None
            raise modulu_VALUE.실행오류('시험용 żball_VALUE')
        if 인수[0] == 'make':
            mogħdija = self.għerq_VALUE / 'os/build/kernel.iso'
            mogħdija.parent.mkdir(parents=True, exist_ok=True)
            mogħdija.write_bytes(b'fake-iso-for-launcher-test')
            return 'build complete\n'
        azzjoni = 인수[1]
        if azzjoni == 'list':
            return '\n'.join('"{}" {{{}}}'.format(VALUE['name'], INDEX) for INDEX, VALUE in self.가상기계들.items())
        if azzjoni == 'createvm':
            INDEX, isem = 인수[인수.index('--uuid') + 1], 인수[인수.index('--name') + 1]
            self.가상기계들[INDEX] = {'UUID': INDEX, 'name': isem, 'VMState': 'poweroff',
                'CfgFile': str(self.għerq_VALUE / '.vbox/machines' / isem / (isem + '.vbox')), 'owner': None}
            return ''
        kompjuter = self.가상기계들[인수[2]]
        if azzjoni == 'showvminfo':
            return '\n'.join('{}={}'.format(json.dumps(isem), json.dumps(VALUE)) for isem, VALUE in kompjuter.items() if isem != 'owner')
        if azzjoni == 'getextradata': return 'Value: ' + kompjuter['owner'] if kompjuter['owner'] else 'No value set!'
        if azzjoni == 'setextradata': kompjuter['owner'] = 인수[4]
        elif azzjoni == 'storagectl': kompjuter['storagecontrollername0'] = 'JKOROS IDE'
        elif azzjoni == 'storageattach': kompjuter['JKOROS IDE-0-0'] = 인수[인수.index('--medium') + 1]
        elif azzjoni == 'startvm': kompjuter['VMState'] = 'running'
        elif azzjoni == 'controlvm':
            assert 인수[3] == 'resume'
            kompjuter['VMState'] = 'running'
        elif azzjoni != 'modifyvm': raise AssertionError(인수)
        return ''


class 실행시험(unittest.TestCase):
    def setUp(self):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-vbox-test-')
        self.addCleanup(self.임시.cleanup)
        self.għerq_VALUE = Path(self.임시.name)
        (self.għerq_VALUE / '.vbox').mkdir()
        self.상자 = 가짜상자(self.għerq_VALUE)
        self.eżegwixxa_kmand = modulu_VALUE.programm_ġabra_ta_apps(self.għerq_VALUE, 'jkoros operating system', kmand=self.상자)

    def ħalaq_entrata(self):
        miżura = self.eżegwixxa_kmand.eżegwixxa_kmand()
        self.상자.명령들.clear()
        return self.상자.가상기계들[miżura['uuid']]

    def 변경없음(self):
        self.assertTrue(all(kmand[0] == 'VBoxManage' and kmand[1] in ('list', 'showvminfo', 'getextradata') for kmand in self.상자.명령들))

    def test_첫생성과광학부팅(self):
        miżura = self.eżegwixxa_kmand.eżegwixxa_kmand()
        self.assertEqual(miżura['state'], 'running')
        self.assertTrue(Path(miżura['iso']).is_file())
        self.assertTrue(any('--nic1' in kmand and 'none' in kmand for kmand in self.상자.명령들))
        self.assertFalse(any('hdd' in kmand or 'discardstate' in kmand or 'createmedium' in kmand for kmand in self.상자.명령들))

    def test_실행중유지(self):
        self.ħalaq_entrata()
        self.assertEqual(self.eżegwixxa_kmand.eżegwixxa_kmand()['state'], 'running')
        self.변경없음()

    def test_저장상태재개와로그보존(self):
        kompjuter = self.ħalaq_entrata()
        kompjuter['VMState'] = 'saved'
        LOG_VALUE = self.eżegwixxa_kmand.mogħdija(self.eżegwixxa_kmand.읽기()['serial_log'])
        LOG_VALUE.write_text('saved log')
        self.eżegwixxa_kmand.eżegwixxa_kmand()
        self.assertFalse(any(kmand[0] == 'make' or kmand[1] == 'modifyvm' for kmand in self.상자.명령들))
        self.assertEqual([mogħdija.read_text() for mogħdija in LOG_VALUE.parent.glob('before-resume-*.log')], ['saved log'])

    def test_일시정지재개(self):
        self.ħalaq_entrata()['VMState'] = 'paused'
        self.eżegwixxa_kmand.eżegwixxa_kmand()
        self.assertTrue(any(kmand[1] == 'controlvm' and kmand[3] == 'resume' for kmand in self.상자.명령들))
        self.assertFalse(any(kmand[0] == 'make' for kmand in self.상자.명령들))

    def test_다른VM이름충돌(self):
        self.상자.가상기계들[str(uuid.uuid4())] = {'name': 'jkoros operating system'}
        with self.assertRaises(modulu_VALUE.실행오류): self.eżegwixxa_kmand.eżegwixxa_kmand()
        self.변경없음()

    def test_소유표식거부(self):
        self.ħalaq_entrata()['owner'] = 'someone-else'
        with self.assertRaises(modulu_VALUE.실행오류): self.eżegwixxa_kmand.eżegwixxa_kmand()
        self.변경없음()

    def test_다른설정경로거부(self):
        self.ħalaq_entrata()['CfgFile'] = '/tmp/someone-else.vbox'
        with self.assertRaises(modulu_VALUE.실행오류): self.eżegwixxa_kmand.eżegwixxa_kmand()
        self.변경없음()

    def test_사용자추가디스크보존(self):
        kompjuter = self.ħalaq_entrata()
        kompjuter['VMState'] = 'poweroff'
        kompjuter['JKOROS IDE-0-1'] = '/external/user.vdi'
        with self.assertRaises(modulu_VALUE.실행오류): self.eżegwixxa_kmand.eżegwixxa_kmand()
        self.변경없음()

    def test_전환중거부(self):
        self.ħalaq_entrata()['VMState'] = 'saving'
        with self.assertRaises(modulu_VALUE.실행오류): self.eżegwixxa_kmand.eżegwixxa_kmand()
        self.변경없음()

    def test_등록해제거부(self):
        self.ħalaq_entrata()
        self.상자.가상기계들.clear()
        with self.assertRaises(modulu_VALUE.실행오류): self.eżegwixxa_kmand.eżegwixxa_kmand()
        self.변경없음()

    def test_빌드실패시VM유지(self):
        kompjuter = self.ħalaq_entrata()
        kompjuter['VMState'] = 'poweroff'
        이전 = dict(kompjuter)
        self.상자.żball_VALUE = 'make'
        with self.assertRaises(modulu_VALUE.실행오류): self.eżegwixxa_kmand.eżegwixxa_kmand()
        self.assertEqual(kompjuter, 이전)

    def test_중단된소유표식설정복구(self):
        self.상자.żball_VALUE = 'setextradata'
        with self.assertRaises(modulu_VALUE.실행오류): self.eżegwixxa_kmand.eżegwixxa_kmand()
        self.상자.명령들.clear()
        self.assertEqual(self.eżegwixxa_kmand.eżegwixxa_kmand()['state'], 'running')
        self.assertFalse(any(kmand[1] == 'createvm' for kmand in self.상자.명령들))

    def test_보존ISO변조거부(self):
        kompjuter = self.ħalaq_entrata()
        kompjuter['VMState'] = 'poweroff'
        Path(kompjuter['JKOROS IDE-0-0']).write_bytes(b'changed')
        with self.assertRaises(modulu_VALUE.실행오류): self.eżegwixxa_kmand.eżegwixxa_kmand()

    def test_상태미생성(self):
        self.assertEqual(self.eżegwixxa_kmand.wera_stat()['state'], 'not-created')
        self.assertFalse(self.상자.명령들)

    def test_경로탈출거부(self):
        for mogħdija in ('../outside', '/tmp/outside'):
            with self.assertRaises(modulu_VALUE.실행오류): self.eżegwixxa_kmand.mogħdija(mogħdija)
        (self.għerq_VALUE / '.vbox/media').symlink_to('/tmp')
        with self.assertRaises(modulu_VALUE.실행오류): self.eżegwixxa_kmand.mogħdija('media/kernel.iso')

    def test_VirtualBox52복합속성(self):
        miżura = modulu_VALUE.attribut_VALUE('VMState="running"\nVideoMode="720,400,0"@0,0 1\n"IDE-0-0"="/a b.iso"')
        self.assertEqual(miżura['VMState'], 'running')
        self.assertEqual(miżura['IDE-0-0'], '/a b.iso')


if __name__ == '__main__': unittest.main()
