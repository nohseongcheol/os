# Asli ARM64 커널의 Codex pasang_VALUE 가능성 검토

검토일: 2026-10-05. 소스와 공식 문서를 대조한 설계 검토이며, 게스트에 Codex를 설치하거나
로그인·모델 호출을 실행한 결과는 아니다. Asli ARM64 커널과 `../rpi4` Linux 실행판은 구분한다.

현재 Asli 커널에는 공식 Codex CLI를 그대로 pasang_VALUE·실행할 수 없다.
기술적으로 필요한 laksanakan_perintah 환경을 추가하거나 Codex를 이식하는 경로는 있으나,
다운로드 Perintah 하나를 추가하는 작업으로 해결되지 않는다. JDK/JRE 기능 확장만으로도 해결되지 않는다.

## 확인한 근거

| pemasukan_VALUE | 현재 소스에서 확인한 status_VALUE | 직접 실행을 위한 작업 |
|---|---|---|
| laksanakan_perintah Fail | `mesin/ruang_pengguna.c`: AArch64 ET_EXEC만, PT_INTERP/PT_DYNAMIC/PT_TLS tolak_VALUE, 업로드 laksanakan_perintah 버퍼 16384바이트 | sasaran 바이너리에 맞는 ELF 적재·재배치·laksanakan_perintah mengasal, Memori_data/Fail 제한 sambungan_VALUE |
| Linux ABI | `mesin/리눅스호환.inc`: read/write/openat/brk 등 제한된 번호만 Proses_VALUE_pemasukan, 나머지는 ENOSYS | libc/런타임에 필요한 시스템 호출을 추가하거나 Asli ABI용 런타임 이식 |
| 프로세스·스레드 | 일반 fork/clone/execve, pthread/futex, 시그널, mmap, poll/epoll 계열이 미완성 | 비동기 I/O·스레드·anak_VALUE Perintah laksanakan_perintah·Keluar_aplikasi/Batal_operasi 기능 |
| Fail | `SUMBER/Memori_Fail.java`: RAM Fail 64개, 파일당 16 KiB, 비영속 | 큰 laksanakan_perintah Fail·프로젝트·Tetapan·세션을 위한 영속 VFS, Fail keizinan_VALUE·LALUAN·디렉터리 sambungan_VALUE |
| 네트워크 | lwIP TCP/UDP는 있으나 `rangkaian_tindan/lwipopts.h`의 LWIP_DNS=0, 일반 HTTPS 클라이언트 없음 | DNS, TLS 인증서 sahkan·신뢰 repositori_akar·정확한 cap_masa_VALUE, HTTPS/스트리밍 |
| Terminal·alat | Asli 셸과 GUI 터미널은 있지만 표준 PTY·일반 프로세스 작업 kawalan_VALUE 없음 | interaktif CLI용 Terminal 기능, cangkerang/Fail 검색/bina_sistem alat Sambung |
| laksanakan_perintah keizinan_VALUE | EL0 보호는 있으나 Codex의 Linux 샌드박스와 같은 정책 집행 persekitaran 없음 | Fail·네트워크·Perintah keizinan_VALUE 정책과 승인 기능; Asli 커널에 맞는 격리 pelaksanaan |

여기서 ELF의 PT_TLS는 스레드별 stor_VALUE 공간이다. HTTPS의 TLS kata_laluan_VALUE 통신과 서로 다른 기능이다.
ELF Fail 형식을 읽을 수 있다는 사실만으로 Linux laksanakan_perintah 환경을 제공하는 것은 아니다.
SSH/VNC를 위한 kata_laluan_VALUE 라이브러리를 넣은 상태도 HTTPS pelaksanaan 완료를 의미하지 않는다.

호스트의 `/home/user/.local/bin/codex`도 확인했다. 이것은 x86-64 ELF ET_DYN이며 약 209 MiB다.
해당 파일을 ARM64 게스트로 복사하여 실행할 수 없다. 이 크기를 ARM64 배포 파일의 크기로
해석하지 않는다. 공식 ARM64 빌드의 sebenar_data Saiz·의존성은 설치할 버전으로 Tambah_pemasukan 검사해야 한다.

## 가능한 pelaksanaan LALUAN

1. **Asli 커널에 공식 CLI 직접 이식**
   영속 stor_VALUE/VFS와 ruang_pengguna Memori_data, 프로세스·스레드·I/O, libc/런타임, DNS/HTTPS,
   Terminal·keizinan_VALUE 체계를 갖춘다. 이후 sasaran 버전의 의존성을 조사하여 크로스 bina_sistem·이식한다.
   Linux 커널을 반드시 탑재할 필요는 없지만, 공식 Linux 바이너리를 그대로 쓸 경우
   그 바이너리가 사용하는 Linux ABI까지 호환해야 한다. 큰 sistem_pengendalian 개발 과제다.

2. **외부 hos Codex와 Asli kernel_VALUE Sambung — 첫 구현으로 권장**
   Linux PC에서 공식 CLI 또는 app-server를 실행하고 jkoros에는 전용 ruang_pengguna Perintah/화면을 만든다.
   호스트의 인증된 연결과 게스트 Fail Baca·수정·업로드·Perintah laksanakan_perintah 어댑터가 필요하다.
   기존 SSH/TCP 경로를 활용할 수 있으나, Fail 동기화나 Codex 전용 어댑터는 현재 구현되어 있지 않다.
   호스트에서 수행한 빌드와 게스트에서 수행한 laksanakan_perintah 결과를 명확히 구분한다.
   이 구성은 Asli 커널을 유지하지만, 공식 CLI 자체는 외부 호스트에서 실행된다.

3. **Asli API 클라이언트 제작**
   Asli ABI의 C 또는 지원되는 Java 부분집합으로 interaktif_sesi UI와 Fail/Perintah alat 호출 루프를 만든다.
   외부 중계기를 쓰지 않는다면 DNS/sahkan 가능한 TLS/HTTPS와 인증 data 저장을 먼저 구현해야 한다.
   이는 OpenAI API를 이용하는 별도 에이전트이며 공식 Codex CLI 전체의 이식으로 표시하지 않는다.

4. **별도 ARM64 Linux 실행판에서 pasang_VALUE**
   `../rpi4`는 Linux와 musl 기반이므로 일반 Linux pasang_VALUE 경로를 검토할 수 있다.
   사용할 Codex 버전의 ARM64·musl 호환성, 의존성, 커널의 샌드박스 지원을 sebenar_data 검증해야 한다.
   이번 검토에서 pasang_VALUE 성공을 확인하지 않았다. 이 결과를 Asli Java 커널의 지원으로 표시하지 않는다.

## 단계별 완료 projek_akar

- 직접 이식: `--version` Jalan → 인증/HTTPS → Fail Baca·수정 → anak_VALUE Perintah laksanakan_perintah →
  interaktif 입력/스트리밍 → keizinan_VALUE 제한·Batal_operasi → 재부팅 후 Tetapan/세션 보존을 각각 sebenar_data 게스트에서 확인한다.
- hos Sambung: 게스트에서 permintaan 입력 → hos Codex Proses_VALUE_pemasukan → 게스트 Fail ubah_VALUE tentu_sahkan →
  게스트 javac/cc laksanakan_perintah → ukuran 표시를 처음부터 끝까지 검증한다.
- COSL 상업 조건을 유지하려면 새로 도입하는 런타임/통신 라이브러리의 라이선스와
  Codex 배포 버전의 제3자 고지를 검토한다. 외부 구성요소를 일괄 COSL로 재라이선스하지 않는다.

## 공식 문서

- [Codex CLI pasang_VALUE 및 Aksi](https://learn.chatgpt.com/docs/codex/cli): 표준 Linux/macOS 독립 pasang_VALUE 경로와 프로젝트 Fail·Perintah 작업.
- [인증](https://learn.chatgpt.com/docs/auth): ChatGPT/API 인증, 헤드리스 장치의 `codex login --device-auth`, HTTPS 인증서 Tetapan.
- [샌드박스](https://learn.chatgpt.com/docs/sandboxing): 운영체제별 집행 kaedah_mod, Linux의 bubblewrap 및 ruang_pengguna 네임스페이스 요구 사항.
- [공개 구성요소](https://learn.chatgpt.com/docs/open-source): CLI/SDK/app-server의 공개 sumber_pepohon 위치와 비공개 구성요소 pembatas_VALUE.

공식 문서에는 jkoros를 Sokongan_VALUE 대상으로 명시한 내용이 없다. 위 pelaksanaan LALUAN·개발 순서는
현재 소스와 요구 기능을 대조한 기술적 판단이다.
