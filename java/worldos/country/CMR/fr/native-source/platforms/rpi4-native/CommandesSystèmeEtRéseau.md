# interne 커널의 네트워크와 valeurSystèmeExploitation commande

게스트 SSH·VNC, LAN 공개 exécuterCommande, Pi4 GENET·DHCP 추가분은 [valeurExtérieur connexion Guide](GuideConnexionExtérieur.md)를 먼저 참고한다. QEMU는 `sl0`, matérielPhysique GENET은 `en0`를 사용한다. matérielPhysique 드라이버는 아직 보드에서 검증하지 않았다.

이 문서는 `platforms/rpi4-native`의 interne ARM64 Java 커널용이다. Linux/OpenJDK 실행환경의 명령어와 구분한다. 새 커널을 빌드하고 valeurRéessayer 부팅해야 적용된다.

셸과 Java의 donnéesEffectif CPU valeurPermission, `ps`/`top`에 표시되는 valeurUnité, Hôte·valeurExtérieur PC connecter 방법은
[exécuterCommande 계층과 valeurExtérieur Communication inspecterÉtatValeur](ContrôlesRéseauExtérieurEtEnvironnementExécution.md)에 정리했다.

```sh
cd /home/user/jkoros/platforms/rpi4-native
make desktop ARGS=--network RESOLUTION=1920x1080
# valeurSériel 셸만 사용할 때
make run ARGS=--network
```

게스트에서 `help`, `help system` 또는 `afficherAide system`을 입력한다. valeurBasExtrémité 두 이름은 같은 동작을 하며 현지어 이름도 Tab으로 완성할 nombre 있다.

| 표준 commande | français commande | 기능 |
|---|---|---|
| ipconfig, ifconfig | 아이피설정 | donnéesEffectif IPv4 adresse·넷마스크·valeurPasserelle·송수신 통계 |
| ip | adresseIP | adresse valeurInterroger·réglages, connecter fichiersTéléverser·내리기, chemin valeurInterroger |
| ping | testRéponseRetour | donnéesEffectif ICMPv4 réponse·손실률·왕복 valeurTemps |
| route | 경로표 | 직접 연결망과 valeurDéfaut valeurPasserelle |
| netstat, ss | 통신현황 | donnéesEffectif TCP/UDP 끝점의 adresse·portMatériel·valeurÉtatValeur·recevoirValeur 대기량 |
| ps | 작업목록 | valeurNoyau 작업과 Utilisateur Programme PID·valeurÉtatValeur·매핑량·valeurTemps |
| top | 작업현황 | 1초마다 Tâche·donnéesMémoire valeurInterroger; q 또는 Ctrl+C로 programmeTerminerSession |
| free | 기억현황 | 펌웨어 RAM, valeurNoyau valeurRégion, AOT valeurTas, Écran, Utilisateur valeurAssocié |
| df | 저장현황 | RAM 파일시스템의 donnéesEffectif valeurCapacité·예약량·자료량·Fichier entréeÉlémentEmplacement |
| uptime | 가동시간 | Amorçage étatValeurAprès 경과 valeurTemps |
| poweroff | désactivéAlimentation | 서비스와 Utilisateur 작업을 정리하고 게스트 programmeQuitter |
| help | afficherAide | 표준·현지어 명령과 description |

## IP 설정과 Communication vérifier

```sh
ipconfig
ip addr show
ipconfig set 10.0.2.20 255.255.255.0 10.0.2.2
아이피설정 set 10.0.2.20 255.255.255.0 10.0.2.2
ping -c 4 -W 1 10.0.2.2
testRéponseRetour -c 4 10.0.2.2
ip route show
ip link set dev sl0 down
ip link set dev sl0 up
netstat
```

초깃값은 `sl0`, `10.0.2.15/24`, valeurPasserelle `10.0.2.2`opérandeTroisième. adresse 설정은 재부팅 전까지 유지된다. TCP/UDP 끝점이 열려 있으면 `error -16`으로 변경을 거부한다. 먼저 `ftpd stop` 등으로 서비스를 닫고 프로그램의 소켓을 닫는다. 잘못된 adresse·비연속 넷마스크·다른 망의 관문은 적용하지 않는다.

`ip`는 valeurSommet 구문의 부분집합이며 Linux iproute2 전체 문법을 구현하지 않는다. `ping`은 IPv4 valeurChiffre adresse, `-c 1..100`, `-W 1..10`초를 지원한다. nom analyserValeur·IPv6는 미지원이며 GENET의 DHCP는 valeurExtérieur connexion 구현에 추가했다. 응답이 없으면 codeQuitter 1, 잘못된 인수는 2, Utilisateur 취소는 130이다. `ping ...; echo $?`로 확인한다.

QEMU valeurExtérieur 통신은 UART SLIP→NAT 연결을 사용한다. `--network` 없이도 interne adresse valeurInterroger·설정은 가능하지만 valeurExtérieur 응답은 오지 않는다. valeurDéfaut NAT는 `10.0.2.0/24`opérandeTroisième. matérielPhysique Pi의 GENET 드라이버는 별도로 추가했으며 CarteMatérielle 검증이 필요하다. Wi-Fi는 미지원이다.

주소를 `.20`으로 바꾼 valeurRetourArrièreCôté FTP 등 **외부에서 들어오는 connecter**jusquÀ 사용할 때는 exécuterCommande 시 valeurAvantDirection 대상도 지정한다.

```sh
make desktop ARGS="--network --guest-ip 10.0.2.20"
# 부팅한 게스트 안에서
ipconfig set 10.0.2.20 255.255.255.0 10.0.2.2
ftpd start
```

`--guest-ip`는 NAT valeurAvantDirection 대상이며 게스트의 주소를 자동 설정하지 않는다. FTP valeurContrôle 포트는 Hôte `127.0.0.1:2121`, 수동 데이터 포트는 50000~50007이다. 여러 VM을 함께 띄울 때는 `--network-host 127.0.0.2 --port 5903`처럼 Hôte 루프백 주소와 VNC 포트를 구분한다. FTP와 Java/C 소켓은 변경된 donnéesEffectif 게스트 IP를 사용한다.

## valeurÉtatValeur 조회의 의미

`ps`는 valeurNoyau/interpréteurCommandes, 살아 있는 협력 Tâche, valeurMaximal 4개의 EL0 Utilisateur 세션을 표시한다. 다른 터미널에 열린 `vi` 등을 `SUSPENDED` 상태로 볼 nombre 있다. `MAPPED_KiB`는 donnéesEffectif 페이지 valeurAssocié, `RUN_ms`는 해당 세션이 선택된 동안의 경과 valeurTemps(시스템 invoquer Entêtes)이며 정밀 CPU 사용률이 아니다. `top -n 1`은 한 번, `top -n 2`는 두 번 표시한다. 리다이렉션된 `top`의 기본값은 한 번이다.

`free`의 AOT valeurTas 사용량은 할당기에서 읽는다. 힙은 valeurNoyau BSS에 포함되므로 각 줄을 construireTous 더하면 중복된다. 고정 예약 영역과 Utilisateur 페이지 매핑을 표시하며 Linux의 가용 RAM 계산이나 Hôte donnéesMémoire 통계를 꾸며서 표시하지 않는다.

`df`는 RAM 파일시스템의 Fichier 64칸 × 16 KiB를 표시한다. Fichier 하나는 논리 크기와 별도로 16 KiB 칸을 예약한다. `Data`는 donnéesEffectif Données longueur valeurTotal, `Reserved`는 valeurUtiliser 중인 entréeÉlémentEmplacement 용량이다. 삭제 후에도 열린 파일은 élémentListeDernier 참조를 닫을 때까지 계산한다. SD/영구 디스크 사용량은 아직 지원하지 않는다.

## 종료와 valider

게스트에서 `poweroff` 또는 `désactivéAlimentation`를 입력한다. FTP·valeurPriseRéseau·Utilisateur 세션을 닫은 valeurRetourArrièreCôté BCM PM programmeQuitter 절차를 실행한다. RAM 파일은 재부팅 étatValeurAprès 보존되지 않는다. QEMU에서는 게스트의 `SHUTDOWN / guest-shutdown` 이벤트와 estNormal 종료를 검증한다. matérielPhysique Pi 4 전원 회로 동작은 아직 시험하지 않았다.

réalisation 근거: [Linux BCM watchdog의 power-off 절차](https://github.com/torvalds/linux/blob/master/drivers/watchdog/bcm2835_wdt.c), [QEMU BCM PM Périphérique](https://github.com/qemu/qemu/blob/master/hw/misc/bcm2835_powermgt.c).

```sh
make test-system
# résultat: build/verification/system-tools/report.json 및 serial.log
```

이 시험은 잘못된 IP rejeterValeur, donnéesEffectif ICMP valeurSuccès·시간초과, connecter up/down, IP changerValeur étatValeurAprès FTP 송수신, df générer·삭제, valeurTas calculRésultat, 다른 터미널의 vi PID·donnéesMémoire, top actualiser·programmeQuitter, texteHangul commande·Tab, 게스트 poweroff를 검사한다.

`java/worldos/Country_CNUM/국가코드` 판에는 같은 기능과 국가별 commande 대응표 `native-commands.json`이 들어간다. 표준 명령은 모든 판에서 유지한다. 새 현지어 이름은 기능 중심 제안이며 현지 화자·어원 검토를 완료한 표준 용어는 아니다. 미번역 항목은 대응표의 `pending`에 명시한다.
