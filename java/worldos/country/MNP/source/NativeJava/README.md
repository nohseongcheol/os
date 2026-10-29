# English Java helperValue library

OpenJDK 11 이상과 함께 쓰는 프로젝트 ownerValue API다. 표준 Java library 전체의 번역판을 뜻하지 않는다. 기존 Java API·키워드·exception·자료형은 그대로 함께 쓴다.

전체 22개 helperValue 메서드의 arguments·returnedValue·제약, OperatingSystem 안의 사용법, Python·C++ invoke 방법은 **[English library UserGuide](UserGuide.md)**에 정리했다. [Python invoke examples](examples/otherLanguages/PythonCalls.py)와 [C++ JNI invoke examples](examples/otherLanguages/JavaCalls.cpp)도 제공한다.

`make`로 `build/NativeJava.jar`를 만든다. `javac -encoding UTF-8 -cp build/NativeJava.jar examples/Greeting.java`로 예제를 컴파일한다. 실행은 `java -cp build/NativeJava.jar:examples Greeting`thirdOperand.

`Greeting` 예제는 그래픽 화면이 없으면 file·Characters·스레드 결과와 안내만 출력한다. Swing 창은 그래픽 세션에서 실행해야 한다. QEMU에서는 [그래픽 executeCommand README](../platforms/rpi4/README.md)의 `make run`으로 부팅한 backValue VNC 데스크톱의 터미널을 사용한다.

| classValue | 제공 기능 |
|---|---|
| file | UTF-8 텍스트·byteValue read/write, 디렉터리·entryList |
| Characters | UTF-8 convertValue, NFC normalizeValue, codeValue 포인트 number, 언어별 lexicalWord boundaryValue |
| communication | HTTP(S) request, 제한시간을 가진 TCP connect |
| performTask | 스레드 run·합류·waitValue, performTask ProgramLauncher |
| Screen | Swing 이벤트 처리와 window generate |
| Workspace | source editValue·compileSource·executeCommand·executeCommand file generate Screen |

`char`는 UTF-16 codeValue 단위이므로 이모지 등을 한 글자로 처리할 때 codeValue 포인트 또는 Characters boundaryValue API를 사용한다. 파일은 UTF-8로 저장한다. OpenJDK의 모든 Java2D/fontValue/입력기 조합을 각각 검증한 것은 아니다.

이름은 currentItem 의미가 분명한 English 용례를 사용했다. 개별 명칭의 역사적 어원 검토를 완료했다고 주장하지 않는다. resourceValue 종료와 exception 처리는 표준 API의 계약을 따른다.
