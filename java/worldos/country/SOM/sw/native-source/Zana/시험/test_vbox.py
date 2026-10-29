import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import uuid

Ufafanuzi_thamani = importlib.util.spec_from_file_location('jkoros_vbox', str(Path(__file__).resolve().parents[1] / '가상상자.py'))
moduli_thamani = importlib.util.module_from_spec(Ufafanuzi_thamani)
Ufafanuzi_thamani.loader.exec_module(moduli_thamani)


class 가짜상자:
    def __init__(self, 뿌리):
        self.뿌리 = 뿌리
        self.명령들 = []
        self.가상기계들 = {}
        self.kushindwa_thamani = None

    def __call__(self, 인수):
        인수 = list(map(str, 인수))
        self.명령들.append(인수)
        if self.kushindwa_thamani == 인수[1] or (인수[0] == 'make' and self.kushindwa_thamani == 'make'):
            self.kushindwa_thamani = None
            raise moduli_thamani.실행오류('시험용 kushindwa_thamani')
        if 인수[0] == 'make':
            njia = self.뿌리 / 'os/build/kernel.iso'
            njia.parent.mkdir(parents=True, exist_ok=True)
            njia.write_bytes(b'fake-iso-for-launcher-test')
            return 'build complete\n'
        Kitendo = 인수[1]
        if Kitendo == 'list':
            return '\n'.join('"{}" {{{}}}'.format(thamani['name'], kielezo) for kielezo, thamani in self.가상기계들.items())
        if Kitendo == 'createvm':
            kielezo, Jina = 인수[인수.index('--uuid') + 1], 인수[인수.index('--name') + 1]
            self.가상기계들[kielezo] = {'UUID': kielezo, 'name': Jina, 'VMState': 'poweroff',
                'CfgFile': str(self.뿌리 / '.vbox/machines' / Jina / (Jina + '.vbox')), 'owner': None}
            return ''
        mashine = self.가상기계들[인수[2]]
        if Kitendo == 'showvminfo':
            return '\n'.join('{}={}'.format(json.dumps(Jina), json.dumps(thamani)) for Jina, thamani in mashine.items() if Jina != 'owner')
        if Kitendo == 'getextradata': return 'Value: ' + mashine['owner'] if mashine['owner'] else 'No value set!'
        if Kitendo == 'setextradata': mashine['owner'] = 인수[4]
        elif Kitendo == 'storagectl': mashine['storagecontrollername0'] = 'JKOROS IDE'
        elif Kitendo == 'storageattach': mashine['JKOROS IDE-0-0'] = 인수[인수.index('--medium') + 1]
        elif Kitendo == 'startvm': mashine['VMState'] = 'running'
        elif Kitendo == 'controlvm':
            assert 인수[3] == 'resume'
            mashine['VMState'] = 'running'
        elif Kitendo != 'modifyvm': raise AssertionError(인수)
        return ''


class 실행시험(unittest.TestCase):
    def setUp(self):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-vbox-test-')
        self.addCleanup(self.임시.cleanup)
        self.뿌리 = Path(self.임시.name)
        (self.뿌리 / '.vbox').mkdir()
        self.상자 = 가짜상자(self.뿌리)
        self.tekeleza_amri = moduli_thamani.programu_droo_ya_programu(self.뿌리, 'jkoros operating system', amri=self.상자)

    def unda_ingizo(self):
        결과 = self.tekeleza_amri.tekeleza_amri()
        self.상자.명령들.clear()
        return self.상자.가상기계들[결과['uuid']]

    def 변경없음(self):
        self.assertTrue(all(amri[0] == 'VBoxManage' and amri[1] in ('list', 'showvminfo', 'getextradata') for amri in self.상자.명령들))

    def test_첫생성과광학부팅(self):
        결과 = self.tekeleza_amri.tekeleza_amri()
        self.assertEqual(결과['state'], 'running')
        self.assertTrue(Path(결과['iso']).is_file())
        self.assertTrue(any('--nic1' in amri and 'none' in amri for amri in self.상자.명령들))
        self.assertFalse(any('hdd' in amri or 'discardstate' in amri or 'createmedium' in amri for amri in self.상자.명령들))

    def test_실행중유지(self):
        self.unda_ingizo()
        self.assertEqual(self.tekeleza_amri.tekeleza_amri()['state'], 'running')
        self.변경없음()

    def test_저장상태재개와로그보존(self):
        mashine = self.unda_ingizo()
        mashine['VMState'] = 'saved'
        batli_thamani = self.tekeleza_amri.njia(self.tekeleza_amri.읽기()['serial_log'])
        batli_thamani.write_text('saved log')
        self.tekeleza_amri.tekeleza_amri()
        self.assertFalse(any(amri[0] == 'make' or amri[1] == 'modifyvm' for amri in self.상자.명령들))
        self.assertEqual([njia.read_text() for njia in batli_thamani.parent.glob('before-resume-*.log')], ['saved log'])

    def test_일시정지재개(self):
        self.unda_ingizo()['VMState'] = 'paused'
        self.tekeleza_amri.tekeleza_amri()
        self.assertTrue(any(amri[1] == 'controlvm' and amri[3] == 'resume' for amri in self.상자.명령들))
        self.assertFalse(any(amri[0] == 'make' for amri in self.상자.명령들))

    def test_다른VM이름충돌(self):
        self.상자.가상기계들[str(uuid.uuid4())] = {'name': 'jkoros operating system'}
        with self.assertRaises(moduli_thamani.실행오류): self.tekeleza_amri.tekeleza_amri()
        self.변경없음()

    def test_소유표식거부(self):
        self.unda_ingizo()['owner'] = 'someone-else'
        with self.assertRaises(moduli_thamani.실행오류): self.tekeleza_amri.tekeleza_amri()
        self.변경없음()

    def test_다른설정경로거부(self):
        self.unda_ingizo()['CfgFile'] = '/tmp/someone-else.vbox'
        with self.assertRaises(moduli_thamani.실행오류): self.tekeleza_amri.tekeleza_amri()
        self.변경없음()

    def test_사용자추가디스크보존(self):
        mashine = self.unda_ingizo()
        mashine['VMState'] = 'poweroff'
        mashine['JKOROS IDE-0-1'] = '/external/user.vdi'
        with self.assertRaises(moduli_thamani.실행오류): self.tekeleza_amri.tekeleza_amri()
        self.변경없음()

    def test_전환중거부(self):
        self.unda_ingizo()['VMState'] = 'saving'
        with self.assertRaises(moduli_thamani.실행오류): self.tekeleza_amri.tekeleza_amri()
        self.변경없음()

    def test_등록해제거부(self):
        self.unda_ingizo()
        self.상자.가상기계들.clear()
        with self.assertRaises(moduli_thamani.실행오류): self.tekeleza_amri.tekeleza_amri()
        self.변경없음()

    def test_빌드실패시VM유지(self):
        mashine = self.unda_ingizo()
        mashine['VMState'] = 'poweroff'
        이전 = dict(mashine)
        self.상자.kushindwa_thamani = 'make'
        with self.assertRaises(moduli_thamani.실행오류): self.tekeleza_amri.tekeleza_amri()
        self.assertEqual(mashine, 이전)

    def test_중단된소유표식설정복구(self):
        self.상자.kushindwa_thamani = 'setextradata'
        with self.assertRaises(moduli_thamani.실행오류): self.tekeleza_amri.tekeleza_amri()
        self.상자.명령들.clear()
        self.assertEqual(self.tekeleza_amri.tekeleza_amri()['state'], 'running')
        self.assertFalse(any(amri[1] == 'createvm' for amri in self.상자.명령들))

    def test_보존ISO변조거부(self):
        mashine = self.unda_ingizo()
        mashine['VMState'] = 'poweroff'
        Path(mashine['JKOROS IDE-0-0']).write_bytes(b'changed')
        with self.assertRaises(moduli_thamani.실행오류): self.tekeleza_amri.tekeleza_amri()

    def test_상태미생성(self):
        self.assertEqual(self.tekeleza_amri.onyesha_hali()['state'], 'not-created')
        self.assertFalse(self.상자.명령들)

    def test_경로탈출거부(self):
        for njia in ('../outside', '/tmp/outside'):
            with self.assertRaises(moduli_thamani.실행오류): self.tekeleza_amri.njia(njia)
        (self.뿌리 / '.vbox/media').symlink_to('/tmp')
        with self.assertRaises(moduli_thamani.실행오류): self.tekeleza_amri.njia('media/kernel.iso')

    def test_VirtualBox52복합속성(self):
        결과 = moduli_thamani.sifa_thamani('VMState="running"\nVideoMode="720,400,0"@0,0 1\n"IDE-0-0"="/a b.iso"')
        self.assertEqual(결과['VMState'], 'running')
        self.assertEqual(결과['IDE-0-0'], '/a b.iso')


if __name__ == '__main__': unittest.main()
