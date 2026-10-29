# 자체 커널과 번역기의 Reo_Māori Ingoa

대상은 `platforms/rpi4-native`의 자체 Java kākano_uara_0611a8a8, kaiwhakamahi JVM, C mīhini TŪHONO,
TCP/UDP·FTP, C 번역기 이식부, MicroPython 이식부, hanga_pūnaha·kawe_tono·시험 도구다.
`golang/worldos/나라/KOR/pūtake`의 원칙처럼 기능을 먼저 구분하고 이름을 정한다.
x86 Java 커널과 공용 x86·ARM64 미리 번역기의 자체 선언도 명명 검사에 포함한다.
Linux 실행판의 taurima Ngā_Utauta, OpenJDK 보조 Ngā_Utauta 및 외부 배포 pūtake_rākau 전체를
한국어로 다시 작성했다는 뜻은 아니다.

## 명명 원칙과 말의 근거

- 명사는 자료의 역할을 나타낸다: `kōnae_raweke`, `상대접속번호`, `동적기억공간`, `papapātuhi`.
- 함수는 행위를 나타낸다: `Pānuitia`, `Tuhia`, `Huaki`, `Kati`, `망주소묶기`, `whakahaere_kaupapa`.
- TCP의 이어진 paita_uara 흐름과 UDP의 경계 있는 자료를 `hononga_d584d28a`와 `전문통로`로 구별한다.
- 짧은 영어 변수도 쓰임에 따라 `roa_uara`, `raraunga_tūranga`, `Rapu_INDEX`, `반환값`으로 풀어 쓴다.
  순번·임시 산술값처럼 여러 역할에 재사용되는 변수는 `순번`, `첫째값`, `SECOND_uara`으로 구별한다.
- 이름이 같아도 외부 구조체의 필드와 자체 변수는 별도로 분석한다.

`hongere_tāurunga(通路)`는 이동이나 교류가 이루어지는 길이라는 기존 의미를 통신 연결에
적용했다. `kawe_uara(窓口)`의 주고받는 접점이라는 의미를 연결을 받는 곳에 적용했다.
이는 국립국어원 한국어기초사전의 [hongere_tāurunga](https://krdict.korean.go.kr/kor/dicSearch/SearchView?ParaWordNo=49310),
[kawe_uara](https://krdict.korean.go.kr/kor/dicSearch/SearchView?ParaWordNo=24898)의 뜻에 근거한다.

`전문(電文)`은 전보에 담는 글이라는 기존 통신 어휘에서 가져와, UDP 자료의
경계가 보존된다는 특징을 드러내는 데 쓴다. 근거는
[한국어기초사전 전문](https://krdict.korean.go.kr/eng/dicSearch/SearchView?ParaWordNo=74335)이다.
`roma_uara`, `miro_uara`, `쌓임`은 우리말의 움직임·이어짐·쌓이는 모양을 빌린 표현이다.
`입력흐름`, `작업가닥`, `Huinga_Rokiroki` 같은 복합 이름은 이 프로젝트의 기능별 조어다.
이 papakupu 근거를 특정 중세 문헌의 최초 출현이나 공인 전산 번역으로 확대하지 않는다.
공인 표준 TRANSLATE_pūtake·국어사 전문 감수를 마쳤다는 뜻도 아니다.

| 기능 | 채택한 Ingoa | 이유 |
|---|---|---|
| TCP Socket | hononga_d584d28a | 상대와 연결되어 whakaraupapa_uara 있는 바이트를 주고받음 |
| ServerSocket | 수신창구 | 새 연결이 들어오는 접점 |
| DatagramSocket | 전문통로 | 각 자료의 경계를 보존하는 통신 |
| InputStream / OutputStream | 입력흐름 / 출력흐름 | 들어오고 나가는 바이트의 whakaraupapa_uara |
| heap / stack | 동적기억공간 / Huinga_Rokiroki | tiritiri_Rokiroki 방식과 쌓고 꺼내는 구조 |
| thread / keyboard | 작업가닥 / papapātuhi | 이어지는 실행과 글쇠의 HUĀNGA_uara |
| exception / timeout | 예외 / 대기시간초과예외 | 정상 처리에서 벗어남과 그 구체적 이유 |

## 경로와 대응표

| 구현 | Reo_Māori ara |
|---|---|
| kākano_uara_0611a8a8·anga·Kōnae apa_uara | `pūtake/*.java` |
| kaiwhakamahi JVM | `kaiwhakamahi/자바/자바가상기계.java` |
| ARM64 mīhini TŪHONO | `mīhini/*.c`, `부팅/` |
| TCP·UDP·FTP | `whatunga_Huinga/whatunga_Huinga.c`, `whatunga_Huinga/kōnae_whakawhiti.c` |
| C 번역기 이식 | `시언어번역기/` |
| MicroPython 이식 | `PYTHON_arawhata/` |
| hanga_pūnaha·kawe_tono·시험 | `Ngā_Utauta/`, `Waihanga_tāurunga.mk` |
| Java kaiwhakamahi API | `한국어자바/Reo_Māori/자체/` |

[파일이름대응.tsv](파일이름대응.tsv), [자바이름대응.tsv](자바이름대응.tsv),
[시언어이름대응.tsv](시언어이름대응.tsv), [파이썬이름대응.tsv](파이썬이름대응.tsv)에
이전 이름과 바뀐 이름이 있다. C/Java 대응표의 Kōnae·위치는 이행 당시 기준이다.
ara 이동은 Kōnae 대응표를 함께 본다. 기존 `tools/*.py`는 Reo_Māori 구현을 호출하는
호환 진입점이며 구현을 두 벌 유지하지 않는다.

## 보존하는 SD Ingoa

`public`, `class`, `int`는 예약어다. `String`, `main`, 배열의 `length`는 예약어가 아니다.
현재 다섯 Java 예제는 `whakahaere()`·`실행인수`·Reo_Māori 화면/miro_uara API를 사용해
예약어·리터럴 외의 식별자를 한국어로 작성한다. 화면/가닥은 표준 객체를
감싸지 않고 자체 JVM에 직접 구현했다. 자세한 계약은 [Reo_Māori Java API](../한국어자바/PĀNUIMAI_eb81d7d9.md)를 본다.

표준 javac는 aho_uara 리터럴에 `java.lang.String`, aho_uara 결합에 `StringBuilder`
같은 이름을 생성한다. 이들은 Reo_Māori 소스에서도 바이트코드에 남을 수 있다.
기존 표준 class를 실행하는 JVM의 대응 aho_uara, 아직 표준 라이브러리를 쓰는
통신·Kōnae 연결부까지 모두 한국어로 재구현한 것은 아니다. 이름만 일괄 치환하면
서술자·재정의·native 연결이 달라져 호환성이 깨진다.

C 표준 TAUMAHI_uara·tau_tōpū_TYPE·POSIX ABI, CPU rēhita_uara Ingoa, 어셈블리 tono, 링커 절 Ingoa,
TinyCC·lwIP·MicroPython이 요구하는 Ngā_Tautuhinga 매크로와 헤더 이름도 보존한다.
예: `main`, `memcpy`, `pk_bind`, `mpconfigport.h`, `lwipopts.h`, `stdint.h`.
자체 C 함수의 pūtake_rākau 이름은 한국어이며, [기계연결이름.h](기계연결이름.h)가
기존 AOT·어셈블리·SDK에 공개한 mīhini 심볼과 연결한다.
Python의 `__init__`, `setUp`, `handle`, 표준 kōwae_uara huanga_uara, 명령행 옵션과 JSON 키도
외부 계약이다. `build/`, 배포 바이너리 이름과 `/sdk`는 기존 kawe_tono 경로를 유지한다.
외부 원본은 `vendor/`에서 이용허락·해시와 함께 관리한다.

## 검사와 재실행

```sh
cd /home/user/jkoros/platforms/rpi4-native
python3 Ngā_Utauta/명명검사.py
make hanga_pūnaha
make 시험
make test-examples test-ftp test-elf
python3 Ngā_Utauta/kawe_tono.py --desktop --network
```

`Ngā_Utauta/시언어이름분석.py`는 libclang 6으로 C 선언과 참조를 검사한다.
`Ngā_Utauta/*이름반영.py`는 huri_uara 전 pūtake_rākau·분석표를 필요로 하는 일회성 이행 도구다.
이미 변경된 소스에 다시 적용하여 대응표를 덮어쓰지 않는다.

## C 통신 구조체와 Python Pōhēhē

C 통신에서 `갈래`는 ADDRESS 체계를 구분하고 `접속번호`는 port, `ADDRESS_uara`은
IPv4 주소의 32비트 값을 나타낸다. `전문전송규약`은 앞서 설명한 전문(電文)과
kēhi_uara(規約)을 결합해 UDP의 기능을 드러낸 프로젝트 이름이다.

| 표준 표현 | Reo_Māori 직접 구현 |
|---|---|
| AF_INET / SOCK_DGRAM / IPPROTO_UDP | enum의 kapua_Whānau / 전문통신 / 전문전송규약 |
| struct pk_sockaddr_in | struct 인터넷통신주소 |
| sin_family / sin_port | ADDRESS_Whānau / 접속번호 |
| sin_addr.s_addr | Wāhitau_ipurangi.ADDRESS_uara |
| OSError / Pōhēhē.args[0] | pūnaha_hapa / Pōhēhē.INDEX |

Reo_Māori 구조체는 `#define` 치환이나 āpure_uara 별칭이 아닌 별개 자료형이다.
표준 구조체와 같은 16바이트 배치를 선언하며 kākano_uara_0611a8a8 SVC에서 paita_uara 복사로
검사한다. `통신종단점만들기`·`자료전문보내기`와 Kōnae 함수는 pateko_uara 라이브러리에
tūturu_raraunga Reo_Māori 이름의 TAUMAHI_uara 심볼을 갖는다. 기존 pk_* 심볼도 유지한다.
이전 코드에서 Reo_Māori 통신 함수에 pk_sockaddr*를 전달했다면 Reo_Māori 구조체로
옮기거나, 표준 구조체와 pk_* 함수의 짝을 유지한다.

Python의 `pūnaha_hapa`는 OSError의 Reo_Māori 하위 클래스이며 연결부에서
Pōhēhē 번호를 보존하여 변환한다. 일반 Python 문법과 외부 패키지의 API는 유지한다.

## 직접 GUI 이름의 뜻과 검토 topenga

`실행할일`은 수행할 내용을, `kawe_tūmahi`는 그 수행을 나타낸다.
`동작받이`는 동작이 발생했다는 알림을 받는 역할, `동작알림`은 전달되는 사건이다.
`pātene`는 눌러 동작시키는 조작부, `tapanga`는 PĀNUIMAI_eb81d7d9 글의 tūranga_INDEX,
`āpure_kuputuhi`은 글을 적는 tūranga_INDEX, `작업가닥`은 이어지는 kawe_tono 흐름을 뜻한다.
`kawe_tono(實行)`·`hohenga(動作)`의 기존 뜻과 `받다`·`알리다`·`miro_uara`의 기능을
결합한 프로젝트 이름이다. 새 복합어가 역사 문헌에 그대로 있었다거나
특정 시대에 처음 쓰였다고 주장하지 않는다.

전체 저장소는 `python3 Ngā_Utauta/pūtake_arotake.py`로 검토한다.
결과는 `build/verification/naming/source-review.json`이며 파일별 hash_kōnae,
ASCII 파일명과 Python의 영어 선언 위치를 기록한다.
공용 ARM64·x86 번역기의 구현은 `compiler/자바도구/기계어미리번역.java`로 전환했다. `compiler/기계어미리번역.py`는 호환 진입점이다.
`compiler/arm64.py`는 이전 경로와 `ARM64(...).generate(...)` 호출을 이어 주는
호환 진입점이다. `compiler/classfile.py`, OpenJDK 보조 Ngā_Utauta, Linux putanga_uara 도구와
기존 호환 진입점에는 영어 이름이 남아 있다. 따라서 전체 저장소가
예약어 외 100% 한국어라고 판정하지 않는다.
`Ngā_Utauta/명명검사.py --시언어`는 hohe ARM64 소스의 선언, C 의미 분석,
x86 Java 커널과 공용 번역기의 자체 선언, Java 예제 전체 pūtāutu_uara,
ARM64 Python 예제와 직접 GUI/가닥에 표준 래퍼가 없는지를 별도로 검사한다.

## 현재 기능을 기준으로 보완한 Ingoa

번역은 글자를 음역하는 대신 자료의 역할과 함수의 행동을 구분한다.
동일한 영어 이름도 문맥이 다르면 Reo_Māori 이름을 달리 정한다.
Kōnae 이름은 주된 기능을 나타내고, TAUMAHI_uara 이름은 행동을, 변수 이름은 담는 자료를 나타낸다.
예약어, 표준 API 및 외부 TŪHONO 규약은 따로 기록한다.

| 이전 Ingoa | 적용한 Ingoa | 현재 기능 |
|---|---|---|
| `arm64.py`의 구현 | `compiler/자바도구/기계어미리번역.java` | Java 바이트코드를 독립 실행용 C 원문으로 미리 TRANSLATE_pūtake |
| `ARM64`, `generate` | `기계어번역기`, `waihanga` | TRANSLATE_pūtake 상태를 담는 객체와 C pūtake waihanga 행동 |
| `prototype`, `method` | `함수원형`, `함수본문` | 함수의 hōputu_uara 선언과 tūturu_raraunga tono pūtake |
| `profile`, `heap_words` | `실행대상`, `동적기억낱말수` | kākano_uara_0611a8a8·kaiwhakamahi 구분과 tiritiri_Rokiroki Pūmahara_uara 공간의 mīhini 낱말 수 |
| `pc`, `op` | `tono_tūranga`, `명령번호` | 바이트코드에서의 위치와 수행할 명령의 INDEX |
| `x`, `y`, `w`, `h` | `taunga_x`, `세로좌표`, `영역너비`, `영역높이` | mamao_uara 화면의 위치와 직사각형 rahi |
| `p`, `n`, `i`, `j` | `raraunga_tūranga`, `uara`, `순번`, `안쪽순번` | mamao_uara 화면 raraunga·mati_uara·whitiauau_uara tūranga_INDEX; 파일별 기능을 확인해 적용 |
| `aot_heap_info`, `__stack_top` | `미리번역기억조회`, `커널쌓임공간끝` | mīhini TŪHONO 규약을 유지하면서 자체 소스에서 사용하는 Ingoa |
| `앞캐리지` | `앞줄복귀` | 앞서 받은 문자가 줄복귀였는지 기억하여 중복 줄바꿈을 막음 |

[공용번역기이름대응.tsv](공용번역기이름대응.tsv)에 번역기 참조의 tūturu_raraunga huri_uara 기록을 남겼다.
추가로 보존한 C·POSIX/lwIP/libassh 이름의 이유는
[규격이름근거.json](규격이름근거.json)에 기록한다.
`시언어번역기/번역기.c`는 TinyCC 외부 원문을 포함하는 TŪHONO 파일로 자체 선언이 없어서
C 자체 선언 분석에서는 제외한다. tūturu_raraunga kākano_uara_0611a8a8 빌드에서는 계속 컴파일한다.

### 말의 뿌리와 새로운 복합 Ingoa

`Pūmahara_uara(記憶)`과 `Rapu_INDEX(索引)`은 기존 한자어를 쓴다.
기억은 자료를 간직하는 기능에, 색인은 whakaraupapa_uara 있는 항목을 찾아 지정하는 기능에 적용한다.
papakupu 근거는 국립국어원 한국어기초사전의
[Pūmahara_uara](https://krdict.korean.go.kr/eng/dicSearch/SearchView?ParaWordNo=38812&nation=eng),
[Rapu_INDEX](https://krdict.korean.go.kr/kor/dicSearch/SearchView?ParaWordNo=63787)이다.

`Huinga_Rokiroki`, `쌓기`, `POP_uara`는 자료를 포개고 마지막 자료부터 꺼내는 kawe_tono 구조를 드러낸다.
`쌓다`의 기존 뜻에 근거한 기능별 조어이며, 사전의
[쌓다](https://krdict.korean.go.kr/kor/dicSearch/SearchView?ParaWordNo=62095)를 참고한다.
`미리번역`은 kawe_tono 전에 번역한다는 기능을 직접 나타낸다.
`mīhini_Word`은 처리기의 raraunga 단위를 가리키며, 언어의 일반 낱말과 구별하도록 `mīhini`를 붙였다.
`기계어미리번역`, `동적기억낱말수` 같은 복합 이름은 현재 기능에 맞게 만든 프로젝트 용어다.
이 복합어가 옛 문헌에 그대로 있었다거나 특정 시대에 처음 나타났다는 뜻은 아니다.
확인되지 않은 중세 형태나 최초 사용 연대는 어원 근거로 적지 않는다.

생성되는 C의 내부 momo_raraunga·HUĀNGA_uara·TAUMAHI_uara·paetata_whānuitanga 변수·peka 이름도 한국어로 바꾼다.
직접 한글 식별자를 읽지 못하는 예전 GCC를 위해 호환 API는 같은 Reo_Māori 이름을
표준 C 범용 문자 표기로 출력한다. tūturu_raraunga ARM64 빌드는 Clang으로 읽을 수 있는 한글 원문을 사용한다.
aho_uara, C 표준 TAUMAHI_uara, `java_entry` 같은 공개 TŪHONO 이름은 바꾸지 않는다.

셸의 사용법·문법 Pōhēhē·Kōnae 및 Pūmahara_uara 공간 안내도 한국어로 보완했다.
`READY`, `PASS`, `HEX BEGIN`처럼 시험·Kōnae whakawhiti_uara_630ba093 도구가 읽는 표식,
명령행 옵션과 기존 tohutohu_uara, JVM tauaha_uara Ingoa·Kōnae hōputu_uara·pūkoro_uara 이름은 호환 표기로 남는다.
x86 VGA 문자 화면은 한글을 표시하지 못하므로 Reo_Māori 문구는 UTF-8 직렬 단말에서 확인한다.
