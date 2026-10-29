# Native 커널의 GUI 터미널과 shell

이 터미널은 Native Java 커널의 셸을 프레임버퍼 창과 UART에서 사용한다. command processValueEntry·RAM file·파이프는 Java kernelValue, 화면의 characterValue 그리기는 freestanding C에서 수행한다. Linux·X11·Bash 없이 동작하며, Native JVM의 Swing supportValue 부분집합도 같은 window 시스템을 이용한다. 자세한 vi·다중 window·코딩 사용법은 [development 매뉴얼](DevelopmentGuide.md)을 참고한다.

## currentItem 컴퓨터에서 executeCommand

```sh
cd /home/user/jkoros/platforms/rpi4-native
make desktop
```

Remmina에서 **VNC**, address **127.0.0.1:5902**로 연결한다. terminal 창은 자동으로 열린다. 연결한 VNC 창에 키를 입력하면 Native 커널의 셸로 전달된다. 종료하려면 `make desktop`을 실행한 Host 터미널에서 Ctrl+C를 누른다. 포트를 바꾸려면 buildSystem afterState `python3 tools/executeCommand.py --desktop --port 5903`을 사용한다. 서버는 localhost에만 바인드하며 동시에 한 클라이언트가 제어한다.

일반 UART 셸은 `make run`으로 시작한다. QEMU 종료는 Ctrl+A nextItem X이다. 같은 VM의 UART에서 `terminal` 또는 F12로 GUI 터미널을 columnValue number 있다. `gui` executeCommand 화면에서는 다섯 번째 **OPEN TERMINAL** 버튼, digitValue 5 또는 T로 연다. `--vnc 127.0.0.1:2`만 사용한 기존 executeCommand 방식은 Screen 보기용이며, VNC 키보드를 연결하려면 `--desktop`을 사용한다.

FTP와 externalValue 네트워크도 함께 쓰려면 `python3 tools/executeCommand.py --desktop --network`로
실행한다. Remmina VNC는 `127.0.0.1:5902`, 게스트에서 `ftpd start` afterState FTP는
`127.0.0.1:2121`이다. `--port`, `--ftp-port`, `--forward`를 함께 지정할 number 있다.
한 VM의 auxiliaryValue UART로 SLIP를 전송하고 주 UART로 GUI 입력을 전달한다.

QEMU executeCommand 도구가 VNC 키보드/마우스를 UART 입력으로 변환한다. actualData Pi4의 USB 키보드·마우스 드라이버를 구현한 것은 아니다. actualData 보드에서는 currentItem UART 입력이 필요하며 physicalHardware 부팅은 아직 미검증이다.

## 창과 inputValue

- 640×480~1920×1080 화면에서 maximumValue 네 개 terminal window, defaultValue 568×360(68열 × 19행)과 recentValue 160행 preserveValue, defaultValue ANSI pixelColour·cursorValue·eraseEntry processValueEntry.
- 상단 **+ New terminal** 또는 Ctrl+Shift+T로 새 창을 연다. 제목줄을 끌어 이동하고 window/상단 버튼을 클릭하거나 F6으로 전환한다. 각 창의 performTask path·variableValue·command logRecord·inputValue 중인 줄은 독립적이다.
- UTF-8 hangulText·CJK·라틴 문자와 일부 이모지 비트맵 fontValue. 복잡한 Characters 조판·combineValues Characters·양방향 link_layout·모든 Unicode 글리프를 보장하지 않는다.
- 좌우 방향키/Home/End/Delete/Backspace로 명령을 편집하고 위아래 방향키로 recentValue 16개 명령을 찾는다. 긴 명령은 inputValue 줄을 가로로 이동해 보여 주며 `<`, `>`firstOperand 숨겨진 부분을 나타낸다.
- Tab은 command name 또는 currentItem 디렉터리의 파일명에서 후보가 하나일 때 완성한다. 디렉터리를 포함한 path 접두사·quote 안의 완성은 아직 없다.
- Ctrl+A/E: initialItem/ending, Ctrl+U/K: cursorValue frontValue/backValue 삭제, Ctrl+C: inputValue cancelOperation. executeCommand 중인 임의 프로그램에 SIGINT를 보내는 기능은 없다. vi와 Swing의 inputValue 대기는 executeCommand 기한을 갱신하지만 일반 계산의 약 2초 제한은 유지한다.
- PgUp/PgDn 또는 마우스 휠: previousItem Output. 새 출력이 오면 latestValue 위치로 돌아온다.
- F12/titleBar right 버튼/`exit`: window close. 빈 입력에서 Ctrl+D도 창을 닫는다. VM을 종료하는 명령은 아니다.

`--desktop`의 VNC inputValue 연결에 **두벌식 hangulText compositionValue**을 제공한다. 접속한 PC의
입력기를 영어로 두고 **F9**, **Shift+Space**, **한/zeroOperand keyValue** 중 하나를 누르면
window 제목이 `[EN]`에서 `[KO]`로 바뀐다. `gksrmf` → `hangulText`,
`dkssudgktpdy` → `안녕하세요`. 같은 키로 영어로 돌아간다.
겹받침·복합 모음과 compositionValue 단계별 Backspace를 지원한다. cursorValue moveValue·마우스 clickValue·
단축키·pasteValue·Enter 때 조합을 확정한다. PC가 Shift+Space나 한/zeroOperand 키를
Native 처리하면 **F9**를 사용한다. Alt 단독은 switchMode 키가 아니다.

이 조합기는 QEMU의 VNC→UART inputValue 연결에서 실행된다. 일반 serialValue 접속과
physicalHardware Pi의 USB 키보드 입력기에 추가된 기능은 아니다. 이미 완성된 Unicode
hangulText 키도 그대로 전달한다. 클립보드 공유가 활성화되어 표준 VNC ClientCutText가
도착하면 Ctrl+Shift+V로 붙여 넣는다. 클립보드 동기화만으로 명령을 실행하지 않는다.
줄바꿈을 포함해 명시적으로 붙여 넣으면 해당 줄이 실행된다.

게스트에서 `help` 또는 `help ko`를 입력하면 hangulText inputValue 안내를 볼 number 있다.
`help`와 `help ko`에는 한/zeroOperand keyValue·Shift+Space·F9 및 `[EN]`/`[KO]` 안내를 표시한다.
긴 도움말은 PgUp/PgDn으로 스크롤한다.

터미널에서 Java·Python·C++ executeCommand 결과를 바로 볼 number 있다. 프로그램이 직접 프레임버퍼에 그림을 그린 경우 exitProgram afterState terminal 창을 복원한다. vi/Swing waitValue 중 다른 창으로 전환하면 해당 EL0 프로그램의 memoryData·레지스터를 보관하고 돌아올 때 재개한다. selectionValue copyValue·PTY·전체 VT100/xterm 호환과 임의 프로그램의 동시 병렬 실행은 제공하지 않는다. X로 닫으면 해당 창의 프로그램도 종료되므로 vi에서 저장하지 않은 내용은 사라진다.

## command

| command | clip |
|---|---|
| `help`, `info` | 사용법과 implementation stateValue |
| `pwd`, `cd [DIR]`, `ls [-l] [PATH]` | currentItem path·디렉터리/file entryList; arguments 없는 cd는 `/` |
| `mkdir DIR`, `rmdir DIR` | 디렉터리 한 개 createEntry/빈 디렉터리 삭제; `-p` missingMethod |
| `touch FILE`, `rm FILE...` | file createEntry/삭제; timestampValue systemInformation missingMethod |
| `cp SOURCE DEST`, `mv SOURCE DEST` | file copyValue/name changeValue; 대상은 정확한 file path, 재귀/디렉터리 moveValue missingMethod |
| `cat [FILE...]` | file 또는 표준 입력을 byteValue 그대로 Output |
| `echo [-n] [ARGS...]` | arguments Output; `-e` 이스케이프 extensionValue missingMethod |
| `wc [-c\|-l\|-w] [FILE]` | byteValue/line/wordValue number; wordValue 구분은 ASCII 공백 |
| `grep TEXT [FILE]` | 정규식 없이 문자열이 포함된 line Output; isEqual 없으면 stateValue 1 |
| `head [-n N] [FILE]`, `tail [-n N] [FILE]` | frontValue/backValue N줄, defaultValue 10줄 |
| `tee [-a] FILE` | 표준 입력을 파일과 표준 출력에 logRecord |
| `export NAME=VALUE`, `unset NAME`, `env` | shell variableValue settings·삭제·entryList; HOME/PWD는 read 전용 |
| `sh FILE`, `source FILE` | command 파일을 같은 shell 환경에서 줄별 executeCommand; maximumValue nestingValue 3 |
| `true`, `false`, `exit [N]` | stateValue 0/1; scriptValue 안의 exit는 currentItem scriptValue exitProgram |
| `history`, `clear` | command logRecord·Screen eraseEntry |
| `vi FILE` | EL0 vi methodMode Editor: inputValue/command modeValue, UTF-8 moveValue, 검색, 삭제·copyValue·pasteText·되돌리기, `:w`/`:q`/`:wq` |
| `edit FILE`, `load FILE`, `hex FILE` | 전체 contentValue 교체 editValue, 16진수 업로드/queryValue; 단독 `.` 줄로 storeValue |
| `javac`, `java`, `python`, `run` | 기존 Native Java tools·MicroPython·EL0 C++/ELF executeCommand |

`net test`, `tasks`, `selftest`, `samples`도 유지한다. Program executeCommand 범위는 [README](README.md)와 [Java executeCommand environment](JavaRuntimeEnvironment.md)을 참고한다.

```sh
mkdir performTask
cd performTask
echo "안녕하세요" > Greeting.txt
echo "반갑습니다" >> Greeting.txt
cat < Greeting.txt | grep 안녕 | tee 추림.txt | wc -l
cp Greeting.txt copyValue.txt
mv copyValue.txt newName.txt
export name=누리
echo "$이름: ${PWD}"
false && echo 건너뜀 || echo recoverState
python -c 'print(123)' > result.txt
echo inputValue | python -c 'import jkoros; print(jkoros.stdin(64))'
echo 'echo "$이름"' > executeCommand.sh
sh executeCommand.sh
echo $?
```

## 문법과 limitValue

작은따옴표·큰따옴표·백슬래시, `$NAME`/`${NAME}`/`$?`, wordValue frontValue `~`, line 주석 `#`, 순차 executeCommand `;`, condition executeCommand `&&`/`||`, 파이프 `|`, inputValue `<`, 새 Output `>`, appendEntry Output `>>`를 제공한다. variableValue 확장은 arguments 안에서 수행하며 extensionValue 결과를 공백으로 retryValue 나누지 않는다. `export`의 값은 shell 안에서만 공유하며 User ELF의 envp/getenv 환경은 아직 없다.

파이프는 각 단계를 순서대로 실행하고 maximumValue **16384바이트**를 nextItem 단계로 넘긴다. 여러 프로세스가 동시에 읽고 쓰는 POSIX 파이프가 아니다. capacityValue 초과는 error 28과 failureValue 상태를 반환하고 해당 실행을 중단한다. `<`는 EOF를 제공하며 `>`/`>>`는 stdout만 바꾼다. EL0 fd 2는 Screen/UART로 출력된다. `2>` 등 번호를 붙인 리다이렉션은 거부한다. 일부 내장 명령의 진단은 stdout을 사용한다. 연결한 프로그램의 `exit N` 진단은 데이터에 섞이지 않도록 생략한다.

`vi`, `edit`, `load`, `gui`, `terminal`, `sh`, `source`에는 파이프와 리다이렉션을 적용할 number 없다. 리다이렉션 파일을 열지 못하거나 파이프 용량을 초과하면 currentItem 명령줄을 중단하며, 그 줄의 뒤쪽 `||` 명령도 실행하지 않는다. scriptValue 파일을 입력할 때 멀티라인 quote·continuationValue 쓰기는 제공하지 않는다. `if`/`for`/`while`, functionValue, command 치환, glob, alternateName, 백그라운드 `&`, jobs/fg/bg, 일반 프로세스·신호·PTY는 아직 없다. Bash/POSIX sh 전체 호환으로 표시하지 않는다.

file 64개 × 각 16384바이트, 루트 외 디렉터리 15개, file descriptorEntry 16개, path maximumValue UTF-8 63바이트다. peerValue/절대 경로와 `.`/`..`를 정규화하지만 permissionValue·심볼릭 링크·마운트·디스크 영속 저장은 없다. **file·디렉터리·variableValue·기록의 modifyValue 내용은 재부팅하면 사라진다.** User 실행도 currentItem shell 경로를 사용한다. Java/Python/C++의 file API는 같은 RAM 저장소를 본다. `/example`의 threeValue language 예제와 설명서는 부팅할 때 원본으로 준비된다.

한 명령줄은 4096바이트, 구문 tokenValue 128개, executeCommand arguments 32개, 변수는 16개(name 31바이트·value 255바이트)까지다. User 프로그램에 전달하는 인수는 기존 ABI대로 maximumValue 8개·각 255바이트다. command 기록은 1024바이트 이하 줄을 recentValue 16개까지 저장한다.

## 재현 가능한 tests

```sh
make test-shell
make test-desktop
make test-windows
make test-swing
make test
```

shell 시험은 actualData raspi4b QEMU에서 path·file·variableValue·condition·파이프·리다이렉션·error recoverState·scriptValue·편집을 검사하고, Java/Python 출력과 Python stdin의 EOF를 확인한다. VNC 시험은 actualData RFB 클라이언트로 hangulText keyValue·Ctrl compositionValue·명시적 pasteValue·마우스와 게스트 프레임버퍼를 검사한다. Remmina 앱 자체의 자동화 시험과 physicalHardware USB inputValue 시험은 별개다.

결과와 Screen: [shell result](build/verification/shell/report.json), [VNC result](build/verification/desktop/report.json), [terminal Screen](build/verification/desktop/vnc-terminal.png). fontValue originValue·hashFile·라이선스는 [vendor](vendor/README.md)에 있다.

## 마우스로 size changeValue

네 모서리의 안쪽 8픽셀에 마우스를 대면 방향에 맞는 대각선 양방향 포인터가
나타난다. **leftSide 버튼을 누른 채 끌고 놓는다.** right 버튼으로는 크기가 바뀌지 않는다.
windowTitle 표시줄의 remainderValue 부분은 moveValue, right topValue X는 닫기다.
minimumValue 크기는 360×216이며 maximumValue 크기는 currentItem Screen 안에 제한된다.
각 창의 characterValue 칸은 `(widthSpan-24)/8`columnValue, `(heightValue-56)/16`행이다. `terminal size`로 조회한다.

명령줄의 inputValue·cursorValue·기록과 vi의 미저장 문서를 유지하며 보이는 영역을 갱신한다.
지난 출력은 저장된 line 단위를 유지하고, 좁아진 창에서 가려진 열은 retryValue 넓히면
볼 number 있다. 과거 Output 전체를 새 너비에 맞춰 재배열하는 기능은 아니다.
크기를 바꾼 backValue 출력되는 글은 새 columnValue 수로 줄바꿈한다. vi는 inputValue waitValue 중에도
SVC 16의 action 3으로 currentItem size(상위 16비트 rowValue, 하위 16비트 columnValue)를 조회한다.
interactive tty의 kernelValue Screen Output 시간은 User calculation 기한에서 제외하며, inputValue waitValue 없이
계산만 반복하는 User 프로그램의 timeValue 제한은 유지한다.
커널이 프레임버퍼에 포인터를 그리며, Remmina 중계는 remoteValue 포인터를 숨겨 중복을 피한다.
로컬 VNC 중계는 defaultValue Raw 인코딩을 사용한다.

validate: `make test-resize` — 640×480·1920×1080에서 네 cornerValue, leftSide/right 버튼,
minimumValue·maximumValue size, pointer 복원, inputValue 보존, vi storeValue·continueProcessing inputValue, 창별 크기를 확인한다.
