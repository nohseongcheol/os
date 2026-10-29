# Raspberry Pi 4 oma Java ydin_ARVO — käyttäjätila Suorita_komento 기반

nykyinen_kohde oma 코드의 COSL 상업 ehto, 제3자 고지 및 LGPL 재연결 자료는 [COSL jakelu_ARVO Lueminut_eb81d7d9](COSL배포안내.md)를 참고한다. MUUTA_tila 전 GPL 구성의 판단은 [Edellinen_kohde 라이선스 검토](lisenssi_arvostelu.md)에 기록했다.

suomi 통신·poikkeus 사용법은 [suomi Java API](한국어자바/Lueminut_eb81d7d9.md), funktio_ARVO·muuttuja_ARVO·tiedoston_nimi 이름의 변경과 어원 근거는 [명명 Lueminut_eb81d7d9](명명/Lueminut_eb81d7d9.md)를 참고한다.

Linux 없이 부팅하는 oma AArch64 커널이다. Java AOT ydin_ARVO 위에 **komentorivi liittymä, 게스트 Java kääntäjä·JVM, MicroPython, EL0 C++ Suorita_komento, tiedoston_nimi·UDP 루프백 시스템 호출, 여러 한글 GUI komentotulkki·vi editori·Swing 부분집합**을 제공한다. 커널의 tiedoston_nimi data/정책·루프백 Siirrä_ARVO·liittymä 상태는 Java, 화면 합성·kuvapiste muuttaa_ARVO·osoitin·클리핑도 Java로 구현하며, CPU/MMU/laite_ARVO 경계와 komentotulkki·merkki_ARVO 그리기 연결은 C와 어셈블리다.

**전체 JDK/JRE·CPython·표준 C++ 런타임·Swing 이식은 아직 완료되지 않았다.** 기존 [ARM64 Linux 실행판](../rpi4/README.md)의 OpenJDK/Python 패키지를 이 oma 커널에 탑재했다고 표시하지 않는다.

새로운 게스트 `cc`/`jaot`, JAR 직접 Suorita_komento, lwIP TCP/UDP와 FTP는 [FTP·C·JAR·AOT 매뉴얼](파일전송과번역.md)을 참고한다. 게스트 SSH·VNC와 Pi4 GENET/PHY·DHCP 드라이버를 추가했다. **SSH·VNC는 QEMU에서 검증하며, 실물 Pi4의 lanka_ARVO 송수신은 아직 미검증이다.** Suorita_komento·yhteys_e05f319b·salasana_ARVO 확인은 [ulkoinen_ARVO yhteys_e05f319b Lueminut_eb81d7d9](ulkoinen_yhteys_opas.md)에 정리했다.

셸은 EL1 ydin_ARVO, `java` 등 käyttäjätila Suorita_komento 파일은 EL0에서 실행한다.
`ps`·`top`의 표시와 제한, QEMU 네트워크 Suorita_komento·yhteys_e05f319b 방법 및 todellinen_data 검증은
[Suorita_komento 계층과 ulkoinen_ARVO 통신 점검](실행계층과외부통신점검.md)을 참고한다.

ELF는 확장자가 아닌 todellinen_data Suorita_komento 형식으로 검사한다. `./인사`처럼 확장자 없이 실행하며, 제한된 Linux ARM64 staattinen_ARVO ELF는 `run --linux tiedostonimi_SMS`으로 실행한다. [ELF·Linux ABI Tuki_ARVO 범위와 동일 바이너리 testit](실행파일규약.md).

GUI와 네트워크는 `python3 työkalut/Suorita_komento.py --desktop --network`로 함께 사용한다. Java·C·Python의 suomi 예제 13개는 [jkoros/example](../../example/README.md)에 있으며, **게스트 koneen_käynnistys 시 `/example/java`, `/example/c`, `/example/python`에 자동으로 준비된다.** `example java|c|python`으로 지운 예제를 복원할 numero 있다. Remmina에서 **F9/Shift+Space/한·nolla_operandi Avain_ARVO**로 `[EN]`↔`[KO]` 두벌식을 전환한다(`help ko`). `make test-examples`는 같은 GUI VM에서 FTP·todellinen_data TCP/UDP·tiedoston_nimi tavu_ARVO·그래픽 픽셀을 검증한다.

게스트에서 `cd /example/java` 후 `java Ikkunaesimerkki`로 suomi Swing 예제를 실행한다. komentotulkki 모서리에 마우스를 대고 **왼쪽 버튼으로 끌면 크기가 바뀐다**. `terminal size`는 nykyinen_kohde SARAKE_ARVO·RIVI_ARVO 수를 보여 준다.

## nykyinen_kohde Tuki_ARVO leikata

| 기능 | toteutus·시험한 leikata | 아직 미지원 |
|---|---|---|
| koneen_käynnistys | Pi4 AArch64 EL1, UART, SD용 kääntää_KUVA, QEMU raspi4b koneen_käynnistys | todellinen_data Pi4 보드에서의 펌웨어 koneen_käynnistys testit |
| Java ydin_ARVO | staattinen_ARVO Java 부분집합 → freestanding C → AArch64 AOT | 전체 Java objekti_ARVO/poikkeus/GC/JVM/표준 kirjasto |
| Java kehitystuote työkalut | 게스트 oma `javac`/`java`, JVM 0.4/JAR: 다중 Luokka_ARVO·objekti_ARVO·상속·poikkeus·GC·일부 컬렉션·Thread·IPv4 Socket/UDP·Swing 일부 API, suomi kirjasto. 게스트 컴파일러는 staattinen_ARVO Java 부분집합 | 전체 JDK/JRE·HotSpot·Java SE·임의의 모든 JAR·AWT/Swing 전체 |
| Python | todellinen_data MicroPython 1.24.1 EL0 이식, lähde_puu kääntää_lähde/Suorita_komento, Luokka_ARVO·poikkeus·GC·큰 kokonaisluku·Unicode·tiedoston_nimi·UDP/화면 Yhdistä | CPython, pip, C tarkenne_ARVO, 부동소수점, 일반 OS/스레드/vastake_ARVO moduuli_ARVO, vuorovaikutteinen REPL |
| liittymä | UTF-8 muutos_ARVO·LOG_TIETUE·valmis_ARVO, 디렉터리·tiedoston_nimi komento, muuttuja_ARVO·ehto·komentosarja_ARVO, 16 KiB 순차 파이프·리다이렉션, ELF Suorita_komento | 전체 POSIX sh/Bash, 작업 ohjain_ARVO·동시 프로세스·PTY |
| C/AOT kääntää_lähde | 게스트 TinyCC 및 staattinen_ARVO Java 부분집합 `jaot` → oma ARM64 ELF | 전체 libc·모든 Java Luokka_ARVO AOT |
| C++ | 독립 ELF64를 EL0에서 Suorita_komento; staattinen_ARVO 생성자, RAII 소멸자, FP/SIMD, suomi tiedoston_nimi/루프백 호출 | libc/libstdc++, STL, C++ poikkeus·RTTI·동적 Yhdistä |
| käyttäjätila suojata_ARVO | 4 KiB 페이지, KOODI_ARVO RX/data RW·NX, ydin_ARVO·MMIO 차단, guard page, 잘못된 osoitin 검사 | 다중 käyttäjätila lupa_ARVO, 일반 프로세스/스레드 스케줄러 |
| Suorita_komento AIKA_ARVO 제한 | GIC-400 타이머로 무한 sprintti_ARVO Lopeta_ohjelma; vuorovaikutteinen syöte_ARVO 대기는 기한 päivittää, 터미널별 EL0 ohjelma_f5044b9b 중단·jatka_suoritus | 일반적인 선점형 다중작업. 긴 ydin_ARVO 호출 도중에는 종료가 지연될 numero 있음 |
| tiedoston_nimi | Java RAM tiedoston_nimi 64개 × 16384바이트, 루트를 포함한 디렉터리 16개, vertaissolmu_ARVO/절대 polku_2 63바이트, 서술자 16개 | lupa_ARVO, 디스크/SD 영속 Store_ARVO |
| 네트워크 | lwIP IPv4 TCP/UDP/ARP/ICMP, SLIP, GENET/PHY·DHCP toteutus, 게스트 FTP·SSH·VNC | GENET 실물 vahvista, Wi-Fi, DNS, 일반 TLS vastake_ARVO, RDP |
| GUI | 최대 네 komentotulkki Ikkuna, valinta_ARVO·siirrä_ARVO_83b651b8·X Sulje, 한글 fontti_ARVO, Swing 부분집합; 게스트 VNC 화면·syöte_ARVO·두벌식 | 실물 USB syöte_ARVO, 전체 AWT/Swing·Java2D·Ikkuna 관리 정책 |
| 작업 säie_ARVO | ydin_ARVO 작업 2개와 주 작업; JVM 내부 säie_ARVO 최대 4개, start/join/yield·synchronized | pthread, SMP, Java Thread 전체 API |
| 다국어 | UTF-16 리터럴→UTF-8 UART, 한글·일본어·아랍어·이모지, UTF-8 tiedostonimi_SMS/datagrammi | GUI의 일반 다국어 조판 |

Suorita_komento 버튼 화면은 5×7 영문 글꼴을 쓰며, komentotulkki 창은 Noto CJK/DejaVu에서 생성한 한글·Unicode 비트맵 글꼴을 쓴다. UART와 todellinen_data 프레임버퍼의 한글 표시를 시험한다. 루프백은 동일 ydin_ARVO 내부의 datagrammi 전달이며 IP 패킷을 Ethernet으로 내보내는 드라이버가 아니다. 바깥 IPv4는 lwIP TCP/UDP 스택으로 보조 UART SLIP 경로를 사용한다. `python3 työkalut/Suorita_komento.py --network`로 QEMU NAT를 연결하고 `ftpd start`로 서비스를 시작한다.

Java의 정확한 API·문법·Suorita_komento 제한과 suomi 사용법은 [oma JVM과 suomi kirjasto](자바실행환경.md)에 정리했다. Luokka_ARVO tiedoston_nimi/JAR 배포는 [한국어자바](한국어자바) 소스에서 재현한다. 기존 Linux판 `suomi.자바`와 별도인 `suomi.oma` 패키지다.

**vi·여러 Ikkuna·Swing·한글 Java/Python/C/C++·posix-kor 예제는 [한글 kehitystuote 매뉴얼](kehitystuote_opas.md)에 정리했다.**

GUI komentotulkki Suorita_komento·단축키·liittymä komento·제한은 [셸과 komentotulkki 사용법](liittymä_JA_Pääte.md)에 정리했다.

## nykyinen_kohde 컴퓨터에서 Suorita_komento

```sh
cd /home/user/jkoros/platforms/rpi4-native
make test
make run
```

Lopeta_ohjelma: **Ctrl+A Seuraava_kohde X**. 게스트 C/AOT työkalut 빌드에는 `make rpi-prepare`로 준비한 ARM64 SDK 헤더와 libgcc 산술 보조 함수도 필요하다. libc나 Linux 커널을 게스트에 넣는 것은 아니다. isäntä 도구는 JDK 11 이상, Python 3.6 이상, Clang/Clang++, AArch64 GNU binutils, Make, `libnewlib-dev` 헤더다. MicroPython은 `/usr/include/newlib` 헤더를 사용하며 다른 위치는 `NEWLIB_INCLUDE`로 지정한다. newlib 런타임을 이식·링크한 것은 아니다. kääntäjä 의미 비교에는 GCC/UBSan도 사용한다. 기존 `../rpi4/build/host`의 QEMU 11.0.3이 있으면 이용하며, 그렇지 않으면 PATH의 QEMU를 사용한다. `QEMU_AARCH64=/절대/polku_2/qemu-system-aarch64`로 지정할 수도 있다. `raspi4b` Tuki_ARVO 여부를 확인한 후 실행한다.

명령은 **Enter를 눌러 Suorita_komento**한다. 기존 한 merkki_ARVO 명령도 Enter가 필요하다.

```text
javac Hello.java
java Hello "한글 argumentit 😀"
python hello.py
python -c 'print(2**100)'
ls
cat python.txt
run cpp
net test
gui
```

| komento | Toiminto |
|---|---|
| `help` / `info` | komento·todellinen_data toteutus Tila_ARVO |
| `ls` / `cat FILE` / `rm FILE` | RAM tiedoston_nimi merkintä_luettelo·Sisältö_ARVO·삭제 |
| `vi FILE` | käyttäjätila alue_ARVO_0e9a97ab vi 부분집합, 한글 muutos_ARVO·Store_ARVO·검색·되돌리기 |
| `edit FILE` | tiedoston_nimi 전체를 새로 syöte_ARVO; 단독 `.` 줄로 Store_ARVO, Ctrl-C로 kumota_leikkaus |
| `javac FILE.java` / `java CLASS [ARGS]` | oma 제한형 Java kääntää_lähde·Suorita_komento |
| `python FILE.py [ARGS]` / `python -c 'CODE'` | MicroPython kääntää_lähde·Suorita_komento |
| `load FILE` / `hex FILE` | 16진수 바이너리 syöte_ARVO/tulostuspaikka; 입력은 단독 `.` 줄로 Store_ARVO |
| `run FILE.elf [ARGS]` / `run cpp` | 업로드한 oma ABI ELF / 내장 C++ 예제 |
| `net test` / `tasks` / `selftest` | UDP 루프백 / 협력식 작업 / EL0 suojata_ARVO testit |
| `gui` / `terminal` | Suorita_komento 화면 / 한글 GUI komentotulkki; F12로 komentotulkki Avaa·Sulje |
| `samples` | 삭제한 oletusarvo 예제 pelastaa_Tila; 기존 파일은 보존 |

예를 들어 `edit 인사.java`를 입력한 Seuraava_kohde 아래 소스를 입력한다.

```java
public class 인사 { public static void main(String[] args) { int ARVO = 7; System.out.println("한글=" + ARVO); } }
```

그다음 단독 `.` 줄로 저장하고 `javac 인사.java`, `java 인사`를 실행한다. 편집기는 기존 파일에 커서를 이동하는 방식이 아니라 전체 교체 방식이다. kumota_leikkaus·잘못된 16진수·kapasiteetti_ARVO 초과는 원본을 보존한다. 줄은 4096바이트, 파일은 16384바이트, Suorita_komento 인수는 최대 8개·각각 UTF-8 255바이트다. 일반 komento 인수는 최대 32개다. Lainaus·백슬래시·liittymä muuttuja_ARVO·파이프·리다이렉션 범위는 [liittymä 설명](liittymä_JA_Pääte.md)을 참고한다.

GUI 터미널은 다음과 같이 실행하고 Remmina에서 **VNC**, OSOITE **127.0.0.1:5902**로 연결한다. 키보드·한글 Unicode syöte_ARVO·명시적 liitä_ARVO_8e45bfbb·Suorita_komento 버튼의 마우스 클릭을 QEMU 도구가 UART에 전달한다.

```sh
make desktop
# GUI + 네트워크: python3 työkalut/Suorita_komento.py --desktop --network
# 다른 laitteisto_portti: python3 työkalut/Suorita_komento.py --desktop --port 5903
```

종료는 실행한 isäntä 터미널에서 Ctrl+C다. 기존 `python3 työkalut/Suorita_komento.py --vnc 127.0.0.1:2`는 화면 보기와 별도 UART 입력을 유지한다. `make run`은 일반 UART 셸이다. todellinen_data Pi4 USB 입력기는 아직 없으며, VNC Yhdistä 도구는 QEMU 시험용이다.

GUI의 다섯 버튼은 todellinen_data C++/UDP ELF Suorita_komento, `Hello.java` kääntää_lähde 후 JVM Suorita_komento, `hello.py` Suorita_komento, GUI komentotulkki 열기를 수행한다. 한 번에 한 프로그램이 CPU에서 실행되며 일반 실행에는 약 2초 기한이 있다. vi·Swing은 vuorovaikutteinen 대기에서 기한을 갱신하고 다른 터미널로 전환할 때 Muisti_data·CPU 문맥을 보관한다. liittymä·편집기에서 입력을 기다리는 시간에는 이 제한이 적용되지 않는다.

## todellinen_data 산출물과 Pi4 SD kääntää_KUVA

```sh
make image   # ydin_ARVO, SD kääntää_KUVA, koneen_käynnistys ZIP, 사용자용 SDK
make sdk     # SDK만 yrittää_uudelleen_ARVO generoida
```

| polku_2 | 용도 |
|---|---|
| `build/kernel8.img` | oma ydin_ARVO 기계어, 적재 OSOITE 0x80000 |
| `build/kernel.elf`, `kernel.map` | ydin_ARVO symboli_ARVO·linkitysasettelu |
| `build/user/demo.elf` | käyttäjätila tila_ARVO C++ tiedoston_nimi/keko_ARVO/liukuluku_ARVO/그래픽 예제 |
| `build/user/network.elf` | käyttäjätila tila_ARVO C++ UDP 루프백 예제 |
| `build/user/java-tools.elf` | oma Java 부분집합 kääntäjä/JVM, 전체 JDK/JRE 아님 |
| `dist/jkoros-native-korean.jar` | isäntä javac용 suomi API Luokka_ARVO; 같은 클래스가 oma JVM에도 내장됨 |
| `dist/jkoros-native-korean-sources.zip` | suomi API Java lähdetiedosto |
| `build/user/vi.elf` | oma UTF-8 vi komento 부분집합 editori |
| `build/user/python.elf` | oma ABI용 MicroPython 1.24.1, CPython 아님 |
| `build/user/fault.elf` | 의도적 침범/무한 반복을 수행하는 suojata_ARVO testit 전용 |
| `build/libposix-kor-arm64.a` | **ydin_ARVO 내부**에서 Java tiedoston_nimi 구현을 직접 부르는 기존 Yhdistä |
| `build/libposix-kor-user.a` | **EL0 käyttäjätila ohjelma_f5044b9b**에서 SVC로 tiedoston_nimi/루프백을 호출하는 새 Yhdistä |
| `dist/jkoros-native-rpi4.img` | 128 MiB MBR/FAT32 SD kääntää_KUVA |
| `dist/jkoros-native-rpi4-boot.zip` | FAT32 koneen_käynnistys 파티션에 복사할 tiedoston_nimi Ryhmä_ARVO |
| `dist/jkoros-native-aarch64-sdk.tar.gz` | 사용자용 헤더·Suorita_2 KOODI_ARVO·kirjasto·링커 komentosarja_ARVO·예제 |
| `dist/manifest.json`, `build/build.json` | SHA256과 todellinen_data Tuki_ARVO Tila_ARVO |

이미지는 확인된 공식 Pi koneen_käynnistys 묶음에서 `start4.elf`, `fixup4.dat`, Pi4 DTB와 disable-bt overlay를 가져온다. Linux kernel/initramfs/rootfs는 넣지 않는다. 펌웨어·MicroPython·komentotulkki fontti_ARVO 라이선스와 fontti_ARVO origo_ARVO 해시도 동봉한다. tiedoston_nimi generoida 스크립트는 물리 디스크에 기록하지 않는다.

예비 microSD에 kääntää_KUVA LOG_TIETUE 도구로 `.img`를 기록하거나 FAT32 koneen_käynnistys 파티션 최상위에 ZIP 내용을 푼다. kääntää_KUVA 기록은 선택한 카드의 기존 내용을 지우므로 대상을 확인한다. Pi4 oletusarvo EEPROM SD 부팅을 전제로 한다. UART는 **3.3V TTL, 115200 8N1**, GPIO14/TXD(8번)→어댑터 RX, GPIO15/RXD(10번)→TX, GND(6번) 연결이다. GPIO에 5V 신호를 연결하지 않는다.

**실물 Pi4 부팅은 미검증이다.** QEMU `-kernel`은 SD의 VideoCore 펌웨어를 실행하지 않고 커널을 직접 적재한다. SD tiedoston_nimi 구성·ydin_ARVO 체크섬 검사와 물리 Taulu koneen_käynnistys 검증은 별개다. MMU käyttö_ARVO 전에는 펌웨어의 캐시/MMU가 꺼져 있고 EL1 또는 EL2로 진입하는 통상 koneen_käynnistys 조건을 전제로 한다. 세 보조 코어는 대기시키며 한 코어만 사용한다.

## C++와 suomi API käyttö_ARVO

SDK를 풀고 호스트에서 컴파일한다.

```sh
tar -xzf dist/jkoros-native-aarch64-sdk.tar.gz -C build
cd build/jkoros-native-sdk
python3 compile.py examples/Tiedostoesimerkki.cpp -o demo.elf
python3 compile.py examples/통신예제.cpp -o network.elf
```

진입점은 `extern "C" int alku_käyttäjä_ohjelma(int)`이다. käyttäjätila C++는 FP/SIMD를 사용할 numero 있다. ydin_ARVO C/Java AOT는 일반 레지스터만 사용하므로 poikkeus prosessi_ARVO_merkintä 중 käyttäjätila FP 상태를 건드리지 않는다. käyttäjätila aloituskohta_ARVO 시 FP 상태를 초기화하고 ydin_ARVO 복귀에 필요한 상태를 보존한다.

```cpp
#include "파일규약.h"
extern "C" int alku_käyttäjä_ohjelma(int) {
    int tiedoston_nimi = avata_Tiedosto("인사.txt", luku_ja_kirjoitus | 없으면만들기 | 내용비우기, 0600);
    if (tiedoston_nimi < 0) return 1;
    const char Sisältö_ARVO[] = "안녕하세요";
    int TULOS = kirjoitus_Tiedosto_data(tiedoston_nimi, Sisältö_ARVO, sizeof(Sisältö_ARVO) - 1);
    Sulje_Tiedosto(tiedoston_nimi);
    return TULOS == sizeof(Sisältö_ARVO) - 1 ? 0 : 2;
}
```

[tiedoston_nimi 예제](käyttäjätila/Tiedostoesimerkki.cpp)와 [통신 예제](käyttäjätila/통신예제.cpp)가 todellinen_data koneen_käynnistys testit 대상이다. `파일규약.h`의 이름은 커널용/사용자용 모두 같지만 **링크하는 라이브러리가 다르다**. 사용자용은 `svc #0`으로 호출하고 tiedoston_nimi prosessi_ARVO_merkintä 및 루프백 전달은 Java 커널에서 실행한다. `통신규약.h`의 vastake_ARVO 함수는 nykyinen_kohde 사용자용 라이브러리에 구현돼 있다.

새 프로그램은 ydin_ARVO 재빌드 없이 `load FILE.elf`와 `run FILE.elf`로 실행한다. 호스트에서 Seuraava_kohde 도구를 사용하면 **새 QEMU를 부팅해 업로드한 todellinen_data 바이트를 재확인한 BACK_ARVO 게스트에서 Suorita_komento**하고 종료한다. 이 도구의 새 VM에서 만든 RAM 자료는 종료할 때 사라진다.

```sh
cd /home/user/jkoros/platforms/rpi4-native
python3 työkalut/Suorita_Tiedosto.py build/jkoros-native-sdk/demo.elf
python3 työkalut/Suorita_Tiedosto.py 예제/Hello.java "한글 argumentit"
python3 työkalut/Suorita_Tiedosto.py 예제/hello.py
```

이 경로는 16KiB 이하의 `.elf`, `.java`, `.class`, `.py`를 지원한다. 큰 내장 Java/MicroPython ELF 자체는 ydin_ARVO 묶음에 포함되어 이 tiedoston_nimi 한도를 적용받지 않는다. **C++ 컴파일러는 isäntä SDK의 Clang++**이며 게스트 내부 GCC/Clang 컴파일러는 아직 없다. SDK만으로 일반 Linux 프로그램을 실행할 수는 없다. Linux ELF, 동적 kirjasto, PT_TLS, PT_INTERP, PT_DYNAMIC, Suorita_komento·Kirjoitus 겸용 세그먼트는 로더가 거부한다. 구체적인 호출 INDEKSI·OSOITE leikata·오류는 [käyttäjätila ABI](사용자호출규약.md)를 참고한다.

RAM 파일은 재부팅 시 사라진다. `vahvistaa_muutokset_Files`은 -1과 ENOSYS를 반환한다. 파일의 mode 인수를 저장하지 않으며 lupa_ARVO·dup/fcntl은 없다. 디렉터리와 vertaissolmu_ARVO/절대 경로는 같은 RAM 저장소에서 처리한다. UDP 전문은 최대 512바이트, 소켓은 8개, saada_ARVO 큐는 소켓당 4개다. 수신할 자료가 없거나 큐가 가득 차면 EAGAIN을 반환한다. käyttäjätila Lopeta_ohjelma 시 열린 tiedoston_nimi 서술자와 소켓을 회수한다.

## vahvista TULOS

`make test-jvm`은 9개 프로그램을 OpenJDK와 todellinen_data oma 커널에서 실행해 결과를 비교한다. `make test`에도 포함된다. 별도 `työkalut/부팅시험.py`는 Java suorakulmio API의 todellinen_data 화면 픽셀까지 검사한다. `make test-shell`, `make test-desktop`은 새 셸과 todellinen_data VNC syöte_ARVO·한글 komentotulkki 화면을 검사하며 `make test`에도 포함된다.

`make test-windows`, `make test-swing`, `make test-stream`, `make test-coding`도 제공하며 `make test`에 포함된다.

`make test`는 OpenJDK와 AOT leikkaus_ARVO TULOS 비교, 런타임 VIRHE 중단, 미지원 Java 거부와 함께 별도 QEMU VM에서 다음을 검사한다.

- 기존 Java ydin_ARVO 계산·UTF-8·C++ 직접 호출·협력식 작업 및 프레임버퍼.
- 손상/잘못된 ABI/OSOITE 초과/겹친 페이지/W+X 등 ELF hylkää_ARVO_e3ecc00b 사례 22개.
- EL0 C++ 생성자·RAII·liukuluku_ARVO leikkaus_ARVO·tiedoston_nimi·keko_ARVO 및 잘못된 시스템 호출 osoitin.
- ydin_ARVO/KOODI_ARVO/MMIO Kirjoitus·pääsy_merkintä_68aed533, NX operandi_Pino·NULL Suorita_komento, guard page, 특권 komento 차단.
- SVC를 호출하지 않는 무한 반복을 타이머로 종료한 후 tietojärjestelmät_normaali ohjelma_f5044b9b 재실행.
- sprintti_ARVO Suorita_komento 시 tiedoston_nimi/vastake_ARVO 누수 방지, UDP 왕복·보낸 OSOITE·잘린 saada_ARVO·큐 포화·빈 datagrammi·미지원 통신 VIRHE.
- liittymä muutos_ARVO·kumota_leikkaus·16진수 업로드/다운로드·käyttäjätila ELF 실행과 잘못된 ELF hylkää_ARVO_e3ecc00b.
- 게스트 Java → OpenJDK `-Xverify:all`, OpenJDK → 게스트 JVM 교차 Suorita_komento, 한글 Luokka_ARVO·muuttuja_ARVO·tiedostonimi_SMS.
- 여러 Ikkuna·vi Store_ARVO·muutos_ARVO·palauttaa_silta·käyttäjätila Tila_ARVO 중단/jatka_suoritus, Swing 한글 syöte_ARVO·이벤트·X Sulje, 연결형 루프백, C/C++ 한글 SDK 예제.
- MicroPython Unicode·큰 kokonaisluku·Luokka_ARVO·GC sprintti_ARVO·tiedoston_nimi import·poikkeus·tiedoston_nimi·UDP 왕복·AIKA_ARVO 초과 후 복귀.
- GUI valinta_ARVO siirrä_ARVO_83b651b8, C++/UDP/Java/MicroPython 버튼 Suorita_komento, 콘솔 복귀 및 todellinen_data 프레임버퍼 픽셀/fontti_ARVO.
- 디렉터리·muuttuja_ARVO·ehto·tiedoston_nimi komento·komentosarja_ARVO·순차 파이프·리다이렉션·kapasiteetti_ARVO 초과 pelastaa_Tila, Python stdin/EOF와 Java/Python stdout.
- komento LOG_TIETUE·긴 한글 syöte_ARVO muutos_ARVO·valmis_ARVO·komentotulkki 스크롤, 그래픽 ohjelma_f5044b9b Lopeta_ohjelma 후 Ikkuna 복원, todellinen_data VNC Unicode Avain_ARVO·liitä_ARVO_8e45bfbb·마우스.

[ydin_ARVO testit LOG_TIETUE](build/verification/implementation-test.log), [liittymä testit](build/verification/shell/report.json), [VNC testit](build/verification/desktop/report.json), [kone 판독 TULOS](build/verification/report.json), [직렬 LOG_ARVO](build/verification/serial.log), [GUI 화면](build/verification/gui-python.png)을 확인할 numero 있다. VNC RFB 3.8 Yhdistä 및 640×480 화면 정보도 검사한다. [SDK 재컴파일 TULOS](build/verification/sdk.json)는 두 예제의 aloituskohta·적재 세그먼트·ABI note가 koneen_käynnistys 시험한 ELF와 일치함을 확인한다. symboli_ARVO 등 비적재 메타데이터를 포함한 tiedoston_nimi 전체의 SHA256까지 같다고 의미하지는 않는다.

## Java와 Python의 정확한 leikata

oma `javac`는 버전 49 `.class`를 생성하며 JVM은 Tuki_ARVO 명령으로 구성된 버전 45–52 클래스를 실행한다. staattinen_ARVO funktio_ARVO·재귀·int/boolean/char/String·ehto/sprintti_ARVO·merkkijono_ARVO 결합과 일부 tiedoston_nimi 스트림을 지원한다. UTF-8 문자열과 문자 리터럴, ASCII 및 현대 한글 음절/kokoonpano_ARVO 자모 식별자를 처리한다. Unicode tunniste_ARVO 전체 HAKU_taulukko·Unicode lähde_puu 이스케이프는 구현하지 않았다. 게스트 lähde_puu 컴파일러는 일반 objekti_ARVO·poikkeus·Thread 구문을 아직 컴파일하지 못한다. isäntä `javac --release 8`로 만든 Tuki_ARVO 부분집합 클래스는 oma JVM 0.4의 objekti_ARVO·poikkeus·Thread·UDP와 suomi API를 사용할 numero 있다. Swing은 문서화한 oma API 부분집합을 제공하며 JAR 로더는 제공하지만 전체 AWT/Swing·JDK 표준 라이브러리는 없다. 정확한 범위는 [oma JVM 설명](자바실행환경.md)이 기준이다. 상세 Kieli 범위는 [공유 Java työkalut 설명](../../문서/Java_kehitysympäristö.md)을 참고하되, 그 문서의 x86 liittymä/Store_ARVO/실행시간과 이 ARM64 판의 차이에 유의한다.

MicroPython은 공식 **1.24.1 lähde_puu**를 oma AArch64 EL0/SVC 대상으로 빌드했다. Python 문법의 funktio_ARVO·Luokka_ARVO·poikkeus·리스트/sanakirja·Unicode·GC·가변 tarkkuus_ARVO_2bff91c1 정수를 제공한다. nykyinen_kohde 구성은 kokonaisluku 빌드로 `float`, `complex`, `math`가 없으며 CPython 전체 표준 kirjasto, pip, subprocess, threading, 일반 socket과 oletusarvo `open()` tiedoston_nimi 객체는 제공하지 않는다. `python FILE.py` 및 `-c` 실행만 제공하며 REPL은 아직 없다. 각 실행의 objekti_ARVO·모듈은 Lopeta_ohjelma 시 회수되고 RAM 파일만 Seuraava_kohde 실행에 남는다.

`import jkoros`로 Seuraava_kohde 시스템 연결을 쓴다. 모두 SVC를 통해 oma Java 커널에 접근한다.

| funktio_ARVO | Toiminto |
|---|---|
| `stdin(limit)` | nykyinen_kohde 표준 입력에서 최대 limit바이트(0…16384)를 bytes로 lukea_KR; EOF는 빈 bytes, UART data 없음은 OSError(11) |
| `read(name)` | vertaissolmu_ARVO/절대 RAM 경로의 tiedoston_nimi 전체를 bytes로 lukea_KR |
| `write(name, data)` | str/bytes 버퍼를 RAM 파일에 새로 Store_ARVO, 쓴 tavu_ARVO numero palauttaa_KR |
| `remove(name)` | RAM tiedoston_nimi 삭제 |
| `rect(x, y, w, h, color)` | 선택한 todellinen_data 화면 Koko 안의 suorakulmio piirustus_ARVO; 기존 보드의 RGB32 ARVO |
| `ticks_ms()` | koneen_käynnistys 후 밀리초, 32비트 kehä_ARVO |
| `udp_open(port)` | 127.0.0.1의 UDP vastake_ARVO Avaa/BIND_päätepiste; 0은 자동 laitteisto_portti |
| `udp_send(fd, port, data)` | 루프백 kohde_ARVO 포트에 str/bytes 버퍼 Siirrä_ARVO |
| `udp_recv(fd)` | `(bytes, 보낸포트)` palauttaa_KR; 비어 있으면 `OSError(11)` |
| `udp_close(fd)` | vastake_ARVO Sulje |

```python
import jkoros
first = jkoros.udp_open(9401)
second = jkoros.udp_open(9402)
jkoros.udp_send(first, 9402, b"hello")
print(jkoros.udp_recv(second))  # (b'hello', 9401)
jkoros.udp_close(first)
jkoros.udp_close(second)
```

이식 KOODI_ARVO: [python/](PYTHON_silta/), [käyttäjätila Java Yhdistä](käyttäjätila/자바연결.c). 공식 [MicroPython 이식 Lueminut_eb81d7d9](https://docs.micropython.org/en/latest/develop/porting.html)를 참고했다. lähde_puu URL·hajautusarvo_Tiedosto·라이선스는 [vendor Lueminut_eb81d7d9](vendor/README.md)에 기록했다.

## 남은 작업

| Seuraava_kohde vaihe_ARVO | 완료 aloite_juuri |
|---|---|
| 영속 Store_ARVO·Suorita_komento tiedoston_nimi syöte_ARVO | SD/MMC 및 디스크 tiedoston_nimi 시스템, 시스템/käyttäjätila 볼륨; nykyinen_kohde ELF tiedoston_nimi 실행은 RAM에 한정 |
| 일반 프로세스·스레드 | 프로세스별 OSOITE OSOITE_alue, 선점 스케줄러, TLS, synkronoi/odottaa_ARVO, 신호, mmap/mprotect |
| libc와 C++ 런타임 | oma ABI용 libc, malloc/free, 표준 I_O·Kello·ympäristö·locale, libstdc++/poikkeus prosessi_ARVO_merkintä vahvista |
| CPython | 해당 libc와 OS API 대상으로 이식·교차 빌드하고 tiedoston_nimi/Unicode/스레드/vastake_ARVO testit |
| OpenJDK/JRE | HotSpot OS kerros_ARVO_e65604ef, GC/JIT/스레드/신호/동적 연결과 Java 네이티브 kirjasto 이식; javac/java todellinen_data Suorita_komento |
| ulkoinen_ARVO 네트워크 | 추가한 GENET/PHY·DHCP 드라이버의 todellinen_data Taulu 송수신 vahvista, DNS·Wi-Fi |
| GUI tarkenne_ARVO | USB HID, 게스트 입력기·문자 조판, Swing Ikkuna Koko 조절·클리핑 tarkenne_ARVO, 전체 AWT/Swing 이식 |

이 표는 남은 작업이며 toteutus 완료 목록이 아니다. QEMU Pi4 모델에는 GENET Ethernet과 PCIe root port가 없어 ulkoinen_ARVO 네트워크 드라이버는 실물 검증도 필요하다. [QEMU laite_ARVO 지원표](https://www.qemu.org/docs/master/system/arm/raspi.html)

laitteisto_ARVO 및 ABI 참고: [BCM2711 lisälaite](https://datasheets.raspberrypi.com/bcm2711/bcm2711-peripherals.pdf), [Pi4 GIC OSOITE](https://github.com/raspberrypi/linux/blob/rpi-6.12.y/arch/arm/boot/dts/broadcom/bcm2711.dtsi), [mailbox sopimuksen_arvo](https://github.com/raspberrypi/firmware/wiki/Mailbox-property-interface), [Arm ELF64](https://github.com/ARM-software/abi-aa/blob/main/aaelf64/aaelf64.rst), [Arm FP ohjain_ARVO 레지스터 Määritelmä_ARVO](https://github.com/ARM-software/arm-trusted-firmware/blob/master/include/arch/aarch64/arch.h).


## suomi C tietotyyppi·Python VIRHE·nippu asentaa_ARVO

C 네트워크 API는 `struct pilvi_vastake_OSOITE`, enum 상수와 todellinen_data suomi 함수로
구현한다. makro_ARVO 별칭을 사용하지 않으며 Edellinen_kohde pk_* ABI도 유지한다.
Python 예제는 `järjestelmävirhe`, `VIRHE.INDEKSI`, `VIRHE.설명`을 사용한다.

`python3 työkalut/Suorita_komento.py --desktop --network --pip`로 시작하면 게스트에서
`pip install micropython-bisect==3.3.3`을 사용할 numero 있다. 현재는 isäntä 중계를
이용하는 제한형 MicroPython lähde_puu 설치기이며 CPython pip·자동 의존성 해결·C 확장은
미지원이다. 설치한 `/lib` 자료는 RAM이다. [사용법과 제한](PYTHON_nippu.md).

## 화면 Koko valinta_ARVO

`python3 työkalut/Suorita_komento.py --desktop --network --resolution 1920x1080`으로 Full HD 화면을 사용한다. 기본값은 640×480이며 1280×720도 가능하다. komentotulkki siirrä_ARVO_83b651b8, Swing 가운데 linkitysasettelu, Java·C·Python 그리기도 todellinen_data 크기를 따른다. SD 영상은 `make image RESOLUTION=1920x1080`으로 만든다. [Asetukset·suomi API·vahvista Lueminut_eb81d7d9](näytön_tarkkuus.md).

## suomi 직접 API와 화면 päivittää

`example/java`는 `실행할일`, `동작받이`, `동작알림`, `painike`, `tapahtuma_jono`,
`työntekijä`, `Suorita_2()`을 사용할 numero 있다. suomi GUI/가닥을 oma JVM에 직접
연결했으며, 표준 Swing/Thread를 감싸지 않는다. merkkijono_ARVO 등 javac의 표준
계약과 전체 lähde_puu 검토 범위는 [명명 Lueminut_eb81d7d9](명명/Lueminut_eb81d7d9.md), 사용법과 호환성 변경은
[suomi Java API](한국어자바/Lueminut_eb81d7d9.md)를 본다.

komentotulkki siirrä_ARVO_83b651b8·Koko 변경은 바뀐 영역만 합성하고 달라진 화소만 표시한다.
[화면 päivittää 설명](자바실행환경.md#komentotulkki-부분-päivittää),
[부분 päivittää 검사](build/verification/redraw/report.json)를 참고한다.
