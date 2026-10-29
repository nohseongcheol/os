# JRouOS

aktuális_cikk saját ARM64 배포판은 [LICENSE](LICENSE)의 COSL 상업 조건을 유지한다. 제3자 라이선스의 권리는 별도로 보장하며, elosztás_ÉRTÉK 시 forrás_fa·재연결 자료를 포함하는 절차는 [COSL elosztás_ÉRTÉK fontos_fájl_eb81d7d9](platforms/rpi4-native/COSL배포안내.md)에 있다.

saját ARM64 판의 `ipconfig`/`ip`, `ping`, `ps`/`top`, `free`/`df`, `poweroff`와 magyar 명령은 [네트워크·operációs_rendszer_ÉRTÉK Parancs fontos_fájl_eb81d7d9](platforms/rpi4-native/네트워크와체계명령.md)를 참고한다. 새 커널을 부팅한 BACK_ÉRTÉK `help system`으로 볼 szám 있다.

Raspberry Pi 4 **saját Java ARM64 kernel_ÉRTÉK**은 [saját Pi4 fontos_fájl_eb81d7d9](platforms/rpi4-native/fontos_fájl_eb81d7d9.md)에 있다. Linux 없이 부팅하며 GUI Terminál·vi, saját JVM의 Swing 일부 API, TCP/UDP·FTP, 게스트 TinyCC·MicroPython, C/C++의 posix-kor 호출을 제공한다. [magyar Java kommunikáció·kivétel API](platforms/rpi4-native/한국어자바/fontos_fájl_eb81d7d9.md)와 [magyar forrás_fa 명명](platforms/rpi4-native/명명/fontos_fájl_eb81d7d9.md)을 지원한다. [saját SSH·VNC 및 GENET 드라이버](platforms/rpi4-native/külső_ismerős_útmutató.md)를 포함하며, 네트워크는 QEMU의 UART SLIP 경로로 검증했다. tényleges_adat Pi 4 GENET 동작은 미검증이고, USB bevitel_ÉRTÉK·영속 저장과 전체 OpenJDK·Swing은 아직 támogat_ÉRTÉK klip 밖이다.

Raspberry Pi 4용 Linux·OpenJDK 실행판과 felhasználó környezet_5d36e09c áthelyez_ÉRTÉK 기능은 [라즈베리파이 실행판](platforms/rpi4/README.md)에 있다. tényleges_adat ARM64 JDK/JRE와 시스템·felhasználó épít_KÉP épít_Rendszer 경로를 제공한다. 기존 saját x86 커널과는 별도 végrehajt_parancs 기반이다. 일반 Java `.class`/JAR의 végrehajt_parancs Fájl 생성은 [OpenJDK végrehajt_parancs Fájl](compiler/OpenJDK-végrehajtható_Fájl.md), magyar API는 [magyar Java kódtár](한국어자바/fontos_fájl_eb81d7d9.md)를 참고한다.

`jkoros`는 `engos`의 기능을 Java 관리 커널로 옮기는 프로젝트다. 프로젝트가 소유하는 Java FÜGGVÉNY_ÉRTÉK, változó_ÉRTÉK, formáz_ÉRTÉK 및 Java Fájl 이름은 한국어로 작성한다. 표준 Java 실행기의 `main`, Java 표준 kódtár formáz_ÉRTÉK, x86 부트 ABI 등 külső_ÉRTÉK 계약은 보존한다. saját ARM64 실행기는 magyar `Futtatás()`도 진입점으로 지원하며, magyar GUI·작업 가닥을 JVM에 직접 구현했다. saját ARM64 C 연결부·Python 도구와 공용 x86·ARM64 AOT 번역기의 saját 이름도 한국어로 작성한다. Előző_cikk 경로의 호환 belépési_pont, OpenJDK 보조 도구와 Linux verzió_ÉRTÉK 도구에는 영어 이름이 남아 있고 [명명 원칙·말의 근거·전체 FORRÁS 검토 klip](platforms/rpi4-native/명명/fontos_fájl_eb81d7d9.md)를 별도로 기록한다.

## aktuális_cikk 구현

아래 목록은 기존 `örökség_forrás/`의 JVM 관리 커널에 대한 것이다. tényleges_adat 네이티브 커널의 범위는 `os/fontos_fájl_eb81d7d9.md`에서 별도로 설명한다.

- igazít_ÉRTÉK 할당과 해제를 지원하는 Memória_régió kezelő_ÉRTÉK
- CÍM CÍM_régió, lap_ÉRTÉK Kapcsolódás, Írás 시 másol_ÉRTÉK(COW)
- folyamat_ÉRTÉK azonosító_ÉRTÉK, Előkészítés 대기열, fork/wait Állapot_ÉRTÉK
- 과정별 Fájl 서술자, open/read/seek/dup/close
- ELF32 식별 및 szakasz_ÉRTÉK 검사
- 키보드·마우스 bevitel_ÉRTÉK Esemény 대기열
- 직렬 단말과 네이티브 hardver_ÉRTÉK határ_ÉRTÉK
- 관리 kernel_ÉRTÉK 전체 자동 시험

세부 leképezés_ÉRTÉK 범위와 아직 필요한 네이티브 연결은 [기능 대응표](문서/funkció_leképezés.md)에 기록한다.

## 빌드와 시험

새 네이티브 구현은 `compiler/`와 `os/`에 있다. 기존 `örökség_forrás/`의 JVM 관리 커널은 그대로 보존하며, 두 구현의 시험과 기능 범위는 서로 다르다.

```sh
cd /home/user/jkoros
make                 # 네이티브 계산 예제 + Java kernel_ÉRTÉK ELF
make iso             # os/build/kernel.iso
make run             # QEMU 직렬 단말; help bevitel_ÉRTÉK (종료는 Ctrl+A, X)
make run-gui         # ISO를 QEMU 화면/PS2 키보드로 végrehajt_parancs
make vbox            # 전용 VirtualBox VM 자동 generálás·végrehajt_parancs (GUI)
make vbox-status     # VirtualBox Állapot_ÉRTÉK·ISO·직렬 LOG_REKORD ÚTVONAL igazol
make test-vbox       # VirtualBox app_indító Állapot_ÉRTÉK folyamat_ÉRTÉK_bejegyzés 시험 (tényleges_adat VM módosítás_ÉRTÉK 없음)
make test            # fordítóprogram 시험 + ELF/ISO 부팅 및 Parancs bevitel_ÉRTÉK 시험
make apps            # 독립 felhasználó ELF app_f5044b9b épít_Rendszer
make test-network    # felhasználó mód_ÉRTÉK·UDP 왕복·Memória_adat véd_ÉRTÉK 시험
make test-java       # 게스트 javac/JVM + OpenJDK 양방향 교차 végrehajt_parancs 시험
make posix-kor       # magyar C 헤더와 tényleges_adat kernel_ÉRTÉK 호출 kódtár
make test-posix      # Fájl/UDP/tár_ÉRTÉK/Java Fájl I_O 시험
make -C os run-store # 전용 tár_ÉRTÉK 매체로 QEMU 부팅
make legacy-test     # 아래 기존 JVM 관리 커널의 47개 시험
```

`compiler/`는 호스트의 `javac`를 문법·beír_ÉRTÉK 검사 전단으로 사용하고 saját 바이트코드→x86 변환기로 ELF32 기계어를 만든다. 빌드할 때는 JDK가 필요하지만 생성된 커널과 ELF는 külső_ÉRTÉK JVM 없이 실행된다. 전체 Java, objektum_ÉRTÉK 모델, 표준 라이브러리와 기존 관리 kernel_ÉRTÉK 전체의 AOT 변환은 아직 지원하지 않는다. 자세한 támogat_ÉRTÉK 문법과 명령은 [fordítóprogram fontos_fájl_eb81d7d9](compiler/fontos_fájl_eb81d7d9.md), tényleges_adat 부팅 기능과 한계는 [네이티브 operációs_rendszer fontos_fájl_eb81d7d9](os/fontos_fájl_eb81d7d9.md)를 참고한다.

네이티브 셸에 saját 제한형 `javac`와 `java`를 추가했다. `edit Demo.java`로 소스를 입력하고 `.save`로 저장한 BACK_ÉRTÉK `javac Demo.java`, `java Demo`로 **게스트 내부에서 컴파일하고 végrehajt_parancs**할 szám 있다. alapértelmezett_érték 예제는 `javac Hello.java`, `java Hello`다. 파일은 RAM에서 동작하며, 전용 tár_ÉRTÉK 매체를 연결하면 `sync`로 재부팅 후에도 보존할 szám 있다. **OpenJDK/JDK 전체 이식은 아니며**, 단일 tanóra_ÉRTÉK·statikus_ÉRTÉK FÜGGVÉNY_ÉRTÉK·egész_szám·sztring_ÉRTÉK·állapot/반복문과 일부 표준 호출을 지원한다. támogat_ÉRTÉK klip, külső_ÉRTÉK Fájl 적재와 시험은 [Java 개발 környezet_5d36e09c fontos_fájl_eb81d7d9](문서/Java_IDE.md)에 있다.

네이티브 셸에서 `apps`, `run hello first second`, `net`, `run netcheck`를 사용할 szám 있다. 독립 ELF를 ring 3에 적재하고 `int 0x80` 호출을 통해 Kimenet·Argumentumok·UDP 네트워크를 제공한다. 별도 gazda 터미널에서 `python3 os/Eszközök/visszhang_adat.py --port 9000`을 실행한 BACK_ÉRTÉK 게스트에서 `run udp 10.0.2.2 9000 hello`로 tényleges_adat 왕복을 확인한다. 새 app_f5044b9b jegyzék_bejegyzés, API 및 제한은 [felhasználó végrehajt_parancs·네트워크 fontos_fájl_eb81d7d9](os/felhasználó/fontos_fájl_eb81d7d9.md)를 참고한다. aktuális_cikk QEMU RTL8139·statikus_ÉRTÉK IPv4·UDP 전용이며 TCP/DNS는 미지원이며, 전용 IDE tár_ÉRTÉK 형식과 POSIX Fájl/UDP 일부 기능을 추가했다.

`make vbox`는 `jkoros operating system` 전용 VM을 만들고 디스크 없이 ISO로 부팅한다. végrehajt_parancs 중이면 유지하고, tár_ÉRTÉK·일시정지 상태이면 재개하며, 꺼져 있을 때만 새 ISO를 빌드해 연결한다. VirtualBox에서 부팅과 셸의 felhasználó app_f5044b9b 실행을 확인했다. 다만 aktuális_cikk VirtualBox용 네트워크 드라이버는 없어 네트워크 장치를 비활성화한다. UDP 시험에는 `make run`을 사용한다. 상태별 동작과 새 épít_Rendszer 반영 방법은 [VirtualBox végrehajt_parancs fontos_fájl_eb81d7d9](문서/가상상자실행.md)에 있다.

기존 관리 커널만 시험하려면:

```sh
cd /home/user/jkoros
make -f készít_bejegyzés.mk 검사
make -f készít_bejegyzés.mk gazda
```

`gazda`는 여전히 JVM 관리 계층의 Művelet 시험이다. `make -f készít_bejegyzés.mk épít_KÉP`는 새 `os/`의 제한형 네이티브 kernel_ÉRTÉK ISO를 만든다. 기존 `örökség_forrás/`의 fájlrendszer·folyamat_ÉRTÉK·hálózat_Sor 구현 전체를 이 ISO에 이식했다는 의미는 아니다.

magyar FÜGGVÉNY_ÉRTÉK·változó_ÉRTÉK·Fájl 이름과 tényleges_adat C API는 [posix-kor](posix-kor/fontos_fájl_eb81d7d9.md)에 있다. 게스트 Java에서는 `FileInputStream`·`FileOutputStream`의 단일 bájt_ÉRTÉK 입출력도 지원한다. 전체 POSIX·OpenJDK·Swing 지원으로 확대된 것은 아니다.

külső_ÉRTÉK 배포용 `pack.sh` / `unpack.sh`와 자동 의존성 복원은 [elosztás_ÉRTÉK fontos_fájl_eb81d7d9](distribution/README.md)를 참고하세요.
