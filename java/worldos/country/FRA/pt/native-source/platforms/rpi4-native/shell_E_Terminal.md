# nativo 커널의 GUI 터미널과 shell

이 터미널은 nativo Java 커널의 셸을 프레임버퍼 창과 UART에서 사용한다. comando Processo_VALOR_entrada·RAM ficheiro·파이프는 Java kernel_VALOR, 화면의 caractere_VALOR 그리기는 freestanding C에서 수행한다. Linux·X11·Bash 없이 동작하며, nativo JVM의 Swing Suporte_VALOR 부분집합도 같은 Janela 시스템을 이용한다. 자세한 vi·다중 Janela·코딩 사용법은 [개발 매뉴얼](개발안내.md)을 참고한다.

## em_dia_item 컴퓨터에서 Executar_comando

```sh
cd /home/user/jkoros/platforms/rpi4-native
make desktop
```

Remmina에서 **VNC**, Endereço **127.0.0.1:5902**로 연결한다. terminal 창은 자동으로 열린다. 연결한 VNC 창에 키를 입력하면 nativo 커널의 셸로 전달된다. 종료하려면 `make desktop`을 실행한 host 터미널에서 Ctrl+C를 누른다. 포트를 바꾸려면 construir 후 `python3 ferramentas/Executar_comando.py --desktop --port 5903`을 사용한다. 서버는 localhost에만 바인드하며 동시에 한 클라이언트가 제어한다.

일반 UART 셸은 `make run`으로 시작한다. QEMU 종료는 Ctrl+A Avançar_item X이다. 같은 VM의 UART에서 `terminal` 또는 F12로 GUI 터미널을 COL_VALOR número 있다. `gui` Executar_comando 화면에서는 다섯 번째 **OPEN TERMINAL** 버튼, dígito_VALOR 5 또는 T로 연다. `--vnc 127.0.0.1:2`만 사용한 기존 Executar_comando 방식은 tela 보기용이며, VNC 키보드를 연결하려면 `--desktop`을 사용한다.

FTP와 externo_VALOR 네트워크도 함께 쓰려면 `python3 ferramentas/Executar_comando.py --desktop --network`로
실행한다. Remmina VNC는 `127.0.0.1:5902`, 게스트에서 `ftpd start` 후 FTP는
`127.0.0.1:2121`이다. `--port`, `--ftp-port`, `--forward`를 함께 지정할 número 있다.
한 VM의 보조 UART로 SLIP를 전송하고 주 UART로 GUI 입력을 전달한다.

QEMU Executar_comando 도구가 VNC 키보드/마우스를 UART 입력으로 변환한다. real_dados Pi4의 USB 키보드·마우스 드라이버를 구현한 것은 아니다. real_dados 보드에서는 em_dia_item UART 입력이 필요하며 실물 부팅은 아직 미검증이다.

## 창과 entrada_VALOR

- 640×480~1920×1080 화면에서 최대 네 개 terminal Janela, valor_padrão 568×360(68열 × 19행)과 recente_VALOR 160행 보관, valor_padrão ANSI 색상·cursor_VALOR·apagar_entrada Processo_VALOR_entrada.
- 상단 **+ New terminal** 또는 Ctrl+Shift+T로 새 창을 연다. 제목줄을 끌어 이동하고 Janela/상단 버튼을 클릭하거나 F6으로 전환한다. 각 창의 작업 caminho·variável_VALOR·comando LOG_linha·entrada_VALOR 중인 줄은 독립적이다.
- UTF-8 한글·CJK·라틴 문자와 일부 이모지 비트맵 fonte_VALOR. 복잡한 문자 조판·결합 문자·양방향 disposição_de_ligação·모든 Unicode 글리프를 보장하지 않는다.
- 좌우 방향키/Home/End/Delete/Backspace로 명령을 편집하고 위아래 방향키로 recente_VALOR 16개 명령을 찾는다. 긴 명령은 entrada_VALOR 줄을 가로로 이동해 보여 주며 `<`, `>`가 숨겨진 부분을 나타낸다.
- Tab은 comando Nome 또는 em_dia_item 디렉터리의 파일명에서 후보가 하나일 때 완성한다. 디렉터리를 포함한 caminho 접두사·Citação 안의 완성은 아직 없다.
- Ctrl+A/E: 처음/끝, Ctrl+U/K: cursor_VALOR câmera_frontal_VALOR/BACK_VALOR 삭제, Ctrl+C: entrada_VALOR Close_cirurgia. Executar_comando 중인 임의 프로그램에 SIGINT를 보내는 기능은 없다. vi와 Swing의 entrada_VALOR 대기는 Executar_comando 기한을 갱신하지만 일반 계산의 약 2초 제한은 유지한다.
- PgUp/PgDn 또는 마우스 휠: Anterior_item saídaTexto. 새 출력이 오면 최신 위치로 돌아온다.
- F12/barra_de_título DIREITA 버튼/`exit`: Janela Fechar. 빈 입력에서 Ctrl+D도 창을 닫는다. VM을 종료하는 명령은 아니다.

`--desktop`의 VNC entrada_VALOR 연결에 **두벌식 한글 composição_VALOR**을 제공한다. 접속한 PC의
입력기를 영어로 두고 **F9**, **Shift+Space**, **한/zero_operando Chave_VALOR** 중 하나를 누르면
Janela 제목이 `[EN]`에서 `[KO]`로 바뀐다. `gksrmf` → `한글`,
`dkssudgktpdy` → `안녕하세요`. 같은 키로 영어로 돌아간다.
겹받침·복합 모음과 composição_VALOR 단계별 Backspace를 지원한다. cursor_VALOR mover_VALOR·마우스 clicar_VALOR·
단축키·colar_VALOR·Enter 때 조합을 확정한다. PC가 Shift+Space나 한/zero_operando 키를
nativo 처리하면 **F9**를 사용한다. Alt 단독은 mudar_MODO 키가 아니다.

이 조합기는 QEMU의 VNC→UART entrada_VALOR 연결에서 실행된다. 일반 직렬 접속과
실물 Pi의 USB 키보드 입력기에 추가된 기능은 아니다. 이미 완성된 Unicode
한글 키도 그대로 전달한다. 클립보드 공유가 활성화되어 표준 VNC ClientCutText가
도착하면 Ctrl+Shift+V로 붙여 넣는다. 클립보드 동기화만으로 명령을 실행하지 않는다.
줄바꿈을 포함해 명시적으로 붙여 넣으면 해당 줄이 실행된다.

게스트에서 `help` 또는 `help ko`를 입력하면 한글 entrada_VALOR 안내를 볼 número 있다.
`help`와 `help ko`에는 한/zero_operando Chave_VALOR·Shift+Space·F9 및 `[EN]`/`[KO]` 안내를 표시한다.
긴 도움말은 PgUp/PgDn으로 스크롤한다.

터미널에서 Java·Python·C++ Executar_comando 결과를 바로 볼 número 있다. 프로그램이 직접 프레임버퍼에 그림을 그린 경우 sair_app 후 terminal 창을 복원한다. vi/Swing aguarde_VALOR 중 다른 창으로 전환하면 해당 EL0 프로그램의 Memória_dados·레지스터를 보관하고 돌아올 때 재개한다. seleção_VALOR copiar_VALOR·PTY·전체 VT100/xterm 호환과 임의 프로그램의 동시 병렬 실행은 제공하지 않는다. X로 닫으면 해당 창의 프로그램도 종료되므로 vi에서 저장하지 않은 내용은 사라진다.

## comando

| comando | recortar |
|---|---|
| `help`, `info` | 사용법과 implementação Estado_VALOR |
| `pwd`, `cd [DIR]`, `ls [-l] [PATH]` | em_dia_item caminho·디렉터리/ficheiro entrada_Lista_f07b3200; argumentos 없는 cd는 `/` |
| `mkdir DIR`, `rmdir DIR` | 디렉터리 한 개 Criar_entrada/빈 디렉터리 삭제; `-p` 없음 |
| `touch FILE`, `rm FILE...` | ficheiro Criar_entrada/삭제; carimbo_de_data_hora_VALOR msinfo32_exe 없음 |
| `cp SOURCE DEST`, `mv SOURCE DEST` | ficheiro copiar_VALOR/Nome alterar_VALOR; 대상은 정확한 ficheiro caminho, 재귀/디렉터리 mover_VALOR 없음 |
| `cat [FILE...]` | ficheiro 또는 표준 입력을 byte_VALOR 그대로 saídaTexto |
| `echo [-n] [ARGS...]` | argumentos saídaTexto; `-e` 이스케이프 extensão_VALOR 없음 |
| `wc [-c\|-l\|-w] [FILE]` | byte_VALOR/linha_de_entrada/Word_VALOR número; Word_VALOR 구분은 ASCII 공백 |
| `grep TEXT [FILE]` | 정규식 없이 문자열이 포함된 linha_de_entrada saídaTexto; 일치 없으면 Estado_VALOR 1 |
| `head [-n N] [FILE]`, `tail [-n N] [FILE]` | câmera_frontal_VALOR/BACK_VALOR N줄, valor_padrão 10줄 |
| `tee [-a] FILE` | 표준 입력을 파일과 표준 출력에 LOG_linha |
| `export NAME=VALUE`, `unset NAME`, `env` | shell variável_VALOR Definições·삭제·entrada_Lista_f07b3200; HOME/PWD는 Leitura 전용 |
| `sh FILE`, `source FILE` | comando 파일을 같은 shell 환경에서 줄별 Executar_comando; 최대 aninhamento_VALOR 3 |
| `true`, `false`, `exit [N]` | Estado_VALOR 0/1; script_VALOR 안의 exit는 em_dia_item script_VALOR sair_app |
| `history`, `clear` | comando LOG_linha·tela apagar_entrada |
| `vi FILE` | EL0 vi método_MODO Editor: entrada_VALOR/comando MODO_VALOR, UTF-8 mover_VALOR, 검색, 삭제·copiar_VALOR·colar_SMS·되돌리기, `:w`/`:q`/`:wq` |
| `edit FILE`, `load FILE`, `hex FILE` | 전체 Conteúdo_VALOR 교체 Editar_VALOR, 16진수 업로드/consulta_VALOR; 단독 `.` 줄로 Store_VALOR |
| `javac`, `java`, `python`, `run` | 기존 nativo Java ferramentas·MicroPython·EL0 C++/ELF Executar_comando |

`net test`, `tasks`, `selftest`, `samples`도 유지한다. app_f5044b9b Executar_comando 범위는 [README](LEIAME_eb81d7d9.md)와 [Java Executar_comando ambiente](자바실행환경.md)을 참고한다.

```sh
mkdir 작업
cd 작업
echo "안녕하세요" > saudação_ae353e94.txt
echo "반갑습니다" >> saudação_ae353e94.txt
cat < saudação_ae353e94.txt | grep 안녕 | tee 추림.txt | wc -l
cp saudação_ae353e94.txt copiar_VALOR.txt
mv copiar_VALOR.txt 새이름.txt
export Nome=누리
echo "$이름: ${PWD}"
false && echo 건너뜀 || echo recuperar_Estado
python -c 'print(123)' > resultado.txt
echo entrada_VALOR | python -c 'import jkoros; print(jkoros.stdin(64))'
echo 'echo "$이름"' > Executar_comando.sh
sh Executar_comando.sh
echo $?
```

## 문법과 제한

작은따옴표·큰따옴표·백슬래시, `$NAME`/`${NAME}`/`$?`, Word_VALOR câmera_frontal_VALOR `~`, linha_de_entrada 주석 `#`, 순차 Executar_comando `;`, doença Executar_comando `&&`/`||`, 파이프 `|`, entrada_VALOR `<`, 새 saídaTexto `>`, Acrescentar_entrada saídaTexto `>>`를 제공한다. variável_VALOR 확장은 argumentos 안에서 수행하며 extensão_VALOR 결과를 공백으로 repetir_VALOR 나누지 않는다. `export`의 값은 shell 안에서만 공유하며 espaço_do_utilizador ELF의 envp/getenv 환경은 아직 없다.

파이프는 각 단계를 순서대로 실행하고 최대 **16384바이트**를 Avançar_item 단계로 넘긴다. 여러 프로세스가 동시에 읽고 쓰는 POSIX 파이프가 아니다. capacidade_VALOR 초과는 erro 28과 falha_VALOR 상태를 반환하고 해당 실행을 중단한다. `<`는 EOF를 제공하며 `>`/`>>`는 stdout만 바꾼다. EL0 fd 2는 tela/UART로 출력된다. `2>` 등 번호를 붙인 리다이렉션은 거부한다. 일부 내장 명령의 진단은 stdout을 사용한다. 연결한 프로그램의 `exit N` 진단은 데이터에 섞이지 않도록 생략한다.

`vi`, `edit`, `load`, `gui`, `terminal`, `sh`, `source`에는 파이프와 리다이렉션을 적용할 número 없다. 리다이렉션 파일을 열지 못하거나 파이프 용량을 초과하면 em_dia_item 명령줄을 중단하며, 그 줄의 뒤쪽 `||` 명령도 실행하지 않는다. script_VALOR 파일을 입력할 때 멀티라인 Citação·이어 쓰기는 제공하지 않는다. `if`/`for`/`while`, FUNÇÃO_VALOR, comando 치환, glob, alternativo_nome, 백그라운드 `&`, jobs/fg/bg, 일반 프로세스·신호·PTY는 아직 없다. Bash/POSIX sh 전체 호환으로 표시하지 않는다.

ficheiro 64개 × 각 16384바이트, 루트 외 디렉터리 15개, ficheiro descritor_entrada 16개, caminho 최대 UTF-8 63바이트다. par_VALOR/절대 경로와 `.`/`..`를 정규화하지만 Permissão_VALOR·심볼릭 링크·마운트·디스크 영속 저장은 없다. **ficheiro·디렉터리·variável_VALOR·기록의 수정 내용은 재부팅하면 사라진다.** espaço_do_utilizador 실행도 em_dia_item shell 경로를 사용한다. Java/Python/C++의 ficheiro API는 같은 RAM 저장소를 본다. `/example`의 세 Idioma 예제와 설명서는 부팅할 때 원본으로 준비된다.

한 명령줄은 4096바이트, 구문 token_VALOR 128개, Executar_comando argumentos 32개, 변수는 16개(Nome 31바이트·VALOR 255바이트)까지다. espaço_do_utilizador 프로그램에 전달하는 인수는 기존 ABI대로 최대 8개·각 255바이트다. comando 기록은 1024바이트 이하 줄을 recente_VALOR 16개까지 저장한다.

## 재현 가능한 testes

```sh
make test-shell
make test-desktop
make test-windows
make test-swing
make test
```

shell 시험은 real_dados raspi4b QEMU에서 caminho·ficheiro·variável_VALOR·doença·파이프·리다이렉션·erro recuperar_Estado·script_VALOR·편집을 검사하고, Java/Python 출력과 Python stdin의 EOF를 확인한다. VNC 시험은 real_dados RFB 클라이언트로 한글 Chave_VALOR·Ctrl composição_VALOR·명시적 colar_VALOR·마우스와 게스트 프레임버퍼를 검사한다. Remmina 앱 자체의 자동화 시험과 실물 USB entrada_VALOR 시험은 별개다.

결과와 tela: [shell resultado](build/verification/shell/report.json), [VNC resultado](build/verification/desktop/report.json), [terminal tela](build/verification/desktop/vnc-terminal.png). fonte_VALOR origem_VALOR·hash_Arquivo·라이선스는 [vendor](vendor/README.md)에 있다.

## 마우스로 Tamanho alterar_VALOR

네 모서리의 안쪽 8픽셀에 마우스를 대면 방향에 맞는 대각선 양방향 포인터가
나타난다. **왼쪽 버튼을 누른 채 끌고 놓는다.** DIREITA 버튼으로는 크기가 바뀌지 않는다.
janela_Título 표시줄의 나머지 부분은 mover_VALOR, DIREITA 위 X는 닫기다.
최소 크기는 360×216이며 최대 크기는 em_dia_item tela 안에 제한된다.
각 창의 caractere_VALOR 칸은 `(폭-24)/8`COL_VALOR, `(altura_VALOR-56)/16`행이다. `terminal size`로 조회한다.

명령줄의 entrada_VALOR·cursor_VALOR·기록과 vi의 미저장 문서를 유지하며 보이는 영역을 갱신한다.
지난 출력은 저장된 linha_de_entrada 단위를 유지하고, 좁아진 창에서 가려진 열은 repetir_VALOR 넓히면
볼 número 있다. 과거 saídaTexto 전체를 새 너비에 맞춰 재배열하는 기능은 아니다.
크기를 바꾼 BACK_VALOR 출력되는 글은 새 COL_VALOR 수로 줄바꿈한다. vi는 entrada_VALOR aguarde_VALOR 중에도
SVC 16의 Acção 3으로 em_dia_item Tamanho(상위 16비트 LIN_VALOR, 하위 16비트 COL_VALOR)를 조회한다.
interativo tty의 kernel_VALOR tela saídaTexto 시간은 espaço_do_utilizador 계산 기한에서 제외하며, entrada_VALOR aguarde_VALOR 없이
계산만 반복하는 espaço_do_utilizador 프로그램의 valor_temporal 제한은 유지한다.
커널이 프레임버퍼에 포인터를 그리며, Remmina 중계는 remoto_VALOR 포인터를 숨겨 중복을 피한다.
로컬 VNC 중계는 valor_padrão Raw 인코딩을 사용한다.

validar: `make test-resize` — 640×480·1920×1080에서 네 모서리, 왼쪽/DIREITA 버튼,
최소·최대 Tamanho, ponteiro 복원, entrada_VALOR 보존, vi Store_VALOR·계속 entrada_VALOR, 창별 크기를 확인한다.
