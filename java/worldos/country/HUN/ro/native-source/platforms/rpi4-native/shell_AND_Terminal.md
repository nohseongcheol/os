# propriu 커널의 GUI 터미널과 shell

이 터미널은 propriu Java 커널의 셸을 프레임버퍼 창과 UART에서 사용한다. Comandă Proces_VALUE_intrare·RAM Fișier·파이프는 Java nucleu_VALUE, 화면의 caracter_VALUE 그리기는 freestanding C에서 수행한다. Linux·X11·Bash 없이 동작하며, propriu JVM의 Swing suport_VALUE 부분집합도 같은 Fereastră 시스템을 이용한다. 자세한 vi·다중 Fereastră·코딩 사용법은 [개발 매뉴얼](개발안내.md)을 참고한다.

## curent_element 컴퓨터에서 executa_comandă

```sh
cd /home/user/jkoros/platforms/rpi4-native
make desktop
```

Remmina에서 **VNC**, adresa **127.0.0.1:5902**로 연결한다. Terminal 창은 자동으로 열린다. 연결한 VNC 창에 키를 입력하면 propriu 커널의 셸로 전달된다. 종료하려면 `make desktop`을 실행한 gazdă 터미널에서 Ctrl+C를 누른다. 포트를 바꾸려면 generare_sistem 후 `python3 Instrumente/executa_comandă.py --desktop --port 5903`을 사용한다. 서버는 localhost에만 바인드하며 동시에 한 클라이언트가 제어한다.

일반 UART 셸은 `make run`으로 시작한다. QEMU 종료는 Ctrl+A Următorul_element X이다. 같은 VM의 UART에서 `terminal` 또는 F12로 GUI 터미널을 COLUMN_VALUE 수 있다. `gui` executa_comandă 화면에서는 다섯 번째 **OPEN TERMINAL** 버튼, cifră_VALUE 5 또는 T로 연다. `--vnc 127.0.0.1:2`만 사용한 기존 executa_comandă 방식은 화면 보기용이며, VNC 키보드를 연결하려면 `--desktop`을 사용한다.

FTP와 extern_VALUE 네트워크도 함께 쓰려면 `python3 Instrumente/executa_comandă.py --desktop --network`로
실행한다. Remmina VNC는 `127.0.0.1:5902`, 게스트에서 `ftpd start` 후 FTP는
`127.0.0.1:2121`이다. `--port`, `--ftp-port`, `--forward`를 함께 지정할 수 있다.
한 VM의 보조 UART로 SLIP를 전송하고 주 UART로 GUI 입력을 전달한다.

QEMU executa_comandă 도구가 VNC 키보드/마우스를 UART 입력으로 변환한다. real_date Pi4의 USB 키보드·마우스 드라이버를 구현한 것은 아니다. real_date 보드에서는 curent_element UART 입력이 필요하며 실물 부팅은 아직 미검증이다.

## 창과 입력

- 640×480~1920×1080 화면에서 최대 네 개 Terminal Fereastră, valoare_implicită 568×360(68열 × 19행)과 recent_VALUE 160행 보관, valoare_implicită ANSI 색상·cursor_VALUE·șterge_intrare Proces_VALUE_intrare.
- 상단 **+ New terminal** 또는 Ctrl+Shift+T로 새 창을 연다. 제목줄을 끌어 이동하고 Fereastră/상단 버튼을 클릭하거나 F6으로 전환한다. 각 창의 작업 Cale·variabilă_VALUE·Comandă LOG_RECORD·입력 중인 줄은 독립적이다.
- UTF-8 한글·CJK·라틴 문자와 일부 이모지 비트맵 font_VALUE. 복잡한 문자 조판·결합 문자·양방향 Link_Aspect·모든 Unicode 글리프를 보장하지 않는다.
- 좌우 방향키/Home/End/Delete/Backspace로 명령을 편집하고 위아래 방향키로 recent_VALUE 16개 명령을 찾는다. 긴 명령은 입력 줄을 가로로 이동해 보여 주며 `<`, `>`가 숨겨진 부분을 나타낸다.
- Tab은 Comandă Nume 또는 curent_element 디렉터리의 파일명에서 후보가 하나일 때 완성한다. 디렉터리를 포함한 Cale 접두사·Citat 안의 완성은 아직 없다.
- Ctrl+A/E: 처음/끝, Ctrl+U/K: cursor_VALUE frontală_VALUE/ÎNAPOI_VALUE 삭제, Ctrl+C: 입력 anula_operație. executa_comandă 중인 임의 프로그램에 SIGINT를 보내는 기능은 없다. vi와 Swing의 입력 대기는 executa_comandă 기한을 갱신하지만 일반 계산의 약 2초 제한은 유지한다.
- PgUp/PgDn 또는 마우스 휠: Anteriorul_element Rezultat. 새 출력이 오면 최신 위치로 돌아온다.
- F12/bară_de_titlu RIGHT 버튼/`exit`: Fereastră Închide. 빈 입력에서 Ctrl+D도 창을 닫는다. VM을 종료하는 명령은 아니다.

`--desktop`의 VNC 입력 연결에 **두벌식 한글 조합**을 제공한다. 접속한 PC의
입력기를 영어로 두고 **F9**, **Shift+Space**, **한/zero_operand Cheie_VALUE** 중 하나를 누르면
Fereastră 제목이 `[EN]`에서 `[KO]`로 바뀐다. `gksrmf` → `한글`,
`dkssudgktpdy` → `안녕하세요`. 같은 키로 영어로 돌아간다.
겹받침·복합 모음과 조합 단계별 Backspace를 지원한다. cursor_VALUE muta_VALUE_83b651b8·마우스 clic_VALUE·
단축키·lipi_VALUE·Enter 때 조합을 확정한다. PC가 Shift+Space나 한/zero_operand 키를
propriu 처리하면 **F9**를 사용한다. Alt 단독은 SWITCH_mod 키가 아니다.

이 조합기는 QEMU의 VNC→UART 입력 연결에서 실행된다. 일반 직렬 접속과
실물 Pi의 USB 키보드 입력기에 추가된 기능은 아니다. 이미 완성된 Unicode
한글 키도 그대로 전달한다. 클립보드 공유가 활성화되어 표준 VNC ClientCutText가
도착하면 Ctrl+Shift+V로 붙여 넣는다. 클립보드 동기화만으로 명령을 실행하지 않는다.
줄바꿈을 포함해 명시적으로 붙여 넣으면 해당 줄이 실행된다.

게스트에서 `help` 또는 `help ko`를 입력하면 한글 입력 안내를 볼 수 있다.
`help`와 `help ko`에는 한/zero_operand Cheie_VALUE·Shift+Space·F9 및 `[EN]`/`[KO]` 안내를 표시한다.
긴 도움말은 PgUp/PgDn으로 스크롤한다.

터미널에서 Java·Python·C++ executa_comandă 결과를 바로 볼 수 있다. 프로그램이 직접 프레임버퍼에 그림을 그린 경우 ieși_program 후 Terminal 창을 복원한다. vi/Swing 대기 중 다른 창으로 전환하면 해당 EL0 프로그램의 Memorie_date·레지스터를 보관하고 돌아올 때 재개한다. selecție_VALUE copia_VALUE·PTY·전체 VT100/xterm 호환과 임의 프로그램의 동시 병렬 실행은 제공하지 않는다. X로 닫으면 해당 창의 프로그램도 종료되므로 vi에서 저장하지 않은 내용은 사라진다.

## Comandă

| Comandă | clip |
|---|---|
| `help`, `info` | 사용법과 구현 Stare_VALUE |
| `pwd`, `cd [DIR]`, `ls [-l] [PATH]` | curent_element Cale·디렉터리/Fișier intrare_Listă; Argumente 없는 cd는 `/` |
| `mkdir DIR`, `rmdir DIR` | 디렉터리 한 개 crea_intrare/빈 디렉터리 삭제; `-p` 없음 |
| `touch FILE`, `rm FILE...` | Fișier crea_intrare/삭제; marcă_de_timp_VALUE msinfo32_exe 없음 |
| `cp SOURCE DEST`, `mv SOURCE DEST` | Fișier copia_VALUE/Nume schimba_VALUE; 대상은 정확한 Fișier Cale, 재귀/디렉터리 muta_VALUE_83b651b8 없음 |
| `cat [FILE...]` | Fișier 또는 표준 입력을 byte_VALUE 그대로 Rezultat |
| `echo [-n] [ARGS...]` | Argumente Rezultat; `-e` 이스케이프 extensie_VALUE 없음 |
| `wc [-c\|-l\|-w] [FILE]` | byte_VALUE/Linie/Word_VALUE 수; Word_VALUE 구분은 ASCII 공백 |
| `grep TEXT [FILE]` | 정규식 없이 문자열이 포함된 Linie Rezultat; 일치 없으면 Stare_VALUE 1 |
| `head [-n N] [FILE]`, `tail [-n N] [FILE]` | frontală_VALUE/ÎNAPOI_VALUE N줄, valoare_implicită 10줄 |
| `tee [-a] FILE` | 표준 입력을 파일과 표준 출력에 LOG_RECORD |
| `export NAME=VALUE`, `unset NAME`, `env` | shell variabilă_VALUE Setări·삭제·intrare_Listă; HOME/PWD는 Citire 전용 |
| `sh FILE`, `source FILE` | Comandă 파일을 같은 shell 환경에서 줄별 executa_comandă; 최대 imbricare_VALUE 3 |
| `true`, `false`, `exit [N]` | Stare_VALUE 0/1; script_VALUE 안의 exit는 curent_element script_VALUE ieși_program |
| `history`, `clear` | Comandă LOG_RECORD·화면 șterge_intrare |
| `vi FILE` | EL0 vi metodă_mod Editor: 입력/Comandă mod_VALUE, UTF-8 muta_VALUE_83b651b8, 검색, 삭제·copia_VALUE·lipi_SMS·되돌리기, `:w`/`:q`/`:wq` |
| `edit FILE`, `load FILE`, `hex FILE` | 전체 Conținut_VALUE 교체 edita_VALUE, 16진수 업로드/interoga_VALUE; 단독 `.` 줄로 Store_VALUE |
| `javac`, `java`, `python`, `run` | 기존 propriu Java Instrumente·MicroPython·EL0 C++/ELF executa_comandă |

`net test`, `tasks`, `selftest`, `samples`도 유지한다. program_f5044b9b executa_comandă 범위는 [README](안내.md)와 [Java executa_comandă 환경](자바실행환경.md)을 참고한다.

```sh
mkdir 작업
cd 작업
echo "안녕하세요" > 인사.txt
echo "반갑습니다" >> 인사.txt
cat < 인사.txt | grep 안녕 | tee 추림.txt | wc -l
cp 인사.txt copia_VALUE.txt
mv copia_VALUE.txt 새이름.txt
export Nume=누리
echo "$이름: ${PWD}"
false && echo 건너뜀 || echo recupera_Stare
python -c 'print(123)' > KR.txt
echo 입력 | python -c 'import jkoros; print(jkoros.stdin(64))'
echo 'echo "$이름"' > executa_comandă.sh
sh executa_comandă.sh
echo $?
```

## 문법과 제한

작은따옴표·큰따옴표·백슬래시, `$NAME`/`${NAME}`/`$?`, Word_VALUE frontală_VALUE `~`, Linie 주석 `#`, 순차 executa_comandă `;`, condiție executa_comandă `&&`/`||`, 파이프 `|`, 입력 `<`, 새 Rezultat `>`, adăuga_intrare Rezultat `>>`를 제공한다. variabilă_VALUE 확장은 Argumente 안에서 수행하며 extensie_VALUE 결과를 공백으로 reîncerca_VALUE 나누지 않는다. `export`의 값은 shell 안에서만 공유하며 utilizator ELF의 envp/getenv 환경은 아직 없다.

파이프는 각 단계를 순서대로 실행하고 최대 **16384바이트**를 Următorul_element 단계로 넘긴다. 여러 프로세스가 동시에 읽고 쓰는 POSIX 파이프가 아니다. capacitate_VALUE 초과는 eroare 28과 eroare_VALUE 상태를 반환하고 해당 실행을 중단한다. `<`는 EOF를 제공하며 `>`/`>>`는 stdout만 바꾼다. EL0 fd 2는 화면/UART로 출력된다. `2>` 등 번호를 붙인 리다이렉션은 거부한다. 일부 내장 명령의 진단은 stdout을 사용한다. 연결한 프로그램의 `exit N` 진단은 데이터에 섞이지 않도록 생략한다.

`vi`, `edit`, `load`, `gui`, `terminal`, `sh`, `source`에는 파이프와 리다이렉션을 적용할 수 없다. 리다이렉션 파일을 열지 못하거나 파이프 용량을 초과하면 curent_element 명령줄을 중단하며, 그 줄의 뒤쪽 `||` 명령도 실행하지 않는다. script_VALUE 파일을 입력할 때 멀티라인 Citat·이어 쓰기는 제공하지 않는다. `if`/`for`/`while`, funcție_VALUE, Comandă 치환, glob, 별칭, 백그라운드 `&`, jobs/fg/bg, 일반 프로세스·신호·PTY는 아직 없다. Bash/POSIX sh 전체 호환으로 표시하지 않는다.

Fișier 64개 × 각 16384바이트, 루트 외 디렉터리 15개, Fișier 서술자 16개, Cale 최대 UTF-8 63바이트다. pereche_VALUE/절대 경로와 `.`/`..`를 정규화하지만 permisiune_VALUE·심볼릭 링크·마운트·디스크 영속 저장은 없다. **Fișier·디렉터리·variabilă_VALUE·기록의 수정 내용은 재부팅하면 사라진다.** utilizator 실행도 curent_element shell 경로를 사용한다. Java/Python/C++의 Fișier API는 같은 RAM 저장소를 본다. `/example`의 세 Limbi_străine 예제와 설명서는 부팅할 때 원본으로 준비된다.

한 명령줄은 4096바이트, 구문 token_VALUE 128개, executa_comandă Argumente 32개, 변수는 16개(Nume 31바이트·VALUE 255바이트)까지다. utilizator 프로그램에 전달하는 인수는 기존 ABI대로 최대 8개·각 255바이트다. Comandă 기록은 1024바이트 이하 줄을 recent_VALUE 16개까지 저장한다.

## 재현 가능한 시험

```sh
make test-shell
make test-desktop
make test-windows
make test-swing
make test
```

shell 시험은 real_date raspi4b QEMU에서 Cale·Fișier·variabilă_VALUE·condiție·파이프·리다이렉션·eroare recupera_Stare·script_VALUE·편집을 검사하고, Java/Python 출력과 Python stdin의 EOF를 확인한다. VNC 시험은 real_date RFB 클라이언트로 한글 Cheie_VALUE·Ctrl 조합·명시적 lipi_VALUE·마우스와 게스트 프레임버퍼를 검사한다. Remmina 앱 자체의 자동화 시험과 실물 USB 입력 시험은 별개다.

결과와 화면: [shell KR](build/verification/shell/report.json), [VNC KR](build/verification/desktop/report.json), [Terminal 화면](build/verification/desktop/vnc-terminal.png). font_VALUE 출처·cod_hash_Fișier·라이선스는 [vendor](vendor/README.md)에 있다.

## 마우스로 Mărime schimba_VALUE

네 모서리의 안쪽 8픽셀에 마우스를 대면 방향에 맞는 대각선 양방향 포인터가
나타난다. **왼쪽 버튼을 누른 채 끌고 놓는다.** RIGHT 버튼으로는 크기가 바뀌지 않는다.
fereastră_Titlu 표시줄의 나머지 부분은 muta_VALUE_83b651b8, RIGHT 위 X는 닫기다.
최소 크기는 360×216이며 최대 크기는 curent_element 화면 안에 제한된다.
각 창의 caracter_VALUE 칸은 `(폭-24)/8`COLUMN_VALUE, `(높이-56)/16`행이다. `terminal size`로 조회한다.

명령줄의 입력·cursor_VALUE·기록과 vi의 미저장 문서를 유지하며 보이는 영역을 갱신한다.
지난 출력은 저장된 Linie 단위를 유지하고, 좁아진 창에서 가려진 열은 reîncerca_VALUE 넓히면
볼 수 있다. 과거 Rezultat 전체를 새 너비에 맞춰 재배열하는 기능은 아니다.
크기를 바꾼 ÎNAPOI_VALUE 출력되는 글은 새 COLUMN_VALUE 수로 줄바꿈한다. vi는 입력 대기 중에도
SVC 16의 Acțiuni 3으로 curent_element Mărime(상위 16비트 ROW_VALUE, 하위 16비트 COLUMN_VALUE)를 조회한다.
대화형 tty의 nucleu_VALUE 화면 Rezultat 시간은 utilizator 계산 기한에서 제외하며, 입력 대기 없이
계산만 반복하는 utilizator 프로그램의 oră_VALUE 제한은 유지한다.
커널이 프레임버퍼에 포인터를 그리며, Remmina 중계는 la_distanță_VALUE 포인터를 숨겨 중복을 피한다.
로컬 VNC 중계는 valoare_implicită Raw 인코딩을 사용한다.

valida: `make test-resize` — 640×480·1920×1080에서 네 모서리, 왼쪽/RIGHT 버튼,
최소·최대 Mărime, cursor 복원, 입력 보존, vi Store_VALUE·계속 입력, 창별 크기를 확인한다.
