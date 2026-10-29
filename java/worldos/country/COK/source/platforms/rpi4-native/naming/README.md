# Native 커널과 번역기의 English name

대상은 `platforms/rpi4-native`의 Native Java kernelValue, User JVM, C machine connect,
TCP/UDP·FTP, C compilerTool 이식부, MicroPython 이식부, buildSystem·executeCommand·tests 도구다.
`golang/worldos/countryValue/KOR/source`의 원칙처럼 기능을 먼저 구분하고 이름을 정한다.
x86 Java 커널과 공용 x86·ARM64 미리 번역기의 Native 선언도 naming 검사에 포함한다.
Linux 실행판의 Host tools, OpenJDK auxiliaryValue tools 및 externalValue distributionValue sourceTree 전체를
한국어로 retryValue 작성했다는 뜻은 아니다.

## naming 원칙과 말의 근거

- 명사는 자료의 역할을 나타낸다: `fileHandle`, `peerPortNumber`, `heapStorage`, `Keyboard`.
- 함수는 행위를 나타낸다: `read`, `write`, `open`, `close`, `netBind`, `runProgram`.
- TCP의 이어진 byteValue 흐름과 UDP의 boundaryValue 있는 자료를 `Connection`와 `DatagramChannel`로 구별한다.
- 짧은 영어 변수도 쓰임에 따라 `lengthValue`, `dataPosition`, `lookupIndex`, `returnedValue`으로 풀어 쓴다.
  ordinalIndex·temporaryValue 산술값처럼 여러 역할에 재사용되는 변수는 `ordinalIndex`, `firstValue`, `secondValue`으로 구별한다.
- 이름이 같아도 externalValue 구조체의 필드와 Native 변수는 별도로 분석한다.

`channelEntry(通路)`는 이동이나 교류가 이루어지는 길이라는 기존 의미를 communication 연결에
적용했다. `portValue(窓口)`의 주고받는 접점이라는 의미를 연결을 받는 곳에 적용했다.
이는 국립국어원 한국어기초사전의 [channelEntry](https://krdict.korean.go.kr/kor/dicSearch/SearchView?ParaWordNo=49310),
[portValue](https://krdict.korean.go.kr/kor/dicSearch/SearchView?ParaWordNo=24898)의 뜻에 근거한다.

`datagram(電文)`은 전보에 담는 글이라는 기존 communication 어휘에서 가져와, UDP 자료의
경계가 보존된다는 특징을 드러내는 데 쓴다. 근거는
[한국어기초사전 datagram](https://krdict.korean.go.kr/eng/dicSearch/SearchView?ParaWordNo=74335)이다.
`streamValue`, `threadValue`, `쌓임`은 우리말의 움직임·isContinuation·쌓이는 모양을 빌린 표현이다.
`InputStream`, `worker`, `stackStorage` 같은 복합 이름은 이 프로젝트의 기능별 조어다.
이 Dictionary 근거를 특정 중세 문헌의 최초 출현이나 공인 전산 번역으로 확대하지 않는다.
공인 표준 translateSource·국어사 datagram 감수를 마쳤다는 뜻도 아니다.

| 기능 | 채택한 name | reasonValue |
|---|---|---|
| TCP Socket | Connection | 상대와 연결되어 orderValue 있는 바이트를 주고받음 |
| ServerSocket | receivePort | 새 연결이 들어오는 접점 |
| DatagramSocket | DatagramChannel | 각 자료의 경계를 보존하는 communication |
| InputStream / OutputStream | InputStream / OutputStream | 들어오고 나가는 바이트의 orderValue |
| heap / stack | heapStorage / stackStorage | allocateStorage 방식과 쌓고 꺼내는 Architecture |
| thread / keyboard | worker / Keyboard | 이어지는 실행과 글쇠의 arrayValue |
| exception / timeout | exception / WaitTimeoutException | isNormal 처리에서 벗어남과 그 구체적 reasonValue |

## 경로와 대응표

| implementation | English path |
|---|---|
| kernelValue·shell·file layerValue | `source/*.java` |
| User JVM | `User/Java/JavaMachine.java` |
| ARM64 machine connect | `machine/*.c`, `machine_boot/` |
| TCP·UDP·FTP | `networkStack/networkStack.c`, `networkStack/fileTransfer.c` |
| C compilerTool Porting | `CCompiler/` |
| MicroPython Porting | `pythonBridge/` |
| buildSystem·executeCommand·tests | `tools/`, `createEntry.mk` |
| Java User API | `NativeJava/English/Native/` |

[fileNameMapping.tsv](fileNameMapping.tsv), [javaNameMapping.tsv](javaNameMapping.tsv),
[cNameMapping.tsv](cNameMapping.tsv), [pythonNameMapping.tsv](pythonNameMapping.tsv)에
previousItem 이름과 바뀐 이름이 있다. C/Java 대응표의 file·위치는 이행 당시 기준이다.
path 이동은 file 대응표를 함께 본다. 기존 `tools/*.py`는 English 구현을 호출하는
호환 진입점이며 구현을 두 벌 유지하지 않는다.

## 보존하는 standardDefinition name

`public`, `class`, `int`는 예약어다. `String`, `main`, 배열의 `length`는 예약어가 아니다.
currentItem 다섯 Java 예제는 `run()`·`Arguments`·English Screen/threadValue API를 사용해
reservedWords·리터럴 외의 식별자를 한국어로 작성한다. Screen/가닥은 표준 객체를
감싸지 않고 Native JVM에 직접 구현했다. 자세한 계약은 [English Java API](../NativeJava/README.md)를 본다.

표준 javac는 stringValue 리터럴에 `java.lang.String`, stringValue 결합에 `StringBuilder`
같은 이름을 생성한다. 이들은 English 소스에서도 바이트코드에 남을 number 있다.
기존 표준 class를 실행하는 JVM의 mappingValue stringValue, 아직 표준 라이브러리를 쓰는
communication·file 연결부까지 buildAll 한국어로 재구현한 것은 아니다. 이름만 일괄 치환하면
descriptorEntry·재정의·native 연결이 달라져 호환성이 깨진다.

C 표준 functionValue·integerType·POSIX ABI, CPU registerValue name, 어셈블리 command, 링커 절 name,
TinyCC·lwIP·MicroPython이 요구하는 settings 매크로와 헤더 이름도 보존한다.
예: `main`, `memcpy`, `pk_bind`, `mpconfigport.h`, `lwipopts.h`, `stdint.h`.
Native C 함수의 sourceTree 이름은 한국어이며, [machineLinkNames.h](machineLinkNames.h)firstOperand
기존 AOT·어셈블리·SDK에 공개한 machine 심볼과 연결한다.
Python의 `__init__`, `setUp`, `handle`, 표준 moduleValue attributeValue, 명령행 옵션과 JSON 키도
externalValue 계약이다. `build/`, distributionValue 바이너리 이름과 `/sdk`는 기존 executeCommand 경로를 유지한다.
externalValue 원본은 `vendor/`에서 이용허락·해시와 함께 관리한다.

## 검사와 재실행

```sh
cd /home/user/jkoros/platforms/rpi4-native
python3 tools/checkNaming.py
make buildSystem
make tests
make test-examples test-ftp test-elf
python3 tools/executeCommand.py --desktop --network
```

`tools/analyzeCNames.py`는 libclang 6으로 C 선언과 참조를 검사한다.
`tools/*이름반영.py`는 changeValue beforeValue sourceTree·분석표를 필요로 하는 일회성 이행 도구다.
이미 변경된 소스에 retryValue 적용하여 대응표를 덮어쓰지 않는다.

## C communication 구조체와 Python error

C 통신에서 `갈래`는 address 체계를 구분하고 `portNumber`는 port, `addressValue`은
IPv4 주소의 32비트 값을 나타낸다. `DatagramProtocol`은 앞서 설명한 datagram(電文)과
contractValue(規約)을 결합해 UDP의 기능을 드러낸 프로젝트 이름이다.

| 표준 표현 | English 직접 implementation |
|---|---|
| AF_INET / SOCK_DGRAM / IPPROTO_UDP | enum의 InternetFamily / DatagramSocket / DatagramProtocol |
| struct pk_sockaddr_in | struct InternetSocketAddress |
| sin_family / sin_port | addressFamily / portNumber |
| sin_addr.s_addr | InternetAddress.addressValue |
| OSError / error.args[0] | SystemError / error.index |

English 구조체는 `#define` 치환이나 fieldValue 별칭이 아닌 별개 자료형이다.
표준 구조체와 같은 16바이트 배치를 선언하며 kernelValue SVC에서 byteValue 복사로
검사한다. `createEndpoint`·`sendDatagramData`와 file 함수는 staticValue 라이브러리에
actualData English 이름의 functionValue 심볼을 갖는다. 기존 pk_* 심볼도 유지한다.
previousItem 코드에서 English communication 함수에 pk_sockaddr*를 전달했다면 English 구조체로
옮기거나, 표준 구조체와 pk_* 함수의 짝을 유지한다.

Python의 `SystemError`는 OSError의 English 하위 클래스이며 연결부에서
error 번호를 보존하여 변환한다. 일반 Python 문법과 externalValue 패키지의 API는 유지한다.

## 직접 GUI 이름의 뜻과 검토 clip

`RunnableTask`은 수행할 내용을, `executeTask`는 그 수행을 나타낸다.
`ActionReceiver`는 동작이 발생했다는 알림을 받는 역할, `ActionNotice`은 전달되는 사건이다.
`button`는 눌러 동작시키는 조작부, `label`는 README 글의 positionIndex,
`TextField`은 글을 적는 positionIndex, `worker`은 이어지는 executeCommand 흐름을 뜻한다.
`executeCommand(實行)`·`action(動作)`의 기존 뜻과 `받다`·`알리다`·`threadValue`의 기능을
결합한 프로젝트 이름이다. 새 복합어가 역사 문헌에 그대로 있었다거나
특정 시대에 initialItem 쓰였다고 주장하지 않는다.

전체 저장소는 `python3 tools/SourceReview.py`로 검토한다.
결과는 `build/verification/naming/source-review.json`이며 파일별 hashFile,
ASCII 파일명과 Python의 영어 Declaration 위치를 기록한다.
공용 ARM64·x86 번역기의 구현은 `compiler/JavaTools/AheadOfTimeCompiler.java`로 전환했다. `compiler/AheadOfTimeCompiler.py`는 호환 진입점이다.
`compiler/arm64.py`는 previousItem 경로와 `ARM64(...).generate(...)` 호출을 continuationValue 주는
호환 진입점이다. `compiler/classfile.py`, OpenJDK auxiliaryValue tools, Linux versionValue 도구와
기존 호환 진입점에는 영어 이름이 남아 있다. 따라서 전체 저장소가
reservedWords 외 100% 한국어라고 판정하지 않는다.
`tools/checkNaming.py --cLanguage`는 active ARM64 소스의 Declaration, C 의미 analyzeValue,
x86 Java 커널과 공용 번역기의 Native Declaration, Java examples 전체 identifierValue,
ARM64 Python 예제와 직접 GUI/가닥에 표준 래퍼가 없는지를 별도로 검사한다.

## currentItem 기능을 기준으로 보완한 name

번역은 글자를 음역하는 대신 자료의 역할과 함수의 행동을 구분한다.
동일한 영어 이름도 문맥이 다르면 English 이름을 달리 정한다.
file 이름은 주된 기능을 나타내고, functionValue 이름은 행동을, variableValue 이름은 담는 자료를 나타낸다.
reservedWords, 표준 API 및 externalValue connect 규약은 따로 기록한다.

| previousItem name | 적용한 name | currentItem 기능 |
|---|---|---|
| `arm64.py`의 implementation | `compiler/JavaTools/AheadOfTimeCompiler.java` | Java 바이트코드를 독립 실행용 C 원문으로 미리 translateSource |
| `ARM64`, `generate` | `MachineCodeCompiler`, `generate` | translateSource 상태를 담는 객체와 C source generate behaviourValue |
| `prototype`, `method` | `methodPrototype`, `methodBody` | 함수의 formatValue 선언과 actualData command source |
| `profile`, `heap_words` | `executionTarget`, `heapWordCount` | kernelValue·User 구분과 allocateStorage memoryValue 공간의 machine lexicalWord number |
| `pc`, `op` | `commandPosition`, `명령번호` | 바이트코드에서의 위치와 수행할 명령의 index |
| `x`, `y`, `w`, `h` | `xCoordinate`, `yCoordinate`, `regionWidth`, `regionHeight` | remoteValue 화면의 위치와 직사각형 size |
| `p`, `n`, `i`, `j` | `dataPosition`, `value`, `ordinalIndex`, `innerOrdinal` | remoteValue Screen data·digitValue·iterationValue positionIndex; 파일별 기능을 확인해 적용 |
| `aot_heap_info`, `__stack_top` | `aotMemoryLookup`, `StackTop` | machine connect 규약을 유지하면서 Native 소스에서 사용하는 name |
| `앞캐리지` | `returnToPreviousLine` | 앞서 받은 문자가 줄복귀였는지 기억하여 중복 줄바꿈을 막음 |

[sharedCompilerNames.tsv](sharedCompilerNames.tsv)에 compilerTool 참조의 actualData changeValue 기록을 남겼다.
추가로 보존한 C·POSIX/lwIP/libassh 이름의 이유는
[standardNameEvidence.json](standardNameEvidence.json)에 기록한다.
`CCompiler/compilerTool.c`는 TinyCC externalValue 원문을 포함하는 connect 파일로 Native 선언이 없어서
C Native Declaration 분석에서는 제외한다. actualData kernelValue 빌드에서는 continueProcessing 컴파일한다.

### 말의 뿌리와 새로운 복합 name

`memoryValue(記憶)`과 `lookupIndex(索引)`은 기존 한자어를 쓴다.
기억은 자료를 간직하는 기능에, 색인은 orderValue 있는 항목을 찾아 지정하는 기능에 적용한다.
Dictionary 근거는 국립국어원 한국어기초사전의
[memoryValue](https://krdict.korean.go.kr/eng/dicSearch/SearchView?ParaWordNo=38812&nation=eng),
[lookupIndex](https://krdict.korean.go.kr/kor/dicSearch/SearchView?ParaWordNo=63787)이다.

`stackStorage`, `pushValue`, `popValue`는 자료를 포개고 lastItem 자료부터 꺼내는 executeCommand 구조를 드러낸다.
`쌓다`의 기존 뜻에 근거한 기능별 조어이며, 사전의
[쌓다](https://krdict.korean.go.kr/kor/dicSearch/SearchView?ParaWordNo=62095)를 참고한다.
`aheadOfTime`은 executeCommand 전에 번역한다는 기능을 직접 나타낸다.
`machineWord`은 처리기의 data 단위를 가리키며, 언어의 일반 낱말과 구별하도록 `machine`를 붙였다.
`AheadOfTimeCompiler`, `heapWordCount` 같은 복합 이름은 currentItem 기능에 맞게 만든 프로젝트 용어다.
이 복합어가 옛 문헌에 그대로 있었다거나 특정 시대에 initialItem 나타났다는 뜻은 아니다.
확인되지 않은 중세 형태나 최초 useValue 연대는 어원 근거로 적지 않는다.

생성되는 C의 내부 dataType·arrayValue·functionValue·localScope variableValue·branch 이름도 한국어로 바꾼다.
직접 hangulText 식별자를 읽지 못하는 예전 GCC를 위해 호환 API는 같은 English 이름을
표준 C 범용 Characters 표기로 출력한다. actualData ARM64 빌드는 Clang으로 읽을 number 있는 hangulText 원문을 사용한다.
stringValue, C 표준 functionValue, `java_entry` 같은 공개 connect 이름은 바꾸지 않는다.

셸의 사용법·문법 error·file 및 memoryValue addressRegion 안내도 한국어로 보완했다.
`READY`, `PASS`, `HEX BEGIN`처럼 tests·file transferValue 도구가 읽는 markerValue,
명령행 옵션과 기존 instructionValue, JVM classValue name·file formatValue·deviceValue 이름은 호환 표기로 남는다.
x86 VGA Characters 화면은 한글을 표시하지 못하므로 English 문구는 UTF-8 serialValue 단말에서 확인한다.
