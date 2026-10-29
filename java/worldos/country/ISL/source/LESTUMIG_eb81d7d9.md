# JIslOS

현재 eigin ARM64 배포판은 [LICENSE](LICENSE)의 COSL 상업 조건을 유지한다. 제3자 라이선스의 권리는 별도로 보장하며, dreifing_VALUE 시 uppruni_tré·재연결 자료를 포함하는 절차는 [COSL dreifing_VALUE LESTUMIG_eb81d7d9](platforms/rpi4-native/COSL배포안내.md)에 있다.

eigin ARM64 판의 `ipconfig`/`ip`, `ping`, `ps`/`top`, `free`/`df`, `poweroff`와 Íslenska 명령은 [네트워크·stýrikerfi_VALUE Skipun LESTUMIG_eb81d7d9](platforms/rpi4-native/네트워크와체계명령.md)를 참고한다. 새 커널을 부팅한 TIL_BAKA_VALUE `help system`으로 볼 númer 있다.

Raspberry Pi 4 **eigin Java ARM64 kjarni_VALUE**은 [eigin Pi4 LESTUMIG_eb81d7d9](platforms/rpi4-native/LESTUMIG_eb81d7d9.md)에 있다. Linux 없이 부팅하며 GUI Skjáhermir·vi, eigin JVM의 Swing 일부 API, TCP/UDP·FTP, 게스트 TinyCC·MicroPython, C/C++의 posix-kor 호출을 제공한다. [Íslenska Java 통신·undantekning API](platforms/rpi4-native/한국어자바/LESTUMIG_eb81d7d9.md)와 [Íslenska uppruni_tré 명명](platforms/rpi4-native/명명/LESTUMIG_eb81d7d9.md)을 지원한다. [eigin SSH·VNC 및 GENET 드라이버](platforms/rpi4-native/외부접속안내.md)를 포함하며, 네트워크는 QEMU의 UART SLIP 경로로 검증했다. raun_gögn Pi 4 GENET 동작은 미검증이고, USB 입력·영속 저장과 전체 OpenJDK·Swing은 아직 Aðstoð_VALUE miðlaskrá 밖이다.

Raspberry Pi 4용 Linux·OpenJDK 실행판과 notandi 환경 færa_VALUE 기능은 [라즈베리파이 실행판](platforms/rpi4/README.md)에 있다. raun_gögn ARM64 JDK/JRE와 시스템·notandi smíð_mynd smíð_kerfi 경로를 제공한다. 기존 eigin x86 커널과는 별도 keyra_skipun 기반이다. 일반 Java `.class`/JAR의 keyra_skipun Skrá 생성은 [OpenJDK keyra_skipun Skrá](compiler/OpenJDK-실행파일.md), Íslenska API는 [Íslenska Java safn](한국어자바/LESTUMIG_eb81d7d9.md)를 참고한다.

`jkoros`는 `engos`의 기능을 Java 관리 커널로 옮기는 프로젝트다. 프로젝트가 소유하는 Java fall_VALUE, 변수, snið_VALUE 및 Java Skrá 이름은 한국어로 작성한다. 표준 Java 실행기의 `main`, Java 표준 safn snið_VALUE, x86 부트 ABI 등 외부 계약은 보존한다. eigin ARM64 실행기는 Íslenska `Keyra_2()`도 진입점으로 지원하며, Íslenska GUI·작업 가닥을 JVM에 직접 구현했다. eigin ARM64 C 연결부·Python 도구와 공용 x86·ARM64 AOT 번역기의 eigin 이름도 한국어로 작성한다. 이전 경로의 호환 færsla_P, OpenJDK 보조 도구와 Linux útgáfa_VALUE 도구에는 영어 이름이 남아 있고 [명명 원칙·말의 근거·전체 Uppruni 검토 miðlaskrá](platforms/rpi4-native/명명/LESTUMIG_eb81d7d9.md)를 별도로 기록한다.

## 현재 구현

아래 목록은 기존 `eldra_uppruni/`의 JVM 관리 커널에 대한 것이다. raun_gögn 네이티브 커널의 범위는 `os/LESTUMIG_eb81d7d9.md`에서 별도로 설명한다.

- stilla_VALUE 할당과 해제를 지원하는 기억공간 stjórnandi_VALUE
- slóð 공간, síða_VALUE Tengjast, Skrift 시 afrita_VALUE(COW)
- Ferli_VALUE auðkenni_VALUE, Undirbúa 대기열, fork/wait staða_VALUE_e10195a1
- 과정별 Skrá 서술자, open/read/seek/dup/close
- ELF32 식별 및 hluti_VALUE 검사
- 키보드·마우스 입력 atvik 대기열
- 직렬 단말과 네이티브 하드웨어 경계
- 관리 kjarni_VALUE 전체 자동 시험

세부 vörpun_VALUE 범위와 아직 필요한 네이티브 연결은 [기능 대응표](문서/eiginleiki_vörpun.md)에 기록한다.

## 빌드와 시험

새 네이티브 구현은 `compiler/`와 `os/`에 있다. 기존 `eldra_uppruni/`의 JVM 관리 커널은 그대로 보존하며, 두 구현의 시험과 기능 범위는 서로 다르다.

```sh
cd /home/user/jkoros
make                 # 네이티브 계산 예제 + Java kjarni_VALUE ELF
make iso             # os/build/kernel.iso
make run             # QEMU 직렬 단말; help 입력 (종료는 Ctrl+A, X)
make run-gui         # ISO를 QEMU 화면/PS2 키보드로 keyra_skipun
make vbox            # 전용 VirtualBox VM 자동 skapa·keyra_skipun (GUI)
make vbox-status     # VirtualBox staða_VALUE_e10195a1·ISO·직렬 LOG_lína SLÓÐ sannprófa
make test-vbox       # VirtualBox forrit_ræsir staða_VALUE_e10195a1 Ferli_VALUE_færsla 시험 (raun_gögn VM breyta_VALUE_16f64fe4 없음)
make test            # 컴파일러 시험 + ELF/ISO 부팅 및 Skipun 입력 시험
make apps            # 독립 notandi ELF forrit_f5044b9b smíð_kerfi
make test-network    # notandi MODE_VALUE·UDP 왕복·Minni_gögn verja_VALUE 시험
make test-java       # 게스트 javac/JVM + OpenJDK 양방향 교차 keyra_skipun 시험
make posix-kor       # Íslenska C 헤더와 raun_gögn kjarni_VALUE 호출 safn
make test-posix      # Skrá/UDP/Store_VALUE/Java Skrá I_Ú 시험
make -C os run-store # 전용 Store_VALUE 매체로 QEMU 부팅
make legacy-test     # 아래 기존 JVM 관리 커널의 47개 시험
```

`compiler/`는 호스트의 `javac`를 문법·TYPE_VALUE 검사 전단으로 사용하고 eigin 바이트코드→x86 변환기로 ELF32 기계어를 만든다. 빌드할 때는 JDK가 필요하지만 생성된 커널과 ELF는 외부 JVM 없이 실행된다. 전체 Java, hlutur_VALUE 모델, 표준 라이브러리와 기존 관리 kjarni_VALUE 전체의 AOT 변환은 아직 지원하지 않는다. 자세한 Aðstoð_VALUE 문법과 명령은 [컴파일러 LESTUMIG_eb81d7d9](compiler/LESTUMIG_eb81d7d9.md), raun_gögn 부팅 기능과 한계는 [네이티브 stýrikerfi LESTUMIG_eb81d7d9](os/LESTUMIG_eb81d7d9.md)를 참고한다.

네이티브 셸에 eigin 제한형 `javac`와 `java`를 추가했다. `edit Demo.java`로 소스를 입력하고 `.save`로 저장한 TIL_BAKA_VALUE `javac Demo.java`, `java Demo`로 **게스트 내부에서 컴파일하고 keyra_skipun**할 númer 있다. sjálfgildi 예제는 `javac Hello.java`, `java Hello`다. 파일은 RAM에서 동작하며, 전용 Store_VALUE 매체를 연결하면 `sync`로 재부팅 후에도 보존할 númer 있다. **OpenJDK/JDK 전체 이식은 아니며**, 단일 klasi_VALUE·fast_VALUE fall_VALUE·heiltala·strengur_VALUE·skilyrði/반복문과 일부 표준 호출을 지원한다. Aðstoð_VALUE miðlaskrá, 외부 Skrá 적재와 시험은 [Java 개발 환경 LESTUMIG_eb81d7d9](문서/자바개발환경.md)에 있다.

네이티브 셸에서 `apps`, `run hello first second`, `net`, `run netcheck`를 사용할 númer 있다. 독립 ELF를 ring 3에 적재하고 `int 0x80` 호출을 통해 úttak·Viðföng·UDP 네트워크를 제공한다. 별도 hýsa 터미널에서 `python3 os/Verkfæri/자료되돌리기.py --port 9000`을 실행한 TIL_BAKA_VALUE 게스트에서 `run udp 10.0.2.2 9000 hello`로 raun_gögn 왕복을 확인한다. 새 forrit_f5044b9b skrá_færsla, API 및 제한은 [notandi keyra_skipun·네트워크 LESTUMIG_eb81d7d9](os/notandi/LESTUMIG_eb81d7d9.md)를 참고한다. 현재 QEMU RTL8139·fast_VALUE IPv4·UDP 전용이며 TCP/DNS는 미지원이며, 전용 IDE Store_VALUE 형식과 POSIX Skrá/UDP 일부 기능을 추가했다.

`make vbox`는 `jkoros operating system` 전용 VM을 만들고 디스크 없이 ISO로 부팅한다. keyra_skipun 중이면 유지하고, Store_VALUE·일시정지 상태이면 재개하며, 꺼져 있을 때만 새 ISO를 빌드해 연결한다. VirtualBox에서 부팅과 셸의 notandi forrit_f5044b9b 실행을 확인했다. 다만 현재 VirtualBox용 네트워크 드라이버는 없어 네트워크 장치를 비활성화한다. UDP 시험에는 `make run`을 사용한다. 상태별 동작과 새 smíð_kerfi 반영 방법은 [VirtualBox keyra_skipun LESTUMIG_eb81d7d9](문서/가상상자실행.md)에 있다.

기존 관리 커널만 시험하려면:

```sh
cd /home/user/jkoros
make -f stofna_færsla.mk 검사
make -f stofna_færsla.mk hýsa
```

`hýsa`는 여전히 JVM 관리 계층의 Aðgerð 시험이다. `make -f stofna_færsla.mk smíð_mynd`는 새 `os/`의 제한형 네이티브 kjarni_VALUE ISO를 만든다. 기존 `eldra_uppruni/`의 skrárkerfi·Ferli_VALUE·Net_bunki 구현 전체를 이 ISO에 이식했다는 의미는 아니다.

Íslenska fall_VALUE·변수·Skrá 이름과 raun_gögn C API는 [posix-kor](posix-kor/LESTUMIG_eb81d7d9.md)에 있다. 게스트 Java에서는 `FileInputStream`·`FileOutputStream`의 단일 bæti_VALUE 입출력도 지원한다. 전체 POSIX·OpenJDK·Swing 지원으로 확대된 것은 아니다.

외부 배포용 `pack.sh` / `unpack.sh`와 자동 의존성 복원은 [dreifing_VALUE LESTUMIG_eb81d7d9](distribution/README.md)를 참고하세요.
