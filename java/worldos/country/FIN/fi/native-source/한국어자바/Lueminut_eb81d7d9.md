# suomi Java apuosa_ARVO kirjasto

OpenJDK 11 이상과 함께 쓰는 프로젝트 omistaja_ARVO API다. 표준 Java kirjasto 전체의 번역판을 뜻하지 않는다. 기존 Java API·키워드·poikkeus·자료형은 그대로 함께 쓴다.

전체 22개 apuosa_ARVO 메서드의 argumentit·반환값·제약, käyttöjärjestelmä 안의 사용법, Python·C++ 호출 방법은 **[suomi kirjasto käyttäjä_opas](käyttäjä_opas.md)**에 정리했다. [Python 호출 예제](예제/다른언어/PYTHON_Puhelut.py)와 [C++ JNI 호출 예제](예제/다른언어/자바호출.cpp)도 제공한다.

`make`로 `build/한국어자바.jar`를 만든다. `javac -encoding UTF-8 -cp build/한국어자바.jar 예제/인사.java`로 예제를 컴파일한다. 실행은 `java -cp build/한국어자바.jar:예제 인사`다.

`인사` 예제는 그래픽 화면이 없으면 tiedoston_nimi·문자·스레드 결과와 안내만 출력한다. Swing 창은 그래픽 세션에서 실행해야 한다. QEMU에서는 [그래픽 Suorita_komento Lueminut_eb81d7d9](../platforms/rpi4/README.md)의 `make run`으로 부팅한 BACK_ARVO VNC 데스크톱의 터미널을 사용한다.

| Luokka_ARVO | 제공 기능 |
|---|---|
| tiedoston_nimi | UTF-8 텍스트·tavu_ARVO Luku/Kirjoitus, 디렉터리·merkintä_luettelo |
| 문자 | UTF-8 MUUNNA_ARVO, NFC normalisoida_ARVO, KOODI_ARVO 포인트 numero, 언어별 낱말 rajattu_alue_ARVO |
| 통신 | HTTP(S) pyyntö, 제한시간을 가진 TCP Yhdistä |
| 작업 | 스레드 Suorita_2·합류·odottaa_ARVO, 작업 ohjelma_sovellusvalikko |
| 화면 | Swing 이벤트 처리와 Ikkuna generoida |
| työtila | lähdetiedosto muutos_ARVO·kääntää_lähde·Suorita_komento·Suorita_komento tiedoston_nimi generoida 화면 |

`char`는 UTF-16 KOODI_ARVO 단위이므로 이모지 등을 한 글자로 처리할 때 KOODI_ARVO 포인트 또는 문자 rajattu_alue_ARVO API를 사용한다. 파일은 UTF-8로 저장한다. OpenJDK의 모든 Java2D/fontti_ARVO/입력기 조합을 각각 검증한 것은 아니다.

이름은 nykyinen_kohde 의미가 분명한 suomi 용례를 사용했다. 개별 명칭의 역사적 어원 검토를 완료했다고 주장하지 않는다. resurssi_ARVO 종료와 poikkeus 처리는 표준 API의 계약을 따른다.
