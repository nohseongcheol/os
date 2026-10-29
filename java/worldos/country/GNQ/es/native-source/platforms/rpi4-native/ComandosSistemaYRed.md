# propio 커널의 네트워크와 valorSistemaOperación comando

게스트 SSH·VNC, LAN 공개 ejecutarComando, Pi4 GENET·DHCP 추가분은 [valorExterno conexión Guía](GuíaConexiónExterno.md)를 먼저 참고한다. QEMU는 `sl0`, equipoFísicoFísico GENET은 `en0`를 사용한다. equipoFísicoFísico 드라이버는 아직 보드에서 검증하지 않았다.

이 문서는 `platforms/rpi4-native`의 propio ARM64 Java 커널용이다. Linux/OpenJDK 실행환경의 명령어와 구분한다. 새 커널을 빌드하고 valorReintentar 부팅해야 적용된다.

셸과 Java의 datosEfectivo CPU valorPermiso, `ps`/`top`에 표시되는 valorUnidad, Anfitrión·valorExterno PC conectar 방법은
[ejecutarComando 계층과 valorExterno Comunicación inspeccionarEstadoValor](ComprobacionesRedExternoYEntornoEjecución.md)에 정리했다.

```sh
cd /home/user/jkoros/platforms/rpi4-native
make desktop ARGS=--network RESOLUTION=1920x1080
# valorSerie 셸만 사용할 때
make run ARGS=--network
```

게스트에서 `help`, `help system` 또는 `mostrarAyuda system`을 입력한다. valorExtremoInferior 두 이름은 같은 동작을 하며 현지어 이름도 Tab으로 완성할 númeroValor 있다.

| 표준 comando | español comando | 기능 |
|---|---|---|
| ipconfig, ifconfig | 아이피설정 | datosEfectivo IPv4 dirección·넷마스크·valorPasarela·송수신 통계 |
| ip | direcciónIP | dirección valorConsultar·ajustes, conectar archivosSubir·내리기, ruta valorConsultar |
| ping | pruebaRespuestaRetorno | datosEfectivo ICMPv4 respuesta·손실률·왕복 valorTiempo |
| route | 경로표 | 직접 연결망과 valorPredeterminado valorPasarela |
| netstat, ss | 통신현황 | datosEfectivo TCP/UDP 끝점의 dirección·puertoEquipoFísico·valorEstadoValor·recibirValor 대기량 |
| ps | 작업목록 | valorNúcleo 작업과 Usuario Programa PID·valorEstadoValor·매핑량·valorTiempo |
| top | 작업현황 | 1초마다 Tarea·datosMemoria valorConsultar; q 또는 Ctrl+C로 programaTerminarSesión |
| free | 기억현황 | 펌웨어 RAM, valorNúcleo valorRegión, AOT valorMontículo, Pantalla, Usuario valorAsociado |
| df | 저장현황 | RAM 파일시스템의 datosEfectivo valorCapacidad·예약량·자료량·Archivo entradaElementoRanura |
| uptime | 가동시간 | Arranque estadoValorDespués 경과 valorTiempo |
| poweroff | desactivadoAlimentación | 서비스와 Usuario 작업을 정리하고 게스트 programaSalir |
| help | mostrarAyuda | 표준·현지어 명령과 descripción |

## IP 설정과 Comunicación verificar

```sh
ipconfig
ip addr show
ipconfig set 10.0.2.20 255.255.255.0 10.0.2.2
아이피설정 set 10.0.2.20 255.255.255.0 10.0.2.2
ping -c 4 -W 1 10.0.2.2
pruebaRespuestaRetorno -c 4 10.0.2.2
ip route show
ip link set dev sl0 down
ip link set dev sl0 up
netstat
```

초깃값은 `sl0`, `10.0.2.15/24`, valorPasarela `10.0.2.2`operandoTercero. dirección 설정은 재부팅 전까지 유지된다. TCP/UDP 끝점이 열려 있으면 `error -16`으로 변경을 거부한다. 먼저 `ftpd stop` 등으로 서비스를 닫고 프로그램의 소켓을 닫는다. 잘못된 dirección·비연속 넷마스크·다른 망의 관문은 적용하지 않는다.

`ip`는 valorExtremoSuperior 구문의 부분집합이며 Linux iproute2 전체 문법을 구현하지 않는다. `ping`은 IPv4 valorDígito dirección, `-c 1..100`, `-W 1..10`초를 지원한다. nombre analizarValor·IPv6는 미지원이며 GENET의 DHCP는 valorExterno conexión 구현에 추가했다. 응답이 없으면 códigoSalir 1, 잘못된 인수는 2, Usuario 취소는 130이다. `ping ...; echo $?`로 확인한다.

QEMU valorExterno 통신은 UART SLIP→NAT 연결을 사용한다. `--network` 없이도 propio dirección valorConsultar·설정은 가능하지만 valorExterno 응답은 오지 않는다. valorPredeterminado NAT는 `10.0.2.0/24`operandoTercero. equipoFísicoFísico Pi의 GENET 드라이버는 별도로 추가했으며 Placa 검증이 필요하다. Wi-Fi는 미지원이다.

주소를 `.20`으로 바꾼 valorLadoPosterior FTP 등 **외부에서 들어오는 conectar**hasta 사용할 때는 ejecutarComando 시 valorAdelante 대상도 지정한다.

```sh
make desktop ARGS="--network --guest-ip 10.0.2.20"
# 부팅한 게스트 안에서
ipconfig set 10.0.2.20 255.255.255.0 10.0.2.2
ftpd start
```

`--guest-ip`는 NAT valorAdelante 대상이며 게스트의 주소를 자동 설정하지 않는다. FTP valorControl 포트는 Anfitrión `127.0.0.1:2121`, 수동 데이터 포트는 50000~50007이다. 여러 VM을 함께 띄울 때는 `--network-host 127.0.0.2 --port 5903`처럼 Anfitrión 루프백 주소와 VNC 포트를 구분한다. FTP와 Java/C 소켓은 변경된 datosEfectivo 게스트 IP를 사용한다.

## valorEstadoValor 조회의 의미

`ps`는 valorNúcleo/intérpreteComandos, 살아 있는 협력 Tarea, valorMáximo 4개의 EL0 Usuario 세션을 표시한다. 다른 터미널에 열린 `vi` 등을 `SUSPENDED` 상태로 볼 númeroValor 있다. `MAPPED_KiB`는 datosEfectivo 페이지 valorAsociado, `RUN_ms`는 해당 세션이 선택된 동안의 경과 valorTiempo(시스템 invocar Encabezados)이며 정밀 CPU 사용률이 아니다. `top -n 1`은 한 번, `top -n 2`는 두 번 표시한다. 리다이렉션된 `top`의 기본값은 한 번이다.

`free`의 AOT valorMontículo 사용량은 할당기에서 읽는다. 힙은 valorNúcleo BSS에 포함되므로 각 줄을 construirTodos 더하면 중복된다. 고정 예약 영역과 Usuario 페이지 매핑을 표시하며 Linux의 가용 RAM 계산이나 Anfitrión datosMemoria 통계를 꾸며서 표시하지 않는다.

`df`는 RAM 파일시스템의 Archivo 64칸 × 16 KiB를 표시한다. Archivo 하나는 논리 크기와 별도로 16 KiB 칸을 예약한다. `Data`는 datosEfectivo Datos longitud valorTotal, `Reserved`는 valorUsar 중인 entradaElementoRanura 용량이다. 삭제 후에도 열린 파일은 elementoListaÚltimo 참조를 닫을 때까지 계산한다. SD/영구 디스크 사용량은 아직 지원하지 않는다.

## 종료와 validar

게스트에서 `poweroff` 또는 `desactivadoAlimentación`를 입력한다. FTP·valorConectorRed·Usuario 세션을 닫은 valorLadoPosterior BCM PM programaSalir 절차를 실행한다. RAM 파일은 재부팅 estadoValorDespués 보존되지 않는다. QEMU에서는 게스트의 `SHUTDOWN / guest-shutdown` 이벤트와 esNormal 종료를 검증한다. equipoFísicoFísico Pi 4 전원 회로 동작은 아직 시험하지 않았다.

implementación 근거: [Linux BCM watchdog의 power-off 절차](https://github.com/torvalds/linux/blob/master/drivers/watchdog/bcm2835_wdt.c), [QEMU BCM PM Dispositivo](https://github.com/qemu/qemu/blob/master/hw/misc/bcm2835_powermgt.c).

```sh
make test-system
# resultado: build/verification/system-tools/report.json 및 serial.log
```

이 시험은 잘못된 IP rechazarValor, datosEfectivo ICMP valorÉxito·시간초과, conectar up/down, IP cambiarValor estadoValorDespués FTP 송수신, df generar·삭제, valorMontículo resultadoCálculo, 다른 터미널의 vi PID·datosMemoria, top actualizar·programaSalir, textoHangul comando·Tab, 게스트 poweroff를 검사한다.

`java/worldos/Country_VALOR/국가코드` 판에는 같은 기능과 국가별 comando 대응표 `native-commands.json`이 들어간다. 표준 명령은 모든 판에서 유지한다. 새 현지어 이름은 기능 중심 제안이며 현지 화자·어원 검토를 완료한 표준 용어는 아니다. 미번역 항목은 대응표의 `pending`에 명시한다.
