# JAlaOS

aktuellt_objekt eget ARM64 배포판은 [LICENSE](LICENSE)의 COSL 상업 조건을 유지한다. 제3자 라이선스의 권리는 별도로 보장하며, fördelning_värde 시 källa_träd·재연결 자료를 포함하는 절차는 [COSL fördelning_värde VIKTIGT_eb81d7d9](platforms/rpi4-native/COSL배포안내.md)에 있다.

eget ARM64 판의 `ipconfig`/`ip`, `ping`, `ps`/`top`, `free`/`df`, `poweroff`와 Svenska 명령은 [네트워크·operativsystem_värde kommando VIKTIGT_eb81d7d9](platforms/rpi4-native/네트워크와체계명령.md)를 참고한다. 새 커널을 부팅한 BACK_värde `help system`으로 볼 nummer 있다.

Raspberry Pi 4 **eget Java ARM64 kärna_värde**은 [eget Pi4 VIKTIGT_eb81d7d9](platforms/rpi4-native/VIKTIGT_eb81d7d9.md)에 있다. Linux 없이 부팅하며 GUI kommandotolk·vi, eget JVM의 Swing 일부 API, TCP/UDP·FTP, 게스트 TinyCC·MicroPython, C/C++의 posix-kor 호출을 제공한다. [Svenska Java kommunikation·fel_31f743d2 API](platforms/rpi4-native/한국어자바/VIKTIGT_eb81d7d9.md)와 [Svenska källa_träd 명명](platforms/rpi4-native/명명/VIKTIGT_eb81d7d9.md)을 지원한다. [eget SSH·VNC 및 GENET 드라이버](platforms/rpi4-native/extern_kontakt_guide.md)를 포함하며, 네트워크는 QEMU의 UART SLIP 경로로 검증했다. verklig_data Pi 4 GENET 동작은 미검증이고, USB indata_värde·영속 저장과 전체 OpenJDK·Swing은 아직 stöd_värde klipp 밖이다.

Raspberry Pi 4용 Linux·OpenJDK 실행판과 användarutrymme miljö flytta_värde 기능은 [라즈베리파이 실행판](platforms/rpi4/README.md)에 있다. verklig_data ARM64 JDK/JRE와 시스템·användarutrymme version_BILD version_System 경로를 제공한다. 기존 eget x86 커널과는 별도 köra_kommando 기반이다. 일반 Java `.class`/JAR의 köra_kommando filnamn 생성은 [OpenJDK köra_kommando filnamn](compiler/OpenJDK-körbar_fil_fil.md), Svenska API는 [Svenska Java bibliotek](한국어자바/VIKTIGT_eb81d7d9.md)를 참고한다.

`jkoros`는 `engos`의 기능을 Java 관리 커널로 옮기는 프로젝트다. 프로젝트가 소유하는 Java FUNKTION_värde, variabel_värde, format_värde 및 Java filnamn 이름은 한국어로 작성한다. 표준 Java 실행기의 `main`, Java 표준 bibliotek format_värde, x86 부트 ABI 등 extern_värde 계약은 보존한다. eget ARM64 실행기는 Svenska `Kör()`도 진입점으로 지원하며, Svenska GUI·작업 가닥을 JVM에 직접 구현했다. eget ARM64 C 연결부·Python 도구와 공용 x86·ARM64 AOT 번역기의 eget 이름도 한국어로 작성한다. Föregående_objekt 경로의 호환 startpunkt, OpenJDK 보조 도구와 Linux version_värde 도구에는 영어 이름이 남아 있고 [명명 원칙·말의 근거·전체 källfil 검토 klipp](platforms/rpi4-native/명명/VIKTIGT_eb81d7d9.md)를 별도로 기록한다.

## aktuellt_objekt implementation

아래 목록은 기존 `äldre_källa/`의 JVM 관리 커널에 대한 것이다. verklig_data 네이티브 커널의 범위는 `os/VIKTIGT_eb81d7d9.md`에서 별도로 설명한다.

- justera_värde 할당과 해제를 지원하는 Minne_område Ansvarig_värde
- Adress ADRESS_område, page_värde Anslut, Skriv 시 kopia_värde(COW)
- Process_värde identifierare_värde, Förbereda 대기열, fork/wait status_värde
- 과정별 filnamn 서술자, open/read/seek/dup/close
- ELF32 식별 및 avsnitt_värde 검사
- 키보드·마우스 indata_värde Händelse 대기열
- 직렬 단말과 네이티브 maskinvara_värde gräns_värde
- 관리 kärna_värde 전체 자동 tester

세부 mappning_värde 범위와 아직 필요한 네이티브 연결은 [기능 대응표](문서/funktion_mappning.md)에 기록한다.

## 빌드와 tester

새 네이티브 구현은 `compiler/`와 `os/`에 있다. 기존 `äldre_källa/`의 JVM 관리 커널은 그대로 보존하며, 두 구현의 시험과 기능 범위는 서로 다르다.

```sh
cd /home/user/jkoros
make                 # 네이티브 계산 예제 + Java kärna_värde ELF
make iso             # os/build/kernel.iso
make run             # QEMU 직렬 단말; help indata_värde (종료는 Ctrl+A, X)
make run-gui         # ISO를 QEMU skärmbild/PS2 키보드로 köra_kommando
make vbox            # 전용 VirtualBox VM 자동 generera·köra_kommando (GUI)
make vbox-status     # VirtualBox status_värde·ISO·직렬 LOG_POST sökväg_2 verifiera
make test-vbox       # VirtualBox app_Startbild status_värde Process_värde_post tester (verklig_data VM ändra_värde 없음)
make test            # kompilerare tester + ELF/ISO maskinstart 및 kommando indata_värde tester
make apps            # 독립 användarutrymme ELF app_f5044b9b version_System
make test-network    # användarutrymme läge_värde·UDP 왕복·Minne_data skydda_värde tester
make test-java       # 게스트 javac/JVM + OpenJDK 양방향 교차 köra_kommando tester
make posix-kor       # Svenska C 헤더와 verklig_data kärna_värde 호출 bibliotek
make test-posix      # filnamn/UDP/Store_värde/Java filnamn indata_utleverans tester
make -C os run-store # 전용 Store_värde 매체로 QEMU maskinstart
make legacy-test     # 아래 기존 JVM 관리 커널의 47개 tester
```

`compiler/`는 호스트의 `javac`를 문법·Typ_värde 검사 전단으로 사용하고 eget 바이트코드→x86 변환기로 ELF32 기계어를 만든다. 빌드할 때는 JDK가 필요하지만 생성된 커널과 ELF는 extern_värde JVM 없이 실행된다. 전체 Java, objekt_värde 모델, 표준 라이브러리와 기존 관리 kärna_värde 전체의 AOT 변환은 아직 지원하지 않는다. 자세한 stöd_värde 문법과 명령은 [kompilerare VIKTIGT_eb81d7d9](compiler/VIKTIGT_eb81d7d9.md), verklig_data maskinstart 기능과 한계는 [네이티브 operativsystem VIKTIGT_eb81d7d9](os/VIKTIGT_eb81d7d9.md)를 참고한다.

네이티브 셸에 eget 제한형 `javac`와 `java`를 추가했다. `edit Demo.java`로 소스를 입력하고 `.save`로 저장한 BACK_värde `javac Demo.java`, `java Demo`로 **게스트 내부에서 컴파일하고 köra_kommando**할 nummer 있다. standardvärde 예제는 `javac Hello.java`, `java Hello`다. 파일은 RAM에서 동작하며, 전용 Store_värde 매체를 연결하면 `sync`로 재부팅 후에도 보존할 nummer 있다. **OpenJDK/JDK 전체 이식은 아니며**, 단일 Kurs_värde·statisk_värde FUNKTION_värde·heltal·sträng_värde·villkor/반복문과 일부 표준 호출을 지원한다. stöd_värde klipp, extern_värde filnamn 적재와 시험은 [Java utveckling miljö VIKTIGT_eb81d7d9](문서/Java_IDE.md)에 있다.

네이티브 셸에서 `apps`, `run hello first second`, `net`, `run netcheck`를 사용할 nummer 있다. 독립 ELF를 ring 3에 적재하고 `int 0x80` 호출을 통해 utmatningsposition·argument·UDP 네트워크를 제공한다. 별도 värd 터미널에서 `python3 os/verktyg/UppdateraSkärm_data.py --port 9000`을 실행한 BACK_värde 게스트에서 `run udp 10.0.2.2 9000 hello`로 verklig_data 왕복을 확인한다. 새 app_f5044b9b register_post, API 및 제한은 [användarutrymme köra_kommando·네트워크 VIKTIGT_eb81d7d9](os/användarutrymme/VIKTIGT_eb81d7d9.md)를 참고한다. aktuellt_objekt QEMU RTL8139·statisk_värde IPv4·UDP 전용이며 TCP/DNS는 미지원이며, 전용 IDE Store_värde 형식과 POSIX filnamn/UDP 일부 기능을 추가했다.

`make vbox`는 `jkoros operating system` 전용 VM을 만들고 디스크 없이 ISO로 부팅한다. köra_kommando 중이면 유지하고, Store_värde·일시정지 상태이면 재개하며, 꺼져 있을 때만 새 ISO를 빌드해 연결한다. VirtualBox에서 부팅과 셸의 användarutrymme app_f5044b9b 실행을 확인했다. 다만 aktuellt_objekt VirtualBox용 네트워크 드라이버는 없어 네트워크 장치를 비활성화한다. UDP 시험에는 `make run`을 사용한다. 상태별 동작과 새 version_System 반영 방법은 [VirtualBox köra_kommando VIKTIGT_eb81d7d9](문서/가상상자실행.md)에 있다.

기존 관리 커널만 시험하려면:

```sh
cd /home/user/jkoros
make -f Skapa_post.mk 검사
make -f Skapa_post.mk värd
```

`värd`는 여전히 JVM 관리 계층의 Åtgärd 시험이다. `make -f Skapa_post.mk version_BILD`는 새 `os/`의 제한형 네이티브 kärna_värde ISO를 만든다. 기존 `äldre_källa/`의 filsystem·Process_värde·nätverk_Stack implementation 전체를 이 ISO에 이식했다는 의미는 아니다.

Svenska FUNKTION_värde·variabel_värde·filnamn 이름과 verklig_data C API는 [posix-kor](posix-kor/VIKTIGT_eb81d7d9.md)에 있다. 게스트 Java에서는 `FileInputStream`·`FileOutputStream`의 단일 byte_värde 입출력도 지원한다. 전체 POSIX·OpenJDK·Swing 지원으로 확대된 것은 아니다.

extern_värde 배포용 `pack.sh` / `unpack.sh`와 자동 의존성 복원은 [fördelning_värde VIKTIGT_eb81d7d9](distribution/README.md)를 참고하세요.
