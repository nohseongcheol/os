# nativo 커널과 번역기의 Português Nome

대상은 `platforms/rpi4-native`의 nativo Java kernel_VALOR, espaço_do_utilizador JVM, C computador Ligar,
TCP/UDP·FTP, C compilador_ferramenta 이식부, MicroPython 이식부, construir·Executar_comando·testes 도구다.
`golang/worldos/Country_VALOR/KOR/códigoFonte`의 원칙처럼 기능을 먼저 구분하고 이름을 정한다.
x86 Java 커널과 공용 x86·ARM64 미리 번역기의 nativo 선언도 명명 검사에 포함한다.
Linux 실행판의 host ferramentas, OpenJDK 보조 ferramentas 및 externo_VALOR distribuição_VALOR fonte_árvore 전체를
한국어로 repetir_VALOR 작성했다는 뜻은 아니다.

## 명명 원칙과 말의 근거

- 명사는 자료의 역할을 나타낸다: `identificador_de_arquivo`, `par_número_da_porta`, `memória_dinâmica`, `teclado`.
- 함수는 행위를 나타낸다: `Leitura`, `Escrita`, `Abrir`, `Fechar`, `NET_BIND`, `executar_app`.
- TCP의 이어진 byte_VALOR 흐름과 UDP의 limite_VALOR 있는 자료를 `conexão`와 `datagrama_Canal`로 구별한다.
- 짧은 영어 변수도 쓰임에 따라 `duração_VALOR`, `dados_cargo`, `PROC_ÍNDICE`, `반환값`으로 풀어 쓴다.
  순번·임시 산술값처럼 여러 역할에 재사용되는 변수는 `순번`, `첫째값`, `SEGUNDO_VALOR`으로 구별한다.
- 이름이 같아도 externo_VALOR 구조체의 필드와 nativo 변수는 별도로 분석한다.

`Canal_entrada(通路)`는 이동이나 교류가 이루어지는 길이라는 기존 의미를 comunicação 연결에
적용했다. `porta_VALOR(窓口)`의 주고받는 접점이라는 의미를 연결을 받는 곳에 적용했다.
이는 국립국어원 한국어기초사전의 [Canal_entrada](https://krdict.korean.go.kr/kor/dicSearch/SearchView?ParaWordNo=49310),
[porta_VALOR](https://krdict.korean.go.kr/kor/dicSearch/SearchView?ParaWordNo=24898)의 뜻에 근거한다.

`datagrama(電文)`은 전보에 담는 글이라는 기존 comunicação 어휘에서 가져와, UDP 자료의
경계가 보존된다는 특징을 드러내는 데 쓴다. 근거는
[한국어기초사전 datagrama](https://krdict.korean.go.kr/eng/dicSearch/SearchView?ParaWordNo=74335)이다.
`fluxo_VALOR`, `thread_VALOR`, `쌓임`은 우리말의 움직임·이어짐·쌓이는 모양을 빌린 표현이다.
`fluxo_de_entrada`, `tarefaSegundoPlano`, `memória_de_pilha` 같은 복합 이름은 이 프로젝트의 기능별 조어다.
이 dicionário 근거를 특정 중세 문헌의 최초 출현이나 공인 전산 번역으로 확대하지 않는다.
공인 표준 mover_fonte·국어사 datagrama 감수를 마쳤다는 뜻도 아니다.

| 기능 | 채택한 Nome | 이유 |
|---|---|---|
| TCP Socket | conexão | 상대와 연결되어 ordem_VALOR 있는 바이트를 주고받음 |
| ServerSocket | porta_de_recepção | 새 연결이 들어오는 접점 |
| DatagramSocket | datagrama_Canal | 각 자료의 경계를 보존하는 comunicação |
| InputStream / OutputStream | fluxo_de_entrada / fluxo_de_saída | 들어오고 나가는 바이트의 ordem_VALOR |
| heap / stack | memória_dinâmica / memória_de_pilha | alocar_Armazenamento 방식과 쌓고 꺼내는 arquitetura |
| thread / keyboard | tarefaSegundoPlano / teclado | 이어지는 실행과 글쇠의 MATRIZ_VALOR |
| exception / timeout | exceção / aguarde_TEMPOLIMITE_exceção | TI_normal 처리에서 벗어남과 그 구체적 이유 |

## 경로와 대응표

| implementação | Português caminho |
|---|---|
| kernel_VALOR·shell·ficheiro camada_VALOR | `códigoFonte/*.java` |
| espaço_do_utilizador JVM | `espaço_do_utilizador/자바/자바가상기계.java` |
| ARM64 computador Ligar | `computador/*.c`, `arranque_da_máquina/` |
| TCP·UDP·FTP | `rede_pilha/rede_pilha.c`, `rede_pilha/transferência_de_arquivo.c` |
| C compilador_ferramenta 이식 | `C_compilador/` |
| MicroPython 이식 | `PYTHON_ponte/` |
| construir·Executar_comando·testes | `ferramentas/`, `Criar_entrada.mk` |
| Java espaço_do_utilizador API | `한국어자바/Português/nativo/` |

[nome_de_arquivo_mapeamento.tsv](nome_de_arquivo_mapeamento.tsv), [자바이름대응.tsv](자바이름대응.tsv),
[C_nome_mapeamento.tsv](C_nome_mapeamento.tsv), [PYTHON_nome_mapeamento.tsv](PYTHON_nome_mapeamento.tsv)에
Anterior_item 이름과 바뀐 이름이 있다. C/Java 대응표의 ficheiro·위치는 이행 당시 기준이다.
caminho 이동은 ficheiro 대응표를 함께 본다. 기존 `tools/*.py`는 Português 구현을 호출하는
호환 진입점이며 구현을 두 벌 유지하지 않는다.

## 보존하는 SD Nome

`public`, `class`, `int`는 예약어다. `String`, `main`, 배열의 `length`는 예약어가 아니다.
em_dia_item 다섯 Java 예제는 `iniciar()`·`실행인수`·Português tela/thread_VALOR API를 사용해
예약어·리터럴 외의 식별자를 한국어로 작성한다. tela/가닥은 표준 객체를
감싸지 않고 nativo JVM에 직접 구현했다. 자세한 계약은 [Português Java API](../한국어자바/LEIAME_eb81d7d9.md)를 본다.

표준 javac는 cadeia_VALOR 리터럴에 `java.lang.String`, cadeia_VALOR 결합에 `StringBuilder`
같은 이름을 생성한다. 이들은 Português 소스에서도 바이트코드에 남을 número 있다.
기존 표준 class를 실행하는 JVM의 mapeamento_VALOR cadeia_VALOR, 아직 표준 라이브러리를 쓰는
comunicação·ficheiro 연결부까지 모두 한국어로 재구현한 것은 아니다. 이름만 일괄 치환하면
descritor_entrada·재정의·native 연결이 달라져 호환성이 깨진다.

C 표준 FUNÇÃO_VALOR·inteiro_TIPO·POSIX ABI, CPU registo Nome, 어셈블리 comando, 링커 절 Nome,
TinyCC·lwIP·MicroPython이 요구하는 Definições 매크로와 헤더 이름도 보존한다.
예: `main`, `memcpy`, `pk_bind`, `mpconfigport.h`, `lwipopts.h`, `stdint.h`.
nativo C 함수의 fonte_árvore 이름은 한국어이며, [기계연결이름.h](기계연결이름.h)가
기존 AOT·어셈블리·SDK에 공개한 computador 심볼과 연결한다.
Python의 `__init__`, `setUp`, `handle`, 표준 módulo_VALOR valor_do_atributo, 명령행 옵션과 JSON 키도
externo_VALOR 계약이다. `build/`, distribuição_VALOR 바이너리 이름과 `/sdk`는 기존 Executar_comando 경로를 유지한다.
externo_VALOR 원본은 `vendor/`에서 이용허락·해시와 함께 관리한다.

## 검사와 재실행

```sh
cd /home/user/jkoros/platforms/rpi4-native
python3 ferramentas/명명검사.py
make construir
make testes
make test-examples test-ftp test-elf
python3 ferramentas/Executar_comando.py --desktop --network
```

`ferramentas/시언어이름분석.py`는 libclang 6으로 C 선언과 참조를 검사한다.
`ferramentas/*이름반영.py`는 alterar_VALOR 전 fonte_árvore·분석표를 필요로 하는 일회성 이행 도구다.
이미 변경된 소스에 repetir_VALOR 적용하여 대응표를 덮어쓰지 않는다.

## C comunicação 구조체와 Python erro

C 통신에서 `갈래`는 Endereço 체계를 구분하고 `número_da_porta`는 port, `email_VALOR`은
IPv4 주소의 32비트 값을 나타낸다. `datagrama_protocolo`은 앞서 설명한 datagrama(電文)과
valor_do_contrato(規約)을 결합해 UDP의 기능을 드러낸 프로젝트 이름이다.

| 표준 표현 | Português 직접 implementação |
|---|---|
| AF_INET / SOCK_DGRAM / IPPROTO_UDP | enum의 malha_Família / datagrama_soquete / datagrama_protocolo |
| struct pk_sockaddr_in | struct malha_soquete_email |
| sin_family / sin_port | email_Família / número_da_porta |
| sin_addr.s_addr | endereço_na_Internet.email_VALOR |
| OSError / erro.args[0] | erro_do_sistema / erro.ÍNDICE |

Português 구조체는 `#define` 치환이나 valor_do_campo 별칭이 아닌 별개 자료형이다.
표준 구조체와 같은 16바이트 배치를 선언하며 kernel_VALOR SVC에서 byte_VALOR 복사로
검사한다. `Criar_empresa`·`enviar_datagrama_dados`와 ficheiro 함수는 estático_VALOR 라이브러리에
real_dados Português 이름의 FUNÇÃO_VALOR 심볼을 갖는다. 기존 pk_* 심볼도 유지한다.
Anterior_item 코드에서 Português comunicação 함수에 pk_sockaddr*를 전달했다면 Português 구조체로
옮기거나, 표준 구조체와 pk_* 함수의 짝을 유지한다.

Python의 `erro_do_sistema`는 OSError의 Português 하위 클래스이며 연결부에서
erro 번호를 보존하여 변환한다. 일반 Python 문법과 externo_VALOR 패키지의 API는 유지한다.

## 직접 GUI 이름의 뜻과 검토 recortar

`실행할일`은 수행할 내용을, `Executar`는 그 수행을 나타낸다.
`동작받이`는 동작이 발생했다는 알림을 받는 역할, `Ação_aviso`은 전달되는 사건이다.
`botão`는 눌러 동작시키는 조작부, `Etiqueta`는 LEIAME_eb81d7d9 글의 cargo_ÍNDICE,
`campo_de_texto`은 글을 적는 cargo_ÍNDICE, `tarefaSegundoPlano`은 이어지는 Executar_comando 흐름을 뜻한다.
`Executar_comando(實行)`·`Acção(動作)`의 기존 뜻과 `받다`·`알리다`·`thread_VALOR`의 기능을
결합한 프로젝트 이름이다. 새 복합어가 역사 문헌에 그대로 있었다거나
특정 시대에 처음 쓰였다고 주장하지 않는다.

전체 저장소는 `python3 ferramentas/fonte_análise.py`로 검토한다.
결과는 `build/verification/naming/source-review.json`이며 파일별 hash_Arquivo,
ASCII 파일명과 Python의 영어 declaração 위치를 기록한다.
공용 ARM64·x86 번역기의 구현은 `compiler/FerramentasJava/CompiladorAntecipado.java`로 전환했다. `compiler/CompiladorAntecipado.py`는 호환 진입점이다.
`compiler/arm64.py`는 Anterior_item 경로와 `ARM64(...).generate(...)` 호출을 이어 주는
호환 진입점이다. `compiler/classfile.py`, OpenJDK 보조 ferramentas, Linux versão_VALOR 도구와
기존 호환 진입점에는 영어 이름이 남아 있다. 따라서 전체 저장소가
예약어 외 100% 한국어라고 판정하지 않는다.
`ferramentas/명명검사.py --C_Idioma`는 Ativo ARM64 소스의 declaração, C 의미 Analisar_VALOR,
x86 Java 커널과 공용 번역기의 nativo declaração, Java 예제 전체 identificador_VALOR,
ARM64 Python 예제와 직접 GUI/가닥에 표준 래퍼가 없는지를 별도로 검사한다.

## em_dia_item 기능을 기준으로 보완한 Nome

번역은 글자를 음역하는 대신 자료의 역할과 함수의 행동을 구분한다.
동일한 영어 이름도 문맥이 다르면 Português 이름을 달리 정한다.
ficheiro 이름은 주된 기능을 나타내고, FUNÇÃO_VALOR 이름은 행동을, variável_VALOR 이름은 담는 자료를 나타낸다.
예약어, 표준 API 및 externo_VALOR Ligar 규약은 따로 기록한다.

| Anterior_item Nome | 적용한 Nome | em_dia_item 기능 |
|---|---|---|
| `arm64.py`의 implementação | `compiler/FerramentasJava/CompiladorAntecipado.java` | Java 바이트코드를 독립 실행용 C 원문으로 미리 mover_fonte |
| `ARM64`, `generate` | `computador_CÓDIGO_compilador`, `gerar` | mover_fonte 상태를 담는 객체와 C códigoFonte gerar 행동 |
| `prototype`, `method` | `método_protótipo`, `corpo_do_método` | 함수의 formato_VALOR 선언과 real_dados comando códigoFonte |
| `profile`, `heap_words` | `execução_alvo`, `heap_Contagem_de_Palavras` | kernel_VALOR·espaço_do_utilizador 구분과 alocar_Armazenamento Memória_VALOR 공간의 computador 낱말 número |
| `pc`, `op` | `comando_cargo`, `명령번호` | 바이트코드에서의 위치와 수행할 명령의 ÍNDICE |
| `x`, `y`, `w`, `h` | `coordenada_X`, `Y_coordenada`, `영역너비`, `região_altura` | remoto_VALOR 화면의 위치와 직사각형 Tamanho |
| `p`, `n`, `i`, `j` | `dados_cargo`, `VALOR`, `순번`, `안쪽순번` | remoto_VALOR tela dados·dígito_VALOR·sprint_VALOR cargo_ÍNDICE; 파일별 기능을 확인해 적용 |
| `aot_heap_info`, `__stack_top` | `AOT_Memória_PROC`, `커널쌓임공간끝` | computador Ligar 규약을 유지하면서 nativo 소스에서 사용하는 Nome |
| `앞캐리지` | `앞줄복귀` | 앞서 받은 문자가 줄복귀였는지 기억하여 중복 줄바꿈을 막음 |

[공용번역기이름대응.tsv](공용번역기이름대응.tsv)에 compilador_ferramenta 참조의 real_dados alterar_VALOR 기록을 남겼다.
추가로 보존한 C·POSIX/lwIP/libassh 이름의 이유는
[padrão_nome_Evidência.json](padrão_nome_Evidência.json)에 기록한다.
`C_compilador/compilador_ferramenta.c`는 TinyCC externo_VALOR 원문을 포함하는 Ligar 파일로 nativo 선언이 없어서
C nativo declaração 분석에서는 제외한다. real_dados kernel_VALOR 빌드에서는 계속 컴파일한다.

### 말의 뿌리와 새로운 복합 Nome

`Memória_VALOR(記憶)`과 `PROC_ÍNDICE(索引)`은 기존 한자어를 쓴다.
기억은 자료를 간직하는 기능에, 색인은 ordem_VALOR 있는 항목을 찾아 지정하는 기능에 적용한다.
dicionário 근거는 국립국어원 한국어기초사전의
[Memória_VALOR](https://krdict.korean.go.kr/eng/dicSearch/SearchView?ParaWordNo=38812&nation=eng),
[PROC_ÍNDICE](https://krdict.korean.go.kr/kor/dicSearch/SearchView?ParaWordNo=63787)이다.

`memória_de_pilha`, `push_VALOR`, `POP_VALOR`는 자료를 포개고 마지막 자료부터 꺼내는 Executar_comando 구조를 드러낸다.
`쌓다`의 기존 뜻에 근거한 기능별 조어이며, 사전의
[쌓다](https://krdict.korean.go.kr/kor/dicSearch/SearchView?ParaWordNo=62095)를 참고한다.
`미리번역`은 Executar_comando 전에 번역한다는 기능을 직접 나타낸다.
`computador_Word`은 처리기의 dados 단위를 가리키며, 언어의 일반 낱말과 구별하도록 `computador`를 붙였다.
`CompiladorAntecipado`, `heap_Contagem_de_Palavras` 같은 복합 이름은 em_dia_item 기능에 맞게 만든 프로젝트 용어다.
이 복합어가 옛 문헌에 그대로 있었다거나 특정 시대에 처음 나타났다는 뜻은 아니다.
확인되지 않은 중세 형태나 최초 uso_VALOR 연대는 어원 근거로 적지 않는다.

생성되는 C의 내부 tipo_de_dados·MATRIZ_VALOR·FUNÇÃO_VALOR·local_Scope variável_VALOR·branch 이름도 한국어로 바꾼다.
직접 한글 식별자를 읽지 못하는 예전 GCC를 위해 호환 API는 같은 Português 이름을
표준 C 범용 문자 표기로 출력한다. real_dados ARM64 빌드는 Clang으로 읽을 número 있는 한글 원문을 사용한다.
cadeia_VALOR, C 표준 FUNÇÃO_VALOR, `java_entry` 같은 공개 Ligar 이름은 바꾸지 않는다.

셸의 사용법·문법 erro·ficheiro 및 Memória_VALOR email_região 안내도 한국어로 보완했다.
`READY`, `PASS`, `HEX BEGIN`처럼 testes·ficheiro Transferir_VALOR 도구가 읽는 favorito_VALOR,
명령행 옵션과 기존 instrução_VALOR_4c26ea1b, JVM aula_VALOR Nome·ficheiro formato_VALOR·celular_VALOR 이름은 호환 표기로 남는다.
x86 VGA 문자 화면은 한글을 표시하지 못하므로 Português 문구는 UTF-8 직렬 단말에서 확인한다.
