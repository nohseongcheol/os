# 자체 커널과 번역기의 한국어 Ad

대상은 `platforms/rpi4-native`의 자체 Java ýadro_baha, ulanyjy JVM, C kompýuter Birikme,
TCP/UDP·FTP, C 번역기 이식부, MicroPython 이식부, düz_ulgam·ýerine_ýetir_buýruk·시험 도구다.
`golang/worldos/나라/KOR/Çeşme`의 원칙처럼 기능을 먼저 구분하고 이름을 정한다.
x86 Java 커널과 공용 x86·ARM64 미리 번역기의 자체 선언도 명명 검사에 포함한다.
Linux 실행판의 esasy Gurallar, OpenJDK 보조 Gurallar 및 외부 배포 gor_agaç 전체를
한국어로 다시 작성했다는 뜻은 아니다.

## 명명 원칙과 말의 근거

- 명사는 자료의 역할을 나타낸다: `faýl_ryçag`, `상대접속번호`, `동적기억공간`, `klawiatura`.
- 함수는 행위를 나타낸다: `Oka`, `Ýaz`, `Aç`, `Ýap`, `망주소묶기`, `işe_goýber_programma`.
- TCP의 이어진 baýt_baha 흐름과 UDP의 경계 있는 자료를 `birikme`와 `전문통로`로 구별한다.
- 짧은 영어 변수도 쓰임에 따라 `dowamlylyk_baha`, `자료위치`, `색인`, `반환값`으로 풀어 쓴다.
  순번·임시 산술값처럼 여러 역할에 재사용되는 변수는 `순번`, `첫째값`, `둘째값`으로 구별한다.
- 이름이 같아도 외부 구조체의 필드와 자체 변수는 별도로 분석한다.

`kanal_girizmeklik(通路)`는 이동이나 교류가 이루어지는 길이라는 기존 의미를 통신 연결에
적용했다. `port_baha(窓口)`의 주고받는 접점이라는 의미를 연결을 받는 곳에 적용했다.
이는 국립국어원 한국어기초사전의 [kanal_girizmeklik](https://krdict.korean.go.kr/kor/dicSearch/SearchView?ParaWordNo=49310),
[port_baha](https://krdict.korean.go.kr/kor/dicSearch/SearchView?ParaWordNo=24898)의 뜻에 근거한다.

`전문(電文)`은 전보에 담는 글이라는 기존 통신 어휘에서 가져와, UDP 자료의
경계가 보존된다는 특징을 드러내는 데 쓴다. 근거는
[한국어기초사전 전문](https://krdict.korean.go.kr/eng/dicSearch/SearchView?ParaWordNo=74335)이다.
`Stream_baha`, `akym_baha`, `쌓임`은 우리말의 움직임·이어짐·쌓이는 모양을 빌린 표현이다.
`입력흐름`, `작업가닥`, `Desse_Ammar` 같은 복합 이름은 이 프로젝트의 기능별 조어다.
이 sözlük 근거를 특정 중세 문헌의 최초 출현이나 공인 전산 번역으로 확대하지 않는다.
공인 표준 Terjime_gor·국어사 전문 감수를 마쳤다는 뜻도 아니다.

| 기능 | 채택한 Ad | 이유 |
|---|---|---|
| TCP Socket | birikme | 상대와 연결되어 tertip_baha 있는 바이트를 주고받음 |
| ServerSocket | 수신창구 | 새 연결이 들어오는 접점 |
| DatagramSocket | 전문통로 | 각 자료의 경계를 보존하는 통신 |
| InputStream / OutputStream | 입력흐름 / 출력흐름 | 들어오고 나가는 바이트의 tertip_baha |
| heap / stack | 동적기억공간 / Desse_Ammar | bölüp_aýyr_Ammar 방식과 쌓고 꺼내는 구조 |
| thread / keyboard | 작업가닥 / klawiatura | 이어지는 실행과 글쇠의 ARRAY_baha |
| exception / timeout | 예외 / 대기시간초과예외 | 정상 처리에서 벗어남과 그 구체적 이유 |

## 경로와 대응표

| 구현 | 한국어 Ýol |
|---|---|
| ýadro_baha·gabyjak·Faýl dereje_baha | `Çeşme/*.java` |
| ulanyjy JVM | `ulanyjy/자바/자바가상기계.java` |
| ARM64 kompýuter Birikme | `kompýuter/*.c`, `부팅/` |
| TCP·UDP·FTP | `Tor_Desse/Tor_Desse.c`, `Tor_Desse/faýl_geçir.c` |
| C 번역기 이식 | `시언어번역기/` |
| MicroPython 이식 | `파이썬연결/` |
| düz_ulgam·ýerine_ýetir_buýruk·시험 | `Gurallar/`, `döretmek_girizmeklik.mk` |
| Java ulanyjy API | `한국어자바/한국어/자체/` |

[파일이름대응.tsv](파일이름대응.tsv), [자바이름대응.tsv](자바이름대응.tsv),
[시언어이름대응.tsv](시언어이름대응.tsv), [파이썬이름대응.tsv](파이썬이름대응.tsv)에
이전 이름과 바뀐 이름이 있다. C/Java 대응표의 Faýl·위치는 이행 당시 기준이다.
Ýol 이동은 Faýl 대응표를 함께 본다. 기존 `tools/*.py`는 한국어 구현을 호출하는
호환 진입점이며 구현을 두 벌 유지하지 않는다.

## 보존하는 SD Ad

`public`, `class`, `int`는 예약어다. `String`, `main`, 배열의 `length`는 예약어가 아니다.
현재 다섯 Java 예제는 `Bitir()`·`실행인수`·한국어 화면/akym_baha API를 사용해
예약어·리터럴 외의 식별자를 한국어로 작성한다. 화면/가닥은 표준 객체를
감싸지 않고 자체 JVM에 직접 구현했다. 자세한 계약은 [한국어 Java API](../한국어자바/README_eb81d7d9.md)를 본다.

표준 javac는 setir_baha_6ca8363c 리터럴에 `java.lang.String`, setir_baha_6ca8363c 결합에 `StringBuilder`
같은 이름을 생성한다. 이들은 한국어 소스에서도 바이트코드에 남을 수 있다.
기존 표준 class를 실행하는 JVM의 대응 setir_baha_6ca8363c, 아직 표준 라이브러리를 쓰는
통신·Faýl 연결부까지 모두 한국어로 재구현한 것은 아니다. 이름만 일괄 치환하면
서술자·재정의·native 연결이 달라져 호환성이 깨진다.

C 표준 FUNCTION_baha·bitin_ýaz·POSIX ABI, CPU 저장기 Ad, 어셈블리 buýruk, 링커 절 Ad,
TinyCC·lwIP·MicroPython이 요구하는 Düzümler 매크로와 헤더 이름도 보존한다.
예: `main`, `memcpy`, `pk_bind`, `mpconfigport.h`, `lwipopts.h`, `stdint.h`.
자체 C 함수의 gor_agaç 이름은 한국어이며, [기계연결이름.h](기계연결이름.h)가
기존 AOT·어셈블리·SDK에 공개한 kompýuter 심볼과 연결한다.
Python의 `__init__`, `setUp`, `handle`, 표준 모듈 alamat_baha, 명령행 옵션과 JSON 키도
외부 계약이다. `build/`, 배포 바이너리 이름과 `/sdk`는 기존 ýerine_ýetir_buýruk 경로를 유지한다.
외부 원본은 `vendor/`에서 이용허락·해시와 함께 관리한다.

## 검사와 재실행

```sh
cd /home/user/jkoros/platforms/rpi4-native
python3 Gurallar/명명검사.py
make düz_ulgam
make 시험
make test-examples test-ftp test-elf
python3 Gurallar/ýerine_ýetir_buýruk.py --desktop --network
```

`Gurallar/시언어이름분석.py`는 libclang 6으로 C 선언과 참조를 검사한다.
`Gurallar/*이름반영.py`는 üýtget_baha 전 gor_agaç·분석표를 필요로 하는 일회성 이행 도구다.
이미 변경된 소스에 다시 적용하여 대응표를 덮어쓰지 않는다.

## C 통신 구조체와 Python Hata

C 통신에서 `갈래`는 salgy 체계를 구분하고 `접속번호`는 port, `salgy_baha`은
IPv4 주소의 32비트 값을 나타낸다. `전문전송규약`은 앞서 설명한 전문(電文)과
ýumuş_baha_102996da(規約)을 결합해 UDP의 기능을 드러낸 프로젝트 이름이다.

| 표준 표현 | 한국어 직접 구현 |
|---|---|
| AF_INET / SOCK_DGRAM / IPPROTO_UDP | enum의 bulut_Maşgala / 전문통신 / 전문전송규약 |
| struct pk_sockaddr_in | struct 인터넷통신주소 |
| sin_family / sin_port | salgy_Maşgala / 접속번호 |
| sin_addr.s_addr | Internet_salgy.salgy_baha |
| OSError / Hata.args[0] | ulgam_säwlik / Hata.indeks |

한국어 구조체는 `#define` 치환이나 meýdan_baha 별칭이 아닌 별개 자료형이다.
표준 구조체와 같은 16바이트 배치를 선언하며 ýadro_baha SVC에서 baýt_baha 복사로
검사한다. `통신종단점만들기`·`자료전문보내기`와 Faýl 함수는 statiki_baha 라이브러리에
hakyky_maglumat 한국어 이름의 FUNCTION_baha 심볼을 갖는다. 기존 pk_* 심볼도 유지한다.
이전 코드에서 한국어 통신 함수에 pk_sockaddr*를 전달했다면 한국어 구조체로
옮기거나, 표준 구조체와 pk_* 함수의 짝을 유지한다.

Python의 `ulgam_säwlik`는 OSError의 한국어 하위 클래스이며 연결부에서
Hata 번호를 보존하여 변환한다. 일반 Python 문법과 외부 패키지의 API는 유지한다.

## 직접 GUI 이름의 뜻과 검토 klip

`실행할일`은 수행할 내용을, `ýerine_ýetir_tabşyryk`는 그 수행을 나타낸다.
`동작받이`는 동작이 발생했다는 알림을 받는 역할, `동작알림`은 전달되는 사건이다.
`düwme`는 눌러 동작시키는 조작부, `belgi`는 README_eb81d7d9 글의 자리,
`tekst_meýdançasy`은 글을 적는 자리, `작업가닥`은 이어지는 ýerine_ýetir_buýruk 흐름을 뜻한다.
`ýerine_ýetir_buýruk(實行)`·`iş(動作)`의 기존 뜻과 `받다`·`알리다`·`akym_baha`의 기능을
결합한 프로젝트 이름이다. 새 복합어가 역사 문헌에 그대로 있었다거나
특정 시대에 처음 쓰였다고 주장하지 않는다.

전체 저장소는 `python3 Gurallar/gor_gözden_geçiriş.py`로 검토한다.
결과는 `build/verification/naming/source-review.json`이며 파일별 heş_kody_faýl,
ASCII 파일명과 Python의 영어 선언 위치를 기록한다.
공용 ARM64·x86 번역기의 구현은 `compiler/자바도구/기계어미리번역.java`로 전환했다. `compiler/기계어미리번역.py`는 호환 진입점이다.
`compiler/arm64.py`는 이전 경로와 `ARM64(...).generate(...)` 호출을 이어 주는
호환 진입점이다. `compiler/classfile.py`, OpenJDK 보조 Gurallar, Linux wersiýa_baha 도구와
기존 호환 진입점에는 영어 이름이 남아 있다. 따라서 전체 저장소가
예약어 외 100% 한국어라고 판정하지 않는다.
`Gurallar/명명검사.py --시언어`는 işjeň ARM64 소스의 선언, C 의미 분석,
x86 Java 커널과 공용 번역기의 자체 선언, Java 예제 전체 tanaýjy_baha,
ARM64 Python 예제와 직접 GUI/가닥에 표준 래퍼가 없는지를 별도로 검사한다.

## 현재 기능을 기준으로 보완한 Ad

번역은 글자를 음역하는 대신 자료의 역할과 함수의 행동을 구분한다.
동일한 영어 이름도 문맥이 다르면 한국어 이름을 달리 정한다.
Faýl 이름은 주된 기능을 나타내고, FUNCTION_baha 이름은 행동을, 변수 이름은 담는 자료를 나타낸다.
예약어, 표준 API 및 외부 Birikme 규약은 따로 기록한다.

| 이전 Ad | 적용한 Ad | 현재 기능 |
|---|---|---|
| `arm64.py`의 구현 | `compiler/자바도구/기계어미리번역.java` | Java 바이트코드를 독립 실행용 C 원문으로 미리 Terjime_gor |
| `ARM64`, `generate` | `기계어번역기`, `생성` | Terjime_gor 상태를 담는 객체와 C Çeşme 생성 행동 |
| `prototype`, `method` | `함수원형`, `함수본문` | 함수의 format_baha 선언과 hakyky_maglumat buýruk Çeşme |
| `profile`, `heap_words` | `실행대상`, `동적기억낱말수` | ýadro_baha·ulanyjy 구분과 bölüp_aýyr_Ammar ýat_baha 공간의 kompýuter 낱말 수 |
| `pc`, `op` | `명령위치`, `명령번호` | 바이트코드에서의 위치와 수행할 명령의 indeks |
| `x`, `y`, `w`, `h` | `x_koordinatasy`, `세로좌표`, `영역너비`, `영역높이` | uzakdan_baha 화면의 위치와 직사각형 Ululyk |
| `p`, `n`, `i`, `j` | `자료위치`, `baha`, `순번`, `안쪽순번` | uzakdan_baha 화면 maglumat·san_baha·iterasiýa_baha 자리; 파일별 기능을 확인해 적용 |
| `aot_heap_info`, `__stack_top` | `미리번역기억조회`, `커널쌓임공간끝` | kompýuter Birikme 규약을 유지하면서 자체 소스에서 사용하는 Ad |
| `앞캐리지` | `앞줄복귀` | 앞서 받은 문자가 줄복귀였는지 기억하여 중복 줄바꿈을 막음 |

[공용번역기이름대응.tsv](공용번역기이름대응.tsv)에 번역기 참조의 hakyky_maglumat üýtget_baha 기록을 남겼다.
추가로 보존한 C·POSIX/lwIP/libassh 이름의 이유는
[규격이름근거.json](규격이름근거.json)에 기록한다.
`시언어번역기/번역기.c`는 TinyCC 외부 원문을 포함하는 Birikme 파일로 자체 선언이 없어서
C 자체 선언 분석에서는 제외한다. hakyky_maglumat ýadro_baha 빌드에서는 계속 컴파일한다.

### 말의 뿌리와 새로운 복합 Ad

`ýat_baha(記憶)`과 `색인(索引)`은 기존 한자어를 쓴다.
기억은 자료를 간직하는 기능에, 색인은 tertip_baha 있는 항목을 찾아 지정하는 기능에 적용한다.
sözlük 근거는 국립국어원 한국어기초사전의
[ýat_baha](https://krdict.korean.go.kr/eng/dicSearch/SearchView?ParaWordNo=38812&nation=eng),
[색인](https://krdict.korean.go.kr/kor/dicSearch/SearchView?ParaWordNo=63787)이다.

`Desse_Ammar`, `쌓기`, `POP_baha`는 자료를 포개고 마지막 자료부터 꺼내는 ýerine_ýetir_buýruk 구조를 드러낸다.
`쌓다`의 기존 뜻에 근거한 기능별 조어이며, 사전의
[쌓다](https://krdict.korean.go.kr/kor/dicSearch/SearchView?ParaWordNo=62095)를 참고한다.
`미리번역`은 ýerine_ýetir_buýruk 전에 번역한다는 기능을 직접 나타낸다.
`kompýuter_Söz`은 처리기의 maglumat 단위를 가리키며, 언어의 일반 낱말과 구별하도록 `kompýuter`를 붙였다.
`기계어미리번역`, `동적기억낱말수` 같은 복합 이름은 현재 기능에 맞게 만든 프로젝트 용어다.
이 복합어가 옛 문헌에 그대로 있었다거나 특정 시대에 처음 나타났다는 뜻은 아니다.
확인되지 않은 중세 형태나 최초 사용 연대는 어원 근거로 적지 않는다.

생성되는 C의 내부 maglumatlaryň_görnüşi·ARRAY_baha·FUNCTION_baha·ýerli_elýeterli_gor 변수·şahalanma 이름도 한국어로 바꾼다.
직접 한글 식별자를 읽지 못하는 예전 GCC를 위해 호환 API는 같은 한국어 이름을
표준 C 범용 문자 표기로 출력한다. hakyky_maglumat ARM64 빌드는 Clang으로 읽을 수 있는 한글 원문을 사용한다.
setir_baha_6ca8363c, C 표준 FUNCTION_baha, `java_entry` 같은 공개 Birikme 이름은 바꾸지 않는다.

셸의 사용법·문법 Hata·Faýl 및 ýat_baha 공간 안내도 한국어로 보완했다.
`READY`, `PASS`, `HEX BEGIN`처럼 시험·Faýl geçir_baha 도구가 읽는 표식,
명령행 옵션과 기존 instruksiýa_baha, JVM klas_baha Ad·Faýl format_baha·enjam_baha 이름은 호환 표기로 남는다.
x86 VGA 문자 화면은 한글을 표시하지 못하므로 한국어 문구는 UTF-8 직렬 단말에서 확인한다.
