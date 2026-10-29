# tựThân ARM64 커널의 Codex càiĐặtGiáTrị 가능성 검토

검토일: 2026-10-05. 소스와 공식 문서를 대조한 설계 검토이며, 게스트에 Codex를 설치하거나
로그인·모델 호출을 실행한 결과는 아니다. tựThân ARM64 커널과 `../rpi4` Linux 실행판은 구분한다.

phầnMụcHiệnTại tựThân 커널에는 공식 Codex CLI를 그대로 càiĐặtGiáTrị·실행할 trịSố 없다.
기술적으로 필요한 thựcThiLệnh 환경을 추가하거나 Codex를 이식하는 경로는 있으나,
다운로드 lệnh 하나를 추가하는 작업으로 해결되지 않는다. JDK/JRE 기능 확장만으로도 해결되지 않는다.

## 확인한 근거

| giáTrịMục | phầnMụcHiệnTại 소스에서 확인한 giáTrịTrạngThái | 직접 실행을 위한 TácVụ |
|---|---|---|
| thựcThiLệnh Tệp | `máy/NgườiDùng.c`: AArch64 ET_EXEC만, PT_INTERP/PT_DYNAMIC/PT_TLS từChốiGiáTrị, 업로드 thựcThiLệnh 버퍼 16384바이트 | giáTrịĐốiĐích 바이너리에 맞는 ELF 적재·재배치·thựcThiLệnh khởiTạo, dữLiệuBộNhớ/Tệp giáTrịGiớiHạn giáTrịPhầnMởRộng |
| Linux ABI | `máy/tươngThíchLinux.inc`: read/write/openat/brk 등 제한된 번호만 mụcGiáTrịTiếnTrình, 나머지는 ENOSYS | libc/런타임에 필요한 시스템 호출을 추가하거나 tựThân ABI용 런타임 ChuyểnNền |
| 프로세스·스레드 | 일반 fork/clone/execve, pthread/futex, 시그널, mmap, poll/epoll 계열이 미완성 | 비동기 I/O·스레드·giáTrịCon lệnh thựcThiLệnh·chươngTrìnhRa/thaoTácHủy 기능 |
| Tệp | `mãNguồn/CácTệpBộNhớ.java`: RAM Tệp 64개, 파일당 16 KiB, 비영속 | 큰 thựcThiLệnh Tệp·프로젝트·cácThiếtLập·세션을 위한 영속 VFS, Tệp giáTrịQuyền·đườngDẫn·디렉터리 giáTrịPhầnMởRộng |
| 네트워크 | lwIP TCP/UDP는 있으나 `NgănXếpMạng/lwipopts.h`의 LWIP_DNS=0, 일반 HTTPS 클라이언트 phươngThứcThiếu | DNS, TLS 인증서 thẩmĐịnh·신뢰 gốcCâyKhoNguồn·정확한 giáTrịDấuThờiGian, HTTPS/스트리밍 |
| thiếtBịCuối·CôngCụ | tựThân 셸과 GUI 터미널은 있지만 표준 PTY·일반 프로세스 TácVụ giáTrịĐiềuKhiển phươngThứcThiếu | tươngTác CLI용 thiếtBịCuối 기능, vỏLệnh/Tệp 검색/xâyDựngHệThống CôngCụ nốiKết |
| thựcThiLệnh giáTrịQuyền | EL0 보호는 있으나 Codex의 Linux 샌드박스와 같은 정책 집행 môiTrường phươngThứcThiếu | Tệp·네트워크·lệnh giáTrịQuyền 정책과 승인 기능; tựThân 커널에 맞는 격리 phầnCàiĐặt |

여기서 ELF의 PT_TLS는 스레드별 giáTrịCất 공간이다. HTTPS의 TLS giáTrịMậtKhẩu 통신과 서로 다른 기능이다.
ELF Tệp 형식을 읽을 trịSố 있다는 사실만으로 Linux thựcThiLệnh 환경을 제공하는 것은 아니다.
SSH/VNC를 위한 giáTrịMậtKhẩu 라이브러리를 넣은 상태도 HTTPS phầnCàiĐặt 완료를 의미하지 않는다.

호스트의 `/home/user/.local/bin/codex`도 확인했다. 이것은 x86-64 ELF ET_DYN이며 약 209 MiB다.
해당 파일을 ARM64 게스트로 복사하여 실행할 trịSố 없다. 이 크기를 ARM64 giáTrịBảnPhânPhối 파일의 크기로
해석하지 않는다. 공식 ARM64 빌드의 dữLiệuThựcTế cỡ·의존성은 설치할 버전으로 thêmCuốiMục 검사해야 한다.

## 가능한 phầnCàiĐặt đườngDẫn

1. **tựThân 커널에 공식 CLI 직접 ChuyểnNền**
   영속 giáTrịCất/VFS와 NgườiDùng dữLiệuBộNhớ, 프로세스·스레드·I/O, libc/런타임, DNS/HTTPS,
   thiếtBịCuối·giáTrịQuyền 체계를 갖춘다. giáTrịSau giáTrịĐốiĐích 버전의 의존성을 조사하여 크로스 xâyDựngHệThống·이식한다.
   Linux 커널을 반드시 탑재할 필요는 없지만, 공식 Linux 바이너리를 그대로 쓸 경우
   그 바이너리가 사용하는 Linux ABI까지 호환해야 한다. 큰 HệĐiềuHành phátTriển 과제다.

2. **giáTrịBênNgoài Chủ Codex와 tựThân giáTrịNhân nốiKết — phầnMụcĐầuTiên 구현으로 권장**
   Linux PC에서 공식 CLI 또는 app-server를 실행하고 jkoros에는 전용 NgườiDùng lệnh/화면을 만든다.
   호스트의 인증된 연결과 게스트 Tệp đọc·chỉnhSửaGiáTrị·업로드·lệnh thựcThiLệnh 어댑터가 필요하다.
   기존 SSH/TCP 경로를 활용할 trịSố 있으나, Tệp 동기화나 Codex 전용 어댑터는 phầnMụcHiệnTại 구현되어 있지 않다.
   호스트에서 수행한 빌드와 게스트에서 수행한 thựcThiLệnh 결과를 명확히 구분한다.
   이 구성은 tựThân 커널을 유지하지만, 공식 CLI 자체는 giáTrịBênNgoài 호스트에서 실행된다.

3. **tựThân API 클라이언트 제작**
   tựThân ABI의 C 또는 지원되는 Java 부분집합으로 phiênTươngTác UI와 Tệp/lệnh CôngCụ gọiThựcHiện 루프를 만든다.
   giáTrịBênNgoài 중계기를 쓰지 않는다면 DNS/thẩmĐịnh 가능한 TLS/HTTPS와 인증 DữLiệu 저장을 먼저 구현해야 한다.
   이는 OpenAI API를 이용하는 별도 에이전트이며 공식 Codex CLI 전체의 이식으로 표시하지 않는다.

4. **별도 ARM64 Linux 실행판에서 càiĐặtGiáTrị**
   `../rpi4`는 Linux와 musl 기반이므로 일반 Linux càiĐặtGiáTrị 경로를 검토할 trịSố 있다.
   사용할 Codex 버전의 ARM64·musl 호환성, cácPhụThuộc, 커널의 샌드박스 지원을 dữLiệuThựcTế 검증해야 한다.
   이번 검토에서 càiĐặtGiáTrị 성공을 확인하지 않았다. 이 결과를 tựThân Java 커널의 지원으로 표시하지 않는다.

## 단계별 làĐầyĐủ gốcCâyDựÁn

- 직접 ChuyểnNền: `--version` chạy → 인증/HTTPS → Tệp đọc·chỉnhSửaGiáTrị → giáTrịCon lệnh thựcThiLệnh →
  tươngTác giáTrịVào/스트리밍 → giáTrịQuyền giáTrịGiớiHạn·thaoTácHủy → 재부팅 trạngTháiSau cácThiếtLập/세션 보존을 각각 dữLiệuThựcTế 게스트에서 확인한다.
- Chủ nốiKết: 게스트에서 yêuCầu giáTrịVào → Chủ Codex mụcGiáTrịTiếnTrình → 게스트 Tệp đổiGiáTrị xácMinh →
  게스트 javac/cc thựcThiLệnh → kếtQuả 표시를 처음부터 끝까지 검증한다.
- COSL 상업 조건을 유지하려면 새로 도입하는 런타임/TruyềnThông 라이브러리의 라이선스와
  Codex giáTrịBảnPhânPhối 버전의 제3자 고지를 검토한다. giáTrịBênNgoài 구성요소를 일괄 COSL로 재라이선스하지 않는다.

## 공식 TàiLiệu

- [Codex CLI càiĐặtGiáTrị 및 hànhĐộng](https://learn.chatgpt.com/docs/codex/cli): 표준 Linux/macOS 독립 càiĐặtGiáTrị 경로와 프로젝트 Tệp·lệnh TácVụ.
- [인증](https://learn.chatgpt.com/docs/auth): ChatGPT/API 인증, 헤드리스 장치의 `codex login --device-auth`, HTTPS 인증서 cácThiếtLập.
- [샌드박스](https://learn.chatgpt.com/docs/sandboxing): 운영체제별 집행 chếĐộPhươngThức, Linux의 bubblewrap 및 NgườiDùng 네임스페이스 giáTrịĐiềuBắtBuộc 사항.
- [공개 구성요소](https://learn.chatgpt.com/docs/open-source): CLI/SDK/app-server의 공개 câyNguồn 위치와 비공개 구성요소 giáTrịDấuPhânCách.

공식 문서에는 jkoros를 giáTrịHỗTrợ 대상으로 명시한 내용이 없다. giáTrịĐỉnh phầnCàiĐặt đườngDẫn·phátTriển 순서는
phầnMụcHiệnTại 소스와 giáTrịĐiềuBắtBuộc 기능을 대조한 기술적 판단이다.
