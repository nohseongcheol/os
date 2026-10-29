# 자체 커널의 GUI 터미널과 blaosc

이 터미널은 자체 Java 커널의 셸을 프레임버퍼 창과 UART에서 사용한다. Ordú Próiseas_VALUE_iontráil·RAM Comhad·파이프는 Java eithne_VALUE, 화면의 carachtar_VALUE 그리기는 freestanding C에서 수행한다. Linux·X11·Bash 없이 동작하며, 자체 JVM의 Swing Tacaíocht_VALUE 부분집합도 같은 fuinneog 시스템을 이용한다. 자세한 vi·다중 fuinneog·코딩 사용법은 [개발 매뉴얼](개발안내.md)을 참고한다.

## 현재 컴퓨터에서 Rith_ordú

```sh
cd /home/user/jkoros/platforms/rpi4-native
make desktop
```

Remmina에서 **VNC**, ADDRESS **127.0.0.1:5902**로 연결한다. Teirminéal 창은 자동으로 열린다. 연결한 VNC 창에 키를 입력하면 자체 커널의 셸로 전달된다. 종료하려면 `make desktop`을 실행한 óstach 터미널에서 Ctrl+C를 누른다. 포트를 바꾸려면 tóg_córas 후 `python3 Uirlisí/Rith_ordú.py --desktop --port 5903`을 사용한다. 서버는 localhost에만 바인드하며 동시에 한 클라이언트가 제어한다.

일반 UART 셸은 `make run`으로 시작한다. QEMU 종료는 Ctrl+A Ar_aghaidh_mír X이다. 같은 VM의 UART에서 `terminal` 또는 F12로 GUI 터미널을 colún_VALUE 수 있다. `gui` Rith_ordú 화면에서는 다섯 번째 **OPEN TERMINAL** 버튼, digit_VALUE 5 또는 T로 연다. `--vnc 127.0.0.1:2`만 사용한 기존 Rith_ordú 방식은 화면 보기용이며, VNC 키보드를 연결하려면 `--desktop`을 사용한다.

FTP와 외부 네트워크도 함께 쓰려면 `python3 Uirlisí/Rith_ordú.py --desktop --network`로
실행한다. Remmina VNC는 `127.0.0.1:5902`, 게스트에서 `ftpd start` 후 FTP는
`127.0.0.1:2121`이다. `--port`, `--ftp-port`, `--forward`를 함께 지정할 수 있다.
한 VM의 보조 UART로 SLIP를 전송하고 주 UART로 GUI 입력을 전달한다.

QEMU Rith_ordú 도구가 VNC 키보드/마우스를 UART 입력으로 변환한다. iarbhír_sonraí Pi4의 USB 키보드·마우스 드라이버를 구현한 것은 아니다. iarbhír_sonraí 보드에서는 현재 UART 입력이 필요하며 실물 부팅은 아직 미검증이다.

## 창과 입력

- 640×480~1920×1080 화면에서 최대 네 개 Teirminéal fuinneog, luach_réamhshocraithe 568×360(68열 × 19행)과 le_déanaí_VALUE 160행 보관, luach_réamhshocraithe ANSI 색상·cúrsóir_VALUE·지우기 Próiseas_VALUE_iontráil.
- 상단 **+ New terminal** 또는 Ctrl+Shift+T로 새 창을 연다. 제목줄을 끌어 이동하고 fuinneog/상단 버튼을 클릭하거나 F6으로 전환한다. 각 창의 작업 CONAIR·변수·Ordú LOG_ró·입력 중인 줄은 독립적이다.
- UTF-8 한글·CJK·라틴 문자와 일부 이모지 비트맵 clófhoireann_VALUE. 복잡한 문자 조판·결합 문자·양방향 Nasc_dáileadh·모든 Unicode 글리프를 보장하지 않는다.
- 좌우 방향키/Home/End/Delete/Backspace로 명령을 편집하고 위아래 방향키로 le_déanaí_VALUE 16개 명령을 찾는다. 긴 명령은 입력 줄을 가로로 이동해 보여 주며 `<`, `>`가 숨겨진 부분을 나타낸다.
- Tab은 Ordú Ainm 또는 현재 디렉터리의 파일명에서 후보가 하나일 때 완성한다. 디렉터리를 포함한 CONAIR 접두사·Athfhriotail 안의 완성은 아직 없다.
- Ctrl+A/E: 처음/끝, Ctrl+U/K: cúrsóir_VALUE 앞/Siar_VALUE 삭제, Ctrl+C: 입력 Cealaigh_oibríocht. Rith_ordú 중인 임의 프로그램에 SIGINT를 보내는 기능은 없다. vi와 Swing의 입력 대기는 Rith_ordú 기한을 갱신하지만 일반 계산의 약 2초 제한은 유지한다.
- PgUp/PgDn 또는 마우스 휠: 이전 Aschur. 새 출력이 오면 최신 위치로 돌아온다.
- F12/barra_teidil RIGHT 버튼/`exit`: fuinneog Dún. 빈 입력에서 Ctrl+D도 창을 닫는다. VM을 종료하는 명령은 아니다.

`--desktop`의 VNC 입력 연결에 **두벌식 한글 조합**을 제공한다. 접속한 PC의
입력기를 영어로 두고 **F9**, **Shift+Space**, **한/영 eochair_VALUE** 중 하나를 누르면
fuinneog 제목이 `[EN]`에서 `[KO]`로 바뀐다. `gksrmf` → `한글`,
`dkssudgktpdy` → `안녕하세요`. 같은 키로 영어로 돌아간다.
겹받침·복합 모음과 조합 단계별 Backspace를 지원한다. cúrsóir_VALUE bog_VALUE·마우스 cliceáil_VALUE·
단축키·greamaigh_VALUE·Enter 때 조합을 확정한다. PC가 Shift+Space나 한/영 키를
자체 처리하면 **F9**를 사용한다. Alt 단독은 SWITCH_mód 키가 아니다.

이 조합기는 QEMU의 VNC→UART 입력 연결에서 실행된다. 일반 직렬 접속과
실물 Pi의 USB 키보드 입력기에 추가된 기능은 아니다. 이미 완성된 Unicode
한글 키도 그대로 전달한다. 클립보드 공유가 활성화되어 표준 VNC ClientCutText가
도착하면 Ctrl+Shift+V로 붙여 넣는다. 클립보드 동기화만으로 명령을 실행하지 않는다.
줄바꿈을 포함해 명시적으로 붙여 넣으면 해당 줄이 실행된다.

게스트에서 `help` 또는 `help ko`를 입력하면 한글 입력 안내를 볼 수 있다.
`help`와 `help ko`에는 한/영 eochair_VALUE·Shift+Space·F9 및 `[EN]`/`[KO]` 안내를 표시한다.
긴 도움말은 PgUp/PgDn으로 스크롤한다.

터미널에서 Java·Python·C++ Rith_ordú 결과를 바로 볼 수 있다. 프로그램이 직접 프레임버퍼에 그림을 그린 경우 scoir_clár 후 Teirminéal 창을 복원한다. vi/Swing 대기 중 다른 창으로 전환하면 해당 EL0 프로그램의 Cuimhne_sonraí·레지스터를 보관하고 돌아올 때 재개한다. roghnú_VALUE ásc_VALUE·PTY·전체 VT100/xterm 호환과 임의 프로그램의 동시 병렬 실행은 제공하지 않는다. X로 닫으면 해당 창의 프로그램도 종료되므로 vi에서 저장하지 않은 내용은 사라진다.

## Ordú

| Ordú | gearrthóg |
|---|---|
| `help`, `info` | 사용법과 구현 staid_VALUE |
| `pwd`, `cd [DIR]`, `ls [-l] [PATH]` | 현재 CONAIR·디렉터리/Comhad iontráil_Liosta; Argóintí 없는 cd는 `/` |
| `mkdir DIR`, `rmdir DIR` | 디렉터리 한 개 Create_iontráil/빈 디렉터리 삭제; `-p` 없음 |
| `touch FILE`, `rm FILE...` | Comhad Create_iontráil/삭제; 시각 msinfo32_exe 없음 |
| `cp SOURCE DEST`, `mv SOURCE DEST` | Comhad ásc_VALUE/Ainm athraigh_VALUE; 대상은 정확한 Comhad CONAIR, 재귀/디렉터리 bog_VALUE 없음 |
| `cat [FILE...]` | Comhad 또는 표준 입력을 beart_VALUE 그대로 Aschur |
| `echo [-n] [ARGS...]` | Argóintí Aschur; `-e` 이스케이프 breisiú_VALUE 없음 |
| `wc [-c\|-l\|-w] [FILE]` | beart_VALUE/Líne/Word_VALUE 수; Word_VALUE 구분은 ASCII 공백 |
| `grep TEXT [FILE]` | 정규식 없이 문자열이 포함된 Líne Aschur; 일치 없으면 staid_VALUE 1 |
| `head [-n N] [FILE]`, `tail [-n N] [FILE]` | 앞/Siar_VALUE N줄, luach_réamhshocraithe 10줄 |
| `tee [-a] FILE` | 표준 입력을 파일과 표준 출력에 LOG_ró |
| `export NAME=VALUE`, `unset NAME`, `env` | blaosc 변수 Socruithe·삭제·iontráil_Liosta; HOME/PWD는 Léigh 전용 |
| `sh FILE`, `source FILE` | Ordú 파일을 같은 blaosc 환경에서 줄별 Rith_ordú; 최대 중첩 3 |
| `true`, `false`, `exit [N]` | staid_VALUE 0/1; script_VALUE 안의 exit는 현재 script_VALUE scoir_clár |
| `history`, `clear` | Ordú LOG_ró·화면 지우기 |
| `vi FILE` | EL0 vi modh_mód Eagarthóir: 입력/Ordú mód_VALUE, UTF-8 bog_VALUE, 검색, 삭제·ásc_VALUE·greamaigh_SMS·되돌리기, `:w`/`:q`/`:wq` |
| `edit FILE`, `load FILE`, `hex FILE` | 전체 Inneachar_VALUE 교체 cuir_in_eagar_VALUE, 16진수 업로드/iarratas_VALUE; 단독 `.` 줄로 Store_VALUE |
| `javac`, `java`, `python`, `run` | 기존 자체 Java Uirlisí·MicroPython·EL0 C++/ELF Rith_ordú |

`net test`, `tasks`, `selftest`, `samples`도 유지한다. clár_f5044b9b Rith_ordú 범위는 [README](LÉIGHMÉ_eb81d7d9.md)와 [Java Rith_ordú 환경](자바실행환경.md)을 참고한다.

```sh
mkdir 작업
cd 작업
echo "안녕하세요" > 인사.txt
echo "반갑습니다" >> 인사.txt
cat < 인사.txt | grep 안녕 | tee 추림.txt | wc -l
cp 인사.txt ásc_VALUE.txt
mv ásc_VALUE.txt 새이름.txt
export Ainm=누리
echo "$이름: ${PWD}"
false && echo 건너뜀 || echo athshlánaigh_staid
python -c 'print(123)' > tomhas.txt
echo 입력 | python -c 'import jkoros; print(jkoros.stdin(64))'
echo 'echo "$이름"' > Rith_ordú.sh
sh Rith_ordú.sh
echo $?
```

## 문법과 제한

작은따옴표·큰따옴표·백슬래시, `$NAME`/`${NAME}`/`$?`, Word_VALUE 앞 `~`, Líne 주석 `#`, 순차 Rith_ordú `;`, coinníoll Rith_ordú `&&`/`||`, 파이프 `|`, 입력 `<`, 새 Aschur `>`, 추가 Aschur `>>`를 제공한다. 변수 확장은 Argóintí 안에서 수행하며 breisiú_VALUE 결과를 공백으로 다시 나누지 않는다. `export`의 값은 blaosc 안에서만 공유하며 úsáideoir ELF의 envp/getenv 환경은 아직 없다.

파이프는 각 단계를 순서대로 실행하고 최대 **16384바이트**를 Ar_aghaidh_mír 단계로 넘긴다. 여러 프로세스가 동시에 읽고 쓰는 POSIX 파이프가 아니다. 용량 초과는 ERREÁID 28과 teip_VALUE 상태를 반환하고 해당 실행을 중단한다. `<`는 EOF를 제공하며 `>`/`>>`는 stdout만 바꾼다. EL0 fd 2는 화면/UART로 출력된다. `2>` 등 번호를 붙인 리다이렉션은 거부한다. 일부 내장 명령의 진단은 stdout을 사용한다. 연결한 프로그램의 `exit N` 진단은 데이터에 섞이지 않도록 생략한다.

`vi`, `edit`, `load`, `gui`, `terminal`, `sh`, `source`에는 파이프와 리다이렉션을 적용할 수 없다. 리다이렉션 파일을 열지 못하거나 파이프 용량을 초과하면 현재 명령줄을 중단하며, 그 줄의 뒤쪽 `||` 명령도 실행하지 않는다. script_VALUE 파일을 입력할 때 멀티라인 Athfhriotail·이어 쓰기는 제공하지 않는다. `if`/`for`/`while`, feidhm_VALUE, Ordú 치환, glob, 별칭, 백그라운드 `&`, jobs/fg/bg, 일반 프로세스·신호·PTY는 아직 없다. Bash/POSIX sh 전체 호환으로 표시하지 않는다.

Comhad 64개 × 각 16384바이트, 루트 외 디렉터리 15개, Comhad 서술자 16개, CONAIR 최대 UTF-8 63바이트다. piara_VALUE/절대 경로와 `.`/`..`를 정규화하지만 cead_VALUE·심볼릭 링크·마운트·디스크 영속 저장은 없다. **Comhad·디렉터리·변수·기록의 수정 내용은 재부팅하면 사라진다.** úsáideoir 실행도 현재 blaosc 경로를 사용한다. Java/Python/C++의 Comhad API는 같은 RAM 저장소를 본다. `/example`의 세 Teanga 예제와 설명서는 부팅할 때 원본으로 준비된다.

한 명령줄은 4096바이트, 구문 licín_VALUE 128개, Rith_ordú Argóintí 32개, 변수는 16개(Ainm 31바이트·VALUE 255바이트)까지다. úsáideoir 프로그램에 전달하는 인수는 기존 ABI대로 최대 8개·각 255바이트다. Ordú 기록은 1024바이트 이하 줄을 le_déanaí_VALUE 16개까지 저장한다.

## 재현 가능한 시험

```sh
make test-shell
make test-desktop
make test-windows
make test-swing
make test
```

blaosc 시험은 iarbhír_sonraí raspi4b QEMU에서 CONAIR·Comhad·변수·coinníoll·파이프·리다이렉션·ERREÁID athshlánaigh_staid·script_VALUE·편집을 검사하고, Java/Python 출력과 Python stdin의 EOF를 확인한다. VNC 시험은 iarbhír_sonraí RFB 클라이언트로 한글 eochair_VALUE·Ctrl 조합·명시적 greamaigh_VALUE·마우스와 게스트 프레임버퍼를 검사한다. Remmina 앱 자체의 자동화 시험과 실물 USB 입력 시험은 별개다.

결과와 화면: [blaosc tomhas](build/verification/shell/report.json), [VNC tomhas](build/verification/desktop/report.json), [Teirminéal 화면](build/verification/desktop/vnc-terminal.png). clófhoireann_VALUE 출처·hais_comhad·라이선스는 [vendor](vendor/README.md)에 있다.

## 마우스로 Méid athraigh_VALUE

네 모서리의 안쪽 8픽셀에 마우스를 대면 방향에 맞는 대각선 양방향 포인터가
나타난다. **왼쪽 버튼을 누른 채 끌고 놓는다.** RIGHT 버튼으로는 크기가 바뀌지 않는다.
fuinneog_Teideal 표시줄의 나머지 부분은 bog_VALUE, RIGHT 위 X는 닫기다.
최소 크기는 360×216이며 최대 크기는 현재 화면 안에 제한된다.
각 창의 carachtar_VALUE 칸은 `(폭-24)/8`colún_VALUE, `(높이-56)/16`행이다. `terminal size`로 조회한다.

명령줄의 입력·cúrsóir_VALUE·기록과 vi의 미저장 문서를 유지하며 보이는 영역을 갱신한다.
지난 출력은 저장된 Líne 단위를 유지하고, 좁아진 창에서 가려진 열은 다시 넓히면
볼 수 있다. 과거 Aschur 전체를 새 너비에 맞춰 재배열하는 기능은 아니다.
크기를 바꾼 Siar_VALUE 출력되는 글은 새 colún_VALUE 수로 줄바꿈한다. vi는 입력 대기 중에도
SVC 16의 Gníomh 3으로 현재 Méid(상위 16비트 ró_VALUE, 하위 16비트 colún_VALUE)를 조회한다.
idirghníomhach tty의 eithne_VALUE 화면 Aschur 시간은 úsáideoir 계산 기한에서 제외하며, 입력 대기 없이
계산만 반복하는 úsáideoir 프로그램의 TIME_VALUE 제한은 유지한다.
커널이 프레임버퍼에 포인터를 그리며, Remmina 중계는 cianda_VALUE 포인터를 숨겨 중복을 피한다.
로컬 VNC 중계는 luach_réamhshocraithe Raw 인코딩을 사용한다.

bailíochtaigh: `make test-resize` — 640×480·1920×1080에서 네 모서리, 왼쪽/RIGHT 버튼,
최소·최대 Méid, pointeoir 복원, 입력 보존, vi Store_VALUE·계속 입력, 창별 크기를 확인한다.
