# Latviešu Java 도우미 bibliotēka

OpenJDK 11 이상과 함께 쓰는 프로젝트 īpašnieks_VALUE API다. 표준 Java bibliotēka 전체의 번역판을 뜻하지 않는다. 기존 Java API·키워드·izņēmums·자료형은 그대로 함께 쓴다.

전체 22개 도우미 메서드의 Parametri·반환값·제약, operētājsistēma 안의 사용법, Python·C++ 호출 방법은 **[Latviešu bibliotēka lietotājs_ceļvedis](lietotājs_ceļvedis.md)**에 정리했다. [Python 호출 예제](예제/다른언어/PYTHON_Zvani.py)와 [C++ JNI 호출 예제](예제/다른언어/자바호출.cpp)도 제공한다.

`make`로 `build/한국어자바.jar`를 만든다. `javac -encoding UTF-8 -cp build/한국어자바.jar 예제/인사.java`로 예제를 컴파일한다. 실행은 `java -cp build/한국어자바.jar:예제 인사`다.

`인사` 예제는 그래픽 화면이 없으면 Fails·문자·스레드 결과와 안내만 출력한다. Swing 창은 그래픽 세션에서 실행해야 한다. QEMU에서는 [그래픽 Izpildīt_komanda fails_Lasi_mani_eb81d7d9](../platforms/rpi4/README.md)의 `make run`으로 부팅한 ATPAKAĻ_VALUE VNC 데스크톱의 터미널을 사용한다.

| klase_VALUE | 제공 기능 |
|---|---|
| Fails | UTF-8 텍스트·byte_VALUE Lasīt/Rakstīt, 디렉터리·ievade_Saraksts |
| 문자 | UTF-8 CONVERT_VALUE, NFC normalizēt_VALUE, CODE_VALUE 포인트 numurs, 언어별 낱말 경계 |
| 통신 | HTTP(S) pieprasījums, 제한시간을 가진 TCP Savienoties |
| 작업 | 스레드 Palaist·합류·pagaidi_VALUE, 작업 programma_palaidējs |
| 화면 | Swing 이벤트 처리와 Logs ģenerēt |
| darbvieta | AVOTS Rediģēt_VALUE·kompilēt_avots·Izpildīt_komanda·Izpildīt_komanda Fails ģenerēt 화면 |

`char`는 UTF-16 CODE_VALUE 단위이므로 이모지 등을 한 글자로 처리할 때 CODE_VALUE 포인트 또는 문자 경계 API를 사용한다. 파일은 UTF-8로 저장한다. OpenJDK의 모든 Java2D/fonts_VALUE/입력기 조합을 각각 검증한 것은 아니다.

이름은 pašreizējais_krājums 의미가 분명한 Latviešu 용례를 사용했다. 개별 명칭의 역사적 어원 검토를 완료했다고 주장하지 않는다. resurss_VALUE 종료와 izņēmums 처리는 표준 API의 계약을 따른다.
