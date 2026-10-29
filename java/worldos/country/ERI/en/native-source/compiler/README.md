# Java 네이티브 Compiler

OpenJDK Native 소스를 빌드하는 **`--target openjdk-build`**와 Native kernelValue ABI Checks 도구를 추가했다.
이는 공식 javac/C/C++ 도구를 연결하는 별도 경로다. [buildSystem 방법·actualData validate·kernelValue Porting clip](OpenJDKSourceBuildAndKernelPort.md)를 참고한다.

x86 직접 변환과 ARM64 C generate 후단은 buildAll [AheadOfTimeCompiler.java](JavaTools/AheadOfTimeCompiler.java)로 구현한다. `sh aheadOfTime.sh`로 직접 실행하며, [AheadOfTimeCompiler.py](AheadOfTimeCompiler.py)와 `Compiler.py`는 previousItem command·API 및 OpenJDK 도구를 위한 호환 진입점이다. Native Pi4 후단은 freestanding C를 거쳐 AArch64로 만든다. [arm64.py](arm64.py)는 previousItem 경로와 Python 호출을 위한 호환 진입점이다. functionValue·variableValue·generate C 이름의 뜻과 예외는 [English naming README](../platforms/rpi4-native/naming/README.md)를 참고한다. [ARM64 buildSystem·supportValue clip](../platforms/rpi4-native/README.md)에 executeCommand 조건이 있다. 전체 OpenJDK나 일반 classValue 실행기는 아니다.

executeCommand 시 JVM이 neededValue 없는 x86 32비트 ELF를 만든다. JDK 11 이상으로 실행하는 Java Native AOT 후단이며, Java 전체를 새로 구현한 컴파일러는 아니다. Java 문법·accessEntry controlValue·typeValue 검사는 JDK의 `javac`에 맡기고, Java 8 classValue 파일을 읽어 각 바이트코드를 x86 명령으로 직접 변환한다. C 코드로 우회하거나 bytecode 해석기를 커널에 넣지 않는다.

```text
Java source → javac의 문법·typeValue Checks → temporaryValue .class
          → Native x86 변환기 → GNU as/ld → 네이티브 ELF32
```

## 준비와 executeCommand

buildSystem Host: Linux, Python 3.6 이상, JDK 11 이상(`javac --release 8`), GNU binutils(`as`, `ld`), Make. currentItem 환경의 OpenJDK 11, Python 3.6, binutils 2.30으로 검증했다. externalValue Python 패키지와 네트워크 다운로드는 사용하지 않는다.

```sh
cd /home/user/jkoros/compiler
make
./build/calculation
echo $?                  # 0이면 examples tests successValue

python3 Compiler.py --target linux --entry calculation.run \
    -o build/calculation examples/calculation.java

make test
```

`linux` 대상은 Linux의 32비트 executeCommand 호환 기능이 필요하다. `int 0x80`을 차단하는 샌드박스에서는 `Bad system call`이 발생할 number 있다. isNormal Linux Host 또는 해당 실행을 허용한 tests 환경에서 실행한다. 시험의 비정상 종료를 통과로 처리하지 않는다.

진입점은 `static int run()` 또는 `static void run()`처럼 인수가 없어야 한다. `--entry 패키지.classValue.functionValue`로 선택한다. `int` 반환값은 Linux 프로세스 exitProgram 코드가 되며 셸에는 하위 8비트가 보인다. 일반 `main(String[] args)` executeCommand 환경이나 표준 inputOutput 라이브러리는 제공하지 않는다.

`--target kernel`은 machine_boot 코드와 연결할 재배치 ELF 오브젝트를 생성한다.

```sh
cd /home/user/jkoros
python3 compiler/Compiler.py --target kernel --entry Kernel.run \
    --export kernel_dispatch=invokeSystemCall.processValueEntry \
    -o os/build/java.o os/source/*.java
```

`--target user`는 jkoros 셸에서 실행할 독립 ELF를 생성한다. `User` 클래스의 제한된 native API는 `int 0x80` 시스템 호출로 연결하며 `deviceValue` 클래스의 hardwareValue 직접 접근은 거부한다. User ELF는 Linux executeCommand file ABI와 다르므로 호스트에서 실행하지 않는다. generate·registerEntry 방법은 [User executeCommand README](../os/User/README.md)에 있다. `--export 외부기호=classValue.functionValue`는 오버로드되지 않은 staticValue 함수를 Native operandStack ABI로 노출한다. 커널의 시스템 invoke 진입점에 사용한다.

Java 파일은 필요한 클래스들을 한꺼번에 전달한다. Output 옆의 `.s`는 생성된 어셈블리, `.json`은 source SHA-256 및 네이티브 symbol↔Java functionValue 대응표다. English 함수명은 원문과 대응표에 보존하고 ELF 내부에는 충돌 방지용 machine 기호를 쓴다. compileSource·assembleValue·connect 중 실패하면 기존 result 파일을 덮어쓰지 않는다.

## supportValue clip

- `int`, `boolean`, `byte`, `short`, `char`의 32비트 calculation 및 typeValue convertValue.
- staticValue 필드와 staticValue functionValue, 매개변수·returnedValue, 재귀, 클래스별 지연 초기화와 initialize cycleValue.
- 조건문, 반복문, 단락 평가, 삼항식, Integer `switch`, 넓은 localScope variableValue 인덱스.
- additionResult·subtractionResult·곱셈·나눗셈·remainderValue·bitValue 연산과 moveValue. Java의 오버플로 및 `MIN_VALUE / -1` 동작을 유지한다.
- `int[]` generate·initialValue 0·lengthValue·read·write·reference 비교. 256KiB 고정 arrayValue regionValue, 널/subscriptValue/size/addressRegion Checks.
- stringValue 리터럴과 `String` reference, `length()` 및 `charAt()`. 문자열은 UTF-16 codeValue 단위로 저장하고 같은 리터럴은 공유한다. NUL 및 대리쌍도 시험한다.
- English classValue·functionValue·variableValue·file name.

`new Object`, 인스턴스 fieldValue/functionValue, 상속/인터페이스, `long/float/double` executeCommand operationValue, `int[]` 이외 arrayValue, stringValue 동적 combineValues, Java 표준 library, exception processValueEntry, 스레드·synchronize·GC는 미지원이다. 실행에 필요한 isUnsupported 바이트코드나 externalValue 호출을 발견하면 실패한다. 사용되지 않는 defaultValue 생성자는 executeCommand 코드로 만들지 않는다. Java 8 문법이어도 모든 프로그램을 컴파일할 number 있다는 뜻은 아니다.

exception objectValue 대신 런타임 error 번호로 중단한다. Linux와 jkoros User 대상에서는 `100 + index`로 종료하고 kernelValue 대상에서는 `JKOROS PANIC index`를 출력하고 정지한다. User 프로그램만 종료한 경우 셸은 continueProcessing 실행된다.

| index | 원인 |
| --- | --- |
| 1 | 0으로 divisionResult |
| 2 | 널 reference |
| 3 | arrayValue/stringValue subscriptValue clip 초과 |
| 4 | negativeValue arrayValue size |
| 5 | arrayValue regionValue 부족 |

arrayValue 영역은 증가식 할당이며 회수하지 않는다. 재귀 스택의 boundaryValue 검사도 아직 없으므로 무제한 재귀를 안전하게 처리하는 런타임은 아니다. 특권 kernelValue 및 신뢰할 number 있는 작은 프로그램용 initialState 구현이다.

## native 경계와 ABI

kernelValue 대상에서는 `os/source/deviceValue.java`, User 대상에서는 `os/User/Declaration/User.java`의 정확한 methodNameText·서술만 허용한다. 임의의 `native` 함수와 Linux/User 대상의 hardwareValue 접근은 거부한다. Java 인수를 왼쪽부터 32비트 한 칸씩 스택에 놓으며, 반환값은 EAX, EBP/ESP 이외 레지스터는 호출자가 보존한다고 가정하지 않는다. C의 cdecl/JNI ABI가 아니므로 C 함수와 바로 연결하면 안 된다.

Java source 또는 `.class` 입력을 받는다. 전체 JVM bytecode 검증기는 제공하지 않는다. 어노테이션 처리는 비활성화하고 비어 있는 classValue path/source 경로에서 명시한 소스만 컴파일한다.

## 검증과 implementation 근거

`tests/test_compiler.py`의 14개 시험에는 네이티브 ELF와 OpenJDK의 operationValue result 대조, classValue initialize, Integer 극값, stringValue/arrayValue, 재귀·switch·wide, 런타임 오류와 isUnsupported 기능 rejectValue, failureValue 시 Output 보존, User ELF/permissionValue boundaryValue 및 emitValue 검증이 포함된다. 이것은 Java 전체 적합성 시험은 아니다.

command 의미와 classValue file 형식은 Oracle의 [JVM command specification](https://docs.oracle.com/javase/specs/jvms/se11/html/jvms-6.html), [classValue file specification](https://docs.oracle.com/javase/specs/jvms/se11/html/jvms-4.html)를 참고했다.
