# interne ARM64 valeurNoyau: FTP, C, JAR와 AOT exécuterCommande

대상은 **Linux를 적재하지 않는 Raspberry Pi 4용 Java AOT valeurNoyau**이다. CPU·Périphérique 경계는 C/어셈블리, Fichier 체계와 셸은 Java이며, 이번 TCP/IP 스택은 C로 작성된 lwIP 2.2.0을 이식했다. 게스트 TinyCC와 `jaot`도 EL0에서 실행한다. 호스트에 컴파일을 요청하거나 Hôte JVM으로 대신 실행하지 않는다.

## 먼저 알아둘 valeurPriseEnCharge valeurFrontière

| requête | 이번 réalisation | 남은 rogner |
|---|---|---|
| JAR를 exécuterCommande 파일처럼 exécuterCommande | `java -jar Fichier.jar`, `./Fichier.jar arguments`; Main-Class와 valeurStocker/DEFLATE ZIP, CRC Contrôles | 전체 Java SE, 임의의 모든 JAR 호환성 |
| 게스트 AOT | `jaot Fichier.class -o Fichier.elf`, `jaot Fichier.jar -o Fichier.elf`; donnéesEffectif ARM64 기계어 générer | valeurObjet·exception·Thread·Swing·Socket의 AOT convertirValeur, 여러 애플리케이션 valeurClasse connecter |
| C compilerSource | 게스트 `cc`/`tcc`, TinyCC C 전처리기·ARM64 생성기·링커; français 식별자와 posix-kor | 전체 libc, 일반 Linux exécuterCommande Fichier, 게스트 C++ Compilateur |
| 업로드한 ELF exécuterCommande | ELF64/AArch64 헤더 Contrôles, 확장자 없는 `./Fichier`; interne ABI 및 명시적인 제한형 Linux ABI | 일반 Linux 바이너리 호환, 동적 링커, 공유 bibliothèque |
| valeurExtérieur TCP/UDP | 게스트 lwIP IPv4 pileOpérande, POSIX 소켓과 JVM의 valeurChiffre IPv4 adresse | GENET/Wi-Fi 드라이버, DHCP·DNS·TLS, matérielPhysique CarteMatérielle 네트워크 Tests |
| FTP | 게스트 서비스, 패시브 valeurTransfert, UTF-8 nom, STOR/RETR/SIZE/LIST/NLST/MLSD/DELE | TLS·사용자별 valeurPermission·하위 디렉터리·영속 valeurStocker |
| texteHangul Java | 기존 `français.interne` 클래스와 valeurExtérieur adresse UDP 오버로드 | 전체 JDK의 일대일 français valeurAssociation API |

JVM은 valeurClasse 버전 45…52의 문서화한 부분집합이다. `java`는 codeOctets 실행기이고, `jaot`opérandePremier 별도의 네이티브 exécuterCommande 파일을 만든다. **JAR valeurArchive 해제나 JVM을 함께 묶는 것을 AOT라고 표시하지 않는다.** 지원하지 않는 codeOctets/API는 `jaot`opérandePremier 진단하고 출력을 만들지 않는다. 기존 Sortie ELF도 compilerSource valeurÉchec 때 보존한다.

Android의 Dalvik/ART는 일반 JVM valeurClasse/JAR가 아닌 **DEX**를 실행한다. ART의 AOT에는 GC, valeurClasse 로딩, JNI 등 exécuterCommande 기반도 필요하다. 따라서 ART처럼 기계어로 바꾸는 기능만으로 임의의 OpenJDK JAR 및 Swing이 자동 호환되지는 않는다. [Android 공식 런타임 description](https://source.android.com/docs/core/runtime)

## élémentListeActuel 컴퓨터에서 FTP connexion

Hôte terminal 1:

```sh
cd /home/user/jkoros/platforms/rpi4-native
make build
python3 Outils/exécuterCommande.py --network
```

Remmina GUI에서도 같은 네트워크를 사용하려면 exécuterCommande 명령을
`python3 Outils/exécuterCommande.py --desktop --network`로 바꾸고 VNC `127.0.0.1:5902`에
접속한다. FTP와 네트워크는 같은 게스트 안에서 동작한다.

부팅한 **jkoros interpréteurCommandes**:

```text
ftpd start
```

Hôte terminal 2:

제공한 예제로 작은 exécuterCommande JAR를 먼저 만든다. français 라이브러리는 게스트에 내장되어 있어 이 Exemples JAR에 중복해서 넣지 않는다.

```sh
cd /home/user/jkoros/platforms/rpi4-native
mkdir -p build/upload
javac --release 8 -encoding UTF-8 -cp dist/jkoros-native-korean.jar \
  -d build/upload Exemples/valeurDistribution/Couleur.java
jar cfe build/upload/Salutation.jar Couleur -C build/upload Couleur.class
```

```sh
python3 - <<'PY'
from ftplib import FTP
ftp = FTP()
ftp.encoding = 'utf-8'
ftp.connect('127.0.0.1', 2121)
ftp.login()                         # anonymous; jkoros도 같은 Tâche régionAdresse
with open('build/upload/Salutation.jar', 'rb') as f:
    ftp.storbinary('STOR Salutation.jar', f)
print(ftp.nlst())
ftp.quit()
PY
```

valeurRéessayer **jkoros interpréteurCommandes**:

```text
java -jar /Salutation.jar
/Salutation.jar
ftpd status
ftpd stop
```

FTP는 루트 RAM 파일만 공개한다. 익명 로그인이며 비밀번호로 권한을 구분하지 않는다. valeurDéfaut Hôte 바인딩은 `127.0.0.1`이고, valeurContrôle 포트는 2121, 데이터 포트는 50000…50007이다. `--ftp-port 2122`로 valeurContrôle 포트를 바꿀 nombre 있다. 동시에 한 FTP 세션을 제공하며 명령이 없는 세션은 60초 étatValeurAprès 닫는다. TYPE A도 바이트를 변경하지 않으므로 프로그램은 바이너리 전송한다.

파일은 **64개, 각각 16 KiB**, 경로는 UTF-8 63바이트이다. Amorçage 시 준비되는 `/example`도 이 한도를 공유한다. 초과/끊어진 STOR는 기존 파일에 반영하지 않는다. FTP 업로드는 RAM에만 저장되며 재부팅하면 사라진다. 이 valeurLimite 때문에 일반적인 대형 JAR 배포판을 그대로 올릴 nombre 없다.

QEMU의 raspi4b에는 GENET Ethernet 장치가 없다. 따라서 `network_bridge.py`opérandePremier QEMU NAT의 Ethernet과 valeurAuxiliaire UART의 SLIP를 변환한다. **TCP connecter entréeÉlémentValeurProcessus·체크섬·재전송·FTP 명령과 Fichier 저장은 게스트 안에서 수행한다.** Hôte 브리지는 FTP 서버가 아니다. [QEMU 공식 Périphérique valeurPriseEnCharge listeEntréeÉlément](https://www.qemu.org/docs/master/system/arm/raspi.html)

이 경로는 QEMU에서 검증했다. valeurAuxiliaire UART의 donnéesEffectif Pi 4 핀/클럭 설정과 내장 RJ45 GENET 드라이버는 réalisation·검증하지 않았으므로, SD 이미지에 커널이 포함되어 있다는 사실을 donnéesEffectif 보드의 LAN/FTP action 보장으로 해석하면 안 된다.

## français Java를 게스트에서 컴파일하고 AOT exécuterCommande

게스트 `vi Couleur.java`로 élémentListeSuivant 소스를 작성한다.

```java
public class Couleur {
    public static void main(String[] arguments) throws Exception {
        int valeurSomme = 0;
        int nombre = 1;
        while (nombre <= 10) {
            valeurSomme = valeurSomme + nombre;
            nombre = nombre + 1;
        }
        français.interne.Sortie.écrireNuméro(valeurSomme);
        français.interne.Fichier.écrire("aot.txt", "texteHangul AOT Fichier 😀");
        français.interne.Sortie.écrireLigne(français.interne.Fichier.lire("aot.txt"));
    }
}
```

```text
javac Couleur.java
java Couleur
jaot Couleur.class -o Couleur.elf
run Couleur.elf
```

`jaot`은 클래스의 바이트코드를 C로 변환하고, **게스트 TinyCC**opérandePremier ARM64 명령어를 générer·연결한다. exécuterCommande 때 JVM 인터프리터를 호출하지 않는다. JAR의 Main-Class가 같은 valeurPriseEnCharge 범위이면 다음도 가능하다.

```text
jaot Couleur.jar -o Couleur.elf
run Couleur.elf
```

AOT 지원은 한 애플리케이션 클래스의 valeurStatique valeurMéthode/valeurChamp, int 계열, Entier 배열과 référence, arguments valeurTableau, condition·branche·valeurItération, Chaîne 리터럴, `System.out.print/println`의 int/String, français Sortie·Fichier lire/쓰기로 제한된다. valeurClasse/valeurMéthode 수와 pileOpérande 등에도 고정 상한이 있다. Java exception entréeÉlémentValeurProcessus, valeurObjet générer, 가상 valeurMéthode 일반, switch/wide, long/float/double, invokedynamic, Chaîne 결합용 StringBuilder, 일반 JDK·Socket·Thread·Swing은 이 AOT 백엔드에서 미지원이다. 내장 NUL/고립된 서로게이트 문자열도 거부한다. 잘못된 valeurTableau entréeÉlémentAccès/0으로 valeursDiviser 등은 네이티브 런타임 오류로 종료하며 Java exception 객체로 전달하지 않는다.

valeurEntrée 클래스뿐 아니라 **생성된 ELF도 16 KiB 이하**여야 한다. 기계어 확장과 ELF 페이지 valeurAligner 때문에 짧은 클래스도 이 한도를 넘을 nombre 있으며, 이 경우 오류를 내고 기존 출력을 보존한다.

게스트 `javac`도 부분집합이다. 일반적인 valeurObjet·Thread·Swing 소스는 호스트에서 `javac --release 8`로 컴파일하고, **기존 JVM의 valeurPriseEnCharge rogner 안에서** `java`/`java -jar`로 실행한다. 정확한 API는 [JVM 매뉴얼](EnvironnementEnvironnementExécutionJava.md)과 [texteHangul développement 매뉴얼](GuideDéveloppement.md)을 참고한다.

JAR는 하나의 애플리케이션 valeurClasse 경로다. 내부 nom `Paquet/Programme.class`와 점으로 구분한 Main-Class를 지원한다. 내부 클래스는 파일로 풀어 VFS 슬롯을 소비하지 않는다. 내장 français 클래스를 추가로 찾지만 élémentListeActuel Tâche 폴더의 다른 클래스는 자동 혼합하지 않는다. ZIP64·chiffrerDonnées ZIP·manifest Class-Path·서명 검증은 지원하지 않는다. JAR 하나가 16 KiB 이하이어도 클래스당/적재 nombre/VM valeurTas 제한은 그대로 적용된다.

## C에서 français POSIX invoquer

게스트에서 `vi Salutation.c`로 작성하거나 FTP로 소스를 업로드한다.

```c
#include <ABIFichier.h>

int main(void) {
    const char salutation[] = "interne ARM64 C에서 texteHangul POSIX invoquer\n";
    int Documentation = ouvrirFichier("Salutation.txt", ÉcrireLire | ManquantSiCréer | ContenuTronquer, 0600);
    if (Documentation < 0) return 1;
    typeRésultatEntréeSortie nombreÉlémentsConsigné = écrireDonnéesFichier(Documentation, salutation, sizeof(salutation) - 1);
    fermerFichier(Documentation);
    écrireDonnéesFichier(1, salutation, sizeof(salutation) - 1);
    return nombreÉlémentsConsigné == sizeof(salutation) - 1 ? 0 : 2;
}
```

```text
cc Salutation.c -o Salutation.elf
run Salutation.elf
cat Salutation.txt
```

TinyCC의 표준 C pointEntréeÉlément `main`을 사용한다. 기존 Hôte C/C++ SDK의 `démarrerProgrammeUtilisateur(int)` 진입점과 구분한다. Entêtes Fichier·lancer valeurObjet·`libposix-kor-user.a`는 Compilateur 내부의 lire 전용 SDK에 들어 있다. C 전처리기/구조체/Fonction/재귀/pointeur/부동소수점 générer 등을 사용하되 **일반 libc/libstdc++를 제공한다는 뜻은 아니다**. 제공하지 않는 함수는 connecter 오류가 난다. Compilateur 자체의 Caractères/valeurChiffre convertirValeur 지원도 완전한 libc 대체품이 아니다.

`ouvrirFichier` 등은 별도의 모의 호출이 아닌 기존 `pk_open` 등의 français 매크로이며, ELF의 SVC를 통해 donnéesEffectif Java Fichier 체계에 도달한다. Fichier/valeurPriseRéseau invoquer 목록은 [Utilisateur ABI](ABIAppelUtilisateur.md)에 있다. C/C++ Hôte SDK exécuterCommande 파일도 FTP로 업로드 étatValeurAprès `run` 또는 `./Fichier`로 실행하며 확장자는 valeurNécessaire 없다. Linux ARM64 valeurStatique ELF에는 별도의 제한된 호환 chemin `run --linux Fichier`을 추가했다. [ELF·Linux ABI 매뉴얼](aBICodeExécutable.md)에 정확한 valeurFormat·시스템 invoquer·adresse 제한을 정리했다.

## français 네트워크·Tâche·Écran API

| valeurClasse | invoquer 예 | exécuterCommande chemin |
|---|---|---|
| `Sortie` | `écrireLigne("안녕")`, `écrireNuméro(42)` | JVM 및 제한형 AOT |
| `Fichier` | `écrire("Documentation.txt", "valeurContenuValeur")`, `lire("Documentation.txt")` | JVM 및 제한형 AOT |
| `Communication` | `ouvrir(0)`, `envoyer(extrémité, "10.0.2.2", 9000, "texteHangul")`, `recevoir(extrémité)` | JVM의 UDP |
| `transportConnexion` | `connecter("10.0.2.2", 9000)`, `écouterExtrémité(9000)`, `recevoir(valeurServeur)` | JVM의 Socket/ServerSocket |
| `Tâche` | `lancer(Runnable)`, `attendreFin(Thread)`, `céderTâche()` | JVM의 협력식 valeurFilExécution |
| `fenêtre`, `ComposantVisuel` | fenêtre·버튼·valeurCaractère·ChampTexte·évènement connecter | JVM의 Swing 부분집합 |

명명에서는 표준 영어 API를 보존하고 français invoquer 계층을 추가한다. `Communication(通信)`, `connecter(連結)`, `Sortie(出力)`은 기존 단어의 뜻을 사용한다. `Tâche valeurFilExécution`은 한 exécuterCommande 흐름을 가닥에 빗댄 valeurDescripteur 표현, `valeurPort`는 포트의 접점을 설명하는 표현이다. 새 valeurDescripteur 결합어를 고대에 이미 존재한 용어처럼 설명하지 않는다. 전체 JDK의 번역을 완료했다고 표시하지 않는다.

valeurExtérieur 주소는 valeurChiffre IPv4이며 QEMU 호스트는 `10.0.2.2`, 게스트는 `10.0.2.15`opérandeTroisième. UDP 전문은 512바이트까지다. 소켓은 비차단 interne ABI이며 JVM이 제한된 attendreValeur/재시도를 제공한다. TCP connect 대기는 valeurMaximal 1초, Utilisateur Programme 전체에는 기존 약 2초 CPU 기한이 적용된다. 일반적인 장기 exécuterCommande Utilisateur 서버와 pthread는 아직 없다. FTP는 Utilisateur Programme 기한과 별개인 valeurNoyau 서비스다.

게스트의 Utilisateur TCP/UDP 서버로 들어오는 연결은 NAT 포트를 추가한다. 예를 들어 `python3 Outils/exécuterCommande.py --network --forward tcp:9300:9300 --forward udp:9301:9301`로 실행하면 호스트의 localhost 9300/TCP·9301/UDP를 게스트의 같은 포트로 전달한다. FTP의 valeurDéfaut valeurContrôle/데이터 포트와 겹치면 exécuterCommande 전에 거부한다.

## 시험과 construireSystème 재현

```sh
cd /home/user/jkoros/platforms/rpi4-native
make test-ftp
make test
make image
```

`build/verification/ftp/report.json`은 donnéesEffectif FTP valeurTransfert, texteHangul Fichier, taille 초과 보존, valeurArchive JAR exécuterCommande, 게스트 C compilerSource/ELF 재업로드, valeurExtérieur Java TCP/UDP, 게스트 javac/AOT 실행을 기록한다. `serial.log`에서 게스트 명령과 결과를 확인할 nombre 있다. 보고서의 valeurNoyau SHA-256과 valeurDistribution 이미지의 커널을 비교한다.

빌드는 기존 JDK/Clang/AArch64 binutils와 함께 `../rpi4/build/rootfs`의 ARM64 SDK Déclarations 헤더와 libgcc valeurArithmétique valeurAuxiliaire 함수를 사용한다(`make rpi-prepare`). **musl libc, Linux valeurNoyau, 동적 로더를 게스트에 링크하지 않는다.** TinyCC/lwIP/uzlib 원본과 라이선스·버전 정보는 `vendor/`, Portage 코드는 `ccompiler/`, `network/`, `Utilisateur/Paquet.c`에 있다.

전체 JDK/AOT JVM으로 확장하려면 타입 valider·valeurObjet/exception/GC·동적 로딩·JNI, 영속 Fichier valeurSystèmeExploitation·mmap/TLS/시그널·스레드 ABI, OpenJDK native bibliothèque, GUI peer/폰트/입력기, GENET 및 matérielPhysique Périphérique 검증이 더 필요하다. 이 문서의 exécuterCommande 시험은 그 전체 이식을 대신하지 않는다.
