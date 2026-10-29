#!/usr/bin/env python3
"""मागील_आयटम Python 경로를 Java 미리 번역기에 연결한다. भाषांतर_करा_स्रोत 구현은 जावा_साधने/에 있다."""
from pathlib import Path
import subprocess
import sys
import tempfile
from संकलक import संकलन_त्रुटी

प्रोजेक्ट_मूळ = Path(__file__).resolve().parent

class मशीन_संहिता_संकलक:
    def __init__(स्वतः, आदान_वर्ग, निष्पादन_लक्ष्य='kernel', गतिमानस्मृतिराशी_शब्द_गणना=262144):
        स्वतः.पथ_यादी = [डेटा.मार्ग for डेटा in आदान_वर्ग]
        स्वतः.निष्पादन_लक्ष्य = निष्पादन_लक्ष्य
        स्वतः.गतिमानस्मृतिराशी_शब्द_गणना = गतिमानस्मृतिराशी_शब्द_गणना

    def तयार_करा(स्वतः, प्रविष्टी_गुण, निर्यात_करा_नोंदी, सार्वत्रिक_वर्ण_संकेतन=False):
        with tempfile.TemporaryDirectory(prefix='java-aot-') as पारपाडा_कार्य:
            मोजमाप_पथ = Path(पारपाडा_कार्य)/'generated.c'
            आदेश = ['sh', str(प्रोजेक्ट_मूळ/'आगाऊ_संबंधित_वेळ.sh'), '--entry', प्रविष्टी_गुण,
                    '--profile', स्वतः.निष्पादन_लक्ष्य, '--heap-words', str(स्वतः.गतिमानस्मृतिराशी_शब्द_गणना), '-o', str(मोजमाप_पथ)]
            if सार्वत्रिक_वर्ण_संकेतन: आदेश.append('--ucn')
            for नेमा_मूल्य in निर्यात_करा_नोंदी: आदेश.extend(['--export', नेमा_मूल्य])
            आदेश.extend(str(मार्ग) for मार्ग in स्वतः.पथ_यादी)
            मोजमाप = subprocess.run(आदेश, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if मोजमाप.returncode: raise संकलन_त्रुटी(मोजमाप.stderr.decode('utf-8', 'replace'))
            return मोजमाप_पथ.read_text()

def सुरू_करा():
    raise SystemExit(subprocess.call(['sh', str(प्रोजेक्ट_मूळ/'आगाऊ_संबंधित_वेळ.sh')] + sys.argv[1:]))

if __name__ == '__main__': सुरू_करा()
