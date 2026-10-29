# własny ARM64 커널의 Codex instalować_WARTOŚĆ 가능성 검토

검토일: 2026-10-05. 소스와 공식 문서를 대조한 설계 검토이며, 게스트에 Codex를 설치하거나
로그인·모델 호출을 실행한 결과는 아니다. własny ARM64 커널과 `../rpi4` Linux 실행판은 구분한다.

bieżący_towar własny 커널에는 공식 Codex CLI를 그대로 instalować_WARTOŚĆ·실행할 identyfikator 없다.
기술적으로 필요한 Wykonaj_polecenie 환경을 추가하거나 Codex를 이식하는 경로는 있으나,
다운로드 polecenie 하나를 추가하는 작업으로 해결되지 않는다. JDK/JRE 기능 확장만으로도 해결되지 않는다.

## 확인한 근거

| wpis_WARTOŚĆ | bieżący_towar 소스에서 확인한 Stan_WARTOŚĆ | 직접 실행을 위한 작업 |
|---|---|---|
| Wykonaj_polecenie nazwa_pliku | `maszyna/przestrzeń_użytkownika.c`: AArch64 ET_EXEC만, PT_INTERP/PT_DYNAMIC/PT_TLS odrzucić_WARTOŚĆ, 업로드 Wykonaj_polecenie 버퍼 16384바이트 | wartość_docelowa 바이너리에 맞는 ELF 적재·재배치·Wykonaj_polecenie inicjuj, Pamięć_dane/nazwa_pliku 제한 rozszerzenie_WARTOŚĆ |
| Linux ABI | `maszyna/리눅스호환.inc`: read/write/openat/brk 등 제한된 번호만 Proces_WARTOŚĆ_wpis, 나머지는 ENOSYS | libc/런타임에 필요한 시스템 호출을 추가하거나 własny ABI용 런타임 이식 |
| 프로세스·스레드 | 일반 fork/clone/execve, pthread/futex, 시그널, mmap, poll/epoll 계열이 미완성 | 비동기 I/O·스레드·dziecko_WARTOŚĆ polecenie Wykonaj_polecenie·wyjść_program/Anuluj_zabieg 기능 |
| nazwa_pliku | `plik_źródłowy/Pamięć_Files.java`: RAM nazwa_pliku 64개, 파일당 16 KiB, 비영속 | 큰 Wykonaj_polecenie nazwa_pliku·프로젝트·Ustawienia·세션을 위한 영속 VFS, nazwa_pliku pozwolenie_WARTOŚĆ·ścieżka_2·디렉터리 rozszerzenie_WARTOŚĆ |
| 네트워크 | lwIP TCP/UDP는 있으나 `sieć_Stos/lwipopts.h`의 LWIP_DNS=0, 일반 HTTPS 클라이언트 없음 | DNS, TLS 인증서 walidować·신뢰 repozytorium_korzeń·정확한 znacznik_czasu_WARTOŚĆ, HTTPS/스트리밍 |
| interpretator_poleceń·narzędzia | własny 셸과 GUI 터미널은 있지만 표준 PTY·일반 프로세스 작업 kontrola_WARTOŚĆ 없음 | interakcyjny CLI용 interpretator_poleceń 기능, powłoka/nazwa_pliku 검색/BLD_System narzędzia Połącz |
| Wykonaj_polecenie pozwolenie_WARTOŚĆ | EL0 보호는 있으나 Codex의 Linux 샌드박스와 같은 정책 집행 środowisko 없음 | nazwa_pliku·네트워크·polecenie pozwolenie_WARTOŚĆ 정책과 승인 기능; własny 커널에 맞는 격리 implementacja |

여기서 ELF의 PT_TLS는 스레드별 Store_WARTOŚĆ 공간이다. HTTPS의 TLS hasło_WARTOŚĆ 통신과 서로 다른 기능이다.
ELF nazwa_pliku 형식을 읽을 identyfikator 있다는 사실만으로 Linux Wykonaj_polecenie 환경을 제공하는 것은 아니다.
SSH/VNC를 위한 hasło_WARTOŚĆ 라이브러리를 넣은 상태도 HTTPS implementacja 완료를 의미하지 않는다.

호스트의 `/home/user/.local/bin/codex`도 확인했다. 이것은 x86-64 ELF ET_DYN이며 약 209 MiB다.
해당 파일을 ARM64 게스트로 복사하여 실행할 identyfikator 없다. 이 크기를 ARM64 dystrybucja_WARTOŚĆ 파일의 크기로
해석하지 않는다. 공식 ARM64 빌드의 rzeczywisty_dane Rozmiar·의존성은 설치할 버전으로 dołączać_wpis 검사해야 한다.

## 가능한 implementacja ścieżka_2

1. **własny 커널에 공식 CLI 직접 이식**
   영속 Store_WARTOŚĆ/VFS와 przestrzeń_użytkownika Pamięć_dane, 프로세스·스레드·I/O, libc/런타임, DNS/HTTPS,
   interpretator_poleceń·pozwolenie_WARTOŚĆ 체계를 갖춘다. 이후 wartość_docelowa 버전의 의존성을 조사하여 크로스 BLD_System·이식한다.
   Linux 커널을 반드시 탑재할 필요는 없지만, 공식 Linux 바이너리를 그대로 쓸 경우
   그 바이너리가 사용하는 Linux ABI까지 호환해야 한다. 큰 system_operacyjny materiał_pochodny 과제다.

2. **zewnętrzny_WARTOŚĆ host Codex와 własny jądro_WARTOŚĆ Połącz — 첫 구현으로 권장**
   Linux PC에서 공식 CLI 또는 app-server를 실행하고 jkoros에는 전용 przestrzeń_użytkownika polecenie/화면을 만든다.
   호스트의 인증된 연결과 게스트 nazwa_pliku Odczyt·수정·업로드·polecenie Wykonaj_polecenie 어댑터가 필요하다.
   기존 SSH/TCP 경로를 활용할 identyfikator 있으나, nazwa_pliku 동기화나 Codex 전용 어댑터는 bieżący_towar 구현되어 있지 않다.
   호스트에서 수행한 빌드와 게스트에서 수행한 Wykonaj_polecenie 결과를 명확히 구분한다.
   이 구성은 własny 커널을 유지하지만, 공식 CLI 자체는 zewnętrzny_WARTOŚĆ 호스트에서 실행된다.

3. **własny API 클라이언트 제작**
   własny ABI의 C 또는 지원되는 Java 부분집합으로 interakcyjny_sesja UI와 nazwa_pliku/polecenie narzędzia 호출 루프를 만든다.
   zewnętrzny_WARTOŚĆ 중계기를 쓰지 않는다면 DNS/walidować 가능한 TLS/HTTPS와 인증 dane 저장을 먼저 구현해야 한다.
   이는 OpenAI API를 이용하는 별도 에이전트이며 공식 Codex CLI 전체의 이식으로 표시하지 않는다.

4. **별도 ARM64 Linux 실행판에서 instalować_WARTOŚĆ**
   `../rpi4`는 Linux와 musl 기반이므로 일반 Linux instalować_WARTOŚĆ 경로를 검토할 identyfikator 있다.
   사용할 Codex 버전의 ARM64·musl 호환성, 의존성, 커널의 샌드박스 지원을 rzeczywisty_dane 검증해야 한다.
   이번 검토에서 instalować_WARTOŚĆ 성공을 확인하지 않았다. 이 결과를 własny Java 커널의 지원으로 표시하지 않는다.

## 단계별 완료 Project_korzeń

- 직접 이식: `--version` Uruchom_2 → 인증/HTTPS → nazwa_pliku Odczyt·수정 → dziecko_WARTOŚĆ polecenie Wykonaj_polecenie →
  interakcyjny wejście_WARTOŚĆ/스트리밍 → pozwolenie_WARTOŚĆ 제한·Anuluj_zabieg → 재부팅 후 Ustawienia/세션 보존을 각각 rzeczywisty_dane 게스트에서 확인한다.
- host Połącz: 게스트에서 żądanie wejście_WARTOŚĆ → host Codex Proces_WARTOŚĆ_wpis → 게스트 nazwa_pliku zmienić_WARTOŚĆ 확인 →
  게스트 javac/cc Wykonaj_polecenie → WYNIK 표시를 처음부터 끝까지 검증한다.
- COSL 상업 조건을 유지하려면 새로 도입하는 런타임/komunikacja 라이브러리의 라이선스와
  Codex dystrybucja_WARTOŚĆ 버전의 제3자 고지를 검토한다. zewnętrzny_WARTOŚĆ 구성요소를 일괄 COSL로 재라이선스하지 않는다.

## 공식 문서

- [Codex CLI instalować_WARTOŚĆ 및 Akcja](https://learn.chatgpt.com/docs/codex/cli): 표준 Linux/macOS 독립 instalować_WARTOŚĆ 경로와 프로젝트 nazwa_pliku·polecenie 작업.
- [인증](https://learn.chatgpt.com/docs/auth): ChatGPT/API 인증, 헤드리스 장치의 `codex login --device-auth`, HTTPS 인증서 Ustawienia.
- [샌드박스](https://learn.chatgpt.com/docs/sandboxing): 운영체제별 집행 metoda_tryb, Linux의 bubblewrap 및 przestrzeń_użytkownika 네임스페이스 wymaganie_WARTOŚĆ 사항.
- [공개 구성요소](https://learn.chatgpt.com/docs/open-source): CLI/SDK/app-server의 공개 źródło_drzewo 위치와 비공개 구성요소 ogranicznik_WARTOŚĆ.

공식 문서에는 jkoros를 wsparcie_WARTOŚĆ 대상으로 명시한 내용이 없다. 위 implementacja ścieżka_2·materiał_pochodny 순서는
bieżący_towar 소스와 wymaganie_WARTOŚĆ 기능을 대조한 기술적 판단이다.
