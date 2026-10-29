# français Java Communication·sortieEntrée·exception API

패키지는 `français.interne`opérandeTroisième. Hôte `javac --release 8`로 컴파일한 class를
interne ARM64 커널의 JVM에서 실행한다. Communication·Fichier·exception API는 OpenJDK와 대조한다. 아래의 직접 구현한 Écran·Tâche valeurFilExécution API는 interne JVM 전용이다.
기존 표준 Java bibliothèque 전체의 français 번역판은 아니다.

```java
import français.interne.*;

public class réseau {
    public static void main(String[] arguments) throws ExceptionSortieEntrée {
        Connexion connecter = Connexion.ouvrir("10.0.2.2", 9000);
        try {
            connecter.délaiExpiration(700);
            connecter.Sortie().écrire(Caractères.encoder("안녕하세요\n"));
            FluxEntrée valeurEntrée = connecter.valeurEntrée();
            Sortie.écrireNuméro(valeurEntrée.lire());
        } catch (ExceptionDélaiExpirationAttendre erreur) {
            Sortie.écrireLigne(erreur.description());
        } finally {
            connecter.fermer();
        }
    }
}
```

`Socket`, `getOutputStream`, `write`, `getInputStream`, `read`, `close`를
Utilisateur 예제에서 직접 호출할 필요가 없다. `try/catch/throws` 등 Java 문법은 유지한다. `String`은 예약어가 아니라 javac가 Chaîne 리터럴에 사용하는 표준 클래스다. interne 실행기는 `public static void lancer()`도 진입점으로 받는다.

## 통신과 valeurFlux

| valeurClasse | français invoquer |
|---|---|
| Connexion | `ouvrir(adresse, numéroPort)`, `valeurEntrée()`, `Sortie()`, `délaiExpiration(millisecondes)`, `numéroPort()`, `numéroPortLocal()`, `connecté()`, `estFermé()`, `fermer()` |
| recevoirPort | `ouvrir(numéroPort)`, `recevoir()`, `numéroPort()`, `délaiExpiration(millisecondes)`, `estFermé()`, `fermer()` |
| FluxEntrée | `lire()`, `lire(byte[])`, `lire(byte[], lancer, longueur)`, `fermer()` |
| FluxSortie | `écrire(int)`, `écrire(byte[])`, `écrire(byte[], lancer, longueur)`, `émettreValeur()`, `fermer()` |
| CanalDatagramme | `ouvrir(numéroPort)`, `envoyer(adresse, numéroPort, texte)`, `recevoir()`, `délaiExpiration(millisecondes)`, `numéroPort()`, `estFermé()`, `fermer()` |
| transportConnexion | `ouvrir(...)`, `ouvrirRécepteur(...)`는 valeurSommet français 객체를 résultatRetourner |
| Contrôles | `exiger(condition, valeurCause)` |

TCP 입력은 한 번에 요청한 모든 바이트가 도착한다고 가정하지 않는다.
`lire()`의 Fichier 끝은 -1, valeurTableau 읽기의 반환값은 donnéesEffectif 읽은 길이다.
네트워크 흐름을 닫으면 연결도 닫힌다. numéroPort 0은 빈 번호를 자동 배정한다.
UDP 전문은 élémentListeActuel interne 커널에서 512바이트까지 받으며, 주소는 valeurChiffre IPv4를 사용한다.
`localhost` 루프백 외의 nom 풀이(DNS)는 interne 커널에 아직 없다.

기존 `transportConnexion.connecter/écouterExtrémité/recevoir`, `Communication.ouvrir/envoyer/recevoir`는 표준 Java 객체를
사용하던 코드와의 연결용이다. 새 코드는 `Connexion`, `recevoirPort`, `CanalDatagramme`를 쓴다.

## français exception

모든 valeurBasExtrémité 클래스는 valeurDéfaut 생성자, `새예외("description")` 형태의 Chaîne 생성자와
`description()`을 제공한다. donnéesEffectif générer 문법은 `new ExceptionDélaiExpirationAttendre("attendreÉtatValeur terminaison")`이다.

| français exception | 상위 valeurClasse / 용도 |
|---|---|
| exception | `java.lang.Exception`, 직접 던지는 일반 Contrôles exception |
| ExceptionExécution | `java.lang.RuntimeException` |
| ExceptionSortieEntrée | `java.io.IOException`, français Fichier·Communication API의 Contrôles exception |
| ExceptionDélaiExpirationAttendre | `ExceptionSortieEntrée`, Communication délaiExpiration 초과 |
| ExceptionRechercherAdresse | `ExceptionSortieEntrée`, adresse vérifier valeurÉchec |
| ExceptionFichierManquant | `ExceptionSortieEntrée`, Fichier ouvrir valeurÉchec |
| ExceptionCommunication | `ExceptionSortieEntrée`, 표준 SocketException convertirValeur |
| ExceptionArgumentInvalide | `java.lang.IllegalArgumentException` |
| ÉchecFormatNuméro | `ExceptionArgumentInvalide` |
| ExceptionBornes | `java.lang.IndexOutOfBoundsException` |
| ExceptionBornesTableau / ExceptionBornesChaîne | `ExceptionBornes` |
| ExceptionRéférenceRéférenceNulle | `java.lang.NullPointerException` |
| ÉchecArithmétique | `java.lang.ArithmeticException` |
| ExceptionÉtatValeur | `java.lang.IllegalStateException` |
| ExceptionConversionTypeType | `java.lang.ClassCastException` |
| ÉchecTailleTableauNégatif | `java.lang.NegativeArraySizeException` |
| ÉchecStockerTableau | `java.lang.ArrayStoreException` |
| ExceptionÉtatValeurFilExécution | `java.lang.IllegalThreadStateException` |
| ExceptionInterrompuAttendre | `java.lang.InterruptedException`, `Tâche.attendreFin`의 attendreValeur 중단 |

`exception`와 `ExceptionExécution`는 모든 français 예외의 valeurCommun 부모가 아니다. valeurSommet 상속 관계를
사용하며, Fichier·Communication 전체를 잡으려면 `catch (ExceptionSortieEntrée erreur)`를 쓴다.
français API가 표준 sortieEntrée 오류를 français 예외로 변환한다.
기존 français Communication 호출에서 `SocketTimeoutException`을 잡던 코드는
`ExceptionDélaiExpirationAttendre`를 잡도록 옮긴다. 표준 `java.net`을 직접 사용하는 코드의
exception 유형은 기존 Java 규약을 따른다.
일반 Java 연산이 자동으로 던지는 표준 예외까지 이름을 바꾸지는 않는다.
예를 들어 `1 / 0`의 ArithmeticException과 직접 만든 산술예외는 서로 다른 형식이다.
élémentListeActuel interne JVM에 이 20종을 추가했다. 임의의 Utilisateur Throwable 하위 valeurClasse 전체를
지원하도록 확장했다는 뜻은 아니다.

## compilerSource·exécuterCommande

```sh
cd /home/user/jkoros/platforms/rpi4-native
make construireSystème
javac --release 8 -encoding UTF-8 -cp dist/jkoros-native-korean.jar \
  -d build/한국어사용 Tests/Java/testMiseEnRéseauCoréen.java
python3 Outils/exécuterFichier.py build/한국어사용/testMiseEnRéseauCoréen.class
make test-jvm
```

내장 라이브러리는 Utilisateur JVM ELF 안에 탑재된다. `.jar`는 Hôte javac의
valeurClasse 경로로 사용한다. arbreSource 묶음은 `dist/jkoros-native-korean-sources.zip`이다.
게스트의 제한형 `javac`는 français 예외의 `throws` 선언과 그 import를 인식한다.
interne JVM의 Thread.interrupt 동작을 새로 구현한 것은 아니다.
try/catch·valeurObjet·valeurPriseRéseau Exemples 전체의 arbreSource 컴파일은 Hôte javac를 사용한다.
`/example/java/ExempleFichier.java`는 게스트 javac로도 컴파일할 nombre 있다.

donnéesEffectif TCP/UDP 예제는 [ExempleRéseau.java](../../../example/java/ExempleRéseau.java),
exécuterCommande 절차는 [example Guide](../../../example/README.md),
arbreSource nommage 원칙은 [nommage Guide](../nommage/Guide.md)에 있다.

## Swing fenêtre Exemples

`/example/java/ExempleFenêtre.java`와 컴파일된 `.class`opérandePremier Amorçage 시 준비된다.
`cd /example/java` élémentListeSuivant `java ExempleFenêtre`로 연다. nom valeurEntrée, saluer 버튼,
인사말과 valeurCliquer nombreÉlémentsRépétition actualiser, X 닫기를 지원한다.

| 기능 | français 직접 API |
|---|---|
| Runnable / run | `TâcheTâcheExécutable.exécuterTâche()` |
| ActionListener / actionPerformed | `RécepteurAction.recevoirAction(NotificationAction notification)` |
| ActionEvent | `NotificationAction.texteCommande()`, `sourceÉvènement()`, `numéro()` |
| JFrame | `fenêtre(titreFenêtre, étendueLargeur, valeurHauteur)`, `ajouterÉlément(ÉlémentÉcran)`, `afficherFenêtre()`, `fermer()`, `estVisible()` |
| JButton | `bouton(texte, positionHorizontal, positionVertical, étendueLargeur, valeurHauteur, valeurRécepteur)`, `définirRécepteurAction(valeurRécepteur)` |
| JLabel / JTextField | `étiquette(...)`, `ChampTexte(...)` |
| valeurCommun Écran valeurÉlément | `ÉlémentÉcran.lireTexte()`, `écrireTexte(texte)`, `définirBornes(positionHorizontal, positionVertical, étendueLargeur, valeurHauteur)` |
| SwingUtilities.invokeLater | `FileAttenteÉvènement.invoquerUltérieur(TâcheTâcheExécutable)`, `estDistributionEnCoursÉvènement()` |
| Thread | `tâcheFond(TâcheTâcheExécutable)`, `démarrerTâche()`, `attendreFin()`, `estVivant()`, `céderTâche()` |
| 명령행 | `lancer()`, `Arguments.nombreÉlémentsÉlémentListe()`, `Arguments.texte(indiceOrdinal)` |

valeurSommet 클래스들은 `JButton`·`Thread` 등의 객체를 만들거나 보관하지 않는다.
interne JVM의 `invoquerÉcranCoréen`, `filExécutionProcessus`opérandePremier français valeurClasse·valeurMéthode·서술자를
해석해 Écran 요소와 exécuterCommande 가닥을 직접 만든다. action 알림도 interne 객체이며
콜백으로 `exécuterTâche`와 `recevoirAction`를 직접 찾는다. 표준 Swing/Thread를
사용하는 기존 프로그램의 exécuterCommande 경로는 별도로 남아 있다.

Java 소스의 `native` 선언은 interne JVM에 구현한 계약이다. 생성자의 예외는
이 계약이 없는 Hôte JVM에서 무동작 객체가 생기지 않도록 하는 rejeterValeur 경로다.
interne JVM은 생성자를 직접 처리한다. 일반 OpenJDK에서는 이 직접 réalisation API를
실행할 nombre 없다. Hôte javac로 컴파일한 valeurRetourArrièreCôté interne JVM에서 실행한다.
`StringUtilities`라는 표준 Swing 클래스는 없으며, Écran 큐 기능은 `SwingUtilities`에 해당한다.

```java
import français.interne.*;
public class 가닥예제 implements TâcheTâcheExécutable {
    public void exécuterTâche() { Sortie.écrireLigne("français Tâche exécuterCommande"); }
    public static void lancer() throws ExceptionInterrompuAttendre {
        tâcheFond valeurFilExécution = Tâche.lancer(new 가닥예제());
        Tâche.attendreFin(valeurFilExécution);
    }
}
```

`example/java`의 다섯 소스는 motsRéservé·리터럴 외 식별자를 한국어로 작성한다.
valeurTableau arguments 대신 `Arguments`, 길이는 `Caractères.nombreÉlémentsOctet`를 사용한다.
표준 Java의 `main(String[])`도 traitementContinuer 지원한다. valeurDeux opérandeTroisième 정의되어 있으면
interne 실행기는 arguments 없는 `lancer()`을 우선한다.
기존 français Écran 래퍼의 표준 `Component`/`Runnable`/`ActionListener` 인수와
`Tâche.lancer(Runnable)`을 사용하던 코드는 새 français 계약으로 수정하고 재컴파일한다.
이는 전체 AWT/Swing·Thread API valeurPriseEnCharge 또는 모든 JDK 소스의 번역을 뜻하지 않는다.

바이트코드에도 valeurClasse·valeurMéthode 이름과 서술자가 남는다.
français nom 자체는 합법이지만, 다른 클래스에서 그 이름을 참조하는 valeurSousPartie,
상속·valeurMéthode 재정의, native connecter, 런처의 진입점도 함께 맞춰야 한다.
근거는 [JLS valeurIdentificateur](https://docs.oracle.com/javase/specs/jls/se25/html/jls-3.html#jls-3.8)와
[JVMS valeurMéthode référence](https://docs.oracle.com/javase/specs/jvms/se25/html/jvms-4.html#jvms-4.4.2)opérandeTroisième.
