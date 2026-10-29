# Eigen 커널의 GUI 터미널과 Shell

이 터미널은 Eigen Java 커널의 셸을 프레임버퍼 창과 UART에서 사용한다. opdracht Proces_WAARDE_invoer·RAM bestand·파이프는 Java kernel_WAARDE, 화면의 teken_WAARDE 그리기는 freestanding C에서 수행한다. Linux·X11·Bash 없이 동작하며, Eigen JVM의 Swing steun_WAARDE 부분집합도 같은 Venster 시스템을 이용한다. 자세한 vi·다중 Venster·코딩 사용법은 [ontwikkeling 매뉴얼](ontwikkeling_guide.md)을 참고한다.

## actueel_item 컴퓨터에서 Uitvoeren_opdracht

```sh
cd /home/user/jkoros/platforms/rpi4-native
make desktop
```

Remmina에서 **VNC**, ADRES **127.0.0.1:5902**로 연결한다. terminal 창은 자동으로 열린다. 연결한 VNC 창에 키를 입력하면 Eigen 커널의 셸로 전달된다. 종료하려면 `make desktop`을 실행한 host 터미널에서 Ctrl+C를 누른다. 포트를 바꾸려면 bouwen 후 `python3 hulpmiddelen/Uitvoeren_opdracht.py --desktop --port 5903`을 사용한다. 서버는 localhost에만 바인드하며 동시에 한 클라이언트가 제어한다.

일반 UART 셸은 `make run`으로 시작한다. QEMU 종료는 Ctrl+A Volgende_item X이다. 같은 VM의 UART에서 `terminal` 또는 F12로 GUI 터미널을 KOLOM_WAARDE nummer 있다. `gui` Uitvoeren_opdracht 화면에서는 다섯 번째 **OPEN TERMINAL** 버튼, cijfer_WAARDE 5 또는 T로 연다. `--vnc 127.0.0.1:2`만 사용한 기존 Uitvoeren_opdracht 방식은 scherm 보기용이며, VNC 키보드를 연결하려면 `--desktop`을 사용한다.

FTP와 extern_WAARDE 네트워크도 함께 쓰려면 `python3 hulpmiddelen/Uitvoeren_opdracht.py --desktop --network`로
실행한다. Remmina VNC는 `127.0.0.1:5902`, 게스트에서 `ftpd start` 후 FTP는
`127.0.0.1:2121`이다. `--port`, `--ftp-port`, `--forward`를 함께 지정할 nummer 있다.
한 VM의 보조 UART로 SLIP를 전송하고 주 UART로 GUI 입력을 전달한다.

QEMU Uitvoeren_opdracht 도구가 VNC 키보드/마우스를 UART 입력으로 변환한다. werkelijk_gegevens Pi4의 USB 키보드·마우스 드라이버를 구현한 것은 아니다. werkelijk_gegevens 보드에서는 actueel_item UART 입력이 필요하며 실물 부팅은 아직 미검증이다.

## 창과 invoer_WAARDE

- 640×480~1920×1080 화면에서 최대 네 개 terminal Venster, standaardwaarde 568×360(68열 × 19행)과 recent_WAARDE 160행 보관, standaardwaarde ANSI 색상·cursor_WAARDE·wissen_invoer Proces_WAARDE_invoer.
- 상단 **+ New terminal** 또는 Ctrl+Shift+T로 새 창을 연다. 제목줄을 끌어 이동하고 Venster/상단 버튼을 클릭하거나 F6으로 전환한다. 각 창의 작업 pad·variabele_WAARDE·opdracht LOG_RECORD·invoer_WAARDE 중인 줄은 독립적이다.
- UTF-8 한글·CJK·라틴 문자와 일부 이모지 비트맵 lettertype_WAARDE. 복잡한 문자 조판·결합 문자·양방향 koppelindeling·모든 Unicode 글리프를 보장하지 않는다.
- 좌우 방향키/Home/End/Delete/Backspace로 명령을 편집하고 위아래 방향키로 recent_WAARDE 16개 명령을 찾는다. 긴 명령은 invoer_WAARDE 줄을 가로로 이동해 보여 주며 `<`, `>`가 숨겨진 부분을 나타낸다.
- Tab은 opdracht Naam 또는 actueel_item 디렉터리의 파일명에서 후보가 하나일 때 완성한다. 디렉터리를 포함한 pad 접두사·Citaat 안의 완성은 아직 없다.
- Ctrl+A/E: 처음/끝, Ctrl+U/K: cursor_WAARDE voorkant_WAARDE/BACK_WAARDE 삭제, Ctrl+C: invoer_WAARDE Annuleren_operatie. Uitvoeren_opdracht 중인 임의 프로그램에 SIGINT를 보내는 기능은 없다. vi와 Swing의 invoer_WAARDE 대기는 Uitvoeren_opdracht 기한을 갱신하지만 일반 계산의 약 2초 제한은 유지한다.
- PgUp/PgDn 또는 마우스 휠: Vorige_item tekstuitvoer. 새 출력이 오면 최신 위치로 돌아온다.
- F12/titelbalk recht 버튼/`exit`: Venster Sluiten. 빈 입력에서 Ctrl+D도 창을 닫는다. VM을 종료하는 명령은 아니다.

`--desktop`의 VNC invoer_WAARDE 연결에 **두벌식 한글 samenstelling_WAARDE**을 제공한다. 접속한 PC의
입력기를 영어로 두고 **F9**, **Shift+Space**, **한/nul_operand toets_WAARDE** 중 하나를 누르면
Venster 제목이 `[EN]`에서 `[KO]`로 바뀐다. `gksrmf` → `한글`,
`dkssudgktpdy` → `안녕하세요`. 같은 키로 영어로 돌아간다.
겹받침·복합 모음과 samenstelling_WAARDE 단계별 Backspace를 지원한다. cursor_WAARDE verplaatsen_WAARDE_83b651b8·마우스 click_WAARDE·
단축키·plakken_WAARDE·Enter 때 조합을 확정한다. PC가 Shift+Space나 한/nul_operand 키를
Eigen 처리하면 **F9**를 사용한다. Alt 단독은 switch_MODUS 키가 아니다.

이 조합기는 QEMU의 VNC→UART invoer_WAARDE 연결에서 실행된다. 일반 직렬 접속과
실물 Pi의 USB 키보드 입력기에 추가된 기능은 아니다. 이미 완성된 Unicode
한글 키도 그대로 전달한다. 클립보드 공유가 활성화되어 표준 VNC ClientCutText가
도착하면 Ctrl+Shift+V로 붙여 넣는다. 클립보드 동기화만으로 명령을 실행하지 않는다.
줄바꿈을 포함해 명시적으로 붙여 넣으면 해당 줄이 실행된다.

게스트에서 `help` 또는 `help ko`를 입력하면 한글 invoer_WAARDE 안내를 볼 nummer 있다.
`help`와 `help ko`에는 한/nul_operand toets_WAARDE·Shift+Space·F9 및 `[EN]`/`[KO]` 안내를 표시한다.
긴 도움말은 PgUp/PgDn으로 스크롤한다.

터미널에서 Java·Python·C++ Uitvoeren_opdracht 결과를 바로 볼 nummer 있다. 프로그램이 직접 프레임버퍼에 그림을 그린 경우 Einde_app 후 terminal 창을 복원한다. vi/Swing wachten_WAARDE 중 다른 창으로 전환하면 해당 EL0 프로그램의 Geheugen_gegevens·레지스터를 보관하고 돌아올 때 재개한다. selectie_WAARDE kopiëren_WAARDE·PTY·전체 VT100/xterm 호환과 임의 프로그램의 동시 병렬 실행은 제공하지 않는다. X로 닫으면 해당 창의 프로그램도 종료되므로 vi에서 저장하지 않은 내용은 사라진다.

## opdracht

| opdracht | clip |
|---|---|
| `help`, `info` | 사용법과 implementatie Status_WAARDE |
| `pwd`, `cd [DIR]`, `ls [-l] [PATH]` | actueel_item pad·디렉터리/bestand invoer_Lijst_f07b3200; argumenten 없는 cd는 `/` |
| `mkdir DIR`, `rmdir DIR` | 디렉터리 한 개 maken_invoer/빈 디렉터리 삭제; `-p` 없음 |
| `touch FILE`, `rm FILE...` | bestand maken_invoer/삭제; timestamp_WAARDE msinfo32_exe 없음 |
| `cp SOURCE DEST`, `mv SOURCE DEST` | bestand kopiëren_WAARDE/Naam wijzigen_WAARDE; 대상은 정확한 bestand pad, 재귀/디렉터리 verplaatsen_WAARDE_83b651b8 없음 |
| `cat [FILE...]` | bestand 또는 표준 입력을 byte_WAARDE 그대로 tekstuitvoer |
| `echo [-n] [ARGS...]` | argumenten tekstuitvoer; `-e` 이스케이프 extensie_WAARDE 없음 |
| `wc [-c\|-l\|-w] [FILE]` | byte_WAARDE/invoerregel/Word_WAARDE nummer; Word_WAARDE 구분은 ASCII 공백 |
| `grep TEXT [FILE]` | 정규식 없이 문자열이 포함된 invoerregel tekstuitvoer; 일치 없으면 Status_WAARDE 1 |
| `head [-n N] [FILE]`, `tail [-n N] [FILE]` | voorkant_WAARDE/BACK_WAARDE N줄, standaardwaarde 10줄 |
| `tee [-a] FILE` | 표준 입력을 파일과 표준 출력에 LOG_RECORD |
| `export NAME=VALUE`, `unset NAME`, `env` | Shell variabele_WAARDE Instellingen·삭제·invoer_Lijst_f07b3200; HOME/PWD는 Lezen 전용 |
| `sh FILE`, `source FILE` | opdracht 파일을 같은 Shell 환경에서 줄별 Uitvoeren_opdracht; 최대 nesting_WAARDE 3 |
| `true`, `false`, `exit [N]` | Status_WAARDE 0/1; script_WAARDE 안의 exit는 actueel_item script_WAARDE Einde_app |
| `history`, `clear` | opdracht LOG_RECORD·scherm wissen_invoer |
| `vi FILE` | EL0 vi methode_MODUS Editor: invoer_WAARDE/opdracht MODUS_WAARDE, UTF-8 verplaatsen_WAARDE_83b651b8, 검색, 삭제·kopiëren_WAARDE·plakken_sms·되돌리기, `:w`/`:q`/`:wq` |
| `edit FILE`, `load FILE`, `hex FILE` | 전체 Inhoud_WAARDE 교체 Bewerk_WAARDE, 16진수 업로드/query_WAARDE; 단독 `.` 줄로 Store_WAARDE |
| `javac`, `java`, `python`, `run` | 기존 Eigen Java hulpmiddelen·MicroPython·EL0 C++/ELF Uitvoeren_opdracht |

`net test`, `tasks`, `selftest`, `samples`도 유지한다. app_f5044b9b Uitvoeren_opdracht 범위는 [README](LEESMIJ_eb81d7d9.md)와 [Java Uitvoeren_opdracht omgeving](자바실행환경.md)을 참고한다.

```sh
mkdir 작업
cd 작업
echo "안녕하세요" > 인사.txt
echo "반갑습니다" >> 인사.txt
cat < 인사.txt | grep 안녕 | tee 추림.txt | wc -l
cp 인사.txt kopiëren_WAARDE.txt
mv kopiëren_WAARDE.txt 새이름.txt
export Naam=누리
echo "$이름: ${PWD}"
false && echo 건너뜀 || echo herstellen_Status
python -c 'print(123)' > resultaat.txt
echo invoer_WAARDE | python -c 'import jkoros; print(jkoros.stdin(64))'
echo 'echo "$이름"' > Uitvoeren_opdracht.sh
sh Uitvoeren_opdracht.sh
echo $?
```

## 문법과 제한

작은따옴표·큰따옴표·백슬래시, `$NAME`/`${NAME}`/`$?`, Word_WAARDE voorkant_WAARDE `~`, invoerregel 주석 `#`, 순차 Uitvoeren_opdracht `;`, toestand Uitvoeren_opdracht `&&`/`||`, 파이프 `|`, invoer_WAARDE `<`, 새 tekstuitvoer `>`, toevoegen_invoer tekstuitvoer `>>`를 제공한다. variabele_WAARDE 확장은 argumenten 안에서 수행하며 extensie_WAARDE 결과를 공백으로 opnieuw_proberen_WAARDE 나누지 않는다. `export`의 값은 Shell 안에서만 공유하며 gebruikersruimte ELF의 envp/getenv 환경은 아직 없다.

파이프는 각 단계를 순서대로 실행하고 최대 **16384바이트**를 Volgende_item 단계로 넘긴다. 여러 프로세스가 동시에 읽고 쓰는 POSIX 파이프가 아니다. capaciteit_WAARDE 초과는 fout 28과 fout_WAARDE 상태를 반환하고 해당 실행을 중단한다. `<`는 EOF를 제공하며 `>`/`>>`는 stdout만 바꾼다. EL0 fd 2는 scherm/UART로 출력된다. `2>` 등 번호를 붙인 리다이렉션은 거부한다. 일부 내장 명령의 진단은 stdout을 사용한다. 연결한 프로그램의 `exit N` 진단은 데이터에 섞이지 않도록 생략한다.

`vi`, `edit`, `load`, `gui`, `terminal`, `sh`, `source`에는 파이프와 리다이렉션을 적용할 nummer 없다. 리다이렉션 파일을 열지 못하거나 파이프 용량을 초과하면 actueel_item 명령줄을 중단하며, 그 줄의 뒤쪽 `||` 명령도 실행하지 않는다. script_WAARDE 파일을 입력할 때 멀티라인 Citaat·이어 쓰기는 제공하지 않는다. `if`/`for`/`while`, FUNCTIE_WAARDE, opdracht 치환, glob, 별칭, 백그라운드 `&`, jobs/fg/bg, 일반 프로세스·신호·PTY는 아직 없다. Bash/POSIX sh 전체 호환으로 표시하지 않는다.

bestand 64개 × 각 16384바이트, 루트 외 디렉터리 15개, bestand 서술자 16개, pad 최대 UTF-8 63바이트다. peer_WAARDE/절대 경로와 `.`/`..`를 정규화하지만 machtiging_WAARDE·심볼릭 링크·마운트·디스크 영속 저장은 없다. **bestand·디렉터리·variabele_WAARDE·기록의 수정 내용은 재부팅하면 사라진다.** gebruikersruimte 실행도 actueel_item Shell 경로를 사용한다. Java/Python/C++의 bestand API는 같은 RAM 저장소를 본다. `/example`의 세 Taal 예제와 설명서는 부팅할 때 원본으로 준비된다.

한 명령줄은 4096바이트, 구문 token_WAARDE 128개, Uitvoeren_opdracht argumenten 32개, 변수는 16개(Naam 31바이트·WAARDE 255바이트)까지다. gebruikersruimte 프로그램에 전달하는 인수는 기존 ABI대로 최대 8개·각 255바이트다. opdracht 기록은 1024바이트 이하 줄을 recent_WAARDE 16개까지 저장한다.

## 재현 가능한 tests

```sh
make test-shell
make test-desktop
make test-windows
make test-swing
make test
```

Shell 시험은 werkelijk_gegevens raspi4b QEMU에서 pad·bestand·variabele_WAARDE·toestand·파이프·리다이렉션·fout herstellen_Status·script_WAARDE·편집을 검사하고, Java/Python 출력과 Python stdin의 EOF를 확인한다. VNC 시험은 werkelijk_gegevens RFB 클라이언트로 한글 toets_WAARDE·Ctrl samenstelling_WAARDE·명시적 plakken_WAARDE·마우스와 게스트 프레임버퍼를 검사한다. Remmina 앱 자체의 자동화 시험과 실물 USB invoer_WAARDE 시험은 별개다.

결과와 scherm: [Shell resultaat](build/verification/shell/report.json), [VNC resultaat](build/verification/desktop/report.json), [terminal scherm](build/verification/desktop/vnc-terminal.png). lettertype_WAARDE oorsprong_WAARDE·hash_Bestand·라이선스는 [vendor](vendor/README.md)에 있다.

## 마우스로 Grootte wijzigen_WAARDE

네 모서리의 안쪽 8픽셀에 마우스를 대면 방향에 맞는 대각선 양방향 포인터가
나타난다. **왼쪽 버튼을 누른 채 끌고 놓는다.** recht 버튼으로는 크기가 바뀌지 않는다.
venster_Titel 표시줄의 나머지 부분은 verplaatsen_WAARDE_83b651b8, recht 위 X는 닫기다.
최소 크기는 360×216이며 최대 크기는 actueel_item scherm 안에 제한된다.
각 창의 teken_WAARDE 칸은 `(폭-24)/8`KOLOM_WAARDE, `(hoogte_WAARDE-56)/16`행이다. `terminal size`로 조회한다.

명령줄의 invoer_WAARDE·cursor_WAARDE·기록과 vi의 미저장 문서를 유지하며 보이는 영역을 갱신한다.
지난 출력은 저장된 invoerregel 단위를 유지하고, 좁아진 창에서 가려진 열은 opnieuw_proberen_WAARDE 넓히면
볼 nummer 있다. 과거 tekstuitvoer 전체를 새 너비에 맞춰 재배열하는 기능은 아니다.
크기를 바꾼 BACK_WAARDE 출력되는 글은 새 KOLOM_WAARDE 수로 줄바꿈한다. vi는 invoer_WAARDE wachten_WAARDE 중에도
SVC 16의 Actie 3으로 actueel_item Grootte(상위 16비트 RIJ_WAARDE, 하위 16비트 KOLOM_WAARDE)를 조회한다.
interactief tty의 kernel_WAARDE scherm tekstuitvoer 시간은 gebruikersruimte 계산 기한에서 제외하며, invoer_WAARDE wachten_WAARDE 없이
계산만 반복하는 gebruikersruimte 프로그램의 TIJD_WAARDE 제한은 유지한다.
커널이 프레임버퍼에 포인터를 그리며, Remmina 중계는 extern_WAARDE_28edcfa1 포인터를 숨겨 중복을 피한다.
로컬 VNC 중계는 standaardwaarde Raw 인코딩을 사용한다.

valideren: `make test-resize` — 640×480·1920×1080에서 네 모서리, 왼쪽/recht 버튼,
최소·최대 Grootte, wijzer 복원, invoer_WAARDE 보존, vi Store_WAARDE·계속 invoer_WAARDE, 창별 크기를 확인한다.
