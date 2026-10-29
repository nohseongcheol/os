import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import uuid

Apibrėžtis_VALUE = importlib.util.spec_from_file_location('jkoros_vbox', str(Path(__file__).resolve().parents[1] / '가상상자.py'))
modulis_VALUE = importlib.util.module_from_spec(Apibrėžtis_VALUE)
Apibrėžtis_VALUE.loader.exec_module(modulis_VALUE)


class 가짜상자:
    def __init__(self, šaknis_VALUE):
        self.šaknis_VALUE = šaknis_VALUE
        self.명령들 = []
        self.가상기계들 = {}
        self.triktis_VALUE = None

    def __call__(self, Argumentai):
        Argumentai = list(map(str, Argumentai))
        self.명령들.append(Argumentai)
        if self.triktis_VALUE == Argumentai[1] or (Argumentai[0] == 'make' and self.triktis_VALUE == 'make'):
            self.triktis_VALUE = None
            raise modulis_VALUE.실행오류('시험용 triktis_VALUE')
        if Argumentai[0] == 'make':
            KELIAS = self.šaknis_VALUE / 'os/build/kernel.iso'
            KELIAS.parent.mkdir(parents=True, exist_ok=True)
            KELIAS.write_bytes(b'fake-iso-for-launcher-test')
            return 'build complete\n'
        Veiksmas = Argumentai[1]
        if Veiksmas == 'list':
            return '\n'.join('"{}" {{{}}}'.format(VALUE['name'], INDEX) for INDEX, VALUE in self.가상기계들.items())
        if Veiksmas == 'createvm':
            INDEX, Pavadinimas_2 = Argumentai[Argumentai.index('--uuid') + 1], Argumentai[Argumentai.index('--name') + 1]
            self.가상기계들[INDEX] = {'UUID': INDEX, 'name': Pavadinimas_2, 'VMState': 'poweroff',
                'CfgFile': str(self.šaknis_VALUE / '.vbox/machines' / Pavadinimas_2 / (Pavadinimas_2 + '.vbox')), 'owner': None}
            return ''
        mašina = self.가상기계들[Argumentai[2]]
        if Veiksmas == 'showvminfo':
            return '\n'.join('{}={}'.format(json.dumps(Pavadinimas_2), json.dumps(VALUE)) for Pavadinimas_2, VALUE in mašina.items() if Pavadinimas_2 != 'owner')
        if Veiksmas == 'getextradata': return 'Value: ' + mašina['owner'] if mašina['owner'] else 'No value set!'
        if Veiksmas == 'setextradata': mašina['owner'] = Argumentai[4]
        elif Veiksmas == 'storagectl': mašina['storagecontrollername0'] = 'JKOROS IDE'
        elif Veiksmas == 'storageattach': mašina['JKOROS IDE-0-0'] = Argumentai[Argumentai.index('--medium') + 1]
        elif Veiksmas == 'startvm': mašina['VMState'] = 'running'
        elif Veiksmas == 'controlvm':
            assert Argumentai[3] == 'resume'
            mašina['VMState'] = 'running'
        elif Veiksmas != 'modifyvm': raise AssertionError(Argumentai)
        return ''


class 실행시험(unittest.TestCase):
    def setUp(self):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-vbox-test-')
        self.addCleanup(self.임시.cleanup)
        self.šaknis_VALUE = Path(self.임시.name)
        (self.šaknis_VALUE / '.vbox').mkdir()
        self.상자 = 가짜상자(self.šaknis_VALUE)
        self.Vykdyti_komanda = modulis_VALUE.programa_programų_skydelis(self.šaknis_VALUE, 'jkoros operating system', Komanda=self.상자)

    def kurti_įrašas(self):
        REZULTATAS = self.Vykdyti_komanda.Vykdyti_komanda()
        self.상자.명령들.clear()
        return self.상자.가상기계들[REZULTATAS['uuid']]

    def 변경없음(self):
        self.assertTrue(all(Komanda[0] == 'VBoxManage' and Komanda[1] in ('list', 'showvminfo', 'getextradata') for Komanda in self.상자.명령들))

    def test_첫생성과광학부팅(self):
        REZULTATAS = self.Vykdyti_komanda.Vykdyti_komanda()
        self.assertEqual(REZULTATAS['state'], 'running')
        self.assertTrue(Path(REZULTATAS['iso']).is_file())
        self.assertTrue(any('--nic1' in Komanda and 'none' in Komanda for Komanda in self.상자.명령들))
        self.assertFalse(any('hdd' in Komanda or 'discardstate' in Komanda or 'createmedium' in Komanda for Komanda in self.상자.명령들))

    def test_실행중유지(self):
        self.kurti_įrašas()
        self.assertEqual(self.Vykdyti_komanda.Vykdyti_komanda()['state'], 'running')
        self.변경없음()

    def test_저장상태재개와로그보존(self):
        mašina = self.kurti_įrašas()
        mašina['VMState'] = 'saved'
        LOG_VALUE = self.Vykdyti_komanda.KELIAS(self.Vykdyti_komanda.Skaitymas()['serial_log'])
        LOG_VALUE.write_text('saved log')
        self.Vykdyti_komanda.Vykdyti_komanda()
        self.assertFalse(any(Komanda[0] == 'make' or Komanda[1] == 'modifyvm' for Komanda in self.상자.명령들))
        self.assertEqual([KELIAS.read_text() for KELIAS in LOG_VALUE.parent.glob('before-resume-*.log')], ['saved log'])

    def test_일시정지재개(self):
        self.kurti_įrašas()['VMState'] = 'paused'
        self.Vykdyti_komanda.Vykdyti_komanda()
        self.assertTrue(any(Komanda[1] == 'controlvm' and Komanda[3] == 'resume' for Komanda in self.상자.명령들))
        self.assertFalse(any(Komanda[0] == 'make' for Komanda in self.상자.명령들))

    def test_다른VM이름충돌(self):
        self.상자.가상기계들[str(uuid.uuid4())] = {'name': 'jkoros operating system'}
        with self.assertRaises(modulis_VALUE.실행오류): self.Vykdyti_komanda.Vykdyti_komanda()
        self.변경없음()

    def test_소유표식거부(self):
        self.kurti_įrašas()['owner'] = 'someone-else'
        with self.assertRaises(modulis_VALUE.실행오류): self.Vykdyti_komanda.Vykdyti_komanda()
        self.변경없음()

    def test_다른설정경로거부(self):
        self.kurti_įrašas()['CfgFile'] = '/tmp/someone-else.vbox'
        with self.assertRaises(modulis_VALUE.실행오류): self.Vykdyti_komanda.Vykdyti_komanda()
        self.변경없음()

    def test_사용자추가디스크보존(self):
        mašina = self.kurti_įrašas()
        mašina['VMState'] = 'poweroff'
        mašina['JKOROS IDE-0-1'] = '/external/user.vdi'
        with self.assertRaises(modulis_VALUE.실행오류): self.Vykdyti_komanda.Vykdyti_komanda()
        self.변경없음()

    def test_전환중거부(self):
        self.kurti_įrašas()['VMState'] = 'saving'
        with self.assertRaises(modulis_VALUE.실행오류): self.Vykdyti_komanda.Vykdyti_komanda()
        self.변경없음()

    def test_등록해제거부(self):
        self.kurti_įrašas()
        self.상자.가상기계들.clear()
        with self.assertRaises(modulis_VALUE.실행오류): self.Vykdyti_komanda.Vykdyti_komanda()
        self.변경없음()

    def test_빌드실패시VM유지(self):
        mašina = self.kurti_įrašas()
        mašina['VMState'] = 'poweroff'
        이전 = dict(mašina)
        self.상자.triktis_VALUE = 'make'
        with self.assertRaises(modulis_VALUE.실행오류): self.Vykdyti_komanda.Vykdyti_komanda()
        self.assertEqual(mašina, 이전)

    def test_중단된소유표식설정복구(self):
        self.상자.triktis_VALUE = 'setextradata'
        with self.assertRaises(modulis_VALUE.실행오류): self.Vykdyti_komanda.Vykdyti_komanda()
        self.상자.명령들.clear()
        self.assertEqual(self.Vykdyti_komanda.Vykdyti_komanda()['state'], 'running')
        self.assertFalse(any(Komanda[1] == 'createvm' for Komanda in self.상자.명령들))

    def test_보존ISO변조거부(self):
        mašina = self.kurti_įrašas()
        mašina['VMState'] = 'poweroff'
        Path(mašina['JKOROS IDE-0-0']).write_bytes(b'changed')
        with self.assertRaises(modulis_VALUE.실행오류): self.Vykdyti_komanda.Vykdyti_komanda()

    def test_상태미생성(self):
        self.assertEqual(self.Vykdyti_komanda.laida_Būsena()['state'], 'not-created')
        self.assertFalse(self.상자.명령들)

    def test_경로탈출거부(self):
        for KELIAS in ('../outside', '/tmp/outside'):
            with self.assertRaises(modulis_VALUE.실행오류): self.Vykdyti_komanda.KELIAS(KELIAS)
        (self.šaknis_VALUE / '.vbox/media').symlink_to('/tmp')
        with self.assertRaises(modulis_VALUE.실행오류): self.Vykdyti_komanda.KELIAS('media/kernel.iso')

    def test_VirtualBox52복합속성(self):
        REZULTATAS = modulis_VALUE.atributas_VALUE('VMState="running"\nVideoMode="720,400,0"@0,0 1\n"IDE-0-0"="/a b.iso"')
        self.assertEqual(REZULTATAS['VMState'], 'running')
        self.assertEqual(REZULTATAS['IDE-0-0'], '/a b.iso')


if __name__ == '__main__': unittest.main()
