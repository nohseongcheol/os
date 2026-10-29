# Raspberry Pi 4 eget Java kerne_VÆRDI — bruger Udfør_kommando 기반

aktuel_vare eget 코드의 COSL 상업 lidelse, 제3자 고지 및 LGPL 재연결 자료는 [COSL distribution_VÆRDI Vigtigt_eb81d7d9](COSL배포안내.md)를 참고한다. SKIFT_HYPPIGST 전 GPL 구성의 판단은 [Forrige_vare 라이선스 검토](licens_gennemse.md)에 기록했다.

Dansk 통신·undtagelse 사용법은 [Dansk Java API](한국어자바/Vigtigt_eb81d7d9.md), FUNKTION_VÆRDI·variabel_VÆRDI·Fil 이름의 변경과 어원 근거는 [명명 Vigtigt_eb81d7d9](명명/Vigtigt_eb81d7d9.md)를 참고한다.

Linux 없이 부팅하는 eget AArch64 커널이다. Java AOT kerne_VÆRDI 위에 **kommandolinje Shell, 게스트 Java compiler·JVM, MicroPython, EL0 C++ Udfør_kommando, Fil·UDP 루프백 시스템 호출, 여러 한글 GUI Terminal·vi Editor·Swing 부분집합**을 제공한다. 커널의 Fil data/정책·루프백 overføre_VÆRDI·Shell 상태는 Java, skærmbillede 합성·pixel ændre_VÆRDI·markør·클리핑도 Java로 구현하며, CPU/MMU/enhed_VÆRDI 경계와 Terminal·tegn_VÆRDI Paint_skærmbillede 연결은 C와 어셈블리다.

**전체 JDK/JRE·CPython·표준 C++ 런타임·Swing 이식은 아직 완료되지 않았다.** 기존 [ARM64 Linux 실행판](../rpi4/README.md)의 OpenJDK/Python 패키지를 이 eget 커널에 탑재했다고 표시하지 않는다.

새로운 게스트 `cc`/`jaot`, JAR 직접 Udfør_kommando, lwIP TCP/UDP와 FTP는 [FTP·C·JAR·AOT 매뉴얼](파일전송과번역.md)을 참고한다. 게스트 SSH·VNC와 Pi4 GENET/PHY·DHCP 드라이버를 추가했다. **SSH·VNC는 QEMU에서 검증하며, 실물 Pi4의 traditionel_VÆRDI 송수신은 아직 미검증이다.** Udfør_kommando·forbindelse_e05f319b·adgangskode_VÆRDI 확인은 [ekstern_VÆRDI forbindelse_e05f319b Vigtigt_eb81d7d9](ekstern_forbindelse_guide.md)에 정리했다.

셸은 EL1 kerne_VÆRDI, `java` 등 bruger Udfør_kommando 파일은 EL0에서 실행한다.
`ps`·`top`의 표시와 제한, QEMU 네트워크 Udfør_kommando·forbindelse_e05f319b 방법 및 faktisk_data 검증은
[Udfør_kommando 계층과 ekstern_VÆRDI 통신 점검](실행계층과외부통신점검.md)을 참고한다.

ELF는 확장자가 아닌 faktisk_data Udfør_kommando 형식으로 검사한다. `./인사`처럼 확장자 없이 실행하며, 제한된 Linux ARM64 statisk_VÆRDI ELF는 `run --linux filnavn_sms`으로 실행한다. [ELF·Linux ABI støtte_VÆRDI 범위와 동일 바이너리 시험](실행파일규약.md).

GUI와 네트워크는 `python3 Værktøjer/Udfør_kommando.py --desktop --network`로 함께 사용한다. Java·C·Python의 Dansk 예제 13개는 [jkoros/example](../../example/README.md)에 있으며, **게스트 부팅 시 `/example/java`, `/example/c`, `/example/python`에 자동으로 준비된다.** `example java|c|python`으로 지운 예제를 복원할 tal 있다. Remmina에서 **F9/Shift+Space/한·nul_operand tast_VÆRDI**로 `[EN]`↔`[KO]` 두벌식을 전환한다(`help ko`). `make test-examples`는 같은 GUI VM에서 FTP·faktisk_data TCP/UDP·Fil byte_VÆRDI·그래픽 픽셀을 검증한다.

게스트에서 `cd /example/java` 후 `java Vindueseksempel`로 Dansk Swing 예제를 실행한다. Terminal 모서리에 마우스를 대고 **왼쪽 버튼으로 끌면 크기가 바뀐다**. `terminal size`는 aktuel_vare KOLONNE_VÆRDI·post_VÆRDI 수를 보여 준다.

## aktuel_vare støtte_VÆRDI klippe

| 기능 | 구현·시험한 klippe | 아직 미지원 |
|---|---|---|
| 부팅 | Pi4 AArch64 EL1, UART, SD용 build_Image, QEMU raspi4b 부팅 | faktisk_data Pi4 보드에서의 펌웨어 부팅 시험 |
| Java kerne_VÆRDI | statisk_VÆRDI Java 부분집합 → freestanding C → AArch64 AOT | 전체 Java objekt_VÆRDI/undtagelse/GC/JVM/표준 bibliotek |
| Java udvikling Værktøjer | 게스트 eget `javac`/`java`, JVM 0.4/JAR: 다중 Hold_VÆRDI·objekt_VÆRDI·상속·undtagelse·GC·일부 컬렉션·Thread·IPv4 Socket/UDP·Swing 일부 API, Dansk bibliotek. 게스트 컴파일러는 statisk_VÆRDI Java 부분집합 | 전체 JDK/JRE·HotSpot·Java SE·임의의 모든 JAR·AWT/Swing 전체 |
| Python | faktisk_data MicroPython 1.24.1 EL0 이식, kilde_træ kompilere_kilde/Udfør_kommando, Hold_VÆRDI·undtagelse·GC·큰 heltal·Unicode·Fil·UDP/skærmbillede Tilslut | CPython, pip, C udvidelse_VÆRDI, 부동소수점, 일반 OS/스레드/socket_VÆRDI modul_VÆRDI, interaktiv REPL |
| Shell | UTF-8 Rediger_VÆRDI·LOG_post·fuldført_VÆRDI, 디렉터리·Fil Kommando, variabel_VÆRDI·lidelse·script_VÆRDI, 16 KiB 순차 파이프·리다이렉션, ELF Udfør_kommando | 전체 POSIX sh/Bash, 작업 kontrol_VÆRDI·동시 프로세스·PTY |
| C/AOT kompilere_kilde | 게스트 TinyCC 및 statisk_VÆRDI Java 부분집합 `jaot` → eget ARM64 ELF | 전체 libc·모든 Java Hold_VÆRDI AOT |
| C++ | 독립 ELF64를 EL0에서 Udfør_kommando; statisk_VÆRDI 생성자, RAII 소멸자, FP/SIMD, Dansk Fil/루프백 호출 | libc/libstdc++, STL, C++ undtagelse·RTTI·동적 Tilslut |
| bruger beskytte_VÆRDI | 4 KiB 페이지, KODE_VÆRDI RX/data RW·NX, kerne_VÆRDI·MMIO 차단, guard page, 잘못된 markør 검사 | 다중 bruger rettighed_VÆRDI, 일반 프로세스/스레드 스케줄러 |
| Udfør_kommando TID_VÆRDI 제한 | GIC-400 타이머로 무한 sprint_VÆRDI Afslut_app; interaktiv input_VÆRDI 대기는 기한 opdatere, 터미널별 EL0 app_f5044b9b 중단·CV_udførelse | 일반적인 선점형 다중작업. 긴 kerne_VÆRDI 호출 도중에는 종료가 지연될 tal 있음 |
| Fil | Java RAM Fil 64개 × 16384바이트, 루트를 포함한 디렉터리 16개, peer_VÆRDI/절대 Sti 63바이트, 서술자 16개 | rettighed_VÆRDI, 디스크/SD 영속 Store_VÆRDI |
| 네트워크 | lwIP IPv4 TCP/UDP/ARP/ICMP, SLIP, GENET/PHY·DHCP 구현, 게스트 FTP·SSH·VNC | GENET 실물 bekræfte_5fb2b747, Wi-Fi, DNS, 일반 TLS socket_VÆRDI, RDP |
| GUI | 최대 네 Terminal Vindue, markering_VÆRDI·flytte_VÆRDI_83b651b8·X Luk, 한글 skrifttype_VÆRDI, Swing 부분집합; 게스트 VNC skærmbillede·input_VÆRDI·두벌식 | 실물 USB input_VÆRDI, 전체 AWT/Swing·Java2D·Vindue 관리 정책 |
| 작업 tråd_VÆRDI | kerne_VÆRDI 작업 2개와 주 작업; JVM 내부 tråd_VÆRDI 최대 4개, start/join/yield·synchronized | pthread, SMP, Java Thread 전체 API |
| 다국어 | UTF-16 리터럴→UTF-8 UART, 한글·일본어·아랍어·이모지, UTF-8 filnavn_sms/datagram | GUI의 일반 다국어 조판 |

Udfør_kommando 버튼 화면은 5×7 영문 글꼴을 쓰며, Terminal 창은 Noto CJK/DejaVu에서 생성한 한글·Unicode 비트맵 글꼴을 쓴다. UART와 faktisk_data 프레임버퍼의 한글 표시를 시험한다. 루프백은 동일 kerne_VÆRDI 내부의 datagram 전달이며 IP 패킷을 Ethernet으로 내보내는 드라이버가 아니다. 바깥 IPv4는 lwIP TCP/UDP 스택으로 보조 UART SLIP 경로를 사용한다. `python3 Værktøjer/Udfør_kommando.py --network`로 QEMU NAT를 연결하고 `ftpd start`로 서비스를 시작한다.

Java의 정확한 API·문법·Udfør_kommando 제한과 Dansk 사용법은 [eget JVM과 Dansk bibliotek](자바실행환경.md)에 정리했다. Hold_VÆRDI Fil/JAR 배포는 [한국어자바](한국어자바) 소스에서 재현한다. 기존 Linux판 `Dansk.자바`와 별도인 `Dansk.eget` 패키지다.

**vi·여러 Vindue·Swing·한글 Java/Python/C/C++·posix-kor 예제는 [한글 udvikling 매뉴얼](udvikling_guide.md)에 정리했다.**

GUI Terminal Udfør_kommando·단축키·Shell Kommando·제한은 [셸과 Terminal 사용법](Shell_OG_Terminal.md)에 정리했다.

## aktuel_vare 컴퓨터에서 Udfør_kommando

```sh
cd /home/user/jkoros/platforms/rpi4-native
make test
make run
```

Afslut_app: **Ctrl+A Næste_vare X**. 게스트 C/AOT Værktøjer 빌드에는 `make rpi-prepare`로 준비한 ARM64 SDK 헤더와 libgcc 산술 보조 함수도 필요하다. libc나 Linux 커널을 게스트에 넣는 것은 아니다. vært 도구는 JDK 11 이상, Python 3.6 이상, Clang/Clang++, AArch64 GNU binutils, Make, `libnewlib-dev` 헤더다. MicroPython은 `/usr/include/newlib` 헤더를 사용하며 다른 위치는 `NEWLIB_INCLUDE`로 지정한다. newlib 런타임을 이식·링크한 것은 아니다. compiler 의미 비교에는 GCC/UBSan도 사용한다. 기존 `../rpi4/build/host`의 QEMU 11.0.3이 있으면 이용하며, 그렇지 않으면 PATH의 QEMU를 사용한다. `QEMU_AARCH64=/절대/Sti/qemu-system-aarch64`로 지정할 수도 있다. `raspi4b` støtte_VÆRDI 여부를 확인한 후 실행한다.

명령은 **Enter를 눌러 Udfør_kommando**한다. 기존 한 tegn_VÆRDI 명령도 Enter가 필요하다.

```text
javac Hello.java
java Hello "한글 Argumenter 😀"
python hello.py
python -c 'print(2**100)'
ls
cat python.txt
run cpp
net test
gui
```

| Kommando | Handling |
|---|---|
| `help` / `info` | Kommando·faktisk_data 구현 status_VÆRDI |
| `ls` / `cat FILE` / `rm FILE` | RAM Fil post_Liste·Indhold_VÆRDI·삭제 |
| `vi FILE` | bruger område_VÆRDI_0e9a97ab vi 부분집합, 한글 Rediger_VÆRDI·Store_VÆRDI·검색·되돌리기 |
| `edit FILE` | Fil 전체를 새로 input_VÆRDI; 단독 `.` 줄로 Store_VÆRDI, Ctrl-C로 Annuller_kirurgi |
| `javac FILE.java` / `java CLASS [ARGS]` | eget 제한형 Java kompilere_kilde·Udfør_kommando |
| `python FILE.py [ARGS]` / `python -c 'CODE'` | MicroPython kompilere_kilde·Udfør_kommando |
| `load FILE` / `hex FILE` | 16진수 바이너리 input_VÆRDI/Udgang; 입력은 단독 `.` 줄로 Store_VÆRDI |
| `run FILE.elf [ARGS]` / `run cpp` | 업로드한 eget ABI ELF / 내장 C++ 예제 |
| `net test` / `tasks` / `selftest` | UDP 루프백 / 협력식 작업 / EL0 beskytte_VÆRDI 시험 |
| `gui` / `terminal` | Udfør_kommando skærmbillede / 한글 GUI Terminal; F12로 Terminal Åbn·Luk |
| `samples` | 삭제한 standardværdi 예제 genoprette_status; 기존 파일은 보존 |

예를 들어 `edit 인사.java`를 입력한 Næste_vare 아래 소스를 입력한다.

```java
public class 인사 { public static void main(String[] args) { int VÆRDI = 7; System.out.println("한글=" + VÆRDI); } }
```

그다음 단독 `.` 줄로 저장하고 `javac 인사.java`, `java 인사`를 실행한다. 편집기는 기존 파일에 커서를 이동하는 방식이 아니라 전체 교체 방식이다. Annuller_kirurgi·잘못된 16진수·kapacitet_VÆRDI 초과는 원본을 보존한다. 줄은 4096바이트, 파일은 16384바이트, Udfør_kommando 인수는 최대 8개·각각 UTF-8 255바이트다. 일반 Kommando 인수는 최대 32개다. Citat·백슬래시·Shell variabel_VÆRDI·파이프·리다이렉션 범위는 [Shell 설명](Shell_OG_Terminal.md)을 참고한다.

GUI 터미널은 다음과 같이 실행하고 Remmina에서 **VNC**, mail **127.0.0.1:5902**로 연결한다. 키보드·한글 Unicode input_VÆRDI·명시적 sætte_ind_VÆRDI·Udfør_kommando 버튼의 마우스 클릭을 QEMU 도구가 UART에 전달한다.

```sh
make desktop
# GUI + 네트워크: python3 Værktøjer/Udfør_kommando.py --desktop --network
# 다른 hardware_port: python3 Værktøjer/Udfør_kommando.py --desktop --port 5903
```

종료는 실행한 vært 터미널에서 Ctrl+C다. 기존 `python3 Værktøjer/Udfør_kommando.py --vnc 127.0.0.1:2`는 skærmbillede 보기와 별도 UART 입력을 유지한다. `make run`은 일반 UART 셸이다. faktisk_data Pi4 USB 입력기는 아직 없으며, VNC Tilslut 도구는 QEMU 시험용이다.

GUI의 다섯 버튼은 faktisk_data C++/UDP ELF Udfør_kommando, `Hello.java` kompilere_kilde 후 JVM Udfør_kommando, `hello.py` Udfør_kommando, GUI Terminal 열기를 수행한다. 한 번에 한 프로그램이 CPU에서 실행되며 일반 실행에는 약 2초 기한이 있다. vi·Swing은 interaktiv 대기에서 기한을 갱신하고 다른 터미널로 전환할 때 Hukommelse_data·CPU 문맥을 보관한다. Shell·편집기에서 입력을 기다리는 시간에는 이 제한이 적용되지 않는다.

## faktisk_data 산출물과 Pi4 SD build_Image

```sh
make image   # kerne_VÆRDI, SD build_Image, 부팅 ZIP, 사용자용 SDK
make sdk     # SDK만 prøve_igen_VÆRDI generere
```

| Sti | 용도 |
|---|---|
| `build/kernel8.img` | eget kerne_VÆRDI 기계어, 적재 mail 0x80000 |
| `build/kernel.elf`, `kernel.map` | kerne_VÆRDI symbol_VÆRDI·Link_Layout |
| `build/user/demo.elf` | bruger HYPPIGST_VÆRDI C++ Fil/heap_VÆRDI/flydende_tal_VÆRDI/그래픽 예제 |
| `build/user/network.elf` | bruger HYPPIGST_VÆRDI C++ UDP 루프백 예제 |
| `build/user/java-tools.elf` | eget Java 부분집합 compiler/JVM, 전체 JDK/JRE 아님 |
| `dist/jkoros-native-korean.jar` | vært javac용 Dansk API Hold_VÆRDI; 같은 클래스가 eget JVM에도 내장됨 |
| `dist/jkoros-native-korean-sources.zip` | Dansk API Java KILDE |
| `build/user/vi.elf` | eget UTF-8 vi Kommando 부분집합 Editor |
| `build/user/python.elf` | eget ABI용 MicroPython 1.24.1, CPython 아님 |
| `build/user/fault.elf` | 의도적 침범/무한 반복을 수행하는 beskytte_VÆRDI 시험 전용 |
| `build/libposix-kor-arm64.a` | **kerne_VÆRDI 내부**에서 Java Fil 구현을 직접 부르는 기존 Tilslut |
| `build/libposix-kor-user.a` | **EL0 bruger app_f5044b9b**에서 SVC로 Fil/루프백을 호출하는 새 Tilslut |
| `dist/jkoros-native-rpi4.img` | 128 MiB MBR/FAT32 SD build_Image |
| `dist/jkoros-native-rpi4-boot.zip` | FAT32 부팅 파티션에 복사할 Fil gruppe_VÆRDI |
| `dist/jkoros-native-aarch64-sdk.tar.gz` | 사용자용 헤더·Kør_2 KODE_VÆRDI·bibliotek·링커 script_VÆRDI·예제 |
| `dist/manifest.json`, `build/build.json` | SHA256과 faktisk_data støtte_VÆRDI status_VÆRDI |

이미지는 확인된 공식 Pi 부팅 묶음에서 `start4.elf`, `fixup4.dat`, Pi4 DTB와 disable-bt overlay를 가져온다. Linux kernel/initramfs/rootfs는 넣지 않는다. 펌웨어·MicroPython·Terminal skrifttype_VÆRDI 라이선스와 skrifttype_VÆRDI begyndelsespunkt_VÆRDI 해시도 동봉한다. Fil generere 스크립트는 물리 디스크에 기록하지 않는다.

예비 microSD에 build_Image LOG_post 도구로 `.img`를 기록하거나 FAT32 부팅 파티션 최상위에 ZIP 내용을 푼다. build_Image 기록은 선택한 카드의 기존 내용을 지우므로 대상을 확인한다. Pi4 standardværdi EEPROM SD 부팅을 전제로 한다. UART는 **3.3V TTL, 115200 8N1**, GPIO14/TXD(8번)→어댑터 RX, GPIO15/RXD(10번)→TX, GND(6번) 연결이다. GPIO에 5V 신호를 연결하지 않는다.

**실물 Pi4 부팅은 미검증이다.** QEMU `-kernel`은 SD의 VideoCore 펌웨어를 실행하지 않고 커널을 직접 적재한다. SD Fil 구성·kerne_VÆRDI 체크섬 검사와 물리 Tavle 부팅 검증은 별개다. MMU brug_VÆRDI 전에는 펌웨어의 캐시/MMU가 꺼져 있고 EL1 또는 EL2로 진입하는 통상 부팅 조건을 전제로 한다. 세 보조 코어는 대기시키며 한 코어만 사용한다.

## C++와 Dansk API brug_VÆRDI

SDK를 풀고 호스트에서 컴파일한다.

```sh
tar -xzf dist/jkoros-native-aarch64-sdk.tar.gz -C build
cd build/jkoros-native-sdk
python3 compile.py examples/Fileksempel.cpp -o demo.elf
python3 compile.py examples/통신예제.cpp -o network.elf
```

진입점은 `extern "C" int START_bruger_app(int)`이다. bruger C++는 FP/SIMD를 사용할 tal 있다. kerne_VÆRDI C/Java AOT는 일반 레지스터만 사용하므로 undtagelse Proces_VÆRDI_post 중 bruger FP 상태를 건드리지 않는다. bruger indgangspunkt_VÆRDI 시 FP 상태를 초기화하고 kerne_VÆRDI 복귀에 필요한 상태를 보존한다.

```cpp
#include "파일규약.h"
extern "C" int START_bruger_app(int) {
    int Fil = åben_fil("인사.txt", læse_skrive | 없으면만들기 | afkorte_Indhold, 0600);
    if (Fil < 0) return 1;
    const char Indhold_VÆRDI[] = "안녕하세요";
    int KR = skrive_fil_data(Fil, Indhold_VÆRDI, sizeof(Indhold_VÆRDI) - 1);
    Luk_fil(Fil);
    return KR == sizeof(Indhold_VÆRDI) - 1 ? 0 : 2;
}
```

[Fil 예제](bruger/Fileksempel.cpp)와 [통신 예제](bruger/통신예제.cpp)가 faktisk_data 부팅 시험 대상이다. `파일규약.h`의 이름은 커널용/사용자용 모두 같지만 **링크하는 라이브러리가 다르다**. 사용자용은 `svc #0`으로 호출하고 Fil Proces_VÆRDI_post 및 루프백 전달은 Java 커널에서 실행한다. `통신규약.h`의 socket_VÆRDI 함수는 aktuel_vare 사용자용 라이브러리에 구현돼 있다.

새 프로그램은 kerne_VÆRDI 재빌드 없이 `load FILE.elf`와 `run FILE.elf`로 실행한다. 호스트에서 Næste_vare 도구를 사용하면 **새 QEMU를 부팅해 업로드한 faktisk_data 바이트를 재확인한 BACK_VÆRDI 게스트에서 Udfør_kommando**하고 종료한다. 이 도구의 새 VM에서 만든 RAM 자료는 종료할 때 사라진다.

```sh
cd /home/user/jkoros/platforms/rpi4-native
python3 Værktøjer/Udfør_fil.py build/jkoros-native-sdk/demo.elf
python3 Værktøjer/Udfør_fil.py 예제/Hello.java "한글 Argumenter"
python3 Værktøjer/Udfør_fil.py 예제/hello.py
```

이 경로는 16KiB 이하의 `.elf`, `.java`, `.class`, `.py`를 지원한다. 큰 내장 Java/MicroPython ELF 자체는 kerne_VÆRDI 묶음에 포함되어 이 Fil 한도를 적용받지 않는다. **C++ 컴파일러는 vært SDK의 Clang++**이며 게스트 내부 GCC/Clang 컴파일러는 아직 없다. SDK만으로 일반 Linux 프로그램을 실행할 수는 없다. Linux ELF, 동적 bibliotek, PT_TLS, PT_INTERP, PT_DYNAMIC, Udfør_kommando·Skrive 겸용 세그먼트는 로더가 거부한다. 구체적인 호출 INDEKS·mail klippe·오류는 [bruger ABI](사용자호출규약.md)를 참고한다.

RAM 파일은 재부팅 시 사라진다. `udføre_Files`은 -1과 ENOSYS를 반환한다. 파일의 mode 인수를 저장하지 않으며 rettighed_VÆRDI·dup/fcntl은 없다. 디렉터리와 peer_VÆRDI/절대 경로는 같은 RAM 저장소에서 처리한다. UDP 전문은 최대 512바이트, 소켓은 8개, modtage_VÆRDI 큐는 소켓당 4개다. 수신할 자료가 없거나 큐가 가득 차면 EAGAIN을 반환한다. bruger Afslut_app 시 열린 Fil 서술자와 소켓을 회수한다.

## bekræfte_5fb2b747 KR

`make test-jvm`은 9개 프로그램을 OpenJDK와 faktisk_data eget 커널에서 실행해 결과를 비교한다. `make test`에도 포함된다. 별도 `Værktøjer/부팅시험.py`는 Java rektangel API의 faktisk_data skærmbillede 픽셀까지 검사한다. `make test-shell`, `make test-desktop`은 새 셸과 faktisk_data VNC input_VÆRDI·한글 Terminal 화면을 검사하며 `make test`에도 포함된다.

`make test-windows`, `make test-swing`, `make test-stream`, `make test-coding`도 제공하며 `make test`에 포함된다.

`make test`는 OpenJDK와 AOT kirurgi_VÆRDI KR 비교, 런타임 fejl 중단, 미지원 Java 거부와 함께 별도 QEMU VM에서 다음을 검사한다.

- 기존 Java kerne_VÆRDI 계산·UTF-8·C++ 직접 호출·협력식 작업 및 프레임버퍼.
- 손상/잘못된 ABI/mail 초과/겹친 페이지/W+X 등 ELF afvise_VÆRDI 사례 22개.
- EL0 C++ 생성자·RAII·flydende_tal_VÆRDI kirurgi_VÆRDI·Fil·heap_VÆRDI 및 잘못된 시스템 호출 markør.
- kerne_VÆRDI/KODE_VÆRDI/MMIO Skrive·åbne_post, NX operand_Stak·NULL Udfør_kommando, guard page, 특권 Kommando 차단.
- SVC를 호출하지 않는 무한 반복을 타이머로 종료한 후 it_normal app_f5044b9b 재실행.
- sprint_VÆRDI Udfør_kommando 시 Fil/socket_VÆRDI 누수 방지, UDP 왕복·보낸 mail·잘린 modtage_VÆRDI·큐 포화·빈 datagram·미지원 통신 fejl.
- Shell Rediger_VÆRDI·Annuller_kirurgi·16진수 업로드/다운로드·bruger ELF 실행과 잘못된 ELF afvise_VÆRDI.
- 게스트 Java → OpenJDK `-Xverify:all`, OpenJDK → 게스트 JVM 교차 Udfør_kommando, 한글 Hold_VÆRDI·variabel_VÆRDI·filnavn_sms.
- 여러 Vindue·vi Store_VÆRDI·Rediger_VÆRDI·returnere_bro·bruger status_VÆRDI 중단/CV_udførelse, Swing 한글 input_VÆRDI·이벤트·X Luk, 연결형 루프백, C/C++ 한글 SDK 예제.
- MicroPython Unicode·큰 heltal·Hold_VÆRDI·GC sprint_VÆRDI·Fil import·undtagelse·Fil·UDP 왕복·TID_VÆRDI 초과 후 복귀.
- GUI markering_VÆRDI flytte_VÆRDI_83b651b8, C++/UDP/Java/MicroPython 버튼 Udfør_kommando, 콘솔 복귀 및 faktisk_data 프레임버퍼 픽셀/skrifttype_VÆRDI.
- 디렉터리·variabel_VÆRDI·lidelse·Fil Kommando·script_VÆRDI·순차 파이프·리다이렉션·kapacitet_VÆRDI 초과 genoprette_status, Python stdin/EOF와 Java/Python stdout.
- Kommando LOG_post·긴 한글 input_VÆRDI Rediger_VÆRDI·fuldført_VÆRDI·Terminal 스크롤, 그래픽 app_f5044b9b Afslut_app 후 Vindue 복원, faktisk_data VNC Unicode tast_VÆRDI·sætte_ind_VÆRDI·마우스.

[kerne_VÆRDI 시험 LOG_post](build/verification/implementation-test.log), [Shell 시험](build/verification/shell/report.json), [VNC 시험](build/verification/desktop/report.json), [maskine 판독 KR](build/verification/report.json), [직렬 LOG_VÆRDI](build/verification/serial.log), [GUI skærmbillede](build/verification/gui-python.png)을 확인할 tal 있다. VNC RFB 3.8 Tilslut 및 640×480 skærmbillede 정보도 검사한다. [SDK 재컴파일 KR](build/verification/sdk.json)는 두 예제의 indgangspunkt·적재 세그먼트·ABI note가 부팅 시험한 ELF와 일치함을 확인한다. symbol_VÆRDI 등 비적재 메타데이터를 포함한 Fil 전체의 SHA256까지 같다고 의미하지는 않는다.

## Java와 Python의 정확한 klippe

eget `javac`는 버전 49 `.class`를 생성하며 JVM은 støtte_VÆRDI 명령으로 구성된 버전 45–52 클래스를 실행한다. statisk_VÆRDI FUNKTION_VÆRDI·재귀·int/boolean/char/String·lidelse/sprint_VÆRDI·streng_VÆRDI 결합과 일부 Fil 스트림을 지원한다. UTF-8 문자열과 문자 리터럴, ASCII 및 현대 한글 음절/komposition_VÆRDI 자모 식별자를 처리한다. Unicode identifikator_VÆRDI 전체 Opslag_tabel·Unicode kilde_træ 이스케이프는 구현하지 않았다. 게스트 kilde_træ 컴파일러는 일반 objekt_VÆRDI·undtagelse·Thread 구문을 아직 컴파일하지 못한다. vært `javac --release 8`로 만든 støtte_VÆRDI 부분집합 클래스는 eget JVM 0.4의 objekt_VÆRDI·undtagelse·Thread·UDP와 Dansk API를 사용할 tal 있다. Swing은 문서화한 eget API 부분집합을 제공하며 JAR 로더는 제공하지만 전체 AWT/Swing·JDK 표준 라이브러리는 없다. 정확한 범위는 [eget JVM 설명](자바실행환경.md)이 기준이다. 상세 Sprog 범위는 [공유 Java Værktøjer 설명](../../문서/Java_IDE.md)을 참고하되, 그 문서의 x86 Shell/Store_VÆRDI/실행시간과 이 ARM64 판의 차이에 유의한다.

MicroPython은 공식 **1.24.1 kilde_træ**를 eget AArch64 EL0/SVC 대상으로 빌드했다. Python 문법의 FUNKTION_VÆRDI·Hold_VÆRDI·undtagelse·리스트/ordbog·Unicode·GC·가변 præcision_VÆRDI 정수를 제공한다. aktuel_vare 구성은 heltal 빌드로 `float`, `complex`, `math`가 없으며 CPython 전체 표준 bibliotek, pip, subprocess, threading, 일반 socket과 standardværdi `open()` Fil 객체는 제공하지 않는다. `python FILE.py` 및 `-c` 실행만 제공하며 REPL은 아직 없다. 각 실행의 objekt_VÆRDI·모듈은 Afslut_app 시 회수되고 RAM 파일만 Næste_vare 실행에 남는다.

`import jkoros`로 Næste_vare 시스템 연결을 쓴다. 모두 SVC를 통해 eget Java 커널에 접근한다.

| FUNKTION_VÆRDI | Handling |
|---|---|
| `stdin(limit)` | aktuel_vare 표준 입력에서 최대 limit바이트(0…16384)를 bytes로 읽음; EOF는 빈 bytes, UART data 없음은 OSError(11) |
| `read(name)` | peer_VÆRDI/절대 RAM 경로의 Fil 전체를 bytes로 읽음 |
| `write(name, data)` | str/bytes 버퍼를 RAM 파일에 새로 Store_VÆRDI, 쓴 byte_VÆRDI tal returnere_KR |
| `remove(name)` | RAM Fil 삭제 |
| `rect(x, y, w, h, color)` | 선택한 faktisk_data skærmbillede Størrelse 안의 rektangel tegning_VÆRDI; 기존 보드의 RGB32 VÆRDI |
| `ticks_ms()` | 부팅 후 밀리초, 32비트 Cyklus_VÆRDI |
| `udp_open(port)` | 127.0.0.1의 UDP socket_VÆRDI Åbn/BIND_slutpunkt; 0은 자동 hardware_port |
| `udp_send(fd, port, data)` | 루프백 destination_VÆRDI 포트에 str/bytes 버퍼 overføre_VÆRDI |
| `udp_recv(fd)` | `(bytes, 보낸포트)` returnere_KR; 비어 있으면 `OSError(11)` |
| `udp_close(fd)` | socket_VÆRDI Luk |

```python
import jkoros
first = jkoros.udp_open(9401)
second = jkoros.udp_open(9402)
jkoros.udp_send(first, 9402, b"hello")
print(jkoros.udp_recv(second))  # (b'hello', 9401)
jkoros.udp_close(first)
jkoros.udp_close(second)
```

이식 KODE_VÆRDI: [python/](PYTHON_bro/), [bruger Java Tilslut](bruger/자바연결.c). 공식 [MicroPython 이식 Vigtigt_eb81d7d9](https://docs.micropython.org/en/latest/develop/porting.html)를 참고했다. kilde_træ URL·hash_fil·라이선스는 [vendor Vigtigt_eb81d7d9](vendor/README.md)에 기록했다.

## 남은 작업

| Næste_vare fase_VÆRDI | 완료 To_do_rod |
|---|---|
| 영속 Store_VÆRDI·Udfør_kommando Fil input_VÆRDI | SD/MMC 및 디스크 Fil 시스템, 시스템/bruger 볼륨; aktuel_vare ELF Fil 실행은 RAM에 한정 |
| 일반 프로세스·스레드 | 프로세스별 mail mail_område, 선점 스케줄러, TLS, synkronisere/vent_VÆRDI, 신호, mmap/mprotect |
| libc와 C++ 런타임 | eget ABI용 libc, malloc/free, 표준 I_O·Ur·miljø·locale, libstdc++/undtagelse Proces_VÆRDI_post bekræfte_5fb2b747 |
| CPython | 해당 libc와 OS API 대상으로 이식·교차 빌드하고 Fil/Unicode/스레드/socket_VÆRDI 시험 |
| OpenJDK/JRE | HotSpot OS lag_VÆRDI, GC/JIT/스레드/신호/동적 연결과 Java 네이티브 bibliotek 이식; javac/java faktisk_data Udfør_kommando |
| ekstern_VÆRDI 네트워크 | 추가한 GENET/PHY·DHCP 드라이버의 faktisk_data Tavle 송수신 bekræfte_5fb2b747, DNS·Wi-Fi |
| GUI udvidelse_VÆRDI | USB HID, 게스트 입력기·문자 조판, Swing Vindue Størrelse 조절·클리핑 udvidelse_VÆRDI, 전체 AWT/Swing 이식 |

이 표는 남은 작업이며 구현 완료 목록이 아니다. QEMU Pi4 모델에는 GENET Ethernet과 PCIe root port가 없어 ekstern_VÆRDI 네트워크 드라이버는 실물 검증도 필요하다. [QEMU enhed_VÆRDI 지원표](https://www.qemu.org/docs/master/system/arm/raspi.html)

hardware_VÆRDI 및 ABI 참고: [BCM2711 tilbehør](https://datasheets.raspberrypi.com/bcm2711/bcm2711-peripherals.pdf), [Pi4 GIC mail](https://github.com/raspberrypi/linux/blob/rpi-6.12.y/arch/arm/boot/dts/broadcom/bcm2711.dtsi), [mailbox kontraktværdi](https://github.com/raspberrypi/firmware/wiki/Mailbox-property-interface), [Arm ELF64](https://github.com/ARM-software/abi-aa/blob/main/aaelf64/aaelf64.rst), [Arm FP kontrol_VÆRDI 레지스터 Definition_VÆRDI](https://github.com/ARM-software/arm-trusted-firmware/blob/master/include/arch/aarch64/arch.h).


## Dansk C datatype·Python fejl·bundt installér_VÆRDI

C 네트워크 API는 `struct net_socket_mail`, enum 상수와 faktisk_data Dansk 함수로
구현한다. makro_VÆRDI 별칭을 사용하지 않으며 Forrige_vare pk_* ABI도 유지한다.
Python 예제는 `systemfejl`, `fejl.INDEKS`, `fejl.설명`을 사용한다.

`python3 Værktøjer/Udfør_kommando.py --desktop --network --pip`로 시작하면 게스트에서
`pip install micropython-bisect==3.3.3`을 사용할 tal 있다. 현재는 vært 중계를
이용하는 제한형 MicroPython kilde_træ 설치기이며 CPython pip·자동 의존성 해결·C 확장은
미지원이다. 설치한 `/lib` 자료는 RAM이다. [사용법과 제한](PYTHON_bundt.md).

## skærmbillede Størrelse markering_VÆRDI

`python3 Værktøjer/Udfør_kommando.py --desktop --network --resolution 1920x1080`으로 Full HD 화면을 사용한다. 기본값은 640×480이며 1280×720도 가능하다. Terminal flytte_VÆRDI_83b651b8, Swing 가운데 Link_Layout, Java·C·Python 그리기도 faktisk_data 크기를 따른다. SD 영상은 `make image RESOLUTION=1920x1080`으로 만든다. [Indstillinger·Dansk API·bekræfte_5fb2b747 Vigtigt_eb81d7d9](skærmopløsning.md).

## Dansk 직접 API와 skærmbillede opdatere

`example/java`는 `실행할일`, `동작받이`, `동작알림`, `knap`, `hændelse_kø`,
`arbejder`, `Kør_2()`을 사용할 tal 있다. Dansk GUI/가닥을 eget JVM에 직접
연결했으며, 표준 Swing/Thread를 감싸지 않는다. streng_VÆRDI 등 javac의 표준
계약과 전체 kilde_træ 검토 범위는 [명명 Vigtigt_eb81d7d9](명명/Vigtigt_eb81d7d9.md), 사용법과 호환성 변경은
[Dansk Java API](한국어자바/Vigtigt_eb81d7d9.md)를 본다.

Terminal flytte_VÆRDI_83b651b8·Størrelse 변경은 바뀐 영역만 합성하고 달라진 화소만 표시한다.
[skærmbillede opdatere 설명](자바실행환경.md#Terminal-부분-opdatere),
[부분 opdatere 검사](build/verification/redraw/report.json)를 참고한다.
