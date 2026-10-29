# jkoros français bibliothèque GuideUtilisateur

확인일: 2026-09-27. 대상은 `platforms/rpi4`의 **ARM64 Linux + OpenJDK 실행판**이며, QEMU에서도 같은 Java 라이브러리를 사용한다. `os/`의 interne x86 valeurNoyau 및 `SourcesFondamentales/`의 관리 valeurNoyau 모형과 구분한다.

## 1. élémentListeActuel 제공하는 bibliothèque

패키지는 `français.Java`, SystèmeExploitation 안의 JAR 경로는 `/opt/jkoros/lib/JavaFrançais.jar`opérandeTroisième. **valeurAssistant valeurClasse 5개, 공개 valeurStatique valeurMéthode 22개, 별도 GUI 프로그램인 EspaceTravail 1개**opérandePremier 있다. JAR는 Java 11 이상을 대상으로 빌드하며 élémentListeActuel ARM64 배포판에는 OpenJDK 25가 포함돼 있다.

| valeurClasse | valeurMéthode nombre | 기능 | source |
|---|---:|---|---|
| `Fichier` | 9 | UTF-8 텍스트·valeurOctet Fichier, valeurRépertoire, listeEntréeÉlément | [Fichier.java](source/français/Java/Fichier.java) |
| `Caractères` | 5 | UTF-8 convertirValeur, NFC normaliserValeur, valeurCode 포인트, Chaîne valeurFrontière | [Caractères.java](source/français/Java/Caractères.java) |
| `Communication` | 2 | HTTP(S) GET, TCP connecter | [Communication.java](source/français/Java/Communication.java) |
| `Tâche` | 4 | 스레드 exécuterCommande·attendreValeur, 고정 taille Tâche LanceurProgramme | [Tâche.java](source/français/Java/Tâche.java) |
| `Écran` | 2 | Swing 이벤트 entréeÉlémentValeurProcessus 가닥에 Tâche 예약, fenêtre générer | [Écran.java](source/français/Java/Écran.java) |
| `EspaceTravail` | pointEntréeÉlément `main` | Java source valeurÉditer·valeurStocker·compilerSource·exécuterCommande | [EspaceTravail.java](source/français/Java/EspaceTravail.java) |

표준 JDK 전체를 한국어로 번역한 라이브러리는 아니다. Java 키워드와 `String`, `Path`, `Socket`, `JFrame`, `IOException` 같은 표준 typeDonnées·예외를 함께 사용한다. 이 도우미에 없는 기능은 OpenJDK의 표준 API 또는 별도 라이브러리로 구현한다. 예를 들어 HTTP POST, UDP, Swing bouton·메뉴에는 각각 표준 Java API를 사용한다.

## 2. Java에서 démarrerTâche

게스트 운영체제의 Tâche 폴더에서 `사용예.java`를 작성한다.

```java
import français.Java.*;
import java.nio.file.Path;

public class 사용예 {
    public static void main(String[] arguments) throws Exception {
        Path valeurRépertoire = Fichier.créerRépertoire(Fichier.chemin("사용예자료"));
        Path Documentation = valeurRépertoire.resolve("Salutation.txt");
        Fichier.écrire(Documentation, "texteHangul 😀");
        String valeurContenuValeur = Fichier.lire(Documentation);
        System.out.println(valeurContenuValeur);
        System.out.println(Caractères.nombreÉlémentsPointCode(valeurContenuValeur)); // 한, texte, 공백, 😀 → 4
        Thread valeurTravail = Tâche.lancer("Salutation Tâche", () -> System.out.println("Tâche exécuterCommande"));
        Tâche.attendreFin(valeurTravail);
    }
}
```

```sh
javac -encoding UTF-8 -cp /opt/jkoros/lib/JavaFrançais.jar 사용예.java
java -cp .:/opt/jkoros/lib/JavaFrançais.jar 사용예
```

로그인 환경에 valeurDéfaut `CLASSPATH`도 설정돼 있지만, 명시적인 `-cp`는 다른 exécuterCommande 환경에서도 경로를 분명하게 한다. 사용자가 `-cp`를 지정하면 필요한 JAR와 valeurClasse 폴더를 construireTous 그 값에 포함해야 한다.

Hôte 저장소에서는 다음처럼 construireSystème·실행한다. Hôte 경로와 게스트의 `/opt/...` 경로는 서로 다르다.

```sh
cd /home/user/jkoros/JavaFrançais
make
javac -encoding UTF-8 -cp build/JavaFrançais.jar Exemples/Salutation.java
java -cp build/JavaFrançais.jar:Exemples Salutation
```

## 3. 전체 valeurAssistant API

valeurBasExtrémité 메서드는 construireTous `public static`이며, 객체를 만들지 않고 `Fichier.lire(...)`처럼 호출한다. 표의 이름은 donnéesEffectif arbreSource 및 JAR의 `javap -public` 결과와 대조했다. 선언된 Contrôles exception 외에도 잘못된 arguments 등에 대한 표준 Java exécuterCommande 시 예외가 발생할 nombre 있다.

### Fichier: `français.Java.Fichier`

`Path`는 `java.nio.file.Path`, `List`는 `java.util.List`opérandeTroisième.

| valeurMéthode | typeRetourner | action·condition |
|---|---|---|
| `chemin(String nom)` | `Path` | 이름을 chemin 객체로 convertirValeur. donnéesEffectif 파일을 만들지는 않음 |
| `lire(Path chemin)` | `String` | Fichier 전체를 UTF-8 텍스트로 lireRésultat |
| `écrire(Path chemin, String valeurContenuValeur)` | `Path` | UTF-8 valeurStocker. 파일이 없으면 생성하고, 있으면 기존 내용을 비움 |
| `lireValeurOctet(Path chemin)` | `byte[]` | Fichier 전체를 valeurOctet 배열로 lireRésultat |
| `écrireValeurOctet(Path chemin, byte[] valeurContenuValeur)` | `Path` | valeurOctet valeurStocker. 없으면 생성하고, 있으면 기존 내용을 비움 |
| `créerRépertoire(Path chemin)` | `Path` | 필요한 상위 폴더까지 générer |
| `effectueExistence(Path chemin)` | `boolean` | 존재 여부 vérifier. 확인할 nombre 없는 경우도 `false`valeurTravail nombre 있음 |
| `effacerEntréeÉlément(Path chemin)` | `boolean` | 삭제했으면 `true`, 없으면 `false`. 폴더의 재귀 삭제는 아님 |
| `listeEntréeÉlément(Path chemin)` | `List<Path>` | 바로 valeurBasExtrémité 항목을 chemin valeurAligner 순서로 résultatRetourner. 재귀 탐색은 아님 |

`chemin`, `effectueExistence`를 제외한 valeurSommet 메서드는 `IOException`을 선언한다. `écrire`와 `écrireValeurOctet`는 상위 폴더를 자동으로 만들거나 내용을 valeurContinuation 쓰지 않는다. 필요한 폴더는 먼저 생성한다. 큰 파일은 전체 내용을 메모리에 담는 대신 표준 Java 스트림·valeurCanal API를 사용하는 방식으로 작성할 nombre 있다.

### Caractères: `français.Java.Caractères`

| valeurMéthode | typeRetourner | action·condition |
|---|---|---|
| `encoder(String valeurContenuValeur)` | `byte[]` | 문자열을 UTF-8 바이트로 convertirValeur |
| `déchiffrerDonnées(byte[] valeurContenuValeur)` | `String` | UTF-8 바이트를 문자열로 convertirValeur. 잘못된 입력은 대체 문자로 entréeÉlémentValeurProcessus |
| `normaliserValeur(String valeurContenuValeur)` | `String` | valeurUnicode NFC normaliserValeur. 예: Combinaison valeurLettreHangul `ᄀ` + `ᅡ` → `opérandePremier` |
| `nombreÉlémentsPointCode(String valeurContenuValeur)` | `int` | UTF-16 valeurCode 단위가 아닌 valeurUnicode valeurCode 포인트 nombre |
| `motLexical(String valeurContenuValeur, Locale Langue)` | `List<String>` | valeurAffecter 언어의 `BreakIterator` motLexical 경계로 나눈 plageTexte |

`motLexical`은 공백·문장부호 구간도 반환한다. 자연어 형태소 분석기나 공백을 제거한 valeurMot listeEntréeÉlément API는 아니다. `normaliserValeur`는 입력기나 traduireSource 기능이 아니다. valeurCode 포인트 nombre 역시 사람이 보는 valeurCaractère 수와 항상 같지는 않다. 여러 valeurCode 포인트로 이루어진 valeursCombiner Caractères·가족 이모지 등을 구분해야 한다.

### Communication: `français.Java.Communication`

| valeurMéthode | typeRetourner | action·condition |
|---|---|---|
| `valeurPrendre(URI adresse, Duration limiteTemps)` | `HttpResponse<String>` | HTTP(S) GET. connecter 및 requête limiteTemps réglages. réponse 본문을 UTF-8로 analyserValeur |
| `connecterExtrémité(String adresse, int portMatériel, int millisecondesLimite)` | `Socket` | TCP connecter étatValeurAprès 같은 값으로 lire 제한시간도 réglages |

`valeurPrendre`는 `IOException`, `InterruptedException`을 선언한다. 제한시간은 양수다. 404·500 같은 HTTP erreur 상태도 응답으로 반환하므로 `statusCode()`로 판단하고 `body()`로 본문을 읽는다. élémentListeActuel 구현은 호출마다 HTTP 클라이언트를 만들며 자동 리다이렉트 설정을 추가하지 않는다.

`connecterExtrémité`는 `IOException`을 선언한다. 연결된 소켓은 호출자가 `close()` 또는 try-with-resources로 닫아야 한다. 제한밀리초의 0은 valeurLimite 없음이며, écrire 전체의 valeurÉchéance 시간을 보장하는 옵션은 아니다.

```java
var réponse = Communication.valeurPrendre(
    java.net.URI.create("http://127.0.0.1:8000/"),
    java.time.Duration.ofSeconds(5));
System.out.println(réponse.statusCode());
System.out.println(réponse.body());
```

valeurSommet 조각은 valeurMéthode 안에서 실행하며 별도로 해당 주소의 서버를 실행해야 한다. Java exception 처리가 필요하다.

### Tâche: `français.Java.Tâche`

| valeurMéthode | typeRetourner | action·condition |
|---|---|---|
| `lancer(String nom, Runnable action)` | `Thread` | 이름을 지정한 스레드를 만들고 즉시 lancer |
| `attendreFin(Thread valeurFilExécution)` | `void` | 해당 스레드가 종료할 때까지 `join()` |
| `brièvementReste(long millisecondes)` | `void` | 호출한 스레드를 valeurAffecter valeurTemps 동안 `sleep()` |
| `valeurAtelier(int nombreÉlémentsFilExécution)` | `ExecutorService` | 고정 taille Tâche LanceurProgramme générer. 가닥수는 양수 |

`attendreFin`, `brièvementReste`는 `InterruptedException`을 선언한다. Tâche 실행기는 valeurUtiliser étatValeurAprès `shutdown()`으로 종료하고 필요하면 `awaitTermination(...)`으로 완료를 기다린다. Swing 이벤트 entréeÉlémentValeurProcessus 가닥에서 긴 작업이나 `attendreFin`를 실행하면 화면이 멈출 nombre 있다.

### Écran: `français.Java.Écran`

| valeurMéthode | typeRetourner | action·condition |
|---|---|---|
| `valeurUltérieur(Runnable action)` | `void` | Swing 이벤트 entréeÉlémentValeurProcessus 가닥에 실행을 예약하고 résultatRetourner |
| `fenêtre(String titreFenêtre, JComponent valeurContenuValeur, int valeurLargeur, int valeurHauteur)` | `JFrame` | valeurContenuValeur·크기를 지정한 창을 생성해 afficherValeur |

`fenêtre`을 Swing 이벤트 entréeÉlémentValeurProcessus valeurFilExécution 밖에서 부르면 `IllegalStateException`이 발생한다. 그래픽 세션도 필요하다. QEMU에서는 VNC 데스크톱의 터미널에서 실행한다.

```java
Écran.valeurUltérieur(() -> Écran.fenêtre(
    "français Écran", new javax.swing.JLabel("안녕하세요"), 500, 180));
```

반환된 `JFrame`에 표준 Swing API를 추가로 사용할 nombre 있다. 창의 fermer 동작은 `DISPOSE_ON_CLOSE`opérandeTroisième. `Écran.valeurUltérieur`opérandePremier 반환됐다고 fenêtre 생성이 이미 끝난 것은 아니다.

### EspaceTravail: valeurÉditer·compilerSource GUI

```sh
java -cp /opt/jkoros/lib/JavaFrançais.jar français.Java.EspaceTravail
```

`~/workspace`의 원문을 ouvrir·저장하고, `javac`로 컴파일해 `java`로 실행한다. exécuterCommande Fichier 만들기는 `jclassc --target openjdk` 경로를 사용한다. 작업마당은 개발용 프로그램이며 별도의 Fichier·Caractères API 클래스가 아니다. 생성하는 exécuterCommande Fichier 방식은 [Compilateur description](../compiler/OpenJDK-fichierCodeExécutable.md)을 따른다.

## 4. Python과 C++에서 사용할 nombre effectueExistence?

| modeMéthode | élémentListeActuel Entêtes valeurÉtatValeur | invoquer 가능 rogner |
|---|---|---|
| Java → français JAR | valeurDéfaut Entêtes | valeurSommet 22개 메서드와 EspaceTravail |
| Python → `java` valeurEnfant 프로세스 | Python·Java valeurDéfaut Entêtes | 작은 Java 진입점을 통해 호출하고 표준 Sortie·Fichier 등으로 résultat valeurAvantDirection |
| Python → JPype → JVM | JPype는 valeurDéfaut 배포에 méthodeManquant | 별도 installerValeur étatValeurAprès Java valeurClasse·valeurMéthode invoquer 가능. 이 배포판의 ARM64/musl/Python 3.14 조합은 ajouterFinEntréeÉlément valider valeurNécessaire |
| C++ → JNI → JVM | `g++`, JNI 헤더, `libjvm.so` Entêtes | JVM을 생성하고 français valeurClasse·메서드를 직접 호출할 nombre 있음 |
| Python용 독립 français bibliothèque | élémentListeActuel valeurDéfaut 제공 méthodeManquant | 필요하면 Python 표준 라이브러리를 감싸는 français 모듈을 별도로 작성 |
| C/C++용 독립 français bibliothèque | interne x86 `posix-kor`와 interne ARM64 커널용 étatValeurInitialValeur RAM Fichier 연결이 별도로 존재 | valeurDeux opérandeTroisième 이 Linux/OpenJDK 실행판의 libc 라이브러리는 아님 |

Python의 일반 `import`opérandeDeuxième `ctypes.CDLL`로 JAR를 바로 읽을 수는 없다. C++의 `#include`opérandeDeuxième 일반 네이티브 링커만으로 Java 메서드를 연결할 수도 없다. JVM 프로세스 또는 JVM connecter 계층을 거쳐야 한다.

### Python: ajouterFinEntréeÉlément 패키지 없이 invoquer

exécuterCommande 가능한 Exemples 원문은 [CommandeTexte.java](Exemples/AutresLangues/CommandeTexte.java), [AppelPython.py](Exemples/AutresLangues/AppelPython.py)opérandeTroisième. Python이 Java 진입점을 실행하고 `Caractères.nombreÉlémentsPointCode`의 Entier 결과를 받는다. arguments 목록을 사용하며 interpréteurCommandes commande 문자열을 조립하지 않는다. `subprocess.run`의 프로세스 exécuterCommande·programmeQuitter valeurCode·Sortie entréeÉlémentValeurProcessus 방식은 [Python 공식 Documentation](https://docs.python.org/3/library/subprocess.html)를 따른다.

두 Exemples 파일을 게스트의 같은 폴더에 복사한 valeurRetourArrièreCôté 그 폴더에서 실행한다. Exemples Fichier 자체는 valeurDéfaut 시스템 이미지에 자동 설치돼 있지 않다.

```sh
mkdir -p classes
javac -encoding UTF-8 -cp /opt/jkoros/lib/JavaFrançais.jar -d classes CommandeTexte.java
python3 AppelPython.py --text 'texteHangul 😀'
```

Sortie: `Python → français.Java.Caractères.nombreÉlémentsPointCode: 4`

이 예제의 Python Fonction `nombreÉlémentsPointCode`는 이번 문서의 connecter 예제이며 기존에 설치된 Python 라이브러리는 아니다. élémentListeActuel 예제는 호출할 때마다 JVM 프로세스를 시작한다. Java valeurObjet 자체를 Python으로 가져오는 방식은 아니며, 다른 메서드를 사용하려면 진입점의 arguments·résultat 형식을 확장한다.

### Python: JPype로 같은 프로세스에서 invoquer

JPype를 별도 설치한 환경에서는 élémentListeSuivant 형태로 연결할 nombre 있다. **아래는 valeurSélection 가능한 connecter 방법이며, élémentListeActuel 배포판에 JPype가 설치돼 있거나 exécuterCommande 검증됐다는 뜻은 아니다.** JVM 시작과 `JClass`를 통한 valeurClasse 접근은 [JPype 공식 description](https://jpype.readthedocs.io/en/latest/userguide.html)을 참고한다.

```python
import jpype

jpype.startJVM(
    "/usr/lib/jvm/java-25-openjdk/lib/server/libjvm.so",
    classpath=["/opt/jkoros/lib/JavaFrançais.jar"])
try:
    Caractères = jpype.JClass("français.Java.Caractères")
    print(Caractères.nombreÉlémentsPointCode(jpype.JString("texteHangul 😀")))
finally:
    jpype.shutdownJVM()
```

Python·JVM·connecter 모듈의 CPU 아키텍처가 맞아야 한다. 이 실행판은 ARM64 + musl이므로 일반 x86_64/glibc용 바이너리를 그대로 설치하는 방식은 맞지 않는다. JPype installerValeur·패키지 빌드는 이번 Documentation 작업에서 수행하지 않았다.

### C++: JNI로 직접 invoquer

[AppelJava.cpp](Exemples/AutresLangues/AppelJava.cpp)는 donnéesEffectif exécuterCommande 가능한 예제다. JVM을 Tâche 스레드에서 생성하고 élémentListeSuivant 메서드를 찾는다.

```cpp
jclass type = env->FindClass("français/Java/Caractères");
jmethodID method = env->GetStaticMethodID(
    type, "nombreÉlémentsPointCode", "(Ljava/lang/String;)I");
```

JVM générer·종료와 스레드 연결은 [JNI Invocation API](https://docs.oracle.com/en/java/javase/25/docs/specs/jni/invocation.html)의 방식이다. `JNIEnv*`는 générer·연결된 스레드에서 사용해야 한다. 예제는 Java 예외를 확인하고 JVM 종료까지 처리한다.

게스트에 `AppelJava.cpp`를 복사한 valeurRetourArrièreCôté 컴파일한다. 로그인 환경의 `JAVA_HOME`은 `/usr/lib/jvm/java-25-openjdk`opérandeTroisième.

```sh
g++ -std=c++11 -Wall -Wextra -pthread \
  -I"$JAVA_HOME/include" -I"$JAVA_HOME/include/linux" \
  AppelJava.cpp -L"$JAVA_HOME/lib/server" \
  -Wl,-rpath,"$JAVA_HOME/lib/server" -ljvm -o AppelJava
./AppelJava /opt/jkoros/lib/JavaFrançais.jar
```

Sortie: `C++ → français.Java.Caractères.nombreÉlémentsPointCode: 4`

예제는 `texteHangul 😀`을 UTF-16으로 만들어 `NewString`에 전달한다. `NewStringUTF`opérandePremier 받는 modified UTF-8은 일반 UTF-8과 차이가 있으므로, 일반 UTF-8 이모지 바이트를 그대로 넘기는 예제로 작성하지 않았다. [JNI Chaîne valeurFormat](https://docs.oracle.com/en/java/javase/25/docs/specs/jni/types.html#modified-utf-8-strings)

다른 français 메서드도 JNI 서명과 arguments 자료형을 맞춰 호출할 nombre 있다. 예를 들어 `Path`를 받는 Fichier API는 먼저 `Fichier.chemin`로 Java chemin 객체를 얻어 전달한다. Swing 호출에는 그래픽 세션과 이벤트 entréeÉlémentValeurProcessus valeurFilExécution 규칙도 그대로 적용된다. JNI는 Java 실행을 기계어로 대체하는 기능이 아니며 JVM이 traitementContinuer 필요하다.

### 기존 posix-kor와의 관계

추가된 [interne ARM64 connecter](../posix-kor/arm64-native/Guide.md)은 C++에서 AOT Java 커널의 RAM Fichier API를 직접 호출하며, 별도 EL0 Utilisateur 라이브러리로 Fichier/UDP 루프백 SVC 호출도 제공한다. JNI를 사용하지 않는다. 이 문서의 ARM64 **Linux** 및 français Java JAR와는 다른 exécuterCommande 기반이며 interne 커널은 별도 제한형 Java Compilateur/JVM과 MicroPython 1.24.1을 실행한다. MicroPython의 `import jkoros`로 Java valeurNoyau Fichier·UDP 루프백·rectangle 호출이 가능하지만 이 문서의 JAR를 가져오는 기능은 아니다. interne 커널의 전체 OpenJDK/JRE/CPython 이식은 아직 미완성이다.

[posix-kor](../posix-kor/Guide.md)에는 `ouvrirFichier`, `lireDonnéesFichier`, `écrireDonnéesFichier`, `fermerFichier`, `créerExtrémité`, `envoyerDonnéesDatagramme` 등의 français C 별칭이 있다. 그러나 구현은 **interne jkoros i386 커널의 `int 0x80` invoquer 규약용**이다.

이 `libposix-kor.a`와 interne `sys/stat.h` 등의 헤더는 élémentListeActuel ARM64 Linux 실행판의 libc/C++용 라이브러리가 아니다. 해당 헤더·바이너리를 ARM64 Linux 프로그램에 그대로 연결해서는 ABI가 맞지 않는다. C++용 français valeurClasse 라이브러리나 Python용 바인딩을 valeurDéfaut 제공하는 상태도 아니다. élémentListeActuel Linux 실행판에서 그와 같은 독립 API를 제공하려면 Linux 표준 라이브러리를 대상으로 별도로 réalisation·빌드해야 한다.

## 5. vérifier 범위와 재현

패키지 Entêtes 여부는 [valeurDistribution 패키지 listeEntréeÉlément](../platforms/rpi4/dist/packages.lock.json) 및 construireSystème 루트의 donnéesEffectif 파일로 확인했다. JNI 헤더는 JDK의 `include/jni.h`, `include/linux/jni_md.h`, JVM 라이브러리는 `lib/server/libjvm.so`에 있다. 사용자가 valeurAprès 별도로 설치한 패키지는 이 valeurDéfaut valeurDistribution 목록과 다를 nombre 있다.

이번에 **Hôte x86_64/OpenJDK 11에서** Python valeurEnfant 프로세스 호출과 C++ JNI 직접 호출을 compilerSource·실행해 각각 résultat 4를 확인했다. JAR 공개 메서드도 소스와 대조했다. Python connecter 예제는 ajouterFinEntréeÉlément 패키지를 설치하지 않는다.

문서의 Java valeurUtiliser 예제도 compilerSource·실행했고, 22개 메서드의 Documentation Entêtes 여부와 로컬 Documentation 링크를 확인했다. [Exemples valider enregistrementJournal](build/AutresLangues/rapportValidation.json)

기존 ARM64 QEMU에서는 Java의 Fichier·valeurUnicode·스레드·HTTP 및 Swing Tests 결과가 있다. 이번 Python/C++ connecter 예제의 **ARM64 게스트 실행과 JPype 설치는 별도 검증하지 않았다.** 이미지와 exécuterCommande 중인 Utilisateur 환경은 이 Documentation 작업에서 변경하지 않았다. [기존 SystèmeExploitation valider enregistrementJournal](../platforms/rpi4/VERIFICATION.md)

호스트에서 Python 예제를 재현하려면:

```sh
cd /home/user/jkoros/JavaFrançais
make
mkdir -p build/AutresLangues
javac -encoding UTF-8 --release 11 -cp build/JavaFrançais.jar \
  -d build/AutresLangues Exemples/AutresLangues/CommandeTexte.java
python3 Exemples/AutresLangues/AppelPython.py \
  --jar build/JavaFrançais.jar --classes build/AutresLangues
```

Hôte C++ 예제는 valeurSommet JNI compilerSource 명령의 JDK 경로를 **Hôte JDK chemin**로 바꾸고, source `Exemples/AutresLangues/AppelJava.cpp`와 JAR `build/JavaFrançais.jar`를 지정한다. ARM64 게스트 JDK의 헤더·bibliothèque 경로를 Hôte x86_64 링크 명령에 섞지 않는다.
