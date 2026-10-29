# Raspberry Pi 4 자체 Java xoox_xëyma — kiy_jariñoo_internet def_ndigel 기반

현재 자체 코드의 COSL 상업 anam, 제3자 고지 및 LGPL 재연결 자료는 [COSL 배포 JANG_MA_eb81d7d9](COSL배포안내.md)를 참고한다. jalantu_anam 전 GPL 구성의 판단은 [이전 라이선스 검토](sañ_sañ_jàngat.md)에 기록했다.

한국어 통신·예외 사용법은 [한국어 Java API](한국어자바/JANG_MA_eb81d7d9.md), liëey_xëyma·변수·bara_denc 이름의 변경과 어원 근거는 [명명 JANG_MA_eb81d7d9](명명/JANG_MA_eb81d7d9.md)를 참고한다.

Linux 없이 부팅하는 자체 AArch64 커널이다. Java AOT xoox_xëyma 위에 **Tegtalu_ndigel Wëreef, 게스트 Java 컴파일러·JVM, MicroPython, EL0 C++ def_ndigel, bara_denc·UDP 루프백 시스템 호출, 여러 한글 GUI 터미널·vi defarkat·Swing 부분집합**을 제공한다. 커널의 bara_denc mbir/정책·루프백 toxal_xëyma_630ba093·Wëreef 상태는 Java, 화면 합성·piksel soppi_xëyma_16f64fe4·joxañukaay·클리핑도 Java로 구현하며, CPU/MMU/toftal_xëyma 경계와 터미널·Araf_xëyma 그리기 연결은 C와 어셈블리다.

**전체 JDK/JRE·CPython·표준 C++ 런타임·Swing 이식은 아직 완료되지 않았다.** 기존 [ARM64 Linux 실행판](../rpi4/README.md)의 OpenJDK/Python 패키지를 이 자체 커널에 탑재했다고 표시하지 않는다.

새로운 게스트 `cc`/`jaot`, JAR 직접 def_ndigel, lwIP TCP/UDP와 FTP는 [FTP·C·JAR·AOT 매뉴얼](파일전송과번역.md)을 참고한다. 게스트 SSH·VNC와 Pi4 GENET/PHY·DHCP 드라이버를 추가했다. **SSH·VNC는 QEMU에서 검증하며, 실물 Pi4의 tënku_xëyma 송수신은 아직 미검증이다.** def_ndigel·jokkalóo_e05f319b·pasu_dugg_xëyma 확인은 [외부 jokkalóo_e05f319b JANG_MA_eb81d7d9](외부접속안내.md)에 정리했다.

셸은 EL1 xoox_xëyma, `java` 등 kiy_jariñoo_internet def_ndigel 파일은 EL0에서 실행한다.
`ps`·`top`의 표시와 제한, QEMU 네트워크 def_ndigel·jokkalóo_e05f319b 방법 및 liteew_mbir 검증은
[def_ndigel 계층과 외부 통신 점검](실행계층과외부통신점검.md)을 참고한다.

ELF는 확장자가 아닌 liteew_mbir def_ndigel 형식으로 검사한다. `./인사`처럼 확장자 없이 실행하며, 제한된 Linux ARM64 Soppeekoodi_xëyma ELF는 `run --linux bara_denc_tur_SMS`으로 실행한다. [ELF·Linux ABI Ndimbal_xëyma 범위와 동일 바이너리 시험](실행파일규약.md).

GUI와 네트워크는 `python3 Jumtukaay_yi/def_ndigel.py --desktop --network`로 함께 사용한다. Java·C·Python의 한국어 예제 13개는 [jkoros/example](../../example/README.md)에 있으며, **게스트 부팅 시 `/example/java`, `/example/c`, `/example/python`에 자동으로 준비된다.** `example java|c|python`으로 지운 예제를 복원할 수 있다. Remmina에서 **F9/Shift+Space/한·영 kër_xëyma**로 `[EN]`↔`[KO]` 두벌식을 전환한다(`help ko`). `make test-examples`는 같은 GUI VM에서 FTP·liteew_mbir TCP/UDP·bara_denc okte_xëyma·그래픽 픽셀을 검증한다.

게스트에서 `cd /example/java` 후 `java 창예제`로 한국어 Swing 예제를 실행한다. 터미널 모서리에 마우스를 대고 **왼쪽 버튼으로 끌면 크기가 바뀐다**. `terminal size`는 현재 Jen_xëyma·Dënk_xëyma 수를 보여 준다.

## 현재 Ndimbal_xëyma kilip

| 기능 | 구현·시험한 kilip | 아직 미지원 |
|---|---|---|
| 부팅 | Pi4 AArch64 EL1, UART, SD용 tabax_nataal, QEMU raspi4b 부팅 | liteew_mbir Pi4 보드에서의 펌웨어 부팅 시험 |
| Java xoox_xëyma | Soppeekoodi_xëyma Java 부분집합 → freestanding C → AArch64 AOT | 전체 Java yëf_xëyma/예외/GC/JVM/표준 daaray_téere |
| Java 개발 Jumtukaay_yi | 게스트 자체 `javac`/`java`, JVM 0.4/JAR: 다중 maas_xëyma·yëf_xëyma·상속·예외·GC·일부 컬렉션·Thread·IPv4 Socket/UDP·Swing 일부 API, 한국어 daaray_téere. 게스트 컴파일러는 Soppeekoodi_xëyma Java 부분집합 | 전체 JDK/JRE·HotSpot·Java SE·임의의 모든 JAR·AWT/Swing 전체 |
| Python | liteew_mbir MicroPython 1.24.1 EL0 이식, Cosaan_tëralinuy_pàcc tabax_Cosaan/def_ndigel, maas_xëyma·예외·GC·큰 lëmm·Unicode·bara_denc·UDP/화면 JOKKOO | CPython, pip, C ñàmbaas_xëyma, 부동소수점, 일반 OS/스레드/소켓 모듈, duglante REPL |
| Wëreef | UTF-8 soppi_xëyma·làq_Dënk·완성, 디렉터리·bara_denc ndigel, 변수·anam·ndigali_doxalin_xëyma, 16 KiB 순차 파이프·리다이렉션, ELF def_ndigel | 전체 POSIX sh/Bash, 작업 Saytu_doxinu_ordinateur_xëyma·동시 프로세스·PTY |
| C/AOT tabax_Cosaan | 게스트 TinyCC 및 Soppeekoodi_xëyma Java 부분집합 `jaot` → 자체 ARM64 ELF | 전체 libc·모든 Java maas_xëyma AOT |
| C++ | 독립 ELF64를 EL0에서 def_ndigel; Soppeekoodi_xëyma 생성자, RAII 소멸자, FP/SIMD, 한국어 bara_denc/루프백 호출 | libc/libstdc++, STL, C++ 예외·RTTI·동적 JOKKOO |
| kiy_jariñoo_internet saama_xëyma | 4 KiB 페이지, 코드 RX/mbir RW·NX, xoox_xëyma·MMIO 차단, guard page, 잘못된 joxañukaay 검사 | 다중 kiy_jariñoo_internet sañ_sañ_xëyma, 일반 프로세스/스레드 스케줄러 |
| def_ndigel 시간 제한 | GIC-400 타이머로 무한 baamtu_xëyma Génn_jëfekaay; duglante 입력 대기는 기한 Yeesal, 터미널별 EL0 jëfekaay_f5044b9b 중단·재개 | 일반적인 선점형 다중작업. 긴 xoox_xëyma 호출 도중에는 종료가 지연될 수 있음 |
| bara_denc | Java RAM bara_denc 64개 × 16384바이트, 루트를 포함한 디렉터리 16개, Nàttangoo_xëyma/절대 Yoonu_jëmale 63바이트, 서술자 16개 | sañ_sañ_xëyma, 디스크/SD 영속 Store_xëyma |
| 네트워크 | lwIP IPv4 TCP/UDP/ARP/ICMP, SLIP, GENET/PHY·DHCP 구현, 게스트 FTP·SSH·VNC | GENET 실물 wéral, Wi-Fi, DNS, 일반 TLS 소켓, RDP |
| GUI | 최대 네 터미널 palanteer, tanneef_xëyma·toxal_xëyma·X Tej, 한글 mbindin_xëyma, Swing 부분집합; 게스트 VNC 화면·입력·두벌식 | 실물 USB 입력, 전체 AWT/Swing·Java2D·palanteer 관리 정책 |
| 작업 buumug_jokkale_xëyma | xoox_xëyma 작업 2개와 주 작업; JVM 내부 buumug_jokkale_xëyma 최대 4개, start/join/yield·synchronized | pthread, SMP, Java Thread 전체 API |
| 다국어 | UTF-16 리터럴→UTF-8 UART, 한글·일본어·아랍어·이모지, UTF-8 bara_denc_tur_SMS/전문 | GUI의 일반 다국어 조판 |

def_ndigel 버튼 화면은 5×7 영문 글꼴을 쓰며, 터미널 창은 Noto CJK/DejaVu에서 생성한 한글·Unicode 비트맵 글꼴을 쓴다. UART와 liteew_mbir 프레임버퍼의 한글 표시를 시험한다. 루프백은 동일 xoox_xëyma 내부의 전문 전달이며 IP 패킷을 Ethernet으로 내보내는 드라이버가 아니다. 바깥 IPv4는 lwIP TCP/UDP 스택으로 보조 UART SLIP 경로를 사용한다. `python3 Jumtukaay_yi/def_ndigel.py --network`로 QEMU NAT를 연결하고 `ftpd start`로 서비스를 시작한다.

Java의 정확한 API·문법·def_ndigel 제한과 한국어 사용법은 [자체 JVM과 한국어 daaray_téere](자바실행환경.md)에 정리했다. maas_xëyma bara_denc/JAR 배포는 [한국어자바](한국어자바) 소스에서 재현한다. 기존 Linux판 `한국어.자바`와 별도인 `한국어.자체` 패키지다.

**vi·여러 palanteer·Swing·한글 Java/Python/C/C++·posix-kor 예제는 [한글 개발 매뉴얼](개발안내.md)에 정리했다.**

GUI 터미널 def_ndigel·단축키·Wëreef ndigel·제한은 [셸과 터미널 사용법](셸과터미널.md)에 정리했다.

## 현재 컴퓨터에서 def_ndigel

```sh
cd /home/user/jkoros/platforms/rpi4-native
make test
make run
```

Génn_jëfekaay: **Ctrl+A 다음 X**. 게스트 C/AOT Jumtukaay_yi 빌드에는 `make rpi-prepare`로 준비한 ARM64 SDK 헤더와 libgcc 산술 보조 함수도 필요하다. libc나 Linux 커널을 게스트에 넣는 것은 아니다. dalal 도구는 JDK 11 이상, Python 3.6 이상, Clang/Clang++, AArch64 GNU binutils, Make, `libnewlib-dev` 헤더다. MicroPython은 `/usr/include/newlib` 헤더를 사용하며 다른 위치는 `NEWLIB_INCLUDE`로 지정한다. newlib 런타임을 이식·링크한 것은 아니다. 컴파일러 의미 비교에는 GCC/UBSan도 사용한다. 기존 `../rpi4/build/host`의 QEMU 11.0.3이 있으면 이용하며, 그렇지 않으면 PATH의 QEMU를 사용한다. `QEMU_AARCH64=/절대/Yoonu_jëmale/qemu-system-aarch64`로 지정할 수도 있다. `raspi4b` Ndimbal_xëyma 여부를 확인한 후 실행한다.

명령은 **Enter를 눌러 def_ndigel**한다. 기존 한 Araf_xëyma 명령도 Enter가 필요하다.

```text
javac Hello.java
java Hello "한글 인수 😀"
python hello.py
python -c 'print(2**100)'
ls
cat python.txt
run cpp
net test
gui
```

| ndigel | jëf |
|---|---|
| `help` / `info` | ndigel·liteew_mbir 구현 nekkin_xëyma |
| `ls` / `cat FILE` / `rm FILE` | RAM bara_denc dugal_xabaar_lim·Këmb_xëyma·삭제 |
| `vi FILE` | kiy_jariñoo_internet 영역 vi 부분집합, 한글 soppi_xëyma·Store_xëyma·검색·되돌리기 |
| `edit FILE` | bara_denc 전체를 새로 입력; 단독 `.` 줄로 Store_xëyma, Ctrl-C로 Bayyi_sëfu_xayma |
| `javac FILE.java` / `java CLASS [ARGS]` | 자체 제한형 Java tabax_Cosaan·def_ndigel |
| `python FILE.py [ARGS]` / `python -c 'CODE'` | MicroPython tabax_Cosaan·def_ndigel |
| `load FILE` / `hex FILE` | 16진수 바이너리 입력/출력; 입력은 단독 `.` 줄로 Store_xëyma |
| `run FILE.elf [ARGS]` / `run cpp` | 업로드한 자체 ABI ELF / 내장 C++ 예제 |
| `net test` / `tasks` / `selftest` | UDP 루프백 / 협력식 작업 / EL0 saama_xëyma 시험 |
| `gui` / `terminal` | def_ndigel 화면 / 한글 GUI 터미널; F12로 터미널 sos·Tej |
| `samples` | 삭제한 xayma_bi_teew 예제 defaru_nekkin; 기존 파일은 보존 |

예를 들어 `edit 인사.java`를 입력한 다음 아래 소스를 입력한다.

```java
public class 인사 { public static void main(String[] args) { int xëyma = 7; System.out.println("한글=" + xëyma); } }
```

그다음 단독 `.` 줄로 저장하고 `javac 인사.java`, `java 인사`를 실행한다. 편집기는 기존 파일에 커서를 이동하는 방식이 아니라 전체 교체 방식이다. Bayyi_sëfu_xayma·잘못된 16진수·용량 초과는 원본을 보존한다. 줄은 4096바이트, 파일은 16384바이트, def_ndigel 인수는 최대 8개·각각 UTF-8 255바이트다. 일반 ndigel 인수는 최대 32개다. 따옴표·백슬래시·Wëreef 변수·파이프·리다이렉션 범위는 [Wëreef 설명](셸과터미널.md)을 참고한다.

GUI 터미널은 다음과 같이 실행하고 Remmina에서 **VNC**, dëkkuwaay **127.0.0.1:5902**로 연결한다. 키보드·한글 Unicode 입력·명시적 Taf_xëyma·def_ndigel 버튼의 마우스 클릭을 QEMU 도구가 UART에 전달한다.

```sh
make desktop
# GUI + 네트워크: python3 Jumtukaay_yi/def_ndigel.py --desktop --network
# 다른 jumtukaay_jël: python3 Jumtukaay_yi/def_ndigel.py --desktop --port 5903
```

종료는 실행한 dalal 터미널에서 Ctrl+C다. 기존 `python3 Jumtukaay_yi/def_ndigel.py --vnc 127.0.0.1:2`는 화면 보기와 별도 UART 입력을 유지한다. `make run`은 일반 UART 셸이다. liteew_mbir Pi4 USB 입력기는 아직 없으며, VNC JOKKOO 도구는 QEMU 시험용이다.

GUI의 다섯 버튼은 liteew_mbir C++/UDP ELF def_ndigel, `Hello.java` tabax_Cosaan 후 JVM def_ndigel, `hello.py` def_ndigel, GUI 터미널 열기를 수행한다. 한 번에 한 프로그램이 CPU에서 실행되며 일반 실행에는 약 2초 기한이 있다. vi·Swing은 duglante 대기에서 기한을 갱신하고 다른 터미널로 전환할 때 fatlekookaay_mbir·CPU 문맥을 보관한다. Wëreef·편집기에서 입력을 기다리는 시간에는 이 제한이 적용되지 않는다.

## liteew_mbir 산출물과 Pi4 SD tabax_nataal

```sh
make image   # xoox_xëyma, SD tabax_nataal, 부팅 ZIP, 사용자용 SDK
make sdk     # SDK만 다시 생성
```

| Yoonu_jëmale | 용도 |
|---|---|
| `build/kernel8.img` | 자체 xoox_xëyma 기계어, 적재 dëkkuwaay 0x80000 |
| `build/kernel.elf`, `kernel.map` | xoox_xëyma sembóol_xëyma·lëkkale_Tëralin |
| `build/user/demo.elf` | kiy_jariñoo_internet anam_xëyma C++ bara_denc/힙/실수/그래픽 예제 |
| `build/user/network.elf` | kiy_jariñoo_internet anam_xëyma C++ UDP 루프백 예제 |
| `build/user/java-tools.elf` | 자체 Java 부분집합 컴파일러/JVM, 전체 JDK/JRE 아님 |
| `dist/jkoros-native-korean.jar` | dalal javac용 한국어 API maas_xëyma; 같은 클래스가 자체 JVM에도 내장됨 |
| `dist/jkoros-native-korean-sources.zip` | 한국어 API Java Cosaan |
| `build/user/vi.elf` | 자체 UTF-8 vi ndigel 부분집합 defarkat |
| `build/user/python.elf` | 자체 ABI용 MicroPython 1.24.1, CPython 아님 |
| `build/user/fault.elf` | 의도적 침범/무한 반복을 수행하는 saama_xëyma 시험 전용 |
| `build/libposix-kor-arm64.a` | **xoox_xëyma 내부**에서 Java bara_denc 구현을 직접 부르는 기존 JOKKOO |
| `build/libposix-kor-user.a` | **EL0 kiy_jariñoo_internet jëfekaay_f5044b9b**에서 SVC로 bara_denc/루프백을 호출하는 새 JOKKOO |
| `dist/jkoros-native-rpi4.img` | 128 MiB MBR/FAT32 SD tabax_nataal |
| `dist/jkoros-native-rpi4-boot.zip` | FAT32 부팅 파티션에 복사할 bara_denc mboolo_xëyma |
| `dist/jkoros-native-aarch64-sdk.tar.gz` | 사용자용 헤더·daw 코드·daaray_téere·링커 ndigali_doxalin_xëyma·예제 |
| `dist/manifest.json`, `build/build.json` | SHA256과 liteew_mbir Ndimbal_xëyma nekkin_xëyma |

이미지는 확인된 공식 Pi 부팅 묶음에서 `start4.elf`, `fixup4.dat`, Pi4 DTB와 disable-bt overlay를 가져온다. Linux kernel/initramfs/rootfs는 넣지 않는다. 펌웨어·MicroPython·터미널 mbindin_xëyma 라이선스와 mbindin_xëyma 출처 해시도 동봉한다. bara_denc 생성 스크립트는 물리 디스크에 기록하지 않는다.

예비 microSD에 tabax_nataal làq_Dënk 도구로 `.img`를 기록하거나 FAT32 부팅 파티션 최상위에 ZIP 내용을 푼다. tabax_nataal 기록은 선택한 카드의 기존 내용을 지우므로 대상을 확인한다. Pi4 xayma_bi_teew EEPROM SD 부팅을 전제로 한다. UART는 **3.3V TTL, 115200 8N1**, GPIO14/TXD(8번)→어댑터 RX, GPIO15/RXD(10번)→TX, GND(6번) 연결이다. GPIO에 5V 신호를 연결하지 않는다.

**실물 Pi4 부팅은 미검증이다.** QEMU `-kernel`은 SD의 VideoCore 펌웨어를 실행하지 않고 커널을 직접 적재한다. SD bara_denc 구성·xoox_xëyma 체크섬 검사와 물리 보드 부팅 검증은 별개다. MMU 사용 전에는 펌웨어의 캐시/MMU가 꺼져 있고 EL1 또는 EL2로 진입하는 통상 부팅 조건을 전제로 한다. 세 보조 코어는 대기시키며 한 코어만 사용한다.

## C++와 한국어 API 사용

SDK를 풀고 호스트에서 컴파일한다.

```sh
tar -xzf dist/jkoros-native-aarch64-sdk.tar.gz -C build
cd build/jkoros-native-sdk
python3 compile.py examples/파일예제.cpp -o demo.elf
python3 compile.py examples/통신예제.cpp -o network.elf
```

진입점은 `extern "C" int Door_kiy_jariñoo_internet_jëfekaay(int)`이다. kiy_jariñoo_internet C++는 FP/SIMD를 사용할 수 있다. xoox_xëyma C/Java AOT는 일반 레지스터만 사용하므로 예외 yokkute_xëyma_dugal_xabaar 중 kiy_jariñoo_internet FP 상태를 건드리지 않는다. kiy_jariñoo_internet dugal_xabaar_Tomb_xëyma 시 FP 상태를 초기화하고 xoox_xëyma 복귀에 필요한 상태를 보존한다.

```cpp
#include "파일규약.h"
extern "C" int Door_kiy_jariñoo_internet_jëfekaay(int) {
    int bara_denc = sos_bara_denc("인사.txt", jàng_bind | 없으면만들기 | 내용비우기, 0600);
    if (bara_denc < 0) return 1;
    const char Këmb_xëyma[] = "안녕하세요";
    int 결과 = biir_bara_denc_mbir(bara_denc, Këmb_xëyma, sizeof(Këmb_xëyma) - 1);
    Tej_bara_denc(bara_denc);
    return 결과 == sizeof(Këmb_xëyma) - 1 ? 0 : 2;
}
```

[bara_denc 예제](kiy_jariñoo_internet/파일예제.cpp)와 [통신 예제](kiy_jariñoo_internet/통신예제.cpp)가 liteew_mbir 부팅 시험 대상이다. `파일규약.h`의 이름은 커널용/사용자용 모두 같지만 **링크하는 라이브러리가 다르다**. 사용자용은 `svc #0`으로 호출하고 bara_denc yokkute_xëyma_dugal_xabaar 및 루프백 전달은 Java 커널에서 실행한다. `통신규약.h`의 소켓 함수는 현재 사용자용 라이브러리에 구현돼 있다.

새 프로그램은 xoox_xëyma 재빌드 없이 `load FILE.elf`와 `run FILE.elf`로 실행한다. 호스트에서 다음 도구를 사용하면 **새 QEMU를 부팅해 업로드한 liteew_mbir 바이트를 재확인한 woñeeku_xëyma 게스트에서 def_ndigel**하고 종료한다. 이 도구의 새 VM에서 만든 RAM 자료는 종료할 때 사라진다.

```sh
cd /home/user/jkoros/platforms/rpi4-native
python3 Jumtukaay_yi/def_bara_denc.py build/jkoros-native-sdk/demo.elf
python3 Jumtukaay_yi/def_bara_denc.py 예제/Hello.java "한글 인수"
python3 Jumtukaay_yi/def_bara_denc.py 예제/hello.py
```

이 경로는 16KiB 이하의 `.elf`, `.java`, `.class`, `.py`를 지원한다. 큰 내장 Java/MicroPython ELF 자체는 xoox_xëyma 묶음에 포함되어 이 bara_denc 한도를 적용받지 않는다. **C++ 컴파일러는 dalal SDK의 Clang++**이며 게스트 내부 GCC/Clang 컴파일러는 아직 없다. SDK만으로 일반 Linux 프로그램을 실행할 수는 없다. Linux ELF, 동적 daaray_téere, PT_TLS, PT_INTERP, PT_DYNAMIC, def_ndigel·biir 겸용 세그먼트는 로더가 거부한다. 구체적인 호출 àlluwa_tur·dëkkuwaay kilip·오류는 [kiy_jariñoo_internet ABI](사용자호출규약.md)를 참고한다.

RAM 파일은 재부팅 시 사라진다. `파일저장확정`은 -1과 ENOSYS를 반환한다. 파일의 mode 인수를 저장하지 않으며 sañ_sañ_xëyma·dup/fcntl은 없다. 디렉터리와 Nàttangoo_xëyma/절대 경로는 같은 RAM 저장소에서 처리한다. UDP 전문은 최대 512바이트, 소켓은 8개, 수신 큐는 소켓당 4개다. 수신할 자료가 없거나 큐가 가득 차면 EAGAIN을 반환한다. kiy_jariñoo_internet Génn_jëfekaay 시 열린 bara_denc 서술자와 소켓을 회수한다.

## wéral 결과

`make test-jvm`은 9개 프로그램을 OpenJDK와 liteew_mbir 자체 커널에서 실행해 결과를 비교한다. `make test`에도 포함된다. 별도 `Jumtukaay_yi/부팅시험.py`는 Java 사각형 API의 liteew_mbir 화면 픽셀까지 검사한다. `make test-shell`, `make test-desktop`은 새 셸과 liteew_mbir VNC 입력·한글 터미널 화면을 검사하며 `make test`에도 포함된다.

`make test-windows`, `make test-swing`, `make test-stream`, `make test-coding`도 제공하며 `make test`에 포함된다.

`make test`는 OpenJDK와 AOT sëfu_xayma_xëyma 결과 비교, 런타임 njumte 중단, 미지원 Java 거부와 함께 별도 QEMU VM에서 다음을 검사한다.

- 기존 Java xoox_xëyma 계산·UTF-8·C++ 직접 호출·협력식 작업 및 프레임버퍼.
- 손상/잘못된 ABI/dëkkuwaay 초과/겹친 페이지/W+X 등 ELF 거부 사례 22개.
- EL0 C++ 생성자·RAII·실수 sëfu_xayma_xëyma·bara_denc·힙 및 잘못된 시스템 호출 joxañukaay.
- xoox_xëyma/코드/MMIO biir·jot_dugal_xabaar, NX 스택·NULL def_ndigel, guard page, 특권 ndigel 차단.
- SVC를 호출하지 않는 무한 반복을 타이머로 종료한 후 정상 jëfekaay_f5044b9b 재실행.
- baamtu_xëyma def_ndigel 시 bara_denc/소켓 누수 방지, UDP 왕복·보낸 dëkkuwaay·잘린 수신·큐 포화·빈 전문·미지원 통신 njumte.
- Wëreef soppi_xëyma·Bayyi_sëfu_xayma·16진수 업로드/다운로드·kiy_jariñoo_internet ELF 실행과 잘못된 ELF 거부.
- 게스트 Java → OpenJDK `-Xverify:all`, OpenJDK → 게스트 JVM 교차 def_ndigel, 한글 maas_xëyma·변수·bara_denc_tur_SMS.
- 여러 palanteer·vi Store_xëyma·soppi_xëyma·되돌림·kiy_jariñoo_internet nekkin_xëyma 중단/재개, Swing 한글 입력·이벤트·X Tej, 연결형 루프백, C/C++ 한글 SDK 예제.
- MicroPython Unicode·큰 lëmm·maas_xëyma·GC baamtu_xëyma·bara_denc import·예외·bara_denc·UDP 왕복·시간 초과 후 복귀.
- GUI tanneef_xëyma toxal_xëyma, C++/UDP/Java/MicroPython 버튼 def_ndigel, 콘솔 복귀 및 liteew_mbir 프레임버퍼 픽셀/mbindin_xëyma.
- 디렉터리·변수·anam·bara_denc ndigel·ndigali_doxalin_xëyma·순차 파이프·리다이렉션·용량 초과 defaru_nekkin, Python stdin/EOF와 Java/Python stdout.
- ndigel làq_Dënk·긴 한글 입력 soppi_xëyma·완성·터미널 스크롤, 그래픽 jëfekaay_f5044b9b Génn_jëfekaay 후 palanteer 복원, liteew_mbir VNC Unicode kër_xëyma·Taf_xëyma·마우스.

[xoox_xëyma 시험 làq_Dënk](build/verification/implementation-test.log), [Wëreef 시험](build/verification/shell/report.json), [VNC 시험](build/verification/desktop/report.json), [masin 판독 결과](build/verification/report.json), [직렬 làq_xëyma](build/verification/serial.log), [GUI 화면](build/verification/gui-python.png)을 확인할 수 있다. VNC RFB 3.8 JOKKOO 및 640×480 화면 정보도 검사한다. [SDK 재컴파일 결과](build/verification/sdk.json)는 두 예제의 dugal_xabaar_Tomb·적재 세그먼트·ABI note가 부팅 시험한 ELF와 일치함을 확인한다. sembóol_xëyma 등 비적재 메타데이터를 포함한 bara_denc 전체의 SHA256까지 같다고 의미하지는 않는다.

## Java와 Python의 정확한 kilip

자체 `javac`는 버전 49 `.class`를 생성하며 JVM은 Ndimbal_xëyma 명령으로 구성된 버전 45–52 클래스를 실행한다. Soppeekoodi_xëyma liëey_xëyma·재귀·int/boolean/char/String·anam/baamtu_xëyma·araf_yu_bennoo_xëyma 결합과 일부 bara_denc 스트림을 지원한다. UTF-8 문자열과 문자 리터럴, ASCII 및 현대 한글 음절/조합 자모 식별자를 처리한다. Unicode raññeekaay_xëyma 전체 표·Unicode Cosaan_tëralinuy_pàcc 이스케이프는 구현하지 않았다. 게스트 Cosaan_tëralinuy_pàcc 컴파일러는 일반 yëf_xëyma·예외·Thread 구문을 아직 컴파일하지 못한다. dalal `javac --release 8`로 만든 Ndimbal_xëyma 부분집합 클래스는 자체 JVM 0.4의 yëf_xëyma·예외·Thread·UDP와 한국어 API를 사용할 수 있다. Swing은 문서화한 자체 API 부분집합을 제공하며 JAR 로더는 제공하지만 전체 AWT/Swing·JDK 표준 라이브러리는 없다. 정확한 범위는 [자체 JVM 설명](자바실행환경.md)이 기준이다. 상세 Làkk 범위는 [공유 Java Jumtukaay_yi 설명](../../문서/자바개발환경.md)을 참고하되, 그 문서의 x86 Wëreef/Store_xëyma/실행시간과 이 ARM64 판의 차이에 유의한다.

MicroPython은 공식 **1.24.1 Cosaan_tëralinuy_pàcc**를 자체 AArch64 EL0/SVC 대상으로 빌드했다. Python 문법의 liëey_xëyma·maas_xëyma·예외·리스트/téereb_Tekki_baat·Unicode·GC·가변 정밀도 정수를 제공한다. 현재 구성은 lëmm 빌드로 `float`, `complex`, `math`가 없으며 CPython 전체 표준 daaray_téere, pip, subprocess, threading, 일반 socket과 xayma_bi_teew `open()` bara_denc 객체는 제공하지 않는다. `python FILE.py` 및 `-c` 실행만 제공하며 REPL은 아직 없다. 각 실행의 yëf_xëyma·모듈은 Génn_jëfekaay 시 회수되고 RAM 파일만 다음 실행에 남는다.

`import jkoros`로 다음 시스템 연결을 쓴다. 모두 SVC를 통해 자체 Java 커널에 접근한다.

| liëey_xëyma | jëf |
|---|---|
| `stdin(limit)` | 현재 표준 입력에서 최대 limit바이트(0…16384)를 bytes로 읽음; EOF는 빈 bytes, UART mbir 없음은 OSError(11) |
| `read(name)` | Nàttangoo_xëyma/절대 RAM 경로의 bara_denc 전체를 bytes로 읽음 |
| `write(name, data)` | str/bytes 버퍼를 RAM 파일에 새로 Store_xëyma, 쓴 okte_xëyma 수 반환 |
| `remove(name)` | RAM bara_denc 삭제 |
| `rect(x, y, w, h, color)` | 선택한 liteew_mbir 화면 tolluwaay 안의 사각형 deseñ_xëyma; 기존 보드의 RGB32 xëyma |
| `ticks_ms()` | 부팅 후 밀리초, 32비트 Wërngal_xëyma |
| `udp_open(port)` | 127.0.0.1의 UDP 소켓 sos/묶기; 0은 자동 jumtukaay_jël |
| `udp_send(fd, port, data)` | 루프백 jëmmukaay_xëyma 포트에 str/bytes 버퍼 toxal_xëyma_630ba093 |
| `udp_recv(fd)` | `(bytes, 보낸포트)` 반환; 비어 있으면 `OSError(11)` |
| `udp_close(fd)` | 소켓 Tej |

```python
import jkoros
first = jkoros.udp_open(9401)
second = jkoros.udp_open(9402)
jkoros.udp_send(first, 9402, b"hello")
print(jkoros.udp_recv(second))  # (b'hello', 9401)
jkoros.udp_close(first)
jkoros.udp_close(second)
```

이식 코드: [python/](파이썬연결/), [kiy_jariñoo_internet Java JOKKOO](kiy_jariñoo_internet/자바연결.c). 공식 [MicroPython 이식 JANG_MA_eb81d7d9](https://docs.micropython.org/en/latest/develop/porting.html)를 참고했다. Cosaan_tëralinuy_pàcc URL·caabiy_teqale_bi_bara_denc·라이선스는 [vendor JANG_MA_eb81d7d9](vendor/README.md)에 기록했다.

## 남은 작업

| 다음 pàcc_xëyma | 완료 기준 |
|---|---|
| 영속 Store_xëyma·def_ndigel bara_denc 입력 | SD/MMC 및 디스크 bara_denc 시스템, 시스템/kiy_jariñoo_internet 볼륨; 현재 ELF bara_denc 실행은 RAM에 한정 |
| 일반 프로세스·스레드 | 프로세스별 dëkkuwaay 공간, 선점 스케줄러, TLS, lëkkale/대기, 신호, mmap/mprotect |
| libc와 C++ 런타임 | 자체 ABI용 libc, malloc/free, 표준 D_G·Yeetekaay_ak_Montar·환경·locale, libstdc++/예외 yokkute_xëyma_dugal_xabaar wéral |
| CPython | 해당 libc와 OS API 대상으로 이식·교차 빌드하고 bara_denc/Unicode/스레드/소켓 시험 |
| OpenJDK/JRE | HotSpot OS déggoob_wet_xëyma, GC/JIT/스레드/신호/동적 연결과 Java 네이티브 daaray_téere 이식; javac/java liteew_mbir def_ndigel |
| 외부 네트워크 | 추가한 GENET/PHY·DHCP 드라이버의 liteew_mbir 보드 송수신 wéral, DNS·Wi-Fi |
| GUI ñàmbaas_xëyma | USB HID, 게스트 입력기·문자 조판, Swing palanteer tolluwaay 조절·클리핑 ñàmbaas_xëyma, 전체 AWT/Swing 이식 |

이 표는 남은 작업이며 구현 완료 목록이 아니다. QEMU Pi4 모델에는 GENET Ethernet과 PCIe root port가 없어 외부 네트워크 드라이버는 실물 검증도 필요하다. [QEMU toftal_xëyma 지원표](https://www.qemu.org/docs/master/system/arm/raspi.html)

jumtukaay_xëyma 및 ABI 참고: [BCM2711 toftal](https://datasheets.raspberrypi.com/bcm2711/bcm2711-peripherals.pdf), [Pi4 GIC dëkkuwaay](https://github.com/raspberrypi/linux/blob/rpi-6.12.y/arch/arm/boot/dts/broadcom/bcm2711.dtsi), [mailbox ay_xëyma](https://github.com/raspberrypi/firmware/wiki/Mailbox-property-interface), [Arm ELF64](https://github.com/ARM-software/abi-aa/blob/main/aaelf64/aaelf64.rst), [Arm FP Saytu_doxinu_ordinateur_xëyma 레지스터 Tekki_baat_xëyma](https://github.com/ARM-software/arm-trusted-firmware/blob/master/include/arch/aarch64/arch.h).


## 한국어 C xéeti_mbir·Python njumte·takku_xéewël samp_xëyma

C 네트워크 API는 `struct 인터넷통신주소`, enum 상수와 liteew_mbir 한국어 함수로
구현한다. gaawtal_xëyma 별칭을 사용하지 않으며 이전 pk_* ABI도 유지한다.
Python 예제는 `kureel_njumte`, `njumte.àlluwa_tur`, `njumte.설명`을 사용한다.

`python3 Jumtukaay_yi/def_ndigel.py --desktop --network --pip`로 시작하면 게스트에서
`pip install micropython-bisect==3.3.3`을 사용할 수 있다. 현재는 dalal 중계를
이용하는 제한형 MicroPython Cosaan_tëralinuy_pàcc 설치기이며 CPython pip·자동 의존성 해결·C 확장은
미지원이다. 설치한 `/lib` 자료는 RAM이다. [사용법과 제한](파이썬꾸러미.md).

## 화면 tolluwaay tanneef_xëyma

`python3 Jumtukaay_yi/def_ndigel.py --desktop --network --resolution 1920x1080`으로 Full HD 화면을 사용한다. 기본값은 640×480이며 1280×720도 가능하다. 터미널 toxal_xëyma, Swing 가운데 lëkkale_Tëralin, Java·C·Python 그리기도 liteew_mbir 크기를 따른다. SD 영상은 `make image RESOLUTION=1920x1080`으로 만든다. [Jekkal_yi·한국어 API·wéral JANG_MA_eb81d7d9](화면해상도.md).

## 한국어 직접 API와 화면 Yeesal

`example/java`는 `실행할일`, `동작받이`, `동작알림`, `butoñ`, `xewxew_Topplante_xaarandi`,
`작업가닥`, `daw()`을 사용할 수 있다. 한국어 GUI/가닥을 자체 JVM에 직접
연결했으며, 표준 Swing/Thread를 감싸지 않는다. araf_yu_bennoo_xëyma 등 javac의 표준
계약과 전체 Cosaan_tëralinuy_pàcc 검토 범위는 [명명 JANG_MA_eb81d7d9](명명/JANG_MA_eb81d7d9.md), 사용법과 호환성 변경은
[한국어 Java API](한국어자바/JANG_MA_eb81d7d9.md)를 본다.

터미널 toxal_xëyma·tolluwaay 변경은 바뀐 영역만 합성하고 달라진 화소만 표시한다.
[화면 Yeesal 설명](자바실행환경.md#터미널-부분-Yeesal),
[부분 Yeesal 검사](build/verification/redraw/report.json)를 참고한다.
