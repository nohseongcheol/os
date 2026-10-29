# Raspberry Pi 4 자체 Java mkpụrụobī_kọmpùta_valuu — òjìàrụ mee_nnyemiwu 기반

현재 자체 코드의 COSL 상업 ọnọdụ, 제3자 고지 및 LGPL 재연결 자료는 [COSL 배포 GỤ̀ỌM_eb81d7d9](COSL배포안내.md)를 참고한다. ngbanwụ_moòdù 전 GPL 구성의 판단은 [이전 라이선스 검토](ìwuikikere_Nyocha.md)에 기록했다.

한국어 통신·예외 사용법은 [한국어 Java API](한국어자바/GỤ̀ỌM_eb81d7d9.md), ọrụ_valuu·변수·Faịlụ 이름의 변경과 어원 근거는 [명명 GỤ̀ỌM_eb81d7d9](명명/GỤ̀ỌM_eb81d7d9.md)를 참고한다.

Linux 없이 부팅하는 자체 AArch64 커널이다. Java AOT mkpụrụobī_kọmpùta_valuu 위에 **ahịrị_nnyemiwu nkọwannyemiwu, 게스트 Java 컴파일러·JVM, MicroPython, EL0 C++ mee_nnyemiwu, Faịlụ·UDP 루프백 시스템 호출, 여러 한글 GUI 터미널·vi òdezi·Swing 부분집합**을 제공한다. 커널의 Faịlụ datà/정책·루프백 dògharịa_valuu·nkọwannyemiwu 상태는 Java, 화면 합성·pel gbanwèe_valuu·nrụaka·클리핑도 Java로 구현하며, CPU/MMU/njìarụ_valuu 경계와 터미널·mkpụrụedemede_valuu 그리기 연결은 C와 어셈블리다.

**전체 JDK/JRE·CPython·표준 C++ 런타임·Swing 이식은 아직 완료되지 않았다.** 기존 [ARM64 Linux 실행판](../rpi4/README.md)의 OpenJDK/Python 패키지를 이 자체 커널에 탑재했다고 표시하지 않는다.

새로운 게스트 `cc`/`jaot`, JAR 직접 mee_nnyemiwu, lwIP TCP/UDP와 FTP는 [FTP·C·JAR·AOT 매뉴얼](파일전송과번역.md)을 참고한다. 게스트 SSH·VNC와 Pi4 GENET/PHY·DHCP 드라이버를 추가했다. **SSH·VNC는 QEMU에서 검증하며, 실물 Pi4의 èjìrìwayàrụ_valuu 송수신은 아직 미검증이다.** mee_nnyemiwu·njikọ_e05f319b·okwuntughe_valuu 확인은 [외부 njikọ_e05f319b GỤ̀ỌM_eb81d7d9](외부접속안내.md)에 정리했다.

셸은 EL1 mkpụrụobī_kọmpùta_valuu, `java` 등 òjìàrụ mee_nnyemiwu 파일은 EL0에서 실행한다.
`ps`·`top`의 표시와 제한, QEMU 네트워크 mee_nnyemiwu·njikọ_e05f319b 방법 및 ǹdịnezie_datà 검증은
[mee_nnyemiwu 계층과 외부 통신 점검](실행계층과외부통신점검.md)을 참고한다.

ELF는 확장자가 아닌 ǹdịnezie_datà mee_nnyemiwu 형식으로 검사한다. `./인사`처럼 확장자 없이 실행하며, 제한된 Linux ARM64 adịmgbanwò_valuu ELF는 `run --linux ọbọakwụkwọ_akara_ahà_SMS`으로 실행한다. [ELF·Linux ABI nkwado_valuu 범위와 동일 바이너리 시험](실행파일규약.md).

GUI와 네트워크는 `python3 Ngwaọrụ/mee_nnyemiwu.py --desktop --network`로 함께 사용한다. Java·C·Python의 한국어 예제 13개는 [jkoros/example](../../example/README.md)에 있으며, **게스트 부팅 시 `/example/java`, `/example/c`, `/example/python`에 자동으로 준비된다.** `example java|c|python`으로 지운 예제를 복원할 수 있다. Remmina에서 **F9/Shift+Space/한·영 ọtụgwo_valuu**로 `[EN]`↔`[KO]` 두벌식을 전환한다(`help ko`). `make test-examples`는 같은 GUI VM에서 FTP·ǹdịnezie_datà TCP/UDP·Faịlụ baịtị_valuu·그래픽 픽셀을 검증한다.

게스트에서 `cd /example/java` 후 `java 창예제`로 한국어 Swing 예제를 실행한다. 터미널 모서리에 마우스를 대고 **왼쪽 버튼으로 끌면 크기가 바뀐다**. `terminal size`는 현재 ọgbàràogō_valuu·ihendekọta_valuu 수를 보여 준다.

## 현재 nkwado_valuu ntipanye

| 기능 | 구현·시험한 ntipanye | 아직 미지원 |
|---|---|---|
| 부팅 | Pi4 AArch64 EL1, UART, SD용 wue_foto, QEMU raspi4b 부팅 | ǹdịnezie_datà Pi4 보드에서의 펌웨어 부팅 시험 |
| Java mkpụrụobī_kọmpùta_valuu | adịmgbanwò_valuu Java 부분집합 → freestanding C → AArch64 AOT | 전체 Java ihe_valuu/예외/GC/JVM/표준 ọbaakwụkwọ |
| Java 개발 Ngwaọrụ | 게스트 자체 `javac`/`java`, JVM 0.4/JAR: 다중 klaàsị_valuu·ihe_valuu·상속·예외·GC·일부 컬렉션·Thread·IPv4 Socket/UDP·Swing 일부 API, 한국어 ọbaakwụkwọ. 게스트 컴파일러는 adịmgbanwò_valuu Java 부분집합 | 전체 JDK/JRE·HotSpot·Java SE·임의의 모든 JAR·AWT/Swing 전체 |
| Python | ǹdịnezie_datà MicroPython 1.24.1 EL0 이식, ebensìbịa_èsèrèsè_osisi wue_ebensìbịa/mee_nnyemiwu, klaàsị_valuu·예외·GC·큰 ọnụọgụ_nzùrùòkè·Unicode·Faịlụ·UDP/화면 Banye | CPython, pip, C mgbatị_valuu, 부동소수점, 일반 OS/스레드/소켓 모듈, kèmmekọrịta REPL |
| nkọwannyemiwu | UTF-8 dezìmà_valuu·ndekọ_NDEKỌ·완성, 디렉터리·Faịlụ Ntiiwu, 변수·ọnọdụ·Èdèrède_ntụziaka_valuu, 16 KiB 순차 파이프·리다이렉션, ELF mee_nnyemiwu | 전체 POSIX sh/Bash, 작업 njizi_valuu·동시 프로세스·PTY |
| C/AOT wue_ebensìbịa | 게스트 TinyCC 및 adịmgbanwò_valuu Java 부분집합 `jaot` → 자체 ARM64 ELF | 전체 libc·모든 Java klaàsị_valuu AOT |
| C++ | 독립 ELF64를 EL0에서 mee_nnyemiwu; adịmgbanwò_valuu 생성자, RAII 소멸자, FP/SIMD, 한국어 Faịlụ/루프백 호출 | libc/libstdc++, STL, C++ 예외·RTTI·동적 Banye |
| òjìàrụ nchedo_valuu | 4 KiB 페이지, 코드 RX/datà RW·NX, mkpụrụobī_kọmpùta_valuu·MMIO 차단, guard page, 잘못된 nrụaka 검사 | 다중 òjìàrụ ikikere_valuu, 일반 프로세스/스레드 스케줄러 |
| mee_nnyemiwu 시간 제한 | GIC-400 타이머로 무한 memmekwa_valuu pụọ_app; kèmmekọrịta 입력 대기는 기한 mèkwa_ọhụrụ, 터미널별 EL0 app_f5044b9b 중단·재개 | 일반적인 선점형 다중작업. 긴 mkpụrụobī_kọmpùta_valuu 호출 도중에는 종료가 지연될 수 있음 |
| Faịlụ | Java RAM Faịlụ 64개 × 16384바이트, 루트를 포함한 디렉터리 16개, ibè_valuu/절대 ụzọ_ozi 63바이트, 서술자 16개 | ikikere_valuu, 디스크/SD 영속 Store_valuu |
| 네트워크 | lwIP IPv4 TCP/UDP/ARP/ICMP, SLIP, GENET/PHY·DHCP 구현, 게스트 FTP·SSH·VNC | GENET 실물 mee_ịbanihe, Wi-Fi, DNS, 일반 TLS 소켓, RDP |
| GUI | 최대 네 터미널 windò, ebenhọrọ_valuu·gàa_valuu·X Mechie, 한글 ọnụndèe_valuu, Swing 부분집합; 게스트 VNC 화면·입력·두벌식 | 실물 USB 입력, 전체 AWT/Swing·Java2D·windò 관리 정책 |
| 작업 treèd_valuu | mkpụrụobī_kọmpùta_valuu 작업 2개와 주 작업; JVM 내부 treèd_valuu 최대 4개, start/join/yield·synchronized | pthread, SMP, Java Thread 전체 API |
| 다국어 | UTF-16 리터럴→UTF-8 UART, 한글·일본어·아랍어·이모지, UTF-8 ọbọakwụkwọ_akara_ahà_SMS/전문 | GUI의 일반 다국어 조판 |

mee_nnyemiwu 버튼 화면은 5×7 영문 글꼴을 쓰며, 터미널 창은 Noto CJK/DejaVu에서 생성한 한글·Unicode 비트맵 글꼴을 쓴다. UART와 ǹdịnezie_datà 프레임버퍼의 한글 표시를 시험한다. 루프백은 동일 mkpụrụobī_kọmpùta_valuu 내부의 전문 전달이며 IP 패킷을 Ethernet으로 내보내는 드라이버가 아니다. 바깥 IPv4는 lwIP TCP/UDP 스택으로 보조 UART SLIP 경로를 사용한다. `python3 Ngwaọrụ/mee_nnyemiwu.py --network`로 QEMU NAT를 연결하고 `ftpd start`로 서비스를 시작한다.

Java의 정확한 API·문법·mee_nnyemiwu 제한과 한국어 사용법은 [자체 JVM과 한국어 ọbaakwụkwọ](자바실행환경.md)에 정리했다. klaàsị_valuu Faịlụ/JAR 배포는 [한국어자바](한국어자바) 소스에서 재현한다. 기존 Linux판 `한국어.자바`와 별도인 `한국어.자체` 패키지다.

**vi·여러 windò·Swing·한글 Java/Python/C/C++·posix-kor 예제는 [한글 개발 매뉴얼](개발안내.md)에 정리했다.**

GUI 터미널 mee_nnyemiwu·단축키·nkọwannyemiwu Ntiiwu·제한은 [셸과 터미널 사용법](셸과터미널.md)에 정리했다.

## 현재 컴퓨터에서 mee_nnyemiwu

```sh
cd /home/user/jkoros/platforms/rpi4-native
make test
make run
```

pụọ_app: **Ctrl+A 다음 X**. 게스트 C/AOT Ngwaọrụ 빌드에는 `make rpi-prepare`로 준비한 ARM64 SDK 헤더와 libgcc 산술 보조 함수도 필요하다. libc나 Linux 커널을 게스트에 넣는 것은 아니다. usu 도구는 JDK 11 이상, Python 3.6 이상, Clang/Clang++, AArch64 GNU binutils, Make, `libnewlib-dev` 헤더다. MicroPython은 `/usr/include/newlib` 헤더를 사용하며 다른 위치는 `NEWLIB_INCLUDE`로 지정한다. newlib 런타임을 이식·링크한 것은 아니다. 컴파일러 의미 비교에는 GCC/UBSan도 사용한다. 기존 `../rpi4/build/host`의 QEMU 11.0.3이 있으면 이용하며, 그렇지 않으면 PATH의 QEMU를 사용한다. `QEMU_AARCH64=/절대/ụzọ_ozi/qemu-system-aarch64`로 지정할 수도 있다. `raspi4b` nkwado_valuu 여부를 확인한 후 실행한다.

명령은 **Enter를 눌러 mee_nnyemiwu**한다. 기존 한 mkpụrụedemede_valuu 명령도 Enter가 필요하다.

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

| Ntiiwu | mmèm |
|---|---|
| `help` / `info` | Ntiiwu·ǹdịnezie_datà 구현 ọnọdụ_valuu |
| `ls` / `cat FILE` / `rm FILE` | RAM Faịlụ ndebà_ndepụta·ndịnà_valuu·삭제 |
| `vi FILE` | òjìàrụ 영역 vi 부분집합, 한글 dezìmà_valuu·Store_valuu·검색·되돌리기 |
| `edit FILE` | Faịlụ 전체를 새로 입력; 단독 `.` 줄로 Store_valuu, Ctrl-C로 kàgbuo_àrụmọrụ |
| `javac FILE.java` / `java CLASS [ARGS]` | 자체 제한형 Java wue_ebensìbịa·mee_nnyemiwu |
| `python FILE.py [ARGS]` / `python -c 'CODE'` | MicroPython wue_ebensìbịa·mee_nnyemiwu |
| `load FILE` / `hex FILE` | 16진수 바이너리 입력/출력; 입력은 단독 `.` 줄로 Store_valuu |
| `run FILE.elf [ARGS]` / `run cpp` | 업로드한 자체 ABI ELF / 내장 C++ 예제 |
| `net test` / `tasks` / `selftest` | UDP 루프백 / 협력식 작업 / EL0 nchedo_valuu 시험 |
| `gui` / `terminal` | mee_nnyemiwu 화면 / 한글 GUI 터미널; F12로 터미널 Mepee·Mechie |
| `samples` | 삭제한 Ngwa_ihe_dịadị 예제 nnweghàchi_ọnọdụ; 기존 파일은 보존 |

예를 들어 `edit 인사.java`를 입력한 다음 아래 소스를 입력한다.

```java
public class 인사 { public static void main(String[] args) { int valuu = 7; System.out.println("한글=" + valuu); } }
```

그다음 단독 `.` 줄로 저장하고 `javac 인사.java`, `java 인사`를 실행한다. 편집기는 기존 파일에 커서를 이동하는 방식이 아니라 전체 교체 방식이다. kàgbuo_àrụmọrụ·잘못된 16진수·용량 초과는 원본을 보존한다. 줄은 4096바이트, 파일은 16384바이트, mee_nnyemiwu 인수는 최대 8개·각각 UTF-8 255바이트다. 일반 Ntiiwu 인수는 최대 32개다. 따옴표·백슬래시·nkọwannyemiwu 변수·파이프·리다이렉션 범위는 [nkọwannyemiwu 설명](셸과터미널.md)을 참고한다.

GUI 터미널은 다음과 같이 실행하고 Remmina에서 **VNC**, àdreèsì **127.0.0.1:5902**로 연결한다. 키보드·한글 Unicode 입력·명시적 nyàpanye_valuu·mee_nnyemiwu 버튼의 마우스 클릭을 QEMU 도구가 UART에 전달한다.

```sh
make desktop
# GUI + 네트워크: python3 Ngwaọrụ/mee_nnyemiwu.py --desktop --network
# 다른 ngwaike_pọọt: python3 Ngwaọrụ/mee_nnyemiwu.py --desktop --port 5903
```

종료는 실행한 usu 터미널에서 Ctrl+C다. 기존 `python3 Ngwaọrụ/mee_nnyemiwu.py --vnc 127.0.0.1:2`는 화면 보기와 별도 UART 입력을 유지한다. `make run`은 일반 UART 셸이다. ǹdịnezie_datà Pi4 USB 입력기는 아직 없으며, VNC Banye 도구는 QEMU 시험용이다.

GUI의 다섯 버튼은 ǹdịnezie_datà C++/UDP ELF mee_nnyemiwu, `Hello.java` wue_ebensìbịa 후 JVM mee_nnyemiwu, `hello.py` mee_nnyemiwu, GUI 터미널 열기를 수행한다. 한 번에 한 프로그램이 CPU에서 실행되며 일반 실행에는 약 2초 기한이 있다. vi·Swing은 kèmmekọrịta 대기에서 기한을 갱신하고 다른 터미널로 전환할 때 memọrị_datà·CPU 문맥을 보관한다. nkọwannyemiwu·편집기에서 입력을 기다리는 시간에는 이 제한이 적용되지 않는다.

## ǹdịnezie_datà 산출물과 Pi4 SD wue_foto

```sh
make image   # mkpụrụobī_kọmpùta_valuu, SD wue_foto, 부팅 ZIP, 사용자용 SDK
make sdk     # SDK만 다시 생성
```

| ụzọ_ozi | 용도 |
|---|---|
| `build/kernel8.img` | 자체 mkpụrụobī_kọmpùta_valuu 기계어, 적재 àdreèsì 0x80000 |
| `build/kernel.elf`, `kernel.map` | mkpụrụobī_kọmpùta_valuu adimara_valuu·Njikọ_Nhàzi |
| `build/user/demo.elf` | òjìàrụ moòdù_valuu C++ Faịlụ/힙/실수/그래픽 예제 |
| `build/user/network.elf` | òjìàrụ moòdù_valuu C++ UDP 루프백 예제 |
| `build/user/java-tools.elf` | 자체 Java 부분집합 컴파일러/JVM, 전체 JDK/JRE 아님 |
| `dist/jkoros-native-korean.jar` | usu javac용 한국어 API klaàsị_valuu; 같은 클래스가 자체 JVM에도 내장됨 |
| `dist/jkoros-native-korean-sources.zip` | 한국어 API Java ebensìbịa |
| `build/user/vi.elf` | 자체 UTF-8 vi Ntiiwu 부분집합 òdezi |
| `build/user/python.elf` | 자체 ABI용 MicroPython 1.24.1, CPython 아님 |
| `build/user/fault.elf` | 의도적 침범/무한 반복을 수행하는 nchedo_valuu 시험 전용 |
| `build/libposix-kor-arm64.a` | **mkpụrụobī_kọmpùta_valuu 내부**에서 Java Faịlụ 구현을 직접 부르는 기존 Banye |
| `build/libposix-kor-user.a` | **EL0 òjìàrụ app_f5044b9b**에서 SVC로 Faịlụ/루프백을 호출하는 새 Banye |
| `dist/jkoros-native-rpi4.img` | 128 MiB MBR/FAT32 SD wue_foto |
| `dist/jkoros-native-rpi4-boot.zip` | FAT32 부팅 파티션에 복사할 Faịlụ otu_valuu |
| `dist/jkoros-native-aarch64-sdk.tar.gz` | 사용자용 헤더·Bido 코드·ọbaakwụkwọ·링커 Èdèrède_ntụziaka_valuu·예제 |
| `dist/manifest.json`, `build/build.json` | SHA256과 ǹdịnezie_datà nkwado_valuu ọnọdụ_valuu |

이미지는 확인된 공식 Pi 부팅 묶음에서 `start4.elf`, `fixup4.dat`, Pi4 DTB와 disable-bt overlay를 가져온다. Linux kernel/initramfs/rootfs는 넣지 않는다. 펌웨어·MicroPython·터미널 ọnụndèe_valuu 라이선스와 ọnụndèe_valuu 출처 해시도 동봉한다. Faịlụ 생성 스크립트는 물리 디스크에 기록하지 않는다.

예비 microSD에 wue_foto ndekọ_NDEKỌ 도구로 `.img`를 기록하거나 FAT32 부팅 파티션 최상위에 ZIP 내용을 푼다. wue_foto 기록은 선택한 카드의 기존 내용을 지우므로 대상을 확인한다. Pi4 Ngwa_ihe_dịadị EEPROM SD 부팅을 전제로 한다. UART는 **3.3V TTL, 115200 8N1**, GPIO14/TXD(8번)→어댑터 RX, GPIO15/RXD(10번)→TX, GND(6번) 연결이다. GPIO에 5V 신호를 연결하지 않는다.

**실물 Pi4 부팅은 미검증이다.** QEMU `-kernel`은 SD의 VideoCore 펌웨어를 실행하지 않고 커널을 직접 적재한다. SD Faịlụ 구성·mkpụrụobī_kọmpùta_valuu 체크섬 검사와 물리 보드 부팅 검증은 별개다. MMU 사용 전에는 펌웨어의 캐시/MMU가 꺼져 있고 EL1 또는 EL2로 진입하는 통상 부팅 조건을 전제로 한다. 세 보조 코어는 대기시키며 한 코어만 사용한다.

## C++와 한국어 API 사용

SDK를 풀고 호스트에서 컴파일한다.

```sh
tar -xzf dist/jkoros-native-aarch64-sdk.tar.gz -C build
cd build/jkoros-native-sdk
python3 compile.py examples/파일예제.cpp -o demo.elf
python3 compile.py examples/통신예제.cpp -o network.elf
```

진입점은 `extern "C" int Mbido_òjìàrụ_app(int)`이다. òjìàrụ C++는 FP/SIMD를 사용할 수 있다. mkpụrụobī_kọmpùta_valuu C/Java AOT는 일반 레지스터만 사용하므로 예외 ùsòrò_valuu_ndebà 중 òjìàrụ FP 상태를 건드리지 않는다. òjìàrụ ndebà_akara_valuu 시 FP 상태를 초기화하고 mkpụrụobī_kọmpùta_valuu 복귀에 필요한 상태를 보존한다.

```cpp
#include "파일규약.h"
extern "C" int Mbido_òjìàrụ_app(int) {
    int Faịlụ = mepee_ọbọakwụkwọ("인사.txt", gụọ_dèe | 없으면만들기 | 내용비우기, 0600);
    if (Faịlụ < 0) return 1;
    const char ndịnà_valuu[] = "안녕하세요";
    int 결과 = dee_ọbọakwụkwọ_datà(Faịlụ, ndịnà_valuu, sizeof(ndịnà_valuu) - 1);
    mmechi_ọbọakwụkwọ(Faịlụ);
    return 결과 == sizeof(ndịnà_valuu) - 1 ? 0 : 2;
}
```

[Faịlụ 예제](òjìàrụ/파일예제.cpp)와 [통신 예제](òjìàrụ/통신예제.cpp)가 ǹdịnezie_datà 부팅 시험 대상이다. `파일규약.h`의 이름은 커널용/사용자용 모두 같지만 **링크하는 라이브러리가 다르다**. 사용자용은 `svc #0`으로 호출하고 Faịlụ ùsòrò_valuu_ndebà 및 루프백 전달은 Java 커널에서 실행한다. `통신규약.h`의 소켓 함수는 현재 사용자용 라이브러리에 구현돼 있다.

새 프로그램은 mkpụrụobī_kọmpùta_valuu 재빌드 없이 `load FILE.elf`와 `run FILE.elf`로 실행한다. 호스트에서 다음 도구를 사용하면 **새 QEMU를 부팅해 업로드한 ǹdịnezie_datà 바이트를 재확인한 Àzụ_valuu 게스트에서 mee_nnyemiwu**하고 종료한다. 이 도구의 새 VM에서 만든 RAM 자료는 종료할 때 사라진다.

```sh
cd /home/user/jkoros/platforms/rpi4-native
python3 Ngwaọrụ/mee_ọbọakwụkwọ.py build/jkoros-native-sdk/demo.elf
python3 Ngwaọrụ/mee_ọbọakwụkwọ.py 예제/Hello.java "한글 인수"
python3 Ngwaọrụ/mee_ọbọakwụkwọ.py 예제/hello.py
```

이 경로는 16KiB 이하의 `.elf`, `.java`, `.class`, `.py`를 지원한다. 큰 내장 Java/MicroPython ELF 자체는 mkpụrụobī_kọmpùta_valuu 묶음에 포함되어 이 Faịlụ 한도를 적용받지 않는다. **C++ 컴파일러는 usu SDK의 Clang++**이며 게스트 내부 GCC/Clang 컴파일러는 아직 없다. SDK만으로 일반 Linux 프로그램을 실행할 수는 없다. Linux ELF, 동적 ọbaakwụkwọ, PT_TLS, PT_INTERP, PT_DYNAMIC, mee_nnyemiwu·Chekwaa_ozi 겸용 세그먼트는 로더가 거부한다. 구체적인 호출 indèks·àdreèsì ntipanye·오류는 [òjìàrụ ABI](사용자호출규약.md)를 참고한다.

RAM 파일은 재부팅 시 사라진다. `파일저장확정`은 -1과 ENOSYS를 반환한다. 파일의 mode 인수를 저장하지 않으며 ikikere_valuu·dup/fcntl은 없다. 디렉터리와 ibè_valuu/절대 경로는 같은 RAM 저장소에서 처리한다. UDP 전문은 최대 512바이트, 소켓은 8개, 수신 큐는 소켓당 4개다. 수신할 자료가 없거나 큐가 가득 차면 EAGAIN을 반환한다. òjìàrụ pụọ_app 시 열린 Faịlụ 서술자와 소켓을 회수한다.

## mee_ịbanihe 결과

`make test-jvm`은 9개 프로그램을 OpenJDK와 ǹdịnezie_datà 자체 커널에서 실행해 결과를 비교한다. `make test`에도 포함된다. 별도 `Ngwaọrụ/부팅시험.py`는 Java 사각형 API의 ǹdịnezie_datà 화면 픽셀까지 검사한다. `make test-shell`, `make test-desktop`은 새 셸과 ǹdịnezie_datà VNC 입력·한글 터미널 화면을 검사하며 `make test`에도 포함된다.

`make test-windows`, `make test-swing`, `make test-stream`, `make test-coding`도 제공하며 `make test`에 포함된다.

`make test`는 OpenJDK와 AOT àrụmọrụ_valuu 결과 비교, 런타임 mmejọ 중단, 미지원 Java 거부와 함께 별도 QEMU VM에서 다음을 검사한다.

- 기존 Java mkpụrụobī_kọmpùta_valuu 계산·UTF-8·C++ 직접 호출·협력식 작업 및 프레임버퍼.
- 손상/잘못된 ABI/àdreèsì 초과/겹친 페이지/W+X 등 ELF 거부 사례 22개.
- EL0 C++ 생성자·RAII·실수 àrụmọrụ_valuu·Faịlụ·힙 및 잘못된 시스템 호출 nrụaka.
- mkpụrụobī_kọmpùta_valuu/코드/MMIO Chekwaa_ozi·òhèrè_ndebà, NX 스택·NULL mee_nnyemiwu, guard page, 특권 Ntiiwu 차단.
- SVC를 호출하지 않는 무한 반복을 타이머로 종료한 후 정상 app_f5044b9b 재실행.
- memmekwa_valuu mee_nnyemiwu 시 Faịlụ/소켓 누수 방지, UDP 왕복·보낸 àdreèsì·잘린 수신·큐 포화·빈 전문·미지원 통신 mmejọ.
- nkọwannyemiwu dezìmà_valuu·kàgbuo_àrụmọrụ·16진수 업로드/다운로드·òjìàrụ ELF 실행과 잘못된 ELF 거부.
- 게스트 Java → OpenJDK `-Xverify:all`, OpenJDK → 게스트 JVM 교차 mee_nnyemiwu, 한글 klaàsị_valuu·변수·ọbọakwụkwọ_akara_ahà_SMS.
- 여러 windò·vi Store_valuu·dezìmà_valuu·되돌림·òjìàrụ ọnọdụ_valuu 중단/재개, Swing 한글 입력·이벤트·X Mechie, 연결형 루프백, C/C++ 한글 SDK 예제.
- MicroPython Unicode·큰 ọnụọgụ_nzùrùòkè·klaàsị_valuu·GC memmekwa_valuu·Faịlụ import·예외·Faịlụ·UDP 왕복·시간 초과 후 복귀.
- GUI ebenhọrọ_valuu gàa_valuu, C++/UDP/Java/MicroPython 버튼 mee_nnyemiwu, 콘솔 복귀 및 ǹdịnezie_datà 프레임버퍼 픽셀/ọnụndèe_valuu.
- 디렉터리·변수·ọnọdụ·Faịlụ Ntiiwu·Èdèrède_ntụziaka_valuu·순차 파이프·리다이렉션·용량 초과 nnweghàchi_ọnọdụ, Python stdin/EOF와 Java/Python stdout.
- Ntiiwu ndekọ_NDEKỌ·긴 한글 입력 dezìmà_valuu·완성·터미널 스크롤, 그래픽 app_f5044b9b pụọ_app 후 windò 복원, ǹdịnezie_datà VNC Unicode ọtụgwo_valuu·nyàpanye_valuu·마우스.

[mkpụrụobī_kọmpùta_valuu 시험 ndekọ_NDEKỌ](build/verification/implementation-test.log), [nkọwannyemiwu 시험](build/verification/shell/report.json), [VNC 시험](build/verification/desktop/report.json), [ngwa_komputa 판독 결과](build/verification/report.json), [직렬 ndekọ_valuu](build/verification/serial.log), [GUI 화면](build/verification/gui-python.png)을 확인할 수 있다. VNC RFB 3.8 Banye 및 640×480 화면 정보도 검사한다. [SDK 재컴파일 결과](build/verification/sdk.json)는 두 예제의 ndebà_akara·적재 세그먼트·ABI note가 부팅 시험한 ELF와 일치함을 확인한다. adimara_valuu 등 비적재 메타데이터를 포함한 Faịlụ 전체의 SHA256까지 같다고 의미하지는 않는다.

## Java와 Python의 정확한 ntipanye

자체 `javac`는 버전 49 `.class`를 생성하며 JVM은 nkwado_valuu 명령으로 구성된 버전 45–52 클래스를 실행한다. adịmgbanwò_valuu ọrụ_valuu·재귀·int/boolean/char/String·ọnọdụ/memmekwa_valuu·ùsòròokwū_valuu 결합과 일부 Faịlụ 스트림을 지원한다. UTF-8 문자열과 문자 리터럴, ASCII 및 현대 한글 음절/조합 자모 식별자를 처리한다. Unicode ihe_nkọwapụta_valuu 전체 표·Unicode ebensìbịa_èsèrèsè_osisi 이스케이프는 구현하지 않았다. 게스트 ebensìbịa_èsèrèsè_osisi 컴파일러는 일반 ihe_valuu·예외·Thread 구문을 아직 컴파일하지 못한다. usu `javac --release 8`로 만든 nkwado_valuu 부분집합 클래스는 자체 JVM 0.4의 ihe_valuu·예외·Thread·UDP와 한국어 API를 사용할 수 있다. Swing은 문서화한 자체 API 부분집합을 제공하며 JAR 로더는 제공하지만 전체 AWT/Swing·JDK 표준 라이브러리는 없다. 정확한 범위는 [자체 JVM 설명](자바실행환경.md)이 기준이다. 상세 Asụsụ 범위는 [공유 Java Ngwaọrụ 설명](../../문서/자바개발환경.md)을 참고하되, 그 문서의 x86 nkọwannyemiwu/Store_valuu/실행시간과 이 ARM64 판의 차이에 유의한다.

MicroPython은 공식 **1.24.1 ebensìbịa_èsèrèsè_osisi**를 자체 AArch64 EL0/SVC 대상으로 빌드했다. Python 문법의 ọrụ_valuu·klaàsị_valuu·예외·리스트/ọkọwa_okwu·Unicode·GC·가변 정밀도 정수를 제공한다. 현재 구성은 ọnụọgụ_nzùrùòkè 빌드로 `float`, `complex`, `math`가 없으며 CPython 전체 표준 ọbaakwụkwọ, pip, subprocess, threading, 일반 socket과 Ngwa_ihe_dịadị `open()` Faịlụ 객체는 제공하지 않는다. `python FILE.py` 및 `-c` 실행만 제공하며 REPL은 아직 없다. 각 실행의 ihe_valuu·모듈은 pụọ_app 시 회수되고 RAM 파일만 다음 실행에 남는다.

`import jkoros`로 다음 시스템 연결을 쓴다. 모두 SVC를 통해 자체 Java 커널에 접근한다.

| ọrụ_valuu | mmèm |
|---|---|
| `stdin(limit)` | 현재 표준 입력에서 최대 limit바이트(0…16384)를 bytes로 읽음; EOF는 빈 bytes, UART datà 없음은 OSError(11) |
| `read(name)` | ibè_valuu/절대 RAM 경로의 Faịlụ 전체를 bytes로 읽음 |
| `write(name, data)` | str/bytes 버퍼를 RAM 파일에 새로 Store_valuu, 쓴 baịtị_valuu 수 반환 |
| `remove(name)` | RAM Faịlụ 삭제 |
| `rect(x, y, w, h, color)` | 선택한 ǹdịnezie_datà 화면 Ụhara 안의 사각형 osise_valuu; 기존 보드의 RGB32 valuu |
| `ticks_ms()` | 부팅 후 밀리초, 32비트 òkirikiri_valuu |
| `udp_open(port)` | 127.0.0.1의 UDP 소켓 Mepee/묶기; 0은 자동 ngwaike_pọọt |
| `udp_send(fd, port, data)` | 루프백 ebemwèga_valuu 포트에 str/bytes 버퍼 dògharịa_valuu |
| `udp_recv(fd)` | `(bytes, 보낸포트)` 반환; 비어 있으면 `OSError(11)` |
| `udp_close(fd)` | 소켓 Mechie |

```python
import jkoros
first = jkoros.udp_open(9401)
second = jkoros.udp_open(9402)
jkoros.udp_send(first, 9402, b"hello")
print(jkoros.udp_recv(second))  # (b'hello', 9401)
jkoros.udp_close(first)
jkoros.udp_close(second)
```

이식 코드: [python/](파이썬연결/), [òjìàrụ Java Banye](òjìàrụ/자바연결.c). 공식 [MicroPython 이식 GỤ̀ỌM_eb81d7d9](https://docs.micropython.org/en/latest/develop/porting.html)를 참고했다. ebensìbịa_èsèrèsè_osisi URL·di_ike_ọbọakwụkwọ·라이선스는 [vendor GỤ̀ỌM_eb81d7d9](vendor/README.md)에 기록했다.

## 남은 작업

| 다음 ebedielu_valuu | 완료 기준 |
|---|---|
| 영속 Store_valuu·mee_nnyemiwu Faịlụ 입력 | SD/MMC 및 디스크 Faịlụ 시스템, 시스템/òjìàrụ 볼륨; 현재 ELF Faịlụ 실행은 RAM에 한정 |
| 일반 프로세스·스레드 | 프로세스별 àdreèsì 공간, 선점 스케줄러, TLS, hàkọọ/대기, 신호, mmap/mprotect |
| libc와 C++ 런타임 | 자체 ABI용 libc, malloc/free, 표준 I_O·elekere·환경·locale, libstdc++/예외 ùsòrò_valuu_ndebà mee_ịbanihe |
| CPython | 해당 libc와 OS API 대상으로 이식·교차 빌드하고 Faịlụ/Unicode/스레드/소켓 시험 |
| OpenJDK/JRE | HotSpot OS òkpùkpù_valuu, GC/JIT/스레드/신호/동적 연결과 Java 네이티브 ọbaakwụkwọ 이식; javac/java ǹdịnezie_datà mee_nnyemiwu |
| 외부 네트워크 | 추가한 GENET/PHY·DHCP 드라이버의 ǹdịnezie_datà 보드 송수신 mee_ịbanihe, DNS·Wi-Fi |
| GUI mgbatị_valuu | USB HID, 게스트 입력기·문자 조판, Swing windò Ụhara 조절·클리핑 mgbatị_valuu, 전체 AWT/Swing 이식 |

이 표는 남은 작업이며 구현 완료 목록이 아니다. QEMU Pi4 모델에는 GENET Ethernet과 PCIe root port가 없어 외부 네트워크 드라이버는 실물 검증도 필요하다. [QEMU njìarụ_valuu 지원표](https://www.qemu.org/docs/master/system/arm/raspi.html)

ngwaike_valuu 및 ABI 참고: [BCM2711 ngwakọmpụtà](https://datasheets.raspberrypi.com/bcm2711/bcm2711-peripherals.pdf), [Pi4 GIC àdreèsì](https://github.com/raspberrypi/linux/blob/rpi-6.12.y/arch/arm/boot/dts/broadcom/bcm2711.dtsi), [mailbox ngō_valuu](https://github.com/raspberrypi/firmware/wiki/Mailbox-property-interface), [Arm ELF64](https://github.com/ARM-software/abi-aa/blob/main/aaelf64/aaelf64.rst), [Arm FP njizi_valuu 레지스터 Nkwuke_valuu](https://github.com/ARM-software/arm-trusted-firmware/blob/master/include/arch/aarch64/arch.h).


## 한국어 C ụdịrị_datà·Python mmejọ·ngwungwu wùbe_valuu

C 네트워크 API는 `struct 인터넷통신주소`, enum 상수와 ǹdịnezie_datà 한국어 함수로
구현한다. nkèokpookpo_valuu 별칭을 사용하지 않으며 이전 pk_* ABI도 유지한다.
Python 예제는 `sistèm_mmejọ`, `mmejọ.indèks`, `mmejọ.설명`을 사용한다.

`python3 Ngwaọrụ/mee_nnyemiwu.py --desktop --network --pip`로 시작하면 게스트에서
`pip install micropython-bisect==3.3.3`을 사용할 수 있다. 현재는 usu 중계를
이용하는 제한형 MicroPython ebensìbịa_èsèrèsè_osisi 설치기이며 CPython pip·자동 의존성 해결·C 확장은
미지원이다. 설치한 `/lib` 자료는 RAM이다. [사용법과 제한](파이썬꾸러미.md).

## 화면 Ụhara ebenhọrọ_valuu

`python3 Ngwaọrụ/mee_nnyemiwu.py --desktop --network --resolution 1920x1080`으로 Full HD 화면을 사용한다. 기본값은 640×480이며 1280×720도 가능하다. 터미널 gàa_valuu, Swing 가운데 Njikọ_Nhàzi, Java·C·Python 그리기도 ǹdịnezie_datà 크기를 따른다. SD 영상은 `make image RESOLUTION=1920x1080`으로 만든다. [Mwube·한국어 API·mee_ịbanihe GỤ̀ỌM_eb81d7d9](화면해상도.md).

## 한국어 직접 API와 화면 mèkwa_ọhụrụ

`example/java`는 `실행할일`, `동작받이`, `동작알림`, `ọdụmbi`, `mmèrème_ọgbàrànchere`,
`작업가닥`, `Bido()`을 사용할 수 있다. 한국어 GUI/가닥을 자체 JVM에 직접
연결했으며, 표준 Swing/Thread를 감싸지 않는다. ùsòròokwū_valuu 등 javac의 표준
계약과 전체 ebensìbịa_èsèrèsè_osisi 검토 범위는 [명명 GỤ̀ỌM_eb81d7d9](명명/GỤ̀ỌM_eb81d7d9.md), 사용법과 호환성 변경은
[한국어 Java API](한국어자바/GỤ̀ỌM_eb81d7d9.md)를 본다.

터미널 gàa_valuu·Ụhara 변경은 바뀐 영역만 합성하고 달라진 화소만 표시한다.
[화면 mèkwa_ọhụrụ 설명](자바실행환경.md#터미널-부분-mèkwa_ọhụrụ),
[부분 mèkwa_ọhụrụ 검사](build/verification/redraw/report.json)를 참고한다.
