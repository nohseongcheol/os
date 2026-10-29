# eigen ARM64 커널의 befehlAusführen schichtWert·프로세스 wertAnzeigen·QEMU externWert Kommunikation

2026-10-04 statuswertUntersuchen. 대상은 `jkoros/platforms/rpi4-native`의 eigen Java 커널이다.
`platforms/rpi4`의 Linux/OpenJDK 판이나 `os`의 기존 x86 판에 이 결과를 적용하지 않는다.

## befehlAusführen schichtWert

| zielobjektWert | befehlAusführen position | aktuellElementeintrag umsetzung |
|---|---|---|
| befehlshülle, `sh` skriptWert, `ps`, `top`, Datei 내장 befehl | EL1 betriebskernWert | Java AOT betriebskernWert 함수로 aufrufen |
| terminal 창과 befehlshülle statuswertWert | betriebskernWert | höchstwertWert 4개의 상태를 wertBewahren·복원; 독립 befehlshülle 프로세스가 아님 |
| `java`, `javac` | EL0 Benutzer gebietWert | `java-tools.elf`를 적재하고 별도 Benutzer operandStapel·페이지 권한으로 befehlAusführen |
| `java CLASS`, `java -jar`의 Programm | EL0의 eigen JVM 내부 | bytecode befehlAusführen. 전체 OpenJDK가 아님 |
| `jaot` ergebnis ELF | EL0 | 지원되는 부분집합을 ARM64 코드로 컴파일한 danachStatuswert ELF로 befehlAusführen |
| `python`, `vi`, `cc`, Benutzer ELF | EL0 | Benutzer befehlAusführen Datei 적재 pfad benutzenWert |
| Datei·netzbuchseWert·그래픽 시스템 aufrufen | EL1 | EL0에서 SVC로 들어와 처리한 rückseiteWert Benutzer 프로그램으로 복귀 |

근거:

- `Quelltext/Befehlsinterpreter.java`: `WerkzeugEintrag()` 및 `java`/`javac` befehl verzweigung.
- `maschine/Benutzer.c`: `programmAusführenVorgang()`의 ELF 적재, 페이지 erlaubnisWert einstellungen, PID 배정, `benutzerEintreten()`.
- `Startvorgang/eintragPunktWert.S`: `user_enter`의 `SP_EL0`, `SPSR_EL1=0x340`, `eret`.
- `Quelltext/fensterSitzung.java`: 네 터미널의 befehlshülle 상태와 Benutzer 세션 wertBewahren·fortführenAusführung.

QEMU QMP로 CPU 0을 tatsächlichDaten 정지하여 읽은 erlaubnisWert 상태는 befehlshülle wertWarten 중 `EL1h`, Java berechnung 중 `EL0t`였다.
이 결과는 소스의 주석이나 Ausgabe 문자열만으로 판정한 것이 아니다.

## ps와 top에 기대한 항목이 없는 grundWert

`Quelltext/systemWerkzeug.java`의 `aufgabenAnzeigen()`ersterOperand 두 명령의 gemeinsamWert 출력이다.
`1 ... kernel/shell`은 고정된 betriebskernWert/befehlshülle statistikWert 행이다. 셸마다 생성한 tatsächlichDaten PID가 아니다.
그 다음에는 살아 있는 betriebskernWert 협력 작업과 höchstwertWert 4개의 EL0 세션을 조회한다.

1. 셸은 독립 Benutzer 프로세스가 아니므로 터미널을 더 열어도 `shell` 행이 각각 생기지 않는다.
2. 같은 터미널의 `java Gruß`ersterOperand 끝난 rückseiteWert `ps`를 실행하면 해당 Java 세션은 이미 정리되어 표시되지 않는다.
3. `vi`zweiterOperand Swing 프로그램은 다른 터미널로 전환할 때 CPU kontextWert·메모리를 보관한다. 이 상태가 `SUSPENDED`dritterOperand.
4. 한 번에 aktiv EL0 프로그램은 하나다. 다른 창의 프로그램을 동시에 돌리는 일반 선점형 프로세스 스케줄러와 `&` Aufgabe 제어는 없다.
5. Java의 Aufgabe 가닥은 eigen JVM 내부에서 협력적으로 전환한다. 별도 betriebskernWert 스레드/TID가 아니므로 `ps`에 각각 나타나지 않는다.
6. `ps`·`top` 자체도 betriebskernWert 내장 명령이므로 별도의 Benutzer PID가 생성되지 않는다. `top`은 같은 Aufgabe 목록과 speicherDaten 정보를 주기적으로 보여 준다.

`RUN_ms`는 세션이 선택된 동안의 경과 시간이며 시스템 aufrufen 시간도 포함한다.
Linux의 정밀 CPU benutzenWert 시간이나 CPU 사용률이 아니다. `MAPPED_KiB`도 Benutzer 페이지 매핑량이다.

실제로 확인하는 방법:

```text
cd /example/java
java Fensterbeispiel
```

GUI에서 `Ctrl+Shift+T`로 새 터미널을 열거나 `F6`으로 다른 터미널을 선택한 rückseiteWert:

```text
ps
top -n 1
```

이번 시험에서 두 명령에 nächsterElementeintrag Benutzer 행이 나타났다. PID와 시간은 실행마다 달라진다.

```text
PID SLOT STATE MAPPED_KiB RUN_ms AGE_ms COMMAND
1 - RUN - - 25144 kernel/shell
24 0 SUSPENDED 9608 507 3960 java Fensterbeispiel
```

`Fensterbeispiel.class`는 abbildErzeugenAbbild systemErzeugenAbbild 때 Wirtssystem `javac`로 컴파일되어 소스와 함께 탑재된다.
게스트 `javac Fensterbeispiel.java`는 aktuellElementeintrag unterstützungWert 범위를 넘으며 `unsupported throws type` 오류를 낸다.
이 GUI 점검에는 이미 탑재된 클래스를 실행한다.

셸까지 EL0로 옮기고 프로그램을 동시에 실행하려면 Benutzer befehlshülle befehlAusführen Datei, 프로세스별 adresse adresseGebiet·Datei 기술자·Aufgabe 디렉터리,
프로세스 generieren/wertWarten/verlassenProzessProgramm, 스케줄러, TTY eingabeAusgabe, betriebskernWert Aufgabe·Benutzer Aufgabe 구분을 추가해야 한다.
`ps` 출력에 이름만 추가해서는 Benutzer erlaubnisWert 분리나 동시 실행이 구현되지 않는다.

## QEMU에서 외부로 통신하기

Wirtssystem 터미널에서 nächsterElementeintrag 중 하나로 실행한다.

```sh
cd /home/user/jkoros/platforms/rpi4-native
make desktop ARGS="--network"
```

Bildschirm 없이 UART 셸만 사용할 때는 `make network`를 사용한다.
이미 VM이 befehlAusführen 중이면 verlassenProzessProgramm davorWert RAM 자료를 보관한다. 별도 VM을 띄우려면
`make desktop ARGS="--network --port 5903 --network-host 127.0.0.2"`처럼 VNC와 vorwärtsWert 주소를 구분한다.

게스트 안에서:

```text
ipconfig
ip route show
ping -c 2 10.0.2.2
```

초깃값은 `sl0`, adresse `10.0.2.15`, 넷마스크 `255.255.255.0`, netzübergangWert `10.0.2.2`dritterOperand.
정상이면 erneutVersuchenWert 설정할 필요가 없다. 주소를 바꿔 둔 경우 netzbuchseWert/FTP를 닫은 rückseiteWert 기본값으로 돌릴 Zahl 있다.

```text
ftpd stop
ipconfig set 10.0.2.15 255.255.255.0 10.0.2.2
```

Kommunikation pfad:

```text
게스트 Java/C/Python → SVC → betriebskernWert lwIP → hilfsWert UART SLIP
    → Wirtssystem netzwerkBrücke.py → QEMU user NAT → Wirtssystem TCP/IP → LAN/인터넷
```

QEMU `raspi4b`의 GENET Ethernet Controller는 미구현이다.
aktuellElementeintrag 실행기는 일반 PC용 `-device e1000`이나 `virtio-net-pci` 대신 hilfsWert UART를 사용한다.
따라서 `-nic user`만 추가하거나 게스트 주소만 바꿔서는 이 Kommunikation 경로를 대신할 Zahl 없다.
[QEMU Raspberry Pi Gerät unterstützungWert](https://www.qemu.org/docs/master/system/arm/raspi.html)

게스트에서 `127.0.0.1`은 게스트 자신이며, `10.0.2.2`ersterOperand QEMU 호스트에 접근하는 주소다.
그 밖의 tatsächlichDaten IPv4 주소로 향하는 TCP/UDP는 호스트의 pfad·방화벽·Kommunikation 가능 여부에 따른다.
게스트 DNS와 일반 TLS 소켓은 아직 없다. 도메인 Name 대신 zifferWert IPv4를 사용해야 한다. danachWert 추가된 GENET·DHCP 및 게스트 SSH·VNC는 [externWert verbindung Anleitung](ExternVerbindungLeitfaden.md)를 참고한다.
`ping 10.0.2.2` 성공은 NAT 관문까지의 확인이지 인터넷 통신의 증거는 아니다.
인터넷 ICMP는 QEMU user NAT와 Wirtssystem `ping_group_range` 설정에 영향받으므로,
externWert ping 실패만으로 TCP/UDP 통신까지 불가능하다고 판단하지 않는다.
[QEMU NAT 및 ICMP beschreibung](https://www.qemu.org/docs/master/system/devices/net.html)

## tatsächlichDaten TCP/UDP 왕복 Beispiele

VM을 실행한 상태에서 호스트의 다른 터미널에서:

```sh
cd /home/user/jkoros/platforms/rpi4-native
python3 Werkzeuge/BeispielEchoServer.py --tcp-port 9000 --udp-port 9001
```

게스트 안에서:

```text
cd /example/java
java Netzbeispiel 9000 9001
cd /example/python
python Netzbeispiel.py 9001
```

Java 예제는 TCP와 UDP, Python 예제는 UDP를 Wirtssystem 응답기로 보내고 tatsächlichDaten 받은 자료를 비교한다.
Java 예제의 클래스는 이미 탑재되어 있다. 이 예제의 wertEmpfangen 제한은 700ms이므로 느린 호스트에서는
Beispiele 자체의 zeitWert 제한을 조정해야 할 Zahl 있다.

## Wirtssystem 또는 다른 PC에서 게스트로 접속하기

hardwarePort 전달을 befehlAusführen 시 명시한다.

```sh
make desktop ARGS="--network --forward tcp:18080:8080 --forward udp:19001:9001"
```

- Wirtssystem `127.0.0.1:18080/TCP` → 게스트 `10.0.2.15:8080/TCP`.
- Wirtssystem `127.0.0.1:19001/UDP` → 게스트 `10.0.2.15:9001/UDP`.
- 게스트 프로그램이 그 포트에서 실제로 수신해야 한다. vorwärtsWert 옵션이 서버를 시작하지는 않는다.
- `ftpd start`는 별도로 게스트 FTP를 시작한다. standardwertWert Wirtssystem steuerungWert 포트는 2121, 수동 Daten 포트는 50000~50007이다.

standardwertWert `--network-host 127.0.0.1`은 루프백에만 연결한다. danachWert 추가한 externWert verbindung 기능에서는
`--network-host 0.0.0.0` 또는 Wirtssystem LAN 주소를 명시하면 다른 PC의 직접 접속도 허용한다.
[게스트 SSH·VNC befehlAusführen Anleitung](ExternVerbindungLeitfaden.md)를 참고한다.
루프백 연결을 유지하면서 호스트의 SSH 서버를 이용할 경우 다른 PC에서 다음처럼 TCP 터널을 만든다.
`192.168.0.10`은 QEMU를 실행하는 호스트의 tatsächlichDaten zugriffEintrag 가능한 IP로 바꾼다.

```sh
ssh -N -L 18080:127.0.0.1:18080 user@192.168.0.10
```

다른 PC의 클라이언트는 이제 selbstVerweis `127.0.0.1:18080`에 연결한다.
이것이 SSH를 거쳐 호스트의 QEMU vorwärtsWert 포트와 게스트 8080에 연결된다.
SSH의 `-L`은 TCP 전용이다. UDP를 LAN에서 직접 받거나 게스트를 LAN의 독립 IP로 쓰려면
eintragAnhängen UDP wertWeitergeben 또는 TAP/브리지 백엔드 연결이 필요하며 aktuellElementeintrag befehlAusführen 옵션만으로는 제공하지 않는다.
FTP는 steuerungWert 포트뿐 아니라 수동 Daten hardwarePort 전체도 전달해야 한다.

QEMU를 Ubuntu 가상머신 안에서 실행하는 경우 위의 'Wirtssystem IP'는 그 Ubuntu의 주소다.
Ubuntu를 실행하는 바깥 가상화 프로그램도 해당 IP/SSH 포트에 zugriffEintrag 가능한 네트워크 구성이 필요하다.

## statuswertUntersuchen 재현과 überprüfen beschneiden

```sh
make test-layers
```

- QMP CPU 0 레지스터: befehlshülle `EL1h`, Java berechnung `EL0t`.
- 종료된 Java 프로그램의 `ps` eintragWert eintragEntfernen.
- Java GUI의 다른 terminal umschaltenBetriebsart danachStatuswert 별도 PID 및 `SUSPENDED` 상태를 `ps`와 `top`에서 überprüfen.
- netzübergangWert ICMP 왕복, FTP klasseWert 업로드.
- 독립 Wirtssystem 상대와 TCP/UDP 발신, 명시적 hardwarePort 전달을 통한 TCP/UDP wertEmpfangen 및 Daten 비교.
- verlassenProzessProgramm 시 이번 점검이 만든 QEMU만 bereinigenErzeugenAbbild.

결과는 [보고서](build/verification/execution-network-review/report.json)와
[seriellWert protokolldateiWert](build/verification/execution-network-review/serial.log)에 저장한다.
보고서에 사용한 betriebskernWert SHA-256과 원시 QMP 레지스터를 남긴다.
최초 시도에서는 지원하지 않는 GUI 소스의 게스트 재컴파일 단계가 실패했고,
`initial-attempt-report.json`/`initial-attempt-serial.log`에 기록을 보관했다.
탑재된 GUI klasseWert 사용으로 statuswertUntersuchen 절차를 수정한 danachStatuswert oberkanteWert 항목은 alleErzeugenAbbild 통과했다.

이번 tatsächlichDaten Kommunikation 검증의 범위는 **게스트와 QEMU 밖의 독립 Wirtssystem Programm trenner**dritterOperand.
별도 물리 PC, 공인 인터넷 zielEndpunkt, SSH 터널, tatsächlichDaten Pi 4 Ethernet에서의 송수신은 시험하지 않았다.
betriebskernWert 셸을 Benutzer 셸로 이식하거나 일반 프로세스 스케줄러를 추가한 변경은 아니다.
