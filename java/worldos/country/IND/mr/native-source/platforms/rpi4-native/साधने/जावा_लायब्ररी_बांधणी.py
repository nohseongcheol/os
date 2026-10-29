"""स्वकीय JVM용 मराठी class/JAR와 EL0에 넣을 वाचन 전용 class 자료를 만든다."""
from pathlib import Path
import json
import zipfile


def जावा_लायब्ररी_तयार_करा(मूळ_पथ, आज्ञा_कार्यवाही_करा):
    (मूळ_पथ / 'build/user').mkdir(parents=True, exist_ok=True)
    प्रदान = मूळ_पथ / 'build/java-library'
    वर्ग_पथ = प्रदान / 'classes'
    वर्ग_पथ.mkdir(parents=True, exist_ok=True)
    स्रोतसूची = sorted((मूळ_पथ / 'स्वकीय_जावा').rglob('*.java'))
    आज्ञा_कार्यवाही_करा(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', वर्ग_पथ] + स्रोतसूची)
    नोंदी_यादी = []
    for मूळ_पत्ता_4c9bece9 in स्रोतसूची:
        सापेक्ष_पथ = मूळ_पत्ता_4c9bece9.relative_to(मूळ_पथ / 'स्वकीय_जावा').with_suffix('.class')
        पेलोड_डेटा = (वर्ग_पथ / सापेक्ष_पथ).read_bytes()
        नाव = str(सापेक्ष_पथ).replace('/', '.')
        if len(पेलोड_डेटा) > 16384 or len(नाव.encode('utf-8')) > 511:
            raise ValueError('JVM class/name limit: ' + नाव)
        नोंदी_यादी.append((सापेक्ष_पथ, नाव, पेलोड_डेटा))
    शीर्षलेख_मूल्य = ['/* Generated class resources; accessed only within the EL0 JVM. */',
              'typedef struct { const char *नाव; const unsigned char *डेटा; unsigned आकार; } जावा_वर्ग_संसाधन;']
    for क्रमांक_अनुक्रमणिका, (_, नाव, पेलोड_डेटा) in enumerate(नोंदी_यादी):
        शीर्षलेख_मूल्य.append('static const unsigned char जावा_वर्ग_डेटा%d[] = {%s};' % (क्रमांक_अनुक्रमणिका, ','.join(str(दुसरे_मूल्य) for दुसरे_मूल्य in पेलोड_डेटा)))
    शीर्षलेख_मूल्य.append('static const जावा_वर्ग_संसाधन जावा_वर्ग_यादी[] = {')
    for क्रमांक_अनुक्रमणिका, (_, नाव, पेलोड_डेटा) in enumerate(नोंदी_यादी):
        शीर्षलेख_मूल्य.append('{%s, जावा_वर्ग_डेटा%d, %d},' % (json.dumps(नाव, ensure_ascii=False), क्रमांक_अनुक्रमणिका, len(पेलोड_डेटा)))
    शीर्षलेख_मूल्य.append('};')
    (मूळ_पथ / 'build/user/java-resources.h').write_text('\n'.join(शीर्षलेख_मूल्य) + '\n', encoding='utf-8')
    वितरण_पथ = मूळ_पथ / 'dist'; वितरण_पथ.mkdir(exist_ok=True)
    with zipfile.ZipFile(str(वितरण_पथ / 'jkoros-native-korean.jar'), 'w', compression=zipfile.ZIP_DEFLATED) as जावा_बंडल:
        for सापेक्ष_पथ, _, पेलोड_डेटा in नोंदी_यादी:
            सिस्टम_माहिती = zipfile.ZipInfo(str(सापेक्ष_पथ), date_time=(1980, 1, 1, 0, 0, 0)); सिस्टम_माहिती.compress_type = zipfile.ZIP_DEFLATED
            जावा_बंडल.writestr(सिस्टम_माहिती, पेलोड_डेटा)
    with zipfile.ZipFile(str(वितरण_पथ / 'jkoros-native-korean-sources.zip'), 'w', compression=zipfile.ZIP_DEFLATED) as संग्रह:
        for मूळ_पत्ता_4c9bece9 in स्रोतसूची:
            सिस्टम_माहिती = zipfile.ZipInfo(str(मूळ_पत्ता_4c9bece9.relative_to(मूळ_पथ / 'स्वकीय_जावा')), date_time=(1980, 1, 1, 0, 0, 0)); सिस्टम_माहिती.compress_type = zipfile.ZIP_DEFLATED
            संग्रह.writestr(सिस्टम_माहिती, मूळ_पत्ता_4c9bece9.read_bytes())
