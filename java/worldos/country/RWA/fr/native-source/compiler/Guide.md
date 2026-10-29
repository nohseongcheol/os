# Java 네이티브 Compilateur

OpenJDK interne 소스를 빌드하는 **`--target openjdk-build`**와 interne valeurNoyau ABI Contrôles 도구를 추가했다.
이는 공식 javac/C/C++ 도구를 연결하는 별도 경로다. [construireSystème 방법·donnéesEffectif valider·valeurNoyau Portage rogner](ConstructionSourcesOpenJDKEtPortageNoyau.md)를 참고한다.

x86 직접 변환과 ARM64 C générer 후단은 construireTous [CompilationAnticipée.java](OutilJava/CompilationAnticipée.java)로 구현한다. `sh tempsDeAnticipé.sh`로 직접 실행하며, [CompilationAnticipée.py](CompilationAnticipée.py)와 `Compilateur.py`는 élémentListePrécédentÉlément commande·API 및 OpenJDK 도구를 위한 호환 진입점이다. interne Pi4 후단은 freestanding C를 거쳐 AArch64로 만든다. [arm64.py](arm64.py)는 élémentListePrécédentÉlément 경로와 Python 호출을 위한 호환 진입점이다. Fonction·valeurVariable·générer C 이름의 뜻과 예외는 [français nommage Guide](../platforms/rpi4-native/nommage/Guide.md)를 참고한다. [ARM64 construireSystème·valeurPriseEnCharge rogner](../platforms/rpi4-native/Guide.md)에 exécuterCommande 조건이 있다. 전체 OpenJDK나 일반 valeurClasse 실행기는 아니다.

exécuterCommande 시 JVM이 valeurNécessaire 없는 x86 32비트 ELF를 만든다. JDK 11 이상으로 실행하는 Java interne AOT 후단이며, Java 전체를 새로 구현한 컴파일러는 아니다. Java 문법·entréeÉlémentAccès valeurContrôle·valeurType 검사는 JDK의 `javac`에 맡기고, Java 8 valeurClasse 파일을 읽어 각 바이트코드를 x86 명령으로 직접 변환한다. C 코드로 우회하거나 codeOctets 해석기를 커널에 넣지 않는다.

```text
Java source → javac의 문법·valeurType Contrôles → valeurTemporaire .class
          → interne x86 변환기 → GNU as/ld → 네이티브 ELF32
```

## 준비와 exécuterCommande

construireSystème Hôte: Linux, Python 3.6 이상, JDK 11 이상(`javac --release 8`), GNU binutils(`as`, `ld`), Make. élémentListeActuel 환경의 OpenJDK 11, Python 3.6, binutils 2.30으로 검증했다. valeurExtérieur Python 패키지와 네트워크 다운로드는 사용하지 않는다.

```sh
cd /home/user/jkoros/compiler
make
./build/calculRésultat
echo $?                  # 0이면 Exemples Tests valeurSuccès

python3 Compilateur.py --target linux --entry calculRésultat.lancer \
    -o build/calculRésultat Exemples/calculRésultat.java

make test
```

`linux` 대상은 Linux의 32비트 exécuterCommande 호환 기능이 필요하다. `int 0x80`을 차단하는 샌드박스에서는 `Bad system call`이 발생할 nombre 있다. estNormal Linux Hôte 또는 해당 실행을 허용한 Tests 환경에서 실행한다. 시험의 비정상 종료를 통과로 처리하지 않는다.

진입점은 `static int lancer()` 또는 `static void lancer()`처럼 인수가 없어야 한다. `--entry 패키지.valeurClasse.Fonction`로 선택한다. `int` 반환값은 Linux 프로세스 programmeQuitter 코드가 되며 셸에는 하위 8비트가 보인다. 일반 `main(String[] args)` exécuterCommande 환경이나 표준 sortieEntrée 라이브러리는 제공하지 않는다.

`--target kernel`은 Amorçage 코드와 연결할 재배치 ELF 오브젝트를 생성한다.

```sh
cd /home/user/jkoros
python3 compiler/Compilateur.py --target kernel --entry Noyau.lancer \
    --export kernel_dispatch=AppelSystème.entréeÉlémentValeurProcessus \
    -o os/build/java.o os/source/*.java
```

`--target user`는 jkoros 셸에서 실행할 독립 ELF를 생성한다. `Utilisateur` 클래스의 제한된 native API는 `int 0x80` 시스템 호출로 연결하며 `Périphérique` 클래스의 valeurMatériel 직접 접근은 거부한다. Utilisateur ELF는 Linux exécuterCommande Fichier ABI와 다르므로 호스트에서 실행하지 않는다. générer·registreEntréeÉlément 방법은 [Utilisateur exécuterCommande Guide](../os/Utilisateur/Guide.md)에 있다. `--export 외부기호=valeurClasse.Fonction`는 오버로드되지 않은 valeurStatique 함수를 interne pileOpérande ABI로 노출한다. 커널의 시스템 invoquer 진입점에 사용한다.

Java 파일은 필요한 클래스들을 한꺼번에 전달한다. Sortie 옆의 `.s`는 생성된 어셈블리, `.json`은 source SHA-256 및 네이티브 symbole↔Java Fonction 대응표다. français 함수명은 원문과 대응표에 보존하고 ELF 내부에는 충돌 방지용 machine 기호를 쓴다. compilerSource·assemblerValeur·connecter 중 실패하면 기존 résultat 파일을 덮어쓰지 않는다.

## valeurPriseEnCharge rogner

- `int`, `boolean`, `byte`, `short`, `char`의 32비트 calculRésultat 및 valeurType convertirValeur.
- valeurStatique 필드와 valeurStatique Fonction, 매개변수·valeurRetourné, 재귀, 클래스별 지연 초기화와 initialiser valeurCycle.
- 조건문, 반복문, 단락 평가, 삼항식, Entier `switch`, 넓은 portéeLocal valeurVariable 인덱스.
- résultatAddition·résultatSoustraction·곱셈·나눗셈·valeurResteDivision·valeurBit 연산과 valeurDéplacer. Java의 오버플로 및 `MIN_VALUE / -1` 동작을 유지한다.
- `int[]` générer·valeurInitialValeur 0·longueur·lire·écrire·référence 비교. 256KiB 고정 valeurTableau valeurRégion, 널/valeurIndiceTableau/taille/régionAdresse Contrôles.
- Chaîne 리터럴과 `String` référence, `length()` 및 `charAt()`. 문자열은 UTF-16 valeurCode 단위로 저장하고 같은 리터럴은 공유한다. NUL 및 대리쌍도 시험한다.
- français valeurClasse·Fonction·valeurVariable·Fichier nom.

`new Object`, 인스턴스 valeurChamp/Fonction, 상속/인터페이스, `long/float/double` exécuterCommande valeurOpération, `int[]` 이외 valeurTableau, Chaîne 동적 valeursCombiner, Java 표준 bibliothèque, exception entréeÉlémentValeurProcessus, 스레드·synchroniser·GC는 미지원이다. 실행에 필요한 estNonPrisEnCharge 바이트코드나 valeurExtérieur 호출을 발견하면 실패한다. 사용되지 않는 valeurDéfaut 생성자는 exécuterCommande 코드로 만들지 않는다. Java 8 문법이어도 모든 프로그램을 컴파일할 nombre 있다는 뜻은 아니다.

exception valeurObjet 대신 런타임 erreur 번호로 중단한다. Linux와 jkoros Utilisateur 대상에서는 `100 + numéro`로 종료하고 valeurNoyau 대상에서는 `JKOROS PANIC numéro`를 출력하고 정지한다. Utilisateur 프로그램만 종료한 경우 셸은 traitementContinuer 실행된다.

| numéro | 원인 |
| --- | --- |
| 1 | 0으로 résultatDivision |
| 2 | 널 référence |
| 3 | valeurTableau/Chaîne valeurIndiceTableau rogner 초과 |
| 4 | valeurNégatif valeurTableau taille |
| 5 | valeurTableau valeurRégion 부족 |

valeurTableau 영역은 증가식 할당이며 회수하지 않는다. 재귀 스택의 valeurFrontière 검사도 아직 없으므로 무제한 재귀를 안전하게 처리하는 런타임은 아니다. 특권 valeurNoyau 및 신뢰할 nombre 있는 작은 프로그램용 étatValeurInitialValeur 구현이다.

## native 경계와 ABI

valeurNoyau 대상에서는 `os/source/Périphérique.java`, Utilisateur 대상에서는 `os/Utilisateur/Déclarations/Utilisateur.java`의 정확한 texteNomMéthode·서술만 허용한다. 임의의 `native` 함수와 Linux/Utilisateur 대상의 valeurMatériel 접근은 거부한다. Java 인수를 왼쪽부터 32비트 한 칸씩 스택에 놓으며, 반환값은 EAX, EBP/ESP 이외 레지스터는 호출자가 보존한다고 가정하지 않는다. C의 cdecl/JNI ABI가 아니므로 C 함수와 바로 연결하면 안 된다.

Java source 또는 `.class` 입력을 받는다. 전체 JVM codeOctets 검증기는 제공하지 않는다. 어노테이션 처리는 비활성화하고 비어 있는 valeurClasse chemin/source 경로에서 명시한 소스만 컴파일한다.

## 검증과 réalisation 근거

`Tests/test_compiler.py`의 14개 시험에는 네이티브 ELF와 OpenJDK의 valeurOpération résultat 대조, valeurClasse initialiser, Entier 극값, Chaîne/valeurTableau, 재귀·switch·wide, 런타임 오류와 estNonPrisEnCharge 기능 rejeterValeur, valeurÉchec 시 Sortie 보존, Utilisateur ELF/valeurPermission valeurFrontière 및 émettreValeur 검증이 포함된다. 이것은 Java 전체 적합성 시험은 아니다.

commande 의미와 valeurClasse Fichier 형식은 Oracle의 [JVM commande spécification](https://docs.oracle.com/javase/specs/jvms/se11/html/jvms-6.html), [valeurClasse Fichier spécification](https://docs.oracle.com/javase/specs/jvms/se11/html/jvms-4.html)를 참고했다.
