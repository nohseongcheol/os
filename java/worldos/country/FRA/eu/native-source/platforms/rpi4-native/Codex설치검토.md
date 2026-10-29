# 자체 ARM64 커널의 Codex instalatu_balio 가능성 검토

검토일: 2026-10-05. 소스와 공식 문서를 대조한 설계 검토이며, 게스트에 Codex를 설치하거나
로그인·모델 호출을 실행한 결과는 아니다. 자체 ARM64 커널과 `../rpi4` Linux 실행판은 구분한다.

현재 자체 커널에는 공식 Codex CLI를 그대로 instalatu_balio·실행할 수 없다.
기술적으로 필요한 exekutatu_komando 환경을 추가하거나 Codex를 이식하는 경로는 있으나,
다운로드 Komandoa 하나를 추가하는 작업으로 해결되지 않는다. JDK/JRE 기능 확장만으로도 해결되지 않는다.

## 확인한 근거

| sarrera_balio | 현재 소스에서 확인한 Egoera_balio | 직접 실행을 위한 작업 |
|---|---|---|
| exekutatu_komando Fitxategia | `gailu/erabiltzaile.c`: AArch64 ET_EXEC만, PT_INTERP/PT_DYNAMIC/PT_TLS baztertu_balio, 업로드 exekutatu_komando 버퍼 16384바이트 | helburu_balio 바이너리에 맞는 ELF 적재·재배치·exekutatu_komando hasieratu, Memoria_datuak/Fitxategia 제한 luzapen_balio |
| Linux ABI | `gailu/리눅스호환.inc`: read/write/openat/brk 등 제한된 번호만 prozesu_balio_sarrera, 나머지는 ENOSYS | libc/런타임에 필요한 시스템 호출을 추가하거나 자체 ABI용 런타임 이식 |
| 프로세스·스레드 | 일반 fork/clone/execve, pthread/futex, 시그널, mmap, poll/epoll 계열이 미완성 | 비동기 I/O·스레드·haur_balio Komandoa exekutatu_komando·irten_aplik/Utzi_kirurgia 기능 |
| Fitxategia | `ITURBURUA/Memoria_Fitxategiak.java`: RAM Fitxategia 64개, 파일당 16 KiB, 비영속 | 큰 exekutatu_komando Fitxategia·프로젝트·Ezarpenak·세션을 위한 영속 VFS, Fitxategia baimen_balio·Bide_izena·디렉터리 luzapen_balio |
| 네트워크 | lwIP TCP/UDP는 있으나 `sare_pila/lwipopts.h`의 LWIP_DNS=0, 일반 HTTPS 클라이언트 없음 | DNS, TLS 인증서 baliozkotu·신뢰 biltegi_erro·정확한 denbora_zigilu_balio, HTTPS/스트리밍 |
| Terminala·Tresnak | 자체 셸과 GUI 터미널은 있지만 표준 PTY·일반 프로세스 작업 kontrol_balio 없음 | interaktibo CLI용 Terminala 기능, shell/Fitxategia 검색/eraiki_sistema Tresnak Konektatu |
| exekutatu_komando baimen_balio | EL0 보호는 있으나 Codex의 Linux 샌드박스와 같은 정책 집행 환경 없음 | Fitxategia·네트워크·Komandoa baimen_balio 정책과 승인 기능; 자체 커널에 맞는 격리 구현 |

여기서 ELF의 PT_TLS는 스레드별 Store_balio 공간이다. HTTPS의 TLS pasahitz_balio 통신과 서로 다른 기능이다.
ELF Fitxategia 형식을 읽을 수 있다는 사실만으로 Linux exekutatu_komando 환경을 제공하는 것은 아니다.
SSH/VNC를 위한 pasahitz_balio 라이브러리를 넣은 상태도 HTTPS 구현 완료를 의미하지 않는다.

호스트의 `/home/user/.local/bin/codex`도 확인했다. 이것은 x86-64 ELF ET_DYN이며 약 209 MiB다.
해당 파일을 ARM64 게스트로 복사하여 실행할 수 없다. 이 크기를 ARM64 배포 파일의 크기로
해석하지 않는다. 공식 ARM64 빌드의 benetako_datuak Tamaina·의존성은 설치할 버전으로 Erantsi_sarrera 검사해야 한다.

## 가능한 구현 Bide_izena

1. **자체 커널에 공식 CLI 직접 이식**
   영속 Store_balio/VFS와 erabiltzaile Memoria_datuak, 프로세스·스레드·I/O, libc/런타임, DNS/HTTPS,
   Terminala·baimen_balio 체계를 갖춘다. 이후 helburu_balio 버전의 의존성을 조사하여 크로스 eraiki_sistema·이식한다.
   Linux 커널을 반드시 탑재할 필요는 없지만, 공식 Linux 바이너리를 그대로 쓸 경우
   그 바이너리가 사용하는 Linux ABI까지 호환해야 한다. 큰 sistema_eragile 개발 과제다.

2. **외부 Ostalari Codex와 자체 nukleo_balio Konektatu — 첫 구현으로 권장**
   Linux PC에서 공식 CLI 또는 app-server를 실행하고 jkoros에는 전용 erabiltzaile Komandoa/화면을 만든다.
   호스트의 인증된 연결과 게스트 Fitxategia Irakurri·수정·업로드·Komandoa exekutatu_komando 어댑터가 필요하다.
   기존 SSH/TCP 경로를 활용할 수 있으나, Fitxategia 동기화나 Codex 전용 어댑터는 현재 구현되어 있지 않다.
   호스트에서 수행한 빌드와 게스트에서 수행한 exekutatu_komando 결과를 명확히 구분한다.
   이 구성은 자체 커널을 유지하지만, 공식 CLI 자체는 외부 호스트에서 실행된다.

3. **자체 API 클라이언트 제작**
   자체 ABI의 C 또는 지원되는 Java 부분집합으로 interaktibo_saio UI와 Fitxategia/Komandoa Tresnak 호출 루프를 만든다.
   외부 중계기를 쓰지 않는다면 DNS/baliozkotu 가능한 TLS/HTTPS와 인증 datuak 저장을 먼저 구현해야 한다.
   이는 OpenAI API를 이용하는 별도 에이전트이며 공식 Codex CLI 전체의 이식으로 표시하지 않는다.

4. **별도 ARM64 Linux 실행판에서 instalatu_balio**
   `../rpi4`는 Linux와 musl 기반이므로 일반 Linux instalatu_balio 경로를 검토할 수 있다.
   사용할 Codex 버전의 ARM64·musl 호환성, 의존성, 커널의 샌드박스 지원을 benetako_datuak 검증해야 한다.
   이번 검토에서 instalatu_balio 성공을 확인하지 않았다. 이 결과를 자체 Java 커널의 지원으로 표시하지 않는다.

## 단계별 완료 Project_erro

- 직접 이식: `--version` Exekutatu_2 → 인증/HTTPS → Fitxategia Irakurri·수정 → haur_balio Komandoa exekutatu_komando →
  interaktibo 입력/스트리밍 → baimen_balio 제한·Utzi_kirurgia → 재부팅 후 Ezarpenak/세션 보존을 각각 benetako_datuak 게스트에서 확인한다.
- Ostalari Konektatu: 게스트에서 eskaera 입력 → Ostalari Codex prozesu_balio_sarrera → 게스트 Fitxategia aldatu_balio egiaztatu →
  게스트 javac/cc exekutatu_komando → EMAITZA 표시를 처음부터 끝까지 검증한다.
- COSL 상업 조건을 유지하려면 새로 도입하는 런타임/통신 라이브러리의 라이선스와
  Codex 배포 버전의 제3자 고지를 검토한다. 외부 구성요소를 일괄 COSL로 재라이선스하지 않는다.

## 공식 문서

- [Codex CLI instalatu_balio 및 Ekintza](https://learn.chatgpt.com/docs/codex/cli): 표준 Linux/macOS 독립 instalatu_balio 경로와 프로젝트 Fitxategia·Komandoa 작업.
- [인증](https://learn.chatgpt.com/docs/auth): ChatGPT/API 인증, 헤드리스 장치의 `codex login --device-auth`, HTTPS 인증서 Ezarpenak.
- [샌드박스](https://learn.chatgpt.com/docs/sandboxing): 운영체제별 집행 방식, Linux의 bubblewrap 및 erabiltzaile 네임스페이스 요구 사항.
- [공개 구성요소](https://learn.chatgpt.com/docs/open-source): CLI/SDK/app-server의 공개 iturburu_zuhaitz 위치와 비공개 구성요소 mugatzaile_balio.

공식 문서에는 jkoros를 Laguntza_balio 대상으로 명시한 내용이 없다. 위 구현 Bide_izena·개발 순서는
현재 소스와 요구 기능을 대조한 기술적 판단이다.
