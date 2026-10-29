# español Java valorAyudante biblioteca

OpenJDK 11 이상과 함께 쓰는 프로젝트 valorPropietario API다. 표준 Java biblioteca 전체의 번역판을 뜻하지 않는다. 기존 Java API·키워드·excepción·자료형은 그대로 함께 쓴다.

전체 22개 valorAyudante 메서드의 argumentos·valorDevuelto·제약, SistemaOperativo 안의 사용법, Python·C++ invocar 방법은 **[español biblioteca GuíaUsuario](GuíaUsuario.md)**에 정리했다. [Python invocar Ejemplos](Ejemplos/OtrasLenguas/LlamadaPython.py)와 [C++ JNI invocar Ejemplos](Ejemplos/OtrasLenguas/LlamadaJava.cpp)도 제공한다.

`make`로 `build/JavaEspañol.jar`를 만든다. `javac -encoding UTF-8 -cp build/JavaEspañol.jar Ejemplos/Saludo.java`로 예제를 컴파일한다. 실행은 `java -cp build/JavaEspañol.jar:Ejemplos Saludo`operandoTercero.

`Saludo` 예제는 그래픽 화면이 없으면 Archivo·Caracteres·스레드 결과와 안내만 출력한다. Swing 창은 그래픽 세션에서 실행해야 한다. QEMU에서는 [그래픽 ejecutarComando Guía](../platforms/rpi4/README.md)의 `make run`으로 부팅한 valorLadoPosterior VNC 데스크톱의 터미널을 사용한다.

| valorClase | 제공 기능 |
|---|---|
| Archivo | UTF-8 텍스트·valorByte leer/escribir, 디렉터리·listaEntradaElemento |
| Caracteres | UTF-8 convertirValor, NFC normalizarValor, valorCódigo 포인트 númeroValor, 언어별 palabraLéxico valorFrontera |
| Comunicación | HTTP(S) petición, 제한시간을 가진 TCP conectar |
| Tarea | 스레드 ponerEnMarcha·합류·esperarValor, Tarea LanzadorPrograma |
| Pantalla | Swing 이벤트 처리와 ventana generar |
| EspacioTrabajo | fuente valorEditar·compilarFuente·ejecutarComando·ejecutarComando Archivo generar Pantalla |

`char`는 UTF-16 valorCódigo 단위이므로 이모지 등을 한 글자로 처리할 때 valorCódigo 포인트 또는 Caracteres valorFrontera API를 사용한다. 파일은 UTF-8로 저장한다. OpenJDK의 모든 Java2D/valorFuenteTipográfica/입력기 조합을 각각 검증한 것은 아니다.

이름은 elementoListaActual 의미가 분명한 español 용례를 사용했다. 개별 명칭의 역사적 어원 검토를 완료했다고 주장하지 않는다. valorRecurso 종료와 excepción 처리는 표준 API의 계약을 따른다.
