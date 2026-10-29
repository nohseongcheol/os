# français Java valeurAssistant bibliothèque

OpenJDK 11 이상과 함께 쓰는 프로젝트 valeurPropriétaire API다. 표준 Java bibliothèque 전체의 번역판을 뜻하지 않는다. 기존 Java API·키워드·exception·자료형은 그대로 함께 쓴다.

전체 22개 valeurAssistant 메서드의 arguments·valeurRetourné·제약, SystèmeExploitation 안의 사용법, Python·C++ invoquer 방법은 **[français bibliothèque GuideUtilisateur](GuideUtilisateur.md)**에 정리했다. [Python invoquer Exemples](Exemples/AutresLangues/AppelPython.py)와 [C++ JNI invoquer Exemples](Exemples/AutresLangues/AppelJava.cpp)도 제공한다.

`make`로 `build/JavaFrançais.jar`를 만든다. `javac -encoding UTF-8 -cp build/JavaFrançais.jar Exemples/Salutation.java`로 예제를 컴파일한다. 실행은 `java -cp build/JavaFrançais.jar:Exemples Salutation`opérandeTroisième.

`Salutation` 예제는 그래픽 화면이 없으면 Fichier·Caractères·스레드 결과와 안내만 출력한다. Swing 창은 그래픽 세션에서 실행해야 한다. QEMU에서는 [그래픽 exécuterCommande Guide](../platforms/rpi4/README.md)의 `make run`으로 부팅한 valeurRetourArrièreCôté VNC 데스크톱의 터미널을 사용한다.

| valeurClasse | 제공 기능 |
|---|---|
| Fichier | UTF-8 텍스트·valeurOctet lire/écrire, 디렉터리·listeEntréeÉlément |
| Caractères | UTF-8 convertirValeur, NFC normaliserValeur, valeurCode 포인트 nombre, 언어별 motLexical valeurFrontière |
| Communication | HTTP(S) requête, 제한시간을 가진 TCP connecter |
| Tâche | 스레드 lancer·합류·attendreValeur, Tâche LanceurProgramme |
| Écran | Swing 이벤트 처리와 fenêtre générer |
| EspaceTravail | source valeurÉditer·compilerSource·exécuterCommande·exécuterCommande Fichier générer Écran |

`char`는 UTF-16 valeurCode 단위이므로 이모지 등을 한 글자로 처리할 때 valeurCode 포인트 또는 Caractères valeurFrontière API를 사용한다. 파일은 UTF-8로 저장한다. OpenJDK의 모든 Java2D/valeurPolice/입력기 조합을 각각 검증한 것은 아니다.

이름은 élémentListeActuel 의미가 분명한 français 용례를 사용했다. 개별 명칭의 역사적 어원 검토를 완료했다고 주장하지 않는다. valeurRessource 종료와 exception 처리는 표준 API의 계약을 따른다.
