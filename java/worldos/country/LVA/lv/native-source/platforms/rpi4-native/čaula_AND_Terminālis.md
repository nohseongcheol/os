# savs 커널의 GUI 터미널과 čaula

이 터미널은 savs Java 커널의 셸을 프레임버퍼 창과 UART에서 사용한다. Komanda Process_VALUE_ievade·RAM Fails·파이프는 Java kodols_VALUE, 화면의 rakstzīme_VALUE 그리기는 freestanding C에서 수행한다. Linux·X11·Bash 없이 동작하며, savs JVM의 Swing Atbalsts_VALUE 부분집합도 같은 Logs 시스템을 이용한다. 자세한 vi·다중 Logs·코딩 사용법은 [개발 매뉴얼](개발안내.md)을 참고한다.

## pašreizējais_krājums 컴퓨터에서 Izpildīt_komanda

```sh
cd /home/user/jkoros/platforms/rpi4-native
make desktop
```

Remmina에서 **VNC**, adrese **127.0.0.1:5902**로 연결한다. Terminālis 창은 자동으로 열린다. 연결한 VNC 창에 키를 입력하면 savs 커널의 셸로 전달된다. 종료하려면 `make desktop`을 실행한 viesot 터미널에서 Ctrl+C를 누른다. 포트를 바꾸려면 būvējums_sistēma 후 `python3 Rīki/Izpildīt_komanda.py --desktop --port 5903`을 사용한다. 서버는 localhost에만 바인드하며 동시에 한 클라이언트가 제어한다.

일반 UART 셸은 `make run`으로 시작한다. QEMU 종료는 Ctrl+A Tālāk_krājums X이다. 같은 VM의 UART에서 `terminal` 또는 F12로 GUI 터미널을 COLUMN_VALUE numurs 있다. `gui` Izpildīt_komanda 화면에서는 다섯 번째 **OPEN TERMINAL** 버튼, cipars_VALUE 5 또는 T로 연다. `--vnc 127.0.0.1:2`만 사용한 기존 Izpildīt_komanda 방식은 화면 보기용이며, VNC 키보드를 연결하려면 `--desktop`을 사용한다.

FTP와 ārējs_VALUE 네트워크도 함께 쓰려면 `python3 Rīki/Izpildīt_komanda.py --desktop --network`로
실행한다. Remmina VNC는 `127.0.0.1:5902`, 게스트에서 `ftpd start` 후 FTP는
`127.0.0.1:2121`이다. `--port`, `--ftp-port`, `--forward`를 함께 지정할 numurs 있다.
한 VM의 보조 UART로 SLIP를 전송하고 주 UART로 GUI 입력을 전달한다.

QEMU Izpildīt_komanda 도구가 VNC 키보드/마우스를 UART 입력으로 변환한다. faktisks_dati Pi4의 USB 키보드·마우스 드라이버를 구현한 것은 아니다. faktisks_dati 보드에서는 pašreizējais_krājums UART 입력이 필요하며 실물 부팅은 아직 미검증이다.

## 창과 입력

- 640×480~1920×1080 화면에서 최대 네 개 Terminālis Logs, noklusējuma_vērtība 568×360(68열 × 19행)과 pēdējās_VALUE 160행 보관, noklusējuma_vērtība ANSI 색상·kursors_VALUE·dzēst_ievade Process_VALUE_ievade.
- 상단 **+ New terminal** 또는 Ctrl+Shift+T로 새 창을 연다. 제목줄을 끌어 이동하고 Logs/상단 버튼을 클릭하거나 F6으로 전환한다. 각 창의 작업 CEĻŠ·mainīgais_VALUE·Komanda LOG_RECORD·입력 중인 줄은 독립적이다.
- UTF-8 한글·CJK·라틴 문자와 일부 이모지 비트맵 fonts_VALUE. 복잡한 문자 조판·결합 문자·양방향 Saite_shēma·모든 Unicode 글리프를 보장하지 않는다.
- 좌우 방향키/Home/End/Delete/Backspace로 명령을 편집하고 위아래 방향키로 pēdējās_VALUE 16개 명령을 찾는다. 긴 명령은 입력 줄을 가로로 이동해 보여 주며 `<`, `>`가 숨겨진 부분을 나타낸다.
- Tab은 Komanda Nosaukums 또는 pašreizējais_krājums 디렉터리의 파일명에서 후보가 하나일 때 완성한다. 디렉터리를 포함한 CEĻŠ 접두사·Citāts 안의 완성은 아직 없다.
- Ctrl+A/E: 처음/끝, Ctrl+U/K: kursors_VALUE priekšējā_VALUE/ATPAKAĻ_VALUE 삭제, Ctrl+C: 입력 Atcelt_operācija. Izpildīt_komanda 중인 임의 프로그램에 SIGINT를 보내는 기능은 없다. vi와 Swing의 입력 대기는 Izpildīt_komanda 기한을 갱신하지만 일반 계산의 약 2초 제한은 유지한다.
- PgUp/PgDn 또는 마우스 휠: 이전 Izvade. 새 출력이 오면 최신 위치로 돌아온다.
- F12/virsrakstjosla RIGHT 버튼/`exit`: Logs Aizvērt. 빈 입력에서 Ctrl+D도 창을 닫는다. VM을 종료하는 명령은 아니다.

`--desktop`의 VNC 입력 연결에 **두벌식 한글 salikums_VALUE**을 제공한다. 접속한 PC의
입력기를 영어로 두고 **F9**, **Shift+Space**, **한/nulle_operands Atslēga_VALUE** 중 하나를 누르면
Logs 제목이 `[EN]`에서 `[KO]`로 바뀐다. `gksrmf` → `한글`,
`dkssudgktpdy` → `안녕하세요`. 같은 키로 영어로 돌아간다.
겹받침·복합 모음과 salikums_VALUE 단계별 Backspace를 지원한다. kursors_VALUE pārvietot_VALUE·마우스 klikšķis_VALUE·
단축키·ielīmēt_VALUE·Enter 때 조합을 확정한다. PC가 Shift+Space나 한/nulle_operands 키를
savs 처리하면 **F9**를 사용한다. Alt 단독은 SWITCH_MODE 키가 아니다.

이 조합기는 QEMU의 VNC→UART 입력 연결에서 실행된다. 일반 직렬 접속과
실물 Pi의 USB 키보드 입력기에 추가된 기능은 아니다. 이미 완성된 Unicode
한글 키도 그대로 전달한다. 클립보드 공유가 활성화되어 표준 VNC ClientCutText가
도착하면 Ctrl+Shift+V로 붙여 넣는다. 클립보드 동기화만으로 명령을 실행하지 않는다.
줄바꿈을 포함해 명시적으로 붙여 넣으면 해당 줄이 실행된다.

게스트에서 `help` 또는 `help ko`를 입력하면 한글 입력 안내를 볼 numurs 있다.
`help`와 `help ko`에는 한/nulle_operands Atslēga_VALUE·Shift+Space·F9 및 `[EN]`/`[KO]` 안내를 표시한다.
긴 도움말은 PgUp/PgDn으로 스크롤한다.

터미널에서 Java·Python·C++ Izpildīt_komanda 결과를 바로 볼 numurs 있다. 프로그램이 직접 프레임버퍼에 그림을 그린 경우 Iziet_programma 후 Terminālis 창을 복원한다. vi/Swing pagaidi_VALUE 중 다른 창으로 전환하면 해당 EL0 프로그램의 atmiņa_dati·레지스터를 보관하고 돌아올 때 재개한다. atlase_VALUE kopēt_VALUE·PTY·전체 VT100/xterm 호환과 임의 프로그램의 동시 병렬 실행은 제공하지 않는다. X로 닫으면 해당 창의 프로그램도 종료되므로 vi에서 저장하지 않은 내용은 사라진다.

## Komanda

| Komanda | klips |
|---|---|
| `help`, `info` | 사용법과 구현 Statuss_VALUE |
| `pwd`, `cd [DIR]`, `ls [-l] [PATH]` | pašreizējais_krājums CEĻŠ·디렉터리/Fails ievade_Saraksts; Parametri 없는 cd는 `/` |
| `mkdir DIR`, `rmdir DIR` | 디렉터리 한 개 atvērt_ievade/빈 디렉터리 삭제; `-p` 없음 |
| `touch FILE`, `rm FILE...` | Fails atvērt_ievade/삭제; timestamp_VALUE msinfo32_exe 없음 |
| `cp SOURCE DEST`, `mv SOURCE DEST` | Fails kopēt_VALUE/Nosaukums mainīt_VALUE; 대상은 정확한 Fails CEĻŠ, 재귀/디렉터리 pārvietot_VALUE 없음 |
| `cat [FILE...]` | Fails 또는 표준 입력을 byte_VALUE 그대로 Izvade |
| `echo [-n] [ARGS...]` | Parametri Izvade; `-e` 이스케이프 paplašinājums_VALUE 없음 |
| `wc [-c\|-l\|-w] [FILE]` | byte_VALUE/Līniju/Word_VALUE numurs; Word_VALUE 구분은 ASCII 공백 |
| `grep TEXT [FILE]` | 정규식 없이 문자열이 포함된 Līniju Izvade; 일치 없으면 Statuss_VALUE 1 |
| `head [-n N] [FILE]`, `tail [-n N] [FILE]` | priekšējā_VALUE/ATPAKAĻ_VALUE N줄, noklusējuma_vērtība 10줄 |
| `tee [-a] FILE` | 표준 입력을 파일과 표준 출력에 LOG_RECORD |
| `export NAME=VALUE`, `unset NAME`, `env` | čaula mainīgais_VALUE Uzstādījumi·삭제·ievade_Saraksts; HOME/PWD는 Lasīt 전용 |
| `sh FILE`, `source FILE` | Komanda 파일을 같은 čaula 환경에서 줄별 Izpildīt_komanda; 최대 ligzda_VALUE 3 |
| `true`, `false`, `exit [N]` | Statuss_VALUE 0/1; skripts_VALUE 안의 exit는 pašreizējais_krājums skripts_VALUE Iziet_programma |
| `history`, `clear` | Komanda LOG_RECORD·화면 dzēst_ievade |
| `vi FILE` | EL0 vi metode_MODE Redaktors: 입력/Komanda MODE_VALUE, UTF-8 pārvietot_VALUE, 검색, 삭제·kopēt_VALUE·ielīmēt_SMS·되돌리기, `:w`/`:q`/`:wq` |
| `edit FILE`, `load FILE`, `hex FILE` | 전체 Saturs_VALUE 교체 Rediģēt_VALUE, 16진수 업로드/vaicāt_VALUE; 단독 `.` 줄로 Store_VALUE |
| `javac`, `java`, `python`, `run` | 기존 savs Java Rīki·MicroPython·EL0 C++/ELF Izpildīt_komanda |

`net test`, `tasks`, `selftest`, `samples`도 유지한다. programma_f5044b9b Izpildīt_komanda 범위는 [README](fails_Lasi_mani_eb81d7d9.md)와 [Java Izpildīt_komanda 환경](자바실행환경.md)을 참고한다.

```sh
mkdir 작업
cd 작업
echo "안녕하세요" > 인사.txt
echo "반갑습니다" >> 인사.txt
cat < 인사.txt | grep 안녕 | tee 추림.txt | wc -l
cp 인사.txt kopēt_VALUE.txt
mv kopēt_VALUE.txt 새이름.txt
export Nosaukums=누리
echo "$이름: ${PWD}"
false && echo 건너뜀 || echo atgūt_Statuss
python -c 'print(123)' > mērs.txt
echo 입력 | python -c 'import jkoros; print(jkoros.stdin(64))'
echo 'echo "$이름"' > Izpildīt_komanda.sh
sh Izpildīt_komanda.sh
echo $?
```

## 문법과 제한

작은따옴표·큰따옴표·백슬래시, `$NAME`/`${NAME}`/`$?`, Word_VALUE priekšējā_VALUE `~`, Līniju 주석 `#`, 순차 Izpildīt_komanda `;`, nosacījums Izpildīt_komanda `&&`/`||`, 파이프 `|`, 입력 `<`, 새 Izvade `>`, Pievienot_ievade Izvade `>>`를 제공한다. mainīgais_VALUE 확장은 Parametri 안에서 수행하며 paplašinājums_VALUE 결과를 공백으로 mēģināt_vēlreiz_VALUE 나누지 않는다. `export`의 값은 čaula 안에서만 공유하며 lietotājs ELF의 envp/getenv 환경은 아직 없다.

파이프는 각 단계를 순서대로 실행하고 최대 **16384바이트**를 Tālāk_krājums 단계로 넘긴다. 여러 프로세스가 동시에 읽고 쓰는 POSIX 파이프가 아니다. noslodze_VALUE 초과는 Kļūda 28과 kļūme_VALUE 상태를 반환하고 해당 실행을 중단한다. `<`는 EOF를 제공하며 `>`/`>>`는 stdout만 바꾼다. EL0 fd 2는 화면/UART로 출력된다. `2>` 등 번호를 붙인 리다이렉션은 거부한다. 일부 내장 명령의 진단은 stdout을 사용한다. 연결한 프로그램의 `exit N` 진단은 데이터에 섞이지 않도록 생략한다.

`vi`, `edit`, `load`, `gui`, `terminal`, `sh`, `source`에는 파이프와 리다이렉션을 적용할 numurs 없다. 리다이렉션 파일을 열지 못하거나 파이프 용량을 초과하면 pašreizējais_krājums 명령줄을 중단하며, 그 줄의 뒤쪽 `||` 명령도 실행하지 않는다. skripts_VALUE 파일을 입력할 때 멀티라인 Citāts·이어 쓰기는 제공하지 않는다. `if`/`for`/`while`, FUNCTION_VALUE, Komanda 치환, glob, 별칭, 백그라운드 `&`, jobs/fg/bg, 일반 프로세스·신호·PTY는 아직 없다. Bash/POSIX sh 전체 호환으로 표시하지 않는다.

Fails 64개 × 각 16384바이트, 루트 외 디렉터리 15개, Fails 서술자 16개, CEĻŠ 최대 UTF-8 63바이트다. vienranga_VALUE/절대 경로와 `.`/`..`를 정규화하지만 atļauja_VALUE·심볼릭 링크·마운트·디스크 영속 저장은 없다. **Fails·디렉터리·mainīgais_VALUE·기록의 수정 내용은 재부팅하면 사라진다.** lietotājs 실행도 pašreizējais_krājums čaula 경로를 사용한다. Java/Python/C++의 Fails API는 같은 RAM 저장소를 본다. `/example`의 세 Valodas 예제와 설명서는 부팅할 때 원본으로 준비된다.

한 명령줄은 4096바이트, 구문 daļiņa_VALUE 128개, Izpildīt_komanda Parametri 32개, 변수는 16개(Nosaukums 31바이트·VALUE 255바이트)까지다. lietotājs 프로그램에 전달하는 인수는 기존 ABI대로 최대 8개·각 255바이트다. Komanda 기록은 1024바이트 이하 줄을 pēdējās_VALUE 16개까지 저장한다.

## 재현 가능한 시험

```sh
make test-shell
make test-desktop
make test-windows
make test-swing
make test
```

čaula 시험은 faktisks_dati raspi4b QEMU에서 CEĻŠ·Fails·mainīgais_VALUE·nosacījums·파이프·리다이렉션·Kļūda atgūt_Statuss·skripts_VALUE·편집을 검사하고, Java/Python 출력과 Python stdin의 EOF를 확인한다. VNC 시험은 faktisks_dati RFB 클라이언트로 한글 Atslēga_VALUE·Ctrl salikums_VALUE·명시적 ielīmēt_VALUE·마우스와 게스트 프레임버퍼를 검사한다. Remmina 앱 자체의 자동화 시험과 실물 USB 입력 시험은 별개다.

결과와 화면: [čaula mērs](build/verification/shell/report.json), [VNC mērs](build/verification/desktop/report.json), [Terminālis 화면](build/verification/desktop/vnc-terminal.png). fonts_VALUE 출처·jaukšana_Fails·라이선스는 [vendor](vendor/README.md)에 있다.

## 마우스로 Izmērs mainīt_VALUE

네 모서리의 안쪽 8픽셀에 마우스를 대면 방향에 맞는 대각선 양방향 포인터가
나타난다. **왼쪽 버튼을 누른 채 끌고 놓는다.** RIGHT 버튼으로는 크기가 바뀌지 않는다.
logs_nosaukums 표시줄의 나머지 부분은 pārvietot_VALUE, RIGHT 위 X는 닫기다.
최소 크기는 360×216이며 최대 크기는 pašreizējais_krājums 화면 안에 제한된다.
각 창의 rakstzīme_VALUE 칸은 `(폭-24)/8`COLUMN_VALUE, `(높이-56)/16`행이다. `terminal size`로 조회한다.

명령줄의 입력·kursors_VALUE·기록과 vi의 미저장 문서를 유지하며 보이는 영역을 갱신한다.
지난 출력은 저장된 Līniju 단위를 유지하고, 좁아진 창에서 가려진 열은 mēģināt_vēlreiz_VALUE 넓히면
볼 numurs 있다. 과거 Izvade 전체를 새 너비에 맞춰 재배열하는 기능은 아니다.
크기를 바꾼 ATPAKAĻ_VALUE 출력되는 글은 새 COLUMN_VALUE 수로 줄바꿈한다. vi는 입력 pagaidi_VALUE 중에도
SVC 16의 Darbība 3으로 pašreizējais_krājums Izmērs(상위 16비트 ROW_VALUE, 하위 16비트 COLUMN_VALUE)를 조회한다.
대화형 tty의 kodols_VALUE 화면 Izvade 시간은 lietotājs 계산 기한에서 제외하며, 입력 pagaidi_VALUE 없이
계산만 반복하는 lietotājs 프로그램의 TIME_VALUE 제한은 유지한다.
커널이 프레임버퍼에 포인터를 그리며, Remmina 중계는 attāls_VALUE 포인터를 숨겨 중복을 피한다.
로컬 VNC 중계는 noklusējuma_vērtība Raw 인코딩을 사용한다.

validēt: `make test-resize` — 640×480·1920×1080에서 네 모서리, 왼쪽/RIGHT 버튼,
최소·최대 Izmērs, rādītājs 복원, 입력 보존, vi Store_VALUE·계속 입력, 창별 크기를 확인한다.
