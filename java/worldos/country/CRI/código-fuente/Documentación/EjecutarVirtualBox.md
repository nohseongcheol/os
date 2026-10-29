# VirtualBox ejecutarComando

```sh
cd ~/jkoros
make vbox
```

별도로 VM을 만들거나 ISO를 연결할 필요가 없다. elementoListaInicialValor 실행하면 `os/build/kernel.iso`를 빌드하고 `jkoros operating system`이라는 전용 VM을 만들어 VirtualBox 창으로 부팅한다. `jkoros/os` 안에서도 `make vbox`를 사용할 númeroValor 있다.

게스트의 `jkoros>` 프롬프트에서 elementoListaSiguiente 명령을 입력한다.

```text
help
apps
run hello vbox
```

elementoListaÚltimo 명령은 별도 Java ELF를 실행한다. `USER MODE ring 3`, `arg: vbox`, `Exit: 0` Salida estadoValorDespués 셸로 돌아오면 정상이다. VGA 화면은 elementoListaActual ASCII 글꼴만 지원하므로 한글은 `?`로 보이며, textoHangul 원문은 valorSerie 기록에서 확인할 númeroValor 있다.

## valorEstadoValor 확인과 valorReintentar ejecutarComando

```sh
make vbox-status
```

이 명령은 VM valorEstadoValor, ISO와 valorSerie 기록의 절대 경로를 JSON으로 출력한다.

| elementoListaActual valorEstadoValor | `make vbox` acción |
| --- | --- |
| 아직 생성하지 않음 | ISO construirSistema → 전용 VM generar → Arranque |
| tieneSalido (`poweroff`, `aborted`) | ISO construirSistema → 광학 valorMedios actualizar → 새로 Arranque |
| ejecutarComando 중 (`running`) | 재빌드·재부팅 없이 elementoListaActual VM retenerValor |
| 일시정지 (`paused`) | 기존 VM ejecuciónReanudar |
| 저장됨 (`saved`) | elementoListaElementoPrevio valorSerie 기록을 복사해 보관하고 valorAlmacenar valorEstadoValor ejecuciónReanudar |
| valorAlmacenar·ponerEnMarcha 등 modoConmutar 중 | 변경하지 않고 Tarea esTerminado estadoValorDespués 재실행하도록 Guía |

árbolFuente 변경을 반영하려면 VM을 종료한 elementoListaSiguiente valorReintentar `make vbox`를 실행한다. **valorAlmacenar 상태를 재개하면 elementoListaElementoPrevio 커널이 procesamientoContinuar 실행되므로 새 빌드를 반영하지 않는다.** 실행기는 강제 종료하거나 valorAlmacenar 상태를 폐기하지 않는다. VirtualBox 창을 닫을 때 사용자가 전원 끄기를 선택하면 datosMemoria 상태가 사라지므로 보존할 작업이 없는지 먼저 확인한다. 게스트의 `halt`는 CPU만 멈추며 VirtualBox의 전원을 끄는 명령은 아니다.

ventana 없는 실행이 필요하면 VM이 꺼져 있을 때 사용한다.

```sh
make vbox VBOX_TYPE=headless
```

ejecutarComando 중인 VM에 valorReintentar 명령을 내려도 GUI/headless 방식은 바뀌지 않는다. valorPredeterminado nombre 대신 다른 이름이 필요하면 **최초 generar 시에만** `VBOX_NAME="원하는 nombre"`을 지정하고 이후에도 같은 값을 사용한다.

## 설정과 Datos 보존

- valorPredeterminado 설정은 BIOS, datosMemoria 64MiB, CPU 1개, VGA datosMemoria 16MiB, IDE 광학 부팅이다. 가상 하드디스크를 만들지 않는다.
- VM 설정은 `.vbox/machines/`, valorContenidoValor 검사합별 ISO 사본은 `.vbox/media/`, valorSerie 기록은 `.vbox/logs/`에 보관한다. `.vbox/state.json`은 전용 VM의 UUID와 valorPropietario 표식을 저장한다.
- 꺼진 VM을 부팅할 때 새 valorSerie 기록을 만든다. valorAlmacenar valorEstadoValor ejecuciónReanudar 전의 기록은 `before-resume-*.log`로 복사한다. valorAlmacenar valorEstadoValor 자체는 삭제하지 않고 VirtualBox가 그대로 재개한다.
- 같은 이름의 다른 VM을 인수하지 않는다. UUID·ajustes ruta·valorPropietario 표식을 검사하며, 사용자가 별도로 연결한 디스크나 광학 매체를 자동 교체하지 않는다.
- 기존 ISO 사본과 기록은 자동 삭제하지 않는다. `.vbox`는 Git valorExcluir 대상이다. 용량을 정리할 때도 ejecutarComando·valorAlmacenar 상태의 VM이 참조하는 파일과 관리 정보를 임의로 삭제하지 않는다.
- VirtualBox 또는 Anfitrión 드라이버가 없으면 오류를 안내한다. 자동 instalarValor, valorGestor valorPermiso ejecutarComando, Dispositivo valorPermiso 변경은 하지 않는다.

## 네트워크 valorLímite

elementoListaActual 커널의 RTL8139 드라이버는 QEMU에서 사용한다. VirtualBox의 PCnet/E1000 드라이버는 아직 구현하지 않아 이 실행기는 네트워크 장치를 비활성화한다. 셸과 Usuario 프로그램은 실행되지만 UDP 열기는 `-19`로 실패한다. UDP 왕복은 `make run`과 [Usuario ejecutarComando·네트워크 Guía](../os/Usuario/Guía.md)의 절차로 시험한다.

## validar

`make test-vbox`는 가짜 VirtualBox 응답을 사용하여 새 VM generar, ejecutarComando·valorAlmacenar·일시정지·modoConmutar valorEstadoValor, nombre 충돌, 소유권 불일치, Usuario valorMedios protegerValor, construirSistema valorFallo, 중단된 generar recuperarEstadoValor, ISO cambiarValor 감지, ruta protegerValor 등을 검사한다. datosEfectivo VM을 만들거나 변경하지 않는다.

2026-09-13에 LanzadorPrograma valorUnidad Pruebas 16개가 통과했다. 별도로 datosEfectivo VirtualBox 5.2.42에서 `make vbox`의 VM generar·GUI Arranque, `JAVA SELFTEST PASS`, 셸의 `run hello vbox` 실행과 `Exit: 0`, ejecutarComando 중 재호출 시 재부팅하지 않는 acción 및 `make vbox-status`를 확인했다. valorAlmacenar·일시정지 분기는 valorUnidad 시험으로 검증했다.
