import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import uuid

Sõnaseletus_VALUE = importlib.util.spec_from_file_location('jkoros_vbox', str(Path(__file__).resolve().parents[1] / '가상상자.py'))
moodul_VALUE = importlib.util.module_from_spec(Sõnaseletus_VALUE)
Sõnaseletus_VALUE.loader.exec_module(moodul_VALUE)


class 가짜상자:
    def __init__(self, juur_VALUE):
        self.juur_VALUE = juur_VALUE
        self.명령들 = []
        self.가상기계들 = {}
        self.tõrge_VALUE = None

    def __call__(self, Argumendid):
        Argumendid = list(map(str, Argumendid))
        self.명령들.append(Argumendid)
        if self.tõrge_VALUE == Argumendid[1] or (Argumendid[0] == 'make' and self.tõrge_VALUE == 'make'):
            self.tõrge_VALUE = None
            raise moodul_VALUE.실행오류('시험용 tõrge_VALUE')
        if Argumendid[0] == 'make':
            RADA = self.juur_VALUE / 'os/build/kernel.iso'
            RADA.parent.mkdir(parents=True, exist_ok=True)
            RADA.write_bytes(b'fake-iso-for-launcher-test')
            return 'build complete\n'
        Nimi = Argumendid[1]
        if Nimi == 'list':
            return '\n'.join('"{}" {{{}}}'.format(VALUE['name'], INDEX) for INDEX, VALUE in self.가상기계들.items())
        if Nimi == 'createvm':
            INDEX, Nimi_2 = Argumendid[Argumendid.index('--uuid') + 1], Argumendid[Argumendid.index('--name') + 1]
            self.가상기계들[INDEX] = {'UUID': INDEX, 'name': Nimi_2, 'VMState': 'poweroff',
                'CfgFile': str(self.juur_VALUE / '.vbox/machines' / Nimi_2 / (Nimi_2 + '.vbox')), 'owner': None}
            return ''
        arvuti = self.가상기계들[Argumendid[2]]
        if Nimi == 'showvminfo':
            return '\n'.join('{}={}'.format(json.dumps(Nimi_2), json.dumps(VALUE)) for Nimi_2, VALUE in arvuti.items() if Nimi_2 != 'owner')
        if Nimi == 'getextradata': return 'Value: ' + arvuti['owner'] if arvuti['owner'] else 'No value set!'
        if Nimi == 'setextradata': arvuti['owner'] = Argumendid[4]
        elif Nimi == 'storagectl': arvuti['storagecontrollername0'] = 'JKOROS IDE'
        elif Nimi == 'storageattach': arvuti['JKOROS IDE-0-0'] = Argumendid[Argumendid.index('--medium') + 1]
        elif Nimi == 'startvm': arvuti['VMState'] = 'running'
        elif Nimi == 'controlvm':
            assert Argumendid[3] == 'resume'
            arvuti['VMState'] = 'running'
        elif Nimi != 'modifyvm': raise AssertionError(Argumendid)
        return ''


class 실행시험(unittest.TestCase):
    def setUp(self):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-vbox-test-')
        self.addCleanup(self.임시.cleanup)
        self.juur_VALUE = Path(self.임시.name)
        (self.juur_VALUE / '.vbox').mkdir()
        self.상자 = 가짜상자(self.juur_VALUE)
        self.Täida_käsk = moodul_VALUE.programm_käiviti(self.juur_VALUE, 'jkoros operating system', Käsk=self.상자)

    def avama_kirje(self):
        TULEMUS = self.Täida_käsk.Täida_käsk()
        self.상자.명령들.clear()
        return self.상자.가상기계들[TULEMUS['uuid']]

    def 변경없음(self):
        self.assertTrue(all(Käsk[0] == 'VBoxManage' and Käsk[1] in ('list', 'showvminfo', 'getextradata') for Käsk in self.상자.명령들))

    def test_첫생성과광학부팅(self):
        TULEMUS = self.Täida_käsk.Täida_käsk()
        self.assertEqual(TULEMUS['state'], 'running')
        self.assertTrue(Path(TULEMUS['iso']).is_file())
        self.assertTrue(any('--nic1' in Käsk and 'none' in Käsk for Käsk in self.상자.명령들))
        self.assertFalse(any('hdd' in Käsk or 'discardstate' in Käsk or 'createmedium' in Käsk for Käsk in self.상자.명령들))

    def test_실행중유지(self):
        self.avama_kirje()
        self.assertEqual(self.Täida_käsk.Täida_käsk()['state'], 'running')
        self.변경없음()

    def test_저장상태재개와로그보존(self):
        arvuti = self.avama_kirje()
        arvuti['VMState'] = 'saved'
        LOG_VALUE = self.Täida_käsk.RADA(self.Täida_käsk.Lugemine()['serial_log'])
        LOG_VALUE.write_text('saved log')
        self.Täida_käsk.Täida_käsk()
        self.assertFalse(any(Käsk[0] == 'make' or Käsk[1] == 'modifyvm' for Käsk in self.상자.명령들))
        self.assertEqual([RADA.read_text() for RADA in LOG_VALUE.parent.glob('before-resume-*.log')], ['saved log'])

    def test_일시정지재개(self):
        self.avama_kirje()['VMState'] = 'paused'
        self.Täida_käsk.Täida_käsk()
        self.assertTrue(any(Käsk[1] == 'controlvm' and Käsk[3] == 'resume' for Käsk in self.상자.명령들))
        self.assertFalse(any(Käsk[0] == 'make' for Käsk in self.상자.명령들))

    def test_다른VM이름충돌(self):
        self.상자.가상기계들[str(uuid.uuid4())] = {'name': 'jkoros operating system'}
        with self.assertRaises(moodul_VALUE.실행오류): self.Täida_käsk.Täida_käsk()
        self.변경없음()

    def test_소유표식거부(self):
        self.avama_kirje()['owner'] = 'someone-else'
        with self.assertRaises(moodul_VALUE.실행오류): self.Täida_käsk.Täida_käsk()
        self.변경없음()

    def test_다른설정경로거부(self):
        self.avama_kirje()['CfgFile'] = '/tmp/someone-else.vbox'
        with self.assertRaises(moodul_VALUE.실행오류): self.Täida_käsk.Täida_käsk()
        self.변경없음()

    def test_사용자추가디스크보존(self):
        arvuti = self.avama_kirje()
        arvuti['VMState'] = 'poweroff'
        arvuti['JKOROS IDE-0-1'] = '/external/user.vdi'
        with self.assertRaises(moodul_VALUE.실행오류): self.Täida_käsk.Täida_käsk()
        self.변경없음()

    def test_전환중거부(self):
        self.avama_kirje()['VMState'] = 'saving'
        with self.assertRaises(moodul_VALUE.실행오류): self.Täida_käsk.Täida_käsk()
        self.변경없음()

    def test_등록해제거부(self):
        self.avama_kirje()
        self.상자.가상기계들.clear()
        with self.assertRaises(moodul_VALUE.실행오류): self.Täida_käsk.Täida_käsk()
        self.변경없음()

    def test_빌드실패시VM유지(self):
        arvuti = self.avama_kirje()
        arvuti['VMState'] = 'poweroff'
        이전 = dict(arvuti)
        self.상자.tõrge_VALUE = 'make'
        with self.assertRaises(moodul_VALUE.실행오류): self.Täida_käsk.Täida_käsk()
        self.assertEqual(arvuti, 이전)

    def test_중단된소유표식설정복구(self):
        self.상자.tõrge_VALUE = 'setextradata'
        with self.assertRaises(moodul_VALUE.실행오류): self.Täida_käsk.Täida_käsk()
        self.상자.명령들.clear()
        self.assertEqual(self.Täida_käsk.Täida_käsk()['state'], 'running')
        self.assertFalse(any(Käsk[1] == 'createvm' for Käsk in self.상자.명령들))

    def test_보존ISO변조거부(self):
        arvuti = self.avama_kirje()
        arvuti['VMState'] = 'poweroff'
        Path(arvuti['JKOROS IDE-0-0']).write_bytes(b'changed')
        with self.assertRaises(moodul_VALUE.실행오류): self.Täida_käsk.Täida_käsk()

    def test_상태미생성(self):
        self.assertEqual(self.Täida_käsk.saade_Olek()['state'], 'not-created')
        self.assertFalse(self.상자.명령들)

    def test_경로탈출거부(self):
        for RADA in ('../outside', '/tmp/outside'):
            with self.assertRaises(moodul_VALUE.실행오류): self.Täida_käsk.RADA(RADA)
        (self.juur_VALUE / '.vbox/media').symlink_to('/tmp')
        with self.assertRaises(moodul_VALUE.실행오류): self.Täida_käsk.RADA('media/kernel.iso')

    def test_VirtualBox52복합속성(self):
        TULEMUS = moodul_VALUE.atribuut_VALUE('VMState="running"\nVideoMode="720,400,0"@0,0 1\n"IDE-0-0"="/a b.iso"')
        self.assertEqual(TULEMUS['VMState'], 'running')
        self.assertEqual(TULEMUS['IDE-0-0'], '/a b.iso')


if __name__ == '__main__': unittest.main()
