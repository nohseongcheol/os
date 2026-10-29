# 자체 ARM64 커널의 Codex tsenya_Boleng 가능성 검토

검토일: 2026-10-05. 소스와 공식 문서를 대조한 설계 검토이며, 게스트에 Codex를 설치하거나
로그인·모델 호출을 실행한 결과는 아니다. 자체 ARM64 커널과 `../rpi4` Linux 실행판은 구분한다.

ga_jaana_selwana 자체 커널에는 공식 Codex CLI를 그대로 tsenya_Boleng·실행할 수 없다.
기술적으로 필요한 diragatsa_Taelo 환경을 추가하거나 Codex를 이식하는 경로는 있으나,
다운로드 Taelo 하나를 추가하는 작업으로 해결되지 않는다. JDK/JRE 기능 확장만으로도 해결되지 않는다.

## 확인한 근거

| tsenyo_Boleng | ga_jaana_selwana 소스에서 확인한 kemo_Boleng | 직접 실행을 위한 작업 |
|---|---|---|
| diragatsa_Taelo faele | `motšhine/modirisi.c`: AArch64 ET_EXEC만, PT_INTERP/PT_DYNAMIC/PT_TLS 거부, 업로드 diragatsa_Taelo 버퍼 16384바이트 | setotwa 바이너리에 맞는 ELF 적재·재배치·diragatsa_Taelo go_baakanyetsa_tiriso, memori_tshedimosetso/faele 제한 katoloso_Boleng |
| Linux ABI | `motšhine/리눅스호환.inc`: read/write/openat/brk 등 제한된 번호만 Thulaganyo_Boleng_tsenyo, 나머지는 ENOSYS | libc/런타임에 필요한 시스템 호출을 추가하거나 자체 ABI용 런타임 이식 |
| 프로세스·스레드 | 일반 fork/clone/execve, pthread/futex, 시그널, mmap, poll/epoll 계열이 미완성 | 비동기 I/O·스레드·ngwana_Boleng Taelo diragatsa_Taelo·tswaya_Tiriso/khansela_tiro 기능 |
| faele | `Motswedi/memori_Difaele.java`: RAM faele 64개, 파일당 16 KiB, 비영속 | 큰 diragatsa_Taelo faele·프로젝트·Diseting·세션을 위한 영속 VFS, faele tetla_Boleng·tsela·디렉터리 katoloso_Boleng |
| 네트워크 | lwIP TCP/UDP는 있으나 `Neteweke_kokoanyodinepe/lwipopts.h`의 LWIP_DNS=0, 일반 HTTPS 클라이언트 없음 | DNS, TLS 인증서 netefatsa_5fb2b747·신뢰 저장소·정확한 시각, HTTPS/스트리밍 |
| 터미널·Thuluse | 자체 셸과 GUI 터미널은 있지만 표준 PTY·일반 프로세스 작업 taolo_Boleng 없음 | Tirisano CLI용 터미널 기능, setlhalosataelo/faele 검색/aga_tsamaiso Thuluse Golaganya |
| diragatsa_Taelo tetla_Boleng | EL0 보호는 있으나 Codex의 Linux 샌드박스와 같은 정책 집행 환경 없음 | faele·네트워크·Taelo tetla_Boleng 정책과 승인 기능; 자체 커널에 맞는 격리 구현 |

여기서 ELF의 PT_TLS는 스레드별 Store_Boleng 공간이다. HTTPS의 TLS khoututseno_Boleng 통신과 서로 다른 기능이다.
ELF faele 형식을 읽을 수 있다는 사실만으로 Linux diragatsa_Taelo 환경을 제공하는 것은 아니다.
SSH/VNC를 위한 khoututseno_Boleng 라이브러리를 넣은 상태도 HTTPS 구현 완료를 의미하지 않는다.

호스트의 `/home/user/.local/bin/codex`도 확인했다. 이것은 x86-64 ELF ET_DYN이며 약 209 MiB다.
해당 파일을 ARM64 게스트로 복사하여 실행할 수 없다. 이 크기를 ARM64 배포 파일의 크기로
해석하지 않는다. 공식 ARM64 빌드의 tota_tshedimosetso lekanya·의존성은 설치할 버전으로 추가 검사해야 한다.

## 가능한 구현 tsela

1. **자체 커널에 공식 CLI 직접 이식**
   영속 Store_Boleng/VFS와 modirisi memori_tshedimosetso, 프로세스·스레드·I/O, libc/런타임, DNS/HTTPS,
   터미널·tetla_Boleng 체계를 갖춘다. 이후 setotwa 버전의 의존성을 조사하여 크로스 aga_tsamaiso·이식한다.
   Linux 커널을 반드시 탑재할 필요는 없지만, 공식 Linux 바이너리를 그대로 쓸 경우
   그 바이너리가 사용하는 Linux ABI까지 호환해야 한다. 큰 Tsamaisotiriso 개발 과제다.

2. **외부 pinagare Codex와 자체 Khenele_Boleng Golaganya — 첫 구현으로 권장**
   Linux PC에서 공식 CLI 또는 app-server를 실행하고 jkoros에는 전용 modirisi Taelo/화면을 만든다.
   호스트의 인증된 연결과 게스트 faele 읽기·수정·업로드·Taelo diragatsa_Taelo 어댑터가 필요하다.
   기존 SSH/TCP 경로를 활용할 수 있으나, faele 동기화나 Codex 전용 어댑터는 ga_jaana_selwana 구현되어 있지 않다.
   호스트에서 수행한 빌드와 게스트에서 수행한 diragatsa_Taelo 결과를 명확히 구분한다.
   이 구성은 자체 커널을 유지하지만, 공식 CLI 자체는 외부 호스트에서 실행된다.

3. **자체 API 클라이언트 제작**
   자체 ABI의 C 또는 지원되는 Java 부분집합으로 Tirisano_nakotiriso UI와 faele/Taelo Thuluse 호출 루프를 만든다.
   외부 중계기를 쓰지 않는다면 DNS/netefatsa_5fb2b747 가능한 TLS/HTTPS와 인증 tshedimosetso 저장을 먼저 구현해야 한다.
   이는 OpenAI API를 이용하는 별도 에이전트이며 공식 Codex CLI 전체의 이식으로 표시하지 않는다.

4. **별도 ARM64 Linux 실행판에서 tsenya_Boleng**
   `../rpi4`는 Linux와 musl 기반이므로 일반 Linux tsenya_Boleng 경로를 검토할 수 있다.
   사용할 Codex 버전의 ARM64·musl 호환성, 의존성, 커널의 샌드박스 지원을 tota_tshedimosetso 검증해야 한다.
   이번 검토에서 tsenya_Boleng 성공을 확인하지 않았다. 이 결과를 자체 Java 커널의 지원으로 표시하지 않는다.

## 단계별 완료 기준

- 직접 이식: `--version` dirisa → 인증/HTTPS → faele 읽기·수정 → ngwana_Boleng Taelo diragatsa_Taelo →
  Tirisano 입력/스트리밍 → tetla_Boleng 제한·khansela_tiro → 재부팅 후 Diseting/세션 보존을 각각 tota_tshedimosetso 게스트에서 확인한다.
- pinagare Golaganya: 게스트에서 요청 입력 → pinagare Codex Thulaganyo_Boleng_tsenyo → 게스트 faele fetola_Boleng netefatsa →
  게스트 javac/cc diragatsa_Taelo → 결과 표시를 처음부터 끝까지 검증한다.
- COSL 상업 조건을 유지하려면 새로 도입하는 런타임/통신 라이브러리의 라이선스와
  Codex 배포 버전의 제3자 고지를 검토한다. 외부 구성요소를 일괄 COSL로 재라이선스하지 않는다.

## 공식 문서

- [Codex CLI tsenya_Boleng 및 tiro](https://learn.chatgpt.com/docs/codex/cli): 표준 Linux/macOS 독립 tsenya_Boleng 경로와 프로젝트 faele·Taelo 작업.
- [인증](https://learn.chatgpt.com/docs/auth): ChatGPT/API 인증, 헤드리스 장치의 `codex login --device-auth`, HTTPS 인증서 Diseting.
- [샌드박스](https://learn.chatgpt.com/docs/sandboxing): 운영체제별 집행 mokgwa_mokgwa, Linux의 bubblewrap 및 modirisi 네임스페이스 요구 사항.
- [공개 구성요소](https://learn.chatgpt.com/docs/open-source): CLI/SDK/app-server의 공개 Motswedi_sebopego_sa_tshedimosetso 위치와 비공개 구성요소 sekgaoganyi_Boleng.

공식 문서에는 jkoros를 Thuso_Boleng 대상으로 명시한 내용이 없다. 위 구현 tsela·개발 순서는
ga_jaana_selwana 소스와 요구 기능을 대조한 기술적 판단이다.
