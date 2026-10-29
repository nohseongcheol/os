# propio 커널과 번역기의 español nombre

대상은 `platforms/rpi4-native`의 propio Java valorNúcleo, Usuario JVM, C máquina conectar,
TCP/UDP·FTP, C herramientaCompilador 이식부, MicroPython 이식부, construirSistema·ejecutarComando·Pruebas 도구다.
`golang/worldos/valorPaís/KOR/fuente`의 원칙처럼 기능을 먼저 구분하고 이름을 정한다.
x86 Java 커널과 공용 x86·ARM64 미리 번역기의 propio 선언도 denominación 검사에 포함한다.
Linux 실행판의 Anfitrión Herramientas, OpenJDK valorAuxiliar Herramientas 및 valorExterno valorDistribución árbolFuente 전체를
한국어로 valorReintentar 작성했다는 뜻은 아니다.

## denominación 원칙과 말의 근거

- 명사는 자료의 역할을 나타낸다: `manejadorArchivo`, `númeroPuertoParRed`, `almacenamientoMontículo`, `Teclado`.
- 함수는 행위를 나타낸다: `leer`, `escribir`, `abrir`, `cerrar`, `asociarRedCorta`, `ponerEnMarchaPrograma`.
- TCP의 이어진 valorByte 흐름과 UDP의 valorFrontera 있는 자료를 `Conexión`와 `CanalDatagrama`로 구별한다.
- 짧은 영어 변수도 쓰임에 따라 `longitud`, `posiciónDatos`, `índiceBuscar`, `valorDevuelto`으로 풀어 쓴다.
  índiceOrdinal·valorTemporal 산술값처럼 여러 역할에 재사용되는 변수는 `índiceOrdinal`, `valorPrimero`, `valorSegundo`으로 구별한다.
- 이름이 같아도 valorExterno 구조체의 필드와 propio 변수는 별도로 분석한다.

`entradaElementoCanal(通路)`는 이동이나 교류가 이루어지는 길이라는 기존 의미를 Comunicación 연결에
적용했다. `valorPuerto(窓口)`의 주고받는 접점이라는 의미를 연결을 받는 곳에 적용했다.
이는 국립국어원 한국어기초사전의 [entradaElementoCanal](https://krdict.korean.go.kr/kor/dicSearch/SearchView?ParaWordNo=49310),
[valorPuerto](https://krdict.korean.go.kr/kor/dicSearch/SearchView?ParaWordNo=24898)의 뜻에 근거한다.

`datagrama(電文)`은 전보에 담는 글이라는 기존 Comunicación 어휘에서 가져와, UDP 자료의
경계가 보존된다는 특징을 드러내는 데 쓴다. 근거는
[한국어기초사전 datagrama](https://krdict.korean.go.kr/eng/dicSearch/SearchView?ParaWordNo=74335)이다.
`valorFlujo`, `valorHiloEjecución`, `쌓임`은 우리말의 움직임·esContinuación·쌓이는 모양을 빌린 표현이다.
`FlujoEntrada`, `tareaFondo`, `almacenamientoPila` 같은 복합 이름은 이 프로젝트의 기능별 조어다.
이 Diccionario 근거를 특정 중세 문헌의 최초 출현이나 공인 전산 번역으로 확대하지 않는다.
공인 표준 traducirFuente·국어사 datagrama 감수를 마쳤다는 뜻도 아니다.

| 기능 | 채택한 nombre | valorRazón |
|---|---|---|
| TCP Socket | Conexión | 상대와 연결되어 valorOrden 있는 바이트를 주고받음 |
| ServerSocket | recibirPuerto | 새 연결이 들어오는 접점 |
| DatagramSocket | CanalDatagrama | 각 자료의 경계를 보존하는 Comunicación |
| InputStream / OutputStream | FlujoEntrada / FlujoSalida | 들어오고 나가는 바이트의 valorOrden |
| heap / stack | almacenamientoMontículo / almacenamientoPila | asignarMemoriaAlmacenamiento 방식과 쌓고 꺼내는 Arquitectura |
| thread / keyboard | tareaFondo / Teclado | 이어지는 실행과 글쇠의 valorArreglo |
| exception / timeout | excepción / ExcepciónTiempoEsperaEsperar | esNormal 처리에서 벗어남과 그 구체적 valorRazón |

## 경로와 대응표

| implementación | español ruta |
|---|---|
| valorNúcleo·intérpreteComandos·Archivo valorCapa | `fuente/*.java` |
| Usuario JVM | `Usuario/Java/MáquinaVirtualJava.java` |
| ARM64 máquina conectar | `máquina/*.c`, `Arranque/` |
| TCP·UDP·FTP | `PilaRed/PilaRed.c`, `PilaRed/transferenciaArchivo.c` |
| C herramientaCompilador AdaptaciónPlataforma | `CompiladorC/` |
| MicroPython AdaptaciónPlataforma | `puentePython/` |
| construirSistema·ejecutarComando·Pruebas | `Herramientas/`, `crearEntradaElemento.mk` |
| Java Usuario API | `JavaEspañol/español/propio/` |

[asociaciónNombreArchivo.tsv](asociaciónNombreArchivo.tsv), [asociaciónNombreJava.tsv](asociaciónNombreJava.tsv),
[asociaciónNombreC.tsv](asociaciónNombreC.tsv), [asociaciónNombrePython.tsv](asociaciónNombrePython.tsv)에
elementoListaElementoPrevio 이름과 바뀐 이름이 있다. C/Java 대응표의 Archivo·위치는 이행 당시 기준이다.
ruta 이동은 Archivo 대응표를 함께 본다. 기존 `tools/*.py`는 español 구현을 호출하는
호환 진입점이며 구현을 두 벌 유지하지 않는다.

## 보존하는 definiciónEstándar nombre

`public`, `class`, `int`는 예약어다. `String`, `main`, 배열의 `length`는 예약어가 아니다.
elementoListaActual 다섯 Java 예제는 `ponerEnMarcha()`·`Argumentos`·español Pantalla/valorHiloEjecución API를 사용해
palabrasReservado·리터럴 외의 식별자를 한국어로 작성한다. Pantalla/가닥은 표준 객체를
감싸지 않고 propio JVM에 직접 구현했다. 자세한 계약은 [español Java API](../JavaEspañol/Guía.md)를 본다.

표준 javac는 Cadena 리터럴에 `java.lang.String`, Cadena 결합에 `StringBuilder`
같은 이름을 생성한다. 이들은 español 소스에서도 바이트코드에 남을 númeroValor 있다.
기존 표준 class를 실행하는 JVM의 valorAsociación Cadena, 아직 표준 라이브러리를 쓰는
Comunicación·Archivo 연결부까지 construirTodos 한국어로 재구현한 것은 아니다. 이름만 일괄 치환하면
entradaElementoDescriptor·재정의·native 연결이 달라져 호환성이 깨진다.

C 표준 Función·tipoEnteroValor·POSIX ABI, CPU registroProcesador nombre, 어셈블리 comando, 링커 절 nombre,
TinyCC·lwIP·MicroPython이 요구하는 ajustes 매크로와 헤더 이름도 보존한다.
예: `main`, `memcpy`, `pk_bind`, `mpconfigport.h`, `lwipopts.h`, `stdint.h`.
propio C 함수의 árbolFuente 이름은 한국어이며, [nombresEnlazarMáquina.h](nombresEnlazarMáquina.h)operandoPrimero
기존 AOT·어셈블리·SDK에 공개한 máquina 심볼과 연결한다.
Python의 `__init__`, `setUp`, `handle`, 표준 valorMódulo valorAtributo, 명령행 옵션과 JSON 키도
valorExterno 계약이다. `build/`, valorDistribución 바이너리 이름과 `/sdk`는 기존 ejecutarComando 경로를 유지한다.
valorExterno 원본은 `vendor/`에서 이용허락·해시와 함께 관리한다.

## 검사와 재실행

```sh
cd /home/user/jkoros/platforms/rpi4-native
python3 Herramientas/comprobarDenominación.py
make construirSistema
make Pruebas
make test-examples test-ftp test-elf
python3 Herramientas/ejecutarComando.py --desktop --network
```

`Herramientas/examinarNombresC.py`는 libclang 6으로 C 선언과 참조를 검사한다.
`Herramientas/*이름반영.py`는 cambiarValor valorAntes árbolFuente·분석표를 필요로 하는 일회성 이행 도구다.
이미 변경된 소스에 valorReintentar 적용하여 대응표를 덮어쓰지 않는다.

## C Comunicación 구조체와 Python error

C 통신에서 `갈래`는 dirección 체계를 구분하고 `númeroPuerto`는 port, `valorDirección`은
IPv4 주소의 32비트 값을 나타낸다. `ProtocoloDatagrama`은 앞서 설명한 datagrama(電文)과
valorContrato(規約)을 결합해 UDP의 기능을 드러낸 프로젝트 이름이다.

| 표준 표현 | español 직접 implementación |
|---|---|
| AF_INET / SOCK_DGRAM / IPPROTO_UDP | enum의 FamiliaInternet / ConectorRedDatagrama / ProtocoloDatagrama |
| struct pk_sockaddr_in | struct DirecciónConectorRedInternet |
| sin_family / sin_port | familiaDirección / númeroPuerto |
| sin_addr.s_addr | DirecciónInternet.valorDirección |
| OSError / error.args[0] | ErrorSistema / error.número |

español 구조체는 `#define` 치환이나 valorCampo 별칭이 아닌 별개 자료형이다.
표준 구조체와 같은 16바이트 배치를 선언하며 valorNúcleo SVC에서 valorByte 복사로
검사한다. `crearExtremo`·`enviarDatosDatagrama`와 Archivo 함수는 valorEstático 라이브러리에
datosEfectivo español 이름의 Función 심볼을 갖는다. 기존 pk_* 심볼도 유지한다.
elementoListaElementoPrevio 코드에서 español Comunicación 함수에 pk_sockaddr*를 전달했다면 español 구조체로
옮기거나, 표준 구조체와 pk_* 함수의 짝을 유지한다.

Python의 `ErrorSistema`는 OSError의 español 하위 클래스이며 연결부에서
error 번호를 보존하여 변환한다. 일반 Python 문법과 valorExterno 패키지의 API는 유지한다.

## 직접 GUI 이름의 뜻과 검토 recortar

`TareaTareaEjecutable`은 수행할 내용을, `ejecutarTarea`는 그 수행을 나타낸다.
`ReceptorAcción`는 동작이 발생했다는 알림을 받는 역할, `NotificaciónAcción`은 전달되는 사건이다.
`botón`는 눌러 동작시키는 조작부, `etiqueta`는 Guía 글의 índicePosición,
`CampoTexto`은 글을 적는 índicePosición, `tareaFondo`은 이어지는 ejecutarComando 흐름을 뜻한다.
`ejecutarComando(實行)`·`acción(動作)`의 기존 뜻과 `받다`·`알리다`·`valorHiloEjecución`의 기능을
결합한 프로젝트 이름이다. 새 복합어가 역사 문헌에 그대로 있었다거나
특정 시대에 elementoListaInicialValor 쓰였다고 주장하지 않는다.

전체 저장소는 `python3 Herramientas/RevisiónExamenFuente.py`로 검토한다.
결과는 `build/verification/naming/source-review.json`이며 파일별 archivoResumenHash,
ASCII 파일명과 Python의 영어 Declaraciones 위치를 기록한다.
공용 ARM64·x86 번역기의 구현은 `compiler/HerramientaJava/CompilaciónAnticipada.java`로 전환했다. `compiler/CompilaciónAnticipada.py`는 호환 진입점이다.
`compiler/arm64.py`는 elementoListaElementoPrevio 경로와 `ARM64(...).generate(...)` 호출을 valorContinuación 주는
호환 진입점이다. `compiler/classfile.py`, OpenJDK valorAuxiliar Herramientas, Linux valorVersión 도구와
기존 호환 진입점에는 영어 이름이 남아 있다. 따라서 전체 저장소가
palabrasReservado 외 100% 한국어라고 판정하지 않는다.
`Herramientas/comprobarDenominación.py --lenguaC`는 activo ARM64 소스의 Declaraciones, C 의미 examinarValor,
x86 Java 커널과 공용 번역기의 propio Declaraciones, Java Ejemplos 전체 valorIdentificador,
ARM64 Python 예제와 직접 GUI/가닥에 표준 래퍼가 없는지를 별도로 검사한다.

## elementoListaActual 기능을 기준으로 보완한 nombre

번역은 글자를 음역하는 대신 자료의 역할과 함수의 행동을 구분한다.
동일한 영어 이름도 문맥이 다르면 español 이름을 달리 정한다.
Archivo 이름은 주된 기능을 나타내고, Función 이름은 행동을, valorVariable 이름은 담는 자료를 나타낸다.
palabrasReservado, 표준 API 및 valorExterno conectar 규약은 따로 기록한다.

| elementoListaElementoPrevio nombre | 적용한 nombre | elementoListaActual 기능 |
|---|---|---|
| `arm64.py`의 implementación | `compiler/HerramientaJava/CompilaciónAnticipada.java` | Java 바이트코드를 독립 실행용 C 원문으로 미리 traducirFuente |
| `ARM64`, `generate` | `CompiladorCódigoMáquina`, `generar` | traducirFuente 상태를 담는 객체와 C fuente generar valorComportamiento |
| `prototype`, `method` | `prototipoMétodo`, `cuerpoMétodo` | 함수의 valorFormato 선언과 datosEfectivo comando fuente |
| `profile`, `heap_words` | `objetivoEjecución`, `númeroElementosPalabraMontículo` | valorNúcleo·Usuario 구분과 asignarMemoriaAlmacenamiento Memoria 공간의 máquina palabraLéxico númeroValor |
| `pc`, `op` | `posiciónComando`, `명령번호` | 바이트코드에서의 위치와 수행할 명령의 número |
| `x`, `y`, `w`, `h` | `coordenadaCoordenadaHorizontal`, `coordenadaCoordenadaVertical`, `anchuraRegión`, `alturaRegión` | valorRemoto 화면의 위치와 직사각형 tamaño |
| `p`, `n`, `i`, `j` | `posiciónDatos`, `valor`, `índiceOrdinal`, `ordinalInterior` | valorRemoto Pantalla Datos·valorDígito·valorIteración índicePosición; 파일별 기능을 확인해 적용 |
| `aot_heap_info`, `__stack_top` | `buscarMemoriaCompilaciónAnticipada`, `ExtremoSuperiorPila` | máquina conectar 규약을 유지하면서 propio 소스에서 사용하는 nombre |
| `앞캐리지` | `líneaElementoPrevioHaciaRetornar` | 앞서 받은 문자가 줄복귀였는지 기억하여 중복 줄바꿈을 막음 |

[nombresCompiladorCompartido.tsv](nombresCompiladorCompartido.tsv)에 herramientaCompilador 참조의 datosEfectivo cambiarValor 기록을 남겼다.
추가로 보존한 C·POSIX/lwIP/libassh 이름의 이유는
[evidenciaNombreEstándar.json](evidenciaNombreEstándar.json)에 기록한다.
`CompiladorC/herramientaCompilador.c`는 TinyCC valorExterno 원문을 포함하는 conectar 파일로 propio 선언이 없어서
C propio Declaraciones 분석에서는 제외한다. datosEfectivo valorNúcleo 빌드에서는 procesamientoContinuar 컴파일한다.

### 말의 뿌리와 새로운 복합 nombre

`Memoria(記憶)`과 `índiceBuscar(索引)`은 기존 한자어를 쓴다.
기억은 자료를 간직하는 기능에, 색인은 valorOrden 있는 항목을 찾아 지정하는 기능에 적용한다.
Diccionario 근거는 국립국어원 한국어기초사전의
[Memoria](https://krdict.korean.go.kr/eng/dicSearch/SearchView?ParaWordNo=38812&nation=eng),
[índiceBuscar](https://krdict.korean.go.kr/kor/dicSearch/SearchView?ParaWordNo=63787)이다.

`almacenamientoPila`, `apilarValor`, `desapilarValor`는 자료를 포개고 elementoListaÚltimo 자료부터 꺼내는 ejecutarComando 구조를 드러낸다.
`쌓다`의 기존 뜻에 근거한 기능별 조어이며, 사전의
[쌓다](https://krdict.korean.go.kr/kor/dicSearch/SearchView?ParaWordNo=62095)를 참고한다.
`tiempoDeAnticipado`은 ejecutarComando 전에 번역한다는 기능을 직접 나타낸다.
`palabraMáquina`은 처리기의 Datos 단위를 가리키며, 언어의 일반 낱말과 구별하도록 `máquina`를 붙였다.
`CompilaciónAnticipada`, `númeroElementosPalabraMontículo` 같은 복합 이름은 elementoListaActual 기능에 맞게 만든 프로젝트 용어다.
이 복합어가 옛 문헌에 그대로 있었다거나 특정 시대에 elementoListaInicialValor 나타났다는 뜻은 아니다.
확인되지 않은 중세 형태나 최초 valorUsar 연대는 어원 근거로 적지 않는다.

생성되는 C의 내부 tipoDatos·valorArreglo·Función·ámbitoLocal valorVariable·rama 이름도 한국어로 바꾼다.
직접 textoHangul 식별자를 읽지 못하는 예전 GCC를 위해 호환 API는 같은 español 이름을
표준 C 범용 Caracteres 표기로 출력한다. datosEfectivo ARM64 빌드는 Clang으로 읽을 númeroValor 있는 textoHangul 원문을 사용한다.
Cadena, C 표준 Función, `java_entry` 같은 공개 conectar 이름은 바꾸지 않는다.

셸의 사용법·문법 error·Archivo 및 Memoria regiónDirección 안내도 한국어로 보완했다.
`READY`, `PASS`, `HEX BEGIN`처럼 Pruebas·Archivo valorTransferencia 도구가 읽는 valorMarcador,
명령행 옵션과 기존 valorInstrucciónMáquina, JVM valorClase nombre·Archivo valorFormato·Dispositivo 이름은 호환 표기로 남는다.
x86 VGA Caracteres 화면은 한글을 표시하지 못하므로 español 문구는 UTF-8 valorSerie 단말에서 확인한다.
