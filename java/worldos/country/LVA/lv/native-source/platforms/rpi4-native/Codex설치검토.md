# savs ARM64 커널의 Codex instalēt_VALUE 가능성 검토

검토일: 2026-10-05. 소스와 공식 문서를 대조한 설계 검토이며, 게스트에 Codex를 설치하거나
로그인·모델 호출을 실행한 결과는 아니다. savs ARM64 커널과 `../rpi4` Linux 실행판은 구분한다.

pašreizējais_krājums savs 커널에는 공식 Codex CLI를 그대로 instalēt_VALUE·실행할 numurs 없다.
기술적으로 필요한 Izpildīt_komanda 환경을 추가하거나 Codex를 이식하는 경로는 있으나,
다운로드 Komanda 하나를 추가하는 작업으로 해결되지 않는다. JDK/JRE 기능 확장만으로도 해결되지 않는다.

## 확인한 근거

| ievade_VALUE | pašreizējais_krājums 소스에서 확인한 Statuss_VALUE | 직접 실행을 위한 작업 |
|---|---|---|
| Izpildīt_komanda Fails | `mašīna/lietotājs.c`: AArch64 ET_EXEC만, PT_INTERP/PT_DYNAMIC/PT_TLS noraidīt_VALUE, 업로드 Izpildīt_komanda 버퍼 16384바이트 | mērķis 바이너리에 맞는 ELF 적재·재배치·Izpildīt_komanda 초기화, atmiņa_dati/Fails 제한 paplašinājums_VALUE |
| Linux ABI | `mašīna/리눅스호환.inc`: read/write/openat/brk 등 제한된 번호만 Process_VALUE_ievade, 나머지는 ENOSYS | libc/런타임에 필요한 시스템 호출을 추가하거나 savs ABI용 런타임 이식 |
| 프로세스·스레드 | 일반 fork/clone/execve, pthread/futex, 시그널, mmap, poll/epoll 계열이 미완성 | 비동기 I/O·스레드·bērns_VALUE Komanda Izpildīt_komanda·Iziet_programma/Atcelt_operācija 기능 |
| Fails | `AVOTS/atmiņa_Faili.java`: RAM Fails 64개, 파일당 16 KiB, 비영속 | 큰 Izpildīt_komanda Fails·프로젝트·Uzstādījumi·세션을 위한 영속 VFS, Fails atļauja_VALUE·CEĻŠ·디렉터리 paplašinājums_VALUE |
| 네트워크 | lwIP TCP/UDP는 있으나 `tīkls_kopa/lwipopts.h`의 LWIP_DNS=0, 일반 HTTPS 클라이언트 없음 | DNS, TLS 인증서 validēt·신뢰 repozitorijs_sakne·정확한 timestamp_VALUE, HTTPS/스트리밍 |
| Terminālis·Rīki | savs 셸과 GUI 터미널은 있지만 표준 PTY·일반 프로세스 작업 vadība_VALUE 없음 | 대화형 CLI용 Terminālis 기능, čaula/Fails 검색/būvējums_sistēma Rīki Savienoties |
| Izpildīt_komanda atļauja_VALUE | EL0 보호는 있으나 Codex의 Linux 샌드박스와 같은 정책 집행 환경 없음 | Fails·네트워크·Komanda atļauja_VALUE 정책과 승인 기능; savs 커널에 맞는 격리 구현 |

여기서 ELF의 PT_TLS는 스레드별 Store_VALUE 공간이다. HTTPS의 TLS parole_VALUE 통신과 서로 다른 기능이다.
ELF Fails 형식을 읽을 numurs 있다는 사실만으로 Linux Izpildīt_komanda 환경을 제공하는 것은 아니다.
SSH/VNC를 위한 parole_VALUE 라이브러리를 넣은 상태도 HTTPS 구현 완료를 의미하지 않는다.

호스트의 `/home/user/.local/bin/codex`도 확인했다. 이것은 x86-64 ELF ET_DYN이며 약 209 MiB다.
해당 파일을 ARM64 게스트로 복사하여 실행할 numurs 없다. 이 크기를 ARM64 sadale_VALUE 파일의 크기로
해석하지 않는다. 공식 ARM64 빌드의 faktisks_dati Izmērs·의존성은 설치할 버전으로 Pievienot_ievade 검사해야 한다.

## 가능한 구현 CEĻŠ

1. **savs 커널에 공식 CLI 직접 이식**
   영속 Store_VALUE/VFS와 lietotājs atmiņa_dati, 프로세스·스레드·I/O, libc/런타임, DNS/HTTPS,
   Terminālis·atļauja_VALUE 체계를 갖춘다. 이후 mērķis 버전의 의존성을 조사하여 크로스 būvējums_sistēma·이식한다.
   Linux 커널을 반드시 탑재할 필요는 없지만, 공식 Linux 바이너리를 그대로 쓸 경우
   그 바이너리가 사용하는 Linux ABI까지 호환해야 한다. 큰 operētājsistēma 개발 과제다.

2. **ārējs_VALUE viesot Codex와 savs kodols_VALUE Savienoties — 첫 구현으로 권장**
   Linux PC에서 공식 CLI 또는 app-server를 실행하고 jkoros에는 전용 lietotājs Komanda/화면을 만든다.
   호스트의 인증된 연결과 게스트 Fails Lasīt·수정·업로드·Komanda Izpildīt_komanda 어댑터가 필요하다.
   기존 SSH/TCP 경로를 활용할 numurs 있으나, Fails 동기화나 Codex 전용 어댑터는 pašreizējais_krājums 구현되어 있지 않다.
   호스트에서 수행한 빌드와 게스트에서 수행한 Izpildīt_komanda 결과를 명확히 구분한다.
   이 구성은 savs 커널을 유지하지만, 공식 CLI 자체는 ārējs_VALUE 호스트에서 실행된다.

3. **savs API 클라이언트 제작**
   savs ABI의 C 또는 지원되는 Java 부분집합으로 대화 UI와 Fails/Komanda Rīki 호출 루프를 만든다.
   ārējs_VALUE 중계기를 쓰지 않는다면 DNS/validēt 가능한 TLS/HTTPS와 인증 dati 저장을 먼저 구현해야 한다.
   이는 OpenAI API를 이용하는 별도 에이전트이며 공식 Codex CLI 전체의 이식으로 표시하지 않는다.

4. **별도 ARM64 Linux 실행판에서 instalēt_VALUE**
   `../rpi4`는 Linux와 musl 기반이므로 일반 Linux instalēt_VALUE 경로를 검토할 numurs 있다.
   사용할 Codex 버전의 ARM64·musl 호환성, 의존성, 커널의 샌드박스 지원을 faktisks_dati 검증해야 한다.
   이번 검토에서 instalēt_VALUE 성공을 확인하지 않았다. 이 결과를 savs Java 커널의 지원으로 표시하지 않는다.

## 단계별 완료 Project_sakne

- 직접 이식: `--version` Palaist → 인증/HTTPS → Fails Lasīt·수정 → bērns_VALUE Komanda Izpildīt_komanda →
  대화형 입력/스트리밍 → atļauja_VALUE 제한·Atcelt_operācija → 재부팅 후 Uzstādījumi/세션 보존을 각각 faktisks_dati 게스트에서 확인한다.
- viesot Savienoties: 게스트에서 pieprasījums 입력 → viesot Codex Process_VALUE_ievade → 게스트 Fails mainīt_VALUE verificēt →
  게스트 javac/cc Izpildīt_komanda → mērs 표시를 처음부터 끝까지 검증한다.
- COSL 상업 조건을 유지하려면 새로 도입하는 런타임/통신 라이브러리의 라이선스와
  Codex sadale_VALUE 버전의 제3자 고지를 검토한다. ārējs_VALUE 구성요소를 일괄 COSL로 재라이선스하지 않는다.

## 공식 문서

- [Codex CLI instalēt_VALUE 및 Darbība](https://learn.chatgpt.com/docs/codex/cli): 표준 Linux/macOS 독립 instalēt_VALUE 경로와 프로젝트 Fails·Komanda 작업.
- [인증](https://learn.chatgpt.com/docs/auth): ChatGPT/API 인증, 헤드리스 장치의 `codex login --device-auth`, HTTPS 인증서 Uzstādījumi.
- [샌드박스](https://learn.chatgpt.com/docs/sandboxing): 운영체제별 집행 metode_MODE, Linux의 bubblewrap 및 lietotājs 네임스페이스 prasība_VALUE 사항.
- [공개 구성요소](https://learn.chatgpt.com/docs/open-source): CLI/SDK/app-server의 공개 avots_koks 위치와 비공개 구성요소 norobežotājs_VALUE.

공식 문서에는 jkoros를 Atbalsts_VALUE 대상으로 명시한 내용이 없다. 위 구현 CEĻŠ·개발 순서는
pašreizējais_krājums 소스와 prasība_VALUE 기능을 대조한 기술적 판단이다.
