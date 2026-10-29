# Dansk Java hjælper_VÆRDI bibliotek

OpenJDK 11 이상과 함께 쓰는 프로젝트 ejer_VÆRDI API다. 표준 Java bibliotek 전체의 번역판을 뜻하지 않는다. 기존 Java API·키워드·undtagelse·자료형은 그대로 함께 쓴다.

전체 22개 hjælper_VÆRDI 메서드의 Argumenter·반환값·제약, operativsystem 안의 사용법, Python·C++ 호출 방법은 **[Dansk bibliotek bruger_guide](bruger_guide.md)**에 정리했다. [Python 호출 예제](예제/다른언어/PYTHON_Opkald.py)와 [C++ JNI 호출 예제](예제/다른언어/자바호출.cpp)도 제공한다.

`make`로 `build/한국어자바.jar`를 만든다. `javac -encoding UTF-8 -cp build/한국어자바.jar 예제/인사.java`로 예제를 컴파일한다. 실행은 `java -cp build/한국어자바.jar:예제 인사`다.

`인사` 예제는 그래픽 화면이 없으면 Fil·문자·스레드 결과와 안내만 출력한다. Swing 창은 그래픽 세션에서 실행해야 한다. QEMU에서는 [그래픽 Udfør_kommando Vigtigt_eb81d7d9](../platforms/rpi4/README.md)의 `make run`으로 부팅한 BACK_VÆRDI VNC 데스크톱의 터미널을 사용한다.

| Hold_VÆRDI | 제공 기능 |
|---|---|
| Fil | UTF-8 텍스트·byte_VÆRDI Læse/Skrive, 디렉터리·post_Liste |
| 문자 | UTF-8 KONVERTER_VÆRDI, NFC normalisere_VÆRDI, KODE_VÆRDI 포인트 tal, 언어별 낱말 grænse_VÆRDI |
| 통신 | HTTP(S) anmodning, 제한시간을 가진 TCP Tilslut |
| 작업 | 스레드 Kør_2·합류·vent_VÆRDI, 작업 app_Kvikstart |
| skærmbillede | Swing 이벤트 처리와 Vindue generere |
| arbejdsområde | KILDE Rediger_VÆRDI·kompilere_kilde·Udfør_kommando·Udfør_kommando Fil generere skærmbillede |

`char`는 UTF-16 KODE_VÆRDI 단위이므로 이모지 등을 한 글자로 처리할 때 KODE_VÆRDI 포인트 또는 문자 grænse_VÆRDI API를 사용한다. 파일은 UTF-8로 저장한다. OpenJDK의 모든 Java2D/skrifttype_VÆRDI/입력기 조합을 각각 검증한 것은 아니다.

이름은 aktuel_vare 의미가 분명한 Dansk 용례를 사용했다. 개별 명칭의 역사적 어원 검토를 완료했다고 주장하지 않는다. ressource_VÆRDI 종료와 undtagelse 처리는 표준 API의 계약을 따른다.
