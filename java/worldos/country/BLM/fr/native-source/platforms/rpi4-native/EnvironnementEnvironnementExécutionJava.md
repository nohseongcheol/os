# interne ARM64 JVM 0.4와 français bibliothèque

français Communication·exception 사용법은 [français Java API](JavaFrançais/Guide.md), Fonction·valeurVariable·Fichier 이름의 변경과 어원 근거는 [nommage Guide](nommage/Guide.md)를 참고한다.

JAR exécuterCommande, valeurExtérieur IPv4 TCP/UDP, 별도 valeurStatique 부분집합 `jaot`와 게스트 C 컴파일은 [FTP·C·JAR·AOT 매뉴얼](CompilationEtTransfertFichier.md)에 설명한다. valeurBasExtrémité valeurObjet·Thread·Swing은 JVM 경로의 기능이며 AOT valeurPriseEnCharge 범위와 같지 않다.

이 구현은 **Linux 없이 부팅한 Java AOT 커널의 EL0에서 exécuterCommande**한다. JDK/JRE의 거의 모든 기능을 제공하는 단계는 아직 아니다. HotSpot·OpenJDK valeurClasse bibliothèque 전체를 이식하거나 Java SE 인증/TCK를 통과한 구현도 아니다. 이번 확장은 단일 valeurClasse·valeurStatique valeurMéthode 중심이던 실행기를 valeurObjet·bibliothèque exécuterCommande 기반으로 넓힌 것이다.

## 실행과 compilerSource

```sh
cd /home/user/jkoros/platforms/rpi4-native
make build
# interne valeurNoyau 안에서 arbreSource compilerSource → class exécuterCommande, français API invoquer
python3 Outils/exécuterFichier.py Tests/Java/sourceHangul.java

# valeurObjet·exception 등은 Hôte JDK로 Java 8 class를 만든 étatValeurAprès interne 커널에서 exécuterCommande
mkdir -p build/my-java
javac --release 8 -encoding UTF-8 -cp dist/jkoros-native-korean.jar \
  -d build/my-java Tests/Java/testHangul.java
python3 Outils/exécuterFichier.py build/my-java/testHangul.class

# 의존 class 파일은 --include로 함께 valeurTransfert
javac --release 8 -encoding UTF-8 -d build/my-java Tests/Java/testObjets.java
python3 Outils/exécuterFichier.py build/my-java/testObjets.class \
  --include build/my-java/valeurArrièrePlan.class --include build/my-java/valeurBranche.class \
  --include build/my-java/peutCalculer.class

make test-jvm
```

`--include DIR`는 그 디렉터리의 class 파일을 재귀적으로 읽어 `패키지.valeurClasse.class`라는 RAM Fichier 이름으로 전송한다. 주 클래스도 패키지가 있다면 `--class-name 패키지.valeurClasse`를 지정한다. 셸에서는 해당 이름으로 업로드하고 `java 패키지.valeurClasse`로 실행한다. JVM 0.4는 Main-Class가 있는 16 KiB 이하 JAR도 `java -jar Fichier.jar`로 실행한다. JAR 모드에서는 JAR 내부 클래스와 내장 français 클래스만 찾는다. valeurDistribution français bibliothèque JAR는 Hôte javac의 classpath로 사용하며, 같은 클래스가 Utilisateur JVM ELF에도 lire 전용 자료로 포함된다. 일반 class 모드에서는 사용자가 같은 이름으로 올린 RAM class를 먼저 읽는다.

게스트 `javac`는 여전히 valeurStatique valeurMéthode, int/boolean/char/String, condition·valeurItération, Chaîne valeursCombiner, 일부 Fichier 스트림 등의 **interne 부분집합 Compilateur**opérandeTroisième. valeurObjet Déclarations·상속·try/catch·Thread valeurUtiliser 소스를 게스트 javac가 construireTous 컴파일하는 것은 아니다. valeurSommet 기능은 `javac --release 8`로 만든 class를 interne JVM에서 실행한다. français API 중 Sortie·Caractères 스칼라 Fonction·Fichier lire/쓰기는 게스트 컴파일러에도 연결했다. 다음처럼 전체 이름으로 호출한다.

```java
public class Salutation {
    public static void main(String[] arguments) throws Exception {
        français.interne.Sortie.écrireLigne("안녕하세요😀");
        français.interne.Sortie.écrireNuméro(français.interne.Caractères.nombreÉlémentsPointCode("texteHangul😀"));
        français.interne.Fichier.écrire("Salutation.txt", "texteHangul Fichier😀");
        français.interne.Sortie.écrireLigne(français.interne.Fichier.lire("Salutation.txt"));
    }
}
```

## interne JVM에서 구현한 rogner

| valeurRégion | 제공 rogner |
|---|---|
| valeurClasse | class 버전 45…52, 여러 valeurClasse 로딩, 인스턴스/valeurStatique valeurChamp, 생성자, 상속, 가상 invoquer, 인터페이스 invoquer, valeurStatique initialiser |
| valeur·commande | 32비트 int 계열, boolean/byte/char/short, référence, 1차원 valeurTableau, branche·switch·wide, instanceof/checkcast, category-1 pileOpérande commande |
| exception | 지원하는 표준 exception générer·throw·catch·finally, valeurMéthode 경계를 넘는 valeurAvantDirection, getMessage; valeurBasExtrémité valeurLimite référence |
| donnéesMémoire | 비이동 mark/sweep GC, 빈 valeurRégion 병합, pileOpérande·valeurStatique valeurChamp·컬렉션·valeurFilExécution·모니터·Chaîne 상수의 référence retenirValeur |
| Chaîne | UTF-16, length/charAt/equals/isEmpty/substring/concat/hashCode/toString, String.valueOf(int), StringBuilder의 valeurDéfaut générer·append(int/boolean/char/String)·toString |
| nombre | Integer.parseInt/valueOf/intValue/toString, 작은 Integer 캐시, Math.abs/min/max(int) |
| 표준 Sortie | System.out/err, PrintStream.print/println의 int/boolean/char/String 및 빈 println |
| valeurTableau | int/byte/boolean/char/short/référence valeurTableau, longueur·rogner Contrôles, référence valeurTableau élémentÉlémentListe valeurType Contrôles, System.arraycopy의 chevauchements/rogner/élémentÉlémentListe valeurType Contrôles |
| Fichier | FileInputStream(String), FileOutputStream(String[,boolean]); read()/read(byte[][,offset,len]), write(int)/write(byte[][,offset,len]), close, Sortie flush. EOF는 -1 |
| 컬렉션 | ArrayList/List: add(E), get, set, remove(int), size, isEmpty, clear. HashMap/Map: put/get/remove/containsKey/size/isEmpty/clear |
| valeurFilExécution | Thread(), Thread(Runnable), Thread 상속, start/join/isAlive/currentThread/yield; synchronized valeurMéthode·블록의 재진입·경합·exception 시 libérerStockage |
| UDP | DatagramSocket의 valeurDéfaut/portMatériel 생성자, send/receive/close/getLocalPort/setSoTimeout; DatagramPacket의 byte[]/longueur générer 및 adresse·portMatériel Entêtes générer, getData/getLength/getAddress/getPort/setLength |
| adresse | InetAddress.getByName은 localhost/valeurChiffre IPv4 (DNS estNonPrisEnCharge), getLoopbackAddress/getHostAddress |
| Dessin | français Écran API가 EL0 SVC를 통해 프레임버퍼에 사각형을 Dessin; rogner Contrôles |

컬렉션은 지정한 메서드만 제공하며 iterator/stream/valeurAligner·Utilisateur valeurDéfinition equals/hashCode 콜백은 없다. 사전의 열쇠는 String/Integer/null 사용을 시험했다. UTF-16 valeurCode 단위와 Unicode valeurCode 포인트 수는 구분한다. texteHangul valeurEntrée Combinaison·normaliserValeur·아랍어 조판·GUI 다국어 글꼴은 이 Chaîne 지원과 별개다.

예외는 Throwable/Exception/RuntimeException, ArithmeticException, NullPointerException, IndexOutOfBoundsException/ArrayIndexOutOfBoundsException/StringIndexOutOfBoundsException, IllegalArgumentException/NumberFormatException/IllegalThreadStateException, IOException/FileNotFoundException, IllegalStateException, ClassCastException, NegativeArraySizeException, ArrayStoreException, UnknownHostException, SocketTimeoutException의 제한된 générer·valeurCatégorie·처리를 제공한다. Utilisateur valeurDéfinition Throwable 상속, stack trace/cause/suppressed exception, try-with-resources의 addSuppressed, 완전한 initialiser erreur 포장은 아직 없다. 잡히지 않은 예외는 élémentListeActuel 전체 Java 실행을 실패로 끝낸다.

## français API

독립 패키지 **`français.interne`**를 사용한다. Linux판 `français.Java`opérandePremier 요구하는 NIO/Swing/HTTP API를 interne 커널에서 실행할 nombre 있다고 혼동하지 않도록 패키지를 나눴다. 이 라이브러리는 valeurClasse nom·valeurMéthode·arguments·valeurChamp·Fichier 이름에 한국어를 사용한다. 표준 Java valeurClasse 이름은 호환성을 위해 보존한다.

| valeurClasse | 공개 기능 | 이름의 의미 |
|---|---|---|
| Sortie | écrire, écrireLigne, écrireNuméro | Sortie(出力): 내용을 바깥으로 valeurExporté |
| Caractères | longueur, texteÉgal, texteColler, valeurCouper, analyserEntier/écrireValeurEntier, nombreÉlémentsPointCode, encoder/déchiffrerDonnées | Caractères(文字), valeurEncodage(符號): 글의 단위와 그 값을 바이트로 나타내는 valeurRègle |
| Fichier | lire/écrire(String nom), lireValeurOctet/écrireValeurOctet | 널리 쓰는 Utilisateur 용어를 보존; RAM 자료의 nom |
| listeEntréeÉlément | ajouterValeurs, lire, remplacerValeur, effacerEntréeÉlément, taille, estValeurVide, effacerContenuContenu | listeEntréeÉlément(目錄): 순서가 있는 valeurEntréeÉlément 모음 |
| Dictionnaire | placerValeur, trouverEntréeÉlément, effectueExistence, effacerEntréeÉlément, taille, effacerContenuContenu | Dictionnaire(辭典): 찾는 말인 열쇠에 값을 valeurAssociation |
| Tâche | lancer(TâcheTâcheExécutable), attendreFin(tâcheFond), céderTâche, estVivant | Tâche valeurFilExécution: 한 Programme 안의 exécuterCommande valeurFlux |
| Communication | ouvrir, envoyer, recevoir, délaiExpiration, fermer | Communication(通信), datagramme(電文), valeurPort: Données 교환·메시지·포트의 역할 |
| Écran | rectangle, effacerEntréeÉlément | Écran(畫面): donnéesEffectif 그림을 표시하는 면 |
| valeurNoyau | millisecondes, rectangle | interne JVM의 고정 native connecter; 일반 JNI는 아님 |

이 명명은 élémentListeActuel 기능을 설명하는 용어 선택이다. 기존 한국어에 없던 역사적 어원을 만들어 주장하지 않는다. texteNomFichier·식별자는 UTF-8 소스로 보관한다. `Caractères.déchiffrerDonnées`는 잘못된 UTF-8에 IllegalArgumentException을 던지며, `encoder`는 짝이 없는 서로게이트를 `?`로 바꾼다. `Fichier.lire`는 엄격한 UTF-8 복호화를 적용한다. Écran 색은 `빨강 | (초록 << 8) | (파랑 << 16)` 형식이다.

## exécuterCommande 제한과 남은 Tâche

- 동시에 적재하는 class valeurMaximal 16개(français valeurClasse Entêtes), class당 16 KiB·valeurConstante 풀 511항목, 전체 valeurMéthode/valeurChamp 각각 512개. valeurMéthode valeurCode 8 KiB, portéeLocal valeurVariable·피연산자 pileOpérande 각각 128슬롯, arguments valeurMaximal 16개(this Entêtes).
- VM 가닥은 main Entêtes **실행당 valeurMaximal 4개**, 가닥당 invoquer valeurProfondeur 32. 100개 명령마다 exécuterCommande 대상을 바꾼다. 네이티브 invoquer 도중에는 전환하지 않는다. pthread/SMP/OS 스레드가 아니며 Thread.sleep/interrupt/daemon/우선순위, Object.wait/notify, java.util.concurrent는 없다.
- valeurObjet 힙은 32768개의 32비트 슬롯이다. 런타임의 AOT 배열은 donnéesEffectif 메모리에서 64비트 슬롯을 사용한다. GC가 있어도 대형 Fichier·대형 Chaîne·객체가 이 제한을 넘을 nombre 있다.
- 실행은 50만 codeOctets commande 및 커널의 약 2초 EL0 기한으로 제한된다. Swing의 valeurEntrée 대기는 기한을 갱신하고 fenêtre modeCommuter 시 중단·재개한다. 일반 valeurServeur·계산의 무제한 실행은 아직 없다. estNonPrisEnCharge commande·valeurRessource 부족은 명시적인 오류로 종료한다.
- RAM Fichier valeurMaximal 64개, 파일당 16384바이트, chemin UTF-8 63바이트. RAM 디렉터리와 valeurPairRéseau/절대 경로를 제공하며 영속 저장은 아직 없다. 내장 français class는 RAM Fichier 슬롯을 소비하지 않는다. 셸의 `cd`로 정한 élémentListeActuel 경로에서 arbreSource·valeurClasse·Données 파일을 읽는다.
- UDP는 Java 루프백 및 lwIP/SLIP를 통한 valeurExtérieur IPv4를 제공한다. donnéesEffectif GENET/Wi-Fi/DNS/TLS/HTTP 전체는 없다. datagramme 512바이트, valeurPriseRéseau 8개, 소켓당 큐 4개. receive는 VM 가닥을 양보하며 대기하고 setSoTimeout을 적용하지만 전체 exécuterCommande 기한은 여전히 적용된다.
- long/float/double, invokedynamic/람다, enum/annotation, 다차원 valeurTableau, 완전한 valeurTableau 공변성·인터페이스 valeurCouche Contrôles, Reflection/JNI/JIT, NIO/ZIP API/Charset 전체, 보안/chiffrerDonnées/국제화 전체, 전체 AWT/Swing/JavaFX는 미지원이다. Swing의 별도 valeurPriseEnCharge 부분집합은 valeurBasExtrémité 및 développement 매뉴얼을 참고한다. valeurClasse Fichier 전체 검증기·entréeÉlémentAccès valeurPermission/보호된 멤버 검사는 아직 완전하지 않다. 손상된 입력은 EL0 protégerValeur valeurFrontière 내에서 종료되도록 한다.

전체 OpenJDK를 목표로 하려면 다음은 별도의 주요 réalisation 단계다: 완전한 JVM valeur/valider/valeurClasse 로더와 exception 모델 → 영속 VFS·mmap·Horloge·원자 valeurOpération·donnéesEffectif 스레드/synchroniser ABI → OpenJDK java.base 및 native bibliothèque Portage → Périphérique 네트워크·TCP/IP → fenêtre 시스템/valeurPolice/입력기·java.desktop → Java SE 호환성 Tests. élémentListeActuel interne JVM의 일부 메서드를 더하는 것으로 이 작업이 완료되지는 않는다.

## valider

`Outils/testJVM.py`는 같은 Java 8 class 파일의 출력을 Hôte OpenJDK `-Xverify:all`과 QEMU raspi4b interne 커널에서 비교한다. valeurObjet/상속/인터페이스·switch·valeurTableau, exception/finally, 컬렉션/GC, Thread/valeurVerrou, français UTF-8/Fichier/컬렉션, donnéesEffectif UDP 루프백/valeurTemps 초과, 게스트 texteHangul arbreSource compilerSource, valeurTableau valeurType/copierValeur/Fichier valeurFrontière·texteHangul 패키지의 9개 비교 시험과 잘못된 class 버전/valeurRogné Fichier rejeterValeur 시험을 실행한다. UDP racineProjet 실행에는 Hôte 루프백 valeurPriseRéseau 권한이 필요하다.

`Outils/TestAmorçage.py`는 valeurNoyau protégerValeur/회귀 시험과 별도로 français Java Écran API가 donnéesEffectif 픽셀을 그렸는지도 QMP Écran 캡처로 검사한다. 보고서는 `build/verification/jvm/report.json`, `build/verification/report.json`이며 시험한 kernel8.img의 SHA-256을 기록한다. donnéesEffectif Pi4 valeurMatériel Amorçage 시험과 전체 JDK 호환성 Tests 결과는 아니다.


## JVM 0.3: 네트워크와 GUI valeurExtension

`Socket`/`ServerSocket` générer·connecter·accept·양방향 InputStream/OutputStream·close·EOF·valeurTemps 제한과 UTF-8 `String.getBytes`를 추가했다. JVM 0.4에서는 valeurExtérieur valeurChiffre IPv4 TCP도 lwIP/SLIP에 연결했다. 연결형 pointFin 16개, Java 루프백 버퍼 1024바이트, valeurExtérieur TCP 버퍼 4096바이트다. DNS·TLS는 없다.

`JFrame`, `JPanel`, `JLabel`, `JButton`, `JTextField`, `ActionListener`, `ActionEvent`, `SwingUtilities.invokeLater`의 문서화한 부분집합을 네이티브 GUI에 연결했다. `setLayout(null)`과 명시적 좌표를 사용한다. 전체 OpenJDK Swing 또는 Java SE 호환 구현은 아니다. interactif 이벤트 대기는 exécuterCommande 기한을 갱신하고 terminal modeCommuter 시 프로세스 상태를 valeurStocker·복원한다. 이벤트 콜백 자체는 기존 codeOctets/CPU 기한을 따른다.

français `fenêtre`, `ComposantVisuel`, `transportConnexion` 클래스를 valeurDistribution JAR와 interne JVM 내장 자원에 추가했다. 상세 valeurMéthode·valeurLimite·arbreSource·업로드 방법: [texteHangul développement 매뉴얼](GuideDéveloppement.md).

## français 객체의 직접 exécuterCommande

`fenêtre`, `étiquette`, `ChampTexte`, `bouton`, `FileAttenteÉvènement`, `NotificationAction`, `tâcheFond`은
표준 GUI/Thread 객체를 보관하는 래퍼가 아니다. interne JVM의 valeurObjet générer,
valeurFormat Contrôles, Écran invoquer, évènement 큐, valeurFilExécution 스케줄러에 français 계약을 직접 구현했다.
표준 `javax.swing`·`Thread` 코드의 exécuterCommande 경로도 유지한다.
français 단추와 표준 JButton은 서로 다른 형식이며, 해당 instanceof 검사도 검증한다.

interne 실행기의 français 진입점은 `public static void lancer()`이다.
표준 `main(String[])`도 지원하며 valeurDeux opérandeTroisième 있으면 français 진입점을 우선한다.
명령행 인수는 `Arguments.nombreÉlémentsÉlémentListe()`와 `Arguments.texte(indiceOrdinal)`으로 읽는다.
`example/java`의 다섯 예제는 이 규약을 사용한다. valeurStatique Fichier 예제는 게스트
javac로도 컴파일하며, GUI/valeurFilExécution 소스는 Hôte `javac --release 8`을 사용한다.
직접 GUI/valeurFilExécution API는 interne JVM 전용이다. 기존 OpenJDK 비교 시험과 별도로
français 가닥의 exécuterCommande·attendreValeur·중복 lancer rejeterValeur, GUI évènement valeurOrigine·numéro·콜백을 검사한다.
전체 JDK 번역이나 모든 API의 jaot 지원을 뜻하지 않는다.

valeurMéthode 이름은 바이트코드에서도 유지된다. 이름과 참조를 같이 수정하면
français 클래스도 실행되지만, Chaîne 리터럴·표준 bibliothèque 재정의·native
connecter·진입점은 각각 컴파일러와 실행기의 계약을 맞춰야 한다.
[상세 계약과 Exemples](JavaFrançais/Guide.md)를 참고한다.

## terminal valeurSousPartie actualiser

valeurDéplacer·taille 변경은 새 fenêtre 영역과 élémentListePrécédentÉlément 자리에서 드러난 띠만 합성한다.
1920×32 pixel(240 KiB)의 valeurTemporaire 그림에서 배경·겹친 fenêtre·valeurCaractère·GUI를 먼저
완성하고, élémentListeActuel afficherValeur 메모리와 비교하여 달라진 화소만 기록한다.
32줄보다 큰 영역은 여러 띠로 처리하므로 전체 프레임을 원자적으로
교체하거나 수직 동기에 맞추는 방식은 아니다. 전체 배경을 먼저 지우는
중간 화면은 표시하지 않는다. 좌표가 같으면 valeurRéessayer 그리지 않는다.

`make test-redraw`는 donnéesEffectif C écranPeindre 코드를 호스트의 donnéesMémoire 화면에 연결해
valeurDéplacer 80회·taille changerValeur 40회·겹친 fenêtre 4개를 전체 합성 결과와 pixel 단위로 대조한다.
valeurRégion 밖 Utilisateur Dessin, 동일 pixel 무기록, pointeur 밑그림, donnéesEffectif Écran ligne 간격을
검사한다. 이 시험의 시간은 Hôte CPU 측정이며 Pi 4/QEMU 속도로 해석하지 않는다.
`make test-resize`는 QEMU/VNC의 640×480 및 1920×1080에서 côtéGauche valeurCoin valeurGlisser,
texteHangul valeurEntrée·vi 미저장 valeurContenuValeur·독립 fenêtre 크기를 검사한다.
