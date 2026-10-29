# Melayu Java 도우미 pustaka

OpenJDK 11 이상과 함께 쓰는 프로젝트 pemilik_VALUE API다. 표준 Java pustaka 전체의 번역판을 뜻하지 않는다. 기존 Java API·키워드·pengecualian·자료형은 그대로 함께 쓴다.

전체 22개 도우미 메서드의 인수·반환값·제약, sistem_pengendalian 안의 사용법, Python·C++ 호출 방법은 **[Melayu pustaka pengguna_panduan](pengguna_panduan.md)**에 정리했다. [Python 호출 예제](예제/다른언어/PYTHON_Panggilan.py)와 [C++ JNI 호출 예제](예제/다른언어/자바호출.cpp)도 제공한다.

`make`로 `build/한국어자바.jar`를 만든다. `javac -encoding UTF-8 -cp build/한국어자바.jar 예제/인사.java`로 예제를 컴파일한다. 실행은 `java -cp build/한국어자바.jar:예제 인사`다.

`인사` 예제는 그래픽 화면이 없으면 Fail·문자·스레드 결과와 안내만 출력한다. Swing 창은 그래픽 세션에서 실행해야 한다. QEMU에서는 [그래픽 laksanakan_perintah README_eb81d7d9](../platforms/rpi4/README.md)의 `make run`으로 부팅한 BACK_VALUE VNC 데스크톱의 터미널을 사용한다.

| Kelas_VALUE | 제공 기능 |
|---|---|
| Fail | UTF-8 텍스트·bait_VALUE Baca/Tulis, 디렉터리·pemasukan_Senarai |
| 문자 | UTF-8 tukar_VALUE, NFC menormalkan_VALUE, kod_VALUE 포인트 수, 언어별 낱말 경계 |
| 통신 | HTTP(S) permintaan, 제한시간을 가진 TCP Sambung |
| 작업 | 스레드 Jalan·합류·tunggu_VALUE, 작업 aplikasi_pelancar |
| 화면 | Swing 이벤트 처리와 Tetingkap jana |
| ruang_kerja | SUMBER edit_VALUE·bina_sumber·laksanakan_perintah·laksanakan_perintah Fail jana 화면 |

`char`는 UTF-16 kod_VALUE 단위이므로 이모지 등을 한 글자로 처리할 때 kod_VALUE 포인트 또는 문자 경계 API를 사용한다. 파일은 UTF-8로 저장한다. OpenJDK의 모든 Java2D/fon_VALUE/입력기 조합을 각각 검증한 것은 아니다.

이름은 현재 의미가 분명한 Melayu 용례를 사용했다. 개별 명칭의 역사적 어원 검토를 완료했다고 주장하지 않는다. sumber_VALUE 종료와 pengecualian 처리는 표준 API의 계약을 따른다.
