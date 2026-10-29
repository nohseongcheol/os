# 자체 커널과 번역기의 Euskara Izena

대상은 `platforms/rpi4-native`의 자체 Java nukleo_balio, erabiltzaile JVM, C gailu Konektatu,
TCP/UDP·FTP, C 번역기 이식부, MicroPython 이식부, eraiki_sistema·exekutatu_komando·시험 도구다.
`golang/worldos/나라/KOR/ITURBURUA`의 원칙처럼 기능을 먼저 구분하고 이름을 정한다.
x86 Java 커널과 공용 x86·ARM64 미리 번역기의 자체 선언도 명명 검사에 포함한다.
Linux 실행판의 Ostalari Tresnak, OpenJDK 보조 Tresnak 및 외부 배포 iturburu_zuhaitz 전체를
한국어로 다시 작성했다는 뜻은 아니다.

## 명명 원칙과 말의 근거

- 명사는 자료의 역할을 나타낸다: `fitxategi_helduleku`, `pareko_ataka_zenbaki`, `동적기억공간`, `teklatu`.
- 함수는 행위를 나타낸다: `Irakurri`, `Idatzi`, `Ireki`, `Itxi`, `망주소묶기`, `exekutatu_aplik`.
- TCP의 이어진 byte_balio 흐름과 UDP의 경계 있는 자료를 `konexio`와 `전문통로`로 구별한다.
- 짧은 영어 변수도 쓰임에 따라 `luzera_balio`, `datuak_kargu`, `BEGIRATU_INDIZE`, `반환값`으로 풀어 쓴다.
  순번·임시 산술값처럼 여러 역할에 재사용되는 변수는 `순번`, `첫째값`, `SEGUNDOA_balio`으로 구별한다.
- 이름이 같아도 외부 구조체의 필드와 자체 변수는 별도로 분석한다.

`kanal_sarrera(通路)`는 이동이나 교류가 이루어지는 길이라는 기존 의미를 통신 연결에
적용했다. `ataka_balio(窓口)`의 주고받는 접점이라는 의미를 연결을 받는 곳에 적용했다.
이는 국립국어원 한국어기초사전의 [kanal_sarrera](https://krdict.korean.go.kr/kor/dicSearch/SearchView?ParaWordNo=49310),
[ataka_balio](https://krdict.korean.go.kr/kor/dicSearch/SearchView?ParaWordNo=24898)의 뜻에 근거한다.

`전문(電文)`은 전보에 담는 글이라는 기존 통신 어휘에서 가져와, UDP 자료의
경계가 보존된다는 특징을 드러내는 데 쓴다. 근거는
[한국어기초사전 전문](https://krdict.korean.go.kr/eng/dicSearch/SearchView?ParaWordNo=74335)이다.
`Stream_balio`, `hari_balio`, `쌓임`은 우리말의 움직임·이어짐·쌓이는 모양을 빌린 표현이다.
`입력흐름`, `작업가닥`, `pila_biltegi` 같은 복합 이름은 이 프로젝트의 기능별 조어다.
이 hiztegi 근거를 특정 중세 문헌의 최초 출현이나 공인 전산 번역으로 확대하지 않는다.
공인 표준 ITZULI_iturburu·국어사 전문 감수를 마쳤다는 뜻도 아니다.

| 기능 | 채택한 Izena | 이유 |
|---|---|---|
| TCP Socket | konexio | 상대와 연결되어 ordena_balio 있는 바이트를 주고받음 |
| ServerSocket | 수신창구 | 새 연결이 들어오는 접점 |
| DatagramSocket | 전문통로 | 각 자료의 경계를 보존하는 통신 |
| InputStream / OutputStream | 입력흐름 / 출력흐름 | 들어오고 나가는 바이트의 ordena_balio |
| heap / stack | 동적기억공간 / pila_biltegi | esleitu_biltegi 방식과 쌓고 꺼내는 구조 |
| thread / keyboard | 작업가닥 / teklatu | 이어지는 실행과 글쇠의 matrize_balio |
| exception / timeout | salbuespen / itxaron_DENBORA_MUGA_salbuespen | 정상 처리에서 벗어남과 그 구체적 이유 |

## 경로와 대응표

| 구현 | Euskara Bide_izena |
|---|---|
| nukleo_balio·shell·Fitxategia maila_balio | `ITURBURUA/*.java` |
| erabiltzaile JVM | `erabiltzaile/자바/자바가상기계.java` |
| ARM64 gailu Konektatu | `gailu/*.c`, `부팅/` |
| TCP·UDP·FTP | `sare_pila/sare_pila.c`, `sare_pila/fitxategi_transferitu.c` |
| C 번역기 이식 | `시언어번역기/` |
| MicroPython 이식 | `PYTHON_zubi/` |
| eraiki_sistema·exekutatu_komando·시험 | `Tresnak/`, `sortu_sarrera.mk` |
| Java erabiltzaile API | `한국어자바/Euskara/자체/` |

[파일이름대응.tsv](파일이름대응.tsv), [자바이름대응.tsv](자바이름대응.tsv),
[시언어이름대응.tsv](시언어이름대응.tsv), [파이썬이름대응.tsv](파이썬이름대응.tsv)에
이전 이름과 바뀐 이름이 있다. C/Java 대응표의 Fitxategia·위치는 이행 당시 기준이다.
Bide_izena 이동은 Fitxategia 대응표를 함께 본다. 기존 `tools/*.py`는 Euskara 구현을 호출하는
호환 진입점이며 구현을 두 벌 유지하지 않는다.

## 보존하는 SD Izena

`public`, `class`, `int`는 예약어다. `String`, `main`, 배열의 `length`는 예약어가 아니다.
현재 다섯 Java 예제는 `Exekutatu_2()`·`실행인수`·Euskara 화면/hari_balio API를 사용해
예약어·리터럴 외의 식별자를 한국어로 작성한다. 화면/가닥은 표준 객체를
감싸지 않고 자체 JVM에 직접 구현했다. 자세한 계약은 [Euskara Java API](../한국어자바/IRAKHAU_eb81d7d9.md)를 본다.

표준 javac는 kate_balio 리터럴에 `java.lang.String`, kate_balio 결합에 `StringBuilder`
같은 이름을 생성한다. 이들은 Euskara 소스에서도 바이트코드에 남을 수 있다.
기존 표준 class를 실행하는 JVM의 대응 kate_balio, 아직 표준 라이브러리를 쓰는
통신·Fitxategia 연결부까지 모두 한국어로 재구현한 것은 아니다. 이름만 일괄 치환하면
서술자·재정의·native 연결이 달라져 호환성이 깨진다.

C 표준 FUNTZIOA_balio·osoko_zenbaki_MOTA·POSIX ABI, CPU izena_eman_balio Izena, 어셈블리 Komandoa, 링커 절 Izena,
TinyCC·lwIP·MicroPython이 요구하는 Ezarpenak 매크로와 헤더 이름도 보존한다.
예: `main`, `memcpy`, `pk_bind`, `mpconfigport.h`, `lwipopts.h`, `stdint.h`.
자체 C 함수의 iturburu_zuhaitz 이름은 한국어이며, [기계연결이름.h](기계연결이름.h)가
기존 AOT·어셈블리·SDK에 공개한 gailu 심볼과 연결한다.
Python의 `__init__`, `setUp`, `handle`, 표준 modulu_balio atributu_balio, 명령행 옵션과 JSON 키도
외부 계약이다. `build/`, 배포 바이너리 이름과 `/sdk`는 기존 exekutatu_komando 경로를 유지한다.
외부 원본은 `vendor/`에서 이용허락·해시와 함께 관리한다.

## 검사와 재실행

```sh
cd /home/user/jkoros/platforms/rpi4-native
python3 Tresnak/명명검사.py
make eraiki_sistema
make 시험
make test-examples test-ftp test-elf
python3 Tresnak/exekutatu_komando.py --desktop --network
```

`Tresnak/시언어이름분석.py`는 libclang 6으로 C 선언과 참조를 검사한다.
`Tresnak/*이름반영.py`는 aldatu_balio 전 iturburu_zuhaitz·분석표를 필요로 하는 일회성 이행 도구다.
이미 변경된 소스에 다시 적용하여 대응표를 덮어쓰지 않는다.

## C 통신 구조체와 Python errorea

C 통신에서 `갈래`는 helbide 체계를 구분하고 `ataka_zenbaki`는 port, `helbide_balio`은
IPv4 주소의 32비트 값을 나타낸다. `전문전송규약`은 앞서 설명한 전문(電文)과
kasu_balio(規約)을 결합해 UDP의 기능을 드러낸 프로젝트 이름이다.

| 표준 표현 | Euskara 직접 구현 |
|---|---|
| AF_INET / SOCK_DGRAM / IPPROTO_UDP | enum의 hodei_sorta / 전문통신 / 전문전송규약 |
| struct pk_sockaddr_in | struct 인터넷통신주소 |
| sin_family / sin_port | helbide_sorta / ataka_zenbaki |
| sin_addr.s_addr | Internet_helbide.helbide_balio |
| OSError / errorea.args[0] | sistema_errore / errorea.INDIZE |

Euskara 구조체는 `#define` 치환이나 eremu_balio 별칭이 아닌 별개 자료형이다.
표준 구조체와 같은 16바이트 배치를 선언하며 nukleo_balio SVC에서 byte_balio 복사로
검사한다. `sortu_amaiera_puntu`·`자료전문보내기`와 Fitxategia 함수는 estatiko_balio 라이브러리에
benetako_datuak Euskara 이름의 FUNTZIOA_balio 심볼을 갖는다. 기존 pk_* 심볼도 유지한다.
이전 코드에서 Euskara 통신 함수에 pk_sockaddr*를 전달했다면 Euskara 구조체로
옮기거나, 표준 구조체와 pk_* 함수의 짝을 유지한다.

Python의 `sistema_errore`는 OSError의 Euskara 하위 클래스이며 연결부에서
errorea 번호를 보존하여 변환한다. 일반 Python 문법과 외부 패키지의 API는 유지한다.

## 직접 GUI 이름의 뜻과 검토 klip

`실행할일`은 수행할 내용을, `Exekutatu`는 그 수행을 나타낸다.
`동작받이`는 동작이 발생했다는 알림을 받는 역할, `동작알림`은 전달되는 사건이다.
`botoia`는 눌러 동작시키는 조작부, `Etiketa`는 IRAKHAU_eb81d7d9 글의 kargu_INDIZE,
`SMS_eremu`은 글을 적는 kargu_INDIZE, `작업가닥`은 이어지는 exekutatu_komando 흐름을 뜻한다.
`exekutatu_komando(實行)`·`Ekintza(動作)`의 기존 뜻과 `받다`·`알리다`·`hari_balio`의 기능을
결합한 프로젝트 이름이다. 새 복합어가 역사 문헌에 그대로 있었다거나
특정 시대에 처음 쓰였다고 주장하지 않는다.

전체 저장소는 `python3 Tresnak/iturburu_iritzi.py`로 검토한다.
결과는 `build/verification/naming/source-review.json`이며 파일별 hash_fitxategi,
ASCII 파일명과 Python의 영어 deklarazio 위치를 기록한다.
공용 ARM64·x86 번역기의 구현은 `compiler/자바도구/기계어미리번역.java`로 전환했다. `compiler/기계어미리번역.py`는 호환 진입점이다.
`compiler/arm64.py`는 이전 경로와 `ARM64(...).generate(...)` 호출을 이어 주는
호환 진입점이다. `compiler/classfile.py`, OpenJDK 보조 Tresnak, Linux bertsio_balio 도구와
기존 호환 진입점에는 영어 이름이 남아 있다. 따라서 전체 저장소가
예약어 외 100% 한국어라고 판정하지 않는다.
`Tresnak/명명검사.py --시언어`는 aktibo ARM64 소스의 deklarazio, C 의미 Analizatu_balio,
x86 Java 커널과 공용 번역기의 자체 deklarazio, Java 예제 전체 identifikatzaile_balio,
ARM64 Python 예제와 직접 GUI/가닥에 표준 래퍼가 없는지를 별도로 검사한다.

## 현재 기능을 기준으로 보완한 Izena

번역은 글자를 음역하는 대신 자료의 역할과 함수의 행동을 구분한다.
동일한 영어 이름도 문맥이 다르면 Euskara 이름을 달리 정한다.
Fitxategia 이름은 주된 기능을 나타내고, FUNTZIOA_balio 이름은 행동을, 변수 이름은 담는 자료를 나타낸다.
예약어, 표준 API 및 외부 Konektatu 규약은 따로 기록한다.

| 이전 Izena | 적용한 Izena | 현재 기능 |
|---|---|---|
| `arm64.py`의 구현 | `compiler/자바도구/기계어미리번역.java` | Java 바이트코드를 독립 실행용 C 원문으로 미리 ITZULI_iturburu |
| `ARM64`, `generate` | `기계어번역기`, `sortu` | ITZULI_iturburu 상태를 담는 객체와 C ITURBURUA sortu 행동 |
| `prototype`, `method` | `함수원형`, `함수본문` | 함수의 formatu_balio 선언과 benetako_datuak Komandoa ITURBURUA |
| `profile`, `heap_words` | `실행대상`, `동적기억낱말수` | nukleo_balio·erabiltzaile 구분과 esleitu_biltegi Memoria_balio 공간의 gailu 낱말 수 |
| `pc`, `op` | `komando_kargu`, `명령번호` | 바이트코드에서의 위치와 수행할 명령의 INDIZE |
| `x`, `y`, `w`, `h` | `X_koordenatu`, `Y_koordenatu`, `영역너비`, `영역높이` | urruneko_balio 화면의 위치와 직사각형 Tamaina |
| `p`, `n`, `i`, `j` | `datuak_kargu`, `balio`, `순번`, `안쪽순번` | urruneko_balio 화면 datuak·digitu_balio·iterazio_balio kargu_INDIZE; 파일별 기능을 확인해 적용 |
| `aot_heap_info`, `__stack_top` | `미리번역기억조회`, `커널쌓임공간끝` | gailu Konektatu 규약을 유지하면서 자체 소스에서 사용하는 Izena |
| `앞캐리지` | `앞줄복귀` | 앞서 받은 문자가 줄복귀였는지 기억하여 중복 줄바꿈을 막음 |

[공용번역기이름대응.tsv](공용번역기이름대응.tsv)에 번역기 참조의 benetako_datuak aldatu_balio 기록을 남겼다.
추가로 보존한 C·POSIX/lwIP/libassh 이름의 이유는
[규격이름근거.json](규격이름근거.json)에 기록한다.
`시언어번역기/번역기.c`는 TinyCC 외부 원문을 포함하는 Konektatu 파일로 자체 선언이 없어서
C 자체 deklarazio 분석에서는 제외한다. benetako_datuak nukleo_balio 빌드에서는 계속 컴파일한다.

### 말의 뿌리와 새로운 복합 Izena

`Memoria_balio(記憶)`과 `BEGIRATU_INDIZE(索引)`은 기존 한자어를 쓴다.
기억은 자료를 간직하는 기능에, 색인은 ordena_balio 있는 항목을 찾아 지정하는 기능에 적용한다.
hiztegi 근거는 국립국어원 한국어기초사전의
[Memoria_balio](https://krdict.korean.go.kr/eng/dicSearch/SearchView?ParaWordNo=38812&nation=eng),
[BEGIRATU_INDIZE](https://krdict.korean.go.kr/kor/dicSearch/SearchView?ParaWordNo=63787)이다.

`pila_biltegi`, `쌓기`, `POP_balio`는 자료를 포개고 마지막 자료부터 꺼내는 exekutatu_komando 구조를 드러낸다.
`쌓다`의 기존 뜻에 근거한 기능별 조어이며, 사전의
[쌓다](https://krdict.korean.go.kr/kor/dicSearch/SearchView?ParaWordNo=62095)를 참고한다.
`미리번역`은 exekutatu_komando 전에 번역한다는 기능을 직접 나타낸다.
`gailu_Word`은 처리기의 datuak 단위를 가리키며, 언어의 일반 낱말과 구별하도록 `gailu`를 붙였다.
`기계어미리번역`, `동적기억낱말수` 같은 복합 이름은 현재 기능에 맞게 만든 프로젝트 용어다.
이 복합어가 옛 문헌에 그대로 있었다거나 특정 시대에 처음 나타났다는 뜻은 아니다.
확인되지 않은 중세 형태나 최초 사용 연대는 어원 근거로 적지 않는다.

생성되는 C의 내부 datu_mota·matrize_balio·FUNTZIOA_balio·lokal_esparru 변수·adar 이름도 한국어로 바꾼다.
직접 한글 식별자를 읽지 못하는 예전 GCC를 위해 호환 API는 같은 Euskara 이름을
표준 C 범용 문자 표기로 출력한다. benetako_datuak ARM64 빌드는 Clang으로 읽을 수 있는 한글 원문을 사용한다.
kate_balio, C 표준 FUNTZIOA_balio, `java_entry` 같은 공개 Konektatu 이름은 바꾸지 않는다.

셸의 사용법·문법 errorea·Fitxategia 및 Memoria_balio 공간 안내도 한국어로 보완했다.
`READY`, `PASS`, `HEX BEGIN`처럼 시험·Fitxategia transferitu_balio 도구가 읽는 표식,
명령행 옵션과 기존 instrukzio_balio_4c26ea1b, JVM Gela_balio Izena·Fitxategia formatu_balio·gailu_balio 이름은 호환 표기로 남는다.
x86 VGA 문자 화면은 한글을 표시하지 못하므로 Euskara 문구는 UTF-8 직렬 단말에서 확인한다.
