import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import uuid

Takrif_VALUE = importlib.util.spec_from_file_location('jkoros_vbox', str(Path(__file__).resolve().parents[1] / '가상상자.py'))
modul_VALUE = importlib.util.module_from_spec(Takrif_VALUE)
Takrif_VALUE.loader.exec_module(modul_VALUE)


class 가짜상자:
    def __init__(self, akar_VALUE):
        self.akar_VALUE = akar_VALUE
        self.명령들 = []
        self.가상기계들 = {}
        self.kegagalan_VALUE = None

    def __call__(self, 인수):
        인수 = list(map(str, 인수))
        self.명령들.append(인수)
        if self.kegagalan_VALUE == 인수[1] or (인수[0] == 'make' and self.kegagalan_VALUE == 'make'):
            self.kegagalan_VALUE = None
            raise modul_VALUE.실행오류('시험용 kegagalan_VALUE')
        if 인수[0] == 'make':
            LALUAN = self.akar_VALUE / 'os/build/kernel.iso'
            LALUAN.parent.mkdir(parents=True, exist_ok=True)
            LALUAN.write_bytes(b'fake-iso-for-launcher-test')
            return 'build complete\n'
        Aksi = 인수[1]
        if Aksi == 'list':
            return '\n'.join('"{}" {{{}}}'.format(VALUE['name'], INDEX) for INDEX, VALUE in self.가상기계들.items())
        if Aksi == 'createvm':
            INDEX, Nama = 인수[인수.index('--uuid') + 1], 인수[인수.index('--name') + 1]
            self.가상기계들[INDEX] = {'UUID': INDEX, 'name': Nama, 'VMState': 'poweroff',
                'CfgFile': str(self.akar_VALUE / '.vbox/machines' / Nama / (Nama + '.vbox')), 'owner': None}
            return ''
        mesin = self.가상기계들[인수[2]]
        if Aksi == 'showvminfo':
            return '\n'.join('{}={}'.format(json.dumps(Nama), json.dumps(VALUE)) for Nama, VALUE in mesin.items() if Nama != 'owner')
        if Aksi == 'getextradata': return 'Value: ' + mesin['owner'] if mesin['owner'] else 'No value set!'
        if Aksi == 'setextradata': mesin['owner'] = 인수[4]
        elif Aksi == 'storagectl': mesin['storagecontrollername0'] = 'JKOROS IDE'
        elif Aksi == 'storageattach': mesin['JKOROS IDE-0-0'] = 인수[인수.index('--medium') + 1]
        elif Aksi == 'startvm': mesin['VMState'] = 'running'
        elif Aksi == 'controlvm':
            assert 인수[3] == 'resume'
            mesin['VMState'] = 'running'
        elif Aksi != 'modifyvm': raise AssertionError(인수)
        return ''


class jalanan_ujian(unittest.TestCase):
    def setUp(self):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-vbox-test-')
        self.addCleanup(self.임시.cleanup)
        self.akar_VALUE = Path(self.임시.name)
        (self.akar_VALUE / '.vbox').mkdir()
        self.상자 = 가짜상자(self.akar_VALUE)
        self.laksanakan_perintah = modul_VALUE.aplikasi_pelancar(self.akar_VALUE, 'jkoros operating system', Perintah=self.상자)

    def cipta_pemasukan(self):
        ukuran = self.laksanakan_perintah.laksanakan_perintah()
        self.상자.명령들.clear()
        return self.상자.가상기계들[ukuran['uuid']]

    def 변경없음(self):
        self.assertTrue(all(Perintah[0] == 'VBoxManage' and Perintah[1] in ('list', 'showvminfo', 'getextradata') for Perintah in self.상자.명령들))

    def test_첫생성과광학부팅(self):
        ukuran = self.laksanakan_perintah.laksanakan_perintah()
        self.assertEqual(ukuran['state'], 'running')
        self.assertTrue(Path(ukuran['iso']).is_file())
        self.assertTrue(any('--nic1' in Perintah and 'none' in Perintah for Perintah in self.상자.명령들))
        self.assertFalse(any('hdd' in Perintah or 'discardstate' in Perintah or 'createmedium' in Perintah for Perintah in self.상자.명령들))

    def test_실행중유지(self):
        self.cipta_pemasukan()
        self.assertEqual(self.laksanakan_perintah.laksanakan_perintah()['state'], 'running')
        self.변경없음()

    def test_저장상태재개와로그보존(self):
        mesin = self.cipta_pemasukan()
        mesin['VMState'] = 'saved'
        LOG_VALUE = self.laksanakan_perintah.LALUAN(self.laksanakan_perintah.Baca()['serial_log'])
        LOG_VALUE.write_text('saved log')
        self.laksanakan_perintah.laksanakan_perintah()
        self.assertFalse(any(Perintah[0] == 'make' or Perintah[1] == 'modifyvm' for Perintah in self.상자.명령들))
        self.assertEqual([LALUAN.read_text() for LALUAN in LOG_VALUE.parent.glob('before-resume-*.log')], ['saved log'])

    def ujian_Jeda_AND_CV(self):
        self.cipta_pemasukan()['VMState'] = 'paused'
        self.laksanakan_perintah.laksanakan_perintah()
        self.assertTrue(any(Perintah[1] == 'controlvm' and Perintah[3] == 'resume' for Perintah in self.상자.명령들))
        self.assertFalse(any(Perintah[0] == 'make' for Perintah in self.상자.명령들))

    def test_다른VM이름충돌(self):
        self.상자.가상기계들[str(uuid.uuid4())] = {'name': 'jkoros operating system'}
        with self.assertRaises(modul_VALUE.실행오류): self.laksanakan_perintah.laksanakan_perintah()
        self.변경없음()

    def test_소유표식거부(self):
        self.cipta_pemasukan()['owner'] = 'someone-else'
        with self.assertRaises(modul_VALUE.실행오류): self.laksanakan_perintah.laksanakan_perintah()
        self.변경없음()

    def test_다른설정경로거부(self):
        self.cipta_pemasukan()['CfgFile'] = '/tmp/someone-else.vbox'
        with self.assertRaises(modul_VALUE.실행오류): self.laksanakan_perintah.laksanakan_perintah()
        self.변경없음()

    def test_사용자추가디스크보존(self):
        mesin = self.cipta_pemasukan()
        mesin['VMState'] = 'poweroff'
        mesin['JKOROS IDE-0-1'] = '/external/user.vdi'
        with self.assertRaises(modul_VALUE.실행오류): self.laksanakan_perintah.laksanakan_perintah()
        self.변경없음()

    def test_전환중거부(self):
        self.cipta_pemasukan()['VMState'] = 'saving'
        with self.assertRaises(modul_VALUE.실행오류): self.laksanakan_perintah.laksanakan_perintah()
        self.변경없음()

    def test_등록해제거부(self):
        self.cipta_pemasukan()
        self.상자.가상기계들.clear()
        with self.assertRaises(modul_VALUE.실행오류): self.laksanakan_perintah.laksanakan_perintah()
        self.변경없음()

    def test_빌드실패시VM유지(self):
        mesin = self.cipta_pemasukan()
        mesin['VMState'] = 'poweroff'
        이전 = dict(mesin)
        self.상자.kegagalan_VALUE = 'make'
        with self.assertRaises(modul_VALUE.실행오류): self.laksanakan_perintah.laksanakan_perintah()
        self.assertEqual(mesin, 이전)

    def test_중단된소유표식설정복구(self):
        self.상자.kegagalan_VALUE = 'setextradata'
        with self.assertRaises(modul_VALUE.실행오류): self.laksanakan_perintah.laksanakan_perintah()
        self.상자.명령들.clear()
        self.assertEqual(self.laksanakan_perintah.laksanakan_perintah()['state'], 'running')
        self.assertFalse(any(Perintah[1] == 'createvm' for Perintah in self.상자.명령들))

    def test_보존ISO변조거부(self):
        mesin = self.cipta_pemasukan()
        mesin['VMState'] = 'poweroff'
        Path(mesin['JKOROS IDE-0-0']).write_bytes(b'changed')
        with self.assertRaises(modul_VALUE.실행오류): self.laksanakan_perintah.laksanakan_perintah()

    def test_상태미생성(self):
        self.assertEqual(self.laksanakan_perintah.tayang_status()['state'], 'not-created')
        self.assertFalse(self.상자.명령들)

    def test_경로탈출거부(self):
        for LALUAN in ('../outside', '/tmp/outside'):
            with self.assertRaises(modul_VALUE.실행오류): self.laksanakan_perintah.LALUAN(LALUAN)
        (self.akar_VALUE / '.vbox/media').symlink_to('/tmp')
        with self.assertRaises(modul_VALUE.실행오류): self.laksanakan_perintah.LALUAN('media/kernel.iso')

    def test_VirtualBox52복합속성(self):
        ukuran = modul_VALUE.atribut_VALUE('VMState="running"\nVideoMode="720,400,0"@0,0 1\n"IDE-0-0"="/a b.iso"')
        self.assertEqual(ukuran['VMState'], 'running')
        self.assertEqual(ukuran['IDE-0-0'], '/a b.iso')


if __name__ == '__main__': unittest.main()
