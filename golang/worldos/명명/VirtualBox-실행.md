# VirtualBox 실행

## 기본 명령

```sh
cd ~/golang/worldos/나라/KOR
make vbox
```

처음에는 `worldos KOR`라는 전용 가상 머신을 등록하고 창으로 실행한다. VirtualBox 설정 화면에서 미리 가상 머신을 만들 필요가 없다. 기존 `koros4 operating system`이나 `eng operating system` 가상 머신의 설정은 변경하지 않는다.

다른 판에서도 해당 폴더에서 같은 명령을 사용한다.

```sh
make -C ~/worldos/나라/JPN vbox
make -C ~/worldos/나라/USA vbox
make -C ~/worldos/문자판/JPN/ja_Hira vbox
make -C ~/worldos/문자판/JPN/ja_Kana vbox
make -C ~/worldos/문자판/CHN/zh_Hant vbox
make -C ~/worldos/문자판/IND/ta_Taml vbox
```

WorldOS 최상위 폴더에서는 `make vbox COUNTRY=KOR`, `make script-vbox VARIANT=JPN/ja_Hira`도 가능하다. 실행기의 적용 범위는 독립 소스를 갖춘 249개 국가판과 46개 문자판이다. `언어/` 아래의 카탈로그 전용 설정 폴더는 이 295개 독립 운영체제에 포함되지 않는다. 전체 경로는 [VirtualBox 목록](../VirtualBox-목록.tsv)을 참고한다.

## 자동으로 준비하는 항목

1. 해당 폴더의 독립 POSIX 함수모음과 명령해석기를 빌드한다.
2. 해당 폴더의 커널을 다시 빌드하고 부팅 ISO를 만든다.
3. 최초 실행에는 기존 부팅 디스크를 새 VDI로 복제한 뒤, 해당 판의 셸·대기 프로그램·실행 시험 프로그램·현지어 명령 예제를 넣는다.
4. 전용 가상 머신에 디스크와 ISO를 연결하고 VirtualBox 창으로 실행한다.

VM 설정은 메모리 512 MiB, CPU 1개, BIOS, PIIX3 칩셋과 PIIX4 IDE다. 디스크는 IDE 포트 0/장치 1, CD는 포트 1/장치 0에 연결한다. 이는 현재 커널이 사용하는 디스크 위치다. 커널·셸 소스는 다른 국가판에서 가져오지 않는다.

셸이 준비되면 직렬 로그에 `WORLDOS-SHELL:READY`가 나온다. 창에서는 `help`, `pwd`, `echo hello` 등을 입력할 수 있다. 현재 자판의 직접 입력 제약 때문에 현지어 명령 예제는 `source /commands`로 실행할 수 있다. 기존 커널의 진단 출력이 셸 화면과 섞일 수 있다.

현재 VGA 문자 화면에는 한글 등 UTF-8 글자가 깨져 보이는 기존 표시 제약도 있다. 이번 변경은 실행·빌드 연결을 위한 것으로, 글꼴 렌더러나 자판 입력기를 새로 구현한 것은 아니다.

## 상태·로그와 보존 정책

```sh
make vbox-status   # 가상 머신 상태, 디스크, ISO, 직렬 로그 경로
make vbox-check    # 해당 판의 실행기·셸·POSIX 연결 확인, VM 변경 없음
make vbox-prepare  # 빌드 및 VM 준비까지만 수행
```

각 판의 `.vbox/`에는 다음 항목이 저장된다.

- `state.json`: 이 판이 만든 VM의 UUID, 소유 표식, 미디어 이력
- `machines/`: 전용 VM 설정
- `media/`: 실행용 VDI와 내용 해시로 구분한 ISO 사본
- `logs/`: 실행별 빌드 기록과 직렬 출력

실행 중 `make vbox`를 다시 호출하면 `ALREADY_RUNNING`을 출력하고 빌드·디스크 교체·강제 종료 없이 끝난다. 저장됨(`saved`) 상태이면 저장된 실행 상태를 다시 시작하고, 일시 정지(`paused`) 상태이면 기존 VM을 재개한다. 이때는 `RESUMED`를 출력하며 재빌드·VM 설정 변경·디스크/ISO 교체를 하지 않는다. 일시 정지된 VM은 기존 표시 방식을 유지한다.

소스 변경을 반영하려면 사용자가 먼저 VM을 종료하여 `poweroff` 상태로 만든 뒤 다시 실행해야 한다. 저장됨 상태에서 재개하면 저장 당시의 커널과 프로그램이 이어서 실행된다. `make vbox-prepare`는 VM을 실행하는 명령이 아니므로 저장됨·일시 정지 상태에서는 재개하지 않고 안내 후 중단한다. 저장·복원·종료 진행 중인 상태에서는 작업이 끝난 후 다시 시도한다. 재개에 실패하더라도 저장 상태를 버리거나 강제로 새로 부팅하지 않는다.

`PGMSyncCR3 ... VERR_PGM_NO_HYPERVISOR_ADDRESS` 같은 오류는 실행기의 저장 상태 차단이 아니라 VirtualBox 내부의 복원 실패다. 현재 환경의 추가 시험에서 정상 재개 후 새로 저장된 상태를 복원할 때 이 오류가 재현됐다. 해당 로그에는 `AMD-V is not available`과 소프트웨어 가상화(`raw-mode`) 사용도 기록되어 있다. 실행기는 이를 자동 초기화로 해결하지 않는다. 저장 상태 삭제는 메모리에만 남은 작업을 잃을 수 있으므로, 복원 환경 점검 또는 상태 백업 후 새 부팅 여부를 사용자가 결정해야 한다.

정지 상태에서 셸 관련 빌드 결과가 같으면 현재 디스크를 재사용한다. 결과가 바뀌면 **현재 사용 디스크의 복제본**에 프로그램을 갱신하고 이전 디스크도 남긴다. 따라서 기존 사용자 데이터는 복제본에도 유지되지만, `USER1`, `USER2`, `USER3`, `SHEXEC`, `COMMANDS`는 실행기가 관리하는 프로그램 파일이므로 갱신될 수 있다. ISO도 별도 사본을 연결하므로 소스의 일반 `make iso`나 `make clean`이 실행 중인 ISO를 덮어쓰지 않는다.

`.vbox/`는 임시 폴더가 아니라 사용자 데이터가 있는 실행 환경이다. 자동 정리나 삭제를 하지 않으므로 세대가 늘면 디스크 공간도 증가한다. 다른 미디어를 수동 연결하거나 소유 표식을 바꾸면 실행기는 덮어쓰기 대신 중단한다. 아래 조건으로 확인된 폴더 이동은 자동 복구하며, 이동과 무관하게 수동으로 등록을 해제한 경우에는 기존처럼 중단한다.

## 작업 폴더를 옮긴 경우

`/home/user/worldos`에서 `/home/user/golang/worldos`로 옮긴 뒤에도 다음 명령을 그대로 쓴다.
경로를 스크립트에서 직접 수정할 필요가 없다.

```sh
cd /home/user/golang/worldos/나라/KOR
make vbox
# 또는 다른 디렉터리에서:
make -C /home/user/golang/worldos/나라/KOR vbox
```

`vbox.py`가 있는 현재 판을 기준으로 파일을 찾는다. `.vbox/state.json` 버전 2는
`disk`, `iso`, `serial_log`, `media_history`와 관리 디스크의 세대 경로를
`.vbox` 기준 상대 경로(`media/system-….vdi` 등)로 저장한다.
`last_location`의 절대 경로는 VirtualBox의 이전 등록을 확인하는 기록일 뿐,
현재 디스크를 여는 기준으로 쓰지 않는다. 외부 원본 디스크의 출처 기록은 유지한다.
`VBOX_BASE_DISK`에 상대 경로를 주면 현재 판 디렉터리를 기준으로 찾는다.

예전 버전 1의 절대 경로도 자동 변환한다. VirtualBox 등록에는 절대 경로가 필요하므로
이전 경로가 사라진 경우 로컬 `.vbox`의 UUID·소유 표식·판 이름과 기존 등록을 대조한다.
설정과 상태 기록을 `.vbox/relocation-backup-…/`에 백업하고, 삭제 옵션 없이 등록을
해제한 다음 현재 위치의 설정을 등록한다. ISO·VDI·`.sav` 내용은 변경하지 않는다.
등록 단계가 실패하면 백업과 실행 자료를 남기며, 다음 실행에서 등록을 다시 시도한다.
[VirtualBox 등록 명령 설명](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/vboxmanage-registervm.html)

이동할 때는 VM을 종료하거나 저장한 뒤 **숨김 폴더 `.vbox`까지 함께 이동**한다.
원래 폴더가 남아 있는 복사본은 기존 VM을 빼앗지 않도록 거부하며, 실행 중인 VM의
등록 변경이나 누락된 저장 상태의 삭제도 하지 않는다. `make vbox-status`는 복구가
필요한지 읽기만 한다. VM을 시작하지 않고 경로만 복구하려면 다음 명령을 쓴다.

```sh
python3 vbox.py relocate
make vbox-status
```

2026-10-03 검증: 실행기 시험 33개와 독립 실행기 295개의 설치 검사가 통과했다.
실제 KOR VM을 새 경로에 다시 등록하고 `saved` 상태를 확인했다. 디스크·ISO·저장 상태
파일 3개의 SHA-256은 복구 전후 동일하다. 최초 경로 복구 검증에서는 VM 재개나 새 부팅을 수행하지 않았다.
[검증 기록](../build-verification/vbox-relocation/summary.json)

이동 후 일반 부팅에서 `Cannot register the hard disk ... UUID ... already exists`가
발생하는 경우도 수정했다. VirtualBox 5.2가 `machines/VM/../../media/…`와 정규화된
절대 경로를 서로 다른 미디어 등록 경로로 처리하기 때문이다. 현재 실행기는 경로를
정규화하여 같은 파일인지 확인하고, 연결된 미디어의 UUID를 재사용한다. 연결이 해제된
기존 미디어도 `list hdds`·`list dvds`에서 찾아 UUID로 연결한다. 새 파일만 경로로 등록한다.
VDI의 UUID를 바꾸거나 기존 디스크 등록을 삭제할 필요가 없다.
[storageattach의 UUID 지정](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/vboxmanage-storageattach.html)

추가 검증: 실행기 시험 37개와 295개 설치 검사를 통과했다. 실제
`make -C /home/user/golang/worldos/나라/KOR vbox`가 종료 코드 0으로 완료되었고,
GUI 실행 및 `WORLDOS-SHELL:READY`를 확인했다. 기존 디스크 UUID와 SHA-256도 유지되었다.
[UUID 재사용·실제 부팅 검증 기록](../build-verification/vbox-medium-uuid/summary.json)

## 처음 사용할 때의 부팅 디스크

현재 설치 설정은 다음 디스크를 최초 복제 원본으로 사용한다.

```text
/home/user/VirtualBox VMs/eng operating system/NewVirtualDisk1-fixed-20260908.vdi
```

이 경로의 `eng operating system`은 기존 디스크가 보관된 폴더 이름일 뿐, 해당 가상 머신을 시작하거나 수정한다는 뜻이 아니다. 복제 전후 SHA-256이 같은지 검사하며 원본에 프로그램을 쓰지 않는다. 원본은 다른 VM에서 사용 중이지 않은 정상적인 부팅 디스크여야 한다.

다른 컴퓨터에서 처음 준비할 때는 경로를 지정한다.

```sh
make vbox VBOX_BASE_DISK="/절대/경로/기존-부팅-디스크.vdi"
```

현재 커널에 맞는 FAT 파티션과 `LINKER`, `LIB1.SO`, `LIB2.SO`가 필요하므로 빈 VDI로 대체할 수 없다. 이미 전용 디스크가 만들어진 뒤에는 이 옵션으로 초기화하지 않고 현재 디스크를 계속 사용한다.

같은 VM 이름이 이미 다른 용도로 등록되어 있으면 그 VM은 수정하지 않는다. 최초 실행 시 다른 이름을 선택한다.

```sh
make vbox VBOX_VM_NAME="worldos KOR local"
```

화면 없는 실행은 `make vbox VBOX_TYPE=headless`로 선택한다. 기본값은 `gui`이며, 이미 실행 중인 VM의 표시 방식을 이 옵션으로 바꾸지는 않는다.

## 호스트 준비 사항과 문제 확인

호스트에는 VirtualBox와 `VBoxManage`, 작동하는 VirtualBox 호스트 드라이버, 기존 커널 빌드 도구(Go, GCC, GNU make, NASM, GRUB, xorriso 등), Python 3, `qemu-img`, `sfdisk`, `mcopy`, `mdir`가 필요하다. 현재 개발 환경에서 이 도구들로 실제 실행을 확인했다. 필요한 패키지는 관리자가 설치하며 실행기는 `sudo`, 드라이버 재설치, 장치 권한 변경을 자동 수행하지 않는다.

Linux에서 `/dev/vboxdrv`가 없다는 오류가 나면 실제 호스트 터미널에서 확인한다. 샌드박스에서는 정상 호스트의 장치가 가려질 수 있다. 장치 권한만 보고 임의로 `chmod`하지 않는다. VirtualBox의 호스트 드라이버와 실행 환경을 먼저 점검한다.

명령은 `나라/KOR` 같은 **판의 상위 폴더**에서 실행한다. 원문 폴더(한국어판 `원문`, 중국어판 `源代码` 등)의 Makefile에 남아 있는 기존 `vbox` 대상은 이번 독립 실행기와 다르므로 사용하지 않는다. 독립 실행기는 `vbox-entry.json`의 `kernel_directory`에서 실제 원문 경로를 읽는다. [관리 경로 변경](관리경로-현지화.md)은 VM 이름·저장 상태·가상 디스크를 변경하지 않는다.

## 설치·검증

```sh
cd ~/worldos
make verify-vbox
make test-vbox
```

실행기 원본은 `tools/worldos_vbox.py`이며 각 판에는 자체 `vbox.py`, `vbox-entry.json`, Makefile 대상이 설치된다. 실행 시 공용 Python 모듈을 가져오지 않는다. 원본을 수정한 관리자는 `python3 tools/install_vbox.py --refresh`로 갱신할 수 있다. 판 안에서 수정된 실행기는 해시 검사로 보호하므로 사용자 수정을 먼저 검토·보존해야 한다. 설치 전 파일은 `/tmp/worldos-vbox-install-backup-*`에 백업한다.

카탈로그·국가 소스 생성기는 `vbox-entry.json`이 설치된 판의 상위 Makefile을 보존하여 셸·POSIX·VirtualBox 대상을 없애지 않는다. 커널 소스 재생성의 기존 동작 자체를 바꾸는 것은 아니다.

검증 범위: 295개 실행기의 독립 연결과 Makefile 진입점을 점검하고, 빌드 실패·VM 이름 충돌·저장 상태·외부 미디어·중복 실행·디스크 보존·빌드 도중 VM 시작을 단위 시험한다. 실제 VirtualBox 창 부팅은 KOR에서 `WORLDOS-SHELL:READY`까지 확인했다. 295개 VM을 모두 실제로 생성·부팅했다는 뜻은 아니다.

2026-09-10 최초 도입 검증에서는 295개 진입점과 전체 회귀 시험 93개(실행기 시험 14개 포함)가 통과했다. [최초 검증 기록](../build-verification/vbox/summary.json)과 [KOR 화면](../build-verification/vbox/KOR.png)을 남겼다. 이후 저장·일시 정지 상태 재개를 추가하고 시험을 확장했다. [재개 수정 검증 기록](../build-verification/vbox-resume/summary.json)은 최초 정상 재개와 이후 VirtualBox 내부 복원 오류를 구분해 기록한다.

VirtualBox 명령과 설정 형식은 [공식 5.2 사용자 설명서](https://download.virtualbox.org/virtualbox/5.2.44/UserManual.pdf)의 `createvm`, `modifyvm`, `storagectl`, `storageattach`, `startvm` 항목을 참고했다.
