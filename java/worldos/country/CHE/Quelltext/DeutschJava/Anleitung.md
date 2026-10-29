# Deutsch Java helferWert bibliothek

OpenJDK 11 이상과 함께 쓰는 프로젝트 eigentümerWert API다. 표준 Java bibliothek 전체의 번역판을 뜻하지 않는다. 기존 Java API·키워드·ausnahme·자료형은 그대로 함께 쓴다.

전체 22개 helferWert 메서드의 argumente·zurückgegebenWert·제약, Betriebssystem 안의 사용법, Python·C++ aufrufen 방법은 **[Deutsch bibliothek BenutzerLeitfaden](BenutzerLeitfaden.md)**에 정리했다. [Python aufrufen Beispiele](Beispiele/AndereSprachen/PythonAufrufen.py)와 [C++ JNI aufrufen Beispiele](Beispiele/AndereSprachen/JavaAufrufen.cpp)도 제공한다.

`make`로 `build/DeutschJava.jar`를 만든다. `javac -encoding UTF-8 -cp build/DeutschJava.jar Beispiele/Gruß.java`로 예제를 컴파일한다. 실행은 `java -cp build/DeutschJava.jar:Beispiele Gruß`dritterOperand.

`Gruß` 예제는 그래픽 화면이 없으면 Datei·Zeichen·스레드 결과와 안내만 출력한다. Swing 창은 그래픽 세션에서 실행해야 한다. QEMU에서는 [그래픽 befehlAusführen Anleitung](../platforms/rpi4/README.md)의 `make run`으로 부팅한 rückseiteWert VNC 데스크톱의 터미널을 사용한다.

| klasseWert | 제공 기능 |
|---|---|
| Datei | UTF-8 텍스트·byteWert lesen/schreiben, 디렉터리·eintragListe |
| Zeichen | UTF-8 wertUmwandeln, NFC wertNormalisieren, kodeWert 포인트 Zahl, 언어별 lexikalischMaschinenwort grenzstelleWert |
| Kommunikation | HTTP(S) anfrage, 제한시간을 가진 TCP verbinden |
| Aufgabe | 스레드 ausführenVorgang·합류·wertWarten, Aufgabe ProgrammStarter |
| Bildschirm | Swing 이벤트 처리와 fenster generieren |
| Arbeitsraum | Quelltext bearbeitenWert·quelltextÜbersetzen·befehlAusführen·befehlAusführen Datei generieren Bildschirm |

`char`는 UTF-16 kodeWert 단위이므로 이모지 등을 한 글자로 처리할 때 kodeWert 포인트 또는 Zeichen grenzstelleWert API를 사용한다. 파일은 UTF-8로 저장한다. OpenJDK의 모든 Java2D/schriftartWert/입력기 조합을 각각 검증한 것은 아니다.

이름은 aktuellElementeintrag 의미가 분명한 Deutsch 용례를 사용했다. 개별 명칭의 역사적 어원 검토를 완료했다고 주장하지 않는다. betriebsmittelEintragWert 종료와 ausnahme 처리는 표준 API의 계약을 따른다.
