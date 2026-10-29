# Raspberry Pi 4 자체 Java bërthamë_VALUE — përdorues zbatoj_komandë 기반

현재 자체 코드의 COSL 상업 kusht, 제3자 고지 및 LGPL 재연결 자료는 [COSL 배포 LEXOMË_eb81d7d9](COSL배포안내.md)를 참고한다. SWITCH_MODE 전 GPL 구성의 판단은 [이전 라이선스 검토](licencoj_recension.md)에 기록했다.

한국어 통신·përjashtim 사용법은 [한국어 Java API](한국어자바/LEXOMË_eb81d7d9.md), FUNCTION_VALUE·변수·Kartelë 이름의 변경과 어원 근거는 [명명 LEXOMË_eb81d7d9](명명/LEXOMË_eb81d7d9.md)를 참고한다.

Linux 없이 부팅하는 자체 AArch64 커널이다. Java AOT bërthamë_VALUE 위에 **rreshti_i_komandës pasues, 게스트 Java 컴파일러·JVM, MicroPython, EL0 C++ zbatoj_komandë, Kartelë·UDP 루프백 시스템 호출, 여러 한글 GUI Terminali·vi Redaktori·Swing 부분집합**을 제공한다. 커널의 Kartelë të_dhëna/정책·루프백 transferim_VALUE·pasues 상태는 Java, 화면 합성·pikëz ndryshoj_VALUE·tregues·클리핑도 Java로 구현하며, CPU/MMU/pajisje_VALUE 경계와 Terminali·karakter_VALUE 그리기 연결은 C와 어셈블리다.

**전체 JDK/JRE·CPython·표준 C++ 런타임·Swing 이식은 아직 완료되지 않았다.** 기존 [ARM64 Linux 실행판](../rpi4/README.md)의 OpenJDK/Python 패키지를 이 자체 커널에 탑재했다고 표시하지 않는다.

새로운 게스트 `cc`/`jaot`, JAR 직접 zbatoj_komandë, lwIP TCP/UDP와 FTP는 [FTP·C·JAR·AOT 매뉴얼](파일전송과번역.md)을 참고한다. 게스트 SSH·VNC와 Pi4 GENET/PHY·DHCP 드라이버를 추가했다. **SSH·VNC는 QEMU에서 검증하며, 실물 Pi4의 i_lidhur_VALUE 송수신은 아직 미검증이다.** zbatoj_komandë·lidhje_e05f319b·fjalëkalim_VALUE 확인은 [외부 lidhje_e05f319b LEXOMË_eb81d7d9](외부접속안내.md)에 정리했다.

셸은 EL1 bërthamë_VALUE, `java` 등 përdorues zbatoj_komandë 파일은 EL0에서 실행한다.
`ps`·`top`의 표시와 제한, QEMU 네트워크 zbatoj_komandë·lidhje_e05f319b 방법 및 aktual_të_dhëna 검증은
[zbatoj_komandë 계층과 외부 통신 점검](실행계층과외부통신점검.md)을 참고한다.

ELF는 확장자가 아닌 aktual_të_dhëna zbatoj_komandë 형식으로 검사한다. `./인사`처럼 확장자 없이 실행하며, 제한된 Linux ARM64 statik_VALUE ELF는 `run --linux skedar_emër_SMS`으로 실행한다. [ELF·Linux ABI Mbështetje_VALUE 범위와 동일 바이너리 시험](실행파일규약.md).

GUI와 네트워크는 `python3 Mjete/zbatoj_komandë.py --desktop --network`로 함께 사용한다. Java·C·Python의 한국어 예제 13개는 [jkoros/example](../../example/README.md)에 있으며, **게스트 부팅 시 `/example/java`, `/example/c`, `/example/python`에 자동으로 준비된다.** `example java|c|python`으로 지운 예제를 복원할 수 있다. Remmina에서 **F9/Shift+Space/한·영 tast_VALUE**로 `[EN]`↔`[KO]` 두벌식을 전환한다(`help ko`). `make test-examples`는 같은 GUI VM에서 FTP·aktual_të_dhëna TCP/UDP·Kartelë bajt_VALUE·그래픽 픽셀을 검증한다.

게스트에서 `cd /example/java` 후 `java 창예제`로 한국어 Swing 예제를 실행한다. Terminali 모서리에 마우스를 대고 **왼쪽 버튼으로 끌면 크기가 바뀐다**. `terminal size`는 현재 COLUMN_VALUE·ROW_VALUE 수를 보여 준다.

## 현재 Mbështetje_VALUE fragment

| 기능 | 구현·시험한 fragment | 아직 미지원 |
|---|---|---|
| 부팅 | Pi4 AArch64 EL1, UART, SD용 ndërtoj_IMAGE, QEMU raspi4b 부팅 | aktual_të_dhëna Pi4 보드에서의 펌웨어 부팅 시험 |
| Java bërthamë_VALUE | statik_VALUE Java 부분집합 → freestanding C → AArch64 AOT | 전체 Java objekt_VALUE/përjashtim/GC/JVM/표준 bibliotekë |
| Java 개발 Mjete | 게스트 자체 `javac`/`java`, JVM 0.4/JAR: 다중 klasë_VALUE·objekt_VALUE·상속·përjashtim·GC·일부 컬렉션·Thread·IPv4 Socket/UDP·Swing 일부 API, 한국어 bibliotekë. 게스트 컴파일러는 statik_VALUE Java 부분집합 | 전체 JDK/JRE·HotSpot·Java SE·임의의 모든 JAR·AWT/Swing 전체 |
| Python | aktual_të_dhëna MicroPython 1.24.1 EL0 이식, burim_degëzim ndërtoj_burim/zbatoj_komandë, klasë_VALUE·përjashtim·GC·큰 numër_i_plotë·Unicode·Kartelë·UDP/화면 Lidhu | CPython, pip, C shtesë_VALUE, 부동소수점, 일반 OS/스레드/소켓 modul_VALUE, ndërvepruese REPL |
| pasues | UTF-8 redaktim_VALUE·LOG_RECORD·완성, 디렉터리·Kartelë Komanda, 변수·kusht·skript_VALUE, 16 KiB 순차 파이프·리다이렉션, ELF zbatoj_komandë | 전체 POSIX sh/Bash, 작업 kontroll_VALUE·동시 프로세스·PTY |
| C/AOT ndërtoj_burim | 게스트 TinyCC 및 statik_VALUE Java 부분집합 `jaot` → 자체 ARM64 ELF | 전체 libc·모든 Java klasë_VALUE AOT |
| C++ | 독립 ELF64를 EL0에서 zbatoj_komandë; statik_VALUE 생성자, RAII 소멸자, FP/SIMD, 한국어 Kartelë/루프백 호출 | libc/libstdc++, STL, C++ përjashtim·RTTI·동적 Lidhu |
| përdorues mbroj_VALUE | 4 KiB 페이지, kod_VALUE RX/të_dhëna RW·NX, bërthamë_VALUE·MMIO 차단, guard page, 잘못된 tregues 검사 | 다중 përdorues leje_VALUE, 일반 프로세스/스레드 스케줄러 |
| zbatoj_komandë Ora_VALUE_4692cef5 제한 | GIC-400 타이머로 무한 përsëritje_VALUE dal_program; ndërvepruese 입력 대기는 기한 freskoj, 터미널별 EL0 program_f5044b9b 중단·재개 | 일반적인 선점형 다중작업. 긴 bërthamë_VALUE 호출 도중에는 종료가 지연될 수 있음 |
| Kartelë | Java RAM Kartelë 64개 × 16384바이트, 루트를 포함한 디렉터리 16개, homolog_VALUE/절대 POZICIONI 63바이트, 서술자 16개 | leje_VALUE, 디스크/SD 영속 Store_VALUE |
| 네트워크 | lwIP IPv4 TCP/UDP/ARP/ICMP, SLIP, GENET/PHY·DHCP 구현, 게스트 FTP·SSH·VNC | GENET 실물 vlerësoj, Wi-Fi, DNS, 일반 TLS 소켓, RDP |
| GUI | 최대 네 Terminali Dritare, përzgjedhje_VALUE·lëviz_VALUE·X Mbyll, 한글 font_VALUE, Swing 부분집합; 게스트 VNC 화면·입력·두벌식 | 실물 USB 입력, 전체 AWT/Swing·Java2D·Dritare 관리 정책 |
| 작업 thread_VALUE | bërthamë_VALUE 작업 2개와 주 작업; JVM 내부 thread_VALUE 최대 4개, start/join/yield·synchronized | pthread, SMP, Java Thread 전체 API |
| 다국어 | UTF-16 리터럴→UTF-8 UART, 한글·일본어·아랍어·이모지, UTF-8 skedar_emër_SMS/전문 | GUI의 일반 다국어 조판 |

zbatoj_komandë 버튼 화면은 5×7 영문 글꼴을 쓰며, Terminali 창은 Noto CJK/DejaVu에서 생성한 한글·Unicode 비트맵 글꼴을 쓴다. UART와 aktual_të_dhëna 프레임버퍼의 한글 표시를 시험한다. 루프백은 동일 bërthamë_VALUE 내부의 전문 전달이며 IP 패킷을 Ethernet으로 내보내는 드라이버가 아니다. 바깥 IPv4는 lwIP TCP/UDP 스택으로 보조 UART SLIP 경로를 사용한다. `python3 Mjete/zbatoj_komandë.py --network`로 QEMU NAT를 연결하고 `ftpd start`로 서비스를 시작한다.

Java의 정확한 API·문법·zbatoj_komandë 제한과 한국어 사용법은 [자체 JVM과 한국어 bibliotekë](자바실행환경.md)에 정리했다. klasë_VALUE Kartelë/JAR 배포는 [한국어자바](한국어자바) 소스에서 재현한다. 기존 Linux판 `한국어.자바`와 별도인 `한국어.자체` 패키지다.

**vi·여러 Dritare·Swing·한글 Java/Python/C/C++·posix-kor 예제는 [한글 개발 매뉴얼](개발안내.md)에 정리했다.**

GUI Terminali zbatoj_komandë·단축키·pasues Komanda·제한은 [셸과 Terminali 사용법](pasues_AND_Terminali.md)에 정리했다.

## 현재 컴퓨터에서 zbatoj_komandë

```sh
cd /home/user/jkoros/platforms/rpi4-native
make test
make run
```

dal_program: **Ctrl+A Tjetër_njësi X**. 게스트 C/AOT Mjete 빌드에는 `make rpi-prepare`로 준비한 ARM64 SDK 헤더와 libgcc 산술 보조 함수도 필요하다. libc나 Linux 커널을 게스트에 넣는 것은 아니다. pritës 도구는 JDK 11 이상, Python 3.6 이상, Clang/Clang++, AArch64 GNU binutils, Make, `libnewlib-dev` 헤더다. MicroPython은 `/usr/include/newlib` 헤더를 사용하며 다른 위치는 `NEWLIB_INCLUDE`로 지정한다. newlib 런타임을 이식·링크한 것은 아니다. 컴파일러 의미 비교에는 GCC/UBSan도 사용한다. 기존 `../rpi4/build/host`의 QEMU 11.0.3이 있으면 이용하며, 그렇지 않으면 PATH의 QEMU를 사용한다. `QEMU_AARCH64=/절대/POZICIONI/qemu-system-aarch64`로 지정할 수도 있다. `raspi4b` Mbështetje_VALUE 여부를 확인한 후 실행한다.

명령은 **Enter를 눌러 zbatoj_komandë**한다. 기존 한 karakter_VALUE 명령도 Enter가 필요하다.

```text
javac Hello.java
java Hello "한글 Argumente 😀"
python hello.py
python -c 'print(2**100)'
ls
cat python.txt
run cpp
net test
gui
```

| Komanda | Veprim |
|---|---|
| `help` / `info` | Komanda·aktual_të_dhëna 구현 status_VALUE |
| `ls` / `cat FILE` / `rm FILE` | RAM Kartelë futje_Listë·Përmbajtje_VALUE·삭제 |
| `vi FILE` | përdorues 영역 vi 부분집합, 한글 redaktim_VALUE·Store_VALUE·검색·되돌리기 |
| `edit FILE` | Kartelë 전체를 새로 입력; 단독 `.` 줄로 Store_VALUE, Ctrl-C로 Anulo_operim |
| `javac FILE.java` / `java CLASS [ARGS]` | 자체 제한형 Java ndërtoj_burim·zbatoj_komandë |
| `python FILE.py [ARGS]` / `python -c 'CODE'` | MicroPython ndërtoj_burim·zbatoj_komandë |
| `load FILE` / `hex FILE` | 16진수 바이너리 입력/출력; 입력은 단독 `.` 줄로 Store_VALUE |
| `run FILE.elf [ARGS]` / `run cpp` | 업로드한 자체 ABI ELF / 내장 C++ 예제 |
| `net test` / `tasks` / `selftest` | UDP 루프백 / 협력식 작업 / EL0 mbroj_VALUE 시험 |
| `gui` / `terminal` | zbatoj_komandë 화면 / 한글 GUI Terminali; F12로 Terminali Hap·Mbyll |
| `samples` | 삭제한 vlerë_e_parazgjedhur 예제 rikuperoj_status; 기존 파일은 보존 |

예를 들어 `edit 인사.java`를 입력한 Tjetër_njësi 아래 소스를 입력한다.

```java
public class 인사 { public static void main(String[] args) { int VALUE = 7; System.out.println("한글=" + VALUE); } }
```

그다음 단독 `.` 줄로 저장하고 `javac 인사.java`, `java 인사`를 실행한다. 편집기는 기존 파일에 커서를 이동하는 방식이 아니라 전체 교체 방식이다. Anulo_operim·잘못된 16진수·용량 초과는 원본을 보존한다. 줄은 4096바이트, 파일은 16384바이트, zbatoj_komandë 인수는 최대 8개·각각 UTF-8 255바이트다. 일반 Komanda 인수는 최대 32개다. Citim·백슬래시·pasues 변수·파이프·리다이렉션 범위는 [pasues 설명](pasues_AND_Terminali.md)을 참고한다.

GUI 터미널은 다음과 같이 실행하고 Remmina에서 **VNC**, email **127.0.0.1:5902**로 연결한다. 키보드·한글 Unicode 입력·명시적 ngjit_VALUE·zbatoj_komandë 버튼의 마우스 클릭을 QEMU 도구가 UART에 전달한다.

```sh
make desktop
# GUI + 네트워크: python3 Mjete/zbatoj_komandë.py --desktop --network
# 다른 포트: python3 Mjete/zbatoj_komandë.py --desktop --port 5903
```

종료는 실행한 pritës 터미널에서 Ctrl+C다. 기존 `python3 Mjete/zbatoj_komandë.py --vnc 127.0.0.1:2`는 화면 보기와 별도 UART 입력을 유지한다. `make run`은 일반 UART 셸이다. aktual_të_dhëna Pi4 USB 입력기는 아직 없으며, VNC Lidhu 도구는 QEMU 시험용이다.

GUI의 다섯 버튼은 aktual_të_dhëna C++/UDP ELF zbatoj_komandë, `Hello.java` ndërtoj_burim 후 JVM zbatoj_komandë, `hello.py` zbatoj_komandë, GUI Terminali 열기를 수행한다. 한 번에 한 프로그램이 CPU에서 실행되며 일반 실행에는 약 2초 기한이 있다. vi·Swing은 ndërvepruese 대기에서 기한을 갱신하고 다른 터미널로 전환할 때 Memorie_të_dhëna·CPU 문맥을 보관한다. pasues·편집기에서 입력을 기다리는 시간에는 이 제한이 적용되지 않는다.

## aktual_të_dhëna 산출물과 Pi4 SD ndërtoj_IMAGE

```sh
make image   # bërthamë_VALUE, SD ndërtoj_IMAGE, 부팅 ZIP, 사용자용 SDK
make sdk     # SDK만 다시 gjeneroj
```

| POZICIONI | 용도 |
|---|---|
| `build/kernel8.img` | 자체 bërthamë_VALUE 기계어, 적재 email 0x80000 |
| `build/kernel.elf`, `kernel.map` | bërthamë_VALUE simbol_VALUE·lidh_Navigimi |
| `build/user/demo.elf` | përdorues MODE_VALUE C++ Kartelë/힙/실수/그래픽 예제 |
| `build/user/network.elf` | përdorues MODE_VALUE C++ UDP 루프백 예제 |
| `build/user/java-tools.elf` | 자체 Java 부분집합 컴파일러/JVM, 전체 JDK/JRE 아님 |
| `dist/jkoros-native-korean.jar` | pritës javac용 한국어 API klasë_VALUE; 같은 클래스가 자체 JVM에도 내장됨 |
| `dist/jkoros-native-korean-sources.zip` | 한국어 API Java BURIMI |
| `build/user/vi.elf` | 자체 UTF-8 vi Komanda 부분집합 Redaktori |
| `build/user/python.elf` | 자체 ABI용 MicroPython 1.24.1, CPython 아님 |
| `build/user/fault.elf` | 의도적 침범/무한 반복을 수행하는 mbroj_VALUE 시험 전용 |
| `build/libposix-kor-arm64.a` | **bërthamë_VALUE 내부**에서 Java Kartelë 구현을 직접 부르는 기존 Lidhu |
| `build/libposix-kor-user.a` | **EL0 përdorues program_f5044b9b**에서 SVC로 Kartelë/루프백을 호출하는 새 Lidhu |
| `dist/jkoros-native-rpi4.img` | 128 MiB MBR/FAT32 SD ndërtoj_IMAGE |
| `dist/jkoros-native-rpi4-boot.zip` | FAT32 부팅 파티션에 복사할 Kartelë grup_VALUE |
| `dist/jkoros-native-aarch64-sdk.tar.gz` | 사용자용 헤더·Ekzekuto kod_VALUE·bibliotekë·링커 skript_VALUE·예제 |
| `dist/manifest.json`, `build/build.json` | SHA256과 aktual_të_dhëna Mbështetje_VALUE status_VALUE |

이미지는 확인된 공식 Pi 부팅 묶음에서 `start4.elf`, `fixup4.dat`, Pi4 DTB와 disable-bt overlay를 가져온다. Linux kernel/initramfs/rootfs는 넣지 않는다. 펌웨어·MicroPython·Terminali font_VALUE 라이선스와 font_VALUE 출처 해시도 동봉한다. Kartelë gjeneroj 스크립트는 물리 디스크에 기록하지 않는다.

예비 microSD에 ndërtoj_IMAGE LOG_RECORD 도구로 `.img`를 기록하거나 FAT32 부팅 파티션 최상위에 ZIP 내용을 푼다. ndërtoj_IMAGE 기록은 선택한 카드의 기존 내용을 지우므로 대상을 확인한다. Pi4 vlerë_e_parazgjedhur EEPROM SD 부팅을 전제로 한다. UART는 **3.3V TTL, 115200 8N1**, GPIO14/TXD(8번)→어댑터 RX, GPIO15/RXD(10번)→TX, GND(6번) 연결이다. GPIO에 5V 신호를 연결하지 않는다.

**실물 Pi4 부팅은 미검증이다.** QEMU `-kernel`은 SD의 VideoCore 펌웨어를 실행하지 않고 커널을 직접 적재한다. SD Kartelë 구성·bërthamë_VALUE 체크섬 검사와 물리 panel 부팅 검증은 별개다. MMU 사용 전에는 펌웨어의 캐시/MMU가 꺼져 있고 EL1 또는 EL2로 진입하는 통상 부팅 조건을 전제로 한다. 세 보조 코어는 대기시키며 한 코어만 사용한다.

## C++와 한국어 API 사용

SDK를 풀고 호스트에서 컴파일한다.

```sh
tar -xzf dist/jkoros-native-aarch64-sdk.tar.gz -C build
cd build/jkoros-native-sdk
python3 compile.py examples/파일예제.cpp -o demo.elf
python3 compile.py examples/통신예제.cpp -o network.elf
```

진입점은 `extern "C" int nis_përdorues_program(int)`이다. përdorues C++는 FP/SIMD를 사용할 수 있다. bërthamë_VALUE C/Java AOT는 일반 레지스터만 사용하므로 përjashtim Proces_VALUE_futje 중 përdorues FP 상태를 건드리지 않는다. përdorues futje_p_VALUE 시 FP 상태를 초기화하고 bërthamë_VALUE 복귀에 필요한 상태를 보존한다.

```cpp
#include "파일규약.h"
extern "C" int nis_përdorues_program(int) {
    int Kartelë = hap_skedar("인사.txt", lexoj_shkruaj | 없으면만들기 | 내용비우기, 0600);
    if (Kartelë < 0) return 1;
    const char Përmbajtje_VALUE[] = "안녕하세요";
    int llogaritje = shkruaj_skedar_të_dhëna(Kartelë, Përmbajtje_VALUE, sizeof(Përmbajtje_VALUE) - 1);
    mbyll_skedar(Kartelë);
    return llogaritje == sizeof(Përmbajtje_VALUE) - 1 ? 0 : 2;
}
```

[Kartelë 예제](përdorues/파일예제.cpp)와 [통신 예제](përdorues/통신예제.cpp)가 aktual_të_dhëna 부팅 시험 대상이다. `파일규약.h`의 이름은 커널용/사용자용 모두 같지만 **링크하는 라이브러리가 다르다**. 사용자용은 `svc #0`으로 호출하고 Kartelë Proces_VALUE_futje 및 루프백 전달은 Java 커널에서 실행한다. `통신규약.h`의 소켓 함수는 현재 사용자용 라이브러리에 구현돼 있다.

새 프로그램은 bërthamë_VALUE 재빌드 없이 `load FILE.elf`와 `run FILE.elf`로 실행한다. 호스트에서 Tjetër_njësi 도구를 사용하면 **새 QEMU를 부팅해 업로드한 aktual_të_dhëna 바이트를 재확인한 PAS_VALUE 게스트에서 zbatoj_komandë**하고 종료한다. 이 도구의 새 VM에서 만든 RAM 자료는 종료할 때 사라진다.

```sh
cd /home/user/jkoros/platforms/rpi4-native
python3 Mjete/zbatoj_skedar.py build/jkoros-native-sdk/demo.elf
python3 Mjete/zbatoj_skedar.py 예제/Hello.java "한글 Argumente"
python3 Mjete/zbatoj_skedar.py 예제/hello.py
```

이 경로는 16KiB 이하의 `.elf`, `.java`, `.class`, `.py`를 지원한다. 큰 내장 Java/MicroPython ELF 자체는 bërthamë_VALUE 묶음에 포함되어 이 Kartelë 한도를 적용받지 않는다. **C++ 컴파일러는 pritës SDK의 Clang++**이며 게스트 내부 GCC/Clang 컴파일러는 아직 없다. SDK만으로 일반 Linux 프로그램을 실행할 수는 없다. Linux ELF, 동적 bibliotekë, PT_TLS, PT_INTERP, PT_DYNAMIC, zbatoj_komandë·Shkrimi 겸용 세그먼트는 로더가 거부한다. 구체적인 호출 INDEX·email fragment·오류는 [përdorues ABI](사용자호출규약.md)를 참고한다.

RAM 파일은 재부팅 시 사라진다. `파일저장확정`은 -1과 ENOSYS를 반환한다. 파일의 mode 인수를 저장하지 않으며 leje_VALUE·dup/fcntl은 없다. 디렉터리와 homolog_VALUE/절대 경로는 같은 RAM 저장소에서 처리한다. UDP 전문은 최대 512바이트, 소켓은 8개, 수신 큐는 소켓당 4개다. 수신할 자료가 없거나 큐가 가득 차면 EAGAIN을 반환한다. përdorues dal_program 시 열린 Kartelë 서술자와 소켓을 회수한다.

## vlerësoj llogaritje

`make test-jvm`은 9개 프로그램을 OpenJDK와 aktual_të_dhëna 자체 커널에서 실행해 결과를 비교한다. `make test`에도 포함된다. 별도 `Mjete/부팅시험.py`는 Java 사각형 API의 aktual_të_dhëna 화면 픽셀까지 검사한다. `make test-shell`, `make test-desktop`은 새 셸과 aktual_të_dhëna VNC 입력·한글 Terminali 화면을 검사하며 `make test`에도 포함된다.

`make test-windows`, `make test-swing`, `make test-stream`, `make test-coding`도 제공하며 `make test`에 포함된다.

`make test`는 OpenJDK와 AOT operim_VALUE llogaritje 비교, 런타임 GABIM 중단, 미지원 Java 거부와 함께 별도 QEMU VM에서 다음을 검사한다.

- 기존 Java bërthamë_VALUE 계산·UTF-8·C++ 직접 호출·협력식 작업 및 프레임버퍼.
- 손상/잘못된 ABI/email 초과/겹친 페이지/W+X 등 ELF refuzo_VALUE 사례 22개.
- EL0 C++ 생성자·RAII·실수 operim_VALUE·Kartelë·힙 및 잘못된 시스템 호출 tregues.
- bërthamë_VALUE/kod_VALUE/MMIO Shkrimi·qasem_futje, NX 스택·NULL zbatoj_komandë, guard page, 특권 Komanda 차단.
- SVC를 호출하지 않는 무한 반복을 타이머로 종료한 후 정상 program_f5044b9b 재실행.
- përsëritje_VALUE zbatoj_komandë 시 Kartelë/소켓 누수 방지, UDP 왕복·보낸 email·잘린 수신·큐 포화·빈 전문·미지원 통신 GABIM.
- pasues redaktim_VALUE·Anulo_operim·16진수 업로드/다운로드·përdorues ELF 실행과 잘못된 ELF refuzo_VALUE.
- 게스트 Java → OpenJDK `-Xverify:all`, OpenJDK → 게스트 JVM 교차 zbatoj_komandë, 한글 klasë_VALUE·변수·skedar_emër_SMS.
- 여러 Dritare·vi Store_VALUE·redaktim_VALUE·Kthe_urë·përdorues status_VALUE 중단/재개, Swing 한글 입력·이벤트·X Mbyll, 연결형 루프백, C/C++ 한글 SDK 예제.
- MicroPython Unicode·큰 numër_i_plotë·klasë_VALUE·GC përsëritje_VALUE·Kartelë import·përjashtim·Kartelë·UDP 왕복·Ora_VALUE_4692cef5 초과 후 복귀.
- GUI përzgjedhje_VALUE lëviz_VALUE, C++/UDP/Java/MicroPython 버튼 zbatoj_komandë, 콘솔 복귀 및 aktual_të_dhëna 프레임버퍼 픽셀/font_VALUE.
- 디렉터리·변수·kusht·Kartelë Komanda·skript_VALUE·순차 파이프·리다이렉션·용량 초과 rikuperoj_status, Python stdin/EOF와 Java/Python stdout.
- Komanda LOG_RECORD·긴 한글 입력 redaktim_VALUE·완성·Terminali 스크롤, 그래픽 program_f5044b9b dal_program 후 Dritare 복원, aktual_të_dhëna VNC Unicode tast_VALUE·ngjit_VALUE·마우스.

[bërthamë_VALUE 시험 LOG_RECORD](build/verification/implementation-test.log), [pasues 시험](build/verification/shell/report.json), [VNC 시험](build/verification/desktop/report.json), [makinë 판독 llogaritje](build/verification/report.json), [직렬 LOG_VALUE](build/verification/serial.log), [GUI 화면](build/verification/gui-python.png)을 확인할 수 있다. VNC RFB 3.8 Lidhu 및 640×480 화면 정보도 검사한다. [SDK 재컴파일 llogaritje](build/verification/sdk.json)는 두 예제의 futje_p·적재 세그먼트·ABI note가 부팅 시험한 ELF와 일치함을 확인한다. simbol_VALUE 등 비적재 메타데이터를 포함한 Kartelë 전체의 SHA256까지 같다고 의미하지는 않는다.

## Java와 Python의 정확한 fragment

자체 `javac`는 버전 49 `.class`를 생성하며 JVM은 Mbështetje_VALUE 명령으로 구성된 버전 45–52 클래스를 실행한다. statik_VALUE FUNCTION_VALUE·재귀·int/boolean/char/String·kusht/përsëritje_VALUE·varg_VALUE 결합과 일부 Kartelë 스트림을 지원한다. UTF-8 문자열과 문자 리터럴, ASCII 및 현대 한글 음절/조합 자모 식별자를 처리한다. Unicode identifikues_VALUE 전체 LOOKUP_tabelë·Unicode burim_degëzim 이스케이프는 구현하지 않았다. 게스트 burim_degëzim 컴파일러는 일반 objekt_VALUE·përjashtim·Thread 구문을 아직 컴파일하지 못한다. pritës `javac --release 8`로 만든 Mbështetje_VALUE 부분집합 클래스는 자체 JVM 0.4의 objekt_VALUE·përjashtim·Thread·UDP와 한국어 API를 사용할 수 있다. Swing은 문서화한 자체 API 부분집합을 제공하며 JAR 로더는 제공하지만 전체 AWT/Swing·JDK 표준 라이브러리는 없다. 정확한 범위는 [자체 JVM 설명](자바실행환경.md)이 기준이다. 상세 Gjuha 범위는 [공유 Java Mjete 설명](../../문서/자바개발환경.md)을 참고하되, 그 문서의 x86 pasues/Store_VALUE/실행시간과 이 ARM64 판의 차이에 유의한다.

MicroPython은 공식 **1.24.1 burim_degëzim**를 자체 AArch64 EL0/SVC 대상으로 빌드했다. Python 문법의 FUNCTION_VALUE·klasë_VALUE·përjashtim·리스트/fjalor·Unicode·GC·가변 정밀도 정수를 제공한다. 현재 구성은 numër_i_plotë 빌드로 `float`, `complex`, `math`가 없으며 CPython 전체 표준 bibliotekë, pip, subprocess, threading, 일반 socket과 vlerë_e_parazgjedhur `open()` Kartelë 객체는 제공하지 않는다. `python FILE.py` 및 `-c` 실행만 제공하며 REPL은 아직 없다. 각 실행의 objekt_VALUE·모듈은 dal_program 시 회수되고 RAM 파일만 Tjetër_njësi 실행에 남는다.

`import jkoros`로 Tjetër_njësi 시스템 연결을 쓴다. 모두 SVC를 통해 자체 Java 커널에 접근한다.

| FUNCTION_VALUE | Veprim |
|---|---|
| `stdin(limit)` | 현재 표준 입력에서 최대 limit바이트(0…16384)를 bytes로 읽음; EOF는 빈 bytes, UART të_dhëna 없음은 OSError(11) |
| `read(name)` | homolog_VALUE/절대 RAM 경로의 Kartelë 전체를 bytes로 읽음 |
| `write(name, data)` | str/bytes 버퍼를 RAM 파일에 새로 Store_VALUE, 쓴 bajt_VALUE 수 Kthe_llogaritje |
| `remove(name)` | RAM Kartelë 삭제 |
| `rect(x, y, w, h, color)` | 선택한 aktual_të_dhëna 화면 Madhësi 안의 사각형 vizatim_VALUE; 기존 보드의 RGB32 VALUE |
| `ticks_ms()` | 부팅 후 밀리초, 32비트 Cikël_VALUE |
| `udp_open(port)` | 127.0.0.1의 UDP 소켓 Hap/묶기; 0은 자동 포트 |
| `udp_send(fd, port, data)` | 루프백 vendmbërritje_VALUE 포트에 str/bytes 버퍼 transferim_VALUE |
| `udp_recv(fd)` | `(bytes, 보낸포트)` Kthe_llogaritje; 비어 있으면 `OSError(11)` |
| `udp_close(fd)` | 소켓 Mbyll |

```python
import jkoros
first = jkoros.udp_open(9401)
second = jkoros.udp_open(9402)
jkoros.udp_send(first, 9402, b"hello")
print(jkoros.udp_recv(second))  # (b'hello', 9401)
jkoros.udp_close(first)
jkoros.udp_close(second)
```

이식 kod_VALUE: [python/](PYTHON_urë/), [përdorues Java Lidhu](përdorues/자바연결.c). 공식 [MicroPython 이식 LEXOMË_eb81d7d9](https://docs.micropython.org/en/latest/develop/porting.html)를 참고했다. burim_degëzim URL·hash_skedar·라이선스는 [vendor LEXOMË_eb81d7d9](vendor/README.md)에 기록했다.

## 남은 작업

| Tjetër_njësi fazë_VALUE | 완료 Project_rrënjë |
|---|---|
| 영속 Store_VALUE·zbatoj_komandë Kartelë 입력 | SD/MMC 및 디스크 Kartelë 시스템, 시스템/përdorues 볼륨; 현재 ELF Kartelë 실행은 RAM에 한정 |
| 일반 프로세스·스레드 | 프로세스별 email 공간, 선점 스케줄러, TLS, sinkronizoj/Prit_VALUE, 신호, mmap/mprotect |
| libc와 C++ 런타임 | 자체 ABI용 libc, malloc/free, 표준 I_O·Ora·환경·locale, libstdc++/përjashtim Proces_VALUE_futje vlerësoj |
| CPython | 해당 libc와 OS API 대상으로 이식·교차 빌드하고 Kartelë/Unicode/스레드/소켓 시험 |
| OpenJDK/JRE | HotSpot OS Shtresë_VALUE, GC/JIT/스레드/신호/동적 연결과 Java 네이티브 bibliotekë 이식; javac/java aktual_të_dhëna zbatoj_komandë |
| 외부 네트워크 | 추가한 GENET/PHY·DHCP 드라이버의 aktual_të_dhëna panel 송수신 vlerësoj, DNS·Wi-Fi |
| GUI shtesë_VALUE | USB HID, 게스트 입력기·문자 조판, Swing Dritare Madhësi 조절·클리핑 shtesë_VALUE, 전체 AWT/Swing 이식 |

이 표는 남은 작업이며 구현 완료 목록이 아니다. QEMU Pi4 모델에는 GENET Ethernet과 PCIe root port가 없어 외부 네트워크 드라이버는 실물 검증도 필요하다. [QEMU pajisje_VALUE 지원표](https://www.qemu.org/docs/master/system/arm/raspi.html)

하드웨어 및 ABI 참고: [BCM2711 aksesor](https://datasheets.raspberrypi.com/bcm2711/bcm2711-peripherals.pdf), [Pi4 GIC email](https://github.com/raspberrypi/linux/blob/rpi-6.12.y/arch/arm/boot/dts/broadcom/bcm2711.dtsi), [mailbox punë_VALUE](https://github.com/raspberrypi/firmware/wiki/Mailbox-property-interface), [Arm ELF64](https://github.com/ARM-software/abi-aa/blob/main/aaelf64/aaelf64.rst), [Arm FP kontroll_VALUE 레지스터 Përkufizim_VALUE](https://github.com/ARM-software/arm-trusted-firmware/blob/master/include/arch/aarch64/arch.h).


## 한국어 C tipi_i_të_dhënave·Python GABIM·grupoj instaloj_VALUE

C 네트워크 API는 `struct 인터넷통신주소`, enum 상수와 aktual_të_dhëna 한국어 함수로
구현한다. makro_VALUE 별칭을 사용하지 않으며 이전 pk_* ABI도 유지한다.
Python 예제는 `sistem_gabim`, `GABIM.INDEX`, `GABIM.설명`을 사용한다.

`python3 Mjete/zbatoj_komandë.py --desktop --network --pip`로 시작하면 게스트에서
`pip install micropython-bisect==3.3.3`을 사용할 수 있다. 현재는 pritës 중계를
이용하는 제한형 MicroPython burim_degëzim 설치기이며 CPython pip·자동 의존성 해결·C 확장은
미지원이다. 설치한 `/lib` 자료는 RAM이다. [사용법과 제한](PYTHON_grupoj.md).

## 화면 Madhësi përzgjedhje_VALUE

`python3 Mjete/zbatoj_komandë.py --desktop --network --resolution 1920x1080`으로 Full HD 화면을 사용한다. 기본값은 640×480이며 1280×720도 가능하다. Terminali lëviz_VALUE, Swing 가운데 lidh_Navigimi, Java·C·Python 그리기도 aktual_të_dhëna 크기를 따른다. SD 영상은 `make image RESOLUTION=1920x1080`으로 만든다. [Rregullime·한국어 API·vlerësoj LEXOMË_eb81d7d9](화면해상도.md).

## 한국어 직접 API와 화면 freskoj

`example/java`는 `실행할일`, `동작받이`, `동작알림`, `Buton`, `ngjarje_radhë`,
`작업가닥`, `Ekzekuto()`을 사용할 수 있다. 한국어 GUI/가닥을 자체 JVM에 직접
연결했으며, 표준 Swing/Thread를 감싸지 않는다. varg_VALUE 등 javac의 표준
계약과 전체 burim_degëzim 검토 범위는 [명명 LEXOMË_eb81d7d9](명명/LEXOMË_eb81d7d9.md), 사용법과 호환성 변경은
[한국어 Java API](한국어자바/LEXOMË_eb81d7d9.md)를 본다.

Terminali lëviz_VALUE·Madhësi 변경은 바뀐 영역만 합성하고 달라진 화소만 표시한다.
[화면 freskoj 설명](자바실행환경.md#Terminali-부분-freskoj),
[부분 freskoj 검사](build/verification/redraw/report.json)를 참고한다.
