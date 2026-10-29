"""ကိုယ်ပိုင် JVM용 မြန်မာ class/JAR와 EL0에 넣을 ဖတ် 전용 class 자료를 만든다."""
from pathlib import Path
import json
import zipfile


def Javaစာကြည့်တိုက်ဖန်တီး(အမြစ်လမ်းကြောင်း, စက်မောင်း):
    (အမြစ်လမ်းကြောင်း / 'build/user').mkdir(parents=True, exist_ok=True)
    출력결과 = အမြစ်လမ်းကြောင်း / 'build/java-library'
    အတန်းလမ်းကြောင်း = 출력결과 / 'classes'
    အတန်းလမ်းကြောင်း.mkdir(parents=True, exist_ok=True)
    မူရင်းကုဒ်စာရင်း = sorted((အမြစ်လမ်းကြောင်း / 'မြန်မာJava').rglob('*.java'))
    စက်မောင်း(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', အတန်းလမ်းကြောင်း] + မူရင်းကုဒ်စာရင်း)
    항목들 = []
    for မူရင်းလိပ်စာ in မူရင်းကုဒ်စာရင်း:
        နှိုင်းယှဉ်ဆက်နွယ်လမ်းကြောင်း = မူရင်းလိပ်စာ.relative_to(အမြစ်လမ်းကြောင်း / 'မြန်မာJava').with_suffix('.class')
        내용자료 = (အတန်းလမ်းကြောင်း / နှိုင်းယှဉ်ဆက်နွယ်လမ်းကြောင်း).read_bytes()
        အမည် = str(နှိုင်းယှဉ်ဆက်နွယ်လမ်းကြောင်း).replace('/', '.')
        if len(내용자료) > 16384 or len(အမည်.encode('utf-8')) > 511:
            raise ValueError('JVM class/name limit: ' + အမည်)
        항목들.append((နှိုင်းယှဉ်ဆက်နွယ်လမ်းကြောင်း, အမည်, 내용자료))
    ခေါင်းစီးတန်ဖိုး = ['/* Generated class resources; accessed only within the EL0 JVM. */',
              'typedef struct { const char *အမည်; const unsigned char *ဒေတာ; unsigned အရွယ်; } Javaအတန်းအရင်းအမြစ်;']
    for အစဉ်အမှတ်, (_, အမည်, 내용자료) in enumerate(항목들):
        ခေါင်းစီးတန်ဖိုး.append('static const unsigned char Javaအတန်းဒေတာ%d[] = {%s};' % (အစဉ်အမှတ်, ','.join(str(ဒုတိယတန်ဖိုး) for ဒုတိယတန်ဖိုး in 내용자료)))
    ခေါင်းစီးတန်ဖိုး.append('static const Javaအတန်းအရင်းအမြစ် Javaအတန်းစာရင်း[] = {')
    for အစဉ်အမှတ်, (_, အမည်, 내용자료) in enumerate(항목들):
        ခေါင်းစီးတန်ဖိုး.append('{%s, Javaအတန်းဒေတာ%d, %d},' % (json.dumps(အမည်, ensure_ascii=False), အစဉ်အမှတ်, len(내용자료)))
    ခေါင်းစီးတန်ဖိုး.append('};')
    (အမြစ်လမ်းကြောင်း / 'build/user/java-resources.h').write_text('\n'.join(ခေါင်းစီးတန်ဖိုး) + '\n', encoding='utf-8')
    ဖြန့်ချိမှုလမ်းကြောင်း = အမြစ်လမ်းကြောင်း / 'dist'; ဖြန့်ချိမှုလမ်းကြောင်း.mkdir(exist_ok=True)
    with zipfile.ZipFile(str(ဖြန့်ချိမှုလမ်းကြောင်း / 'jkoros-native-korean.jar'), 'w', compression=zipfile.ZIP_DEFLATED) as Javaအထုပ်:
        for နှိုင်းယှဉ်ဆက်နွယ်လမ်းကြောင်း, _, 내용자료 in 항목들:
            စနစ်သတင်းအချက်အလက် = zipfile.ZipInfo(str(နှိုင်းယှဉ်ဆက်နွယ်လမ်းကြောင်း), date_time=(1980, 1, 1, 0, 0, 0)); စနစ်သတင်းအချက်အလက်.compress_type = zipfile.ZIP_DEFLATED
            Javaအထုပ်.writestr(စနစ်သတင်းအချက်အလက်, 내용자료)
    with zipfile.ZipFile(str(ဖြန့်ချိမှုလမ်းကြောင်း / 'jkoros-native-korean-sources.zip'), 'w', compression=zipfile.ZIP_DEFLATED) as မော်ကွန်း:
        for မူရင်းလိပ်စာ in မူရင်းကုဒ်စာရင်း:
            စနစ်သတင်းအချက်အလက် = zipfile.ZipInfo(str(မူရင်းလိပ်စာ.relative_to(အမြစ်လမ်းကြောင်း / 'မြန်မာJava')), date_time=(1980, 1, 1, 0, 0, 0)); စနစ်သတင်းအချက်အလက်.compress_type = zipfile.ZIP_DEFLATED
            မော်ကွန်း.writestr(စနစ်သတင်းအချက်အလက်, မူရင်းလိပ်စာ.read_bytes())
