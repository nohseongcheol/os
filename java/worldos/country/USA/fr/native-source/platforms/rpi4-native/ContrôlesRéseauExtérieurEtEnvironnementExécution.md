# interne ARM64 커널의 exécuterCommande valeurCouche·프로세스 afficherValeur·QEMU valeurExtérieur Communication

2026-10-04 inspecterÉtatValeur. 대상은 `jkoros/platforms/rpi4-native`의 interne Java 커널이다.
`platforms/rpi4`의 Linux/OpenJDK 판이나 `os`의 기존 x86 판에 이 결과를 적용하지 않는다.

## exécuterCommande valeurCouche

| valeurCible | exécuterCommande position | élémentListeActuel réalisation |
|---|---|---|
| interpréteurCommandes, `sh` valeurScript, `ps`, `top`, Fichier 내장 commande | EL1 valeurNoyau | Java AOT valeurNoyau 함수로 invoquer |
| terminal 창과 interpréteurCommandes valeurÉtatValeur | valeurNoyau | valeurMaximal 4개의 상태를 préserverValeur·복원; 독립 interpréteurCommandes 프로세스가 아님 |
| `java`, `javac` | EL0 Utilisateur valeurRégion | `java-tools.elf`를 적재하고 별도 Utilisateur pileOpérande·페이지 권한으로 exécuterCommande |
| `java CLASS`, `java -jar`의 Programme | EL0의 interne JVM 내부 | codeOctets exécuterCommande. 전체 OpenJDK가 아님 |
| `jaot` résultat ELF | EL0 | 지원되는 부분집합을 ARM64 코드로 컴파일한 étatValeurAprès ELF로 exécuterCommande |
| `python`, `vi`, `cc`, Utilisateur ELF | EL0 | Utilisateur exécuterCommande Fichier 적재 chemin valeurUtiliser |
| Fichier·valeurPriseRéseau·그래픽 시스템 invoquer | EL1 | EL0에서 SVC로 들어와 처리한 valeurRetourArrièreCôté Utilisateur 프로그램으로 복귀 |

근거:

- `source/InterpréteurCommandes.java`: `EntréeÉlémentOutil()` 및 `java`/`javac` commande branche.
- `machine/Utilisateur.c`: `lancerProgramme()`의 ELF 적재, 페이지 valeurPermission réglages, PID 배정, `entrerUtilisateur()`.
- `Amorçage/valeurPointEntréeÉlément.S`: `user_enter`의 `SP_EL0`, `SPSR_EL1=0x340`, `eret`.
- `source/sessionFenêtre.java`: 네 터미널의 interpréteurCommandes 상태와 Utilisateur 세션 préserverValeur·exécutionReprendre.

QEMU QMP로 CPU 0을 donnéesEffectif 정지하여 읽은 valeurPermission 상태는 interpréteurCommandes attendreValeur 중 `EL1h`, Java calculRésultat 중 `EL0t`였다.
이 결과는 소스의 주석이나 Sortie 문자열만으로 판정한 것이 아니다.

## ps와 top에 기대한 항목이 없는 valeurRaison

`source/outilSystème.java`의 `afficherTâches()`opérandePremier 두 명령의 valeurCommun 출력이다.
`1 ... kernel/shell`은 고정된 valeurNoyau/interpréteurCommandes valeurStatistiques 행이다. 셸마다 생성한 donnéesEffectif PID가 아니다.
그 다음에는 살아 있는 valeurNoyau 협력 작업과 valeurMaximal 4개의 EL0 세션을 조회한다.

1. 셸은 독립 Utilisateur 프로세스가 아니므로 터미널을 더 열어도 `shell` 행이 각각 생기지 않는다.
2. 같은 터미널의 `java Salutation`opérandePremier 끝난 valeurRetourArrièreCôté `ps`를 실행하면 해당 Java 세션은 이미 정리되어 표시되지 않는다.
3. `vi`opérandeDeuxième Swing 프로그램은 다른 터미널로 전환할 때 CPU valeurContexte·메모리를 보관한다. 이 상태가 `SUSPENDED`opérandeTroisième.
4. 한 번에 actif EL0 프로그램은 하나다. 다른 창의 프로그램을 동시에 돌리는 일반 선점형 프로세스 스케줄러와 `&` Tâche 제어는 없다.
5. Java의 Tâche 가닥은 interne JVM 내부에서 협력적으로 전환한다. 별도 valeurNoyau 스레드/TID가 아니므로 `ps`에 각각 나타나지 않는다.
6. `ps`·`top` 자체도 valeurNoyau 내장 명령이므로 별도의 Utilisateur PID가 생성되지 않는다. `top`은 같은 Tâche 목록과 donnéesMémoire 정보를 주기적으로 보여 준다.

`RUN_ms`는 세션이 선택된 동안의 경과 시간이며 시스템 invoquer 시간도 포함한다.
Linux의 정밀 CPU valeurUtiliser 시간이나 CPU 사용률이 아니다. `MAPPED_KiB`도 Utilisateur 페이지 매핑량이다.

실제로 확인하는 방법:

```text
cd /example/java
java ExempleFenêtre
```

GUI에서 `Ctrl+Shift+T`로 새 터미널을 열거나 `F6`으로 다른 터미널을 선택한 valeurRetourArrièreCôté:

```text
ps
top -n 1
```

이번 시험에서 두 명령에 élémentListeSuivant Utilisateur 행이 나타났다. PID와 시간은 실행마다 달라진다.

```text
PID SLOT STATE MAPPED_KiB RUN_ms AGE_ms COMMAND
1 - RUN - - 25144 kernel/shell
24 0 SUSPENDED 9608 507 3960 java ExempleFenêtre
```

`ExempleFenêtre.class`는 construireImage construireSystème 때 Hôte `javac`로 컴파일되어 소스와 함께 탑재된다.
게스트 `javac ExempleFenêtre.java`는 élémentListeActuel valeurPriseEnCharge 범위를 넘으며 `unsupported throws type` 오류를 낸다.
이 GUI 점검에는 이미 탑재된 클래스를 실행한다.

셸까지 EL0로 옮기고 프로그램을 동시에 실행하려면 Utilisateur interpréteurCommandes exécuterCommande Fichier, 프로세스별 adresse régionAdresse·Fichier 기술자·Tâche 디렉터리,
프로세스 générer/attendreValeur/programmeQuitter, 스케줄러, TTY sortieEntrée, valeurNoyau Tâche·Utilisateur Tâche 구분을 추가해야 한다.
`ps` 출력에 이름만 추가해서는 Utilisateur valeurPermission 분리나 동시 실행이 구현되지 않는다.

## QEMU에서 외부로 통신하기

Hôte 터미널에서 élémentListeSuivant 중 하나로 실행한다.

```sh
cd /home/user/jkoros/platforms/rpi4-native
make desktop ARGS="--network"
```

Écran 없이 UART 셸만 사용할 때는 `make network`를 사용한다.
이미 VM이 exécuterCommande 중이면 programmeQuitter valeurAvant RAM 자료를 보관한다. 별도 VM을 띄우려면
`make desktop ARGS="--network --port 5903 --network-host 127.0.0.2"`처럼 VNC와 valeurAvantDirection 주소를 구분한다.

게스트 안에서:

```text
ipconfig
ip route show
ping -c 2 10.0.2.2
```

초깃값은 `sl0`, adresse `10.0.2.15`, 넷마스크 `255.255.255.0`, valeurPasserelle `10.0.2.2`opérandeTroisième.
정상이면 valeurRéessayer 설정할 필요가 없다. 주소를 바꿔 둔 경우 valeurPriseRéseau/FTP를 닫은 valeurRetourArrièreCôté 기본값으로 돌릴 nombre 있다.

```text
ftpd stop
ipconfig set 10.0.2.15 255.255.255.0 10.0.2.2
```

Communication chemin:

```text
게스트 Java/C/Python → SVC → valeurNoyau lwIP → valeurAuxiliaire UART SLIP
    → Hôte pontRéseau.py → QEMU user NAT → Hôte TCP/IP → LAN/인터넷
```

QEMU `raspi4b`의 GENET Ethernet Controller는 미구현이다.
élémentListeActuel 실행기는 일반 PC용 `-device e1000`이나 `virtio-net-pci` 대신 valeurAuxiliaire UART를 사용한다.
따라서 `-nic user`만 추가하거나 게스트 주소만 바꿔서는 이 Communication 경로를 대신할 nombre 없다.
[QEMU Raspberry Pi Périphérique valeurPriseEnCharge](https://www.qemu.org/docs/master/system/arm/raspi.html)

게스트에서 `127.0.0.1`은 게스트 자신이며, `10.0.2.2`opérandePremier QEMU 호스트에 접근하는 주소다.
그 밖의 donnéesEffectif IPv4 주소로 향하는 TCP/UDP는 호스트의 chemin·방화벽·Communication 가능 여부에 따른다.
게스트 DNS와 일반 TLS 소켓은 아직 없다. 도메인 nom 대신 valeurChiffre IPv4를 사용해야 한다. valeurAprès 추가된 GENET·DHCP 및 게스트 SSH·VNC는 [valeurExtérieur connexion Guide](GuideConnexionExtérieur.md)를 참고한다.
`ping 10.0.2.2` 성공은 NAT 관문까지의 확인이지 인터넷 통신의 증거는 아니다.
인터넷 ICMP는 QEMU user NAT와 Hôte `ping_group_range` 설정에 영향받으므로,
valeurExtérieur ping 실패만으로 TCP/UDP 통신까지 불가능하다고 판단하지 않는다.
[QEMU NAT 및 ICMP description](https://www.qemu.org/docs/master/system/devices/net.html)

## donnéesEffectif TCP/UDP 왕복 Exemples

VM을 실행한 상태에서 호스트의 다른 터미널에서:

```sh
cd /home/user/jkoros/platforms/rpi4-native
python3 Outils/ServeurÉchoExemple.py --tcp-port 9000 --udp-port 9001
```

게스트 안에서:

```text
cd /example/java
java ExempleRéseau 9000 9001
cd /example/python
python ExempleRéseau.py 9001
```

Java 예제는 TCP와 UDP, Python 예제는 UDP를 Hôte 응답기로 보내고 donnéesEffectif 받은 자료를 비교한다.
Java 예제의 클래스는 이미 탑재되어 있다. 이 예제의 recevoirValeur 제한은 700ms이므로 느린 호스트에서는
Exemples 자체의 valeurTemps 제한을 조정해야 할 nombre 있다.

## Hôte 또는 다른 PC에서 게스트로 접속하기

portMatériel 전달을 exécuterCommande 시 명시한다.

```sh
make desktop ARGS="--network --forward tcp:18080:8080 --forward udp:19001:9001"
```

- Hôte `127.0.0.1:18080/TCP` → 게스트 `10.0.2.15:8080/TCP`.
- Hôte `127.0.0.1:19001/UDP` → 게스트 `10.0.2.15:9001/UDP`.
- 게스트 프로그램이 그 포트에서 실제로 수신해야 한다. valeurAvantDirection 옵션이 서버를 시작하지는 않는다.
- `ftpd start`는 별도로 게스트 FTP를 시작한다. valeurDéfaut Hôte valeurContrôle 포트는 2121, 수동 Données 포트는 50000~50007이다.

valeurDéfaut `--network-host 127.0.0.1`은 루프백에만 연결한다. valeurAprès 추가한 valeurExtérieur connexion 기능에서는
`--network-host 0.0.0.0` 또는 Hôte LAN 주소를 명시하면 다른 PC의 직접 접속도 허용한다.
[게스트 SSH·VNC exécuterCommande Guide](GuideConnexionExtérieur.md)를 참고한다.
루프백 연결을 유지하면서 호스트의 SSH 서버를 이용할 경우 다른 PC에서 다음처럼 TCP 터널을 만든다.
`192.168.0.10`은 QEMU를 실행하는 호스트의 donnéesEffectif entréeÉlémentAccès 가능한 IP로 바꾼다.

```sh
ssh -N -L 18080:127.0.0.1:18080 user@192.168.0.10
```

다른 PC의 클라이언트는 이제 référenceSoi `127.0.0.1:18080`에 연결한다.
이것이 SSH를 거쳐 호스트의 QEMU valeurAvantDirection 포트와 게스트 8080에 연결된다.
SSH의 `-L`은 TCP 전용이다. UDP를 LAN에서 직접 받거나 게스트를 LAN의 독립 IP로 쓰려면
ajouterFinEntréeÉlément UDP relayerValeur 또는 TAP/브리지 백엔드 연결이 필요하며 élémentListeActuel exécuterCommande 옵션만으로는 제공하지 않는다.
FTP는 valeurContrôle 포트뿐 아니라 수동 Données portMatériel 전체도 전달해야 한다.

QEMU를 Ubuntu 가상머신 안에서 실행하는 경우 위의 'Hôte IP'는 그 Ubuntu의 주소다.
Ubuntu를 실행하는 바깥 가상화 프로그램도 해당 IP/SSH 포트에 entréeÉlémentAccès 가능한 네트워크 구성이 필요하다.

## inspecterÉtatValeur 재현과 vérifier rogner

```sh
make test-layers
```

- QMP CPU 0 레지스터: interpréteurCommandes `EL1h`, Java calculRésultat `EL0t`.
- 종료된 Java 프로그램의 `ps` valeurEntréeÉlément supprimerEntréeÉlément.
- Java GUI의 다른 terminal modeCommuter étatValeurAprès 별도 PID 및 `SUSPENDED` 상태를 `ps`와 `top`에서 vérifier.
- valeurPasserelle ICMP 왕복, FTP valeurClasse 업로드.
- 독립 Hôte 상대와 TCP/UDP 발신, 명시적 portMatériel 전달을 통한 TCP/UDP recevoirValeur 및 Données 비교.
- programmeQuitter 시 이번 점검이 만든 QEMU만 construireNettoyer.

결과는 [보고서](build/verification/execution-network-review/report.json)와
[valeurSériel valeurJournal](build/verification/execution-network-review/serial.log)에 저장한다.
보고서에 사용한 valeurNoyau SHA-256과 원시 QMP 레지스터를 남긴다.
최초 시도에서는 지원하지 않는 GUI 소스의 게스트 재컴파일 단계가 실패했고,
`initial-attempt-report.json`/`initial-attempt-serial.log`에 기록을 보관했다.
탑재된 GUI valeurClasse 사용으로 inspecterÉtatValeur 절차를 수정한 étatValeurAprès valeurSommet 항목은 construireTous 통과했다.

이번 donnéesEffectif Communication 검증의 범위는 **게스트와 QEMU 밖의 독립 Hôte Programme séparateur**opérandeTroisième.
별도 물리 PC, 공인 인터넷 extrémitéDestination, SSH 터널, donnéesEffectif Pi 4 Ethernet에서의 송수신은 시험하지 않았다.
valeurNoyau 셸을 Utilisateur 셸로 이식하거나 일반 프로세스 스케줄러를 추가한 변경은 아니다.
