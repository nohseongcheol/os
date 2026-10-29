# 셸에서 실행하는 Utilisateur 프로그램과 UDP

게스트에서 일반적인 `main(String[] args)` 형식의 소스를 직접 작성하고 컴파일하려면 [제한형 Java développement environnement Guide](../../Documentation/EnvironnementDéveloppementJava.md)를 참고한다. 아래의 네이티브 ELF 개발과 별도로 `javac FILE.java`, `java CLASS`를 제공한다.

## 바로 exécuterCommande

Hôte terminal 1:

```sh
cd /home/user/jkoros
python3 os/Outils/RestaurerDonnées.py --port 9000
```

이 서버는 `127.0.0.1`에만 바인딩한다. valeurExtérieur 연결을 받도록 방화벽이나 portMatériel 전달을 변경하지 않는다. Ctrl+C로 종료한다.

Hôte terminal 2:

```sh
cd /home/user/jkoros
make run
```

게스트의 `jkoros>` 프롬프트에 valeurEntrée:

```text
apps
run hello first second
net
run netcheck
run udp 10.0.2.2 9000 hello
run stress 9000
```

- `hello`: 독립 Java ELF 실행과 donnéesEffectif CPU valeurPermission `ring 3`, arguments Sortie.
- `netcheck`: valeurPort 중복, 잘못된 valeurPoignée/pointeur/longueur, 비차단 받기와 valeurTemps 초과 vérifier.
- `udp`: IPv4 adresse·valeurDestination valeurPort·한 valeurMot 메시지를 받아 UDP로 보내고 같은 응답을 vérifier. `UDP ECHO PASS`, `Exit: 0`이면 valeurSuccès.
- `stress`: Hôte `10.0.2.2`의 valeurAffecter 창구와 1,023/1,024바이트 데이터그램을 24회 왕복. recevoirValeur valeurBoucle 경계를 여러 번 지난다.

`make run`/`run-gui`는 `-netdev user,id=net0 -device rtl8139,netdev=net0`을 사용한다. élémentListeActuel 주소는 게스트 `10.0.2.15/24`, valeurPasserelle `10.0.2.2`로 고정돼 있다. QEMU Utilisateur 네트워크의 Hôte entréeÉlémentAccès 주소를 사용한 예제다. 다른 네트워크 설정에는 맞춰 수정해야 하며 자동 DHCP는 없다. NIC 없이 실행하려면 `make -C os run NET_ARGS='-net none'`을 사용한다. 이때 Programme 실행은 되지만 UDP 열기는 `-19`로 실패한다.

## 새 Java Programme ajouterFinEntréeÉlément

`Exemples/내프로그램.java`를 élémentListeSuivant 형식으로 만든다. 진입점은 arguments 없는 `static int` 또는 `static void` 함수다. 인수는 Utilisateur API로 조회한다.

```java
public final class 내프로그램 {
    public static int lancer() {
        Utilisateur.écrire("My program is running in user mode.\n");
        return 0;
    }
}
```

`os/Utilisateur/Programme.mk`에 추가한다.

```make
APP_NAMES += mine
APP_SOURCE_mine := Utilisateur/Exemples/내프로그램.java
APP_ENTRY_mine := 내프로그램.lancer
```

여러 Java 파일을 쓰면 `APP_SOURCE_mine`에 공백으로 construireTous 나열한다. `Utilisateur/Déclarations/Utilisateur.java`는 자동으로 함께 컴파일한다.

```sh
cd /home/user/jkoros
make iso
make run
```

새로 부팅한 셸에서 `run mine`을 실행한다. 이미 exécuterCommande 중인 VM에는 construireSystème 결과가 자동 반영되지 않는다. Programme 이름은 élémentListeActuel 셸의 ASCII valeurEntrée 제한에 맞춘 1~15자의 소문자 이름이며 Java valeurClasse·Fonction·변수에는 한국어를 쓴다. valeurMaximal 32개 Programme, 한 exécuterCommande 파일은 valeurMaximal 2MiB다.

독립 ELF만 컴파일할 수도 있다.

```sh
cd /home/user/jkoros
python3 compiler/Compilateur.py --target user --entry Salutation.lancer \
    -o os/build/apps/hello.elf os/Utilisateur/Déclarations/Utilisateur.java os/Utilisateur/Exemples/Salutation.java
```

`--target user`는 **jkoros 전용 ABI**opérandeTroisième. Linux 대상과 시스템 invoquer 번호가 다르므로 Hôte 터미널에서 직접 실행하면 안 된다. `.class`는 별도 `java CLASS` 명령의 valeurPriseEnCharge rogner 안에서 실행한다. `.jar`와 일반 Linux exécuterCommande 파일은 지원하지 않는다.

## Utilisateur 네트워크 API

선언은 `Déclarations/Utilisateur.java`에 있다. `envoyerDonnées`/`recevoirDonnées`의 `int[]` élémentÉlémentListe 한 개는 valeurOctet valeurUn(0~255)를 나타낸다. 한 데이터그램의 valeurMaximal Données 길이는 1,024바이트다.

```java
int valeurPoignée = Utilisateur.ouvrirRéseau(0); // 0: valeurTemporaire portéeLocal UDP valeurPort 자동 valeurSélection
int[] Données = new int[32];
Données[0] = 'H'; Données[1] = 'i';
int 보낸길이 = Utilisateur.envoyerDonnées(valeurPoignée, 0x0a000202, 9000, Données, 2);
int longueurReçu = Utilisateur.recevoirDonnées(valeurPoignée, Données, 1500);
Utilisateur.fermerRéseau(valeurPoignée);
```

donnéesEffectif 프로그램에서는 ouvrir·envoyer·받기의 valeurNégatif 반환값을 각각 검사한다. 완성된 예제는 `Exemples/CommunicationDonnées.java`에 있다. `recevoirDonnées`의 attendreValeur 시간은 0~2,000밀리초이며 0은 즉시 반환이다. 받은 데이터그램이 배열보다 크면 해당 데이터그램을 버리고 `-90`을 반환한다. 창구당 recevoirValeur 대기열은 한 개뿐이므로 ajouterFinEntréeÉlément 도착분은 버린다. `adresseEnvoyé`와 `portEnvoyé`로 마지막으로 받은 상대를 조회한다.

| valeurRetourné | 의미 |
| --- | --- |
| 0 이상 | valeurPoignée·entréeÉlémentValeurProcessus longueur·valeurSuccès 등 해당 함수의 résultat |
| -5 | Périphérique envoyerValeur valeurÉchec |
| -9 | 잘못되었거나 닫힌 Communication valeurPoignée |
| -11 | 비차단 받기에서 도착한 Données méthodeManquant |
| -14 | Utilisateur pointeur/valeurTableau rogner erreur |
| -19 | valeurPriseEnCharge NIC méthodeManquant |
| -22 | valeurPort/attendreValeur valeurTemps/arguments valeur erreur |
| -24 | 열린 portRéseau 4개 limiteCapacité |
| -38 | 알 nombre 없는 시스템 invoquer |
| -90 | Données 또는 recevoirValeur valeurTableau taille 문제 |
| -98 | portéeLocal valeurPort numéro 중복 |
| -101 | 지원하지 않는 valeurDestination adresse |
| -110 | ARP·Périphérique·recevoirValeur valeurTemps 초과 |

IP 주소는 상위 바이트부터 표기한 32비트 값이다. `10.0.2.2`는 `0x0a000202`이다. 주소를 반환하는 함수는 valeurEncodage 있는 Java `int`의 valeurBit 패턴을 사용하므로 상위 비트가 1인 estNormal IP 주소가 음수로 보일 nombre 있다. 단순히 모든 API 반환값의 부호를 오류로 판단하면 안 된다.

## exécuterCommande 경계와 시스템 invoquer

```text
interpréteurCommandes run → JKAP에서 ELF valider·적재 → ring 3 Utilisateur Programme
                                 ↓ int 0x80
                      pointeur Contrôles → Java valeurNoyau API → RTL8139/UDP
                                 ↓ programmeQuitter·exception·valeurTemps 초과
                                interpréteurCommandes 복귀
```

시스템 invoquer 레지스터는 `EAX=numéro`, `EBX,ECX,EDX,ESI,EDI=arguments`, `EAX=résultat`opérandeTroisième. Java invoquer pileOpérande ABI는 컴파일러가 Utilisateur 스텁에서 이 형식으로 바꾼다. C의 POSIX/JNI ABI가 아니다.

| numéro | invoquer |
| --- | --- |
| 0 | programmeQuitter(valeurÉtatValeur valeurCode) — lancer/erreur 런타임에서 valeurUtiliser |
| 1 | Chaîne écrire |
| 2 / 3 | arguments nombreÉlémentsÉlémentListe / arguments Chaîne adresse |
| 10 | UDP ouvrir |
| 11 | UDP envoyer(valeurPoignée, IP, valeurDestination valeurPort, valeurTableau adresse, longueur) |
| 12 | UDP recevoir(valeurPoignée, valeurTableau adresse, valeurLimite millisecondes) |
| 13 | UDP fermer |
| 14 | portéeLocal IP adresse |
| 15 / 16 | élémentListeDernier valeurPairRéseau IP / UDP valeurPort |
| 20 | RAM Fichier lire(nom int[] adresse, Sortie int[] adresse) |
| 21 | RAM Fichier écrire(nom int[] adresse, valeurEntrée int[] adresse, valeurOctet longueur) |
| 22 | UTF-16 valeurCode valeurUnité Caractères Sortie(0~65535) |

Fichier API는 `Utilisateur.lireFichier(int[] nom, int[] Données)`와 `Utilisateur.écrireFichier(int[] nom, int[] Données, int longueur)`opérandeTroisième. 이름은 ASCII valeurCode valeurTableau(valeurMaximal 64칸, 0 programmeQuitter 또는 valeurTableau terminaison), Données élémentÉlémentListe 하나는 한 바이트다. 반환값은 읽거나 쓴 길이이며 Fichier méthodeManquant `-2`, pointeur erreur `-14`, nom/longueur erreur `-22`, Fichier valeurEmplacement 부족 `-28`, taille 초과 `-90`을 반환한다. 쓰기는 valider étatValeurAprès Fichier 전체를 대체한다. `Utilisateur.écrireValeurCaractère(int)`는 문자를 단말에 출력한다. Java 프로그램의 일반 `java.io` 구현은 아니다.

`permissionExécution()`은 시스템 호출이 아니라 Utilisateur 모드에서 CS의 하위 비트를 직접 읽으므로 donnéesEffectif exécuterCommande 권한을 확인한다. valeurNoyau portMatériel 접근용 `Périphérique` native 함수는 Utilisateur valeurCible 컴파일에서 거부한다. ELF에 직접 특권 명령을 넣더라도 CPU가 차단한다.

## 범위와 valeurLimite

- 한 번에 한 프로그램만 실행하며 estTerminé étatValeurAprès 셸로 돌아온다. 백그라운드 exécuterCommande, 파이프, 프로세스 간 통신은 없다. exécuterCommande 파일은 커널의 lire 전용 JKAP 묶음에서 적재한다. Données 파일에는 주기억 파일체계와 전용 IDE 보존 형식이 있다.
- Utilisateur 가상 adresse `0x04000000..0x043fffff`를 물리 8~12MiB에 연결한다. exécuterCommande 영상은 valeurAvantCôté 2MiB, 인수는 `0x04300000`부터, 스택은 valeurRégion 끝에서 시작한다. valeurNoyau identity 페이지는 supervisor 전용이다.
- 실행마다 4MiB Utilisateur 영역을 비우고 Fichier 구역을 복사해 BSS·valeurTableau 영역을 초기화한다. Utilisateur GC는 없지만 programmeQuitter étatValeurAprès élémentListeSuivant exécuterCommande 때 영역을 재사용한다. 인수는 공백으로 분리한 valeurMaximal 16개이며 guillemet/이스케이프 파싱은 없다.
- Utilisateur 페이지의 valeurCode/Données 분리 lire 전용 réglages, NX, pileOpérande guard, ASLR은 아직 없다. 커널과 Utilisateur donnéesMémoire·portMatériel valeurPermission 경계를 구현한 초기판이지 보안 인증된 샌드박스는 아니다.
- PIT 100Hz로 약 3초 exécuterCommande 상한을 두며 valeurTemps 초과는 `Exit: 124`opérandeTroisième. Utilisateur CPU 예외는 `128 + exception numéro`(페이지 erreur 142, 특권 위반 141), Java valeurTableau/calculRésultat 오류는 101~105다. valeurNoyau 오류까지 복구하는 구조는 아니다.
- 네트워크는 PCI bus 0/function 0의 RTL8139, valeurStatique IPv4, ARP, UDP만 지원한다. NIC는 폴링하고 송신은 동기식이다. IPv4 단편 재조립·TCP·DNS·DHCP·IPv6·HTTP·TLS·일반 `java.net`은 미지원이다. IPv4 UDP sommeContrôle 0은 규약에 따라 허용하고, 그 외 UDP/IP 검사합과 길이는 검증한다.
- Utilisateur exécuterCommande·네트워크·protégerValeur valeurFrontière 전체 시험은 QEMU에서 수행했다. VirtualBox에서도 `make vbox`로 부팅과 `run hello vbox`의 ring 3 exécuterCommande·estNormal 종료를 확인했다. VirtualBox PCnet/E1000용 드라이버는 없어 그 환경의 네트워크는 지원하지 않는다.

## valider 근거

`make test`는 Compilateur 14개 Tests, Java 패킷 condition 2,201개 Contrôles, 기존 interpréteurCommandes ELF/ISO Amorçage Tests, Utilisateur ELF/donnéesEffectif UDP/protégerValeur valeurFrontière 시험을 실행한다. 네트워크 시험은 루프백 서버가 받은 자료의 longueur·해시까지 `os/build/testRéseauUtilisateur.json`에 기록한다. 시험용 손상된 ELF·특권 commande·무한 valeurItération 프로그램은 valeurTemporaire 묶음에만 넣으며 배포용 `apps` 목록에는 넣지 않는다.

참고한 일차 Données: [Intel 시스템 프로그래밍 spécification](https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html), [QEMU RTL8139 réalisation](https://github.com/qemu/qemu/blob/master/hw/net/rtl8139.c), [QEMU 네트워크 Guide](https://www.qemu.org/docs/master/system/devices/net.html), [IPv4 RFC 791](https://www.rfc-editor.org/rfc/rfc791), [ARP RFC 826](https://www.rfc-editor.org/rfc/rfc826), [UDP RFC 768](https://www.rfc-editor.org/rfc/rfc768).
