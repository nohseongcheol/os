# Raspberry Pi 4 eigin Java kjarni_VALUE — notandi keyra_skipun 기반

현재 eigin 코드의 COSL 상업 skilyrði, 제3자 고지 및 LGPL 재연결 자료는 [COSL dreifing_VALUE LESTUMIG_eb81d7d9](COSL배포안내.md)를 참고한다. SWITCH_MODE 전 GPL 구성의 판단은 [이전 라이선스 검토](leyfi_umsögn.md)에 기록했다.

Íslenska 통신·undantekning 사용법은 [Íslenska Java API](한국어자바/LESTUMIG_eb81d7d9.md), fall_VALUE·변수·Skrá 이름의 변경과 어원 근거는 [명명 LESTUMIG_eb81d7d9](명명/LESTUMIG_eb81d7d9.md)를 참고한다.

Linux 없이 부팅하는 eigin AArch64 커널이다. Java AOT kjarni_VALUE 위에 **skipanalína skel, 게스트 Java 컴파일러·JVM, MicroPython, EL0 C++ keyra_skipun, Skrá·UDP 루프백 시스템 호출, 여러 한글 GUI Skjáhermir·vi ritill·Swing 부분집합**을 제공한다. 커널의 Skrá gögn/정책·루프백 flytja_VALUE·skel 상태는 Java, 화면 합성·díll breyta_VALUE_16f64fe4·bendill·클리핑도 Java로 구현하며, CPU/MMU/tæki_VALUE 경계와 Skjáhermir·stafur_VALUE 그리기 연결은 C와 어셈블리다.

**전체 JDK/JRE·CPython·표준 C++ 런타임·Swing 이식은 아직 완료되지 않았다.** 기존 [ARM64 Linux 실행판](../rpi4/README.md)의 OpenJDK/Python 패키지를 이 eigin 커널에 탑재했다고 표시하지 않는다.

새로운 게스트 `cc`/`jaot`, JAR 직접 keyra_skipun, lwIP TCP/UDP와 FTP는 [FTP·C·JAR·AOT 매뉴얼](파일전송과번역.md)을 참고한다. 게스트 SSH·VNC와 Pi4 GENET/PHY·DHCP 드라이버를 추가했다. **SSH·VNC는 QEMU에서 검증하며, 실물 Pi4의 vírað_VALUE 송수신은 아직 미검증이다.** keyra_skipun·tenging_e05f319b·aðgangsorð_VALUE 확인은 [외부 tenging_e05f319b LESTUMIG_eb81d7d9](외부접속안내.md)에 정리했다.

셸은 EL1 kjarni_VALUE, `java` 등 notandi keyra_skipun 파일은 EL0에서 실행한다.
`ps`·`top`의 표시와 제한, QEMU 네트워크 keyra_skipun·tenging_e05f319b 방법 및 raun_gögn 검증은
[keyra_skipun 계층과 외부 통신 점검](실행계층과외부통신점검.md)을 참고한다.

ELF는 확장자가 아닌 raun_gögn keyra_skipun 형식으로 검사한다. `./인사`처럼 확장자 없이 실행하며, 제한된 Linux ARM64 fast_VALUE ELF는 `run --linux skrá_heiti_SMS`으로 실행한다. [ELF·Linux ABI Aðstoð_VALUE 범위와 동일 바이너리 시험](실행파일규약.md).

GUI와 네트워크는 `python3 Verkfæri/keyra_skipun.py --desktop --network`로 함께 사용한다. Java·C·Python의 Íslenska 예제 13개는 [jkoros/example](../../example/README.md)에 있으며, **게스트 부팅 시 `/example/java`, `/example/c`, `/example/python`에 자동으로 준비된다.** `example java|c|python`으로 지운 예제를 복원할 númer 있다. Remmina에서 **F9/Shift+Space/한·영 Lykill_VALUE**로 `[EN]`↔`[KO]` 두벌식을 전환한다(`help ko`). `make test-examples`는 같은 GUI VM에서 FTP·raun_gögn TCP/UDP·Skrá bæti_VALUE·그래픽 픽셀을 검증한다.

게스트에서 `cd /example/java` 후 `java Gluggadæmi`로 Íslenska Swing 예제를 실행한다. Skjáhermir 모서리에 마우스를 대고 **왼쪽 버튼으로 끌면 크기가 바뀐다**. `terminal size`는 현재 COLUMN_VALUE·ROW_VALUE 수를 보여 준다.

## 현재 Aðstoð_VALUE miðlaskrá

| 기능 | 구현·시험한 miðlaskrá | 아직 미지원 |
|---|---|---|
| 부팅 | Pi4 AArch64 EL1, UART, SD용 smíð_mynd, QEMU raspi4b 부팅 | raun_gögn Pi4 보드에서의 펌웨어 부팅 시험 |
| Java kjarni_VALUE | fast_VALUE Java 부분집합 → freestanding C → AArch64 AOT | 전체 Java hlutur_VALUE/undantekning/GC/JVM/표준 safn |
| Java 개발 Verkfæri | 게스트 eigin `javac`/`java`, JVM 0.4/JAR: 다중 klasi_VALUE·hlutur_VALUE·상속·undantekning·GC·일부 컬렉션·Thread·IPv4 Socket/UDP·Swing 일부 API, Íslenska safn. 게스트 컴파일러는 fast_VALUE Java 부분집합 | 전체 JDK/JRE·HotSpot·Java SE·임의의 모든 JAR·AWT/Swing 전체 |
| Python | raun_gögn MicroPython 1.24.1 EL0 이식, uppruni_tré þýða_uppruni/keyra_skipun, klasi_VALUE·undantekning·GC·큰 heiltala·Unicode·Skrá·UDP/화면 Tengjast | CPython, pip, C viðbót_VALUE, 부동소수점, 일반 OS/스레드/소켓 eining_VALUE_6d2d8bf4, gagnvirkur REPL |
| skel | UTF-8 breyta_VALUE·LOG_lína·lokið_VALUE, 디렉터리·Skrá Skipun, 변수·skilyrði·forskrift_VALUE, 16 KiB 순차 파이프·리다이렉션, ELF keyra_skipun | 전체 POSIX sh/Bash, 작업 stýring_VALUE·동시 프로세스·PTY |
| C/AOT þýða_uppruni | 게스트 TinyCC 및 fast_VALUE Java 부분집합 `jaot` → eigin ARM64 ELF | 전체 libc·모든 Java klasi_VALUE AOT |
| C++ | 독립 ELF64를 EL0에서 keyra_skipun; fast_VALUE 생성자, RAII 소멸자, FP/SIMD, Íslenska Skrá/루프백 호출 | libc/libstdc++, STL, C++ undantekning·RTTI·동적 Tengjast |
| notandi verja_VALUE | 4 KiB 페이지, CODE_VALUE RX/gögn RW·NX, kjarni_VALUE·MMIO 차단, guard page, 잘못된 bendill 검사 | 다중 notandi leyfi_VALUE, 일반 프로세스/스레드 스케줄러 |
| keyra_skipun TIME_VALUE 제한 | GIC-400 타이머로 무한 ítrekun_VALUE loka_forrit; gagnvirkur 입력 대기는 기한 uppfæra, 터미널별 EL0 forrit_f5044b9b 중단·재개 | 일반적인 선점형 다중작업. 긴 kjarni_VALUE 호출 도중에는 종료가 지연될 númer 있음 |
| Skrá | Java RAM Skrá 64개 × 16384바이트, 루트를 포함한 디렉터리 16개, jafningi_VALUE/절대 SLÓÐ 63바이트, 서술자 16개 | leyfi_VALUE, 디스크/SD 영속 Store_VALUE |
| 네트워크 | lwIP IPv4 TCP/UDP/ARP/ICMP, SLIP, GENET/PHY·DHCP 구현, 게스트 FTP·SSH·VNC | GENET 실물 staðfesta, Wi-Fi, DNS, 일반 TLS 소켓, RDP |
| GUI | 최대 네 Skjáhermir Gluggi, val_VALUE·færa_VALUE·X Loka, 한글 leturgerð_VALUE, Swing 부분집합; 게스트 VNC 화면·입력·두벌식 | 실물 USB 입력, 전체 AWT/Swing·Java2D·Gluggi 관리 정책 |
| 작업 þráður_VALUE | kjarni_VALUE 작업 2개와 주 작업; JVM 내부 þráður_VALUE 최대 4개, start/join/yield·synchronized | pthread, SMP, Java Thread 전체 API |
| 다국어 | UTF-16 리터럴→UTF-8 UART, 한글·일본어·아랍어·이모지, UTF-8 skrá_heiti_SMS/전문 | GUI의 일반 다국어 조판 |

keyra_skipun 버튼 화면은 5×7 영문 글꼴을 쓰며, Skjáhermir 창은 Noto CJK/DejaVu에서 생성한 한글·Unicode 비트맵 글꼴을 쓴다. UART와 raun_gögn 프레임버퍼의 한글 표시를 시험한다. 루프백은 동일 kjarni_VALUE 내부의 전문 전달이며 IP 패킷을 Ethernet으로 내보내는 드라이버가 아니다. 바깥 IPv4는 lwIP TCP/UDP 스택으로 보조 UART SLIP 경로를 사용한다. `python3 Verkfæri/keyra_skipun.py --network`로 QEMU NAT를 연결하고 `ftpd start`로 서비스를 시작한다.

Java의 정확한 API·문법·keyra_skipun 제한과 Íslenska 사용법은 [eigin JVM과 Íslenska safn](자바실행환경.md)에 정리했다. klasi_VALUE Skrá/JAR 배포는 [한국어자바](한국어자바) 소스에서 재현한다. 기존 Linux판 `Íslenska.자바`와 별도인 `Íslenska.eigin` 패키지다.

**vi·여러 Gluggi·Swing·한글 Java/Python/C/C++·posix-kor 예제는 [한글 개발 매뉴얼](개발안내.md)에 정리했다.**

GUI Skjáhermir keyra_skipun·단축키·skel Skipun·제한은 [셸과 Skjáhermir 사용법](skel_AND_Endastöð.md)에 정리했다.

## 현재 컴퓨터에서 keyra_skipun

```sh
cd /home/user/jkoros/platforms/rpi4-native
make test
make run
```

loka_forrit: **Ctrl+A Áfram_vara X**. 게스트 C/AOT Verkfæri 빌드에는 `make rpi-prepare`로 준비한 ARM64 SDK 헤더와 libgcc 산술 보조 함수도 필요하다. libc나 Linux 커널을 게스트에 넣는 것은 아니다. hýsa 도구는 JDK 11 이상, Python 3.6 이상, Clang/Clang++, AArch64 GNU binutils, Make, `libnewlib-dev` 헤더다. MicroPython은 `/usr/include/newlib` 헤더를 사용하며 다른 위치는 `NEWLIB_INCLUDE`로 지정한다. newlib 런타임을 이식·링크한 것은 아니다. 컴파일러 의미 비교에는 GCC/UBSan도 사용한다. 기존 `../rpi4/build/host`의 QEMU 11.0.3이 있으면 이용하며, 그렇지 않으면 PATH의 QEMU를 사용한다. `QEMU_AARCH64=/절대/SLÓÐ/qemu-system-aarch64`로 지정할 수도 있다. `raspi4b` Aðstoð_VALUE 여부를 확인한 후 실행한다.

명령은 **Enter를 눌러 keyra_skipun**한다. 기존 한 stafur_VALUE 명령도 Enter가 필요하다.

```text
javac Hello.java
java Hello "한글 Viðföng 😀"
python hello.py
python -c 'print(2**100)'
ls
cat python.txt
run cpp
net test
gui
```

| Skipun | Aðgerð |
|---|---|
| `help` / `info` | Skipun·raun_gögn 구현 staða_VALUE_e10195a1 |
| `ls` / `cat FILE` / `rm FILE` | RAM Skrá færsla_Listi·Efni_VALUE·삭제 |
| `vi FILE` | notandi 영역 vi 부분집합, 한글 breyta_VALUE·Store_VALUE·검색·되돌리기 |
| `edit FILE` | Skrá 전체를 새로 입력; 단독 `.` 줄로 Store_VALUE, Ctrl-C로 Hætta_við_aðgerð |
| `javac FILE.java` / `java CLASS [ARGS]` | eigin 제한형 Java þýða_uppruni·keyra_skipun |
| `python FILE.py [ARGS]` / `python -c 'CODE'` | MicroPython þýða_uppruni·keyra_skipun |
| `load FILE` / `hex FILE` | 16진수 바이너리 입력/úttak; 입력은 단독 `.` 줄로 Store_VALUE |
| `run FILE.elf [ARGS]` / `run cpp` | 업로드한 eigin ABI ELF / 내장 C++ 예제 |
| `net test` / `tasks` / `selftest` | UDP 루프백 / 협력식 작업 / EL0 verja_VALUE 시험 |
| `gui` / `terminal` | keyra_skipun 화면 / 한글 GUI Skjáhermir; F12로 Skjáhermir Opna·Loka |
| `samples` | 삭제한 sjálfgildi 예제 endurheimta_staða; 기존 파일은 보존 |

예를 들어 `edit 인사.java`를 입력한 Áfram_vara 아래 소스를 입력한다.

```java
public class 인사 { public static void main(String[] args) { int VALUE = 7; System.out.println("한글=" + VALUE); } }
```

그다음 단독 `.` 줄로 저장하고 `javac 인사.java`, `java 인사`를 실행한다. 편집기는 기존 파일에 커서를 이동하는 방식이 아니라 전체 교체 방식이다. Hætta_við_aðgerð·잘못된 16진수·afkastageta_VALUE 초과는 원본을 보존한다. 줄은 4096바이트, 파일은 16384바이트, keyra_skipun 인수는 최대 8개·각각 UTF-8 255바이트다. 일반 Skipun 인수는 최대 32개다. Tilvitnun·백슬래시·skel 변수·파이프·리다이렉션 범위는 [skel 설명](skel_AND_Endastöð.md)을 참고한다.

GUI 터미널은 다음과 같이 실행하고 Remmina에서 **VNC**, slóð **127.0.0.1:5902**로 연결한다. 키보드·한글 Unicode 입력·명시적 líma_VALUE·keyra_skipun 버튼의 마우스 클릭을 QEMU 도구가 UART에 전달한다.

```sh
make desktop
# GUI + 네트워크: python3 Verkfæri/keyra_skipun.py --desktop --network
# 다른 포트: python3 Verkfæri/keyra_skipun.py --desktop --port 5903
```

종료는 실행한 hýsa 터미널에서 Ctrl+C다. 기존 `python3 Verkfæri/keyra_skipun.py --vnc 127.0.0.1:2`는 화면 보기와 별도 UART 입력을 유지한다. `make run`은 일반 UART 셸이다. raun_gögn Pi4 USB 입력기는 아직 없으며, VNC Tengjast 도구는 QEMU 시험용이다.

GUI의 다섯 버튼은 raun_gögn C++/UDP ELF keyra_skipun, `Hello.java` þýða_uppruni 후 JVM keyra_skipun, `hello.py` keyra_skipun, GUI Skjáhermir 열기를 수행한다. 한 번에 한 프로그램이 CPU에서 실행되며 일반 실행에는 약 2초 기한이 있다. vi·Swing은 gagnvirkur 대기에서 기한을 갱신하고 다른 터미널로 전환할 때 Minni_gögn·CPU 문맥을 보관한다. skel·편집기에서 입력을 기다리는 시간에는 이 제한이 적용되지 않는다.

## raun_gögn 산출물과 Pi4 SD smíð_mynd

```sh
make image   # kjarni_VALUE, SD smíð_mynd, 부팅 ZIP, 사용자용 SDK
make sdk     # SDK만 다시 skapa
```

| SLÓÐ | 용도 |
|---|---|
| `build/kernel8.img` | eigin kjarni_VALUE 기계어, 적재 slóð 0x80000 |
| `build/kernel.elf`, `kernel.map` | kjarni_VALUE tákn_VALUE·tengja_útlit |
| `build/user/demo.elf` | notandi MODE_VALUE C++ Skrá/힙/실수/그래픽 예제 |
| `build/user/network.elf` | notandi MODE_VALUE C++ UDP 루프백 예제 |
| `build/user/java-tools.elf` | eigin Java 부분집합 컴파일러/JVM, 전체 JDK/JRE 아님 |
| `dist/jkoros-native-korean.jar` | hýsa javac용 Íslenska API klasi_VALUE; 같은 클래스가 eigin JVM에도 내장됨 |
| `dist/jkoros-native-korean-sources.zip` | Íslenska API Java Uppruni |
| `build/user/vi.elf` | eigin UTF-8 vi Skipun 부분집합 ritill |
| `build/user/python.elf` | eigin ABI용 MicroPython 1.24.1, CPython 아님 |
| `build/user/fault.elf` | 의도적 침범/무한 반복을 수행하는 verja_VALUE 시험 전용 |
| `build/libposix-kor-arm64.a` | **kjarni_VALUE 내부**에서 Java Skrá 구현을 직접 부르는 기존 Tengjast |
| `build/libposix-kor-user.a` | **EL0 notandi forrit_f5044b9b**에서 SVC로 Skrá/루프백을 호출하는 새 Tengjast |
| `dist/jkoros-native-rpi4.img` | 128 MiB MBR/FAT32 SD smíð_mynd |
| `dist/jkoros-native-rpi4-boot.zip` | FAT32 부팅 파티션에 복사할 Skrá Hópur_VALUE |
| `dist/jkoros-native-aarch64-sdk.tar.gz` | 사용자용 헤더·Keyra_2 CODE_VALUE·safn·링커 forskrift_VALUE·예제 |
| `dist/manifest.json`, `build/build.json` | SHA256과 raun_gögn Aðstoð_VALUE staða_VALUE_e10195a1 |

이미지는 확인된 공식 Pi 부팅 묶음에서 `start4.elf`, `fixup4.dat`, Pi4 DTB와 disable-bt overlay를 가져온다. Linux kernel/initramfs/rootfs는 넣지 않는다. 펌웨어·MicroPython·Skjáhermir leturgerð_VALUE 라이선스와 leturgerð_VALUE 출처 해시도 동봉한다. Skrá skapa 스크립트는 물리 디스크에 기록하지 않는다.

예비 microSD에 smíð_mynd LOG_lína 도구로 `.img`를 기록하거나 FAT32 부팅 파티션 최상위에 ZIP 내용을 푼다. smíð_mynd 기록은 선택한 카드의 기존 내용을 지우므로 대상을 확인한다. Pi4 sjálfgildi EEPROM SD 부팅을 전제로 한다. UART는 **3.3V TTL, 115200 8N1**, GPIO14/TXD(8번)→어댑터 RX, GPIO15/RXD(10번)→TX, GND(6번) 연결이다. GPIO에 5V 신호를 연결하지 않는다.

**실물 Pi4 부팅은 미검증이다.** QEMU `-kernel`은 SD의 VideoCore 펌웨어를 실행하지 않고 커널을 직접 적재한다. SD Skrá 구성·kjarni_VALUE 체크섬 검사와 물리 bretti 부팅 검증은 별개다. MMU 사용 전에는 펌웨어의 캐시/MMU가 꺼져 있고 EL1 또는 EL2로 진입하는 통상 부팅 조건을 전제로 한다. 세 보조 코어는 대기시키며 한 코어만 사용한다.

## C++와 Íslenska API 사용

SDK를 풀고 호스트에서 컴파일한다.

```sh
tar -xzf dist/jkoros-native-aarch64-sdk.tar.gz -C build
cd build/jkoros-native-sdk
python3 compile.py examples/Skráardæmi.cpp -o demo.elf
python3 compile.py examples/통신예제.cpp -o network.elf
```

진입점은 `extern "C" int Opna_notandi_forrit(int)`이다. notandi C++는 FP/SIMD를 사용할 númer 있다. kjarni_VALUE C/Java AOT는 일반 레지스터만 사용하므로 undantekning Ferli_VALUE_færsla 중 notandi FP 상태를 건드리지 않는다. notandi færsla_P_VALUE 시 FP 상태를 초기화하고 kjarni_VALUE 복귀에 필요한 상태를 보존한다.

```cpp
#include "파일규약.h"
extern "C" int Opna_notandi_forrit(int) {
    int Skrá = opið_skrá("인사.txt", les_skrifheimild | 없으면만들기 | 내용비우기, 0600);
    if (Skrá < 0) return 1;
    const char Efni_VALUE[] = "안녕하세요";
    int NIÐURSTAÐA = skrifa_skrá_gögn(Skrá, Efni_VALUE, sizeof(Efni_VALUE) - 1);
    loka_skrá(Skrá);
    return NIÐURSTAÐA == sizeof(Efni_VALUE) - 1 ? 0 : 2;
}
```

[Skrá 예제](notandi/Skráardæmi.cpp)와 [통신 예제](notandi/통신예제.cpp)가 raun_gögn 부팅 시험 대상이다. `파일규약.h`의 이름은 커널용/사용자용 모두 같지만 **링크하는 라이브러리가 다르다**. 사용자용은 `svc #0`으로 호출하고 Skrá Ferli_VALUE_færsla 및 루프백 전달은 Java 커널에서 실행한다. `통신규약.h`의 소켓 함수는 현재 사용자용 라이브러리에 구현돼 있다.

새 프로그램은 kjarni_VALUE 재빌드 없이 `load FILE.elf`와 `run FILE.elf`로 실행한다. 호스트에서 Áfram_vara 도구를 사용하면 **새 QEMU를 부팅해 업로드한 raun_gögn 바이트를 재확인한 TIL_BAKA_VALUE 게스트에서 keyra_skipun**하고 종료한다. 이 도구의 새 VM에서 만든 RAM 자료는 종료할 때 사라진다.

```sh
cd /home/user/jkoros/platforms/rpi4-native
python3 Verkfæri/keyra_skrá.py build/jkoros-native-sdk/demo.elf
python3 Verkfæri/keyra_skrá.py 예제/Hello.java "한글 Viðföng"
python3 Verkfæri/keyra_skrá.py 예제/hello.py
```

이 경로는 16KiB 이하의 `.elf`, `.java`, `.class`, `.py`를 지원한다. 큰 내장 Java/MicroPython ELF 자체는 kjarni_VALUE 묶음에 포함되어 이 Skrá 한도를 적용받지 않는다. **C++ 컴파일러는 hýsa SDK의 Clang++**이며 게스트 내부 GCC/Clang 컴파일러는 아직 없다. SDK만으로 일반 Linux 프로그램을 실행할 수는 없다. Linux ELF, 동적 safn, PT_TLS, PT_INTERP, PT_DYNAMIC, keyra_skipun·Skrift 겸용 세그먼트는 로더가 거부한다. 구체적인 호출 INDEX·slóð miðlaskrá·오류는 [notandi ABI](사용자호출규약.md)를 참고한다.

RAM 파일은 재부팅 시 사라진다. `파일저장확정`은 -1과 ENOSYS를 반환한다. 파일의 mode 인수를 저장하지 않으며 leyfi_VALUE·dup/fcntl은 없다. 디렉터리와 jafningi_VALUE/절대 경로는 같은 RAM 저장소에서 처리한다. UDP 전문은 최대 512바이트, 소켓은 8개, 수신 큐는 소켓당 4개다. 수신할 자료가 없거나 큐가 가득 차면 EAGAIN을 반환한다. notandi loka_forrit 시 열린 Skrá 서술자와 소켓을 회수한다.

## staðfesta NIÐURSTAÐA

`make test-jvm`은 9개 프로그램을 OpenJDK와 raun_gögn eigin 커널에서 실행해 결과를 비교한다. `make test`에도 포함된다. 별도 `Verkfæri/부팅시험.py`는 Java 사각형 API의 raun_gögn 화면 픽셀까지 검사한다. `make test-shell`, `make test-desktop`은 새 셸과 raun_gögn VNC 입력·한글 Skjáhermir 화면을 검사하며 `make test`에도 포함된다.

`make test-windows`, `make test-swing`, `make test-stream`, `make test-coding`도 제공하며 `make test`에 포함된다.

`make test`는 OpenJDK와 AOT aðgerð_VALUE NIÐURSTAÐA 비교, 런타임 Villa 중단, 미지원 Java 거부와 함께 별도 QEMU VM에서 다음을 검사한다.

- 기존 Java kjarni_VALUE 계산·UTF-8·C++ 직접 호출·협력식 작업 및 프레임버퍼.
- 손상/잘못된 ABI/slóð 초과/겹친 페이지/W+X 등 ELF hafna_VALUE 사례 22개.
- EL0 C++ 생성자·RAII·실수 aðgerð_VALUE·Skrá·힙 및 잘못된 시스템 호출 bendill.
- kjarni_VALUE/CODE_VALUE/MMIO Skrift·aðgangur_færsla, NX 스택·NULL keyra_skipun, guard page, 특권 Skipun 차단.
- SVC를 호출하지 않는 무한 반복을 타이머로 종료한 후 정상 forrit_f5044b9b 재실행.
- ítrekun_VALUE keyra_skipun 시 Skrá/소켓 누수 방지, UDP 왕복·보낸 slóð·잘린 수신·큐 포화·빈 전문·미지원 통신 Villa.
- skel breyta_VALUE·Hætta_við_aðgerð·16진수 업로드/다운로드·notandi ELF 실행과 잘못된 ELF hafna_VALUE.
- 게스트 Java → OpenJDK `-Xverify:all`, OpenJDK → 게스트 JVM 교차 keyra_skipun, 한글 klasi_VALUE·변수·skrá_heiti_SMS.
- 여러 Gluggi·vi Store_VALUE·breyta_VALUE·skila_brú·notandi staða_VALUE_e10195a1 중단/재개, Swing 한글 입력·이벤트·X Loka, 연결형 루프백, C/C++ 한글 SDK 예제.
- MicroPython Unicode·큰 heiltala·klasi_VALUE·GC ítrekun_VALUE·Skrá import·undantekning·Skrá·UDP 왕복·TIME_VALUE 초과 후 복귀.
- GUI val_VALUE færa_VALUE, C++/UDP/Java/MicroPython 버튼 keyra_skipun, 콘솔 복귀 및 raun_gögn 프레임버퍼 픽셀/leturgerð_VALUE.
- 디렉터리·변수·skilyrði·Skrá Skipun·forskrift_VALUE·순차 파이프·리다이렉션·afkastageta_VALUE 초과 endurheimta_staða, Python stdin/EOF와 Java/Python stdout.
- Skipun LOG_lína·긴 한글 입력 breyta_VALUE·lokið_VALUE·Skjáhermir 스크롤, 그래픽 forrit_f5044b9b loka_forrit 후 Gluggi 복원, raun_gögn VNC Unicode Lykill_VALUE·líma_VALUE·마우스.

[kjarni_VALUE 시험 LOG_lína](build/verification/implementation-test.log), [skel 시험](build/verification/shell/report.json), [VNC 시험](build/verification/desktop/report.json), [vél 판독 NIÐURSTAÐA](build/verification/report.json), [직렬 LOG_VALUE](build/verification/serial.log), [GUI 화면](build/verification/gui-python.png)을 확인할 númer 있다. VNC RFB 3.8 Tengjast 및 640×480 화면 정보도 검사한다. [SDK 재컴파일 NIÐURSTAÐA](build/verification/sdk.json)는 두 예제의 færsla_P·적재 세그먼트·ABI note가 부팅 시험한 ELF와 일치함을 확인한다. tákn_VALUE 등 비적재 메타데이터를 포함한 Skrá 전체의 SHA256까지 같다고 의미하지는 않는다.

## Java와 Python의 정확한 miðlaskrá

eigin `javac`는 버전 49 `.class`를 생성하며 JVM은 Aðstoð_VALUE 명령으로 구성된 버전 45–52 클래스를 실행한다. fast_VALUE fall_VALUE·재귀·int/boolean/char/String·skilyrði/ítrekun_VALUE·strengur_VALUE 결합과 일부 Skrá 스트림을 지원한다. UTF-8 문자열과 문자 리터럴, ASCII 및 현대 한글 음절/samsetning_VALUE 자모 식별자를 처리한다. Unicode auðkenni_VALUE 전체 LOOKUP_tafla·Unicode uppruni_tré 이스케이프는 구현하지 않았다. 게스트 uppruni_tré 컴파일러는 일반 hlutur_VALUE·undantekning·Thread 구문을 아직 컴파일하지 못한다. hýsa `javac --release 8`로 만든 Aðstoð_VALUE 부분집합 클래스는 eigin JVM 0.4의 hlutur_VALUE·undantekning·Thread·UDP와 Íslenska API를 사용할 númer 있다. Swing은 문서화한 eigin API 부분집합을 제공하며 JAR 로더는 제공하지만 전체 AWT/Swing·JDK 표준 라이브러리는 없다. 정확한 범위는 [eigin JVM 설명](자바실행환경.md)이 기준이다. 상세 Tungumál 범위는 [공유 Java Verkfæri 설명](../../문서/자바개발환경.md)을 참고하되, 그 문서의 x86 skel/Store_VALUE/실행시간과 이 ARM64 판의 차이에 유의한다.

MicroPython은 공식 **1.24.1 uppruni_tré**를 eigin AArch64 EL0/SVC 대상으로 빌드했다. Python 문법의 fall_VALUE·klasi_VALUE·undantekning·리스트/orðabók·Unicode·GC·가변 정밀도 정수를 제공한다. 현재 구성은 heiltala 빌드로 `float`, `complex`, `math`가 없으며 CPython 전체 표준 safn, pip, subprocess, threading, 일반 socket과 sjálfgildi `open()` Skrá 객체는 제공하지 않는다. `python FILE.py` 및 `-c` 실행만 제공하며 REPL은 아직 없다. 각 실행의 hlutur_VALUE·모듈은 loka_forrit 시 회수되고 RAM 파일만 Áfram_vara 실행에 남는다.

`import jkoros`로 Áfram_vara 시스템 연결을 쓴다. 모두 SVC를 통해 eigin Java 커널에 접근한다.

| fall_VALUE | Aðgerð |
|---|---|
| `stdin(limit)` | 현재 표준 입력에서 최대 limit바이트(0…16384)를 bytes로 읽음; EOF는 빈 bytes, UART gögn 없음은 OSError(11) |
| `read(name)` | jafningi_VALUE/절대 RAM 경로의 Skrá 전체를 bytes로 읽음 |
| `write(name, data)` | str/bytes 버퍼를 RAM 파일에 새로 Store_VALUE, 쓴 bæti_VALUE númer skila_mæld_stærð |
| `remove(name)` | RAM Skrá 삭제 |
| `rect(x, y, w, h, color)` | 선택한 raun_gögn 화면 Stærð 안의 사각형 teikning_VALUE; 기존 보드의 RGB32 VALUE |
| `ticks_ms()` | 부팅 후 밀리초, 32비트 lota_VALUE |
| `udp_open(port)` | 127.0.0.1의 UDP 소켓 Opna/BIND_endastöð; 0은 자동 포트 |
| `udp_send(fd, port, data)` | 루프백 endastaður_VALUE 포트에 str/bytes 버퍼 flytja_VALUE |
| `udp_recv(fd)` | `(bytes, 보낸포트)` skila_mæld_stærð; 비어 있으면 `OSError(11)` |
| `udp_close(fd)` | 소켓 Loka |

```python
import jkoros
first = jkoros.udp_open(9401)
second = jkoros.udp_open(9402)
jkoros.udp_send(first, 9402, b"hello")
print(jkoros.udp_recv(second))  # (b'hello', 9401)
jkoros.udp_close(first)
jkoros.udp_close(second)
```

이식 CODE_VALUE: [python/](PYTHON_brú/), [notandi Java Tengjast](notandi/자바연결.c). 공식 [MicroPython 이식 LESTUMIG_eb81d7d9](https://docs.micropython.org/en/latest/develop/porting.html)를 참고했다. uppruni_tré URL·tæting_skrá·라이선스는 [vendor LESTUMIG_eb81d7d9](vendor/README.md)에 기록했다.

## 남은 작업

| Áfram_vara stig_VALUE | 완료 verk_rót |
|---|---|
| 영속 Store_VALUE·keyra_skipun Skrá 입력 | SD/MMC 및 디스크 Skrá 시스템, 시스템/notandi 볼륨; 현재 ELF Skrá 실행은 RAM에 한정 |
| 일반 프로세스·스레드 | 프로세스별 slóð 공간, 선점 스케줄러, TLS, samstilla/Bíddu_VALUE, 신호, mmap/mprotect |
| libc와 C++ 런타임 | eigin ABI용 libc, malloc/free, 표준 I_Ú·klukka·환경·locale, libstdc++/undantekning Ferli_VALUE_færsla staðfesta |
| CPython | 해당 libc와 OS API 대상으로 이식·교차 빌드하고 Skrá/Unicode/스레드/소켓 시험 |
| OpenJDK/JRE | HotSpot OS lag_VALUE, GC/JIT/스레드/신호/동적 연결과 Java 네이티브 safn 이식; javac/java raun_gögn keyra_skipun |
| 외부 네트워크 | 추가한 GENET/PHY·DHCP 드라이버의 raun_gögn bretti 송수신 staðfesta, DNS·Wi-Fi |
| GUI viðbót_VALUE | USB HID, 게스트 입력기·문자 조판, Swing Gluggi Stærð 조절·클리핑 viðbót_VALUE, 전체 AWT/Swing 이식 |

이 표는 남은 작업이며 구현 완료 목록이 아니다. QEMU Pi4 모델에는 GENET Ethernet과 PCIe root port가 없어 외부 네트워크 드라이버는 실물 검증도 필요하다. [QEMU tæki_VALUE 지원표](https://www.qemu.org/docs/master/system/arm/raspi.html)

하드웨어 및 ABI 참고: [BCM2711 aukabúnaður](https://datasheets.raspberrypi.com/bcm2711/bcm2711-peripherals.pdf), [Pi4 GIC slóð](https://github.com/raspberrypi/linux/blob/rpi-6.12.y/arch/arm/boot/dts/broadcom/bcm2711.dtsi), [mailbox samningsvirði](https://github.com/raspberrypi/firmware/wiki/Mailbox-property-interface), [Arm ELF64](https://github.com/ARM-software/abi-aa/blob/main/aaelf64/aaelf64.rst), [Arm FP stýring_VALUE 레지스터 Skilgreining_VALUE](https://github.com/ARM-software/arm-trusted-firmware/blob/master/include/arch/aarch64/arch.h).


## Íslenska C gagnagerð·Python Villa·búnt setja_upp_VALUE

C 네트워크 API는 `struct 인터넷통신주소`, enum 상수와 raun_gögn Íslenska 함수로
구현한다. fjölvi_VALUE 별칭을 사용하지 않으며 이전 pk_* ABI도 유지한다.
Python 예제는 `kerfi_villa`, `Villa.INDEX`, `Villa.설명`을 사용한다.

`python3 Verkfæri/keyra_skipun.py --desktop --network --pip`로 시작하면 게스트에서
`pip install micropython-bisect==3.3.3`을 사용할 númer 있다. 현재는 hýsa 중계를
이용하는 제한형 MicroPython uppruni_tré 설치기이며 CPython pip·자동 의존성 해결·C 확장은
미지원이다. 설치한 `/lib` 자료는 RAM이다. [사용법과 제한](PYTHON_búnt.md).

## 화면 Stærð val_VALUE

`python3 Verkfæri/keyra_skipun.py --desktop --network --resolution 1920x1080`으로 Full HD 화면을 사용한다. 기본값은 640×480이며 1280×720도 가능하다. Skjáhermir færa_VALUE, Swing 가운데 tengja_útlit, Java·C·Python 그리기도 raun_gögn 크기를 따른다. SD 영상은 `make image RESOLUTION=1920x1080`으로 만든다. [Stillingar·Íslenska API·staðfesta LESTUMIG_eb81d7d9](화면해상도.md).

## Íslenska 직접 API와 화면 uppfæra

`example/java`는 `실행할일`, `동작받이`, `동작알림`, `hnappur`, `atvik_biðröð`,
`starfskraftur`, `Keyra_2()`을 사용할 númer 있다. Íslenska GUI/가닥을 eigin JVM에 직접
연결했으며, 표준 Swing/Thread를 감싸지 않는다. strengur_VALUE 등 javac의 표준
계약과 전체 uppruni_tré 검토 범위는 [명명 LESTUMIG_eb81d7d9](명명/LESTUMIG_eb81d7d9.md), 사용법과 호환성 변경은
[Íslenska Java API](한국어자바/LESTUMIG_eb81d7d9.md)를 본다.

Skjáhermir færa_VALUE·Stærð 변경은 바뀐 영역만 합성하고 달라진 화소만 표시한다.
[화면 uppfæra 설명](자바실행환경.md#Skjáhermir-부분-uppfæra),
[부분 uppfæra 검사](build/verification/redraw/report.json)를 참고한다.
