import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import uuid

व्याख्या_मूल्य = importlib.util.spec_from_file_location('jkoros_vbox', str(Path(__file__).resolve().parents[1] / 'व्हर्च्युअल_पेटी_व्यवस्थापक.py'))
मॉड्यूल_मूल्य = importlib.util.module_from_spec(व्याख्या_मूल्य)
व्याख्या_मूल्य.loader.exec_module(मॉड्यूल_मूल्य)


class अनुकृत_पेटी:
    def __init__(self, मूळ_मूल्य):
        self.मूळ_मूल्य = मूळ_मूल्य
        self.आदेश_यादी = []
        self.व्हर्च्युअल_यंत्रे = {}
        self.बिघाड_मूल्य = None

    def __call__(self, बाबी):
        बाबी = list(map(str, बाबी))
        self.आदेश_यादी.append(बाबी)
        if self.बिघाड_मूल्य == बाबी[1] or (बाबी[0] == 'make' and self.बिघाड_मूल्य == 'make'):
            self.बिघाड_मूल्य = None
            raise मॉड्यूल_मूल्य.निष्पादन_त्रुटी('시험용 बिघाड_मूल्य')
        if बाबी[0] == 'make':
            मार्ग = self.मूळ_मूल्य / 'os/build/kernel.iso'
            मार्ग.parent.mkdir(parents=True, exist_ok=True)
            मार्ग.write_bytes(b'fake-iso-for-launcher-test')
            return 'build complete\n'
        कृती = बाबी[1]
        if कृती == 'list':
            return '\n'.join('"{}" {{{}}}'.format(मूल्य['name'], अनुक्रमणिका) for अनुक्रमणिका, मूल्य in self.व्हर्च्युअल_यंत्रे.items())
        if कृती == 'createvm':
            अनुक्रमणिका, नाव = बाबी[बाबी.index('--uuid') + 1], बाबी[बाबी.index('--name') + 1]
            self.व्हर्च्युअल_यंत्रे[अनुक्रमणिका] = {'UUID': अनुक्रमणिका, 'name': नाव, 'VMState': 'poweroff',
                'CfgFile': str(self.मूळ_मूल्य / '.vbox/machines' / नाव / (नाव + '.vbox')), 'owner': None}
            return ''
        मशीन = self.व्हर्च्युअल_यंत्रे[बाबी[2]]
        if कृती == 'showvminfo':
            return '\n'.join('{}={}'.format(json.dumps(नाव), json.dumps(मूल्य)) for नाव, मूल्य in मशीन.items() if नाव != 'owner')
        if कृती == 'getextradata': return 'Value: ' + मशीन['owner'] if मशीन['owner'] else 'No value set!'
        if कृती == 'setextradata': मशीन['owner'] = बाबी[4]
        elif कृती == 'storagectl': मशीन['storagecontrollername0'] = 'JKOROS IDE'
        elif कृती == 'storageattach': मशीन['JKOROS IDE-0-0'] = बाबी[बाबी.index('--medium') + 1]
        elif कृती == 'startvm': मशीन['VMState'] = 'running'
        elif कृती == 'controlvm':
            assert बाबी[3] == 'resume'
            मशीन['VMState'] = 'running'
        elif कृती != 'modifyvm': raise AssertionError(बाबी)
        return ''


class रन_चाचणी(unittest.TestCase):
    def setUp(self):
        self.तात्पुरते_मूल्य = tempfile.TemporaryDirectory(prefix='jkoros-vbox-test-')
        self.addCleanup(self.तात्पुरते_मूल्य.cleanup)
        self.मूळ_मूल्य = Path(self.तात्पुरते_मूल्य.name)
        (self.मूळ_मूल्य / '.vbox').mkdir()
        self.पेटी_मूल्य = अनुकृत_पेटी(self.मूळ_मूल्य)
        self.आज्ञा_कार्यवाही_करा = मॉड्यूल_मूल्य.अनुप्रयोग_चालक(self.मूळ_मूल्य, 'jkoros operating system', आदेश=self.पेटी_मूल्य)

    def प्रविष्टी_तयार_करा(self):
        मोजमाप = self.आज्ञा_कार्यवाही_करा.आज्ञा_कार्यवाही_करा()
        self.पेटी_मूल्य.आदेश_यादी.clear()
        return self.पेटी_मूल्य.व्हर्च्युअल_यंत्रे[मोजमाप['uuid']]

    def आहे_अपरिवर्तित(self):
        self.assertTrue(all(आदेश[0] == 'VBoxManage' and आदेश[1] in ('list', 'showvminfo', 'getextradata') for आदेश in self.पेटी_मूल्य.आदेश_यादी))

    def प्रारंभिक_निर्मिती_आणि_प्रकाशीय_प्रणालीप्रारंभ_चाचणी(self):
        मोजमाप = self.आज्ञा_कार्यवाही_करा.आज्ञा_कार्यवाही_करा()
        self.assertEqual(मोजमाप['state'], 'running')
        self.assertTrue(Path(मोजमाप['iso']).is_file())
        self.assertTrue(any('--nic1' in आदेश and 'none' in आदेश for आदेश in self.पेटी_मूल्य.आदेश_यादी))
        self.assertFalse(any('hdd' in आदेश or 'discardstate' in आदेश or 'createmedium' in आदेश for आदेश in self.पेटी_मूल्य.आदेश_यादी))

    def धावणे_आभासीयंत्र_जतनकेलेले_चाचणी(self):
        self.प्रविष्टी_तयार_करा()
        self.assertEqual(self.आज्ञा_कार्यवाही_करा.आज्ञा_कार्यवाही_करा()['state'], 'running')
        self.आहे_अपरिवर्तित()

    def साठवलेले_राज्य_पुन्हाचालूकरा_आणि_लॉग_जतन_चाचणी(self):
        मशीन = self.प्रविष्टी_तयार_करा()
        मशीन['VMState'] = 'saved'
        लॉग_मूल्य = self.आज्ञा_कार्यवाही_करा.मार्ग(self.आज्ञा_कार्यवाही_करा.वाचन()['serial_log'])
        लॉग_मूल्य.write_text('saved log')
        self.आज्ञा_कार्यवाही_करा.आज्ञा_कार्यवाही_करा()
        self.assertFalse(any(आदेश[0] == 'make' or आदेश[1] == 'modifyvm' for आदेश in self.पेटी_मूल्य.आदेश_यादी))
        self.assertEqual([मार्ग.read_text() for मार्ग in लॉग_मूल्य.parent.glob('before-resume-*.log')], ['saved log'])

    def विराम_आणि_पुन्हाचालूकरा_चाचणी(self):
        self.प्रविष्टी_तयार_करा()['VMState'] = 'paused'
        self.आज्ञा_कार्यवाही_करा.आज्ञा_कार्यवाही_करा()
        self.assertTrue(any(आदेश[1] == 'controlvm' and आदेश[3] == 'resume' for आदेश in self.पेटी_मूल्य.आदेश_यादी))
        self.assertFalse(any(आदेश[0] == 'make' for आदेश in self.पेटी_मूल्य.आदेश_यादी))

    def दुसरे_आभासीयंत्र_नाव_नामसंघर्ष_चाचणी(self):
        self.पेटी_मूल्य.व्हर्च्युअल_यंत्रे[str(uuid.uuid4())] = {'name': 'jkoros operating system'}
        with self.assertRaises(मॉड्यूल_मूल्य.निष्पादन_त्रुटी): self.आज्ञा_कार्यवाही_करा.आज्ञा_कार्यवाही_करा()
        self.आहे_अपरिवर्तित()

    def मालकी_खूण_नाकारलेले_चाचणी(self):
        self.प्रविष्टी_तयार_करा()['owner'] = 'someone-else'
        with self.assertRaises(मॉड्यूल_मूल्य.निष्पादन_त्रुटी): self.आज्ञा_कार्यवाही_करा.आज्ञा_कार्यवाही_करा()
        self.आहे_अपरिवर्तित()

    def दुसरे_सेटिंग्ज_पथ_नाकारलेले_चाचणी(self):
        self.प्रविष्टी_तयार_करा()['CfgFile'] = '/tmp/someone-else.vbox'
        with self.assertRaises(मॉड्यूल_मूल्य.निष्पादन_त्रुटी): self.आज्ञा_कार्यवाही_करा.आज्ञा_कार्यवाही_करा()
        self.आहे_अपरिवर्तित()

    def अतिरिक्त_प्रयोक्ता_डिस्क_जतनकेलेले_चाचणी(self):
        मशीन = self.प्रविष्टी_तयार_करा()
        मशीन['VMState'] = 'poweroff'
        मशीन['JKOROS IDE-0-1'] = '/external/user.vdi'
        with self.assertRaises(मॉड्यूल_मूल्य.निष्पादन_त्रुटी): self.आज्ञा_कार्यवाही_करा.आज्ञा_कार्यवाही_करा()
        self.आहे_अपरिवर्तित()

    def संक्रमण_नाकारलेले_चाचणी(self):
        self.प्रविष्टी_तयार_करा()['VMState'] = 'saving'
        with self.assertRaises(मॉड्यूल_मूल्य.निष्पादन_त्रुटी): self.आज्ञा_कार्यवाही_करा.आज्ञा_कार्यवाही_करा()
        self.आहे_अपरिवर्तित()

    def नोंदणीकाढा_नाकारलेले_चाचणी(self):
        self.प्रविष्टी_तयार_करा()
        self.पेटी_मूल्य.व्हर्च्युअल_यंत्रे.clear()
        with self.assertRaises(मॉड्यूल_मूल्य.निष्पादन_त्रुटी): self.आज्ञा_कार्यवाही_करा.आज्ञा_कार्यवाही_करा()
        self.आहे_अपरिवर्तित()

    def आभासीयंत्र_जतनकेलेले_चालू_बांधणी_बिघाड_चाचणी(self):
        मशीन = self.प्रविष्टी_तयार_करा()
        मशीन['VMState'] = 'poweroff'
        मागील_आयटम = dict(मशीन)
        self.पेटी_मूल्य.बिघाड_मूल्य = 'make'
        with self.assertRaises(मॉड्यूल_मूल्य.निष्पादन_त्रुटी): self.आज्ञा_कार्यवाही_करा.आज्ञा_कार्यवाही_करा()
        self.assertEqual(मशीन, मागील_आयटम)

    def खंडित_मालकी_खूण_पुनर्प्राप्ती_चाचणी(self):
        self.पेटी_मूल्य.बिघाड_मूल्य = 'setextradata'
        with self.assertRaises(मॉड्यूल_मूल्य.निष्पादन_त्रुटी): self.आज्ञा_कार्यवाही_करा.आज्ञा_कार्यवाही_करा()
        self.पेटी_मूल्य.आदेश_यादी.clear()
        self.assertEqual(self.आज्ञा_कार्यवाही_करा.आज्ञा_कार्यवाही_करा()['state'], 'running')
        self.assertFalse(any(आदेश[1] == 'createvm' for आदेश in self.पेटी_मूल्य.आदेश_यादी))

    def जतनकेलेले_आयएसओ_अनधिकृतफेरफार_नाकारलेले_चाचणी(self):
        मशीन = self.प्रविष्टी_तयार_करा()
        मशीन['VMState'] = 'poweroff'
        Path(मशीन['JKOROS IDE-0-0']).write_bytes(b'changed')
        with self.assertRaises(मॉड्यूल_मूल्य.निष्पादन_त्रुटी): self.आज्ञा_कार्यवाही_करा.आज्ञा_कार्यवाही_करा()

    def नाही_राज्य_निर्मित_चाचणी(self):
        self.assertEqual(self.आज्ञा_कार्यवाही_करा.राज्य_शो()['state'], 'not-created')
        self.assertFalse(self.पेटी_मूल्य.आदेश_यादी)

    def पथ_निसटवणी_नाकारलेले_चाचणी(self):
        for मार्ग in ('../outside', '/tmp/outside'):
            with self.assertRaises(मॉड्यूल_मूल्य.निष्पादन_त्रुटी): self.आज्ञा_कार्यवाही_करा.मार्ग(मार्ग)
        (self.मूळ_मूल्य / '.vbox/media').symlink_to('/tmp')
        with self.assertRaises(मॉड्यूल_मूल्य.निष्पादन_त्रुटी): self.आज्ञा_कार्यवाही_करा.मार्ग('media/kernel.iso')

    def व्हर्च्युअलबॉक्स_52_संमिश्र_गुणधर्म_चाचणी(self):
        मोजमाप = मॉड्यूल_मूल्य.गुणधर्म_मूल्य('VMState="running"\nVideoMode="720,400,0"@0,0 1\n"IDE-0-0"="/a b.iso"')
        self.assertEqual(मोजमाप['VMState'], 'running')
        self.assertEqual(मोजमाप['IDE-0-0'], '/a b.iso')


if __name__ == '__main__': unittest.main()
