# oma ARM64 커널의 Codex installima_VALUE 가능성 검토

검토일: 2026-10-05. 소스와 공식 문서를 대조한 설계 검토이며, 게스트에 Codex를 설치하거나
로그인·모델 호출을 실행한 결과는 아니다. oma ARM64 커널과 `../rpi4` Linux 실행판은 구분한다.

tähtaja_piires_kaup oma 커널에는 공식 Codex CLI를 그대로 installima_VALUE·실행할 number 없다.
기술적으로 필요한 Täida_käsk 환경을 추가하거나 Codex를 이식하는 경로는 있으나,
다운로드 Käsk 하나를 추가하는 작업으로 해결되지 않는다. JDK/JRE 기능 확장만으로도 해결되지 않는다.

## 확인한 근거

| kirje_VALUE | tähtaja_piires_kaup 소스에서 확인한 Olek_VALUE | 직접 실행을 위한 작업 |
|---|---|---|
| Täida_käsk Fail | `arvuti/kasutaja.c`: AArch64 ET_EXEC만, PT_INTERP/PT_DYNAMIC/PT_TLS keelduma_VALUE, 업로드 Täida_käsk 버퍼 16384바이트 | siht 바이너리에 맞는 ELF 적재·재배치·Täida_käsk 초기화, Mälu_andmed/Fail 제한 laiendus_VALUE |
| Linux ABI | `arvuti/리눅스호환.inc`: read/write/openat/brk 등 제한된 번호만 Joonis_VALUE_kirje, 나머지는 ENOSYS | libc/런타임에 필요한 시스템 호출을 추가하거나 oma ABI용 런타임 이식 |
| 프로세스·스레드 | 일반 fork/clone/execve, pthread/futex, 시그널, mmap, poll/epoll 계열이 미완성 | 비동기 I/O·스레드·laps_VALUE Käsk Täida_käsk·Välju_programm/Loobu_lõikus 기능 |
| Fail | `ALLIKAS/Mälu_Failid.java`: RAM Fail 64개, 파일당 16 KiB, 비영속 | 큰 Täida_käsk Fail·프로젝트·Seaded·세션을 위한 영속 VFS, Fail luba_VALUE·RADA·디렉터리 laiendus_VALUE |
| 네트워크 | lwIP TCP/UDP는 있으나 `võrk_Virn/lwipopts.h`의 LWIP_DNS=0, 일반 HTTPS 클라이언트 없음 | DNS, TLS 인증서 valideerima·신뢰 hoidla_juur·정확한 ajatempel_VALUE, HTTPS/스트리밍 |
| terminal·Tööriistad | oma 셸과 GUI 터미널은 있지만 표준 PTY·일반 프로세스 작업 meede_VALUE 없음 | 대화형 CLI용 terminal 기능, kest/Fail 검색/järk_süsteem Tööriistad Ühendu |
| Täida_käsk luba_VALUE | EL0 보호는 있으나 Codex의 Linux 샌드박스와 같은 정책 집행 환경 없음 | Fail·네트워크·Käsk luba_VALUE 정책과 승인 기능; oma 커널에 맞는 격리 구현 |

여기서 ELF의 PT_TLS는 스레드별 salv_VALUE 공간이다. HTTPS의 TLS parool_VALUE 통신과 서로 다른 기능이다.
ELF Fail 형식을 읽을 number 있다는 사실만으로 Linux Täida_käsk 환경을 제공하는 것은 아니다.
SSH/VNC를 위한 parool_VALUE 라이브러리를 넣은 상태도 HTTPS 구현 완료를 의미하지 않는다.

호스트의 `/home/user/.local/bin/codex`도 확인했다. 이것은 x86-64 ELF ET_DYN이며 약 209 MiB다.
해당 파일을 ARM64 게스트로 복사하여 실행할 number 없다. 이 크기를 ARM64 turustus_VALUE 파일의 크기로
해석하지 않는다. 공식 ARM64 빌드의 tegelik_andmed Suurus·의존성은 설치할 버전으로 Lisa_kirje 검사해야 한다.

## 가능한 구현 RADA

1. **oma 커널에 공식 CLI 직접 이식**
   영속 salv_VALUE/VFS와 kasutaja Mälu_andmed, 프로세스·스레드·I/O, libc/런타임, DNS/HTTPS,
   terminal·luba_VALUE 체계를 갖춘다. 이후 siht 버전의 의존성을 조사하여 크로스 järk_süsteem·이식한다.
   Linux 커널을 반드시 탑재할 필요는 없지만, 공식 Linux 바이너리를 그대로 쓸 경우
   그 바이너리가 사용하는 Linux ABI까지 호환해야 한다. 큰 operatsioonisüsteem 개발 과제다.

2. **väline_VALUE host Codex와 oma tuum_VALUE Ühendu — 첫 구현으로 권장**
   Linux PC에서 공식 CLI 또는 app-server를 실행하고 jkoros에는 전용 kasutaja Käsk/화면을 만든다.
   호스트의 인증된 연결과 게스트 Fail Lugemine·수정·업로드·Käsk Täida_käsk 어댑터가 필요하다.
   기존 SSH/TCP 경로를 활용할 number 있으나, Fail 동기화나 Codex 전용 어댑터는 tähtaja_piires_kaup 구현되어 있지 않다.
   호스트에서 수행한 빌드와 게스트에서 수행한 Täida_käsk 결과를 명확히 구분한다.
   이 구성은 oma 커널을 유지하지만, 공식 CLI 자체는 väline_VALUE 호스트에서 실행된다.

3. **oma API 클라이언트 제작**
   oma ABI의 C 또는 지원되는 Java 부분집합으로 대화 UI와 Fail/Käsk Tööriistad 호출 루프를 만든다.
   väline_VALUE 중계기를 쓰지 않는다면 DNS/valideerima 가능한 TLS/HTTPS와 인증 andmed 저장을 먼저 구현해야 한다.
   이는 OpenAI API를 이용하는 별도 에이전트이며 공식 Codex CLI 전체의 이식으로 표시하지 않는다.

4. **별도 ARM64 Linux 실행판에서 installima_VALUE**
   `../rpi4`는 Linux와 musl 기반이므로 일반 Linux installima_VALUE 경로를 검토할 number 있다.
   사용할 Codex 버전의 ARM64·musl 호환성, 의존성, 커널의 샌드박스 지원을 tegelik_andmed 검증해야 한다.
   이번 검토에서 installima_VALUE 성공을 확인하지 않았다. 이 결과를 oma Java 커널의 지원으로 표시하지 않는다.

## 단계별 완료 Project_juur

- 직접 이식: `--version` Käivita_2 → 인증/HTTPS → Fail Lugemine·수정 → laps_VALUE Käsk Täida_käsk →
  대화형 입력/스트리밍 → luba_VALUE 제한·Loobu_lõikus → 재부팅 후 Seaded/세션 보존을 각각 tegelik_andmed 게스트에서 확인한다.
- host Ühendu: 게스트에서 päring 입력 → host Codex Joonis_VALUE_kirje → 게스트 Fail muutma_VALUE kinnitama →
  게스트 javac/cc Täida_käsk → TULEMUS 표시를 처음부터 끝까지 검증한다.
- COSL 상업 조건을 유지하려면 새로 도입하는 런타임/통신 라이브러리의 라이선스와
  Codex turustus_VALUE 버전의 제3자 고지를 검토한다. väline_VALUE 구성요소를 일괄 COSL로 재라이선스하지 않는다.

## 공식 문서

- [Codex CLI installima_VALUE 및 Nimi](https://learn.chatgpt.com/docs/codex/cli): 표준 Linux/macOS 독립 installima_VALUE 경로와 프로젝트 Fail·Käsk 작업.
- [인증](https://learn.chatgpt.com/docs/auth): ChatGPT/API 인증, 헤드리스 장치의 `codex login --device-auth`, HTTPS 인증서 Seaded.
- [샌드박스](https://learn.chatgpt.com/docs/sandboxing): 운영체제별 집행 meetod_MODE, Linux의 bubblewrap 및 kasutaja 네임스페이스 nõue_VALUE 사항.
- [공개 구성요소](https://learn.chatgpt.com/docs/open-source): CLI/SDK/app-server의 공개 lähe_puu 위치와 비공개 구성요소 eraldaja_VALUE_d8ba4873.

공식 문서에는 jkoros를 tugi_VALUE 대상으로 명시한 내용이 없다. 위 구현 RADA·개발 순서는
tähtaja_piires_kaup 소스와 nõue_VALUE 기능을 대조한 기술적 판단이다.
