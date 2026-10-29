# 셸에서 실행하는 gebruikersruimte 프로그램과 UDP

게스트에서 일반적인 `main(String[] args)` 형식의 소스를 직접 작성하고 컴파일하려면 [제한형 Java ontwikkeling omgeving LEESMIJ_eb81d7d9](../../Guides/Java_IDE.md)를 참고한다. 아래의 네이티브 ELF 개발과 별도로 `javac FILE.java`, `java CLASS`를 제공한다.

## 바로 Uitvoeren_opdracht

host terminal 1:

```sh
cd /home/user/jkoros
python3 os/hulpmiddelen/echo_gegevens.py --port 9000
```

이 서버는 `127.0.0.1`에만 바인딩한다. extern_WAARDE 연결을 받도록 방화벽이나 hardware_poort 전달을 변경하지 않는다. Ctrl+C로 종료한다.

host terminal 2:

```sh
cd /home/user/jkoros
make run
```

게스트의 `jkoros>` 프롬프트에 invoer_WAARDE:

```text
apps
run hello first second
net
run netcheck
run udp 10.0.2.2 9000 hello
run stress 9000
```

- `hello`: 독립 Java ELF 실행과 werkelijk_gegevens CPU machtiging_WAARDE `ring 3`, argumenten tekstuitvoer.
- `netcheck`: poort_WAARDE 중복, 잘못된 greep_WAARDE/wijzer/tijdsduur_WAARDE, 비차단 받기와 TIJD_WAARDE 초과 bevestigen.
- `udp`: IPv4 ADRES·doel_WAARDE poort_WAARDE·한 Word_WAARDE 메시지를 받아 UDP로 보내고 같은 응답을 bevestigen. `UDP ECHO PASS`, `Exit: 0`이면 성공.
- `stress`: host `10.0.2.2`의 Toewijzen_WAARDE 창구와 1,023/1,024바이트 데이터그램을 24회 왕복. ontvangen_WAARDE lus_WAARDE 경계를 여러 번 지난다.

`make run`/`run-gui`는 `-netdev user,id=net0 -device rtl8139,netdev=net0`을 사용한다. actueel_item 주소는 게스트 `10.0.2.15/24`, gateway_WAARDE `10.0.2.2`로 고정돼 있다. QEMU gebruikersruimte 네트워크의 host toegang_invoer 주소를 사용한 예제다. 다른 네트워크 설정에는 맞춰 수정해야 하며 자동 DHCP는 없다. NIC 없이 실행하려면 `make -C os run NET_ARGS='-net none'`을 사용한다. 이때 app_f5044b9b 실행은 되지만 UDP 열기는 `-19`로 실패한다.

## 새 Java app_f5044b9b toevoegen_invoer

`예제/내프로그램.java`를 Volgende_item 형식으로 만든다. 진입점은 argumenten 없는 `static int` 또는 `static void` 함수다. 인수는 gebruikersruimte API로 조회한다.

```java
public final class 내프로그램 {
    public static int starten() {
        gebruikersruimte.Schrijven("My program is running in user mode.\n");
        return 0;
    }
}
```

`os/gebruikersruimte/app_f5044b9b.mk`에 추가한다.

```make
APP_NAMES += mine
APP_SOURCE_mine := gebruikersruimte/예제/내프로그램.java
APP_ENTRY_mine := 내프로그램.starten
```

여러 Java 파일을 쓰면 `APP_SOURCE_mine`에 공백으로 모두 나열한다. `gebruikersruimte/aangifte/gebruikersruimte.java`는 자동으로 함께 컴파일한다.

```sh
cd /home/user/jkoros
make iso
make run
```

새로 부팅한 셸에서 `run mine`을 실행한다. 이미 Uitvoeren_opdracht 중인 VM에는 bouwen 결과가 자동 반영되지 않는다. app_f5044b9b 이름은 actueel_item 셸의 ASCII invoer_WAARDE 제한에 맞춘 1~15자의 소문자 이름이며 Java les_WAARDE·FUNCTIE_WAARDE·변수에는 한국어를 쓴다. 최대 32개 app_f5044b9b, 한 Uitvoeren_opdracht 파일은 최대 2MiB다.

독립 ELF만 컴파일할 수도 있다.

```sh
cd /home/user/jkoros
python3 compiler/compiler.py --target user --entry 인사.starten \
    -o os/build/apps/hello.elf os/gebruikersruimte/aangifte/gebruikersruimte.java os/gebruikersruimte/예제/인사.java
```

`--target user`는 **jkoros 전용 ABI**다. Linux 대상과 시스템 호출 번호가 다르므로 host 터미널에서 직접 실행하면 안 된다. `.class`는 별도 `java CLASS` 명령의 steun_WAARDE clip 안에서 실행한다. `.jar`와 일반 Linux Uitvoeren_opdracht 파일은 지원하지 않는다.

## gebruikersruimte 네트워크 API

선언은 `aangifte/gebruikersruimte.java`에 있다. `e_mailen_gegevens`/`ontvangen_gegevens`의 `int[]` item_element 한 개는 byte_WAARDE 하나(0~255)를 나타낸다. 한 데이터그램의 최대 gegevens 길이는 1,024바이트다.

```java
int greep_WAARDE = gebruikersruimte.open_net(0); // 0: 임시 lokaal_scope UDP poort_WAARDE 자동 selectie_WAARDE
int[] gegevens = new int[32];
gegevens[0] = 'H'; gegevens[1] = 'i';
int 보낸길이 = gebruikersruimte.e_mailen_gegevens(greep_WAARDE, 0x0a000202, 9000, gegevens, 2);
int OPBRENGST_tijdsduur = gebruikersruimte.ontvangen_gegevens(greep_WAARDE, gegevens, 1500);
gebruikersruimte.Sluiten_net(greep_WAARDE);
```

werkelijk_gegevens 프로그램에서는 Openen·e_mailen·받기의 음수 반환값을 각각 검사한다. 완성된 예제는 `예제/gegevens_communicatie.java`에 있다. `ontvangen_gegevens`의 wachten_WAARDE 시간은 0~2,000밀리초이며 0은 즉시 반환이다. 받은 데이터그램이 배열보다 크면 해당 데이터그램을 버리고 `-90`을 반환한다. 창구당 ontvangen_WAARDE 대기열은 한 개뿐이므로 toevoegen_invoer 도착분은 버린다. `보낸주소`와 `보낸창구`로 마지막으로 받은 상대를 조회한다.

| 반환값 | 의미 |
| --- | --- |
| 0 이상 | greep_WAARDE·Proces_WAARDE_invoer tijdsduur_WAARDE·성공 등 해당 함수의 resultaat |
| -5 | mobiel_WAARDE e_mailen_WAARDE fout_WAARDE |
| -9 | 잘못되었거나 닫힌 communicatie greep_WAARDE |
| -11 | 비차단 받기에서 도착한 gegevens 없음 |
| -14 | gebruikersruimte wijzer/MATRIX_WAARDE clip fout |
| -19 | steun_WAARDE NIC 없음 |
| -22 | poort_WAARDE/wachten_WAARDE TIJD_WAARDE/argumenten WAARDE fout |
| -24 | 열린 net_poort 4개 한도 |
| -38 | 알 nummer 없는 시스템 호출 |
| -90 | gegevens 또는 ontvangen_WAARDE MATRIX_WAARDE Grootte 문제 |
| -98 | lokaal_scope poort_WAARDE INDEX 중복 |
| -101 | 지원하지 않는 doel_WAARDE ADRES |
| -110 | ARP·mobiel_WAARDE·ontvangen_WAARDE TIJD_WAARDE 초과 |

IP 주소는 상위 바이트부터 표기한 32비트 값이다. `10.0.2.2`는 `0x0a000202`이다. 주소를 반환하는 함수는 Encoding_WAARDE 있는 Java `int`의 bit_WAARDE 패턴을 사용하므로 상위 비트가 1인 informatie_normaal IP 주소가 음수로 보일 nummer 있다. 단순히 모든 API 반환값의 부호를 오류로 판단하면 안 된다.

## Uitvoeren_opdracht 경계와 시스템 호출

```text
Shell run → JKAP에서 ELF valideren·적재 → ring 3 gebruikersruimte app_f5044b9b
                                 ↓ int 0x80
                      wijzer 검사 → Java kernel_WAARDE API → RTL8139/UDP
                                 ↓ Einde_app·uitzondering·TIJD_WAARDE 초과
                                Shell 복귀
```

시스템 호출 레지스터는 `EAX=INDEX`, `EBX,ECX,EDX,ESI,EDI=argumenten`, `EAX=resultaat`다. Java 호출 operand_stack ABI는 컴파일러가 gebruikersruimte 스텁에서 이 형식으로 바꾼다. C의 POSIX/JNI ABI가 아니다.

| INDEX | 호출 |
| --- | --- |
| 0 | Einde_app(Status_WAARDE CODE_WAARDE) — starten/fout 런타임에서 gebruik_WAARDE |
| 1 | tekenreeks_WAARDE Schrijven |
| 2 / 3 | argumenten item_AANTAL / argumenten tekenreeks_WAARDE ADRES |
| 10 | UDP Openen |
| 11 | UDP e_mailen(greep_WAARDE, IP, doel_WAARDE poort_WAARDE, MATRIX_WAARDE ADRES, tijdsduur_WAARDE) |
| 12 | UDP ontvangen(greep_WAARDE, MATRIX_WAARDE ADRES, 제한 밀리초) |
| 13 | UDP Sluiten |
| 14 | lokaal_scope IP ADRES |
| 15 / 16 | 마지막 peer_WAARDE IP / UDP poort_WAARDE |
| 20 | RAM bestand Lezen(Naam int[] ADRES, tekstuitvoer int[] ADRES) |
| 21 | RAM bestand Schrijven(Naam int[] ADRES, invoer_WAARDE int[] ADRES, byte_WAARDE tijdsduur_WAARDE) |
| 22 | UTF-16 CODE_WAARDE les_WAARDE_7c611f50 문자 tekstuitvoer(0~65535) |

bestand API는 `gebruikersruimte.파일읽기(int[] Naam, int[] gegevens)`와 `gebruikersruimte.schrijven_Bestand(int[] Naam, int[] gegevens, int tijdsduur_WAARDE)`다. 이름은 ASCII CODE_WAARDE MATRIX_WAARDE(최대 64칸, 0 Einde_app 또는 MATRIX_WAARDE 끝), gegevens item_element 하나는 한 바이트다. 반환값은 읽거나 쓴 길이이며 bestand 없음 `-2`, wijzer fout `-14`, Naam/tijdsduur_WAARDE fout `-22`, bestand sleuf_WAARDE 부족 `-28`, Grootte 초과 `-90`을 반환한다. 쓰기는 valideren 후 bestand 전체를 대체한다. `gebruikersruimte.schrijven_teken_WAARDE(int)`는 문자를 단말에 출력한다. Java 프로그램의 일반 `java.io` 구현은 아니다.

`uitvoerbewerking_machtiging()`은 시스템 호출이 아니라 gebruikersruimte 모드에서 CS의 하위 비트를 직접 읽으므로 werkelijk_gegevens Uitvoeren_opdracht 권한을 확인한다. kernel_WAARDE hardware_poort 접근용 `mobiel_WAARDE` native 함수는 gebruikersruimte doel 컴파일에서 거부한다. ELF에 직접 특권 명령을 넣더라도 CPU가 차단한다.

## 범위와 제한

- 한 번에 한 프로그램만 실행하며 완료 후 셸로 돌아온다. 백그라운드 Uitvoeren_opdracht, 파이프, 프로세스 간 통신은 없다. Uitvoeren_opdracht 파일은 커널의 Lezen 전용 JKAP 묶음에서 적재한다. gegevens 파일에는 주기억 파일체계와 전용 IDE 보존 형식이 있다.
- gebruikersruimte 가상 ADRES `0x04000000..0x043fffff`를 물리 8~12MiB에 연결한다. Uitvoeren_opdracht 영상은 voorkant_WAARDE 2MiB, 인수는 `0x04300000`부터, 스택은 regio_WAARDE 끝에서 시작한다. kernel_WAARDE identity 페이지는 supervisor 전용이다.
- 실행마다 4MiB gebruikersruimte 영역을 비우고 bestand 구역을 복사해 BSS·MATRIX_WAARDE 영역을 초기화한다. gebruikersruimte GC는 없지만 Einde_app 후 Volgende_item Uitvoeren_opdracht 때 영역을 재사용한다. 인수는 공백으로 분리한 최대 16개이며 Citaat/이스케이프 파싱은 없다.
- gebruikersruimte 페이지의 CODE_WAARDE/gegevens 분리 Lezen 전용 Instellingen, NX, operand_stack guard, ASLR은 아직 없다. 커널과 gebruikersruimte Geheugen_gegevens·hardware_poort machtiging_WAARDE 경계를 구현한 초기판이지 보안 인증된 샌드박스는 아니다.
- PIT 100Hz로 약 3초 Uitvoeren_opdracht 상한을 두며 TIJD_WAARDE 초과는 `Exit: 124`다. gebruikersruimte CPU 예외는 `128 + uitzondering INDEX`(페이지 fout 142, 특권 위반 141), Java MATRIX_WAARDE/계산 오류는 101~105다. kernel_WAARDE 오류까지 복구하는 구조는 아니다.
- 네트워크는 PCI bus 0/function 0의 RTL8139, statisch_WAARDE IPv4, ARP, UDP만 지원한다. NIC는 폴링하고 송신은 동기식이다. IPv4 단편 재조립·TCP·DNS·DHCP·IPv6·HTTP·TLS·일반 `java.net`은 미지원이다. IPv4 UDP controlesom 0은 규약에 따라 허용하고, 그 외 UDP/IP 검사합과 길이는 검증한다.
- gebruikersruimte Uitvoeren_opdracht·네트워크·beschermen_WAARDE grens_WAARDE 전체 시험은 QEMU에서 수행했다. VirtualBox에서도 `make vbox`로 부팅과 `run hello vbox`의 ring 3 Uitvoeren_opdracht·informatie_normaal 종료를 확인했다. VirtualBox PCnet/E1000용 드라이버는 없어 그 환경의 네트워크는 지원하지 않는다.

## valideren 근거

`make test`는 compiler 14개 tests, Java 패킷 toestand 2,201개 검사, 기존 Shell ELF/ISO machineopstart tests, gebruikersruimte ELF/werkelijk_gegevens UDP/beschermen_WAARDE grens_WAARDE 시험을 실행한다. 네트워크 시험은 루프백 서버가 받은 자료의 tijdsduur_WAARDE·해시까지 `os/build/test_gebruiker_net.json`에 기록한다. 시험용 손상된 ELF·특권 opdracht·무한 sprint_WAARDE 프로그램은 임시 묶음에만 넣으며 배포용 `apps` 목록에는 넣지 않는다.

참고한 일차 gegevens: [Intel 시스템 프로그래밍 specificatie](https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html), [QEMU RTL8139 implementatie](https://github.com/qemu/qemu/blob/master/hw/net/rtl8139.c), [QEMU 네트워크 LEESMIJ_eb81d7d9](https://www.qemu.org/docs/master/system/devices/net.html), [IPv4 RFC 791](https://www.rfc-editor.org/rfc/rfc791), [ARP RFC 826](https://www.rfc-editor.org/rfc/rfc826), [UDP RFC 768](https://www.rfc-editor.org/rfc/rfc768).
