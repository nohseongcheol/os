import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import uuid

Izoh_VALUE = importlib.util.spec_from_file_location('jkoros_vbox', str(Path(__file__).resolve().parents[1] / '가상상자.py'))
modul_VALUE = importlib.util.module_from_spec(Izoh_VALUE)
Izoh_VALUE.loader.exec_module(modul_VALUE)


class 가짜상자:
    def __init__(self, ildiz_VALUE):
        self.ildiz_VALUE = ildiz_VALUE
        self.명령들 = []
        self.가상기계들 = {}
        self.to_xtab_qolish_VALUE = None

    def __call__(self, 인수):
        인수 = list(map(str, 인수))
        self.명령들.append(인수)
        if self.to_xtab_qolish_VALUE == 인수[1] or (인수[0] == 'make' and self.to_xtab_qolish_VALUE == 'make'):
            self.to_xtab_qolish_VALUE = None
            raise modul_VALUE.실행오류('시험용 to_xtab_qolish_VALUE')
        if 인수[0] == 'make':
            yo_l = self.ildiz_VALUE / 'os/build/kernel.iso'
            yo_l.parent.mkdir(parents=True, exist_ok=True)
            yo_l.write_bytes(b'fake-iso-for-launcher-test')
            return 'build complete\n'
        Amal = 인수[1]
        if Amal == 'list':
            return '\n'.join('"{}" {{{}}}'.format(VALUE['name'], INDEX) for INDEX, VALUE in self.가상기계들.items())
        if Amal == 'createvm':
            INDEX, Nomi = 인수[인수.index('--uuid') + 1], 인수[인수.index('--name') + 1]
            self.가상기계들[INDEX] = {'UUID': INDEX, 'name': Nomi, 'VMState': 'poweroff',
                'CfgFile': str(self.ildiz_VALUE / '.vbox/machines' / Nomi / (Nomi + '.vbox')), 'owner': None}
            return ''
        기계 = self.가상기계들[인수[2]]
        if Amal == 'showvminfo':
            return '\n'.join('{}={}'.format(json.dumps(Nomi), json.dumps(VALUE)) for Nomi, VALUE in 기계.items() if Nomi != 'owner')
        if Amal == 'getextradata': return 'Value: ' + 기계['owner'] if 기계['owner'] else 'No value set!'
        if Amal == 'setextradata': 기계['owner'] = 인수[4]
        elif Amal == 'storagectl': 기계['storagecontrollername0'] = 'JKOROS IDE'
        elif Amal == 'storageattach': 기계['JKOROS IDE-0-0'] = 인수[인수.index('--medium') + 1]
        elif Amal == 'startvm': 기계['VMState'] = 'running'
        elif Amal == 'controlvm':
            assert 인수[3] == 'resume'
            기계['VMState'] = 'running'
        elif Amal != 'modifyvm': raise AssertionError(인수)
        return ''


class 실행시험(unittest.TestCase):
    def setUp(self):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-vbox-test-')
        self.addCleanup(self.임시.cleanup)
        self.ildiz_VALUE = Path(self.임시.name)
        (self.ildiz_VALUE / '.vbox').mkdir()
        self.상자 = 가짜상자(self.ildiz_VALUE)
        self.bajarmoq_buyruq = modul_VALUE.ilova_ilovalar_paneli(self.ildiz_VALUE, 'jkoros operating system', Buyruq=self.상자)

    def Yaratish_kiritish(self):
        o_lchov = self.bajarmoq_buyruq.bajarmoq_buyruq()
        self.상자.명령들.clear()
        return self.상자.가상기계들[o_lchov['uuid']]

    def 변경없음(self):
        self.assertTrue(all(Buyruq[0] == 'VBoxManage' and Buyruq[1] in ('list', 'showvminfo', 'getextradata') for Buyruq in self.상자.명령들))

    def test_첫생성과광학부팅(self):
        o_lchov = self.bajarmoq_buyruq.bajarmoq_buyruq()
        self.assertEqual(o_lchov['state'], 'running')
        self.assertTrue(Path(o_lchov['iso']).is_file())
        self.assertTrue(any('--nic1' in Buyruq and 'none' in Buyruq for Buyruq in self.상자.명령들))
        self.assertFalse(any('hdd' in Buyruq or 'discardstate' in Buyruq or 'createmedium' in Buyruq for Buyruq in self.상자.명령들))

    def test_실행중유지(self):
        self.Yaratish_kiritish()
        self.assertEqual(self.bajarmoq_buyruq.bajarmoq_buyruq()['state'], 'running')
        self.변경없음()

    def test_저장상태재개와로그보존(self):
        기계 = self.Yaratish_kiritish()
        기계['VMState'] = 'saved'
        LOG_VALUE = self.bajarmoq_buyruq.yo_l(self.bajarmoq_buyruq.Oʻqish()['serial_log'])
        LOG_VALUE.write_text('saved log')
        self.bajarmoq_buyruq.bajarmoq_buyruq()
        self.assertFalse(any(Buyruq[0] == 'make' or Buyruq[1] == 'modifyvm' for Buyruq in self.상자.명령들))
        self.assertEqual([yo_l.read_text() for yo_l in LOG_VALUE.parent.glob('before-resume-*.log')], ['saved log'])

    def test_일시정지재개(self):
        self.Yaratish_kiritish()['VMState'] = 'paused'
        self.bajarmoq_buyruq.bajarmoq_buyruq()
        self.assertTrue(any(Buyruq[1] == 'controlvm' and Buyruq[3] == 'resume' for Buyruq in self.상자.명령들))
        self.assertFalse(any(Buyruq[0] == 'make' for Buyruq in self.상자.명령들))

    def test_다른VM이름충돌(self):
        self.상자.가상기계들[str(uuid.uuid4())] = {'name': 'jkoros operating system'}
        with self.assertRaises(modul_VALUE.실행오류): self.bajarmoq_buyruq.bajarmoq_buyruq()
        self.변경없음()

    def test_소유표식거부(self):
        self.Yaratish_kiritish()['owner'] = 'someone-else'
        with self.assertRaises(modul_VALUE.실행오류): self.bajarmoq_buyruq.bajarmoq_buyruq()
        self.변경없음()

    def test_다른설정경로거부(self):
        self.Yaratish_kiritish()['CfgFile'] = '/tmp/someone-else.vbox'
        with self.assertRaises(modul_VALUE.실행오류): self.bajarmoq_buyruq.bajarmoq_buyruq()
        self.변경없음()

    def test_사용자추가디스크보존(self):
        기계 = self.Yaratish_kiritish()
        기계['VMState'] = 'poweroff'
        기계['JKOROS IDE-0-1'] = '/external/user.vdi'
        with self.assertRaises(modul_VALUE.실행오류): self.bajarmoq_buyruq.bajarmoq_buyruq()
        self.변경없음()

    def test_전환중거부(self):
        self.Yaratish_kiritish()['VMState'] = 'saving'
        with self.assertRaises(modul_VALUE.실행오류): self.bajarmoq_buyruq.bajarmoq_buyruq()
        self.변경없음()

    def test_등록해제거부(self):
        self.Yaratish_kiritish()
        self.상자.가상기계들.clear()
        with self.assertRaises(modul_VALUE.실행오류): self.bajarmoq_buyruq.bajarmoq_buyruq()
        self.변경없음()

    def test_빌드실패시VM유지(self):
        기계 = self.Yaratish_kiritish()
        기계['VMState'] = 'poweroff'
        이전 = dict(기계)
        self.상자.to_xtab_qolish_VALUE = 'make'
        with self.assertRaises(modul_VALUE.실행오류): self.bajarmoq_buyruq.bajarmoq_buyruq()
        self.assertEqual(기계, 이전)

    def test_중단된소유표식설정복구(self):
        self.상자.to_xtab_qolish_VALUE = 'setextradata'
        with self.assertRaises(modul_VALUE.실행오류): self.bajarmoq_buyruq.bajarmoq_buyruq()
        self.상자.명령들.clear()
        self.assertEqual(self.bajarmoq_buyruq.bajarmoq_buyruq()['state'], 'running')
        self.assertFalse(any(Buyruq[1] == 'createvm' for Buyruq in self.상자.명령들))

    def test_보존ISO변조거부(self):
        기계 = self.Yaratish_kiritish()
        기계['VMState'] = 'poweroff'
        Path(기계['JKOROS IDE-0-0']).write_bytes(b'changed')
        with self.assertRaises(modul_VALUE.실행오류): self.bajarmoq_buyruq.bajarmoq_buyruq()

    def test_상태미생성(self):
        self.assertEqual(self.bajarmoq_buyruq.ko_rsatmoq_holat()['state'], 'not-created')
        self.assertFalse(self.상자.명령들)

    def test_경로탈출거부(self):
        for yo_l in ('../outside', '/tmp/outside'):
            with self.assertRaises(modul_VALUE.실행오류): self.bajarmoq_buyruq.yo_l(yo_l)
        (self.ildiz_VALUE / '.vbox/media').symlink_to('/tmp')
        with self.assertRaises(modul_VALUE.실행오류): self.bajarmoq_buyruq.yo_l('media/kernel.iso')

    def test_VirtualBox52복합속성(self):
        o_lchov = modul_VALUE.xususiyat_VALUE('VMState="running"\nVideoMode="720,400,0"@0,0 1\n"IDE-0-0"="/a b.iso"')
        self.assertEqual(o_lchov['VMState'], 'running')
        self.assertEqual(o_lchov['IDE-0-0'], '/a b.iso')


if __name__ == '__main__': unittest.main()
