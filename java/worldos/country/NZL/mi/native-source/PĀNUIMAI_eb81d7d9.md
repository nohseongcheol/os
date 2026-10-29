# JNzlOS

현재 자체 ARM64 배포판은 [LICENSE](LICENSE)의 COSL 상업 조건을 유지한다. 제3자 라이선스의 권리는 별도로 보장하며, 배포 시 pūtake_rākau·재연결 자료를 포함하는 절차는 [COSL 배포 PĀNUIMAI_eb81d7d9](platforms/rpi4-native/COSL배포안내.md)에 있다.

자체 ARM64 판의 `ipconfig`/`ip`, `ping`, `ps`/`top`, `free`/`df`, `poweroff`와 Reo_Māori 명령은 [네트워크·pūnaha_mahi_uara tono PĀNUIMAI_eb81d7d9](platforms/rpi4-native/네트워크와체계명령.md)를 참고한다. 새 커널을 부팅한 Hoki_uara `help system`으로 볼 수 있다.

Raspberry Pi 4 **자체 Java ARM64 kākano_uara_0611a8a8**은 [자체 Pi4 PĀNUIMAI_eb81d7d9](platforms/rpi4-native/PĀNUIMAI_eb81d7d9.md)에 있다. Linux 없이 부팅하며 GUI Tauranga·vi, 자체 JVM의 Swing 일부 API, TCP/UDP·FTP, 게스트 TinyCC·MicroPython, C/C++의 posix-kor 호출을 제공한다. [Reo_Māori Java 통신·예외 API](platforms/rpi4-native/한국어자바/PĀNUIMAI_eb81d7d9.md)와 [Reo_Māori pūtake_rākau 명명](platforms/rpi4-native/명명/PĀNUIMAI_eb81d7d9.md)을 지원한다. [자체 SSH·VNC 및 GENET 드라이버](platforms/rpi4-native/외부접속안내.md)를 포함하며, 네트워크는 QEMU의 UART SLIP 경로로 검증했다. tūturu_raraunga Pi 4 GENET 동작은 미검증이고, USB 입력·영속 저장과 전체 OpenJDK·Swing은 아직 Tautoko_uara topenga 밖이다.

Raspberry Pi 4용 Linux·OpenJDK 실행판과 kaiwhakamahi 환경 nuku_uara 기능은 [라즈베리파이 실행판](platforms/rpi4/README.md)에 있다. tūturu_raraunga ARM64 JDK/JRE와 시스템·kaiwhakamahi hanga_IMAGE hanga_pūnaha 경로를 제공한다. 기존 자체 x86 커널과는 별도 kawe_tono 기반이다. 일반 Java `.class`/JAR의 kawe_tono Kōnae 생성은 [OpenJDK kawe_tono Kōnae](compiler/OpenJDK-실행파일.md), Reo_Māori API는 [Reo_Māori Java puna](한국어자바/PĀNUIMAI_eb81d7d9.md)를 참고한다.

`jkoros`는 `engos`의 기능을 Java 관리 커널로 옮기는 프로젝트다. 프로젝트가 소유하는 Java TAUMAHI_uara, 변수, hōputu_uara 및 Java Kōnae 이름은 한국어로 작성한다. 표준 Java 실행기의 `main`, Java 표준 puna hōputu_uara, x86 부트 ABI 등 외부 계약은 보존한다. 자체 ARM64 실행기는 Reo_Māori `whakahaere()`도 진입점으로 지원하며, Reo_Māori GUI·작업 가닥을 JVM에 직접 구현했다. 자체 ARM64 C 연결부·Python 도구와 공용 x86·ARM64 AOT 번역기의 자체 이름도 한국어로 작성한다. 이전 경로의 호환 tāurunga_ira, OpenJDK 보조 도구와 Linux putanga_uara 도구에는 영어 이름이 남아 있고 [명명 원칙·말의 근거·전체 pūtake 검토 topenga](platforms/rpi4-native/명명/PĀNUIMAI_eb81d7d9.md)를 별도로 기록한다.

## 현재 구현

아래 목록은 기존 `tawhito_pūtake/`의 JVM 관리 커널에 대한 것이다. tūturu_raraunga 네이티브 커널의 범위는 `os/PĀNUIMAI_eb81d7d9.md`에서 별도로 설명한다.

- tiaro_uara 할당과 해제를 지원하는 기억공간 pouwhakahaere_uara
- ADDRESS 공간, whārangi_uara TŪHONO, Tuhia 시 tārua_uara(COW)
- Hātepe_uara pūtāutu_uara, Whakarite 대기열, fork/wait tūnga_uara
- 과정별 Kōnae 서술자, open/read/seek/dup/close
- ELF32 식별 및 wāhanga_uara 검사
- 키보드·마우스 입력 hui 대기열
- 직렬 단말과 네이티브 하드웨어 경계
- 관리 kākano_uara_0611a8a8 전체 자동 시험

세부 대응 범위와 아직 필요한 네이티브 연결은 [기능 대응표](문서/기능대응.md)에 기록한다.

## 빌드와 시험

새 네이티브 구현은 `compiler/`와 `os/`에 있다. 기존 `tawhito_pūtake/`의 JVM 관리 커널은 그대로 보존하며, 두 구현의 시험과 기능 범위는 서로 다르다.

```sh
cd /home/user/jkoros
make                 # 네이티브 계산 예제 + Java kākano_uara_0611a8a8 ELF
make iso             # os/build/kernel.iso
make run             # QEMU 직렬 단말; help 입력 (종료는 Ctrl+A, X)
make run-gui         # ISO를 QEMU 화면/PS2 키보드로 kawe_tono
make vbox            # 전용 VirtualBox VM 자동 waihanga·kawe_tono (GUI)
make vbox-status     # VirtualBox tūnga_uara·ISO·직렬 LOG_RECORD ara manatoko
make test-vbox       # VirtualBox kaupapa_pūwhiri_taupānga tūnga_uara Hātepe_uara_tāurunga 시험 (tūturu_raraunga VM huri_uara 없음)
make test            # 컴파일러 시험 + ELF/ISO 부팅 및 tono 입력 시험
make apps            # 독립 kaiwhakamahi ELF kaupapa_f5044b9b hanga_pūnaha
make test-network    # kaiwhakamahi MODE_uara·UDP 왕복·Pūmahara_raraunga pare_uara 시험
make test-java       # 게스트 javac/JVM + OpenJDK 양방향 교차 kawe_tono 시험
make posix-kor       # Reo_Māori C 헤더와 tūturu_raraunga kākano_uara_0611a8a8 호출 puna
make test-posix      # Kōnae/UDP/Store_uara/Java Kōnae I_O 시험
make -C os run-store # 전용 Store_uara 매체로 QEMU 부팅
make legacy-test     # 아래 기존 JVM 관리 커널의 47개 시험
```

`compiler/`는 호스트의 `javac`를 문법·TYPE_uara 검사 전단으로 사용하고 자체 바이트코드→x86 변환기로 ELF32 기계어를 만든다. 빌드할 때는 JDK가 필요하지만 생성된 커널과 ELF는 외부 JVM 없이 실행된다. 전체 Java, ahanoa_uara 모델, 표준 라이브러리와 기존 관리 kākano_uara_0611a8a8 전체의 AOT 변환은 아직 지원하지 않는다. 자세한 Tautoko_uara 문법과 명령은 [컴파일러 PĀNUIMAI_eb81d7d9](compiler/PĀNUIMAI_eb81d7d9.md), tūturu_raraunga 부팅 기능과 한계는 [네이티브 pūnaha_mahi PĀNUIMAI_eb81d7d9](os/PĀNUIMAI_eb81d7d9.md)를 참고한다.

네이티브 셸에 자체 제한형 `javac`와 `java`를 추가했다. `edit Demo.java`로 소스를 입력하고 `.save`로 저장한 Hoki_uara `javac Demo.java`, `java Demo`로 **게스트 내부에서 컴파일하고 kawe_tono**할 수 있다. uara_taunoa 예제는 `javac Hello.java`, `java Hello`다. 파일은 RAM에서 동작하며, 전용 Store_uara 매체를 연결하면 `sync`로 재부팅 후에도 보존할 수 있다. **OpenJDK/JDK 전체 이식은 아니며**, 단일 tauaha_uara·pateko_uara TAUMAHI_uara·tau_tōpū·aho_uara·here/반복문과 일부 표준 호출을 지원한다. Tautoko_uara topenga, 외부 Kōnae 적재와 시험은 [Java 개발 환경 PĀNUIMAI_eb81d7d9](문서/자바개발환경.md)에 있다.

네이티브 셸에서 `apps`, `run hello first second`, `net`, `run netcheck`를 사용할 수 있다. 독립 ELF를 ring 3에 적재하고 `int 0x80` 호출을 통해 출력·인수·UDP 네트워크를 제공한다. 별도 taurima 터미널에서 `python3 os/Ngā_Utauta/자료되돌리기.py --port 9000`을 실행한 Hoki_uara 게스트에서 `run udp 10.0.2.2 9000 hello`로 tūturu_raraunga 왕복을 확인한다. 새 kaupapa_f5044b9b rēhita_tāurunga, API 및 제한은 [kaiwhakamahi kawe_tono·네트워크 PĀNUIMAI_eb81d7d9](os/kaiwhakamahi/PĀNUIMAI_eb81d7d9.md)를 참고한다. 현재 QEMU RTL8139·pateko_uara IPv4·UDP 전용이며 TCP/DNS는 미지원이며, 전용 IDE Store_uara 형식과 POSIX Kōnae/UDP 일부 기능을 추가했다.

`make vbox`는 `jkoros operating system` 전용 VM을 만들고 디스크 없이 ISO로 부팅한다. kawe_tono 중이면 유지하고, Store_uara·일시정지 상태이면 재개하며, 꺼져 있을 때만 새 ISO를 빌드해 연결한다. VirtualBox에서 부팅과 셸의 kaiwhakamahi kaupapa_f5044b9b 실행을 확인했다. 다만 현재 VirtualBox용 네트워크 드라이버는 없어 네트워크 장치를 비활성화한다. UDP 시험에는 `make run`을 사용한다. 상태별 동작과 새 hanga_pūnaha 반영 방법은 [VirtualBox kawe_tono PĀNUIMAI_eb81d7d9](문서/가상상자실행.md)에 있다.

기존 관리 커널만 시험하려면:

```sh
cd /home/user/jkoros
make -f Waihanga_tāurunga.mk 검사
make -f Waihanga_tāurunga.mk taurima
```

`taurima`는 여전히 JVM 관리 계층의 hohenga 시험이다. `make -f Waihanga_tāurunga.mk hanga_IMAGE`는 새 `os/`의 제한형 네이티브 kākano_uara_0611a8a8 ISO를 만든다. 기존 `tawhito_pūtake/`의 pūnaha_kōnae·Hātepe_uara·whatunga_Huinga 구현 전체를 이 ISO에 이식했다는 의미는 아니다.

Reo_Māori TAUMAHI_uara·변수·Kōnae 이름과 tūturu_raraunga C API는 [posix-kor](posix-kor/PĀNUIMAI_eb81d7d9.md)에 있다. 게스트 Java에서는 `FileInputStream`·`FileOutputStream`의 단일 paita_uara 입출력도 지원한다. 전체 POSIX·OpenJDK·Swing 지원으로 확대된 것은 아니다.

외부 배포용 `pack.sh` / `unpack.sh`와 자동 의존성 복원은 [배포 PĀNUIMAI_eb81d7d9](distribution/README.md)를 참고하세요.
