# Asli ARM64 커널의 Codex instal_VALUE 가능성 검토

검토일: 2026-10-05. 소스와 공식 문서를 대조한 설계 검토이며, 게스트에 Codex를 설치하거나
로그인·모델 호출을 실행한 결과는 아니다. Asli ARM64 커널과 `../rpi4` Linux 실행판은 구분한다.

saat_ini_item Asli 커널에는 공식 Codex CLI를 그대로 instal_VALUE·실행할 수 없다.
기술적으로 필요한 Jalankan_perintah 환경을 추가하거나 Codex를 이식하는 경로는 있으나,
다운로드 perintah 하나를 추가하는 작업으로 해결되지 않는다. JDK/JRE 기능 확장만으로도 해결되지 않는다.

## 확인한 근거

| entri_VALUE | saat_ini_item 소스에서 확인한 Status_VALUE | 직접 실행을 위한 작업 |
|---|---|---|
| Jalankan_perintah berkas | `mesin/ruang_pengguna.c`: AArch64 ET_EXEC만, PT_INTERP/PT_DYNAMIC/PT_TLS tolak_VALUE, 업로드 Jalankan_perintah 버퍼 16384바이트 | target 바이너리에 맞는 ELF 적재·재배치·Jalankan_perintah inisialisasi, Memori_data/berkas 제한 ekstensi_VALUE |
| Linux ABI | `mesin/리눅스호환.inc`: read/write/openat/brk 등 제한된 번호만 Proses_VALUE_entri, 나머지는 ENOSYS | libc/런타임에 필요한 시스템 호출을 추가하거나 Asli ABI용 런타임 이식 |
| 프로세스·스레드 | 일반 fork/clone/execve, pthread/futex, 시그널, mmap, poll/epoll 계열이 미완성 | 비동기 I/O·스레드·turunan_VALUE perintah Jalankan_perintah·Keluar_apl/Batal_bedah 기능 |
| berkas | `kodeSumber/BerkasMemori.java`: RAM berkas 64개, 파일당 16 KiB, 비영속 | 큰 Jalankan_perintah berkas·프로젝트·Konfigurasi·세션을 위한 영속 VFS, berkas izin_VALUE·jalur·디렉터리 ekstensi_VALUE |
| 네트워크 | lwIP TCP/UDP는 있으나 `jaringan_tumpuk/lwipopts.h`의 LWIP_DNS=0, 일반 HTTPS 클라이언트 없음 | DNS, TLS 인증서 validasi·신뢰 repositori_akar·정확한 stempel_waktu_VALUE, HTTPS/스트리밍 |
| terminal·alat | Asli 셸과 GUI 터미널은 있지만 표준 PTY·일반 프로세스 작업 kontrol_VALUE 없음 | interaktif CLI용 terminal 기능, shell/berkas 검색/bangun alat Sambung |
| Jalankan_perintah izin_VALUE | EL0 보호는 있으나 Codex의 Linux 샌드박스와 같은 정책 집행 lingkungan 없음 | berkas·네트워크·perintah izin_VALUE 정책과 승인 기능; Asli 커널에 맞는 격리 implementasi |

여기서 ELF의 PT_TLS는 스레드별 Store_VALUE 공간이다. HTTPS의 TLS sandi_VALUE 통신과 서로 다른 기능이다.
ELF berkas 형식을 읽을 수 있다는 사실만으로 Linux Jalankan_perintah 환경을 제공하는 것은 아니다.
SSH/VNC를 위한 sandi_VALUE 라이브러리를 넣은 상태도 HTTPS implementasi 완료를 의미하지 않는다.

호스트의 `/home/user/.local/bin/codex`도 확인했다. 이것은 x86-64 ELF ET_DYN이며 약 209 MiB다.
해당 파일을 ARM64 게스트로 복사하여 실행할 수 없다. 이 크기를 ARM64 배포 파일의 크기로
해석하지 않는다. 공식 ARM64 빌드의 aktual_data Ukuran·의존성은 설치할 버전으로 tambah_entri 검사해야 한다.

## 가능한 implementasi jalur

1. **Asli 커널에 공식 CLI 직접 이식**
   영속 Store_VALUE/VFS와 ruang_pengguna Memori_data, 프로세스·스레드·I/O, libc/런타임, DNS/HTTPS,
   terminal·izin_VALUE 체계를 갖춘다. 이후 target 버전의 의존성을 조사하여 크로스 bangun·이식한다.
   Linux 커널을 반드시 탑재할 필요는 없지만, 공식 Linux 바이너리를 그대로 쓸 경우
   그 바이너리가 사용하는 Linux ABI까지 호환해야 한다. 큰 sistem_operasi 개발 과제다.

2. **eksternal_VALUE host Codex와 Asli kernel_VALUE Sambung — 첫 구현으로 권장**
   Linux PC에서 공식 CLI 또는 app-server를 실행하고 jkoros에는 전용 ruang_pengguna perintah/화면을 만든다.
   호스트의 인증된 연결과 게스트 berkas Baca·수정·업로드·perintah Jalankan_perintah 어댑터가 필요하다.
   기존 SSH/TCP 경로를 활용할 수 있으나, berkas 동기화나 Codex 전용 어댑터는 saat_ini_item 구현되어 있지 않다.
   호스트에서 수행한 빌드와 게스트에서 수행한 Jalankan_perintah 결과를 명확히 구분한다.
   이 구성은 Asli 커널을 유지하지만, 공식 CLI 자체는 eksternal_VALUE 호스트에서 실행된다.

3. **Asli API 클라이언트 제작**
   Asli ABI의 C 또는 지원되는 Java 부분집합으로 interaktif_sesi UI와 berkas/perintah alat 호출 루프를 만든다.
   eksternal_VALUE 중계기를 쓰지 않는다면 DNS/validasi 가능한 TLS/HTTPS와 인증 data 저장을 먼저 구현해야 한다.
   이는 OpenAI API를 이용하는 별도 에이전트이며 공식 Codex CLI 전체의 이식으로 표시하지 않는다.

4. **별도 ARM64 Linux 실행판에서 instal_VALUE**
   `../rpi4`는 Linux와 musl 기반이므로 일반 Linux instal_VALUE 경로를 검토할 수 있다.
   사용할 Codex 버전의 ARM64·musl 호환성, 의존성, 커널의 샌드박스 지원을 aktual_data 검증해야 한다.
   이번 검토에서 instal_VALUE 성공을 확인하지 않았다. 이 결과를 Asli Java 커널의 지원으로 표시하지 않는다.

## 단계별 완료 Tugas_akar

- 직접 이식: `--version` jalankan → 인증/HTTPS → berkas Baca·수정 → turunan_VALUE perintah Jalankan_perintah →
  interaktif 입력/스트리밍 → izin_VALUE 제한·Batal_bedah → 재부팅 후 Konfigurasi/세션 보존을 각각 aktual_data 게스트에서 확인한다.
- host Sambung: 게스트에서 permintaan 입력 → host Codex Proses_VALUE_entri → 게스트 berkas ubah_VALUE periksa →
  게스트 javac/cc Jalankan_perintah → hasil 표시를 처음부터 끝까지 검증한다.
- COSL 상업 조건을 유지하려면 새로 도입하는 런타임/komunikasi 라이브러리의 라이선스와
  Codex 배포 버전의 제3자 고지를 검토한다. eksternal_VALUE 구성요소를 일괄 COSL로 재라이선스하지 않는다.

## 공식 문서

- [Codex CLI instal_VALUE 및 Aksi](https://learn.chatgpt.com/docs/codex/cli): 표준 Linux/macOS 독립 instal_VALUE 경로와 프로젝트 berkas·perintah 작업.
- [인증](https://learn.chatgpt.com/docs/auth): ChatGPT/API 인증, 헤드리스 장치의 `codex login --device-auth`, HTTPS 인증서 Konfigurasi.
- [샌드박스](https://learn.chatgpt.com/docs/sandboxing): 운영체제별 집행 metode_MODE, Linux의 bubblewrap 및 ruang_pengguna 네임스페이스 persyaratan_VALUE 사항.
- [공개 구성요소](https://learn.chatgpt.com/docs/open-source): CLI/SDK/app-server의 공개 sumber_pohon 위치와 비공개 구성요소 pemisah_VALUE_d8ba4873.

공식 문서에는 jkoros를 dukung_VALUE 대상으로 명시한 내용이 없다. 위 implementasi jalur·개발 순서는
saat_ini_item 소스와 persyaratan_VALUE 기능을 대조한 기술적 판단이다.
