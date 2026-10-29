# Raspberry Pi 4 자체 Java cnewyllyn_VALUE — defnyddiwr Gweithredu_gorchymyn 기반

현재 자체 코드의 COSL 상업 cyflwr, 제3자 고지 및 LGPL 재연결 자료는 [COSL 배포 GWYBODAETH_eb81d7d9](COSL배포안내.md)를 참고한다. newid_MODE 전 GPL 구성의 판단은 [이전 라이선스 검토](trwyddedu_adolygu.md)에 기록했다.

Cymraeg 통신·eithriad 사용법은 [Cymraeg Java API](한국어자바/GWYBODAETH_eb81d7d9.md), SWYDDOGAETH_VALUE·변수·Ffeil 이름의 변경과 어원 근거는 [명명 GWYBODAETH_eb81d7d9](명명/GWYBODAETH_eb81d7d9.md)를 참고한다.

Linux 없이 부팅하는 자체 AArch64 커널이다. Java AOT cnewyllyn_VALUE 위에 **llinell_gorchymyn cragen, 게스트 Java 컴파일러·JVM, MicroPython, EL0 C++ Gweithredu_gorchymyn, Ffeil·UDP 루프백 시스템 호출, 여러 한글 GUI Terfynell·vi Editor·Swing 부분집합**을 제공한다. 커널의 Ffeil data/정책·루프백 trosglwyddo_VALUE·cragen 상태는 Java, 화면 합성·pel newid_VALUE·pwyntydd·클리핑도 Java로 구현하며, CPU/MMU/dyfais_VALUE 경계와 Terfynell·nod_VALUE 그리기 연결은 C와 어셈블리다.

**전체 JDK/JRE·CPython·표준 C++ 런타임·Swing 이식은 아직 완료되지 않았다.** 기존 [ARM64 Linux 실행판](../rpi4/README.md)의 OpenJDK/Python 패키지를 이 자체 커널에 탑재했다고 표시하지 않는다.

새로운 게스트 `cc`/`jaot`, JAR 직접 Gweithredu_gorchymyn, lwIP TCP/UDP와 FTP는 [FTP·C·JAR·AOT 매뉴얼](파일전송과번역.md)을 참고한다. 게스트 SSH·VNC와 Pi4 GENET/PHY·DHCP 드라이버를 추가했다. **SSH·VNC는 QEMU에서 검증하며, 실물 Pi4의 wedi_i_wifro_VALUE 송수신은 아직 미검증이다.** Gweithredu_gorchymyn·cyswllt_e05f319b·cyfrinair_VALUE 확인은 [외부 cyswllt_e05f319b GWYBODAETH_eb81d7d9](외부접속안내.md)에 정리했다.

셸은 EL1 cnewyllyn_VALUE, `java` 등 defnyddiwr Gweithredu_gorchymyn 파일은 EL0에서 실행한다.
`ps`·`top`의 표시와 제한, QEMU 네트워크 Gweithredu_gorchymyn·cyswllt_e05f319b 방법 및 go_iawn_data 검증은
[Gweithredu_gorchymyn 계층과 외부 통신 점검](실행계층과외부통신점검.md)을 참고한다.

ELF는 확장자가 아닌 go_iawn_data Gweithredu_gorchymyn 형식으로 검사한다. `./인사`처럼 확장자 없이 실행하며, 제한된 Linux ARM64 statig_VALUE ELF는 `run --linux ffeil_enw_SMS`으로 실행한다. [ELF·Linux ABI Cymorth_VALUE 범위와 동일 바이너리 시험](실행파일규약.md).

GUI와 네트워크는 `python3 Offer/Gweithredu_gorchymyn.py --desktop --network`로 함께 사용한다. Java·C·Python의 Cymraeg 예제 13개는 [jkoros/example](../../example/README.md)에 있으며, **게스트 부팅 시 `/example/java`, `/example/c`, `/example/python`에 자동으로 준비된다.** `example java|c|python`으로 지운 예제를 복원할 수 있다. Remmina에서 **F9/Shift+Space/한·영 bysell_VALUE**로 `[EN]`↔`[KO]` 두벌식을 전환한다(`help ko`). `make test-examples`는 같은 GUI VM에서 FTP·go_iawn_data TCP/UDP·Ffeil beit_VALUE·그래픽 픽셀을 검증한다.

게스트에서 `cd /example/java` 후 `java 창예제`로 Cymraeg Swing 예제를 실행한다. Terfynell 모서리에 마우스를 대고 **왼쪽 버튼으로 끌면 크기가 바뀐다**. `terminal size`는 현재 COLUMN_VALUE·ROW_VALUE 수를 보여 준다.

## 현재 Cymorth_VALUE clip

| 기능 | 구현·시험한 clip | 아직 미지원 |
|---|---|---|
| 부팅 | Pi4 AArch64 EL1, UART, SD용 llunio_llun, QEMU raspi4b 부팅 | go_iawn_data Pi4 보드에서의 펌웨어 부팅 시험 |
| Java cnewyllyn_VALUE | statig_VALUE Java 부분집합 → freestanding C → AArch64 AOT | 전체 Java gwrthrych_VALUE/eithriad/GC/JVM/표준 llyfrgell |
| Java 개발 Offer | 게스트 자체 `javac`/`java`, JVM 0.4/JAR: 다중 Dosbarth_VALUE·gwrthrych_VALUE·상속·eithriad·GC·일부 컬렉션·Thread·IPv4 Socket/UDP·Swing 일부 API, Cymraeg llyfrgell. 게스트 컴파일러는 statig_VALUE Java 부분집합 | 전체 JDK/JRE·HotSpot·Java SE·임의의 모든 JAR·AWT/Swing 전체 |
| Python | go_iawn_data MicroPython 1.24.1 EL0 이식, ffynhonnell_coeden llunio_ffynhonnell/Gweithredu_gorchymyn, Dosbarth_VALUE·eithriad·GC·큰 cyfanrif·Unicode·Ffeil·UDP/화면 Cysylltu | CPython, pip, C estyniad_VALUE, 부동소수점, 일반 OS/스레드/소켓 modiwl_VALUE, rhyngweithiol REPL |
| cragen | UTF-8 Golygu_VALUE·LOG_rhes·완성, 디렉터리·Ffeil Gorchymyn, 변수·cyflwr·sgript_VALUE, 16 KiB 순차 파이프·리다이렉션, ELF Gweithredu_gorchymyn | 전체 POSIX sh/Bash, 작업 rheoli_VALUE·동시 프로세스·PTY |
| C/AOT llunio_ffynhonnell | 게스트 TinyCC 및 statig_VALUE Java 부분집합 `jaot` → 자체 ARM64 ELF | 전체 libc·모든 Java Dosbarth_VALUE AOT |
| C++ | 독립 ELF64를 EL0에서 Gweithredu_gorchymyn; statig_VALUE 생성자, RAII 소멸자, FP/SIMD, Cymraeg Ffeil/루프백 호출 | libc/libstdc++, STL, C++ eithriad·RTTI·동적 Cysylltu |
| defnyddiwr diogelu_VALUE | 4 KiB 페이지, cod_VALUE RX/data RW·NX, cnewyllyn_VALUE·MMIO 차단, guard page, 잘못된 pwyntydd 검사 | 다중 defnyddiwr hawl_VALUE, 일반 프로세스/스레드 스케줄러 |
| Gweithredu_gorchymyn TIME_VALUE 제한 | GIC-400 타이머로 무한 iteriad_VALUE gadael_Rhaglen; rhyngweithiol 입력 대기는 기한 adnewyddu, 터미널별 EL0 Rhaglen_f5044b9b 중단·재개 | 일반적인 선점형 다중작업. 긴 cnewyllyn_VALUE 호출 도중에는 종료가 지연될 수 있음 |
| Ffeil | Java RAM Ffeil 64개 × 16384바이트, 루트를 포함한 디렉터리 16개, cymar_VALUE/절대 LLWYBR 63바이트, 서술자 16개 | hawl_VALUE, 디스크/SD 영속 Store_VALUE |
| 네트워크 | lwIP IPv4 TCP/UDP/ARP/ICMP, SLIP, GENET/PHY·DHCP 구현, 게스트 FTP·SSH·VNC | GENET 실물 dilysu_5fb2b747, Wi-Fi, DNS, 일반 TLS 소켓, RDP |
| GUI | 최대 네 Terfynell ffenestr, dewisiad_VALUE·symud_VALUE·X Cau, 한글 ffont_VALUE, Swing 부분집합; 게스트 VNC 화면·입력·두벌식 | 실물 USB 입력, 전체 AWT/Swing·Java2D·ffenestr 관리 정책 |
| 작업 edefyn_VALUE | cnewyllyn_VALUE 작업 2개와 주 작업; JVM 내부 edefyn_VALUE 최대 4개, start/join/yield·synchronized | pthread, SMP, Java Thread 전체 API |
| 다국어 | UTF-16 리터럴→UTF-8 UART, 한글·일본어·아랍어·이모지, UTF-8 ffeil_enw_SMS/전문 | GUI의 일반 다국어 조판 |

Gweithredu_gorchymyn 버튼 화면은 5×7 영문 글꼴을 쓰며, Terfynell 창은 Noto CJK/DejaVu에서 생성한 한글·Unicode 비트맵 글꼴을 쓴다. UART와 go_iawn_data 프레임버퍼의 한글 표시를 시험한다. 루프백은 동일 cnewyllyn_VALUE 내부의 전문 전달이며 IP 패킷을 Ethernet으로 내보내는 드라이버가 아니다. 바깥 IPv4는 lwIP TCP/UDP 스택으로 보조 UART SLIP 경로를 사용한다. `python3 Offer/Gweithredu_gorchymyn.py --network`로 QEMU NAT를 연결하고 `ftpd start`로 서비스를 시작한다.

Java의 정확한 API·문법·Gweithredu_gorchymyn 제한과 Cymraeg 사용법은 [자체 JVM과 Cymraeg llyfrgell](자바실행환경.md)에 정리했다. Dosbarth_VALUE Ffeil/JAR 배포는 [한국어자바](한국어자바) 소스에서 재현한다. 기존 Linux판 `Cymraeg.자바`와 별도인 `Cymraeg.자체` 패키지다.

**vi·여러 ffenestr·Swing·한글 Java/Python/C/C++·posix-kor 예제는 [한글 개발 매뉴얼](개발안내.md)에 정리했다.**

GUI Terfynell Gweithredu_gorchymyn·단축키·cragen Gorchymyn·제한은 [셸과 Terfynell 사용법](cragen_AND_Terfynell.md)에 정리했다.

## 현재 컴퓨터에서 Gweithredu_gorchymyn

```sh
cd /home/user/jkoros/platforms/rpi4-native
make test
make run
```

gadael_Rhaglen: **Ctrl+A Nesaf_eitem X**. 게스트 C/AOT Offer 빌드에는 `make rpi-prepare`로 준비한 ARM64 SDK 헤더와 libgcc 산술 보조 함수도 필요하다. libc나 Linux 커널을 게스트에 넣는 것은 아니다. lletya 도구는 JDK 11 이상, Python 3.6 이상, Clang/Clang++, AArch64 GNU binutils, Make, `libnewlib-dev` 헤더다. MicroPython은 `/usr/include/newlib` 헤더를 사용하며 다른 위치는 `NEWLIB_INCLUDE`로 지정한다. newlib 런타임을 이식·링크한 것은 아니다. 컴파일러 의미 비교에는 GCC/UBSan도 사용한다. 기존 `../rpi4/build/host`의 QEMU 11.0.3이 있으면 이용하며, 그렇지 않으면 PATH의 QEMU를 사용한다. `QEMU_AARCH64=/절대/LLWYBR/qemu-system-aarch64`로 지정할 수도 있다. `raspi4b` Cymorth_VALUE 여부를 확인한 후 실행한다.

명령은 **Enter를 눌러 Gweithredu_gorchymyn**한다. 기존 한 nod_VALUE 명령도 Enter가 필요하다.

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

| Gorchymyn | Gweithrediad |
|---|---|
| `help` / `info` | Gorchymyn·go_iawn_data 구현 cyflwr_VALUE |
| `ls` / `cat FILE` / `rm FILE` | RAM Ffeil cofnod_Rhestr·Cynnwys_VALUE·삭제 |
| `vi FILE` | defnyddiwr 영역 vi 부분집합, 한글 Golygu_VALUE·Store_VALUE·검색·되돌리기 |
| `edit FILE` | Ffeil 전체를 새로 입력; 단독 `.` 줄로 Store_VALUE, Ctrl-C로 Canslo_gweithrediad |
| `javac FILE.java` / `java CLASS [ARGS]` | 자체 제한형 Java llunio_ffynhonnell·Gweithredu_gorchymyn |
| `python FILE.py [ARGS]` / `python -c 'CODE'` | MicroPython llunio_ffynhonnell·Gweithredu_gorchymyn |
| `load FILE` / `hex FILE` | 16진수 바이너리 입력/Allbwn; 입력은 단독 `.` 줄로 Store_VALUE |
| `run FILE.elf [ARGS]` / `run cpp` | 업로드한 자체 ABI ELF / 내장 C++ 예제 |
| `net test` / `tasks` / `selftest` | UDP 루프백 / 협력식 작업 / EL0 diogelu_VALUE 시험 |
| `gui` / `terminal` | Gweithredu_gorchymyn 화면 / 한글 GUI Terfynell; F12로 Terfynell Agor·Cau |
| `samples` | 삭제한 gwerth_diofyn 예제 adfer_cyflwr; 기존 파일은 보존 |

예를 들어 `edit 인사.java`를 입력한 Nesaf_eitem 아래 소스를 입력한다.

```java
public class 인사 { public static void main(String[] args) { int VALUE = 7; System.out.println("한글=" + VALUE); } }
```

그다음 단독 `.` 줄로 저장하고 `javac 인사.java`, `java 인사`를 실행한다. 편집기는 기존 파일에 커서를 이동하는 방식이 아니라 전체 교체 방식이다. Canslo_gweithrediad·잘못된 16진수·용량 초과는 원본을 보존한다. 줄은 4096바이트, 파일은 16384바이트, Gweithredu_gorchymyn 인수는 최대 8개·각각 UTF-8 255바이트다. 일반 Gorchymyn 인수는 최대 32개다. Dyfyniad·백슬래시·cragen 변수·파이프·리다이렉션 범위는 [cragen 설명](cragen_AND_Terfynell.md)을 참고한다.

GUI 터미널은 다음과 같이 실행하고 Remmina에서 **VNC**, ADDRESS **127.0.0.1:5902**로 연결한다. 키보드·한글 Unicode 입력·명시적 gludo_VALUE·Gweithredu_gorchymyn 버튼의 마우스 클릭을 QEMU 도구가 UART에 전달한다.

```sh
make desktop
# GUI + 네트워크: python3 Offer/Gweithredu_gorchymyn.py --desktop --network
# 다른 포트: python3 Offer/Gweithredu_gorchymyn.py --desktop --port 5903
```

종료는 실행한 lletya 터미널에서 Ctrl+C다. 기존 `python3 Offer/Gweithredu_gorchymyn.py --vnc 127.0.0.1:2`는 화면 보기와 별도 UART 입력을 유지한다. `make run`은 일반 UART 셸이다. go_iawn_data Pi4 USB 입력기는 아직 없으며, VNC Cysylltu 도구는 QEMU 시험용이다.

GUI의 다섯 버튼은 go_iawn_data C++/UDP ELF Gweithredu_gorchymyn, `Hello.java` llunio_ffynhonnell 후 JVM Gweithredu_gorchymyn, `hello.py` Gweithredu_gorchymyn, GUI Terfynell 열기를 수행한다. 한 번에 한 프로그램이 CPU에서 실행되며 일반 실행에는 약 2초 기한이 있다. vi·Swing은 rhyngweithiol 대기에서 기한을 갱신하고 다른 터미널로 전환할 때 Cof_data·CPU 문맥을 보관한다. cragen·편집기에서 입력을 기다리는 시간에는 이 제한이 적용되지 않는다.

## go_iawn_data 산출물과 Pi4 SD llunio_llun

```sh
make image   # cnewyllyn_VALUE, SD llunio_llun, 부팅 ZIP, 사용자용 SDK
make sdk     # SDK만 다시 cynhyrchu
```

| LLWYBR | 용도 |
|---|---|
| `build/kernel8.img` | 자체 cnewyllyn_VALUE 기계어, 적재 ADDRESS 0x80000 |
| `build/kernel.elf`, `kernel.map` | cnewyllyn_VALUE symbol_VALUE·Dolen_Llywio |
| `build/user/demo.elf` | defnyddiwr MODE_VALUE C++ Ffeil/힙/실수/그래픽 예제 |
| `build/user/network.elf` | defnyddiwr MODE_VALUE C++ UDP 루프백 예제 |
| `build/user/java-tools.elf` | 자체 Java 부분집합 컴파일러/JVM, 전체 JDK/JRE 아님 |
| `dist/jkoros-native-korean.jar` | lletya javac용 Cymraeg API Dosbarth_VALUE; 같은 클래스가 자체 JVM에도 내장됨 |
| `dist/jkoros-native-korean-sources.zip` | Cymraeg API Java FFYNHONNELL |
| `build/user/vi.elf` | 자체 UTF-8 vi Gorchymyn 부분집합 Editor |
| `build/user/python.elf` | 자체 ABI용 MicroPython 1.24.1, CPython 아님 |
| `build/user/fault.elf` | 의도적 침범/무한 반복을 수행하는 diogelu_VALUE 시험 전용 |
| `build/libposix-kor-arm64.a` | **cnewyllyn_VALUE 내부**에서 Java Ffeil 구현을 직접 부르는 기존 Cysylltu |
| `build/libposix-kor-user.a` | **EL0 defnyddiwr Rhaglen_f5044b9b**에서 SVC로 Ffeil/루프백을 호출하는 새 Cysylltu |
| `dist/jkoros-native-rpi4.img` | 128 MiB MBR/FAT32 SD llunio_llun |
| `dist/jkoros-native-rpi4-boot.zip` | FAT32 부팅 파티션에 복사할 Ffeil Grŵp_VALUE |
| `dist/jkoros-native-aarch64-sdk.tar.gz` | 사용자용 헤더·Gweithredu_2 cod_VALUE·llyfrgell·링커 sgript_VALUE·예제 |
| `dist/manifest.json`, `build/build.json` | SHA256과 go_iawn_data Cymorth_VALUE cyflwr_VALUE |

이미지는 확인된 공식 Pi 부팅 묶음에서 `start4.elf`, `fixup4.dat`, Pi4 DTB와 disable-bt overlay를 가져온다. Linux kernel/initramfs/rootfs는 넣지 않는다. 펌웨어·MicroPython·Terfynell ffont_VALUE 라이선스와 ffont_VALUE 출처 해시도 동봉한다. Ffeil cynhyrchu 스크립트는 물리 디스크에 기록하지 않는다.

예비 microSD에 llunio_llun LOG_rhes 도구로 `.img`를 기록하거나 FAT32 부팅 파티션 최상위에 ZIP 내용을 푼다. llunio_llun 기록은 선택한 카드의 기존 내용을 지우므로 대상을 확인한다. Pi4 gwerth_diofyn EEPROM SD 부팅을 전제로 한다. UART는 **3.3V TTL, 115200 8N1**, GPIO14/TXD(8번)→어댑터 RX, GPIO15/RXD(10번)→TX, GND(6번) 연결이다. GPIO에 5V 신호를 연결하지 않는다.

**실물 Pi4 부팅은 미검증이다.** QEMU `-kernel`은 SD의 VideoCore 펌웨어를 실행하지 않고 커널을 직접 적재한다. SD Ffeil 구성·cnewyllyn_VALUE 체크섬 검사와 물리 bwrdd 부팅 검증은 별개다. MMU 사용 전에는 펌웨어의 캐시/MMU가 꺼져 있고 EL1 또는 EL2로 진입하는 통상 부팅 조건을 전제로 한다. 세 보조 코어는 대기시키며 한 코어만 사용한다.

## C++와 Cymraeg API 사용

SDK를 풀고 호스트에서 컴파일한다.

```sh
tar -xzf dist/jkoros-native-aarch64-sdk.tar.gz -C build
cd build/jkoros-native-sdk
python3 compile.py examples/파일예제.cpp -o demo.elf
python3 compile.py examples/통신예제.cpp -o network.elf
```

진입점은 `extern "C" int START_defnyddiwr_Rhaglen(int)`이다. defnyddiwr C++는 FP/SIMD를 사용할 수 있다. cnewyllyn_VALUE C/Java AOT는 일반 레지스터만 사용하므로 eithriad Proses_VALUE_cofnod 중 defnyddiwr FP 상태를 건드리지 않는다. defnyddiwr cofnod_p_VALUE 시 FP 상태를 초기화하고 cnewyllyn_VALUE 복귀에 필요한 상태를 보존한다.

```cpp
#include "파일규약.h"
extern "C" int START_defnyddiwr_Rhaglen(int) {
    int Ffeil = agor_ffeil("인사.txt", darllen_ysgrifennu | 없으면만들기 | 내용비우기, 0600);
    if (Ffeil < 0) return 1;
    const char Cynnwys_VALUE[] = "안녕하세요";
    int mesur = ysgrifennu_ffeil_data(Ffeil, Cynnwys_VALUE, sizeof(Cynnwys_VALUE) - 1);
    cau_ffeil(Ffeil);
    return mesur == sizeof(Cynnwys_VALUE) - 1 ? 0 : 2;
}
```

[Ffeil 예제](defnyddiwr/파일예제.cpp)와 [통신 예제](defnyddiwr/통신예제.cpp)가 go_iawn_data 부팅 시험 대상이다. `파일규약.h`의 이름은 커널용/사용자용 모두 같지만 **링크하는 라이브러리가 다르다**. 사용자용은 `svc #0`으로 호출하고 Ffeil Proses_VALUE_cofnod 및 루프백 전달은 Java 커널에서 실행한다. `통신규약.h`의 소켓 함수는 현재 사용자용 라이브러리에 구현돼 있다.

새 프로그램은 cnewyllyn_VALUE 재빌드 없이 `load FILE.elf`와 `run FILE.elf`로 실행한다. 호스트에서 Nesaf_eitem 도구를 사용하면 **새 QEMU를 부팅해 업로드한 go_iawn_data 바이트를 재확인한 BACK_VALUE 게스트에서 Gweithredu_gorchymyn**하고 종료한다. 이 도구의 새 VM에서 만든 RAM 자료는 종료할 때 사라진다.

```sh
cd /home/user/jkoros/platforms/rpi4-native
python3 Offer/Gweithredu_ffeil.py build/jkoros-native-sdk/demo.elf
python3 Offer/Gweithredu_ffeil.py 예제/Hello.java "한글 인수"
python3 Offer/Gweithredu_ffeil.py 예제/hello.py
```

이 경로는 16KiB 이하의 `.elf`, `.java`, `.class`, `.py`를 지원한다. 큰 내장 Java/MicroPython ELF 자체는 cnewyllyn_VALUE 묶음에 포함되어 이 Ffeil 한도를 적용받지 않는다. **C++ 컴파일러는 lletya SDK의 Clang++**이며 게스트 내부 GCC/Clang 컴파일러는 아직 없다. SDK만으로 일반 Linux 프로그램을 실행할 수는 없다. Linux ELF, 동적 llyfrgell, PT_TLS, PT_INTERP, PT_DYNAMIC, Gweithredu_gorchymyn·Ysgrifennu 겸용 세그먼트는 로더가 거부한다. 구체적인 호출 INDEX·ADDRESS clip·오류는 [defnyddiwr ABI](사용자호출규약.md)를 참고한다.

RAM 파일은 재부팅 시 사라진다. `파일저장확정`은 -1과 ENOSYS를 반환한다. 파일의 mode 인수를 저장하지 않으며 hawl_VALUE·dup/fcntl은 없다. 디렉터리와 cymar_VALUE/절대 경로는 같은 RAM 저장소에서 처리한다. UDP 전문은 최대 512바이트, 소켓은 8개, 수신 큐는 소켓당 4개다. 수신할 자료가 없거나 큐가 가득 차면 EAGAIN을 반환한다. defnyddiwr gadael_Rhaglen 시 열린 Ffeil 서술자와 소켓을 회수한다.

## dilysu_5fb2b747 mesur

`make test-jvm`은 9개 프로그램을 OpenJDK와 go_iawn_data 자체 커널에서 실행해 결과를 비교한다. `make test`에도 포함된다. 별도 `Offer/부팅시험.py`는 Java 사각형 API의 go_iawn_data 화면 픽셀까지 검사한다. `make test-shell`, `make test-desktop`은 새 셸과 go_iawn_data VNC 입력·한글 Terfynell 화면을 검사하며 `make test`에도 포함된다.

`make test-windows`, `make test-swing`, `make test-stream`, `make test-coding`도 제공하며 `make test`에 포함된다.

`make test`는 OpenJDK와 AOT gweithrediad_VALUE mesur 비교, 런타임 Gwall 중단, 미지원 Java 거부와 함께 별도 QEMU VM에서 다음을 검사한다.

- 기존 Java cnewyllyn_VALUE 계산·UTF-8·C++ 직접 호출·협력식 작업 및 프레임버퍼.
- 손상/잘못된 ABI/ADDRESS 초과/겹친 페이지/W+X 등 ELF gwrthod_VALUE 사례 22개.
- EL0 C++ 생성자·RAII·실수 gweithrediad_VALUE·Ffeil·힙 및 잘못된 시스템 호출 pwyntydd.
- cnewyllyn_VALUE/cod_VALUE/MMIO Ysgrifennu·mynediad_cofnod, NX 스택·NULL Gweithredu_gorchymyn, guard page, 특권 Gorchymyn 차단.
- SVC를 호출하지 않는 무한 반복을 타이머로 종료한 후 technoleg_gwybodaeth_normal Rhaglen_f5044b9b 재실행.
- iteriad_VALUE Gweithredu_gorchymyn 시 Ffeil/소켓 누수 방지, UDP 왕복·보낸 ADDRESS·잘린 수신·큐 포화·빈 전문·미지원 통신 Gwall.
- cragen Golygu_VALUE·Canslo_gweithrediad·16진수 업로드/다운로드·defnyddiwr ELF 실행과 잘못된 ELF gwrthod_VALUE.
- 게스트 Java → OpenJDK `-Xverify:all`, OpenJDK → 게스트 JVM 교차 Gweithredu_gorchymyn, 한글 Dosbarth_VALUE·변수·ffeil_enw_SMS.
- 여러 ffenestr·vi Store_VALUE·Golygu_VALUE·return_pont·defnyddiwr cyflwr_VALUE 중단/재개, Swing 한글 입력·이벤트·X Cau, 연결형 루프백, C/C++ 한글 SDK 예제.
- MicroPython Unicode·큰 cyfanrif·Dosbarth_VALUE·GC iteriad_VALUE·Ffeil import·eithriad·Ffeil·UDP 왕복·TIME_VALUE 초과 후 복귀.
- GUI dewisiad_VALUE symud_VALUE, C++/UDP/Java/MicroPython 버튼 Gweithredu_gorchymyn, 콘솔 복귀 및 go_iawn_data 프레임버퍼 픽셀/ffont_VALUE.
- 디렉터리·변수·cyflwr·Ffeil Gorchymyn·sgript_VALUE·순차 파이프·리다이렉션·용량 초과 adfer_cyflwr, Python stdin/EOF와 Java/Python stdout.
- Gorchymyn LOG_rhes·긴 한글 입력 Golygu_VALUE·완성·Terfynell 스크롤, 그래픽 Rhaglen_f5044b9b gadael_Rhaglen 후 ffenestr 복원, go_iawn_data VNC Unicode bysell_VALUE·gludo_VALUE·마우스.

[cnewyllyn_VALUE 시험 LOG_rhes](build/verification/implementation-test.log), [cragen 시험](build/verification/shell/report.json), [VNC 시험](build/verification/desktop/report.json), [peiriant 판독 mesur](build/verification/report.json), [직렬 LOG_VALUE](build/verification/serial.log), [GUI 화면](build/verification/gui-python.png)을 확인할 수 있다. VNC RFB 3.8 Cysylltu 및 640×480 화면 정보도 검사한다. [SDK 재컴파일 mesur](build/verification/sdk.json)는 두 예제의 cofnod_p·적재 세그먼트·ABI note가 부팅 시험한 ELF와 일치함을 확인한다. symbol_VALUE 등 비적재 메타데이터를 포함한 Ffeil 전체의 SHA256까지 같다고 의미하지는 않는다.

## Java와 Python의 정확한 clip

자체 `javac`는 버전 49 `.class`를 생성하며 JVM은 Cymorth_VALUE 명령으로 구성된 버전 45–52 클래스를 실행한다. statig_VALUE SWYDDOGAETH_VALUE·재귀·int/boolean/char/String·cyflwr/iteriad_VALUE·testun_VALUE 결합과 일부 Ffeil 스트림을 지원한다. UTF-8 문자열과 문자 리터럴, ASCII 및 현대 한글 음절/조합 자모 식별자를 처리한다. Unicode dynodwr_VALUE 전체 LOOKUP_tabl·Unicode ffynhonnell_coeden 이스케이프는 구현하지 않았다. 게스트 ffynhonnell_coeden 컴파일러는 일반 gwrthrych_VALUE·eithriad·Thread 구문을 아직 컴파일하지 못한다. lletya `javac --release 8`로 만든 Cymorth_VALUE 부분집합 클래스는 자체 JVM 0.4의 gwrthrych_VALUE·eithriad·Thread·UDP와 Cymraeg API를 사용할 수 있다. Swing은 문서화한 자체 API 부분집합을 제공하며 JAR 로더는 제공하지만 전체 AWT/Swing·JDK 표준 라이브러리는 없다. 정확한 범위는 [자체 JVM 설명](자바실행환경.md)이 기준이다. 상세 Iaith 범위는 [공유 Java Offer 설명](../../문서/자바개발환경.md)을 참고하되, 그 문서의 x86 cragen/Store_VALUE/실행시간과 이 ARM64 판의 차이에 유의한다.

MicroPython은 공식 **1.24.1 ffynhonnell_coeden**를 자체 AArch64 EL0/SVC 대상으로 빌드했다. Python 문법의 SWYDDOGAETH_VALUE·Dosbarth_VALUE·eithriad·리스트/geiriadur·Unicode·GC·가변 정밀도 정수를 제공한다. 현재 구성은 cyfanrif 빌드로 `float`, `complex`, `math`가 없으며 CPython 전체 표준 llyfrgell, pip, subprocess, threading, 일반 socket과 gwerth_diofyn `open()` Ffeil 객체는 제공하지 않는다. `python FILE.py` 및 `-c` 실행만 제공하며 REPL은 아직 없다. 각 실행의 gwrthrych_VALUE·모듈은 gadael_Rhaglen 시 회수되고 RAM 파일만 Nesaf_eitem 실행에 남는다.

`import jkoros`로 Nesaf_eitem 시스템 연결을 쓴다. 모두 SVC를 통해 자체 Java 커널에 접근한다.

| SWYDDOGAETH_VALUE | Gweithrediad |
|---|---|
| `stdin(limit)` | 현재 표준 입력에서 최대 limit바이트(0…16384)를 bytes로 읽음; EOF는 빈 bytes, UART data 없음은 OSError(11) |
| `read(name)` | cymar_VALUE/절대 RAM 경로의 Ffeil 전체를 bytes로 읽음 |
| `write(name, data)` | str/bytes 버퍼를 RAM 파일에 새로 Store_VALUE, 쓴 beit_VALUE 수 return_mesur |
| `remove(name)` | RAM Ffeil 삭제 |
| `rect(x, y, w, h, color)` | 선택한 go_iawn_data 화면 Maint 안의 사각형 lluniad_VALUE; 기존 보드의 RGB32 VALUE |
| `ticks_ms()` | 부팅 후 밀리초, 32비트 Cylch_VALUE |
| `udp_open(port)` | 127.0.0.1의 UDP 소켓 Agor/묶기; 0은 자동 포트 |
| `udp_send(fd, port, data)` | 루프백 cyrchfan_VALUE 포트에 str/bytes 버퍼 trosglwyddo_VALUE |
| `udp_recv(fd)` | `(bytes, 보낸포트)` return_mesur; 비어 있으면 `OSError(11)` |
| `udp_close(fd)` | 소켓 Cau |

```python
import jkoros
first = jkoros.udp_open(9401)
second = jkoros.udp_open(9402)
jkoros.udp_send(first, 9402, b"hello")
print(jkoros.udp_recv(second))  # (b'hello', 9401)
jkoros.udp_close(first)
jkoros.udp_close(second)
```

이식 cod_VALUE: [python/](PYTHON_pont/), [defnyddiwr Java Cysylltu](defnyddiwr/자바연결.c). 공식 [MicroPython 이식 GWYBODAETH_eb81d7d9](https://docs.micropython.org/en/latest/develop/porting.html)를 참고했다. ffynhonnell_coeden URL·hash_ffeil·라이선스는 [vendor GWYBODAETH_eb81d7d9](vendor/README.md)에 기록했다.

## 남은 작업

| Nesaf_eitem cam_VALUE | 완료 prosiect_gwraidd |
|---|---|
| 영속 Store_VALUE·Gweithredu_gorchymyn Ffeil 입력 | SD/MMC 및 디스크 Ffeil 시스템, 시스템/defnyddiwr 볼륨; 현재 ELF Ffeil 실행은 RAM에 한정 |
| 일반 프로세스·스레드 | 프로세스별 ADDRESS 공간, 선점 스케줄러, TLS, cysoni/aros_VALUE, 신호, mmap/mprotect |
| libc와 C++ 런타임 | 자체 ABI용 libc, malloc/free, 표준 I_O·Cloc·환경·locale, libstdc++/eithriad Proses_VALUE_cofnod dilysu_5fb2b747 |
| CPython | 해당 libc와 OS API 대상으로 이식·교차 빌드하고 Ffeil/Unicode/스레드/소켓 시험 |
| OpenJDK/JRE | HotSpot OS haen_VALUE, GC/JIT/스레드/신호/동적 연결과 Java 네이티브 llyfrgell 이식; javac/java go_iawn_data Gweithredu_gorchymyn |
| 외부 네트워크 | 추가한 GENET/PHY·DHCP 드라이버의 go_iawn_data bwrdd 송수신 dilysu_5fb2b747, DNS·Wi-Fi |
| GUI estyniad_VALUE | USB HID, 게스트 입력기·문자 조판, Swing ffenestr Maint 조절·클리핑 estyniad_VALUE, 전체 AWT/Swing 이식 |

이 표는 남은 작업이며 구현 완료 목록이 아니다. QEMU Pi4 모델에는 GENET Ethernet과 PCIe root port가 없어 외부 네트워크 드라이버는 실물 검증도 필요하다. [QEMU dyfais_VALUE 지원표](https://www.qemu.org/docs/master/system/arm/raspi.html)

하드웨어 및 ABI 참고: [BCM2711 ategolyn](https://datasheets.raspberrypi.com/bcm2711/bcm2711-peripherals.pdf), [Pi4 GIC ADDRESS](https://github.com/raspberrypi/linux/blob/rpi-6.12.y/arch/arm/boot/dts/broadcom/bcm2711.dtsi), [mailbox tasg_VALUE](https://github.com/raspberrypi/firmware/wiki/Mailbox-property-interface), [Arm ELF64](https://github.com/ARM-software/abi-aa/blob/main/aaelf64/aaelf64.rst), [Arm FP rheoli_VALUE 레지스터 Diffiniad_VALUE](https://github.com/ARM-software/arm-trusted-firmware/blob/master/include/arch/aarch64/arch.h).


## Cymraeg C math_data·Python Gwall·bwndel gosod_VALUE

C 네트워크 API는 `struct 인터넷통신주소`, enum 상수와 go_iawn_data Cymraeg 함수로
구현한다. macro_VALUE 별칭을 사용하지 않으며 이전 pk_* ABI도 유지한다.
Python 예제는 `system_gwall`, `Gwall.INDEX`, `Gwall.설명`을 사용한다.

`python3 Offer/Gweithredu_gorchymyn.py --desktop --network --pip`로 시작하면 게스트에서
`pip install micropython-bisect==3.3.3`을 사용할 수 있다. 현재는 lletya 중계를
이용하는 제한형 MicroPython ffynhonnell_coeden 설치기이며 CPython pip·자동 의존성 해결·C 확장은
미지원이다. 설치한 `/lib` 자료는 RAM이다. [사용법과 제한](PYTHON_bwndel.md).

## 화면 Maint dewisiad_VALUE

`python3 Offer/Gweithredu_gorchymyn.py --desktop --network --resolution 1920x1080`으로 Full HD 화면을 사용한다. 기본값은 640×480이며 1280×720도 가능하다. Terfynell symud_VALUE, Swing 가운데 Dolen_Llywio, Java·C·Python 그리기도 go_iawn_data 크기를 따른다. SD 영상은 `make image RESOLUTION=1920x1080`으로 만든다. [Gosodiadau·Cymraeg API·dilysu_5fb2b747 GWYBODAETH_eb81d7d9](화면해상도.md).

## Cymraeg 직접 API와 화면 adnewyddu

`example/java`는 `실행할일`, `동작받이`, `동작알림`, `botwm`, `digwyddiad_ciw`,
`작업가닥`, `Gweithredu_2()`을 사용할 수 있다. Cymraeg GUI/가닥을 자체 JVM에 직접
연결했으며, 표준 Swing/Thread를 감싸지 않는다. testun_VALUE 등 javac의 표준
계약과 전체 ffynhonnell_coeden 검토 범위는 [명명 GWYBODAETH_eb81d7d9](명명/GWYBODAETH_eb81d7d9.md), 사용법과 호환성 변경은
[Cymraeg Java API](한국어자바/GWYBODAETH_eb81d7d9.md)를 본다.

Terfynell symud_VALUE·Maint 변경은 바뀐 영역만 합성하고 달라진 화소만 표시한다.
[화면 adnewyddu 설명](자바실행환경.md#Terfynell-부분-adnewyddu),
[부분 adnewyddu 검사](build/verification/redraw/report.json)를 참고한다.
