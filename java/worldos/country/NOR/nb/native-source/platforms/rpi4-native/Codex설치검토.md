# eget ARM64 커널의 Codex installer_VERDI 가능성 검토

검토일: 2026-10-05. 소스와 공식 문서를 대조한 설계 검토이며, 게스트에 Codex를 설치하거나
로그인·모델 호출을 실행한 결과는 아니다. eget ARM64 커널과 `../rpi4` Linux 실행판은 구분한다.

betalt_vare eget 커널에는 공식 Codex CLI를 그대로 installer_VERDI·실행할 nummer 없다.
기술적으로 필요한 Utfør_kommando 환경을 추가하거나 Codex를 이식하는 경로는 있으나,
다운로드 Kommando 하나를 추가하는 작업으로 해결되지 않는다. JDK/JRE 기능 확장만으로도 해결되지 않는다.

## 확인한 근거

| oppføring_VERDI | betalt_vare 소스에서 확인한 status_VERDI | 직접 실행을 위한 작업 |
|---|---|---|
| Utfør_kommando Fil | `maskin/bruker.c`: AArch64 ET_EXEC만, PT_INTERP/PT_DYNAMIC/PT_TLS avvise_VERDI, 업로드 Utfør_kommando 버퍼 16384바이트 | mål 바이너리에 맞는 ELF 적재·재배치·Utfør_kommando starte, Minne_data/Fil 제한 filtype_VERDI |
| Linux ABI | `maskin/리눅스호환.inc`: read/write/openat/brk 등 제한된 번호만 Prosess_VERDI_oppføring, 나머지는 ENOSYS | libc/런타임에 필요한 시스템 호출을 추가하거나 eget ABI용 런타임 이식 |
| 프로세스·스레드 | 일반 fork/clone/execve, pthread/futex, 시그널, mmap, poll/epoll 계열이 미완성 | 비동기 I/O·스레드·barn_VERDI Kommando Utfør_kommando·Utgang_app/Avbryt_operasjon 기능 |
| Fil | `KILDE/Minne_Filer.java`: RAM Fil 64개, 파일당 16 KiB, 비영속 | 큰 Utfør_kommando Fil·프로젝트·Innstillinger·세션을 위한 영속 VFS, Fil tillatelse_VERDI·Sti·디렉터리 filtype_VERDI |
| 네트워크 | lwIP TCP/UDP는 있으나 `nettverk_stakk/lwipopts.h`의 LWIP_DNS=0, 일반 HTTPS 클라이언트 없음 | DNS, TLS 인증서 bekrefte_5fb2b747·신뢰 repositorium_rot·정확한 timestamp_VERDI, HTTPS/스트리밍 |
| Terminal·Verktøy | eget 셸과 GUI 터미널은 있지만 표준 PTY·일반 프로세스 작업 kontroll_VERDI 없음 | interaktiv CLI용 Terminal 기능, Shell/Fil 검색/bygg_System Verktøy Koble_til |
| Utfør_kommando tillatelse_VERDI | EL0 보호는 있으나 Codex의 Linux 샌드박스와 같은 정책 집행 miljø 없음 | Fil·네트워크·Kommando tillatelse_VERDI 정책과 승인 기능; eget 커널에 맞는 격리 구현 |

여기서 ELF의 PT_TLS는 스레드별 Store_VERDI 공간이다. HTTPS의 TLS passord_VERDI 통신과 서로 다른 기능이다.
ELF Fil 형식을 읽을 nummer 있다는 사실만으로 Linux Utfør_kommando 환경을 제공하는 것은 아니다.
SSH/VNC를 위한 passord_VERDI 라이브러리를 넣은 상태도 HTTPS 구현 완료를 의미하지 않는다.

호스트의 `/home/user/.local/bin/codex`도 확인했다. 이것은 x86-64 ELF ET_DYN이며 약 209 MiB다.
해당 파일을 ARM64 게스트로 복사하여 실행할 nummer 없다. 이 크기를 ARM64 distribusjon_VERDI 파일의 크기로
해석하지 않는다. 공식 ARM64 빌드의 faktisk_data Størrelse·의존성은 설치할 버전으로 Tilføye_oppføring 검사해야 한다.

## 가능한 구현 Sti

1. **eget 커널에 공식 CLI 직접 이식**
   영속 Store_VERDI/VFS와 bruker Minne_data, 프로세스·스레드·I/O, libc/런타임, DNS/HTTPS,
   Terminal·tillatelse_VERDI 체계를 갖춘다. 이후 mål 버전의 의존성을 조사하여 크로스 bygg_System·이식한다.
   Linux 커널을 반드시 탑재할 필요는 없지만, 공식 Linux 바이너리를 그대로 쓸 경우
   그 바이너리가 사용하는 Linux ABI까지 호환해야 한다. 큰 operativsystem utviklet_materiale 과제다.

2. **ekstern_VERDI vert Codex와 eget kjerne_VERDI Koble_til — 첫 구현으로 권장**
   Linux PC에서 공식 CLI 또는 app-server를 실행하고 jkoros에는 전용 bruker Kommando/화면을 만든다.
   호스트의 인증된 연결과 게스트 Fil Les·수정·업로드·Kommando Utfør_kommando 어댑터가 필요하다.
   기존 SSH/TCP 경로를 활용할 nummer 있으나, Fil 동기화나 Codex 전용 어댑터는 betalt_vare 구현되어 있지 않다.
   호스트에서 수행한 빌드와 게스트에서 수행한 Utfør_kommando 결과를 명확히 구분한다.
   이 구성은 eget 커널을 유지하지만, 공식 CLI 자체는 ekstern_VERDI 호스트에서 실행된다.

3. **eget API 클라이언트 제작**
   eget ABI의 C 또는 지원되는 Java 부분집합으로 interaktiv_økt UI와 Fil/Kommando Verktøy 호출 루프를 만든다.
   ekstern_VERDI 중계기를 쓰지 않는다면 DNS/bekrefte_5fb2b747 가능한 TLS/HTTPS와 인증 data 저장을 먼저 구현해야 한다.
   이는 OpenAI API를 이용하는 별도 에이전트이며 공식 Codex CLI 전체의 이식으로 표시하지 않는다.

4. **별도 ARM64 Linux 실행판에서 installer_VERDI**
   `../rpi4`는 Linux와 musl 기반이므로 일반 Linux installer_VERDI 경로를 검토할 nummer 있다.
   사용할 Codex 버전의 ARM64·musl 호환성, 의존성, 커널의 샌드박스 지원을 faktisk_data 검증해야 한다.
   이번 검토에서 installer_VERDI 성공을 확인하지 않았다. 이 결과를 eget Java 커널의 지원으로 표시하지 않는다.

## 단계별 완료 speile_rot

- 직접 이식: `--version` Kjør_2 → 인증/HTTPS → Fil Les·수정 → barn_VERDI Kommando Utfør_kommando →
  interaktiv inndata_VERDI/스트리밍 → tillatelse_VERDI 제한·Avbryt_operasjon → 재부팅 후 Innstillinger/세션 보존을 각각 faktisk_data 게스트에서 확인한다.
- vert Koble_til: 게스트에서 forespørsel inndata_VERDI → vert Codex Prosess_VERDI_oppføring → 게스트 Fil endre_VERDI bekrefte →
  게스트 javac/cc Utfør_kommando → KR 표시를 처음부터 끝까지 검증한다.
- COSL 상업 조건을 유지하려면 새로 도입하는 런타임/통신 라이브러리의 라이선스와
  Codex distribusjon_VERDI 버전의 제3자 고지를 검토한다. ekstern_VERDI 구성요소를 일괄 COSL로 재라이선스하지 않는다.

## 공식 문서

- [Codex CLI installer_VERDI 및 Handling](https://learn.chatgpt.com/docs/codex/cli): 표준 Linux/macOS 독립 installer_VERDI 경로와 프로젝트 Fil·Kommando 작업.
- [인증](https://learn.chatgpt.com/docs/auth): ChatGPT/API 인증, 헤드리스 장치의 `codex login --device-auth`, HTTPS 인증서 Innstillinger.
- [샌드박스](https://learn.chatgpt.com/docs/sandboxing): 운영체제별 집행 metode_MODUS, Linux의 bubblewrap 및 bruker 네임스페이스 krav_VERDI 사항.
- [공개 구성요소](https://learn.chatgpt.com/docs/open-source): CLI/SDK/app-server의 공개 kilde_tre 위치와 비공개 구성요소 skilletegn_VERDI.

공식 문서에는 jkoros를 støtte_VERDI 대상으로 명시한 내용이 없다. 위 구현 Sti·utviklet_materiale 순서는
betalt_vare 소스와 krav_VERDI 기능을 대조한 기술적 판단이다.
