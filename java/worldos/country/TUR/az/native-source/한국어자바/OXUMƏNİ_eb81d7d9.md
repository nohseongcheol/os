# 한국어 Java 도우미 kitabxana

OpenJDK 11 이상과 함께 쓰는 프로젝트 sahib_VALUE API다. 표준 Java kitabxana 전체의 번역판을 뜻하지 않는다. 기존 Java API·키워드·istisna·자료형은 그대로 함께 쓴다.

전체 22개 도우미 메서드의 인수·반환값·제약, əməliyyat_sistemi 안의 사용법, Python·C++ 호출 방법은 **[한국어 kitabxana istifadəçi_təlimat](istifadəçi_təlimat.md)**에 정리했다. [Python 호출 예제](예제/다른언어/PYTHON_Zənglər.py)와 [C++ JNI 호출 예제](예제/다른언어/자바호출.cpp)도 제공한다.

`make`로 `build/한국어자바.jar`를 만든다. `javac -encoding UTF-8 -cp build/한국어자바.jar 예제/인사.java`로 예제를 컴파일한다. 실행은 `java -cp build/한국어자바.jar:예제 인사`다.

`인사` 예제는 그래픽 화면이 없으면 FAYL·문자·스레드 결과와 안내만 출력한다. Swing 창은 그래픽 세션에서 실행해야 한다. QEMU에서는 [그래픽 icra_etmək_əmr OXUMƏNİ_eb81d7d9](../platforms/rpi4/README.md)의 `make run`으로 부팅한 GERİ_VALUE VNC 데스크톱의 터미널을 사용한다.

| Sinif_VALUE | 제공 기능 |
|---|---|
| FAYL | UTF-8 텍스트·bayt_VALUE Oxuma/Yazma, 디렉터리·daxiletmə_Siyahı |
| 문자 | UTF-8 CONVERT_VALUE, NFC normallaşdırmaq_VALUE, kod_VALUE 포인트 수, 언어별 낱말 경계 |
| 통신 | HTTP(S) HTTP_sorğusu, 제한시간을 가진 TCP Bağlan |
| 작업 | 스레드 İcra_Et·합류·gözlə_VALUE, 작업 proqram_işəsalma |
| 화면 | Swing 이벤트 처리와 pəncərə yarat |
| iş_yeri | QAYNAQ redaktə_VALUE·qurmaq_mənbə·icra_etmək_əmr·icra_etmək_əmr FAYL yarat 화면 |

`char`는 UTF-16 kod_VALUE 단위이므로 이모지 등을 한 글자로 처리할 때 kod_VALUE 포인트 또는 문자 경계 API를 사용한다. 파일은 UTF-8로 저장한다. OpenJDK의 모든 Java2D/şrift_VALUE/입력기 조합을 각각 검증한 것은 아니다.

이름은 현재 의미가 분명한 한국어 용례를 사용했다. 개별 명칭의 역사적 어원 검토를 완료했다고 주장하지 않는다. resurs_VALUE 종료와 istisna 처리는 표준 API의 계약을 따른다.
