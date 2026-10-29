# Raspberry Pi 4 eget Java kärna_värde — användarutrymme köra_kommando 기반

aktuellt_objekt eget 코드의 COSL 상업 villkor, 제3자 고지 및 LGPL 재연결 자료는 [COSL fördelning_värde VIKTIGT_eb81d7d9](COSL배포안내.md)를 참고한다. byta_läge 전 GPL 구성의 판단은 [Föregående_objekt 라이선스 검토](licens_granska.md)에 기록했다.

Svenska kommunikation·fel_31f743d2 사용법은 [Svenska Java API](한국어자바/VIKTIGT_eb81d7d9.md), FUNKTION_värde·variabel_värde·filnamn 이름의 변경과 어원 근거는 [명명 VIKTIGT_eb81d7d9](명명/VIKTIGT_eb81d7d9.md)를 참고한다.

Linux 없이 부팅하는 eget AArch64 커널이다. Java AOT kärna_värde 위에 **kommandorad Shell, 게스트 Java kompilerare·JVM, MicroPython, EL0 C++ köra_kommando, filnamn·UDP 루프백 시스템 호출, 여러 한글 GUI kommandotolk·vi Editor·Swing 부분집합**을 제공한다. 커널의 filnamn data/정책·루프백 Överför_värde·Shell 상태는 Java, skärmbild 합성·bildpunkt ändra_värde·markör·클리핑도 Java로 구현하며, CPU/MMU/enhet_värde 경계와 kommandotolk·tecken_värde Paint_skärmbild 연결은 C와 어셈블리다.

**전체 JDK/JRE·CPython·표준 C++ 런타임·Swing 이식은 아직 완료되지 않았다.** 기존 [ARM64 Linux 실행판](../rpi4/README.md)의 OpenJDK/Python 패키지를 이 eget 커널에 탑재했다고 표시하지 않는다.

새로운 게스트 `cc`/`jaot`, JAR 직접 köra_kommando, lwIP TCP/UDP와 FTP는 [FTP·C·JAR·AOT 매뉴얼](파일전송과번역.md)을 참고한다. 게스트 SSH·VNC와 Pi4 GENET/PHY·DHCP 드라이버를 추가했다. **SSH·VNC는 QEMU에서 검증하며, 실물 Pi4의 kabelansluten_värde 송수신은 아직 미검증이다.** köra_kommando·kontakt_e05f319b·lösenord_värde 확인은 [extern_värde kontakt_e05f319b VIKTIGT_eb81d7d9](extern_kontakt_guide.md)에 정리했다.

셸은 EL1 kärna_värde, `java` 등 användarutrymme köra_kommando 파일은 EL0에서 실행한다.
`ps`·`top`의 표시와 제한, QEMU 네트워크 köra_kommando·kontakt_e05f319b 방법 및 verklig_data 검증은
[köra_kommando 계층과 extern_värde kommunikation 점검](실행계층과외부통신점검.md)을 참고한다.

ELF는 확장자가 아닌 verklig_data köra_kommando 형식으로 검사한다. `./인사`처럼 확장자 없이 실행하며, 제한된 Linux ARM64 statisk_värde ELF는 `run --linux filnamn_SMS`으로 실행한다. [ELF·Linux ABI stöd_värde 범위와 동일 바이너리 tester](실행파일규약.md).

GUI와 네트워크는 `python3 verktyg/köra_kommando.py --desktop --network`로 함께 사용한다. Java·C·Python의 Svenska 예제 13개는 [jkoros/example](../../example/README.md)에 있으며, **게스트 maskinstart 시 `/example/java`, `/example/c`, `/example/python`에 자동으로 준비된다.** `example java|c|python`으로 지운 예제를 복원할 nummer 있다. Remmina에서 **F9/Shift+Space/한·noll_operand Nyckel_värde**로 `[EN]`↔`[KO]` 두벌식을 전환한다(`help ko`). `make test-examples`는 같은 GUI VM에서 FTP·verklig_data TCP/UDP·filnamn byte_värde·그래픽 픽셀을 검증한다.

게스트에서 `cd /example/java` 후 `java Fönsterexempel`로 Svenska Swing 예제를 실행한다. kommandotolk 모서리에 마우스를 대고 **왼쪽 버튼으로 끌면 크기가 바뀐다**. `terminal size`는 aktuellt_objekt spalt_värde·RAD_värde 수를 보여 준다.

## aktuellt_objekt stöd_värde klipp

| 기능 | implementation·시험한 klipp | 아직 미지원 |
|---|---|---|
| maskinstart | Pi4 AArch64 EL1, UART, SD용 version_BILD, QEMU raspi4b maskinstart | verklig_data Pi4 보드에서의 펌웨어 maskinstart tester |
| Java kärna_värde | statisk_värde Java 부분집합 → freestanding C → AArch64 AOT | 전체 Java objekt_värde/fel_31f743d2/GC/JVM/표준 bibliotek |
| Java utveckling verktyg | 게스트 eget `javac`/`java`, JVM 0.4/JAR: 다중 Kurs_värde·objekt_värde·상속·fel_31f743d2·GC·일부 컬렉션·Thread·IPv4 Socket/UDP·Swing 일부 API, Svenska bibliotek. 게스트 컴파일러는 statisk_värde Java 부분집합 | 전체 JDK/JRE·HotSpot·Java SE·임의의 모든 JAR·AWT/Swing 전체 |
| Python | verklig_data MicroPython 1.24.1 EL0 이식, källa_träd kompilera_källa/köra_kommando, Kurs_värde·fel_31f743d2·GC·큰 heltal·Unicode·filnamn·UDP/skärmbild Anslut | CPython, pip, C tillägg_värde, 부동소수점, 일반 OS/스레드/socket_värde modul_värde, interaktiv REPL |
| Shell | UTF-8 ändring_värde·LOG_POST·Slutfört_värde, 디렉터리·filnamn kommando, variabel_värde·villkor·skript_värde, 16 KiB 순차 파이프·리다이렉션, ELF köra_kommando | 전체 POSIX sh/Bash, 작업 kontroll_värde·동시 프로세스·PTY |
| C/AOT kompilera_källa | 게스트 TinyCC 및 statisk_värde Java 부분집합 `jaot` → eget ARM64 ELF | 전체 libc·모든 Java Kurs_värde AOT |
| C++ | 독립 ELF64를 EL0에서 köra_kommando; statisk_värde 생성자, RAII 소멸자, FP/SIMD, Svenska filnamn/루프백 호출 | libc/libstdc++, STL, C++ fel_31f743d2·RTTI·동적 Anslut |
| användarutrymme skydda_värde | 4 KiB 페이지, KOD_värde RX/data RW·NX, kärna_värde·MMIO 차단, guard page, 잘못된 markör 검사 | 다중 användarutrymme behörighet_värde, 일반 프로세스/스레드 스케줄러 |
| köra_kommando tid_värde 제한 | GIC-400 타이머로 무한 sprint_värde Utgång_app; interaktiv indata_värde 대기는 기한 uppdatera, 터미널별 EL0 app_f5044b9b 중단·CV_körning | 일반적인 선점형 다중작업. 긴 kärna_värde 호출 도중에는 종료가 지연될 nummer 있음 |
| filnamn | Java RAM filnamn 64개 × 16384바이트, 루트를 포함한 디렉터리 16개, peer_värde/절대 sökväg_2 63바이트, 서술자 16개 | behörighet_värde, 디스크/SD 영속 Store_värde |
| 네트워크 | lwIP IPv4 TCP/UDP/ARP/ICMP, SLIP, GENET/PHY·DHCP implementation, 게스트 FTP·SSH·VNC | GENET 실물 validera, Wi-Fi, DNS, 일반 TLS socket_värde, RDP |
| GUI | 최대 네 kommandotolk Fönster, markering_värde·flytta_värde·X Stäng, 한글 teckensnitt_värde, Swing 부분집합; 게스트 VNC skärmbild·indata_värde·두벌식 | 실물 USB indata_värde, 전체 AWT/Swing·Java2D·Fönster 관리 정책 |
| 작업 tråd_värde | kärna_värde 작업 2개와 주 작업; JVM 내부 tråd_värde 최대 4개, start/join/yield·synchronized | pthread, SMP, Java Thread 전체 API |
| 다국어 | UTF-16 리터럴→UTF-8 UART, 한글·일본어·아랍어·이모지, UTF-8 filnamn_SMS/datagram | GUI의 일반 다국어 조판 |

köra_kommando 버튼 화면은 5×7 영문 글꼴을 쓰며, kommandotolk 창은 Noto CJK/DejaVu에서 생성한 한글·Unicode 비트맵 글꼴을 쓴다. UART와 verklig_data 프레임버퍼의 한글 표시를 시험한다. 루프백은 동일 kärna_värde 내부의 datagram 전달이며 IP 패킷을 Ethernet으로 내보내는 드라이버가 아니다. 바깥 IPv4는 lwIP TCP/UDP 스택으로 보조 UART SLIP 경로를 사용한다. `python3 verktyg/köra_kommando.py --network`로 QEMU NAT를 연결하고 `ftpd start`로 서비스를 시작한다.

Java의 정확한 API·문법·köra_kommando 제한과 Svenska 사용법은 [eget JVM과 Svenska bibliotek](자바실행환경.md)에 정리했다. Kurs_värde filnamn/JAR 배포는 [한국어자바](한국어자바) 소스에서 재현한다. 기존 Linux판 `Svenska.자바`와 별도인 `Svenska.eget` 패키지다.

**vi·여러 Fönster·Swing·한글 Java/Python/C/C++·posix-kor 예제는 [한글 utveckling 매뉴얼](utveckling_guide.md)에 정리했다.**

GUI kommandotolk köra_kommando·단축키·Shell kommando·제한은 [셸과 kommandotolk 사용법](Shell_AND_Terminal.md)에 정리했다.

## aktuellt_objekt 컴퓨터에서 köra_kommando

```sh
cd /home/user/jkoros/platforms/rpi4-native
make test
make run
```

Utgång_app: **Ctrl+A Nästa_objekt X**. 게스트 C/AOT verktyg 빌드에는 `make rpi-prepare`로 준비한 ARM64 SDK 헤더와 libgcc 산술 보조 함수도 필요하다. libc나 Linux 커널을 게스트에 넣는 것은 아니다. värd 도구는 JDK 11 이상, Python 3.6 이상, Clang/Clang++, AArch64 GNU binutils, Make, `libnewlib-dev` 헤더다. MicroPython은 `/usr/include/newlib` 헤더를 사용하며 다른 위치는 `NEWLIB_INCLUDE`로 지정한다. newlib 런타임을 이식·링크한 것은 아니다. kompilerare 의미 비교에는 GCC/UBSan도 사용한다. 기존 `../rpi4/build/host`의 QEMU 11.0.3이 있으면 이용하며, 그렇지 않으면 PATH의 QEMU를 사용한다. `QEMU_AARCH64=/절대/sökväg_2/qemu-system-aarch64`로 지정할 수도 있다. `raspi4b` stöd_värde 여부를 확인한 후 실행한다.

명령은 **Enter를 눌러 köra_kommando**한다. 기존 한 tecken_värde 명령도 Enter가 필요하다.

```text
javac Hello.java
java Hello "한글 argument 😀"
python hello.py
python -c 'print(2**100)'
ls
cat python.txt
run cpp
net test
gui
```

| kommando | Åtgärd |
|---|---|
| `help` / `info` | kommando·verklig_data implementation status_värde |
| `ls` / `cat FILE` / `rm FILE` | RAM filnamn post_ange·Innehåll_värde·삭제 |
| `vi FILE` | användarutrymme område_värde_0e9a97ab vi 부분집합, 한글 ändring_värde·Store_värde·검색·되돌리기 |
| `edit FILE` | filnamn 전체를 새로 indata_värde; 단독 `.` 줄로 Store_värde, Ctrl-C로 Avbryt_åtgärd |
| `javac FILE.java` / `java CLASS [ARGS]` | eget 제한형 Java kompilera_källa·köra_kommando |
| `python FILE.py [ARGS]` / `python -c 'CODE'` | MicroPython kompilera_källa·köra_kommando |
| `load FILE` / `hex FILE` | 16진수 바이너리 indata_värde/utmatningsposition; 입력은 단독 `.` 줄로 Store_värde |
| `run FILE.elf [ARGS]` / `run cpp` | 업로드한 eget ABI ELF / 내장 C++ 예제 |
| `net test` / `tasks` / `selftest` | UDP 루프백 / 협력식 작업 / EL0 skydda_värde tester |
| `gui` / `terminal` | köra_kommando skärmbild / 한글 GUI kommandotolk; F12로 kommandotolk Öppna·Stäng |
| `samples` | 삭제한 standardvärde 예제 återställa_status; 기존 파일은 보존 |

예를 들어 `edit 인사.java`를 입력한 Nästa_objekt 아래 소스를 입력한다.

```java
public class 인사 { public static void main(String[] args) { int värde = 7; System.out.println("한글=" + värde); } }
```

그다음 단독 `.` 줄로 저장하고 `javac 인사.java`, `java 인사`를 실행한다. 편집기는 기존 파일에 커서를 이동하는 방식이 아니라 전체 교체 방식이다. Avbryt_åtgärd·잘못된 16진수·kapacitet_värde 초과는 원본을 보존한다. 줄은 4096바이트, 파일은 16384바이트, köra_kommando 인수는 최대 8개·각각 UTF-8 255바이트다. 일반 kommando 인수는 최대 32개다. Citat·백슬래시·Shell variabel_värde·파이프·리다이렉션 범위는 [Shell 설명](Shell_AND_Terminal.md)을 참고한다.

GUI 터미널은 다음과 같이 실행하고 Remmina에서 **VNC**, Adress **127.0.0.1:5902**로 연결한다. 키보드·한글 Unicode indata_värde·명시적 klistra_in_värde·köra_kommando 버튼의 마우스 클릭을 QEMU 도구가 UART에 전달한다.

```sh
make desktop
# GUI + 네트워크: python3 verktyg/köra_kommando.py --desktop --network
# 다른 maskinvara_port: python3 verktyg/köra_kommando.py --desktop --port 5903
```

종료는 실행한 värd 터미널에서 Ctrl+C다. 기존 `python3 verktyg/köra_kommando.py --vnc 127.0.0.1:2`는 skärmbild 보기와 별도 UART 입력을 유지한다. `make run`은 일반 UART 셸이다. verklig_data Pi4 USB 입력기는 아직 없으며, VNC Anslut 도구는 QEMU 시험용이다.

GUI의 다섯 버튼은 verklig_data C++/UDP ELF köra_kommando, `Hello.java` kompilera_källa 후 JVM köra_kommando, `hello.py` köra_kommando, GUI kommandotolk 열기를 수행한다. 한 번에 한 프로그램이 CPU에서 실행되며 일반 실행에는 약 2초 기한이 있다. vi·Swing은 interaktiv 대기에서 기한을 갱신하고 다른 터미널로 전환할 때 Minne_data·CPU 문맥을 보관한다. Shell·편집기에서 입력을 기다리는 시간에는 이 제한이 적용되지 않는다.

## verklig_data 산출물과 Pi4 SD version_BILD

```sh
make image   # kärna_värde, SD version_BILD, maskinstart ZIP, 사용자용 SDK
make sdk     # SDK만 försöka_igen_värde generera
```

| sökväg_2 | 용도 |
|---|---|
| `build/kernel8.img` | eget kärna_värde 기계어, 적재 Adress 0x80000 |
| `build/kernel.elf`, `kernel.map` | kärna_värde symbol_värde·länkningslayout |
| `build/user/demo.elf` | användarutrymme läge_värde C++ filnamn/heap_värde/flyttal_värde/그래픽 예제 |
| `build/user/network.elf` | användarutrymme läge_värde C++ UDP 루프백 예제 |
| `build/user/java-tools.elf` | eget Java 부분집합 kompilerare/JVM, 전체 JDK/JRE 아님 |
| `dist/jkoros-native-korean.jar` | värd javac용 Svenska API Kurs_värde; 같은 클래스가 eget JVM에도 내장됨 |
| `dist/jkoros-native-korean-sources.zip` | Svenska API Java källfil |
| `build/user/vi.elf` | eget UTF-8 vi kommando 부분집합 Editor |
| `build/user/python.elf` | eget ABI용 MicroPython 1.24.1, CPython 아님 |
| `build/user/fault.elf` | 의도적 침범/무한 반복을 수행하는 skydda_värde tester 전용 |
| `build/libposix-kor-arm64.a` | **kärna_värde 내부**에서 Java filnamn 구현을 직접 부르는 기존 Anslut |
| `build/libposix-kor-user.a` | **EL0 användarutrymme app_f5044b9b**에서 SVC로 filnamn/루프백을 호출하는 새 Anslut |
| `dist/jkoros-native-rpi4.img` | 128 MiB MBR/FAT32 SD version_BILD |
| `dist/jkoros-native-rpi4-boot.zip` | FAT32 maskinstart 파티션에 복사할 filnamn grupp_värde |
| `dist/jkoros-native-aarch64-sdk.tar.gz` | 사용자용 헤더·Kör KOD_värde·bibliotek·링커 skript_värde·예제 |
| `dist/manifest.json`, `build/build.json` | SHA256과 verklig_data stöd_värde status_värde |

이미지는 확인된 공식 Pi maskinstart 묶음에서 `start4.elf`, `fixup4.dat`, Pi4 DTB와 disable-bt overlay를 가져온다. Linux kernel/initramfs/rootfs는 넣지 않는다. 펌웨어·MicroPython·kommandotolk teckensnitt_värde 라이선스와 teckensnitt_värde origo_värde 해시도 동봉한다. filnamn generera 스크립트는 물리 디스크에 기록하지 않는다.

예비 microSD에 version_BILD LOG_POST 도구로 `.img`를 기록하거나 FAT32 maskinstart 파티션 최상위에 ZIP 내용을 푼다. version_BILD 기록은 선택한 카드의 기존 내용을 지우므로 대상을 확인한다. Pi4 standardvärde EEPROM SD 부팅을 전제로 한다. UART는 **3.3V TTL, 115200 8N1**, GPIO14/TXD(8번)→어댑터 RX, GPIO15/RXD(10번)→TX, GND(6번) 연결이다. GPIO에 5V 신호를 연결하지 않는다.

**실물 Pi4 부팅은 미검증이다.** QEMU `-kernel`은 SD의 VideoCore 펌웨어를 실행하지 않고 커널을 직접 적재한다. SD filnamn 구성·kärna_värde 체크섬 검사와 물리 Tavla maskinstart 검증은 별개다. MMU använda_värde 전에는 펌웨어의 캐시/MMU가 꺼져 있고 EL1 또는 EL2로 진입하는 통상 maskinstart 조건을 전제로 한다. 세 보조 코어는 대기시키며 한 코어만 사용한다.

## C++와 Svenska API använda_värde

SDK를 풀고 호스트에서 컴파일한다.

```sh
tar -xzf dist/jkoros-native-aarch64-sdk.tar.gz -C build
cd build/jkoros-native-sdk
python3 compile.py examples/Filexempel.cpp -o demo.elf
python3 compile.py examples/통신예제.cpp -o network.elf
```

진입점은 `extern "C" int START_användare_app(int)`이다. användarutrymme C++는 FP/SIMD를 사용할 nummer 있다. kärna_värde C/Java AOT는 일반 레지스터만 사용하므로 fel_31f743d2 Process_värde_post 중 användarutrymme FP 상태를 건드리지 않는다. användarutrymme startpunkt_värde 시 FP 상태를 초기화하고 kärna_värde 복귀에 필요한 상태를 보존한다.

```cpp
#include "파일규약.h"
extern "C" int START_användare_app(int) {
    int filnamn = skapa_fil("인사.txt", läsa_skriva | 없으면만들기 | trimma_Innehåll, 0600);
    if (filnamn < 0) return 1;
    const char Innehåll_värde[] = "안녕하세요";
    int RESULTAT = skriva_fil_data(filnamn, Innehåll_värde, sizeof(Innehåll_värde) - 1);
    Stäng_fil(filnamn);
    return RESULTAT == sizeof(Innehåll_värde) - 1 ? 0 : 2;
}
```

[filnamn 예제](användarutrymme/Filexempel.cpp)와 [kommunikation 예제](användarutrymme/통신예제.cpp)가 verklig_data maskinstart tester 대상이다. `파일규약.h`의 이름은 커널용/사용자용 모두 같지만 **링크하는 라이브러리가 다르다**. 사용자용은 `svc #0`으로 호출하고 filnamn Process_värde_post 및 루프백 전달은 Java 커널에서 실행한다. `통신규약.h`의 socket_värde 함수는 aktuellt_objekt 사용자용 라이브러리에 구현돼 있다.

새 프로그램은 kärna_värde 재빌드 없이 `load FILE.elf`와 `run FILE.elf`로 실행한다. 호스트에서 Nästa_objekt 도구를 사용하면 **새 QEMU를 부팅해 업로드한 verklig_data 바이트를 재확인한 BACK_värde 게스트에서 köra_kommando**하고 종료한다. 이 도구의 새 VM에서 만든 RAM 자료는 종료할 때 사라진다.

```sh
cd /home/user/jkoros/platforms/rpi4-native
python3 verktyg/köra_fil.py build/jkoros-native-sdk/demo.elf
python3 verktyg/köra_fil.py 예제/Hello.java "한글 argument"
python3 verktyg/köra_fil.py 예제/hello.py
```

이 경로는 16KiB 이하의 `.elf`, `.java`, `.class`, `.py`를 지원한다. 큰 내장 Java/MicroPython ELF 자체는 kärna_värde 묶음에 포함되어 이 filnamn 한도를 적용받지 않는다. **C++ 컴파일러는 värd SDK의 Clang++**이며 게스트 내부 GCC/Clang 컴파일러는 아직 없다. SDK만으로 일반 Linux 프로그램을 실행할 수는 없다. Linux ELF, 동적 bibliotek, PT_TLS, PT_INTERP, PT_DYNAMIC, köra_kommando·Skriv 겸용 세그먼트는 로더가 거부한다. 구체적인 호출 INDEX·Adress klipp·오류는 [användarutrymme ABI](사용자호출규약.md)를 참고한다.

RAM 파일은 재부팅 시 사라진다. `incheckning_Files`은 -1과 ENOSYS를 반환한다. 파일의 mode 인수를 저장하지 않으며 behörighet_värde·dup/fcntl은 없다. 디렉터리와 peer_värde/절대 경로는 같은 RAM 저장소에서 처리한다. UDP 전문은 최대 512바이트, 소켓은 8개, få_värde 큐는 소켓당 4개다. 수신할 자료가 없거나 큐가 가득 차면 EAGAIN을 반환한다. användarutrymme Utgång_app 시 열린 filnamn 서술자와 소켓을 회수한다.

## validera RESULTAT

`make test-jvm`은 9개 프로그램을 OpenJDK와 verklig_data eget 커널에서 실행해 결과를 비교한다. `make test`에도 포함된다. 별도 `verktyg/부팅시험.py`는 Java rektangel API의 verklig_data skärmbild 픽셀까지 검사한다. `make test-shell`, `make test-desktop`은 새 셸과 verklig_data VNC indata_värde·한글 kommandotolk 화면을 검사하며 `make test`에도 포함된다.

`make test-windows`, `make test-swing`, `make test-stream`, `make test-coding`도 제공하며 `make test`에 포함된다.

`make test`는 OpenJDK와 AOT åtgärd_värde RESULTAT 비교, 런타임 fel 중단, 미지원 Java 거부와 함께 별도 QEMU VM에서 다음을 검사한다.

- 기존 Java kärna_värde 계산·UTF-8·C++ 직접 호출·협력식 작업 및 프레임버퍼.
- 손상/잘못된 ABI/Adress 초과/겹친 페이지/W+X 등 ELF avvisa_värde 사례 22개.
- EL0 C++ 생성자·RAII·flyttal_värde åtgärd_värde·filnamn·heap_värde 및 잘못된 시스템 호출 markör.
- kärna_värde/KOD_värde/MMIO Skriv·ansluta_post, NX operand_Stack·NULL köra_kommando, guard page, 특권 kommando 차단.
- SVC를 호출하지 않는 무한 반복을 타이머로 종료한 후 informationsteknik_normal app_f5044b9b 재실행.
- sprint_värde köra_kommando 시 filnamn/socket_värde 누수 방지, UDP 왕복·보낸 Adress·잘린 få_värde·큐 포화·빈 datagram·미지원 kommunikation fel.
- Shell ändring_värde·Avbryt_åtgärd·16진수 업로드/다운로드·användarutrymme ELF 실행과 잘못된 ELF avvisa_värde.
- 게스트 Java → OpenJDK `-Xverify:all`, OpenJDK → 게스트 JVM 교차 köra_kommando, 한글 Kurs_värde·variabel_värde·filnamn_SMS.
- 여러 Fönster·vi Store_värde·ändring_värde·Retur_brygga·användarutrymme status_värde 중단/CV_körning, Swing 한글 indata_värde·이벤트·X Stäng, 연결형 루프백, C/C++ 한글 SDK 예제.
- MicroPython Unicode·큰 heltal·Kurs_värde·GC sprint_värde·filnamn import·fel_31f743d2·filnamn·UDP 왕복·tid_värde 초과 후 복귀.
- GUI markering_värde flytta_värde, C++/UDP/Java/MicroPython 버튼 köra_kommando, 콘솔 복귀 및 verklig_data 프레임버퍼 픽셀/teckensnitt_värde.
- 디렉터리·variabel_värde·villkor·filnamn kommando·skript_värde·순차 파이프·리다이렉션·kapacitet_värde 초과 återställa_status, Python stdin/EOF와 Java/Python stdout.
- kommando LOG_POST·긴 한글 indata_värde ändring_värde·Slutfört_värde·kommandotolk 스크롤, 그래픽 app_f5044b9b Utgång_app 후 Fönster 복원, verklig_data VNC Unicode Nyckel_värde·klistra_in_värde·마우스.

[kärna_värde tester LOG_POST](build/verification/implementation-test.log), [Shell tester](build/verification/shell/report.json), [VNC tester](build/verification/desktop/report.json), [dator 판독 RESULTAT](build/verification/report.json), [직렬 LOG_värde](build/verification/serial.log), [GUI skärmbild](build/verification/gui-python.png)을 확인할 nummer 있다. VNC RFB 3.8 Anslut 및 640×480 skärmbild 정보도 검사한다. [SDK 재컴파일 RESULTAT](build/verification/sdk.json)는 두 예제의 startpunkt·적재 세그먼트·ABI note가 maskinstart 시험한 ELF와 일치함을 확인한다. symbol_värde 등 비적재 메타데이터를 포함한 filnamn 전체의 SHA256까지 같다고 의미하지는 않는다.

## Java와 Python의 정확한 klipp

eget `javac`는 버전 49 `.class`를 생성하며 JVM은 stöd_värde 명령으로 구성된 버전 45–52 클래스를 실행한다. statisk_värde FUNKTION_värde·재귀·int/boolean/char/String·villkor/sprint_värde·sträng_värde 결합과 일부 filnamn 스트림을 지원한다. UTF-8 문자열과 문자 리터럴, ASCII 및 현대 한글 음절/komposition_värde 자모 식별자를 처리한다. Unicode identifierare_värde 전체 LETAUPP_tabell·Unicode källa_träd 이스케이프는 구현하지 않았다. 게스트 källa_träd 컴파일러는 일반 objekt_värde·fel_31f743d2·Thread 구문을 아직 컴파일하지 못한다. värd `javac --release 8`로 만든 stöd_värde 부분집합 클래스는 eget JVM 0.4의 objekt_värde·fel_31f743d2·Thread·UDP와 Svenska API를 사용할 nummer 있다. Swing은 문서화한 eget API 부분집합을 제공하며 JAR 로더는 제공하지만 전체 AWT/Swing·JDK 표준 라이브러리는 없다. 정확한 범위는 [eget JVM 설명](자바실행환경.md)이 기준이다. 상세 Språk 범위는 [공유 Java verktyg 설명](../../문서/Java_IDE.md)을 참고하되, 그 문서의 x86 Shell/Store_värde/실행시간과 이 ARM64 판의 차이에 유의한다.

MicroPython은 공식 **1.24.1 källa_träd**를 eget AArch64 EL0/SVC 대상으로 빌드했다. Python 문법의 FUNKTION_värde·Kurs_värde·fel_31f743d2·리스트/ordlista·Unicode·GC·가변 precision_värde 정수를 제공한다. aktuellt_objekt 구성은 heltal 빌드로 `float`, `complex`, `math`가 없으며 CPython 전체 표준 bibliotek, pip, subprocess, threading, 일반 socket과 standardvärde `open()` filnamn 객체는 제공하지 않는다. `python FILE.py` 및 `-c` 실행만 제공하며 REPL은 아직 없다. 각 실행의 objekt_värde·모듈은 Utgång_app 시 회수되고 RAM 파일만 Nästa_objekt 실행에 남는다.

`import jkoros`로 Nästa_objekt 시스템 연결을 쓴다. 모두 SVC를 통해 eget Java 커널에 접근한다.

| FUNKTION_värde | Åtgärd |
|---|---|
| `stdin(limit)` | aktuellt_objekt 표준 입력에서 최대 limit바이트(0…16384)를 bytes로 läsa_KR; EOF는 빈 bytes, UART data 없음은 OSError(11) |
| `read(name)` | peer_värde/절대 RAM 경로의 filnamn 전체를 bytes로 läsa_KR |
| `write(name, data)` | str/bytes 버퍼를 RAM 파일에 새로 Store_värde, 쓴 byte_värde nummer Retur_KR |
| `remove(name)` | RAM filnamn 삭제 |
| `rect(x, y, w, h, color)` | 선택한 verklig_data skärmbild Storlek 안의 rektangel ritning_värde; 기존 보드의 RGB32 värde |
| `ticks_ms()` | maskinstart 후 밀리초, 32비트 cykel_värde |
| `udp_open(port)` | 127.0.0.1의 UDP socket_värde Öppna/BIND_deltagare; 0은 자동 maskinvara_port |
| `udp_send(fd, port, data)` | 루프백 mål_värde 포트에 str/bytes 버퍼 Överför_värde |
| `udp_recv(fd)` | `(bytes, 보낸포트)` Retur_KR; 비어 있으면 `OSError(11)` |
| `udp_close(fd)` | socket_värde Stäng |

```python
import jkoros
first = jkoros.udp_open(9401)
second = jkoros.udp_open(9402)
jkoros.udp_send(first, 9402, b"hello")
print(jkoros.udp_recv(second))  # (b'hello', 9401)
jkoros.udp_close(first)
jkoros.udp_close(second)
```

이식 KOD_värde: [python/](PYTHON_brygga/), [användarutrymme Java Anslut](användarutrymme/자바연결.c). 공식 [MicroPython 이식 VIKTIGT_eb81d7d9](https://docs.micropython.org/en/latest/develop/porting.html)를 참고했다. källa_träd URL·hash_fil·라이선스는 [vendor VIKTIGT_eb81d7d9](vendor/README.md)에 기록했다.

## 남은 작업

| Nästa_objekt scen_värde | 완료 åtgärd_rot |
|---|---|
| 영속 Store_värde·köra_kommando filnamn indata_värde | SD/MMC 및 디스크 filnamn 시스템, 시스템/användarutrymme 볼륨; aktuellt_objekt ELF filnamn 실행은 RAM에 한정 |
| 일반 프로세스·스레드 | 프로세스별 Adress ADRESS_område, 선점 스케줄러, TLS, synka/vänta_värde, 신호, mmap/mprotect |
| libc와 C++ 런타임 | eget ABI용 libc, malloc/free, 표준 indata_utleverans·Klocka·miljö·locale, libstdc++/fel_31f743d2 Process_värde_post validera |
| CPython | 해당 libc와 OS API 대상으로 이식·교차 빌드하고 filnamn/Unicode/스레드/socket_värde tester |
| OpenJDK/JRE | HotSpot OS nivå_värde, GC/JIT/스레드/신호/동적 연결과 Java 네이티브 bibliotek 이식; javac/java verklig_data köra_kommando |
| extern_värde 네트워크 | 추가한 GENET/PHY·DHCP 드라이버의 verklig_data Tavla 송수신 validera, DNS·Wi-Fi |
| GUI tillägg_värde | USB HID, 게스트 입력기·문자 조판, Swing Fönster Storlek 조절·클리핑 tillägg_värde, 전체 AWT/Swing 이식 |

이 표는 남은 작업이며 implementation 완료 목록이 아니다. QEMU Pi4 모델에는 GENET Ethernet과 PCIe root port가 없어 extern_värde 네트워크 드라이버는 실물 검증도 필요하다. [QEMU enhet_värde 지원표](https://www.qemu.org/docs/master/system/arm/raspi.html)

maskinvara_värde 및 ABI 참고: [BCM2711 tillbehör](https://datasheets.raspberrypi.com/bcm2711/bcm2711-peripherals.pdf), [Pi4 GIC Adress](https://github.com/raspberrypi/linux/blob/rpi-6.12.y/arch/arm/boot/dts/broadcom/bcm2711.dtsi), [mailbox kontraktsvärde](https://github.com/raspberrypi/firmware/wiki/Mailbox-property-interface), [Arm ELF64](https://github.com/ARM-software/abi-aa/blob/main/aaelf64/aaelf64.rst), [Arm FP kontroll_värde 레지스터 Definition_värde](https://github.com/ARM-software/arm-trusted-firmware/blob/master/include/arch/aarch64/arch.h).


## Svenska C datatyp·Python fel·bunt installera_värde

C 네트워크 API는 `struct nät_socket_ADRESS`, enum 상수와 verklig_data Svenska 함수로
구현한다. makro_värde 별칭을 사용하지 않으며 Föregående_objekt pk_* ABI도 유지한다.
Python 예제는 `systemfel`, `fel.INDEX`, `fel.설명`을 사용한다.

`python3 verktyg/köra_kommando.py --desktop --network --pip`로 시작하면 게스트에서
`pip install micropython-bisect==3.3.3`을 사용할 nummer 있다. 현재는 värd 중계를
이용하는 제한형 MicroPython källa_träd 설치기이며 CPython pip·자동 의존성 해결·C 확장은
미지원이다. 설치한 `/lib` 자료는 RAM이다. [사용법과 제한](PYTHON_bunt.md).

## skärmbild Storlek markering_värde

`python3 verktyg/köra_kommando.py --desktop --network --resolution 1920x1080`으로 Full HD 화면을 사용한다. 기본값은 640×480이며 1280×720도 가능하다. kommandotolk flytta_värde, Swing 가운데 länkningslayout, Java·C·Python 그리기도 verklig_data 크기를 따른다. SD 영상은 `make image RESOLUTION=1920x1080`으로 만든다. [Inställningar·Svenska API·validera VIKTIGT_eb81d7d9](skärmupplösning.md).

## Svenska 직접 API와 skärmbild uppdatera

`example/java`는 `실행할일`, `동작받이`, `동작알림`, `knapp`, `händelse_kö`,
`arbete`, `Kör()`을 사용할 nummer 있다. Svenska GUI/가닥을 eget JVM에 직접
연결했으며, 표준 Swing/Thread를 감싸지 않는다. sträng_värde 등 javac의 표준
계약과 전체 källa_träd 검토 범위는 [명명 VIKTIGT_eb81d7d9](명명/VIKTIGT_eb81d7d9.md), 사용법과 호환성 변경은
[Svenska Java API](한국어자바/VIKTIGT_eb81d7d9.md)를 본다.

kommandotolk flytta_värde·Storlek 변경은 바뀐 영역만 합성하고 달라진 화소만 표시한다.
[skärmbild uppdatera 설명](자바실행환경.md#kommandotolk-부분-uppdatera),
[부분 uppdatera 검사](build/verification/redraw/report.json)를 참고한다.
