# nativo ARM64 커널의 Codex instalar_VALOR 가능성 검토

검토일: 2026-10-05. 소스와 공식 문서를 대조한 설계 검토이며, 게스트에 Codex를 설치하거나
로그인·모델 호출을 실행한 결과는 아니다. nativo ARM64 커널과 `../rpi4` Linux 실행판은 구분한다.

em_dia_item nativo 커널에는 공식 Codex CLI를 그대로 instalar_VALOR·실행할 número 없다.
기술적으로 필요한 Executar_comando 환경을 추가하거나 Codex를 이식하는 경로는 있으나,
다운로드 comando 하나를 추가하는 작업으로 해결되지 않는다. JDK/JRE 기능 확장만으로도 해결되지 않는다.

## 확인한 근거

| entrada_VALOR_962f286b | em_dia_item 소스에서 확인한 Estado_VALOR | 직접 실행을 위한 작업 |
|---|---|---|
| Executar_comando ficheiro | `computador/espaço_do_utilizador.c`: AArch64 ET_EXEC만, PT_INTERP/PT_DYNAMIC/PT_TLS rejeitar_VALOR, 업로드 Executar_comando 버퍼 16384바이트 | meta 바이너리에 맞는 ELF 적재·재배치·Executar_comando inicializar, Memória_dados/ficheiro 제한 extensão_VALOR |
| Linux ABI | `computador/리눅스호환.inc`: read/write/openat/brk 등 제한된 번호만 Processo_VALOR_entrada, 나머지는 ENOSYS | libc/런타임에 필요한 시스템 호출을 추가하거나 nativo ABI용 런타임 이식 |
| 프로세스·스레드 | 일반 fork/clone/execve, pthread/futex, 시그널, mmap, poll/epoll 계열이 미완성 | 비동기 I/O·스레드·filho_VALOR comando Executar_comando·sair_app/Close_cirurgia 기능 |
| ficheiro | `códigoFonte/FicheirosMemória.java`: RAM ficheiro 64개, 파일당 16 KiB, 비영속 | 큰 Executar_comando ficheiro·프로젝트·Definições·세션을 위한 영속 VFS, ficheiro Permissão_VALOR·caminho·디렉터리 extensão_VALOR |
| 네트워크 | lwIP TCP/UDP는 있으나 `rede_pilha/lwipopts.h`의 LWIP_DNS=0, 일반 HTTPS 클라이언트 없음 | DNS, TLS 인증서 validar·신뢰 repositório_raiz·정확한 carimbo_de_data_hora_VALOR, HTTPS/스트리밍 |
| terminal·ferramentas | nativo 셸과 GUI 터미널은 있지만 표준 PTY·일반 프로세스 작업 visual_VALOR 없음 | interativo CLI용 terminal 기능, shell/ficheiro 검색/construir ferramentas Ligar |
| Executar_comando Permissão_VALOR | EL0 보호는 있으나 Codex의 Linux 샌드박스와 같은 정책 집행 ambiente 없음 | ficheiro·네트워크·comando Permissão_VALOR 정책과 승인 기능; nativo 커널에 맞는 격리 implementação |

여기서 ELF의 PT_TLS는 스레드별 Store_VALOR 공간이다. HTTPS의 TLS senha_VALOR 통신과 서로 다른 기능이다.
ELF ficheiro 형식을 읽을 número 있다는 사실만으로 Linux Executar_comando 환경을 제공하는 것은 아니다.
SSH/VNC를 위한 senha_VALOR 라이브러리를 넣은 상태도 HTTPS implementação 완료를 의미하지 않는다.

호스트의 `/home/user/.local/bin/codex`도 확인했다. 이것은 x86-64 ELF ET_DYN이며 약 209 MiB다.
해당 파일을 ARM64 게스트로 복사하여 실행할 número 없다. 이 크기를 ARM64 distribuição_VALOR 파일의 크기로
해석하지 않는다. 공식 ARM64 빌드의 real_dados Tamanho·의존성은 설치할 버전으로 Acrescentar_entrada 검사해야 한다.

## 가능한 implementação caminho

1. **nativo 커널에 공식 CLI 직접 이식**
   영속 Store_VALOR/VFS와 espaço_do_utilizador Memória_dados, 프로세스·스레드·I/O, libc/런타임, DNS/HTTPS,
   terminal·Permissão_VALOR 체계를 갖춘다. 이후 meta 버전의 의존성을 조사하여 크로스 construir·이식한다.
   Linux 커널을 반드시 탑재할 필요는 없지만, 공식 Linux 바이너리를 그대로 쓸 경우
   그 바이너리가 사용하는 Linux ABI까지 호환해야 한다. 큰 SO 개발 과제다.

2. **externo_VALOR host Codex와 nativo kernel_VALOR Ligar — 첫 구현으로 권장**
   Linux PC에서 공식 CLI 또는 app-server를 실행하고 jkoros에는 전용 espaço_do_utilizador comando/화면을 만든다.
   호스트의 인증된 연결과 게스트 ficheiro Leitura·수정·업로드·comando Executar_comando 어댑터가 필요하다.
   기존 SSH/TCP 경로를 활용할 número 있으나, ficheiro 동기화나 Codex 전용 어댑터는 em_dia_item 구현되어 있지 않다.
   호스트에서 수행한 빌드와 게스트에서 수행한 Executar_comando 결과를 명확히 구분한다.
   이 구성은 nativo 커널을 유지하지만, 공식 CLI 자체는 externo_VALOR 호스트에서 실행된다.

3. **nativo API 클라이언트 제작**
   nativo ABI의 C 또는 지원되는 Java 부분집합으로 interativo_sessão UI와 ficheiro/comando ferramentas 호출 루프를 만든다.
   externo_VALOR 중계기를 쓰지 않는다면 DNS/validar 가능한 TLS/HTTPS와 인증 dados 저장을 먼저 구현해야 한다.
   이는 OpenAI API를 이용하는 별도 에이전트이며 공식 Codex CLI 전체의 이식으로 표시하지 않는다.

4. **별도 ARM64 Linux 실행판에서 instalar_VALOR**
   `../rpi4`는 Linux와 musl 기반이므로 일반 Linux instalar_VALOR 경로를 검토할 número 있다.
   사용할 Codex 버전의 ARM64·musl 호환성, 의존성, 커널의 샌드박스 지원을 real_dados 검증해야 한다.
   이번 검토에서 instalar_VALOR 성공을 확인하지 않았다. 이 결과를 nativo Java 커널의 지원으로 표시하지 않는다.

## 단계별 완료 ação_raiz

- 직접 이식: `--version` iniciar → 인증/HTTPS → ficheiro Leitura·수정 → filho_VALOR comando Executar_comando →
  interativo entrada_VALOR/스트리밍 → Permissão_VALOR 제한·Close_cirurgia → 재부팅 후 Definições/세션 보존을 각각 real_dados 게스트에서 확인한다.
- host Ligar: 게스트에서 solicitação entrada_VALOR → host Codex Processo_VALOR_entrada → 게스트 ficheiro alterar_VALOR verificar →
  게스트 javac/cc Executar_comando → resultado 표시를 처음부터 끝까지 검증한다.
- COSL 상업 조건을 유지하려면 새로 도입하는 런타임/comunicação 라이브러리의 라이선스와
  Codex distribuição_VALOR 버전의 제3자 고지를 검토한다. externo_VALOR 구성요소를 일괄 COSL로 재라이선스하지 않는다.

## 공식 문서

- [Codex CLI instalar_VALOR 및 Acção](https://learn.chatgpt.com/docs/codex/cli): 표준 Linux/macOS 독립 instalar_VALOR 경로와 프로젝트 ficheiro·comando 작업.
- [인증](https://learn.chatgpt.com/docs/auth): ChatGPT/API 인증, 헤드리스 장치의 `codex login --device-auth`, HTTPS 인증서 Definições.
- [샌드박스](https://learn.chatgpt.com/docs/sandboxing): 운영체제별 집행 método_MODO, Linux의 bubblewrap 및 espaço_do_utilizador 네임스페이스 requisito_VALOR 사항.
- [공개 구성요소](https://learn.chatgpt.com/docs/open-source): CLI/SDK/app-server의 공개 fonte_árvore 위치와 비공개 구성요소 delimitador_VALOR.

공식 문서에는 jkoros를 Suporte_VALOR 대상으로 명시한 내용이 없다. 위 implementação caminho·개발 순서는
em_dia_item 소스와 requisito_VALOR 기능을 대조한 기술적 판단이다.
