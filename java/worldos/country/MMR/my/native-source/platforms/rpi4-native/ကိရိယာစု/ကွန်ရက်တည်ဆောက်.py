from pathlib import Path
import tempfile
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from ip_config import write_header


def ကွန်ရက်ဖန်တီး(အမြစ်လမ်းကြောင်း, Cဘာသာပြန်စက်, မော်ကွန်းကိရိယာတစ်ခု, ပြင်ဆင်မှုဘစ်များ, စက်မောင်း):
    မူရင်းဒေတာ = အမြစ်လမ်းကြောင်း / 'vendor/lwip/src'
    ဆက်သွယ်ပေါက်ကိန်း = အမြစ်လမ်းကြောင်း / 'ကွန်ရက်အလွှာစု'
    출력결과 = အမြစ်လမ်းကြောင်း / 'build/network'
    출력결과.mkdir(exist_ok=True)
    write_header(အမြစ်လမ်းကြောင်း, 출력결과 / 'ip_config.h')
    ဖိုင်စာရင်း = sorted((မူရင်းဒေတာ / 'core').glob('*.c')) + sorted((မူရင်းဒေတာ / 'core/ipv4').glob('*.c'))
    ဖိုင်စာရင်း += [မူရင်းဒေတာ / 'netif/ethernet.c']
    ဖိုင်စာရင်း += sorted(ဆက်သွယ်ပေါက်ကိန်း.glob('*.c'))
    ဦးတည်ရာဖိုင်များ = []
    for လမ်း in ဖိုင်စာရင်း:
        ဦးတည်ရာဖိုင် = 출력결과 / (လမ်း.stem + '.o')
        စက်မောင်း([Cဘာသာပြန်စက်] + ပြင်ဆင်မှုဘစ်များ + ['-include', 출력결과 / 'ip_config.h', '-std=c11', '-I', ဆက်သွယ်ပေါက်ကိန်း, '-I', မူရင်းဒေတာ / 'include',
             '-I', အမြစ်လမ်းကြောင်း.parents[1] / 'posix-kor/arm64-native/ခေါင်းစီးဖိုင်', '-c', လမ်း, '-o', ဦးတည်ရာဖိုင်])
        ဦးတည်ရာဖိုင်များ.append(ဦးတည်ရာဖိုင်)
    စာကြည့်တိုက် = 출력결과 / 'libnetwork.a'
    # ar rcs retains members removed or renamed in the source tree. Build a
    # fresh archive so old English/Korean object names cannot coexist.
    with tempfile.TemporaryDirectory(prefix='archive-', dir=str(출력결과)) as ယာယီလမ်းကြောင်း:
        အသစ်စာကြည့်တိုက်=Path(ယာယီလမ်းကြောင်း)/'libnetwork.a'
        စက်မောင်း([မော်ကွန်းကိရိယာတစ်ခု, 'rcs', အသစ်စာကြည့်တိုက်] + ဦးတည်ရာဖိုင်များ)
        အသစ်စာကြည့်တိုက်.replace(စာကြည့်တိုက်)
    return စာကြည့်တိုက်
