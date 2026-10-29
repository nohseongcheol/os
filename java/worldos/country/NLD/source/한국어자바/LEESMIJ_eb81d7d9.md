# Nederlands Java helper_WAARDE bibliotheek

OpenJDK 11 이상과 함께 쓰는 프로젝트 eigenaar_WAARDE API다. 표준 Java bibliotheek 전체의 번역판을 뜻하지 않는다. 기존 Java API·키워드·uitzondering·자료형은 그대로 함께 쓴다.

전체 22개 helper_WAARDE 메서드의 argumenten·반환값·제약, besturingssysteem 안의 사용법, Python·C++ 호출 방법은 **[Nederlands bibliotheek gebruiker_guide](gebruiker_guide.md)**에 정리했다. [Python 호출 예제](예제/다른언어/PYTHON_Oproepen.py)와 [C++ JNI 호출 예제](예제/다른언어/자바호출.cpp)도 제공한다.

`make`로 `build/한국어자바.jar`를 만든다. `javac -encoding UTF-8 -cp build/한국어자바.jar 예제/인사.java`로 예제를 컴파일한다. 실행은 `java -cp build/한국어자바.jar:예제 인사`다.

`인사` 예제는 그래픽 화면이 없으면 bestand·문자·스레드 결과와 안내만 출력한다. Swing 창은 그래픽 세션에서 실행해야 한다. QEMU에서는 [그래픽 Uitvoeren_opdracht LEESMIJ_eb81d7d9](../platforms/rpi4/README.md)의 `make run`으로 부팅한 BACK_WAARDE VNC 데스크톱의 터미널을 사용한다.

| les_WAARDE | 제공 기능 |
|---|---|
| bestand | UTF-8 텍스트·byte_WAARDE Lezen/Schrijven, 디렉터리·invoer_Lijst_f07b3200 |
| 문자 | UTF-8 CONVERTEREN_WAARDE, NFC normaliseren_WAARDE, CODE_WAARDE 포인트 nummer, 언어별 낱말 grens_WAARDE |
| communicatie | HTTP(S) aanvraag, 제한시간을 가진 TCP Verbinden |
| 작업 | 스레드 starten·합류·wachten_WAARDE, 작업 app_app_lade |
| scherm | Swing 이벤트 처리와 Venster genereren |
| werkgebied | broncode Bewerk_WAARDE·compileren_bron·Uitvoeren_opdracht·Uitvoeren_opdracht bestand genereren scherm |

`char`는 UTF-16 CODE_WAARDE 단위이므로 이모지 등을 한 글자로 처리할 때 CODE_WAARDE 포인트 또는 문자 grens_WAARDE API를 사용한다. 파일은 UTF-8로 저장한다. OpenJDK의 모든 Java2D/lettertype_WAARDE/입력기 조합을 각각 검증한 것은 아니다.

이름은 actueel_item 의미가 분명한 Nederlands 용례를 사용했다. 개별 명칭의 역사적 어원 검토를 완료했다고 주장하지 않는다. bron_WAARDE 종료와 uitzondering 처리는 표준 API의 계약을 따른다.
