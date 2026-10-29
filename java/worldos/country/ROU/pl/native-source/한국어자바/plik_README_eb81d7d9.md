# polski Java pomocnik_WARTOŚĆ biblioteka

OpenJDK 11 이상과 함께 쓰는 프로젝트 właściciel_WARTOŚĆ API다. 표준 Java biblioteka 전체의 번역판을 뜻하지 않는다. 기존 Java API·키워드·wyjątek·자료형은 그대로 함께 쓴다.

전체 22개 pomocnik_WARTOŚĆ 메서드의 argumenty·반환값·제약, system_operacyjny 안의 사용법, Python·C++ 호출 방법은 **[polski biblioteka użytkownik_prowadnica](użytkownik_prowadnica.md)**에 정리했다. [Python 호출 예제](예제/다른언어/PYTHON_Połączenia.py)와 [C++ JNI 호출 예제](예제/다른언어/자바호출.cpp)도 제공한다.

`make`로 `build/한국어자바.jar`를 만든다. `javac -encoding UTF-8 -cp build/한국어자바.jar 예제/인사.java`로 예제를 컴파일한다. 실행은 `java -cp build/한국어자바.jar:예제 인사`다.

`인사` 예제는 그래픽 화면이 없으면 nazwa_pliku·문자·스레드 결과와 안내만 출력한다. Swing 창은 그래픽 세션에서 실행해야 한다. QEMU에서는 [그래픽 Wykonaj_polecenie plik_README_eb81d7d9](../platforms/rpi4/README.md)의 `make run`으로 부팅한 BACK_WARTOŚĆ VNC 데스크톱의 터미널을 사용한다.

| Klasa_WARTOŚĆ | 제공 기능 |
|---|---|
| nazwa_pliku | UTF-8 텍스트·bajt_WARTOŚĆ Odczyt/Zapis, 디렉터리·wpis_Lista |
| 문자 | UTF-8 KONWERTUJ_WARTOŚĆ, NFC normalizować_WARTOŚĆ, KOD_WARTOŚĆ 포인트 identyfikator, 언어별 낱말 granica_WARTOŚĆ |
| komunikacja | HTTP(S) żądanie, 제한시간을 가진 TCP Połącz |
| 작업 | 스레드 Uruchom_2·합류·chwileczkę_WARTOŚĆ, 작업 program_Launcher |
| 화면 | Swing 이벤트 처리와 Okno generować |
| obszar_roboczy | plik_źródłowy Edytuj_WARTOŚĆ·kompilować_źródło·Wykonaj_polecenie·Wykonaj_polecenie nazwa_pliku generować 화면 |

`char`는 UTF-16 KOD_WARTOŚĆ 단위이므로 이모지 등을 한 글자로 처리할 때 KOD_WARTOŚĆ 포인트 또는 문자 granica_WARTOŚĆ API를 사용한다. 파일은 UTF-8로 저장한다. OpenJDK의 모든 Java2D/czcionka_WARTOŚĆ/입력기 조합을 각각 검증한 것은 아니다.

이름은 bieżący_towar 의미가 분명한 polski 용례를 사용했다. 개별 명칭의 역사적 어원 검토를 완료했다고 주장하지 않는다. zasób_WARTOŚĆ 종료와 wyjątek 처리는 표준 API의 계약을 따른다.
