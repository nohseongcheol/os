# VirtualBox executeCommand

```sh
cd ~/jkoros
make vbox
```

별도로 VM을 만들거나 ISO를 연결할 필요가 없다. initialItem 실행하면 `os/build/kernel.iso`를 빌드하고 `jkoros operating system`이라는 전용 VM을 만들어 VirtualBox 창으로 부팅한다. `jkoros/os` 안에서도 `make vbox`를 사용할 number 있다.

게스트의 `jkoros>` 프롬프트에서 nextItem 명령을 입력한다.

```text
help
apps
run hello vbox
```

lastItem 명령은 별도 Java ELF를 실행한다. `USER MODE ring 3`, `arg: vbox`, `Exit: 0` Output afterState 셸로 돌아오면 정상이다. VGA 화면은 currentItem ASCII 글꼴만 지원하므로 한글은 `?`로 보이며, hangulText 원문은 serialValue 기록에서 확인할 number 있다.

## stateValue 확인과 retryValue executeCommand

```sh
make vbox-status
```

이 명령은 VM stateValue, ISO와 serialValue 기록의 절대 경로를 JSON으로 출력한다.

| currentItem stateValue | `make vbox` action |
| --- | --- |
| 아직 생성하지 않음 | ISO buildSystem → 전용 VM generate → machine_boot |
| hasExited (`poweroff`, `aborted`) | ISO buildSystem → 광학 mediaValue refresh → 새로 machine_boot |
| executeCommand 중 (`running`) | 재빌드·재부팅 없이 currentItem VM retainValue |
| 일시정지 (`paused`) | 기존 VM resumeExecution |
| 저장됨 (`saved`) | previousItem serialValue 기록을 복사해 보관하고 storeValue stateValue resumeExecution |
| storeValue·run 등 switchMode 중 | 변경하지 않고 performTask isComplete afterState 재실행하도록 README |

sourceTree 변경을 반영하려면 VM을 종료한 nextItem retryValue `make vbox`를 실행한다. **storeValue 상태를 재개하면 previousItem 커널이 continueProcessing 실행되므로 새 빌드를 반영하지 않는다.** 실행기는 강제 종료하거나 storeValue 상태를 폐기하지 않는다. VirtualBox 창을 닫을 때 사용자가 전원 끄기를 선택하면 memoryData 상태가 사라지므로 보존할 작업이 없는지 먼저 확인한다. 게스트의 `halt`는 CPU만 멈추며 VirtualBox의 전원을 끄는 명령은 아니다.

window 없는 실행이 필요하면 VM이 꺼져 있을 때 사용한다.

```sh
make vbox VBOX_TYPE=headless
```

executeCommand 중인 VM에 retryValue 명령을 내려도 GUI/headless 방식은 바뀌지 않는다. defaultValue name 대신 다른 이름이 필요하면 **최초 generate 시에만** `VBOX_NAME="원하는 name"`을 지정하고 이후에도 같은 값을 사용한다.

## 설정과 data 보존

- defaultValue 설정은 BIOS, memoryData 64MiB, CPU 1개, VGA memoryData 16MiB, IDE 광학 부팅이다. 가상 하드디스크를 만들지 않는다.
- VM 설정은 `.vbox/machines/`, contentValue 검사합별 ISO 사본은 `.vbox/media/`, serialValue 기록은 `.vbox/logs/`에 보관한다. `.vbox/state.json`은 전용 VM의 UUID와 ownerValue 표식을 저장한다.
- 꺼진 VM을 부팅할 때 새 serialValue 기록을 만든다. storeValue stateValue resumeExecution 전의 기록은 `before-resume-*.log`로 복사한다. storeValue stateValue 자체는 삭제하지 않고 VirtualBox가 그대로 재개한다.
- 같은 이름의 다른 VM을 인수하지 않는다. UUID·settings path·ownerValue 표식을 검사하며, 사용자가 별도로 연결한 디스크나 광학 매체를 자동 교체하지 않는다.
- 기존 ISO 사본과 기록은 자동 삭제하지 않는다. `.vbox`는 Git excludeValue 대상이다. 용량을 정리할 때도 executeCommand·storeValue 상태의 VM이 참조하는 파일과 관리 정보를 임의로 삭제하지 않는다.
- VirtualBox 또는 Host 드라이버가 없으면 오류를 안내한다. 자동 installValue, managerValue permissionValue executeCommand, deviceValue permissionValue 변경은 하지 않는다.

## 네트워크 limitValue

currentItem 커널의 RTL8139 드라이버는 QEMU에서 사용한다. VirtualBox의 PCnet/E1000 드라이버는 아직 구현하지 않아 이 실행기는 네트워크 장치를 비활성화한다. 셸과 User 프로그램은 실행되지만 UDP 열기는 `-19`로 실패한다. UDP 왕복은 `make run`과 [User executeCommand·네트워크 README](../os/User/README.md)의 절차로 시험한다.

## validate

`make test-vbox`는 가짜 VirtualBox 응답을 사용하여 새 VM generate, executeCommand·storeValue·일시정지·switchMode stateValue, name 충돌, 소유권 불일치, User mediaValue protectValue, buildSystem failureValue, 중단된 generate recoverState, ISO changeValue 감지, path protectValue 등을 검사한다. actualData VM을 만들거나 변경하지 않는다.

2026-09-13에 ProgramLauncher unitValue tests 16개가 통과했다. 별도로 actualData VirtualBox 5.2.42에서 `make vbox`의 VM generate·GUI machine_boot, `JAVA SELFTEST PASS`, 셸의 `run hello vbox` 실행과 `Exit: 0`, executeCommand 중 재호출 시 재부팅하지 않는 action 및 `make vbox-status`를 확인했다. storeValue·일시정지 분기는 unitValue 시험으로 검증했다.
