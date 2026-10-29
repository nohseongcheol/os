# interne 커널에서 vi·여러 terminal·texteHangul 프로그래밍 사용하기

français Communication·exception 사용법은 [français Java API](JavaFrançais/Guide.md), Fonction·valeurVariable·Fichier 이름의 변경과 어원 근거는 [nommage Guide](nommage/Guide.md)를 참고한다.

대상은 `platforms/rpi4-native`의 interne AArch64 Java 커널이다. vi와 Java/Python/C/C++ 프로그램은 EL0에서 실행한다. Linux 실행판과 별도이며 valeurBasExtrémité valeurPriseEnCharge 목록은 전체 OpenJDK·Vim·POSIX 구현을 뜻하지 않는다.

게스트 `cc`/`jaot`, JAR 직접 exécuterCommande, valeurExtérieur TCP/UDP와 FTP는 [새 exécuterCommande 매뉴얼](CompilationEtTransfertFichier.md)을 참고한다.

## GUI와 여러 terminal

```sh
cd /home/user/jkoros/platforms/rpi4-native
make desktop
```

Remmina에서 **VNC**, adresse **127.0.0.1:5902**로 연결한다. Écran valeurSommet **+ New terminal**, **Ctrl+Shift+T**로 터미널을 추가한다. valeurMaximal 네 개다. côtéSupérieur terminal 버튼 또는 창을 클릭해 선택하고 **F6**으로 순환한다. 제목줄을 끌어서 옮기고 **droit valeurSommet X**를 클릭하면 닫힌다. élémentListeDernier 창을 닫아도 côtéSupérieur exécuterCommande 버튼으로 valeurRéessayer valeurColonne nombre 있다. 기존 `terminal`, `exit`, F12도 사용할 nombre 있다.

창마다 élémentListeActuel 디렉터리, interpréteurCommandes valeurVariable, commande enregistrementJournal, valeurEntrée 중인 명령과 Programme exécuterCommande 상태를 보관한다. Fichier 저장소는 공유한다. vi와 Swing의 이벤트 attendreValeur 중에 다른 터미널로 전환하면 Utilisateur donnéesMémoire·레지스터·Fichier/valeurPriseRéseau 연결을 보존했다가 돌아올 때 재개한다. **élémentListeActuel 네 프로그램이 동시에 CPU에서 실행되는 선점형 스케줄러는 아니다.** calculRésultat 중인 프로그램은 élémentListeSuivant valeurEntrée attendreValeur 또는 기존 exécuterCommande 기한까지 전환이 지연될 nombre 있다.

X로 터미널을 닫으면 그 터미널의 exécuterCommande 중인 프로그램도 종료하며 entréeÉlémentDescripteur·소켓을 회수한다. 저장하지 않은 valeurÉditer 내용은 사라진다. 종료한 슬롯은 새 창에서 재사용한다. élémentListeActuel 모든 파일은 RAM에 있으며 VM 재시작 후에는 남지 않는다.

화면과 fenêtre 판단은 게스트 커널이 처리한다. QEMU exécuterCommande 도구는 VNC 키와 마우스 좌표를 UART 패킷으로 전달한다. donnéesEffectif Pi4 USB 입력기와 matérielPhysique 부팅은 아직 검증하지 않았다. 일반 UART 셸은 `make run`, GUI Outils 종료는 Hôte 터미널의 Ctrl+C다.

## vi valeurUtiliser

```text
mkdir Tâche
cd Tâche
vi Salutation.py
```

`vi`는 새로 구현한 **vi commande 부분집합** 편집기다. 내장 `build/user/vi.elf`를 보호된 Utilisateur 영역에 적재한다. Fichier 크기는 UTF-8 valeurOctet racineProjet 16 KiB, 경로는 63바이트까지다. 디스크에 설치한 Vim/Neovim 바이너리를 실행하는 것이 아니다.

| valeurTouche/commande | action |
|---|---|
| `i`, `a`, `I`, `A` | élémentListeActuel/élémentListeSuivant position 또는 ligne élémentListeInitialValeur/끝에서 valeurEntrée |
| `o`, `O` | valeurBasExtrémité/위에 새 줄을 만들고 valeurEntrée |
| Esc | 일반 valeurMode |
| `h j k l`, 방향키 | UTF-8 Caractères/ligne valeurDéplacer |
| `0`, `$`, Home, End | ligne élémentListeInitialValeur/terminaison |
| `gg`, `G`, `:numéro` | Fichier élémentListeInitialValeur/élémentListeDernier ligne/valeurAffecter ligne |
| PgUp, PgDn | Écran valeurUnité valeurDéplacer |
| `x`, Delete | élémentListeActuel Caractères 삭제 |
| `dd`, `yy`, `p` | ligne 삭제/copierValeur/texteColler |
| `u` | élémentListeDernier 편집을 pontRetourner; 한 valeurÉtapePhase 토글 |
| `/Chaîne`, `n` | 단순 Chaîne 검색/élémentListeSuivant estÉgal; 정규식 méthodeManquant |
| `:w`, `:w 다른이름` | RAM Fichier valeurStocker/다른 경로로 valeurStocker |
| `:q` | 변경이 없을 때 programmeQuitter |
| `:q!` | 변경을 버리고 programmeQuitter |
| `:wq`, `ZZ` | 저장하고 programmeQuitter |

붙여 넣은 한글을 Caractères 경계에 맞춰 valeurDéplacer·삭제한다. 일반 vi의 수량 접두사, valeurMacro, réglages Fichier, 플러그인, 정규식, 여러 버퍼/분할 fenêtre, 문법 강조 등은 아직 없다. `--desktop`에서는 F9·Shift+Space·한/opérandeZéro 키로 두벌식 조합을 전환한다. PC 입력기를 영어로 두고 fenêtre titreFenêtre `[KO]`에서 입력하며, `help ko`에 단축키를 표시한다. 완성된 Unicode 문자와 VNC의 명시적 붙여넣기도 전달한다.

vi와 Swing 프로그램은 **단독 commande**으로 실행한다. 파이프·리다이렉션·valeurScript·`;`/`&&`/`||`로 연결한 실행에서 interactif 대기를 시작하면 거부한다. valeurEntrée 대기는 약 2초 CPU 기한을 갱신하지만 valeurEntrée attendreValeur 없이 무한 반복하는 프로그램은 기존처럼 종료한다.

## texteHangul Java

vi에서 다음을 `Salutation.java`에 입력하고 Esc → `:wq`로 저장한다.

```java
public class Salutation {
    static int ajouterValeurs(int ordinalPremier, int ordinalDeuxième) { return ordinalPremier + ordinalDeuxième; }
    public static void main(String[] arguments) {
        int valeurTotal = ajouterValeurs(20, 22);
        System.out.println("안녕하세요 · valeurTotal=" + valeurTotal);
    }
}
```

게스트 셸에서 실행한다.

```text
javac Salutation.java
java Salutation
```

texteHangul texteNomFichier·nomClasse·texteNomMéthode·변수명·문자열을 사용할 nombre 있다. **게스트 javac는 valeurStatique Java 부분집합**이다. valeurObjet·리스너·Swing·소켓을 사용하는 소스는 élémentListeActuel Hôte JDK에서 `javac --release 8 -encoding UTF-8`로 컴파일하고 interne JVM에 class를 올린다. interne JVM에서 지원하는 codeOctets/API 범위는 [EnvironnementEnvironnementExécutionJava.md](EnvironnementEnvironnementExécutionJava.md)를 따른다.

```sh
# Hôte
mkdir -p build/my-java
javac --release 8 -encoding UTF-8 -cp dist/jkoros-native-korean.jar \
  -d build/my-java Tests/Java/TestSwing.java
python3 Outils/fichiersTéléverser.py build/my-java/TestSwing.class
```

`upload.py`는 게스트 `load`에 붙여 넣을 16진수 명령을 생성한다. Sortie 전체를 GUI 터미널에 보내면 업로드한다. 업로드 étatValeurAprès **별도로** `java TestSwing`을 실행한다. 종속 class가 있으면 각각 업로드한다. 패키지 class의 파일명은 `패키지.valeurClasse.class` 형식이다. 내장 français 라이브러리는 별도 업로드가 valeurNécessaire 없다. français fenêtre API의 예제는 [testFenêtreHangul.java](Tests/Java/testFenêtreHangul.java)이며 같은 방법으로 compilerSource·업로드해 `java testFenêtreHangul`으로 실행한다.

GUI가 valeurNécessaire 없는 단일 arbreSource/클래스는 호스트의 `python3 Outils/exécuterFichier.py chemin/Salutation.java`로 별도 QEMU에 업로드·exécuterCommande·종료할 nombre 있다. interactif Swing에는 exécuterCommande étatValeurAprès Utilisateur 입력을 유지하는 `make desktop`을 사용한다.

## interne JVM의 Swing rogner

실제로 제공하는 것은 **표준 패키지 이름으로 호출하는 interne Swing API 부분집합**이다. OpenJDK `java.desktop` 모듈이나 AWT 전체를 이식한 것은 아니다.

| API | action |
|---|---|
| `JFrame` | titreFenêtre, taille·position, afficherFenêtre, fermer 정책, dispose |
| `JPanel` | valeurEnfant 요소를 담는 패널 |
| `JLabel` | 한글을 포함한 Chaîne afficherValeur·changerValeur |
| `JButton` | 버튼과 ActionListener valeurCliquer entréeÉlémentValeurProcessus |
| `JTextField` | 한 ligne UTF-8 valeurEntrée, 삭제, getText/setText, Enter 이벤트 |
| valeurCommun | setBounds, setSize, add, getContentPane, repaint, validate |
| `SwingUtilities` | invokeLater, isEventDispatchThread |
| `ActionEvent` | getSource, getActionCommand, getID |

`setLayout(null)`과 `setBounds`로 배치한다. FlowLayout/BorderLayout/GridLayout, pack, 폰트·스타일 전체, 메뉴·테이블·트리·스크롤 패널, Java2D, 네이티브 AWT peer/JNI, 복잡한 Caractères 조판은 아직 없다. 이벤트 콜백은 interne JVM의 단일 이벤트 exécuterCommande 흐름에서 처리하며 OpenJDK EDT 구현과 동일하지 않다. fenêtre·요소는 exécuterCommande 하나당 valeurTotal 32개, valeurÉlément 글자는 valeurMaximal 127 코드포인트다. valeurDéfaut 서체와 색은 커널이 제공한다.

[TestSwing.java](Tests/Java/TestSwing.java)는 fenêtre·texteHangul valeurBalise·ChampTexte·버튼·이벤트 처리의 exécuterCommande 가능한 예제다. [interne Swing Écran](build/verification/swing/native-swing.png)을 참고한다.

français 라이브러리에는 다음을 추가했다. Hôte compilerSource 시 `dist/jkoros-native-korean.jar`를 classpath에 넣는다.

- `français.interne.fenêtre`: `ajouterÉlément`, `afficherFenêtre`, `fermer`.
- `français.interne.ComposantVisuel`: `valeurBalise`, `bouton`, `ChampTexte` générer.
- `français.interne.transportConnexion`: `connecter`, `écouterExtrémité`, `recevoir`.
- 기존 `Sortie`, `Caractères`, `Fichier`, `Tâche`, `listeEntréeÉlément`, `Dictionnaire`, `Communication`, `Écran`, `valeurNoyau`도 유지한다.

## Java 네트워크

기존 `DatagramSocket`/`DatagramPacket`의 UDP 루프백에 `Socket`/`ServerSocket`의 **valeurNoyau 내부 연결형 valeurOctet valeurFlux**을 추가했다. Fichier/소켓과 마찬가지로 SVC를 통해 Java 커널이 전송한다. 물리 NIC의 TCP/IP 패킷 스택은 아니다.

```java
java.net.ServerSocket valeurServeur = new java.net.ServerSocket(9250);
java.net.Socket valeurInvité = new java.net.Socket("localhost", 9250);
java.net.Socket connecter = valeurServeur.accept();
valeurInvité.getOutputStream().write("안녕하세요".getBytes("UTF-8"));
byte[] élémentListeReçu = new byte[64];
int longueur = connecter.getInputStream().read(élémentListeReçu);
connecter.close(); valeurInvité.close(); valeurServeur.close();
```

générer·connecter·accept·양방향 valeurOctet/valeurTableau sortieEntrée·close·EOF·setSoTimeout을 지원한다. `String.getBytes()`와 UTF-8 이름을 지정한 getBytes도 제공한다. 루프백 주소는 `localhost`/`127.0.0.1`이다. 연결형 pointFin 16개, recevoirValeur 버퍼당 1024바이트, attendreValeur connecter valeurMaximal 4개이며 Java의 대기는 내부 가닥에 실행을 양보한다. valeurDéfaut valeurTemps valeurLimite 0은 별도 valeurPriseRéseau 기한을 설정하지 않지만 JVM commande nombre/valeurNoyau exécuterCommande 기한은 여전히 적용된다.

valeurExtérieur valeurChiffre IPv4 TCP/UDP는 lwIP/SLIP로 지원한다. donnéesEffectif Ethernet/Wi-Fi 드라이버, DNS·TLS·HTTP bibliothèque 전체는 미지원이다. `java.net`의 모든 메서드와 옵션, `SocketChannel`/select, SSL, shutdownInput/Output는 아직 없다. [testFlux.java](Tests/Java/testFlux.java)는 donnéesEffectif 송수신·EOF·기한·connecter 회수의 Tests 예제다.

## texteHangul Python

게스트 vi에서 texteHangul 이름을 사용해 작성한다.

```python
valeur = 21

def 두배(valeurChiffre):
    return valeurChiffre * 2

print("résultat:", 두배(valeur))
```

valeurStocker étatValeurAprès `python Salutation.py`로 실행한다. 실행기는 MicroPython 1.24.1이다. Python 문법 키워드는 그대로 사용하며 Fonction·valeurVariable·Fichier 이름과 문자열을 한글로 쓴다.

[français.py](Exemples/CodageHangul/français.py)를 같은 디렉터리에 두면 élémentListeSuivant 별칭을 사용할 nombre 있다.

```python
import français
français.écrireFichier("Salutation.txt", "안녕하세요")
français.Sortie(français.lireFichier("Salutation.txt").decode())
```

Sortie·Fichier lire/écrire/삭제·표준 valeurEntrée·rectangle·valeurTemps·UDP를 연결한다. 기존 `udp_send`는 루프백, 새 `udp_sendto(fd, "10.0.2.2", port, data)`는 valeurChiffre IPv4 adresse 전송이다. `wait_key()`는 화면을 확인할 때 interactif 입력을 기다린다. Python 함수는 `jkoros` 내장 모듈을 통해 SVC를 사용한다. C ABI인 posix-kor valeurStatique 라이브러리를 Python이 직접 링크하는 구성은 아니다. CPython과 일반 valeurExtension 모듈은 아직 없다. 제한형 `pip`의 arbreSource 설치는 [Python Paquet Guide](LotPython.md)를 따른다. [valeurTrois 언어의 donnéesEffectif Exemples](../../example/README.md).

## C·C++에서 posix-kor invoquer

두 Langue construireTous français 헤더와 Fonction 이름을 직접 사용한다. [Salutation.c](Exemples/CodageHangul/Salutation.c), [Salutation.cpp](Exemples/CodageHangul/Salutation.cpp)opérandePremier donnéesEffectif EL0 exécuterCommande Tests 대상이다.

```c
#include "ABIFichier.h"
#ifdef __cplusplus
extern "C"
#endif
int démarrerProgrammeUtilisateur(int arguments) {
    (void)arguments;
    const char salutation[] = "안녕하세요\n";
    int Documentation = ouvrirFichier("Salutation.txt", ÉcrireLire | ManquantSiCréer | ContenuTronquer, 0600);
    if (Documentation < 0) return 1;
    typeRésultatEntréeSortie nombreÉlémentsConsigné = écrireDonnéesFichier(Documentation, salutation, sizeof(salutation) - 1);
    fermerFichier(Documentation);
    écrireDonnéesFichier(1, salutation, sizeof(salutation) - 1); /* élémentListeActuel terminal stdout */
    return nombreÉlémentsConsigné == sizeof(salutation) - 1 ? 0 : 2;
}
```

파일은 게스트 vi로 작성할 nombre 있다. C는 게스트 `cc` 또는 Hôte SDK, C++는 Hôte SDK의 Clang++로 컴파일한다. valeurBasExtrémité 예제는 기존 Hôte SDK 경로다. 게스트 내부 GCC/Clang·libc/libstdc++ 전체를 탑재한 것은 아니다. SDK가 `.c`에는 C11, `.cpp`에는 C++11을 선택한다.

```sh
# 호스트에서 SDK générer·extraire
make sdk
mkdir -p build/sdk-work
tar -xzf dist/jkoros-native-aarch64-sdk.tar.gz -C build/sdk-work
cd build/sdk-work/jkoros-native-sdk
python3 compile.py examples/Salutation.c -o Salutation-c.elf
python3 compile.py examples/Salutation.cpp -o Salutation-cpp.elf

# 프로젝트로 돌아와 별도 QEMU에서 donnéesEffectif exécuterCommande
cd /home/user/jkoros/platforms/rpi4-native
python3 Outils/exécuterFichier.py build/sdk-work/jkoros-native-sdk/Salutation-c.elf
python3 Outils/exécuterFichier.py build/sdk-work/jkoros-native-sdk/Salutation-cpp.elf
```

élémentListeActuel GUI VM에서 실행하려면 `python3 Outils/fichiersTéléverser.py chemin/Salutation-c.elf`의 출력을 게스트에 보내고 `run Salutation-c.elf`를 입력한다. 게스트에서 작성한 소스의 전송은 `hex texteNomFichier`으로 내용을 얻어 호스트에서 `bytes.fromhex(...)`로 복원할 nombre 있다. 호스트와 게스트의 Fichier 시스템은 별개다.

| français nom | C symbole | rogner |
|---|---|---|
| ouvrirFichier/fermerFichier | pk_open/pk_close | RAM Fichier, valeurPairRéseau/절대 chemin |
| lireDonnéesFichier/écrireDonnéesFichier | pk_read/pk_write | Fichier, fd 0/1/2 표준 sortieEntrée, 연결형 valeurPriseRéseau |
| positionnerFichier | pk_lseek | DébutDepuis/racineActuel/origineFin |
| tailleFichier/définirLongueurFichier | pk_size/pk_ftruncate | longueur valeurInterroger/changerValeur |
| supprimerNomEntréeÉlémentFichier | pk_unlink | Fichier nom 삭제 |
| stockageFichierConfirmer | pk_fsync | RAM이므로 -1, numéroErreur=ENOSYS |
| créerExtrémité/associerAdresse | pk_socket/pk_bind | AF_INET, SOCK_DGRAM 또는 SOCK_STREAM |
| envoyerDonnéesDatagramme/recevoirDonnéesDatagramme | pk_sendto/pk_recvfrom | UDP 루프백 |
| connecterRéseau | pk_connect | 연결형 루프백 |
| attendreConnexionRéseauPour | pk_listen | attendreValeur connecter valeurMaximal 4개 |
| accepterConnexionRéseau | pk_accept | élémentListeActuel adresse 인수는 NULL/NULL만 valeurPriseEnCharge |
| lireAdressePriseRéseau | pk_getsockname | 로컬 adresse/valeurPort |

`ABIRéseau.h`의 interne `pk_sockaddr_in`을 사용하며 valeurPort·주소는 `courtRéseau`/`entierRéseau`로 변환한다. C valeurPriseRéseau 호출은 비차단이며 Données/연결이 없으면 -1과 `numéroErreur=11`(EAGAIN)을 반환한다. 양수 sortieEntrée 결과가 요청보다 작을 nombre 있으므로 valeurItération 처리한다. valeurÉchec 후에만 오류번호를 확인한다.

[valeurFlux.c](Exemples/CodageHangul/valeurFlux.c)는 C에서 français 이름으로 connecter·accept·valeurSousPartie lire/écrire·큐 포화·EOF를 처리하는 exécuterCommande 예제다. SDK의 `examples/valeurFlux.c`를 같은 `compile.py`로 컴파일한다.

SDK는 **libposix-kor-user.a**를 링크한다. invoquer 흐름은 C/C++ → donnéesEffectif français C Fonction 또는 호환용 `pk_*` → `svc #0` → 커널의 소유권·pointeur Contrôles → Java RAM Fichier/루프백 또는 valeurExtérieur lwIP TCP/UDP 구현이다. `libposix-kor-arm64.a`는 valeurNoyau 내부용이므로 EL0 프로그램에 링크하지 않는다. Linux 헤더나 Linux ELF와 혼합하지 않는다. 동적 connecter, 표준 C printf, libstdc++/STL, exception·RTTI는 제공하지 않으며 C++의 valeurStatique 생성자·portéeLocal valeurObjet 소멸자는 지원한다. 상세 numéro·donnéesMémoire 범위는 [ABIAppelUtilisateur.md](ABIAppelUtilisateur.md)를 참고한다.

## valider

`make test-windows`, `make test-swing`, `make test-stream`, `make test-coding`으로 새 기능을 각각 시험한다. `make test`는 기존 interpréteurCommandes·VNC·JVM·AOT·valeurNoyau protégerValeur 시험까지 포함한다. donnéesEffectif CarteMatérielle 대신 QEMU raspi4b에서 수행한다. 결과는 [élémentListePrécédentÉlément GUI valeurExtension valider enregistrementJournal](build/verification/release.json)과 [élémentListeActuel EnvironnementExécution valider enregistrementJournal](build/verification/native-runtime-summary.json), [여러 terminal Écran](build/verification/windows/four-terminals.png), [Swing Écran](build/verification/swing/native-swing.png)을 참고한다.

réalisation 시 참고한 표준 API: [Socket](https://docs.oracle.com/javase/8/docs/api/java/net/Socket.html), [JFrame](https://docs.oracle.com/javase/8/docs/api/javax/swing/JFrame.html), [JButton](https://docs.oracle.com/javase/8/docs/api/javax/swing/JButton.html). 이 문서의 réalisation 범위가 valeurSommet 표준 전체를 지원한다는 뜻은 아니다.

## français 이름으로 직접 작성하는 창과 valeurFilExécution

`example/java/ExempleFenêtre.java`는 `TâcheTâcheExécutable.exécuterTâche`,
`RécepteurAction.recevoirAction(NotificationAction)`, `bouton`, `FileAttenteÉvènement.invoquerUltérieur`, `lancer()`을 쓴다.
interne JVM에 이 이름들의 valeurObjet·valeurMéthode·콜백을 직접 구현했으며 영어 Swing 객체를
보관하는 래퍼가 아니다. `tâcheFond`도 interne 스케줄러와 직접 연결된다.
세부 메서드와 기존 français API에서의 변경은 [français API Documentation](JavaFrançais/Guide.md)를 본다.

Hôte javac는 valeurDistribution JAR를 valeurClasse 경로로 사용한다.

```sh
javac --release 8 -encoding UTF-8 -cp dist/jkoros-native-korean.jar \
  -d build/한국어사용 ../../example/java/ExempleFenêtre.java
python3 Outils/exécuterCommande.py --desktop --network --resolution 1920x1080
```

게스트에는 빌드한 예제가 `/example/java`에 설치된다.

```text
cd /example/java
java ExempleFenêtre
```

직접 Écran/valeurFilExécution API와 `lancer()` 진입점은 interne JVM 전용이다.
전체 OpenJDK·Swing 재구현이나 일반 OpenJDK에서 같은 API의 실행을 보장하지 않는다.
기존 표준 `main(String[])` 프로그램은 traitementContinuer 실행할 nombre 있다.
