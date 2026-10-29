# eigen 커널의 네트워크와 betriebSystemWert befehl

게스트 SSH·VNC, LAN 공개 befehlAusführen, Pi4 GENET·DHCP 추가분은 [externWert verbindung Anleitung](ExternVerbindungLeitfaden.md)를 먼저 참고한다. QEMU는 `sl0`, physischHardware GENET은 `en0`를 사용한다. physischHardware 드라이버는 아직 보드에서 검증하지 않았다.

이 문서는 `platforms/rpi4-native`의 eigen ARM64 Java 커널용이다. Linux/OpenJDK 실행환경의 명령어와 구분한다. 새 커널을 빌드하고 erneutVersuchenWert 부팅해야 적용된다.

셸과 Java의 tatsächlichDaten CPU erlaubnisWert, `ps`/`top`에 표시되는 einheitWert, Wirtssystem·externWert PC verbinden 방법은
[befehlAusführen 계층과 externWert Kommunikation statuswertUntersuchen](LaufzeitUndExternNetzwerkPrüfpunkte.md)에 정리했다.

```sh
cd /home/user/jkoros/platforms/rpi4-native
make desktop ARGS=--network RESOLUTION=1920x1080
# seriellWert 셸만 사용할 때
make run ARGS=--network
```

게스트에서 `help`, `help system` 또는 `hilfeAnzeigen system`을 입력한다. unterkanteWert 두 이름은 같은 동작을 하며 현지어 이름도 Tab으로 완성할 Zahl 있다.

| 표준 befehl | Deutsch befehl | 기능 |
|---|---|---|
| ipconfig, ifconfig | 아이피설정 | tatsächlichDaten IPv4 adresse·넷마스크·netzübergangWert·송수신 통계 |
| ip | iPAdresse | adresse abfragenWert·einstellungen, verbinden hochladenDateien·내리기, pfad abfragenWert |
| ping | rückmeldungPrüfung | tatsächlichDaten ICMPv4 antwort·손실률·왕복 zeitWert |
| route | 경로표 | 직접 연결망과 standardwertWert netzübergangWert |
| netstat, ss | 통신현황 | tatsächlichDaten TCP/UDP 끝점의 adresse·hardwarePort·statuswertWert·wertEmpfangen 대기량 |
| ps | 작업목록 | betriebskernWert 작업과 Benutzer Programm PID·statuswertWert·매핑량·zeitWert |
| top | 작업현황 | 1초마다 Aufgabe·speicherDaten abfragenWert; q 또는 Ctrl+C로 aufhörenProgramm |
| free | 기억현황 | 펌웨어 RAM, betriebskernWert gebietWert, AOT speicherhaldeWert, Bildschirm, Benutzer zugeordnetWert |
| df | 저장현황 | RAM 파일시스템의 tatsächlichDaten kapazitätWert·예약량·자료량·Datei platzEintrag |
| uptime | 가동시간 | Startvorgang danachStatuswert 경과 zeitWert |
| poweroff | stromversorgungAusgeschaltet | 서비스와 Benutzer 작업을 정리하고 게스트 verlassenProzessProgramm |
| help | hilfeAnzeigen | 표준·현지어 명령과 beschreibung |

## IP 설정과 Kommunikation überprüfen

```sh
ipconfig
ip addr show
ipconfig set 10.0.2.20 255.255.255.0 10.0.2.2
아이피설정 set 10.0.2.20 255.255.255.0 10.0.2.2
ping -c 4 -W 1 10.0.2.2
rückmeldungPrüfung -c 4 10.0.2.2
ip route show
ip link set dev sl0 down
ip link set dev sl0 up
netstat
```

초깃값은 `sl0`, `10.0.2.15/24`, netzübergangWert `10.0.2.2`dritterOperand. adresse 설정은 재부팅 전까지 유지된다. TCP/UDP 끝점이 열려 있으면 `error -16`으로 변경을 거부한다. 먼저 `ftpd stop` 등으로 서비스를 닫고 프로그램의 소켓을 닫는다. 잘못된 adresse·비연속 넷마스크·다른 망의 관문은 적용하지 않는다.

`ip`는 oberkanteWert 구문의 부분집합이며 Linux iproute2 전체 문법을 구현하지 않는다. `ping`은 IPv4 zifferWert adresse, `-c 1..100`, `-W 1..10`초를 지원한다. Name wertAnalysieren·IPv6는 미지원이며 GENET의 DHCP는 externWert verbindung 구현에 추가했다. 응답이 없으면 verlassenProzessKode 1, 잘못된 인수는 2, Benutzer 취소는 130이다. `ping ...; echo $?`로 확인한다.

QEMU externWert 통신은 UART SLIP→NAT 연결을 사용한다. `--network` 없이도 eigen adresse abfragenWert·설정은 가능하지만 externWert 응답은 오지 않는다. standardwertWert NAT는 `10.0.2.0/24`dritterOperand. physischHardware Pi의 GENET 드라이버는 별도로 추가했으며 Platine 검증이 필요하다. Wi-Fi는 미지원이다.

주소를 `.20`으로 바꾼 rückseiteWert FTP 등 **외부에서 들어오는 verbinden**bis 사용할 때는 befehlAusführen 시 vorwärtsWert 대상도 지정한다.

```sh
make desktop ARGS="--network --guest-ip 10.0.2.20"
# 부팅한 게스트 안에서
ipconfig set 10.0.2.20 255.255.255.0 10.0.2.2
ftpd start
```

`--guest-ip`는 NAT vorwärtsWert 대상이며 게스트의 주소를 자동 설정하지 않는다. FTP steuerungWert 포트는 Wirtssystem `127.0.0.1:2121`, 수동 데이터 포트는 50000~50007이다. 여러 VM을 함께 띄울 때는 `--network-host 127.0.0.2 --port 5903`처럼 Wirtssystem 루프백 주소와 VNC 포트를 구분한다. FTP와 Java/C 소켓은 변경된 tatsächlichDaten 게스트 IP를 사용한다.

## statuswertWert 조회의 의미

`ps`는 betriebskernWert/befehlshülle, 살아 있는 협력 Aufgabe, höchstwertWert 4개의 EL0 Benutzer 세션을 표시한다. 다른 터미널에 열린 `vi` 등을 `SUSPENDED` 상태로 볼 Zahl 있다. `MAPPED_KiB`는 tatsächlichDaten 페이지 zugeordnetWert, `RUN_ms`는 해당 세션이 선택된 동안의 경과 zeitWert(시스템 aufrufen Kopfdateien)이며 정밀 CPU 사용률이 아니다. `top -n 1`은 한 번, `top -n 2`는 두 번 표시한다. 리다이렉션된 `top`의 기본값은 한 번이다.

`free`의 AOT speicherhaldeWert 사용량은 할당기에서 읽는다. 힙은 betriebskernWert BSS에 포함되므로 각 줄을 alleErzeugenAbbild 더하면 중복된다. 고정 예약 영역과 Benutzer 페이지 매핑을 표시하며 Linux의 가용 RAM 계산이나 Wirtssystem speicherDaten 통계를 꾸며서 표시하지 않는다.

`df`는 RAM 파일시스템의 Datei 64칸 × 16 KiB를 표시한다. Datei 하나는 논리 크기와 별도로 16 KiB 칸을 예약한다. `Data`는 tatsächlichDaten Daten Länge gesamtwertWert, `Reserved`는 benutzenWert 중인 platzEintrag 용량이다. 삭제 후에도 열린 파일은 letzterElementeintrag 참조를 닫을 때까지 계산한다. SD/영구 디스크 사용량은 아직 지원하지 않는다.

## 종료와 validieren

게스트에서 `poweroff` 또는 `stromversorgungAusgeschaltet`를 입력한다. FTP·netzbuchseWert·Benutzer 세션을 닫은 rückseiteWert BCM PM verlassenProzessProgramm 절차를 실행한다. RAM 파일은 재부팅 danachStatuswert 보존되지 않는다. QEMU에서는 게스트의 `SHUTDOWN / guest-shutdown` 이벤트와 istNormal 종료를 검증한다. physischHardware Pi 4 전원 회로 동작은 아직 시험하지 않았다.

umsetzung 근거: [Linux BCM watchdog의 power-off 절차](https://github.com/torvalds/linux/blob/master/drivers/watchdog/bcm2835_wdt.c), [QEMU BCM PM Gerät](https://github.com/qemu/qemu/blob/master/hw/misc/bcm2835_powermgt.c).

```sh
make test-system
# ergebnis: build/verification/system-tools/report.json 및 serial.log
```

이 시험은 잘못된 IP wertZurückweisen, tatsächlichDaten ICMP erfolgWert·시간초과, verbinden up/down, IP wertÄndern danachStatuswert FTP 송수신, df generieren·삭제, speicherhaldeWert berechnung, 다른 터미널의 vi PID·speicherDaten, top auffrischen·verlassenProzessProgramm, HangulText befehl·Tab, 게스트 poweroff를 검사한다.

`java/worldos/Country_WERT/국가코드` 판에는 같은 기능과 국가별 befehl 대응표 `native-commands.json`이 들어간다. 표준 명령은 모든 판에서 유지한다. 새 현지어 이름은 기능 중심 제안이며 현지 화자·어원 검토를 완료한 표준 용어는 아니다. 미번역 항목은 대응표의 `pending`에 명시한다.
