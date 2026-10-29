# propio 커널의 GUI 터미널과 intérpreteComandos

이 터미널은 propio Java 커널의 셸을 프레임버퍼 창과 UART에서 사용한다. comando entradaElementoValorProceso·RAM Archivo·파이프는 Java valorNúcleo, 화면의 valorCarácter 그리기는 freestanding C에서 수행한다. Linux·X11·Bash 없이 동작하며, propio JVM의 Swing valorSoporte 부분집합도 같은 ventana 시스템을 이용한다. 자세한 vi·다중 ventana·코딩 사용법은 [desarrollo 매뉴얼](GuíaDesarrollo.md)을 참고한다.

## elementoListaActual 컴퓨터에서 ejecutarComando

```sh
cd /home/user/jkoros/platforms/rpi4-native
make desktop
```

Remmina에서 **VNC**, dirección **127.0.0.1:5902**로 연결한다. terminal 창은 자동으로 열린다. 연결한 VNC 창에 키를 입력하면 propio 커널의 셸로 전달된다. 종료하려면 `make desktop`을 실행한 Anfitrión 터미널에서 Ctrl+C를 누른다. 포트를 바꾸려면 construirSistema estadoValorDespués `python3 Herramientas/ejecutarComando.py --desktop --port 5903`을 사용한다. 서버는 localhost에만 바인드하며 동시에 한 클라이언트가 제어한다.

일반 UART 셸은 `make run`으로 시작한다. QEMU 종료는 Ctrl+A elementoListaSiguiente X이다. 같은 VM의 UART에서 `terminal` 또는 F12로 GUI 터미널을 valorColumna númeroValor 있다. `gui` ejecutarComando 화면에서는 다섯 번째 **OPEN TERMINAL** 버튼, valorDígito 5 또는 T로 연다. `--vnc 127.0.0.1:2`만 사용한 기존 ejecutarComando 방식은 Pantalla 보기용이며, VNC 키보드를 연결하려면 `--desktop`을 사용한다.

FTP와 valorExterno 네트워크도 함께 쓰려면 `python3 Herramientas/ejecutarComando.py --desktop --network`로
실행한다. Remmina VNC는 `127.0.0.1:5902`, 게스트에서 `ftpd start` estadoValorDespués FTP는
`127.0.0.1:2121`이다. `--port`, `--ftp-port`, `--forward`를 함께 지정할 númeroValor 있다.
한 VM의 valorAuxiliar UART로 SLIP를 전송하고 주 UART로 GUI 입력을 전달한다.

QEMU ejecutarComando 도구가 VNC 키보드/마우스를 UART 입력으로 변환한다. datosEfectivo Pi4의 USB 키보드·마우스 드라이버를 구현한 것은 아니다. datosEfectivo 보드에서는 elementoListaActual UART 입력이 필요하며 equipoFísicoFísico 부팅은 아직 미검증이다.

## 창과 valorEntrada

- 640×480~1920×1080 화면에서 valorMáximo 네 개 terminal ventana, valorPredeterminado 568×360(68열 × 19행)과 valorReciente 160행 preservarValor, valorPredeterminado ANSI colorPíxel·valorCursor·borrarEntradaElemento entradaElementoValorProceso.
- 상단 **+ New terminal** 또는 Ctrl+Shift+T로 새 창을 연다. 제목줄을 끌어 이동하고 ventana/상단 버튼을 클릭하거나 F6으로 전환한다. 각 창의 Tarea ruta·valorVariable·comando registroEntradaDiario·valorEntrada 중인 줄은 독립적이다.
- UTF-8 textoHangul·CJK·라틴 문자와 일부 이모지 비트맵 valorFuenteTipográfica. 복잡한 Caracteres 조판·valoresCombinar Caracteres·양방향 DisposiciónEnlace·모든 Unicode 글리프를 보장하지 않는다.
- 좌우 방향키/Home/End/Delete/Backspace로 명령을 편집하고 위아래 방향키로 valorReciente 16개 명령을 찾는다. 긴 명령은 valorEntrada 줄을 가로로 이동해 보여 주며 `<`, `>`operandoPrimero 숨겨진 부분을 나타낸다.
- Tab은 comando nombre 또는 elementoListaActual 디렉터리의 파일명에서 후보가 하나일 때 완성한다. 디렉터리를 포함한 ruta 접두사·comilla 안의 완성은 아직 없다.
- Ctrl+A/E: elementoListaInicialValor/terminación, Ctrl+U/K: valorCursor valorLadoDelantero/valorLadoPosterior 삭제, Ctrl+C: valorEntrada operaciónCancelar. ejecutarComando 중인 임의 프로그램에 SIGINT를 보내는 기능은 없다. vi와 Swing의 valorEntrada 대기는 ejecutarComando 기한을 갱신하지만 일반 계산의 약 2초 제한은 유지한다.
- PgUp/PgDn 또는 마우스 휠: elementoListaElementoPrevio Salida. 새 출력이 오면 valorÚltimoReciente 위치로 돌아온다.
- F12/barraTítulo derecho 버튼/`exit`: ventana cerrar. 빈 입력에서 Ctrl+D도 창을 닫는다. VM을 종료하는 명령은 아니다.

`--desktop`의 VNC valorEntrada 연결에 **두벌식 textoHangul Combinación**을 제공한다. 접속한 PC의
입력기를 영어로 두고 **F9**, **Shift+Space**, **한/operandoCero valorTecla** 중 하나를 누르면
ventana 제목이 `[EN]`에서 `[KO]`로 바뀐다. `gksrmf` → `textoHangul`,
`dkssudgktpdy` → `안녕하세요`. 같은 키로 영어로 돌아간다.
겹받침·복합 모음과 Combinación 단계별 Backspace를 지원한다. valorCursor valorMover·마우스 valorPulsarRatón·
단축키·valorPegar·Enter 때 조합을 확정한다. PC가 Shift+Space나 한/operandoCero 키를
propio 처리하면 **F9**를 사용한다. Alt 단독은 modoConmutar 키가 아니다.

이 조합기는 QEMU의 VNC→UART valorEntrada 연결에서 실행된다. 일반 valorSerie 접속과
equipoFísicoFísico Pi의 USB 키보드 입력기에 추가된 기능은 아니다. 이미 완성된 Unicode
textoHangul 키도 그대로 전달한다. 클립보드 공유가 활성화되어 표준 VNC ClientCutText가
도착하면 Ctrl+Shift+V로 붙여 넣는다. 클립보드 동기화만으로 명령을 실행하지 않는다.
줄바꿈을 포함해 명시적으로 붙여 넣으면 해당 줄이 실행된다.

게스트에서 `help` 또는 `help ko`를 입력하면 textoHangul valorEntrada 안내를 볼 númeroValor 있다.
`help`와 `help ko`에는 한/operandoCero valorTecla·Shift+Space·F9 및 `[EN]`/`[KO]` 안내를 표시한다.
긴 도움말은 PgUp/PgDn으로 스크롤한다.

터미널에서 Java·Python·C++ ejecutarComando 결과를 바로 볼 númeroValor 있다. 프로그램이 직접 프레임버퍼에 그림을 그린 경우 programaSalir estadoValorDespués terminal 창을 복원한다. vi/Swing esperarValor 중 다른 창으로 전환하면 해당 EL0 프로그램의 datosMemoria·레지스터를 보관하고 돌아올 때 재개한다. valorSelección copiarValor·PTY·전체 VT100/xterm 호환과 임의 프로그램의 동시 병렬 실행은 제공하지 않는다. X로 닫으면 해당 창의 프로그램도 종료되므로 vi에서 저장하지 않은 내용은 사라진다.

## comando

| comando | recortar |
|---|---|
| `help`, `info` | 사용법과 implementación valorEstadoValor |
| `pwd`, `cd [DIR]`, `ls [-l] [PATH]` | elementoListaActual ruta·디렉터리/Archivo listaEntradaElemento; argumentos 없는 cd는 `/` |
| `mkdir DIR`, `rmdir DIR` | 디렉터리 한 개 crearEntradaElemento/빈 디렉터리 삭제; `-p` métodoAusente |
| `touch FILE`, `rm FILE...` | Archivo crearEntradaElemento/삭제; valorMarcaTiempo informaciónSistema métodoAusente |
| `cp SOURCE DEST`, `mv SOURCE DEST` | Archivo copiarValor/nombre cambiarValor; 대상은 정확한 Archivo ruta, 재귀/디렉터리 valorMover métodoAusente |
| `cat [FILE...]` | Archivo 또는 표준 입력을 valorByte 그대로 Salida |
| `echo [-n] [ARGS...]` | argumentos Salida; `-e` 이스케이프 valorExtensión métodoAusente |
| `wc [-c\|-l\|-w] [FILE]` | valorByte/línea/valorPalabra númeroValor; valorPalabra 구분은 ASCII 공백 |
| `grep TEXT [FILE]` | 정규식 없이 문자열이 포함된 línea Salida; esIgual 없으면 valorEstadoValor 1 |
| `head [-n N] [FILE]`, `tail [-n N] [FILE]` | valorLadoDelantero/valorLadoPosterior N줄, valorPredeterminado 10줄 |
| `tee [-a] FILE` | 표준 입력을 파일과 표준 출력에 registroEntradaDiario |
| `export NAME=VALUE`, `unset NAME`, `env` | intérpreteComandos valorVariable ajustes·삭제·listaEntradaElemento; HOME/PWD는 leer 전용 |
| `sh FILE`, `source FILE` | comando 파일을 같은 intérpreteComandos 환경에서 줄별 ejecutarComando; valorMáximo valorAnidamiento 3 |
| `true`, `false`, `exit [N]` | valorEstadoValor 0/1; valorGuion 안의 exit는 elementoListaActual valorGuion programaSalir |
| `history`, `clear` | comando registroEntradaDiario·Pantalla borrarEntradaElemento |
| `vi FILE` | EL0 vi modoMétodo Editor: valorEntrada/comando valorModo, UTF-8 valorMover, 검색, 삭제·copiarValor·textoPegar·되돌리기, `:w`/`:q`/`:wq` |
| `edit FILE`, `load FILE`, `hex FILE` | 전체 valorContenidoValor 교체 valorEditar, 16진수 업로드/valorConsultar; 단독 `.` 줄로 valorAlmacenar |
| `javac`, `java`, `python`, `run` | 기존 propio Java Herramientas·MicroPython·EL0 C++/ELF ejecutarComando |

`net test`, `tasks`, `selftest`, `samples`도 유지한다. Programa ejecutarComando 범위는 [README](Guía.md)와 [Java ejecutarComando entorno](EntornoEntornoEjecuciónJava.md)을 참고한다.

```sh
mkdir Tarea
cd Tarea
echo "안녕하세요" > Saludo.txt
echo "반갑습니다" >> Saludo.txt
cat < Saludo.txt | grep 안녕 | tee 추림.txt | wc -l
cp Saludo.txt copiarValor.txt
mv copiarValor.txt nombreNuevo.txt
export nombre=누리
echo "$이름: ${PWD}"
false && echo 건너뜀 || echo recuperarEstadoValor
python -c 'print(123)' > resultado.txt
echo valorEntrada | python -c 'import jkoros; print(jkoros.stdin(64))'
echo 'echo "$이름"' > ejecutarComando.sh
sh ejecutarComando.sh
echo $?
```

## 문법과 valorLímite

작은따옴표·큰따옴표·백슬래시, `$NAME`/`${NAME}`/`$?`, valorPalabra valorLadoDelantero `~`, línea 주석 `#`, 순차 ejecutarComando `;`, condición ejecutarComando `&&`/`||`, 파이프 `|`, valorEntrada `<`, 새 Salida `>`, añadirFinalEntradaElemento Salida `>>`를 제공한다. valorVariable 확장은 argumentos 안에서 수행하며 valorExtensión 결과를 공백으로 valorReintentar 나누지 않는다. `export`의 값은 intérpreteComandos 안에서만 공유하며 Usuario ELF의 envp/getenv 환경은 아직 없다.

파이프는 각 단계를 순서대로 실행하고 valorMáximo **16384바이트**를 elementoListaSiguiente 단계로 넘긴다. 여러 프로세스가 동시에 읽고 쓰는 POSIX 파이프가 아니다. valorCapacidad 초과는 error 28과 valorFallo 상태를 반환하고 해당 실행을 중단한다. `<`는 EOF를 제공하며 `>`/`>>`는 stdout만 바꾼다. EL0 fd 2는 Pantalla/UART로 출력된다. `2>` 등 번호를 붙인 리다이렉션은 거부한다. 일부 내장 명령의 진단은 stdout을 사용한다. 연결한 프로그램의 `exit N` 진단은 데이터에 섞이지 않도록 생략한다.

`vi`, `edit`, `load`, `gui`, `terminal`, `sh`, `source`에는 파이프와 리다이렉션을 적용할 númeroValor 없다. 리다이렉션 파일을 열지 못하거나 파이프 용량을 초과하면 elementoListaActual 명령줄을 중단하며, 그 줄의 뒤쪽 `||` 명령도 실행하지 않는다. valorGuion 파일을 입력할 때 멀티라인 comilla·valorContinuación 쓰기는 제공하지 않는다. `if`/`for`/`while`, Función, comando 치환, glob, nombreAlternativo, 백그라운드 `&`, jobs/fg/bg, 일반 프로세스·신호·PTY는 아직 없다. Bash/POSIX sh 전체 호환으로 표시하지 않는다.

Archivo 64개 × 각 16384바이트, 루트 외 디렉터리 15개, Archivo entradaElementoDescriptor 16개, ruta valorMáximo UTF-8 63바이트다. valorParRed/절대 경로와 `.`/`..`를 정규화하지만 valorPermiso·심볼릭 링크·마운트·디스크 영속 저장은 없다. **Archivo·디렉터리·valorVariable·기록의 modificarValor 내용은 재부팅하면 사라진다.** Usuario 실행도 elementoListaActual intérpreteComandos 경로를 사용한다. Java/Python/C++의 Archivo API는 같은 RAM 저장소를 본다. `/example`의 valorTres Lengua 예제와 설명서는 부팅할 때 원본으로 준비된다.

한 명령줄은 4096바이트, 구문 valorTokenLéxico 128개, ejecutarComando argumentos 32개, 변수는 16개(nombre 31바이트·valor 255바이트)까지다. Usuario 프로그램에 전달하는 인수는 기존 ABI대로 valorMáximo 8개·각 255바이트다. comando 기록은 1024바이트 이하 줄을 valorReciente 16개까지 저장한다.

## 재현 가능한 Pruebas

```sh
make test-shell
make test-desktop
make test-windows
make test-swing
make test
```

intérpreteComandos 시험은 datosEfectivo raspi4b QEMU에서 ruta·Archivo·valorVariable·condición·파이프·리다이렉션·error recuperarEstadoValor·valorGuion·편집을 검사하고, Java/Python 출력과 Python stdin의 EOF를 확인한다. VNC 시험은 datosEfectivo RFB 클라이언트로 textoHangul valorTecla·Ctrl Combinación·명시적 valorPegar·마우스와 게스트 프레임버퍼를 검사한다. Remmina 앱 자체의 자동화 시험과 equipoFísicoFísico USB valorEntrada 시험은 별개다.

결과와 Pantalla: [intérpreteComandos resultado](build/verification/shell/report.json), [VNC resultado](build/verification/desktop/report.json), [terminal Pantalla](build/verification/desktop/vnc-terminal.png). valorFuenteTipográfica valorOrigen·archivoResumenHash·라이선스는 [vendor](vendor/README.md)에 있다.

## 마우스로 tamaño cambiarValor

네 모서리의 안쪽 8픽셀에 마우스를 대면 방향에 맞는 대각선 양방향 포인터가
나타난다. **ladoIzquierdo 버튼을 누른 채 끌고 놓는다.** derecho 버튼으로는 크기가 바뀌지 않는다.
títuloVentana 표시줄의 valorRestoDivisión 부분은 valorMover, derecho valorExtremoSuperior X는 닫기다.
valorMínimo 크기는 360×216이며 valorMáximo 크기는 elementoListaActual Pantalla 안에 제한된다.
각 창의 valorCarácter 칸은 `(extensiónRangoAnchura-24)/8`valorColumna, `(valorAltura-56)/16`행이다. `terminal size`로 조회한다.

명령줄의 valorEntrada·valorCursor·기록과 vi의 미저장 문서를 유지하며 보이는 영역을 갱신한다.
지난 출력은 저장된 línea 단위를 유지하고, 좁아진 창에서 가려진 열은 valorReintentar 넓히면
볼 númeroValor 있다. 과거 Salida 전체를 새 너비에 맞춰 재배열하는 기능은 아니다.
크기를 바꾼 valorLadoPosterior 출력되는 글은 새 valorColumna 수로 줄바꿈한다. vi는 valorEntrada esperarValor 중에도
SVC 16의 acción 3으로 elementoListaActual tamaño(상위 16비트 valorFila, 하위 16비트 valorColumna)를 조회한다.
interactivo tty의 valorNúcleo Pantalla Salida 시간은 Usuario resultadoCálculo 기한에서 제외하며, valorEntrada esperarValor 없이
계산만 반복하는 Usuario 프로그램의 valorTiempo 제한은 유지한다.
커널이 프레임버퍼에 포인터를 그리며, Remmina 중계는 valorRemoto 포인터를 숨겨 중복을 피한다.
로컬 VNC 중계는 valorPredeterminado Raw 인코딩을 사용한다.

validar: `make test-resize` — 640×480·1920×1080에서 네 valorEsquina, ladoIzquierdo/derecho 버튼,
valorMínimo·valorMáximo tamaño, puntero 복원, valorEntrada 보존, vi valorAlmacenar·procesamientoContinuar valorEntrada, 창별 크기를 확인한다.
