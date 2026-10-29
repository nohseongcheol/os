# Ikinyarwanda Java 도우미 isomero

OpenJDK 11 이상과 함께 쓰는 프로젝트 nyirayo_agaciro API다. 표준 Java isomero 전체의 번역판을 뜻하지 않는다. 기존 Java API·키워드·예외·자료형은 그대로 함께 쓴다.

전체 22개 도우미 메서드의 인수·반환값·제약, sisitemu_ngengamikorere 안의 사용법, Python·C++ 호출 방법은 **[Ikinyarwanda isomero ukoresha_inyobora](ukoresha_inyobora.md)**에 정리했다. [Python 호출 예제](예제/다른언어/파이썬호출.py)와 [C++ JNI 호출 예제](예제/다른언어/자바호출.cpp)도 제공한다.

`make`로 `build/한국어자바.jar`를 만든다. `javac -encoding UTF-8 -cp build/한국어자바.jar 예제/인사.java`로 예제를 컴파일한다. 실행은 `java -cp build/한국어자바.jar:예제 인사`다.

`인사` 예제는 그래픽 화면이 없으면 Idosiye·문자·스레드 결과와 안내만 출력한다. Swing 창은 그래픽 세션에서 실행해야 한다. QEMU에서는 [그래픽 gukora_ibwiriza NSOMA_eb81d7d9](../platforms/rpi4/README.md)의 `make run`으로 부팅한 Ikibanza_agaciro VNC 데스크톱의 터미널을 사용한다.

| icyiciro_agaciro_55654bf1 | 제공 기능 |
|---|---|
| Idosiye | UTF-8 텍스트·bayiti_agaciro 읽기/kwandika, 디렉터리·icyinjizwa_Urutonde |
| 문자 | UTF-8 변환, NFC kuboneza_agaciro, 코드 포인트 수, 언어별 낱말 경계 |
| 통신 | HTTP(S) 요청, 제한시간을 가진 TCP Guhuza |
| 작업 | 스레드 ihuriro·합류·대기, 작업 porogaramu_umukozi |
| 화면 | Swing 이벤트 처리와 idirishya 생성 |
| imbuga_y_akazi | Inkomoko guhindura_agaciro·gusohora_inkomoko·gukora_ibwiriza·gukora_ibwiriza Idosiye 생성 화면 |

`char`는 UTF-16 코드 단위이므로 이모지 등을 한 글자로 처리할 때 코드 포인트 또는 문자 경계 API를 사용한다. 파일은 UTF-8로 저장한다. OpenJDK의 모든 Java2D/imyandikire_agaciro/입력기 조합을 각각 검증한 것은 아니다.

이름은 현재 의미가 분명한 Ikinyarwanda 용례를 사용했다. 개별 명칭의 역사적 어원 검토를 완료했다고 주장하지 않는다. umutungo_agaciro 종료와 예외 처리는 표준 API의 계약을 따른다.
