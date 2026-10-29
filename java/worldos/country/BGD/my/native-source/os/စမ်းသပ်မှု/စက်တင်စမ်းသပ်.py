#!/usr/bin/env python3
"""독립 QEMU를 디스크 없이 실행해 ELF/GRUB ISO 및 အစဉ်ဆက်တန်ဖိုး/PS2 입력을 검증한다."""
import json
from pathlib import Path
import select
import socket
import subprocess
import tempfile
import time

နေရာ = Path(__file__).resolve().parents[1]


def စောင့်(စစ်ဆေးချက်, ရှင်းလင်းချက်, ကန့်သတ်ချက်တန်ဖိုး=15):
    အဆုံး = time.monotonic() + ကန့်သတ်ချက်တန်ဖိုး
    while time.monotonic() < အဆုံး:
        ရလဒ် = စစ်ဆေးချက်()
        if ရလဒ်:
            return ရလဒ်
        time.sleep(0.05)
    raise AssertionError('အချိန်တန်ဖိုး 초과: ' + ရှင်းလင်းချက်)


def စမ်းသပ်မှု(အမျိုးအစားတန်ဖိုး):
    with tempfile.TemporaryDirectory(prefix='jkoros-boot-test-') as ယာယီတန်ဖိုး:
        ယာယီတန်ဖိုး = Path(ယာယီတန်ဖိုး)
        အစဉ်ဆက်လမ်းကြောင်း = ယာယီတန်ဖိုး / 'serial.sock'
        ကြီးကြပ်သူလမ်းကြောင်း = ယာယီတန်ဖိုး / 'monitor.sock'
        အမိန့် = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot',
                '-serial', 'unix:' + str(အစဉ်ဆက်လမ်းကြောင်း) + ',server,nowait',
                '-monitor', 'unix:' + str(ကြီးကြပ်သူလမ်းကြောင်း) + ',server,nowait']
        အမိန့် += ['-kernel', str(နေရာ / 'build/kernel.elf')] if အမျိုးအစားတန်ဖိုး == 'elf' else [
            '-cdrom', str(နေရာ / 'build/kernel.iso'), '-boot', 'd']
        # အစဉ်ဆက်တန်ဖိုး 클라이언트가 연결되기 전에 출력이 유실되지 않도록 CPU를 일시 정지한다.
        အမိန့် += ['-S']
        လုပ်ငန်းစဉ် = subprocess.Popen(အမိန့်, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        အစဉ်ဆက်တန်ဖိုး = socket.socket(socket.AF_UNIX)
        ကြီးကြပ်သူတန်ဖိုး = socket.socket(socket.AF_UNIX)
        မှတ်တမ်းမှတ်တမ်းတစ်ခု = bytearray()
        try:
            def ကွန်ရက်ပေါက်ပြင်ဆင်():
                if လုပ်ငန်းစဉ်.poll() is not None:
                    raise AssertionError(လုပ်ငန်းစဉ်.stderr.read().decode('utf-8', 'replace'))
                return အစဉ်ဆက်လမ်းကြောင်း.exists() and ကြီးကြပ်သူလမ်းကြောင်း.exists()
            စောင့်(ကွန်ရက်ပေါက်ပြင်ဆင်, 'QEMU ကွန်ရက်ပေါက်တန်ဖိုး')
            အစဉ်ဆက်တန်ဖိုး.connect(str(အစဉ်ဆက်လမ်းကြောင်း))
            ကြီးကြပ်သူတန်ဖိုး.connect(str(ကြီးကြပ်သူလမ်းကြောင်း))
            အစဉ်ဆက်တန်ဖိုး.setblocking(False)
            ကြီးကြပ်သူတန်ဖိုး.sendall(b'cont\n')

            def ခေါင်းစီးဖိုင်(အက္ခရာစဉ်, လုပ်ဆောင်=0):
                ဖတ်, _, _ = select.select([အစဉ်ဆက်တန်ဖိုး], [], [], 0.1)
                if ဖတ်:
                    ဒေတာ = အစဉ်ဆက်တန်ဖိုး.recv(65536)
                    if not ဒေတာ:
                        raise AssertionError('အစဉ်ဆက်တန်ဖိုး ချိတ်ဆက် ထွက်ပရိုဂရမ်')
                    မှတ်တမ်းမှတ်တမ်းတစ်ခု.extend(ဒေတာ)
                if လုပ်ငန်းစဉ်.poll() is not None:
                    raise AssertionError('QEMU 비정상 ထွက်ပရိုဂရမ်: ' + str(လုပ်ငန်းစဉ်.returncode))
                return အက္ခရာစဉ်.encode('utf-8') in မှတ်တမ်းမှတ်တမ်းတစ်ခု[လုပ်ဆောင်:]

            def အမိန့်များစမ်းသပ်(ဝင်ဒေတာ, မျှော်လင့်ချက်):
                လုပ်ဆောင် = len(မှတ်တမ်းမှတ်တမ်းတစ်ခု)
                အစဉ်ဆက်တန်ဖိုး.sendall(ဝင်ဒေတာ.encode('ascii'))
                စောင့်(lambda: ခေါင်းစီးဖိုင်(မျှော်လင့်ချက်, လုပ်ဆောင်), မျှော်လင့်ချက်)
                စောင့်(lambda: ခေါင်းစီးဖိုင်('jkoros> ', လုပ်ဆောင်), 'အမိန့် 후 프롬프트')

            စောင့်(lambda: ခေါင်းစီးဖိုင်('READY'), အမျိုးအစားတန်ဖိုး + ' စက်တင်')
            assert b'JAVA SELFTEST PASS' in မှတ်တမ်းမှတ်တမ်းတစ်ခု
            assert 'Java 기계어 အူတိုင်တန်ဖိုး လုပ်ဆောင်'.encode() in မှတ်တမ်းမှတ်တမ်းတစ်ခု
            အမိန့်များစမ်းသပ်('info\r\n', 'embedded subset JVM / polling kernel')
            အမိန့်များစမ်းသပ်('help\n', 'free N | echo TEXT')
            အမိန့်များစမ်းသပ်('mem\n', ' / 8 (각 4096바이트)')
            အမိန့်များစမ်းသပ်('echo natix\bve\n', 'native\r\n')
            for နံပါတ် in range(8):
                အမိန့်များစမ်းသပ်('alloc\n', 'ကဏ္ဍတန်ဖိုး နံပါတ်: ' + str(နံပါတ်))
            အမိန့်များစမ်းသပ်('alloc\n', 'ကဏ္ဍတန်ဖိုး နံပါတ်: -1')
            အမိန့်များစမ်းသပ်('free 3\n', '반환됨')
            အမိန့်များစမ်းသပ်('free 3\n', '할당되지 않은 ကဏ္ဍတန်ဖိုး')
            အမိန့်များစမ်းသပ်('free 99\n', '사용법: free 0..7')
            အမိန့်များစမ်းသပ်('alloc\n', 'ကဏ္ဍတန်ဖိုး နံပါတ်: 3')
            အမိန့်များစမ်းသပ်('free 0\n', '반환됨')
            အမိန့်များစမ်းသပ်('test\n', 'JAVA SELFTEST PASS')
            အမိန့်များစမ်းသပ်('unknown\n', '알 ကိန်းတန်ဖိုး 없는 명령입니다')
            အမိန့်များစမ်းသပ်('clear\n', 'jkoros> ')

            # GUI 자판과 동일한 PS/2 장치를 통해 명령을 주입한다.
            လုပ်ဆောင် = len(မှတ်တမ်းမှတ်တမ်းတစ်ခု)
            for သော့တန်ဖိုး in ('i', 'n', 'f', 'o', 'ret'):
                ကြီးကြပ်သူတန်ဖိုး.sendall(('sendkey ' + သော့တန်ဖိုး + ' 30\n').encode())
                time.sleep(0.09)
            စောင့်(lambda: ခေါင်းစီးဖိုင်('embedded subset JVM / polling kernel', လုပ်ဆောင်), 'PS/2 info ဝင်ဒေတာ')
            အမိန့်များစမ်းသပ်('echo ' + 'a' * 150 + '\n', 'a' * 123)
            အစဉ်ဆက်တန်ဖိုး.sendall(b'halt\n')
            စောင့်(lambda: ခေါင်းစီးဖိုင်('HALTED'), 'လုပ်ဆောင်မှုရပ် အမိန့်')
            assert b'PANIC' not in မှတ်တမ်းမှတ်တမ်းတစ်ခု and b'SELFTEST FAIL' not in မှတ်တမ်းမှတ်တမ်းတစ်ခု
            print('PASS: {} စက်တင်, Java ကိုယ်ပိုင် စမ်းသပ်မှု, အစဉ်ဆက်တန်ဖိုး အမိန့်, PS/2 ဝင်ဒေတာ, သိုလှောင်ရာခွဲဝေ/ပြန်ပေးရလဒ်, လုပ်ဆောင်မှုရပ်'.format(အမျိုးအစားတန်ဖိုး))
            return မှတ်တမ်းမှတ်တမ်းတစ်ခု.decode('utf-8', 'replace')
        finally:
            အစဉ်ဆက်တန်ဖိုး.close()
            ကြီးကြပ်သူတန်ဖိုး.close()
            လုပ်ငန်းစဉ်.terminate()
            try:
                လုပ်ငန်းစဉ်.wait(timeout=3)
            except subprocess.TimeoutExpired:
                လုပ်ငန်းစဉ်.kill()
                လုပ်ငန်းစဉ်.wait()


if __name__ == '__main__':
    ရလဒ် = {အမျိုးအစားတန်ဖိုး: စမ်းသပ်မှု(အမျိုးအစားတန်ဖိုး) for အမျိုးအစားတန်ဖိုး in ('elf', 'iso')}
    (နေရာ / 'build/စက်တင်စမ်းသပ်.json').write_text(json.dumps(ရလဒ်, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
