# jkoros 안에서 Java compilerSource·exécuterCommande

이 문서의 Amorçage·interpréteurCommandes·valeurStocker 명령은 **x86 valeurVersion** 기준이다. 공유 Java Compilateur/JVM은 [interne ARM64 Pi4 valeurVersion](../platforms/rpi4-native/README.md)에도 연결되어 있다. ARM64에서는 UTF-8 UART valeurEntrée·texteHangul texteNomFichier, `edit`의 단독 `.` valeurStocker, 16개 RAM Fichier, 약 2초 exécuterCommande 제한을 사용한다.

`javac FILE.java`와 `java CLASS [ARGS]`를 네이티브 jkoros 셸에서 실행한다. 컴파일러와 JVM은 각각 독립 ELF로 적재되어 ring 3에서 동작한다. 소스를 게스트에서 읽어 donnéesEffectif JVM `.class` 파일을 만들고, 그 파일의 바이트코드를 게스트 JVM이 해석한다. Hôte compilerSource 서버나 Linux 게스트는 사용하지 않는다.

**élémentListeActuel 구현은 interne 제한형 Compilateur·JVM이다. OpenJDK/JDK 전체를 이식하거나 설치한 것이 아니며 Java SE 호환 환경도 아니다.** 표준 라이브러리는 아래의 일부 호출을 구현한 것이다. `java -version`과 `javac -version`에도 이 범위를 표시한다. 일반 JAR, Maven/Gradle, 임의의 Java Programme 실행은 아직 지원하지 않는다.

## 바로 exécuterCommande

호스트에서:

```sh
cd /home/user/jkoros
make iso
make run
```

게스트에서:

```text
jkoros> javac -version
jkoros> java -version
jkoros> ls
jkoros> cat Hello.java
jkoros> javac Hello.java
Compiled: Hello.class (JVM class version 49)
Exit: 0
jkoros> java Hello
Hello from jkoros JVM!
55
Exit: 0
```

ISO는 `os/build/kernel.iso`opérandeTroisième. 기존 VirtualBox 실행기도 같은 ISO를 사용한다. exécuterCommande 중이거나 저장된 VM에는 새 ISO가 자동 반영되지 않는다. 새 Amorçage 절차는 [VirtualBox exécuterCommande Guide](LancerVirtualBox.md)를 따른다. 이 변경의 Java 자동 시험은 QEMU에서 수행했다.

## 직접 작성

`edit`는 Fichier 전체를 새 내용으로 작성한다. 기존 내용의 ligne valeurÉditer 기능은 아니다. `.save`로 저장하고 `.cancel`로 취소한다.

```text
jkoros> edit Demo.java
...> public class Demo {
...>  public static int square(int n) { return n * n; }
...>  public static void main(String[] args) {
...>   int n = Integer.parseInt(args[0]);
...>   System.out.println("square=" + square(n));
...>  }
...> }
...> .save
jkoros> javac Demo.java
jkoros> java Demo 12
square=144
Exit: 0
```

- `ls`: 파일과 valeurOctet nombre afficherValeur.
- `cat FILE`: Fichier valeurContenuValeur afficherValeur. 텍스트 소스에 사용한다.
- `rm FILE`: donnéesMémoire Fichier 삭제.
- `edit FILE`: 전체 내용을 새로 valeurEntrée. 빈 파일도 저장할 nombre 있다.
- 구문·valeurType Contrôles valeurÉchec 시 기존 `.class`는 유지된다. 소스를 고친 valeurRetourArrièreCôté 컴파일이 실패했다면 élémentListePrécédentÉlément exécuterCommande 파일이 남아 있으므로 compilerSource valeurSuccès 여부를 확인한다.

파일은 RAM에서 동작한다. 전용 valeurStocker 매체가 없거나 `sync`하지 않은 내용은 재부팅하면 사라진다. `make -C os run-store`로 연결한 매체에는 `sync`로 arbreSource·valeurClasse·Données 파일을 보존할 nombre 있다. valeurMaximal 8개, 파일마다 16KiB, Fichier 이름은 ASCII 1~63자다. arbreSource 이름은 `.class` 확장자 régionAdresse 때문에 valeurMaximal 62자다. valeurÉditer 입력은 ASCII이고 한 ligne valeurMaximal 128자다. ligne 또는 Fichier 한도를 넘긴 편집은 `.save`에서 거부하여 기존 파일을 보존한다. valeurNoyau/Compilateur/JVM 구현의 Java 식별자는 한국어이며, élémentListeActuel 게스트 valeurEntrée valeurLimite 때문에 Utilisateur Exemples 이름은 ASCII로 작성한다.

## valeurExtérieur Fichier 적재

호스트에서 만든 소스나 valeurPriseEnCharge rogner 안의 `.class`를 Amorçage 이미지에 포함할 nombre 있다. `JAVA_FILES`는 `게스트이름=호스트경로` 목록이다. 아래의 경로는 예시이며 donnéesEffectif 파일의 절대 경로로 바꾼다. 공백 없는 경로를 사용한다.

```sh
# Hôte JDK로 컴파일한 클래스도 사용할 nombre 있다.
javac --release 8 /tmp/Demo.java
make -C /home/user/jkoros iso \
  JAVA_FILES='Demo.java=/tmp/Demo.java Demo.class=/tmp/Demo.class'
make -C /home/user/jkoros run \
  JAVA_FILES='Demo.java=/tmp/Demo.java Demo.class=/tmp/Demo.class'
```

새 Amorçage étatValeurAprès `java Demo 12`를 실행한다. 소스만 넣었으면 게스트에서 `javac Demo.java`부터 실행한다. `JAVA_FILES`를 생략한 élémentListeSuivant 빌드에서는 ajouterFinEntréeÉlément 파일을 포함하지 않는다. Fichier valeurContenuValeur 변경과 listeEntréeÉlément 제거도 élémentListeSuivant 빌드에 반영된다. original Hôte 파일에는 쓰지 않는다. valeurDéfaut `Hello.java`jusquÀ 합해 8개이며, 같은 이름을 명시하면 valeurDéfaut 예제를 대체한다. 새 `.class`를 저장할 빈 슬롯도 남겨 둔다.

`--release 8`은 valeurClasse Fichier 버전을 맞추는 옵션이다. 사용하는 문법·codeOctets·라이브러리도 valeurBasExtrémité valeurPriseEnCharge rogner 안에 있어야 한다.

## valeurPriseEnCharge rogner

| 기능 | 게스트 javac | 게스트 JVM |
| --- | --- | --- |
| valeurClasse | 패키지 없는 단일 valeurClasse, valeurStatique Fonction, 재귀, arguments/résultatRetourner | 실행마다 단일 valeurClasse 적재, public static main(String[]) |
| valeurDéfaut valeur | int, boolean, char, String, main의 String[] arguments | Entier·référence pileOpérande, String, int[], String[], 내부 StringBuilder |
| valeurInstruction | valeurInitialValeur 있는 portéeLocal Déclarations, valeurAffectation, `+=`, `-=`, `*=`, `/=`, `%=`, 후위 ++/--, 블록, if/else, while, for, return | 해당 Entier·référence 바이트코드와 condition branche |
| valeurExpression | 십진 Entier, UTF-8 소스의 Chaîne/Caractères, + - * / %, 비교, ==/!=, !/&&/\|\|, Chaîne valeursCombiner | Entier valeurOpération·valeurBit valeurOpération·valeurType convertirValeur, 단락 평가, valeurTableau entréeÉlémentAccès |
| Fichier | FileInputStream(String), FileOutputStream(String[, boolean]), read()/write(int)/close() | donnéesEffectif valeurNoyau 파일서술자와 connecter, générer·effacerContenuContenu·ajouterFinContinuation·EOF |
| Sortie | System.out.print/println: int/boolean/char/String, println() | 동일 |
| Chaîne/arguments | String.length(), args.length, args[index], Integer.parseInt | 추가로 String.charAt(), Chaîne 상수의 modified UTF-8 해독 |

선언은 지원하는 문법만 허용한다. 여러 변수를 한 선언에 나열하기, valeurInitialValeur 없는 portéeLocal Déclarations, 오버로드, 임의 valeurType convertirValeur, valeurTableau générer source, 8/16진 리터럴, Unicode arbreSource 이스케이프 등은 미지원이다. `char`는 Caractères 리터럴로 초기화하며 일반 JDK의 모든 valeurConstante 축소 변환을 구현하지 않는다. valeurExtérieur `.class`의 `int[]` générer/lire/쓰기는 지원하므로 Hôte `javac --release 8`로 만든 valeurTableau 예제는 실행할 nombre 있다.

valeurObjet valeurChamp·일반 valeurObjet générer·상속·인터페이스·여러 valeurClasse connecter, long/float/double, exception entréeÉlémentValeurProcessus, 스레드·모니터, 리플렉션, JNI, JIT, GC, valeurSommet 표에 없는 `java.io`와 `java.nio`/`java.net` 일반 API, 컬렉션, JAR와 클래스패스는 미지원이다. 런타임 오류는 Java exception 객체를 던지지 않고 valeurDiagnostic étatValeurAprès élémentListeActuel 프로그램을 종료한다. 객체와 Chaîne valeurStocker 공간은 exécuterCommande programmeQuitter 시 Utilisateur valeurRégion 전체와 함께 회수한다. 지속 exécuterCommande 중 GC는 없다.

## exécuterCommande 한도와 erreur

| valeurRessource | limiteCapacité |
| --- | --- |
| arbreSource/valeurClasse Fichier | 각각 16KiB |
| Compilateur | valeurJeton 2,047개, générer valeurCode 4KiB, valeurConstante 풀 4KiB |
| Fonction/arguments | 클래스당 32함수, 함수당 16인수 |
| JVM valeurConstante | 511개 |
| JVM Fonction valeurCode | 함수당 8KiB |
| JVM invoquer/pileOpérande/portéeLocal valeurVariable | 32프레임, 프레임당 pileOpérande 128칸·portéeLocal 128칸 |
| JVM valeurObjet valeurStocker régionAdresse | 8,192개 32비트 entréeÉlémentEmplacement, 헤더 Entêtes 약 32KiB |
| exécuterCommande | valeurMaximal 500,000 commande, 기존 커널의 약 3초 CPU exécuterCommande 상한도 적용 |

게스트 컴파일러는 버전 49.0 `.class`를 생성하며 JVM은 45.0~52.0 중 valeurPriseEnCharge 명령으로 구성된 파일을 읽는다. 스택맵을 이용한 완전한 JVM Dictionnaire 검증기를 구현한 것은 아니다. Fichier/valeurAttribut longueur, valeurConstante référence, commande·branche 경계를 검사하고, exécuterCommande 중 pileOpérande valeurFormat·portéeLocal initialiser·valeurTableau valeurIndiceTableau·valeurObjet 참조를 검사한다. Utilisateur 코드의 페이지·portMatériel 접근은 기존 ring 3 경계로 보호한다.

일반 성공은 `Exit: 0`, compilerSource·JVM 오류는 `Exit: 1`, commande arguments 오류는 `Exit: 2`opérandeTroisième. CPU valeurTemps 상한은 기존 `Exit: 124`이며, Utilisateur ELF 자체의 CPU/런타임 오류는 기존 programmeQuitter 코드를 따른다. valeurÉchec étatValeurAprès 셸에서 다른 프로그램을 traitementContinuer 실행할 nombre 있다.

## réalisation 위치와 Tests

- `os/Utilisateur/Java/CompilateurJava.java`: 게스트 어휘·구문·valeurType Contrôles, valeurConstante 풀 및 codeOctets générer.
- `os/Utilisateur/Java/MachineVirtuelleJava.java`: valeurClasse 적재, pileOpérande·프레임·valeurObjet valeurStocker, commande 해석과 제한된 표준 invoquer.
- `os/source/SystèmeFichiersMémoire.java`: donnéesMémoire SystèmeFichier, valeurÉditer, Amorçage Fichier 적재.
- `os/source/AppelSystème.java`, `compiler/démarrerProgrammeUtilisateur.s`: Fichier/Caractères Sortie API와 Utilisateur pointeur Contrôles.
- `os/Outils/EmballerFichiersJava.py`: Hôte valeurEntrée Fichier valider·Amorçage valeurGroupe générer.

```sh
make test-java
make test
```

`os/Tests/TestJava.py`는 ELF/ISO Amorçage, 게스트 compilerSource·exécuterCommande, Utilisateur valeurEntrée, 재귀·반복문·Entier 극값·Chaîne valeursCombiner·단락 평가, 재실행, arbreSource erreur étatValeurAprès 기존 valeurClasse 보존, valeurTableau/nombre 해독 erreur, 무한 valeurItération valeurLimite, valeurÉditer 넘침과 Fichier 부족을 검사한다. 게스트 générer 클래스의 바이트를 QEMU 메모리에서 꺼내 OpenJDK `java -Xverify:all`로 실행하고 결과를 대조한다. 반대 방향으로 Hôte OpenJDK의 valeurClasse, Entier 배열과 texteHangul 상수를 게스트에 적재하며, 손상된 Fichier valeurMarqueur·버전·valeurConstante nombre·branche·스택을 거부하는지도 검사한다. 기록은 `os/build/TestJava.json`에 남는다. 디스크 없는 별도 Tests VM만 생성하고 종료한다.

réalisation 형식의 참고 Données: Oracle [JVM valeurClasse Fichier spécification](https://docs.oracle.com/javase/specs/jvms/se8/html/jvms-4.html), [JVM commande spécification](https://docs.oracle.com/javase/specs/jvms/se8/html/jvms-6.html).

## Java Fichier sortieEntrée

[FileDemo.java](../posix-kor/ExempleJava/FileDemo.java)는 일반 Java 표준 valeurClasse 이름을 사용한다. 소스를 `edit FileDemo.java`로 입력하거나 `JAVA_FILES`로 Amorçage 이미지에 넣은 valeurRetourArrièreCôté `javac FileDemo.java`, `java FileDemo`를 실행한다. 결과는 `65`, `255`, `66`, `-1`, `JAVA FILE IO PASS`opérandeTroisième. `write(int)`는 하위 8비트를 쓰고 `read()`는 0~255 또는 EOF -1을 반환한다. valeurDéfaut Sortie 생성자는 내용을 비우고, boolean 인수가 true이면 이어쓴다.

두 스트림과 IOException의 명시적 import, main의 `throws Exception` 또는 `throws IOException` 표기를 허용한다. exception valeurObjet·try/catch·try-with-resources는 지원하지 않으며 Fichier 오류를 진단하고 프로그램을 종료한다. valeurTableau sortieEntrée, InputStream/OutputStream으로의 다형성, Reader/Writer, getFD, 일반 Fichier 메타데이터 API는 아직 없다. close는 열린 서술자를 닫고, 재부팅 보존에는 interpréteurCommandes `sync`opérandePremier 필요하다. 예제의 Fichier 이름은 élémentListeActuel 셸과 파일체계에 맞춰 ASCII로 쓴다.

`os/Tests/TestFichierJava.py`는 donnéesEffectif 게스트 compilerSource 결과를 OpenJDK `-Xverify:all`로 valeurRéessayer 실행해 Fichier 바이트와 출력을 대조한다. 범위와 valeurStocker valeurSupports 사용법은 [posix-kor Guide](../posix-kor/Guide.md)를 참고한다. 참고한 표준 API는 Oracle [FileOutputStream](https://docs.oracle.com/javase/8/docs/api/java/io/FileOutputStream.html)이다.
