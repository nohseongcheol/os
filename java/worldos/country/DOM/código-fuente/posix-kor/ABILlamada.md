# Usuario invocar valorFrontera

대상은 jkoros i386 ELF32다. Linux i386의 invocar 번호와 바이너리 호환이 아니다. C의 cdecl 인수를 `máquina/LlamadasSistemaOperación.s`에서 EAX(número), EBX·ECX·EDX·ESI·EDI(ordinalPrimero~ordinalQuinto argumentos)로 변환한다. EBX·ESI·EDI·EBP를 보존하며 결과는 EAX다. valorNúcleo 실패는 valorNegativo error número, C biblioteca 실패는 -1과 양수 errno다.

커널은 0x04000000 이상, 0x04400000 미만의 Usuario valorRegión 안에 자료의 전체 길이가 들어가는지 확인한다. 단순 널 검사가 아니다. C Datos 주소는 valorByte 주소이며, 기존 Java AOT `int[]` 포인터와 혼용하지 않는다. Java Archivo 흐름의 어셈블리 경계가 별도 valorByte 버퍼를 마련하여 같은 호출을 사용한다.

| número | acción | argumentos |
|---|---|---|
| 30 | abrirArchivo | NUL terminación nombre dirección, ajustes, concederPermiso |
| 31 | leerDatosArchivo | entradaElementoDescriptor, Datos dirección, valorByte númeroValor |
| 32 | escribirDatosArchivo | entradaElementoDescriptor, Datos dirección, valorByte númeroValor |
| 33 | cerrarArchivo | entradaElementoDescriptor |
| 34 | posicionarArchivo | entradaElementoDescriptor, valorCodificaciónEstado 있는 valorDesfase, raízProyecto |
| 35 | descriptorArchivoDuplicado | entradaElementoDescriptor |
| 36 | enPosiciónDescriptorArchivoDuplicado | entradaElementoDescriptor, 새 entradaElementoDescriptor |
| 37 | leerEstadoArchivo | entradaElementoDescriptor, 48바이트 valorEstadoValor dirección |
| 38 | eliminarNombreEntradaElementoArchivo | NUL terminación nombre dirección |
| 39 | establecerLongitudArchivo | entradaElementoDescriptor, 새 longitud |
| 40 | descriptorArchivoControl | entradaElementoDescriptor, comando, valor |
| 41 | crearExtremo | dirección valorSistemaOperación, valorClaseTipo, valorContrato número |
| 42 | asociarDirección | entradaElementoDescriptor, sockaddr_in dirección, longitud |
| 43 | enviarDatosDatagrama | entradaElementoDescriptor, Datos dirección, longitud, ajustes, petición dirección |
| 44 | recibirDatosDatagrama | entradaElementoDescriptor, Datos dirección, longitud, ajustes, petición dirección |
| 45 | leerDirecciónConectorRed | entradaElementoDescriptor, sockaddr dirección, socklen_t dirección |
| 46 | establecerTiempoEsperaRecibir | entradaElementoDescriptor, 0~2000 milisegundos |
| 47 | almacenamientoArchivoConfirmar | entradaElementoDescriptor |

43번 요청은 32비트 주소와 32비트 길이의 두 칸이다. 44번 요청은 32비트 주소와 길이를 담은 32비트 값의 dirección 두 칸이다. recibirValor 주소가 NULL이면 valorParRed dirección 기록을 생략한다. sockaddr_in은 16바이트이며 dirección 체계는 Dispositivo valorByte valorSecuencia, 접속번호와 IP 주소는 네트워크 valorByte 차례다. 축소된 dirección 버퍼에도 들어가는 앞부분을 쓰고 전체 dirección tamaño 16을 반환한다.

0~22번의 기존 Java AOT 호출은 유지한다. 0은 programaSalir, 2·3은 기존 argumentos 조회다. elementoListaActual 커널의 argumentos 목록이 ejecutarComando 이름을 제외하므로 C 진입기는 argv[0]에 고정 Cadena `jkoros-app`을 넣고 valorDespués 인수를 전달한다. argv 끝에는 NULL이 있다. 이 제한도 일반 UNIX valorProceso ABI와 다른 점이다.

표준 헤더의 EnteroValor tamaño, valorBanderas valor, stat valorCampo 순서는 `fuente/Encabezados/`에 정의한다. 동적 conectar·다중 valorProceso·스레드가 추가되면 error número 저장과 valorRecurso 수명, invocar 경계도 함께 검토해야 한다.
