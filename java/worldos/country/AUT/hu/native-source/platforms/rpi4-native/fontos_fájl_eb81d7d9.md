# Raspberry Pi 4 saját Java kernel_ÉRTÉK — felhasználó végrehajt_parancs 기반

aktuális_cikk saját 코드의 COSL 상업 állapot, 제3자 고지 및 LGPL 재연결 자료는 [COSL elosztás_ÉRTÉK fontos_fájl_eb81d7d9](COSL배포안내.md)를 참고한다. vált_mód 전 GPL 구성의 판단은 [Előző_cikk 라이선스 검토](licenc_vélemény.md)에 기록했다.

magyar kommunikáció·kivétel 사용법은 [magyar Java API](한국어자바/fontos_fájl_eb81d7d9.md), FÜGGVÉNY_ÉRTÉK·változó_ÉRTÉK·Fájl 이름의 변경과 어원 근거는 [명명 fontos_fájl_eb81d7d9](명명/fontos_fájl_eb81d7d9.md)를 참고한다.

Linux 없이 부팅하는 saját AArch64 커널이다. Java AOT kernel_ÉRTÉK 위에 **parancssor felület, 게스트 Java fordítóprogram·JVM, MicroPython, EL0 C++ végrehajt_parancs, Fájl·UDP 루프백 시스템 호출, 여러 한글 GUI Terminál·vi Írássegéd·Swing 부분집합**을 제공한다. 커널의 Fájl adat/정책·루프백 átvisz_ÉRTÉK·felület 상태는 Java, 화면 합성·képpont módosítás_ÉRTÉK·mutató·클리핑도 Java로 구현하며, CPU/MMU/mobil_ÉRTÉK 경계와 Terminál·karakter_ÉRTÉK 그리기 연결은 C와 어셈블리다.

**전체 JDK/JRE·CPython·표준 C++ 런타임·Swing 이식은 아직 완료되지 않았다.** 기존 [ARM64 Linux 실행판](../rpi4/README.md)의 OpenJDK/Python 패키지를 이 saját 커널에 탑재했다고 표시하지 않는다.

새로운 게스트 `cc`/`jaot`, JAR 직접 végrehajt_parancs, lwIP TCP/UDP와 FTP는 [FTP·C·JAR·AOT 매뉴얼](파일전송과번역.md)을 참고한다. 게스트 SSH·VNC와 Pi4 GENET/PHY·DHCP 드라이버를 추가했다. **SSH·VNC는 QEMU에서 검증하며, 실물 Pi4의 vezetékes_ÉRTÉK 송수신은 아직 미검증이다.** végrehajt_parancs·ismerős_e05f319b·jelszó_ÉRTÉK 확인은 [külső_ÉRTÉK ismerős_e05f319b fontos_fájl_eb81d7d9](külső_ismerős_útmutató.md)에 정리했다.

셸은 EL1 kernel_ÉRTÉK, `java` 등 felhasználó végrehajt_parancs 파일은 EL0에서 실행한다.
`ps`·`top`의 표시와 제한, QEMU 네트워크 végrehajt_parancs·ismerős_e05f319b 방법 및 tényleges_adat 검증은
[végrehajt_parancs 계층과 külső_ÉRTÉK kommunikáció 점검](실행계층과외부통신점검.md)을 참고한다.

ELF는 확장자가 아닌 tényleges_adat végrehajt_parancs 형식으로 검사한다. `./인사`처럼 확장자 없이 실행하며, 제한된 Linux ARM64 statikus_ÉRTÉK ELF는 `run --linux fájlnév_SMS`으로 실행한다. [ELF·Linux ABI támogat_ÉRTÉK 범위와 동일 바이너리 시험](실행파일규약.md).

GUI와 네트워크는 `python3 Eszközök/végrehajt_parancs.py --desktop --network`로 함께 사용한다. Java·C·Python의 magyar 예제 13개는 [jkoros/example](../../example/README.md)에 있으며, **게스트 부팅 시 `/example/java`, `/example/c`, `/example/python`에 자동으로 준비된다.** `example java|c|python`으로 지운 예제를 복원할 szám 있다. Remmina에서 **F9/Shift+Space/한·nulla_operandus Kulcs_ÉRTÉK**로 `[EN]`↔`[KO]` 두벌식을 전환한다(`help ko`). `make test-examples`는 같은 GUI VM에서 FTP·tényleges_adat TCP/UDP·Fájl bájt_ÉRTÉK·그래픽 픽셀을 검증한다.

게스트에서 `cd /example/java` 후 `java AblakPélda`로 magyar Swing 예제를 실행한다. Terminál 모서리에 마우스를 대고 **왼쪽 버튼으로 끌면 크기가 바뀐다**. `terminal size`는 aktuális_cikk OSZLOP_ÉRTÉK·SOR_ÉRTÉK 수를 보여 준다.

## aktuális_cikk támogat_ÉRTÉK klip

| 기능 | 구현·시험한 klip | 아직 미지원 |
|---|---|---|
| 부팅 | Pi4 AArch64 EL1, UART, SD용 épít_KÉP, QEMU raspi4b 부팅 | tényleges_adat Pi4 보드에서의 펌웨어 부팅 시험 |
| Java kernel_ÉRTÉK | statikus_ÉRTÉK Java 부분집합 → freestanding C → AArch64 AOT | 전체 Java objektum_ÉRTÉK/kivétel/GC/JVM/표준 kódtár |
| Java 개발 Eszközök | 게스트 saját `javac`/`java`, JVM 0.4/JAR: 다중 tanóra_ÉRTÉK·objektum_ÉRTÉK·상속·kivétel·GC·일부 컬렉션·Thread·IPv4 Socket/UDP·Swing 일부 API, magyar kódtár. 게스트 컴파일러는 statikus_ÉRTÉK Java 부분집합 | 전체 JDK/JRE·HotSpot·Java SE·임의의 모든 JAR·AWT/Swing 전체 |
| Python | tényleges_adat MicroPython 1.24.1 EL0 이식, forrás_fa épít_forrás/végrehajt_parancs, tanóra_ÉRTÉK·kivétel·GC·큰 egész_szám·Unicode·Fájl·UDP/화면 Kapcsolódás | CPython, pip, C bővítmény_ÉRTÉK, 부동소수점, 일반 OS/스레드/szoftvercsatorna_ÉRTÉK modul_ÉRTÉK, interaktív REPL |
| felület | UTF-8 szerkeszt_ÉRTÉK·LOG_REKORD·Kész_ÉRTÉK, 디렉터리·Fájl Parancs, változó_ÉRTÉK·állapot·parancsfájl_ÉRTÉK, 16 KiB 순차 파이프·리다이렉션, ELF végrehajt_parancs | 전체 POSIX sh/Bash, 작업 vezérlő_ÉRTÉK·동시 프로세스·PTY |
| C/AOT épít_forrás | 게스트 TinyCC 및 statikus_ÉRTÉK Java 부분집합 `jaot` → saját ARM64 ELF | 전체 libc·모든 Java tanóra_ÉRTÉK AOT |
| C++ | 독립 ELF64를 EL0에서 végrehajt_parancs; statikus_ÉRTÉK 생성자, RAII 소멸자, FP/SIMD, magyar Fájl/루프백 호출 | libc/libstdc++, STL, C++ kivétel·RTTI·동적 Kapcsolódás |
| felhasználó véd_ÉRTÉK | 4 KiB 페이지, KÓD_ÉRTÉK RX/adat RW·NX, kernel_ÉRTÉK·MMIO 차단, guard page, 잘못된 mutató 검사 | 다중 felhasználó engedély_ÉRTÉK, 일반 프로세스/스레드 스케줄러 |
| végrehajt_parancs IDŐ_ÉRTÉK 제한 | GIC-400 타이머로 무한 futam_ÉRTÉK kilép_app; interaktív bevitel_ÉRTÉK 대기는 기한 frissít, 터미널별 EL0 app_f5044b9b 중단·CV_végrehajtás | 일반적인 선점형 다중작업. 긴 kernel_ÉRTÉK 호출 도중에는 종료가 지연될 szám 있음 |
| Fájl | Java RAM Fájl 64개 × 16384바이트, 루트를 포함한 디렉터리 16개, társ_ÉRTÉK/절대 ÚTVONAL 63바이트, 서술자 16개 | engedély_ÉRTÉK, 디스크/SD 영속 tár_ÉRTÉK |
| 네트워크 | lwIP IPv4 TCP/UDP/ARP/ICMP, SLIP, GENET/PHY·DHCP 구현, 게스트 FTP·SSH·VNC | GENET 실물 ellenőriz, Wi-Fi, DNS, 일반 TLS szoftvercsatorna_ÉRTÉK, RDP |
| GUI | 최대 네 Terminál Ablak, kijelölés_ÉRTÉK·áthelyez_ÉRTÉK·X Bezárás, 한글 betűkészlet_ÉRTÉK, Swing 부분집합; 게스트 VNC 화면·bevitel_ÉRTÉK·두벌식 | 실물 USB bevitel_ÉRTÉK, 전체 AWT/Swing·Java2D·Ablak 관리 정책 |
| 작업 szál_ÉRTÉK | kernel_ÉRTÉK 작업 2개와 주 작업; JVM 내부 szál_ÉRTÉK 최대 4개, start/join/yield·synchronized | pthread, SMP, Java Thread 전체 API |
| 다국어 | UTF-16 리터럴→UTF-8 UART, 한글·일본어·아랍어·이모지, UTF-8 fájlnév_SMS/datagram | GUI의 일반 다국어 조판 |

végrehajt_parancs 버튼 화면은 5×7 영문 글꼴을 쓰며, Terminál 창은 Noto CJK/DejaVu에서 생성한 한글·Unicode 비트맵 글꼴을 쓴다. UART와 tényleges_adat 프레임버퍼의 한글 표시를 시험한다. 루프백은 동일 kernel_ÉRTÉK 내부의 datagram 전달이며 IP 패킷을 Ethernet으로 내보내는 드라이버가 아니다. 바깥 IPv4는 lwIP TCP/UDP 스택으로 보조 UART SLIP 경로를 사용한다. `python3 Eszközök/végrehajt_parancs.py --network`로 QEMU NAT를 연결하고 `ftpd start`로 서비스를 시작한다.

Java의 정확한 API·문법·végrehajt_parancs 제한과 magyar 사용법은 [saját JVM과 magyar kódtár](자바실행환경.md)에 정리했다. tanóra_ÉRTÉK Fájl/JAR 배포는 [한국어자바](한국어자바) 소스에서 재현한다. 기존 Linux판 `magyar.자바`와 별도인 `magyar.saját` 패키지다.

**vi·여러 Ablak·Swing·한글 Java/Python/C/C++·posix-kor 예제는 [한글 개발 매뉴얼](개발안내.md)에 정리했다.**

GUI Terminál végrehajt_parancs·단축키·felület Parancs·제한은 [셸과 Terminál 사용법](felület_ÉS_Terminál.md)에 정리했다.

## aktuális_cikk 컴퓨터에서 végrehajt_parancs

```sh
cd /home/user/jkoros/platforms/rpi4-native
make test
make run
```

kilép_app: **Ctrl+A Tovább_cikk X**. 게스트 C/AOT Eszközök 빌드에는 `make rpi-prepare`로 준비한 ARM64 SDK 헤더와 libgcc 산술 보조 함수도 필요하다. libc나 Linux 커널을 게스트에 넣는 것은 아니다. gazda 도구는 JDK 11 이상, Python 3.6 이상, Clang/Clang++, AArch64 GNU binutils, Make, `libnewlib-dev` 헤더다. MicroPython은 `/usr/include/newlib` 헤더를 사용하며 다른 위치는 `NEWLIB_INCLUDE`로 지정한다. newlib 런타임을 이식·링크한 것은 아니다. fordítóprogram 의미 비교에는 GCC/UBSan도 사용한다. 기존 `../rpi4/build/host`의 QEMU 11.0.3이 있으면 이용하며, 그렇지 않으면 PATH의 QEMU를 사용한다. `QEMU_AARCH64=/절대/ÚTVONAL/qemu-system-aarch64`로 지정할 수도 있다. `raspi4b` támogat_ÉRTÉK 여부를 확인한 후 실행한다.

명령은 **Enter를 눌러 végrehajt_parancs**한다. 기존 한 karakter_ÉRTÉK 명령도 Enter가 필요하다.

```text
javac Hello.java
java Hello "한글 Argumentumok 😀"
python hello.py
python -c 'print(2**100)'
ls
cat python.txt
run cpp
net test
gui
```

| Parancs | Művelet |
|---|---|
| `help` / `info` | Parancs·tényleges_adat 구현 Állapot_ÉRTÉK |
| `ls` / `cat FILE` / `rm FILE` | RAM Fájl bejegyzés_Lista·Tartalom_ÉRTÉK·삭제 |
| `vi FILE` | felhasználó régió_ÉRTÉK vi 부분집합, 한글 szerkeszt_ÉRTÉK·tár_ÉRTÉK·검색·되돌리기 |
| `edit FILE` | Fájl 전체를 새로 bevitel_ÉRTÉK; 단독 `.` 줄로 tár_ÉRTÉK, Ctrl-C로 Mégse_műtét |
| `javac FILE.java` / `java CLASS [ARGS]` | saját 제한형 Java épít_forrás·végrehajt_parancs |
| `python FILE.py [ARGS]` / `python -c 'CODE'` | MicroPython épít_forrás·végrehajt_parancs |
| `load FILE` / `hex FILE` | 16진수 바이너리 bevitel_ÉRTÉK/Kimenet; 입력은 단독 `.` 줄로 tár_ÉRTÉK |
| `run FILE.elf [ARGS]` / `run cpp` | 업로드한 saját ABI ELF / 내장 C++ 예제 |
| `net test` / `tasks` / `selftest` | UDP 루프백 / 협력식 작업 / EL0 véd_ÉRTÉK 시험 |
| `gui` / `terminal` | végrehajt_parancs 화면 / 한글 GUI Terminál; F12로 Terminál Megnyitás·Bezárás |
| `samples` | 삭제한 alapértelmezett_érték 예제 helyreállít_Állapot; 기존 파일은 보존 |

예를 들어 `edit 인사.java`를 입력한 Tovább_cikk 아래 소스를 입력한다.

```java
public class 인사 { public static void main(String[] args) { int ÉRTÉK = 7; System.out.println("한글=" + ÉRTÉK); } }
```

그다음 단독 `.` 줄로 저장하고 `javac 인사.java`, `java 인사`를 실행한다. 편집기는 기존 파일에 커서를 이동하는 방식이 아니라 전체 교체 방식이다. Mégse_műtét·잘못된 16진수·kapacitás_ÉRTÉK 초과는 원본을 보존한다. 줄은 4096바이트, 파일은 16384바이트, végrehajt_parancs 인수는 최대 8개·각각 UTF-8 255바이트다. 일반 Parancs 인수는 최대 32개다. Idézet·백슬래시·felület változó_ÉRTÉK·파이프·리다이렉션 범위는 [felület 설명](felület_ÉS_Terminál.md)을 참고한다.

GUI 터미널은 다음과 같이 실행하고 Remmina에서 **VNC**, CÍM **127.0.0.1:5902**로 연결한다. 키보드·한글 Unicode bevitel_ÉRTÉK·명시적 beilleszt_ÉRTÉK·végrehajt_parancs 버튼의 마우스 클릭을 QEMU 도구가 UART에 전달한다.

```sh
make desktop
# GUI + 네트워크: python3 Eszközök/végrehajt_parancs.py --desktop --network
# 다른 hardver_port: python3 Eszközök/végrehajt_parancs.py --desktop --port 5903
```

종료는 실행한 gazda 터미널에서 Ctrl+C다. 기존 `python3 Eszközök/végrehajt_parancs.py --vnc 127.0.0.1:2`는 화면 보기와 별도 UART 입력을 유지한다. `make run`은 일반 UART 셸이다. tényleges_adat Pi4 USB 입력기는 아직 없으며, VNC Kapcsolódás 도구는 QEMU 시험용이다.

GUI의 다섯 버튼은 tényleges_adat C++/UDP ELF végrehajt_parancs, `Hello.java` épít_forrás 후 JVM végrehajt_parancs, `hello.py` végrehajt_parancs, GUI Terminál 열기를 수행한다. 한 번에 한 프로그램이 CPU에서 실행되며 일반 실행에는 약 2초 기한이 있다. vi·Swing은 interaktív 대기에서 기한을 갱신하고 다른 터미널로 전환할 때 Memória_adat·CPU 문맥을 보관한다. felület·편집기에서 입력을 기다리는 시간에는 이 제한이 적용되지 않는다.

## tényleges_adat 산출물과 Pi4 SD épít_KÉP

```sh
make image   # kernel_ÉRTÉK, SD épít_KÉP, 부팅 ZIP, 사용자용 SDK
make sdk     # SDK만 újrapróbál_ÉRTÉK generálás
```

| ÚTVONAL | 용도 |
|---|---|
| `build/kernel8.img` | saját kernel_ÉRTÉK 기계어, 적재 CÍM 0x80000 |
| `build/kernel.elf`, `kernel.map` | kernel_ÉRTÉK szimbólum_ÉRTÉK·csatol_Navigáció |
| `build/user/demo.elf` | felhasználó mód_ÉRTÉK C++ Fájl/halommemória_ÉRTÉK/lebegőpontos_szám_ÉRTÉK/그래픽 예제 |
| `build/user/network.elf` | felhasználó mód_ÉRTÉK C++ UDP 루프백 예제 |
| `build/user/java-tools.elf` | saját Java 부분집합 fordítóprogram/JVM, 전체 JDK/JRE 아님 |
| `dist/jkoros-native-korean.jar` | gazda javac용 magyar API tanóra_ÉRTÉK; 같은 클래스가 saját JVM에도 내장됨 |
| `dist/jkoros-native-korean-sources.zip` | magyar API Java FORRÁS |
| `build/user/vi.elf` | saját UTF-8 vi Parancs 부분집합 Írássegéd |
| `build/user/python.elf` | saját ABI용 MicroPython 1.24.1, CPython 아님 |
| `build/user/fault.elf` | 의도적 침범/무한 반복을 수행하는 véd_ÉRTÉK 시험 전용 |
| `build/libposix-kor-arm64.a` | **kernel_ÉRTÉK 내부**에서 Java Fájl 구현을 직접 부르는 기존 Kapcsolódás |
| `build/libposix-kor-user.a` | **EL0 felhasználó app_f5044b9b**에서 SVC로 Fájl/루프백을 호출하는 새 Kapcsolódás |
| `dist/jkoros-native-rpi4.img` | 128 MiB MBR/FAT32 SD épít_KÉP |
| `dist/jkoros-native-rpi4-boot.zip` | FAT32 부팅 파티션에 복사할 Fájl Csoport_ÉRTÉK |
| `dist/jkoros-native-aarch64-sdk.tar.gz` | 사용자용 헤더·Futtatás KÓD_ÉRTÉK·kódtár·링커 parancsfájl_ÉRTÉK·예제 |
| `dist/manifest.json`, `build/build.json` | SHA256과 tényleges_adat támogat_ÉRTÉK Állapot_ÉRTÉK |

이미지는 확인된 공식 Pi 부팅 묶음에서 `start4.elf`, `fixup4.dat`, Pi4 DTB와 disable-bt overlay를 가져온다. Linux kernel/initramfs/rootfs는 넣지 않는다. 펌웨어·MicroPython·Terminál betűkészlet_ÉRTÉK 라이선스와 betűkészlet_ÉRTÉK eredet_ÉRTÉK 해시도 동봉한다. Fájl generálás 스크립트는 물리 디스크에 기록하지 않는다.

예비 microSD에 épít_KÉP LOG_REKORD 도구로 `.img`를 기록하거나 FAT32 부팅 파티션 최상위에 ZIP 내용을 푼다. épít_KÉP 기록은 선택한 카드의 기존 내용을 지우므로 대상을 확인한다. Pi4 alapértelmezett_érték EEPROM SD 부팅을 전제로 한다. UART는 **3.3V TTL, 115200 8N1**, GPIO14/TXD(8번)→어댑터 RX, GPIO15/RXD(10번)→TX, GND(6번) 연결이다. GPIO에 5V 신호를 연결하지 않는다.

**실물 Pi4 부팅은 미검증이다.** QEMU `-kernel`은 SD의 VideoCore 펌웨어를 실행하지 않고 커널을 직접 적재한다. SD Fájl 구성·kernel_ÉRTÉK 체크섬 검사와 물리 fal 부팅 검증은 별개다. MMU használ_ÉRTÉK 전에는 펌웨어의 캐시/MMU가 꺼져 있고 EL1 또는 EL2로 진입하는 통상 부팅 조건을 전제로 한다. 세 보조 코어는 대기시키며 한 코어만 사용한다.

## C++와 magyar API használ_ÉRTÉK

SDK를 풀고 호스트에서 컴파일한다.

```sh
tar -xzf dist/jkoros-native-aarch64-sdk.tar.gz -C build
cd build/jkoros-native-sdk
python3 compile.py examples/FájlPélda.cpp -o demo.elf
python3 compile.py examples/통신예제.cpp -o network.elf
```

진입점은 `extern "C" int START_felhasználó_app(int)`이다. felhasználó C++는 FP/SIMD를 사용할 szám 있다. kernel_ÉRTÉK C/Java AOT는 일반 레지스터만 사용하므로 kivétel folyamat_ÉRTÉK_bejegyzés 중 felhasználó FP 상태를 건드리지 않는다. felhasználó belépési_pont_ÉRTÉK 시 FP 상태를 초기화하고 kernel_ÉRTÉK 복귀에 필요한 상태를 보존한다.

```cpp
#include "파일규약.h"
extern "C" int START_felhasználó_app(int) {
    int Fájl = készít_Fájl("인사.txt", 읽고쓰기 | 없으면만들기 | vág_Tartalom, 0600);
    if (Fájl < 0) return 1;
    const char Tartalom_ÉRTÉK[] = "안녕하세요";
    int KR = ír_Fájl_adat(Fájl, Tartalom_ÉRTÉK, sizeof(Tartalom_ÉRTÉK) - 1);
    bezár_Fájl(Fájl);
    return KR == sizeof(Tartalom_ÉRTÉK) - 1 ? 0 : 2;
}
```

[Fájl 예제](felhasználó/FájlPélda.cpp)와 [kommunikáció 예제](felhasználó/통신예제.cpp)가 tényleges_adat 부팅 시험 대상이다. `파일규약.h`의 이름은 커널용/사용자용 모두 같지만 **링크하는 라이브러리가 다르다**. 사용자용은 `svc #0`으로 호출하고 Fájl folyamat_ÉRTÉK_bejegyzés 및 루프백 전달은 Java 커널에서 실행한다. `통신규약.h`의 szoftvercsatorna_ÉRTÉK 함수는 aktuális_cikk 사용자용 라이브러리에 구현돼 있다.

새 프로그램은 kernel_ÉRTÉK 재빌드 없이 `load FILE.elf`와 `run FILE.elf`로 실행한다. 호스트에서 Tovább_cikk 도구를 사용하면 **새 QEMU를 부팅해 업로드한 tényleges_adat 바이트를 재확인한 BACK_ÉRTÉK 게스트에서 végrehajt_parancs**하고 종료한다. 이 도구의 새 VM에서 만든 RAM 자료는 종료할 때 사라진다.

```sh
cd /home/user/jkoros/platforms/rpi4-native
python3 Eszközök/végrehajt_Fájl.py build/jkoros-native-sdk/demo.elf
python3 Eszközök/végrehajt_Fájl.py 예제/Hello.java "한글 Argumentumok"
python3 Eszközök/végrehajt_Fájl.py 예제/hello.py
```

이 경로는 16KiB 이하의 `.elf`, `.java`, `.class`, `.py`를 지원한다. 큰 내장 Java/MicroPython ELF 자체는 kernel_ÉRTÉK 묶음에 포함되어 이 Fájl 한도를 적용받지 않는다. **C++ 컴파일러는 gazda SDK의 Clang++**이며 게스트 내부 GCC/Clang 컴파일러는 아직 없다. SDK만으로 일반 Linux 프로그램을 실행할 수는 없다. Linux ELF, 동적 kódtár, PT_TLS, PT_INTERP, PT_DYNAMIC, végrehajt_parancs·Írás 겸용 세그먼트는 로더가 거부한다. 구체적인 호출 INDEX·CÍM klip·오류는 [felhasználó ABI](사용자호출규약.md)를 참고한다.

RAM 파일은 재부팅 시 사라진다. `véglegesít_Files`은 -1과 ENOSYS를 반환한다. 파일의 mode 인수를 저장하지 않으며 engedély_ÉRTÉK·dup/fcntl은 없다. 디렉터리와 társ_ÉRTÉK/절대 경로는 같은 RAM 저장소에서 처리한다. UDP 전문은 최대 512바이트, 소켓은 8개, fogad_ÉRTÉK 큐는 소켓당 4개다. 수신할 자료가 없거나 큐가 가득 차면 EAGAIN을 반환한다. felhasználó kilép_app 시 열린 Fájl 서술자와 소켓을 회수한다.

## ellenőriz KR

`make test-jvm`은 9개 프로그램을 OpenJDK와 tényleges_adat saját 커널에서 실행해 결과를 비교한다. `make test`에도 포함된다. 별도 `Eszközök/부팅시험.py`는 Java téglalap API의 tényleges_adat 화면 픽셀까지 검사한다. `make test-shell`, `make test-desktop`은 새 셸과 tényleges_adat VNC bevitel_ÉRTÉK·한글 Terminál 화면을 검사하며 `make test`에도 포함된다.

`make test-windows`, `make test-swing`, `make test-stream`, `make test-coding`도 제공하며 `make test`에 포함된다.

`make test`는 OpenJDK와 AOT műtét_ÉRTÉK KR 비교, 런타임 HIBA 중단, 미지원 Java 거부와 함께 별도 QEMU VM에서 다음을 검사한다.

- 기존 Java kernel_ÉRTÉK 계산·UTF-8·C++ 직접 호출·협력식 작업 및 프레임버퍼.
- 손상/잘못된 ABI/CÍM 초과/겹친 페이지/W+X 등 ELF elutasít_ÉRTÉK 사례 22개.
- EL0 C++ 생성자·RAII·lebegőpontos_szám_ÉRTÉK műtét_ÉRTÉK·Fájl·halommemória_ÉRTÉK 및 잘못된 시스템 호출 mutató.
- kernel_ÉRTÉK/KÓD_ÉRTÉK/MMIO Írás·hozzáfér_bejegyzés, NX operandus_Sor·NULL végrehajt_parancs, guard page, 특권 Parancs 차단.
- SVC를 호출하지 않는 무한 반복을 타이머로 종료한 후 informatikai_részleg_normál app_f5044b9b 재실행.
- futam_ÉRTÉK végrehajt_parancs 시 Fájl/szoftvercsatorna_ÉRTÉK 누수 방지, UDP 왕복·보낸 CÍM·잘린 fogad_ÉRTÉK·큐 포화·빈 datagram·미지원 kommunikáció HIBA.
- felület szerkeszt_ÉRTÉK·Mégse_műtét·16진수 업로드/다운로드·felhasználó ELF 실행과 잘못된 ELF elutasít_ÉRTÉK.
- 게스트 Java → OpenJDK `-Xverify:all`, OpenJDK → 게스트 JVM 교차 végrehajt_parancs, 한글 tanóra_ÉRTÉK·változó_ÉRTÉK·fájlnév_SMS.
- 여러 Ablak·vi tár_ÉRTÉK·szerkeszt_ÉRTÉK·visszaküld_híd·felhasználó Állapot_ÉRTÉK 중단/CV_végrehajtás, Swing 한글 bevitel_ÉRTÉK·이벤트·X Bezárás, 연결형 루프백, C/C++ 한글 SDK 예제.
- MicroPython Unicode·큰 egész_szám·tanóra_ÉRTÉK·GC futam_ÉRTÉK·Fájl import·kivétel·Fájl·UDP 왕복·IDŐ_ÉRTÉK 초과 후 복귀.
- GUI kijelölés_ÉRTÉK áthelyez_ÉRTÉK, C++/UDP/Java/MicroPython 버튼 végrehajt_parancs, 콘솔 복귀 및 tényleges_adat 프레임버퍼 픽셀/betűkészlet_ÉRTÉK.
- 디렉터리·változó_ÉRTÉK·állapot·Fájl Parancs·parancsfájl_ÉRTÉK·순차 파이프·리다이렉션·kapacitás_ÉRTÉK 초과 helyreállít_Állapot, Python stdin/EOF와 Java/Python stdout.
- Parancs LOG_REKORD·긴 한글 bevitel_ÉRTÉK szerkeszt_ÉRTÉK·Kész_ÉRTÉK·Terminál 스크롤, 그래픽 app_f5044b9b kilép_app 후 Ablak 복원, tényleges_adat VNC Unicode Kulcs_ÉRTÉK·beilleszt_ÉRTÉK·마우스.

[kernel_ÉRTÉK 시험 LOG_REKORD](build/verification/implementation-test.log), [felület 시험](build/verification/shell/report.json), [VNC 시험](build/verification/desktop/report.json), [gép 판독 KR](build/verification/report.json), [직렬 LOG_ÉRTÉK](build/verification/serial.log), [GUI 화면](build/verification/gui-python.png)을 확인할 szám 있다. VNC RFB 3.8 Kapcsolódás 및 640×480 화면 정보도 검사한다. [SDK 재컴파일 KR](build/verification/sdk.json)는 두 예제의 belépési_pont·적재 세그먼트·ABI note가 부팅 시험한 ELF와 일치함을 확인한다. szimbólum_ÉRTÉK 등 비적재 메타데이터를 포함한 Fájl 전체의 SHA256까지 같다고 의미하지는 않는다.

## Java와 Python의 정확한 klip

saját `javac`는 버전 49 `.class`를 생성하며 JVM은 támogat_ÉRTÉK 명령으로 구성된 버전 45–52 클래스를 실행한다. statikus_ÉRTÉK FÜGGVÉNY_ÉRTÉK·재귀·int/boolean/char/String·állapot/futam_ÉRTÉK·sztring_ÉRTÉK 결합과 일부 Fájl 스트림을 지원한다. UTF-8 문자열과 문자 리터럴, ASCII 및 현대 한글 음절/rész_egész_ÉRTÉK 자모 식별자를 처리한다. Unicode azonosító_ÉRTÉK 전체 keresőtáblázat·Unicode forrás_fa 이스케이프는 구현하지 않았다. 게스트 forrás_fa 컴파일러는 일반 objektum_ÉRTÉK·kivétel·Thread 구문을 아직 컴파일하지 못한다. gazda `javac --release 8`로 만든 támogat_ÉRTÉK 부분집합 클래스는 saját JVM 0.4의 objektum_ÉRTÉK·kivétel·Thread·UDP와 magyar API를 사용할 szám 있다. Swing은 문서화한 saját API 부분집합을 제공하며 JAR 로더는 제공하지만 전체 AWT/Swing·JDK 표준 라이브러리는 없다. 정확한 범위는 [saját JVM 설명](자바실행환경.md)이 기준이다. 상세 Nyelv 범위는 [공유 Java Eszközök 설명](../../문서/Java_IDE.md)을 참고하되, 그 문서의 x86 felület/tár_ÉRTÉK/실행시간과 이 ARM64 판의 차이에 유의한다.

MicroPython은 공식 **1.24.1 forrás_fa**를 saját AArch64 EL0/SVC 대상으로 빌드했다. Python 문법의 FÜGGVÉNY_ÉRTÉK·tanóra_ÉRTÉK·kivétel·리스트/szótár·Unicode·GC·가변 pontosság_ÉRTÉK 정수를 제공한다. aktuális_cikk 구성은 egész_szám 빌드로 `float`, `complex`, `math`가 없으며 CPython 전체 표준 kódtár, pip, subprocess, threading, 일반 socket과 alapértelmezett_érték `open()` Fájl 객체는 제공하지 않는다. `python FILE.py` 및 `-c` 실행만 제공하며 REPL은 아직 없다. 각 실행의 objektum_ÉRTÉK·모듈은 kilép_app 시 회수되고 RAM 파일만 Tovább_cikk 실행에 남는다.

`import jkoros`로 Tovább_cikk 시스템 연결을 쓴다. 모두 SVC를 통해 saját Java 커널에 접근한다.

| FÜGGVÉNY_ÉRTÉK | Művelet |
|---|---|
| `stdin(limit)` | aktuális_cikk 표준 입력에서 최대 limit바이트(0…16384)를 bytes로 읽음; EOF는 빈 bytes, UART adat 없음은 OSError(11) |
| `read(name)` | társ_ÉRTÉK/절대 RAM 경로의 Fájl 전체를 bytes로 읽음 |
| `write(name, data)` | str/bytes 버퍼를 RAM 파일에 새로 tár_ÉRTÉK, 쓴 bájt_ÉRTÉK szám visszaküld_KR |
| `remove(name)` | RAM Fájl 삭제 |
| `rect(x, y, w, h, color)` | 선택한 tényleges_adat 화면 Méret 안의 téglalap rajz_ÉRTÉK; 기존 보드의 RGB32 ÉRTÉK |
| `ticks_ms()` | 부팅 후 밀리초, 32비트 Ciklus_ÉRTÉK |
| `udp_open(port)` | 127.0.0.1의 UDP szoftvercsatorna_ÉRTÉK Megnyitás/BIND_végpont; 0은 자동 hardver_port |
| `udp_send(fd, port, data)` | 루프백 cél_ÉRTÉK 포트에 str/bytes 버퍼 átvisz_ÉRTÉK |
| `udp_recv(fd)` | `(bytes, 보낸포트)` visszaküld_KR; 비어 있으면 `OSError(11)` |
| `udp_close(fd)` | szoftvercsatorna_ÉRTÉK Bezárás |

```python
import jkoros
first = jkoros.udp_open(9401)
second = jkoros.udp_open(9402)
jkoros.udp_send(first, 9402, b"hello")
print(jkoros.udp_recv(second))  # (b'hello', 9401)
jkoros.udp_close(first)
jkoros.udp_close(second)
```

이식 KÓD_ÉRTÉK: [python/](PYTHON_híd/), [felhasználó Java Kapcsolódás](felhasználó/자바연결.c). 공식 [MicroPython 이식 fontos_fájl_eb81d7d9](https://docs.micropython.org/en/latest/develop/porting.html)를 참고했다. forrás_fa URL·kivonat_Fájl·라이선스는 [vendor fontos_fájl_eb81d7d9](vendor/README.md)에 기록했다.

## 남은 작업

| Tovább_cikk fázis_ÉRTÉK | 완료 teendő_gyök |
|---|---|
| 영속 tár_ÉRTÉK·végrehajt_parancs Fájl bevitel_ÉRTÉK | SD/MMC 및 디스크 Fájl 시스템, 시스템/felhasználó 볼륨; aktuális_cikk ELF Fájl 실행은 RAM에 한정 |
| 일반 프로세스·스레드 | 프로세스별 CÍM CÍM_régió, 선점 스케줄러, TLS, szinkronizál/várj_ÉRTÉK, 신호, mmap/mprotect |
| libc와 C++ 런타임 | saját ABI용 libc, malloc/free, 표준 I_O·Óra·környezet_5d36e09c·locale, libstdc++/kivétel folyamat_ÉRTÉK_bejegyzés ellenőriz |
| CPython | 해당 libc와 OS API 대상으로 이식·교차 빌드하고 Fájl/Unicode/스레드/szoftvercsatorna_ÉRTÉK 시험 |
| OpenJDK/JRE | HotSpot OS réteg_ÉRTÉK, GC/JIT/스레드/신호/동적 연결과 Java 네이티브 kódtár 이식; javac/java tényleges_adat végrehajt_parancs |
| külső_ÉRTÉK 네트워크 | 추가한 GENET/PHY·DHCP 드라이버의 tényleges_adat fal 송수신 ellenőriz, DNS·Wi-Fi |
| GUI bővítmény_ÉRTÉK | USB HID, 게스트 입력기·문자 조판, Swing Ablak Méret 조절·클리핑 bővítmény_ÉRTÉK, 전체 AWT/Swing 이식 |

이 표는 남은 작업이며 구현 완료 목록이 아니다. QEMU Pi4 모델에는 GENET Ethernet과 PCIe root port가 없어 külső_ÉRTÉK 네트워크 드라이버는 실물 검증도 필요하다. [QEMU mobil_ÉRTÉK 지원표](https://www.qemu.org/docs/master/system/arm/raspi.html)

hardver_ÉRTÉK 및 ABI 참고: [BCM2711 tartozék](https://datasheets.raspberrypi.com/bcm2711/bcm2711-peripherals.pdf), [Pi4 GIC CÍM](https://github.com/raspberrypi/linux/blob/rpi-6.12.y/arch/arm/boot/dts/broadcom/bcm2711.dtsi), [mailbox szerződés_értéke](https://github.com/raspberrypi/firmware/wiki/Mailbox-property-interface), [Arm ELF64](https://github.com/ARM-software/abi-aa/blob/main/aaelf64/aaelf64.rst), [Arm FP vezérlő_ÉRTÉK 레지스터 Definíció_ÉRTÉK](https://github.com/ARM-software/arm-trusted-firmware/blob/master/include/arch/aarch64/arch.h).


## magyar C adattípus·Python HIBA·köteg telepít_ÉRTÉK

C 네트워크 API는 `struct háló_szoftvercsatorna_CÍM`, enum 상수와 tényleges_adat magyar 함수로
구현한다. makró_ÉRTÉK 별칭을 사용하지 않으며 Előző_cikk pk_* ABI도 유지한다.
Python 예제는 `rendszerhiba`, `HIBA.INDEX`, `HIBA.설명`을 사용한다.

`python3 Eszközök/végrehajt_parancs.py --desktop --network --pip`로 시작하면 게스트에서
`pip install micropython-bisect==3.3.3`을 사용할 szám 있다. 현재는 gazda 중계를
이용하는 제한형 MicroPython forrás_fa 설치기이며 CPython pip·자동 의존성 해결·C 확장은
미지원이다. 설치한 `/lib` 자료는 RAM이다. [사용법과 제한](PYTHON_köteg.md).

## 화면 Méret kijelölés_ÉRTÉK

`python3 Eszközök/végrehajt_parancs.py --desktop --network --resolution 1920x1080`으로 Full HD 화면을 사용한다. 기본값은 640×480이며 1280×720도 가능하다. Terminál áthelyez_ÉRTÉK, Swing 가운데 csatol_Navigáció, Java·C·Python 그리기도 tényleges_adat 크기를 따른다. SD 영상은 `make image RESOLUTION=1920x1080`으로 만든다. [Beállítások·magyar API·ellenőriz fontos_fájl_eb81d7d9](képernyőfelbontás.md).

## magyar 직접 API와 화면 frissít

`example/java`는 `실행할일`, `동작받이`, `Action_alapelv`, `gomb`, `esemény_várólista`,
`dolgozó`, `Futtatás()`을 사용할 szám 있다. magyar GUI/가닥을 saját JVM에 직접
연결했으며, 표준 Swing/Thread를 감싸지 않는다. sztring_ÉRTÉK 등 javac의 표준
계약과 전체 forrás_fa 검토 범위는 [명명 fontos_fájl_eb81d7d9](명명/fontos_fájl_eb81d7d9.md), 사용법과 호환성 변경은
[magyar Java API](한국어자바/fontos_fájl_eb81d7d9.md)를 본다.

Terminál áthelyez_ÉRTÉK·Méret 변경은 바뀐 영역만 합성하고 달라진 화소만 표시한다.
[화면 frissít 설명](자바실행환경.md#Terminál-부분-frissít),
[부분 frissít 검사](build/verification/redraw/report.json)를 참고한다.
