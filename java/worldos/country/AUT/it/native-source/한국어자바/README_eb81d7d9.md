# Italiano Java helper_VALORE Catalogo

OpenJDK 11 이상과 함께 쓰는 프로젝트 proprietario_VALORE API다. 표준 Java Catalogo 전체의 번역판을 뜻하지 않는다. 기존 Java API·키워드·eccezione·자료형은 그대로 함께 쓴다.

전체 22개 helper_VALORE 메서드의 argomenti·반환값·제약, sistema_operativo 안의 사용법, Python·C++ 호출 방법은 **[Italiano Catalogo USER_guida](USER_guida.md)**에 정리했다. [Python 호출 예제](예제/다른언어/PYTHON_Chiamate.py)와 [C++ JNI 호출 예제](예제/다른언어/자바호출.cpp)도 제공한다.

`make`로 `build/한국어자바.jar`를 만든다. `javac -encoding UTF-8 -cp build/한국어자바.jar 예제/messaggio_di_saluto_ae353e94.java`로 예제를 컴파일한다. 실행은 `java -cp build/한국어자바.jar:예제 messaggio_di_saluto_ae353e94`다.

`messaggio_di_saluto_ae353e94` 예제는 그래픽 화면이 없으면 file·문자·스레드 결과와 안내만 출력한다. Swing 창은 그래픽 세션에서 실행해야 한다. QEMU에서는 [그래픽 Esegui_comando README_eb81d7d9](../platforms/rpi4/README.md)의 `make run`으로 부팅한 BACK_VALORE VNC 데스크톱의 터미널을 사용한다.

| Corso_VALORE | 제공 기능 |
|---|---|
| file | UTF-8 텍스트·byte_VALORE Lettura/Scrittura, 디렉터리·voce_elenco |
| 문자 | UTF-8 CONVERTI_VALORE, NFC normalizzare_VALORE, CODICE_VALORE 포인트 numero, 언어별 낱말 limite_VALORE |
| comunicazione | HTTP(S) richiesta, 제한시간을 가진 TCP Connetti |
| 작업 | 스레드 avvia·합류·aspetta_VALORE, 작업 app_Launcher |
| schermata | Swing 이벤트 처리와 Finestra generare |
| area_di_lavoro | codiceSorgente Modifica_VALORE·compilare_fonte·Esegui_comando·Esegui_comando file generare schermata |

`char`는 UTF-16 CODICE_VALORE 단위이므로 이모지 등을 한 글자로 처리할 때 CODICE_VALORE 포인트 또는 문자 limite_VALORE API를 사용한다. 파일은 UTF-8로 저장한다. OpenJDK의 모든 Java2D/tipo_di_carattere_VALORE/입력기 조합을 각각 검증한 것은 아니다.

이름은 Regolari_articolo 의미가 분명한 Italiano 용례를 사용했다. 개별 명칭의 역사적 어원 검토를 완료했다고 주장하지 않는다. risorsa_VALORE 종료와 eccezione 처리는 표준 API의 계약을 따른다.
