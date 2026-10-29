import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import uuid

சொற்பொருள்_விளக்கம்_மதிப்பு = importlib.util.spec_from_file_location('jkoros_vbox', str(Path(__file__).resolve().parents[1] / '가상상자.py'))
தொகுதி_மதிப்பு = importlib.util.module_from_spec(சொற்பொருள்_விளக்கம்_மதிப்பு)
சொற்பொருள்_விளக்கம்_மதிப்பு.loader.exec_module(தொகுதி_மதிப்பு)


class 가짜상자:
    def __init__(self, மூலம்_மதிப்பு):
        self.மூலம்_மதிப்பு = மூலம்_மதிப்பு
        self.명령들 = []
        self.가상기계들 = {}
        self.செயலிழப்பு_மதிப்பு = None

    def __call__(self, செயலுருபுகள்):
        செயலுருபுகள் = list(map(str, செயலுருபுகள்))
        self.명령들.append(செயலுருபுகள்)
        if self.செயலிழப்பு_மதிப்பு == செயலுருபுகள்[1] or (செயலுருபுகள்[0] == 'make' and self.செயலிழப்பு_மதிப்பு == 'make'):
            self.செயலிழப்பு_மதிப்பு = None
            raise தொகுதி_மதிப்பு.실행오류('시험용 செயலிழப்பு_மதிப்பு')
        if செயலுருபுகள்[0] == 'make':
            பாதை_2 = self.மூலம்_மதிப்பு / 'os/build/kernel.iso'
            பாதை_2.parent.mkdir(parents=True, exist_ok=True)
            பாதை_2.write_bytes(b'fake-iso-for-launcher-test')
            return 'build complete\n'
        செயல் = செயலுருபுகள்[1]
        if செயல் == 'list':
            return '\n'.join('"{}" {{{}}}'.format(மதிப்பு['name'], அடைவு) for அடைவு, மதிப்பு in self.가상기계들.items())
        if செயல் == 'createvm':
            அடைவு, பெயர் = செயலுருபுகள்[செயலுருபுகள்.index('--uuid') + 1], செயலுருபுகள்[செயலுருபுகள்.index('--name') + 1]
            self.가상기계들[அடைவு] = {'UUID': அடைவு, 'name': பெயர், 'VMState': 'poweroff',
                'CfgFile': str(self.மூலம்_மதிப்பு / '.vbox/machines' / பெயர் / (பெயர் + '.vbox')), 'owner': None}
            return ''
        இயந்திரம் = self.가상기계들[செயலுருபுகள்[2]]
        if செயல் == 'showvminfo':
            return '\n'.join('{}={}'.format(json.dumps(பெயர்), json.dumps(மதிப்பு)) for பெயர், மதிப்பு in இயந்திரம்.items() if பெயர் != 'owner')
        if செயல் == 'getextradata': return 'Value: ' + இயந்திரம்['owner'] if இயந்திரம்['owner'] else 'No value set!'
        if செயல் == 'setextradata': இயந்திரம்['owner'] = செயலுருபுகள்[4]
        elif செயல் == 'storagectl': இயந்திரம்['storagecontrollername0'] = 'JKOROS IDE'
        elif செயல் == 'storageattach': இயந்திரம்['JKOROS IDE-0-0'] = செயலுருபுகள்[செயலுருபுகள்.index('--medium') + 1]
        elif செயல் == 'startvm': இயந்திரம்['VMState'] = 'running'
        elif செயல் == 'controlvm':
            assert செயலுருபுகள்[3] == 'resume'
            இயந்திரம்['VMState'] = 'running'
        elif செயல் != 'modifyvm': raise AssertionError(செயலுருபுகள்)
        return ''


class சோதனை_இயக்கம்(unittest.TestCase):
    def setUp(self):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-vbox-test-')
        self.addCleanup(self.임시.cleanup)
        self.மூலம்_மதிப்பு = Path(self.임시.name)
        (self.மூலம்_மதிப்பு / '.vbox').mkdir()
        self.상자 = 가짜상자(self.மூலம்_மதிப்பு)
        self.இயக்கு_கட்டளை = தொகுதி_மதிப்பு.நிரல்_துவக்குநர்(self.மூலம்_மதிப்பு, 'jkoros operating system', கட்டளை=self.상자)

    def உருவாக்கு_உள்ளீடு(self):
        அளவிடக்கூடியது = self.இயக்கு_கட்டளை.இயக்கு_கட்டளை()
        self.상자.명령들.clear()
        return self.상자.가상기계들[அளவிடக்கூடியது['uuid']]

    def 변경없음(self):
        self.assertTrue(all(கட்டளை[0] == 'VBoxManage' and கட்டளை[1] in ('list', 'showvminfo', 'getextradata') for கட்டளை in self.상자.명령들))

    def test_첫생성과광학부팅(self):
        அளவிடக்கூடியது = self.இயக்கு_கட்டளை.இயக்கு_கட்டளை()
        self.assertEqual(அளவிடக்கூடியது['state'], 'running')
        self.assertTrue(Path(அளவிடக்கூடியது['iso']).is_file())
        self.assertTrue(any('--nic1' in கட்டளை and 'none' in கட்டளை for கட்டளை in self.상자.명령들))
        self.assertFalse(any('hdd' in கட்டளை or 'discardstate' in கட்டளை or 'createmedium' in கட்டளை for கட்டளை in self.상자.명령들))

    def test_실행중유지(self):
        self.உருவாக்கு_உள்ளீடு()
        self.assertEqual(self.இயக்கு_கட்டளை.இயக்கு_கட்டளை()['state'], 'running')
        self.변경없음()

    def test_저장상태재개와로그보존(self):
        இயந்திரம் = self.உருவாக்கு_உள்ளீடு()
        இயந்திரம்['VMState'] = 'saved'
        பதிவு_மதிப்பு = self.இயக்கு_கட்டளை.பாதை_2(self.இயக்கு_கட்டளை.படி()['serial_log'])
        பதிவு_மதிப்பு.write_text('saved log')
        self.இயக்கு_கட்டளை.இயக்கு_கட்டளை()
        self.assertFalse(any(கட்டளை[0] == 'make' or கட்டளை[1] == 'modifyvm' for கட்டளை in self.상자.명령들))
        self.assertEqual([பாதை_2.read_text() for பாதை_2 in பதிவு_மதிப்பு.parent.glob('before-resume-*.log')], ['saved log'])

    def test_일시정지재개(self):
        self.உருவாக்கு_உள்ளீடு()['VMState'] = 'paused'
        self.இயக்கு_கட்டளை.இயக்கு_கட்டளை()
        self.assertTrue(any(கட்டளை[1] == 'controlvm' and கட்டளை[3] == 'resume' for கட்டளை in self.상자.명령들))
        self.assertFalse(any(கட்டளை[0] == 'make' for கட்டளை in self.상자.명령들))

    def test_다른VM이름충돌(self):
        self.상자.가상기계들[str(uuid.uuid4())] = {'name': 'jkoros operating system'}
        with self.assertRaises(தொகுதி_மதிப்பு.실행오류): self.இயக்கு_கட்டளை.இயக்கு_கட்டளை()
        self.변경없음()

    def test_소유표식거부(self):
        self.உருவாக்கு_உள்ளீடு()['owner'] = 'someone-else'
        with self.assertRaises(தொகுதி_மதிப்பு.실행오류): self.இயக்கு_கட்டளை.இயக்கு_கட்டளை()
        self.변경없음()

    def test_다른설정경로거부(self):
        self.உருவாக்கு_உள்ளீடு()['CfgFile'] = '/tmp/someone-else.vbox'
        with self.assertRaises(தொகுதி_மதிப்பு.실행오류): self.இயக்கு_கட்டளை.இயக்கு_கட்டளை()
        self.변경없음()

    def test_사용자추가디스크보존(self):
        இயந்திரம் = self.உருவாக்கு_உள்ளீடு()
        இயந்திரம்['VMState'] = 'poweroff'
        இயந்திரம்['JKOROS IDE-0-1'] = '/external/user.vdi'
        with self.assertRaises(தொகுதி_மதிப்பு.실행오류): self.இயக்கு_கட்டளை.இயக்கு_கட்டளை()
        self.변경없음()

    def test_전환중거부(self):
        self.உருவாக்கு_உள்ளீடு()['VMState'] = 'saving'
        with self.assertRaises(தொகுதி_மதிப்பு.실행오류): self.இயக்கு_கட்டளை.இயக்கு_கட்டளை()
        self.변경없음()

    def test_등록해제거부(self):
        self.உருவாக்கு_உள்ளீடு()
        self.상자.가상기계들.clear()
        with self.assertRaises(தொகுதி_மதிப்பு.실행오류): self.இயக்கு_கட்டளை.இயக்கு_கட்டளை()
        self.변경없음()

    def test_빌드실패시VM유지(self):
        இயந்திரம் = self.உருவாக்கு_உள்ளீடு()
        இயந்திரம்['VMState'] = 'poweroff'
        이전 = dict(இயந்திரம்)
        self.상자.செயலிழப்பு_மதிப்பு = 'make'
        with self.assertRaises(தொகுதி_மதிப்பு.실행오류): self.இயக்கு_கட்டளை.இயக்கு_கட்டளை()
        self.assertEqual(இயந்திரம், 이전)

    def test_중단된소유표식설정복구(self):
        self.상자.செயலிழப்பு_மதிப்பு = 'setextradata'
        with self.assertRaises(தொகுதி_மதிப்பு.실행오류): self.இயக்கு_கட்டளை.இயக்கு_கட்டளை()
        self.상자.명령들.clear()
        self.assertEqual(self.இயக்கு_கட்டளை.இயக்கு_கட்டளை()['state'], 'running')
        self.assertFalse(any(கட்டளை[1] == 'createvm' for கட்டளை in self.상자.명령들))

    def test_보존ISO변조거부(self):
        இயந்திரம் = self.உருவாக்கு_உள்ளீடு()
        இயந்திரம்['VMState'] = 'poweroff'
        Path(இயந்திரம்['JKOROS IDE-0-0']).write_bytes(b'changed')
        with self.assertRaises(தொகுதி_மதிப்பு.실행오류): self.இயக்கு_கட்டளை.இயக்கு_கட்டளை()

    def test_상태미생성(self):
        self.assertEqual(self.இயக்கு_கட்டளை.காட்சி_நிலை()['state'], 'not-created')
        self.assertFalse(self.상자.명령들)

    def test_경로탈출거부(self):
        for பாதை_2 in ('../outside', '/tmp/outside'):
            with self.assertRaises(தொகுதி_மதிப்பு.실행오류): self.இயக்கு_கட்டளை.பாதை_2(பாதை_2)
        (self.மூலம்_மதிப்பு / '.vbox/media').symlink_to('/tmp')
        with self.assertRaises(தொகுதி_மதிப்பு.실행오류): self.இயக்கு_கட்டளை.பாதை_2('media/kernel.iso')

    def test_VirtualBox52복합속성(self):
        அளவிடக்கூடியது = தொகுதி_மதிப்பு.பண்புக்கூறு_மதிப்பு('VMState="running"\nVideoMode="720,400,0"@0,0 1\n"IDE-0-0"="/a b.iso"')
        self.assertEqual(அளவிடக்கூடியது['VMState'], 'running')
        self.assertEqual(அளவிடக்கூடியது['IDE-0-0'], '/a b.iso')


if __name__ == '__main__': unittest.main()
