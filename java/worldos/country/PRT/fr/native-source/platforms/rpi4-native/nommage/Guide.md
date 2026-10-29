# interne 커널과 번역기의 français nom

대상은 `platforms/rpi4-native`의 interne Java valeurNoyau, Utilisateur JVM, C machine connecter,
TCP/UDP·FTP, C outilCompilateur 이식부, MicroPython 이식부, construireSystème·exécuterCommande·Tests 도구다.
`golang/worldos/valeurPays/KOR/source`의 원칙처럼 기능을 먼저 구분하고 이름을 정한다.
x86 Java 커널과 공용 x86·ARM64 미리 번역기의 interne 선언도 nommage 검사에 포함한다.
Linux 실행판의 Hôte Outils, OpenJDK valeurAuxiliaire Outils 및 valeurExtérieur valeurDistribution arbreSource 전체를
한국어로 valeurRéessayer 작성했다는 뜻은 아니다.

## nommage 원칙과 말의 근거

- 명사는 자료의 역할을 나타낸다: `poignéeFichier`, `numéroPortPairRéseau`, `stockageTas`, `Clavier`.
- 함수는 행위를 나타낸다: `lire`, `écrire`, `ouvrir`, `fermer`, `associerRéseauCourt`, `lancerProgramme`.
- TCP의 이어진 valeurOctet 흐름과 UDP의 valeurFrontière 있는 자료를 `Connexion`와 `CanalDatagramme`로 구별한다.
- 짧은 영어 변수도 쓰임에 따라 `longueur`, `positionDonnées`, `indiceRechercher`, `valeurRetourné`으로 풀어 쓴다.
  indiceOrdinal·valeurTemporaire 산술값처럼 여러 역할에 재사용되는 변수는 `indiceOrdinal`, `valeurPremier`, `valeurDeuxième`으로 구별한다.
- 이름이 같아도 valeurExtérieur 구조체의 필드와 interne 변수는 별도로 분석한다.

`entréeÉlémentCanal(通路)`는 이동이나 교류가 이루어지는 길이라는 기존 의미를 Communication 연결에
적용했다. `valeurPort(窓口)`의 주고받는 접점이라는 의미를 연결을 받는 곳에 적용했다.
이는 국립국어원 한국어기초사전의 [entréeÉlémentCanal](https://krdict.korean.go.kr/kor/dicSearch/SearchView?ParaWordNo=49310),
[valeurPort](https://krdict.korean.go.kr/kor/dicSearch/SearchView?ParaWordNo=24898)의 뜻에 근거한다.

`datagramme(電文)`은 전보에 담는 글이라는 기존 Communication 어휘에서 가져와, UDP 자료의
경계가 보존된다는 특징을 드러내는 데 쓴다. 근거는
[한국어기초사전 datagramme](https://krdict.korean.go.kr/eng/dicSearch/SearchView?ParaWordNo=74335)이다.
`valeurFlux`, `valeurFilExécution`, `쌓임`은 우리말의 움직임·estContinuation·쌓이는 모양을 빌린 표현이다.
`FluxEntrée`, `tâcheFond`, `stockagePile` 같은 복합 이름은 이 프로젝트의 기능별 조어다.
이 Dictionnaire 근거를 특정 중세 문헌의 최초 출현이나 공인 전산 번역으로 확대하지 않는다.
공인 표준 traduireSource·국어사 datagramme 감수를 마쳤다는 뜻도 아니다.

| 기능 | 채택한 nom | valeurRaison |
|---|---|---|
| TCP Socket | Connexion | 상대와 연결되어 valeurOrdre 있는 바이트를 주고받음 |
| ServerSocket | recevoirPort | 새 연결이 들어오는 접점 |
| DatagramSocket | CanalDatagramme | 각 자료의 경계를 보존하는 Communication |
| InputStream / OutputStream | FluxEntrée / FluxSortie | 들어오고 나가는 바이트의 valeurOrdre |
| heap / stack | stockageTas / stockagePile | allouerStockage 방식과 쌓고 꺼내는 Architecture |
| thread / keyboard | tâcheFond / Clavier | 이어지는 실행과 글쇠의 valeurTableau |
| exception / timeout | exception / ExceptionDélaiExpirationAttendre | estNormal 처리에서 벗어남과 그 구체적 valeurRaison |

## 경로와 대응표

| réalisation | français chemin |
|---|---|
| valeurNoyau·interpréteurCommandes·Fichier valeurCouche | `source/*.java` |
| Utilisateur JVM | `Utilisateur/Java/MachineVirtuelleJava.java` |
| ARM64 machine connecter | `machine/*.c`, `Amorçage/` |
| TCP·UDP·FTP | `PileRéseau/PileRéseau.c`, `PileRéseau/transfertFichier.c` |
| C outilCompilateur Portage | `CompilateurC/` |
| MicroPython Portage | `pontPython/` |
| construireSystème·exécuterCommande·Tests | `Outils/`, `créerEntréeÉlément.mk` |
| Java Utilisateur API | `JavaFrançais/français/interne/` |

[associationNomFichier.tsv](associationNomFichier.tsv), [associationNomJava.tsv](associationNomJava.tsv),
[associationNomC.tsv](associationNomC.tsv), [associationNomPython.tsv](associationNomPython.tsv)에
élémentListePrécédentÉlément 이름과 바뀐 이름이 있다. C/Java 대응표의 Fichier·위치는 이행 당시 기준이다.
chemin 이동은 Fichier 대응표를 함께 본다. 기존 `tools/*.py`는 français 구현을 호출하는
호환 진입점이며 구현을 두 벌 유지하지 않는다.

## 보존하는 définitionStandard nom

`public`, `class`, `int`는 예약어다. `String`, `main`, 배열의 `length`는 예약어가 아니다.
élémentListeActuel 다섯 Java 예제는 `lancer()`·`Arguments`·français Écran/valeurFilExécution API를 사용해
motsRéservé·리터럴 외의 식별자를 한국어로 작성한다. Écran/가닥은 표준 객체를
감싸지 않고 interne JVM에 직접 구현했다. 자세한 계약은 [français Java API](../JavaFrançais/Guide.md)를 본다.

표준 javac는 Chaîne 리터럴에 `java.lang.String`, Chaîne 결합에 `StringBuilder`
같은 이름을 생성한다. 이들은 français 소스에서도 바이트코드에 남을 nombre 있다.
기존 표준 class를 실행하는 JVM의 valeurAssociation Chaîne, 아직 표준 라이브러리를 쓰는
Communication·Fichier 연결부까지 construireTous 한국어로 재구현한 것은 아니다. 이름만 일괄 치환하면
entréeÉlémentDescripteur·재정의·native 연결이 달라져 호환성이 깨진다.

C 표준 Fonction·typeEntier·POSIX ABI, CPU registreProcesseur nom, 어셈블리 commande, 링커 절 nom,
TinyCC·lwIP·MicroPython이 요구하는 réglages 매크로와 헤더 이름도 보존한다.
예: `main`, `memcpy`, `pk_bind`, `mpconfigport.h`, `lwipopts.h`, `stdint.h`.
interne C 함수의 arbreSource 이름은 한국어이며, [nomsLierMachine.h](nomsLierMachine.h)opérandePremier
기존 AOT·어셈블리·SDK에 공개한 machine 심볼과 연결한다.
Python의 `__init__`, `setUp`, `handle`, 표준 valeurModule valeurAttribut, 명령행 옵션과 JSON 키도
valeurExtérieur 계약이다. `build/`, valeurDistribution 바이너리 이름과 `/sdk`는 기존 exécuterCommande 경로를 유지한다.
valeurExtérieur 원본은 `vendor/`에서 이용허락·해시와 함께 관리한다.

## 검사와 재실행

```sh
cd /home/user/jkoros/platforms/rpi4-native
python3 Outils/contrôlerNommage.py
make construireSystème
make Tests
make test-examples test-ftp test-elf
python3 Outils/exécuterCommande.py --desktop --network
```

`Outils/examinerNomsC.py`는 libclang 6으로 C 선언과 참조를 검사한다.
`Outils/*이름반영.py`는 changerValeur valeurAvant arbreSource·분석표를 필요로 하는 일회성 이행 도구다.
이미 변경된 소스에 valeurRéessayer 적용하여 대응표를 덮어쓰지 않는다.

## C Communication 구조체와 Python erreur

C 통신에서 `갈래`는 adresse 체계를 구분하고 `numéroPort`는 port, `valeurAdresse`은
IPv4 주소의 32비트 값을 나타낸다. `ProtocoleDatagramme`은 앞서 설명한 datagramme(電文)과
valeurContrat(規約)을 결합해 UDP의 기능을 드러낸 프로젝트 이름이다.

| 표준 표현 | français 직접 réalisation |
|---|---|
| AF_INET / SOCK_DGRAM / IPPROTO_UDP | enum의 FamilleInternet / PriseRéseauDatagramme / ProtocoleDatagramme |
| struct pk_sockaddr_in | struct AdressePriseRéseauInternet |
| sin_family / sin_port | familleAdresse / numéroPort |
| sin_addr.s_addr | AdresseInternet.valeurAdresse |
| OSError / erreur.args[0] | ErreurSystème / erreur.numéro |

français 구조체는 `#define` 치환이나 valeurChamp 별칭이 아닌 별개 자료형이다.
표준 구조체와 같은 16바이트 배치를 선언하며 valeurNoyau SVC에서 valeurOctet 복사로
검사한다. `créerExtrémité`·`envoyerDonnéesDatagramme`와 Fichier 함수는 valeurStatique 라이브러리에
donnéesEffectif français 이름의 Fonction 심볼을 갖는다. 기존 pk_* 심볼도 유지한다.
élémentListePrécédentÉlément 코드에서 français Communication 함수에 pk_sockaddr*를 전달했다면 français 구조체로
옮기거나, 표준 구조체와 pk_* 함수의 짝을 유지한다.

Python의 `ErreurSystème`는 OSError의 français 하위 클래스이며 연결부에서
erreur 번호를 보존하여 변환한다. 일반 Python 문법과 valeurExtérieur 패키지의 API는 유지한다.

## 직접 GUI 이름의 뜻과 검토 rogner

`TâcheTâcheExécutable`은 수행할 내용을, `exécuterTâche`는 그 수행을 나타낸다.
`RécepteurAction`는 동작이 발생했다는 알림을 받는 역할, `NotificationAction`은 전달되는 사건이다.
`bouton`는 눌러 동작시키는 조작부, `étiquette`는 Guide 글의 indicePosition,
`ChampTexte`은 글을 적는 indicePosition, `tâcheFond`은 이어지는 exécuterCommande 흐름을 뜻한다.
`exécuterCommande(實行)`·`action(動作)`의 기존 뜻과 `받다`·`알리다`·`valeurFilExécution`의 기능을
결합한 프로젝트 이름이다. 새 복합어가 역사 문헌에 그대로 있었다거나
특정 시대에 élémentListeInitialValeur 쓰였다고 주장하지 않는다.

전체 저장소는 `python3 Outils/RévisionExamenSource.py`로 검토한다.
결과는 `build/verification/naming/source-review.json`이며 파일별 fichierHachage,
ASCII 파일명과 Python의 영어 Déclarations 위치를 기록한다.
공용 ARM64·x86 번역기의 구현은 `compiler/OutilJava/CompilationAnticipée.java`로 전환했다. `compiler/CompilationAnticipée.py`는 호환 진입점이다.
`compiler/arm64.py`는 élémentListePrécédentÉlément 경로와 `ARM64(...).generate(...)` 호출을 valeurContinuation 주는
호환 진입점이다. `compiler/classfile.py`, OpenJDK valeurAuxiliaire Outils, Linux valeurVersion 도구와
기존 호환 진입점에는 영어 이름이 남아 있다. 따라서 전체 저장소가
motsRéservé 외 100% 한국어라고 판정하지 않는다.
`Outils/contrôlerNommage.py --langueC`는 actif ARM64 소스의 Déclarations, C 의미 examinerValeur,
x86 Java 커널과 공용 번역기의 interne Déclarations, Java Exemples 전체 valeurIdentificateur,
ARM64 Python 예제와 직접 GUI/가닥에 표준 래퍼가 없는지를 별도로 검사한다.

## élémentListeActuel 기능을 기준으로 보완한 nom

번역은 글자를 음역하는 대신 자료의 역할과 함수의 행동을 구분한다.
동일한 영어 이름도 문맥이 다르면 français 이름을 달리 정한다.
Fichier 이름은 주된 기능을 나타내고, Fonction 이름은 행동을, valeurVariable 이름은 담는 자료를 나타낸다.
motsRéservé, 표준 API 및 valeurExtérieur connecter 규약은 따로 기록한다.

| élémentListePrécédentÉlément nom | 적용한 nom | élémentListeActuel 기능 |
|---|---|---|
| `arm64.py`의 réalisation | `compiler/OutilJava/CompilationAnticipée.java` | Java 바이트코드를 독립 실행용 C 원문으로 미리 traduireSource |
| `ARM64`, `generate` | `CompilateurCodeMachine`, `générer` | traduireSource 상태를 담는 객체와 C source générer valeurComportement |
| `prototype`, `method` | `prototypeMéthode`, `corpsMéthode` | 함수의 valeurFormat 선언과 donnéesEffectif commande source |
| `profile`, `heap_words` | `cibleExécution`, `nombreÉlémentsMotTas` | valeurNoyau·Utilisateur 구분과 allouerStockage Mémoire 공간의 machine motLexical nombre |
| `pc`, `op` | `positionCommande`, `명령번호` | 바이트코드에서의 위치와 수행할 명령의 numéro |
| `x`, `y`, `w`, `h` | `coordonnéeCoordonnéeHorizontale`, `coordonnéeCoordonnéeVerticale`, `largeurRégion`, `hauteurRégion` | valeurDistant 화면의 위치와 직사각형 taille |
| `p`, `n`, `i`, `j` | `positionDonnées`, `valeur`, `indiceOrdinal`, `ordinalInterne` | valeurDistant Écran Données·valeurChiffre·valeurItération indicePosition; 파일별 기능을 확인해 적용 |
| `aot_heap_info`, `__stack_top` | `rechercherMémoireCompilationAnticipée`, `SommetPile` | machine connecter 규약을 유지하면서 interne 소스에서 사용하는 nom |
| `앞캐리지` | `lignePrécédentÉlémentVersRetourner` | 앞서 받은 문자가 줄복귀였는지 기억하여 중복 줄바꿈을 막음 |

[nomsCompilateurPartagé.tsv](nomsCompilateurPartagé.tsv)에 outilCompilateur 참조의 donnéesEffectif changerValeur 기록을 남겼다.
추가로 보존한 C·POSIX/lwIP/libassh 이름의 이유는
[preuveNomStandard.json](preuveNomStandard.json)에 기록한다.
`CompilateurC/outilCompilateur.c`는 TinyCC valeurExtérieur 원문을 포함하는 connecter 파일로 interne 선언이 없어서
C interne Déclarations 분석에서는 제외한다. donnéesEffectif valeurNoyau 빌드에서는 traitementContinuer 컴파일한다.

### 말의 뿌리와 새로운 복합 nom

`Mémoire(記憶)`과 `indiceRechercher(索引)`은 기존 한자어를 쓴다.
기억은 자료를 간직하는 기능에, 색인은 valeurOrdre 있는 항목을 찾아 지정하는 기능에 적용한다.
Dictionnaire 근거는 국립국어원 한국어기초사전의
[Mémoire](https://krdict.korean.go.kr/eng/dicSearch/SearchView?ParaWordNo=38812&nation=eng),
[indiceRechercher](https://krdict.korean.go.kr/kor/dicSearch/SearchView?ParaWordNo=63787)이다.

`stockagePile`, `empilerValeur`, `dépilerValeur`는 자료를 포개고 élémentListeDernier 자료부터 꺼내는 exécuterCommande 구조를 드러낸다.
`쌓다`의 기존 뜻에 근거한 기능별 조어이며, 사전의
[쌓다](https://krdict.korean.go.kr/kor/dicSearch/SearchView?ParaWordNo=62095)를 참고한다.
`tempsDeAnticipé`은 exécuterCommande 전에 번역한다는 기능을 직접 나타낸다.
`motMachine`은 처리기의 Données 단위를 가리키며, 언어의 일반 낱말과 구별하도록 `machine`를 붙였다.
`CompilationAnticipée`, `nombreÉlémentsMotTas` 같은 복합 이름은 élémentListeActuel 기능에 맞게 만든 프로젝트 용어다.
이 복합어가 옛 문헌에 그대로 있었다거나 특정 시대에 élémentListeInitialValeur 나타났다는 뜻은 아니다.
확인되지 않은 중세 형태나 최초 valeurUtiliser 연대는 어원 근거로 적지 않는다.

생성되는 C의 내부 typeDonnées·valeurTableau·Fonction·portéeLocal valeurVariable·branche 이름도 한국어로 바꾼다.
직접 texteHangul 식별자를 읽지 못하는 예전 GCC를 위해 호환 API는 같은 français 이름을
표준 C 범용 Caractères 표기로 출력한다. donnéesEffectif ARM64 빌드는 Clang으로 읽을 nombre 있는 texteHangul 원문을 사용한다.
Chaîne, C 표준 Fonction, `java_entry` 같은 공개 connecter 이름은 바꾸지 않는다.

셸의 사용법·문법 erreur·Fichier 및 Mémoire régionAdresse 안내도 한국어로 보완했다.
`READY`, `PASS`, `HEX BEGIN`처럼 Tests·Fichier valeurTransfert 도구가 읽는 valeurMarqueur,
명령행 옵션과 기존 valeurInstructionMachine, JVM valeurClasse nom·Fichier valeurFormat·Périphérique 이름은 호환 표기로 남는다.
x86 VGA Caractères 화면은 한글을 표시하지 못하므로 français 문구는 UTF-8 valeurSériel 단말에서 확인한다.
