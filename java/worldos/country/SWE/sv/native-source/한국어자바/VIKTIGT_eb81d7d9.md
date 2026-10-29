# Svenska Java hjälpkomponent_värde bibliotek

OpenJDK 11 이상과 함께 쓰는 프로젝트 ägare_värde API다. 표준 Java bibliotek 전체의 번역판을 뜻하지 않는다. 기존 Java API·키워드·fel_31f743d2·자료형은 그대로 함께 쓴다.

전체 22개 hjälpkomponent_värde 메서드의 argument·반환값·제약, operativsystem 안의 사용법, Python·C++ 호출 방법은 **[Svenska bibliotek användare_guide](användare_guide.md)**에 정리했다. [Python 호출 예제](예제/다른언어/PYTHON_Samtal.py)와 [C++ JNI 호출 예제](예제/다른언어/자바호출.cpp)도 제공한다.

`make`로 `build/한국어자바.jar`를 만든다. `javac -encoding UTF-8 -cp build/한국어자바.jar 예제/인사.java`로 예제를 컴파일한다. 실행은 `java -cp build/한국어자바.jar:예제 인사`다.

`인사` 예제는 그래픽 화면이 없으면 filnamn·문자·스레드 결과와 안내만 출력한다. Swing 창은 그래픽 세션에서 실행해야 한다. QEMU에서는 [그래픽 köra_kommando VIKTIGT_eb81d7d9](../platforms/rpi4/README.md)의 `make run`으로 부팅한 BACK_värde VNC 데스크톱의 터미널을 사용한다.

| Kurs_värde | 제공 기능 |
|---|---|
| filnamn | UTF-8 텍스트·byte_värde Läs/Skriv, 디렉터리·post_ange |
| 문자 | UTF-8 KONVERTERA_värde, NFC normalisera_värde, KOD_värde 포인트 nummer, 언어별 낱말 gräns_värde |
| kommunikation | HTTP(S) begäran, 제한시간을 가진 TCP Anslut |
| 작업 | 스레드 Kör·합류·vänta_värde, 작업 app_Startbild |
| skärmbild | Swing 이벤트 처리와 Fönster generera |
| arbetsyta | källfil ändring_värde·kompilera_källa·köra_kommando·köra_kommando filnamn generera skärmbild |

`char`는 UTF-16 KOD_värde 단위이므로 이모지 등을 한 글자로 처리할 때 KOD_värde 포인트 또는 문자 gräns_värde API를 사용한다. 파일은 UTF-8로 저장한다. OpenJDK의 모든 Java2D/teckensnitt_värde/입력기 조합을 각각 검증한 것은 아니다.

이름은 aktuellt_objekt 의미가 분명한 Svenska 용례를 사용했다. 개별 명칭의 역사적 어원 검토를 완료했다고 주장하지 않는다. resurs_värde 종료와 fel_31f743d2 처리는 표준 API의 계약을 따른다.
