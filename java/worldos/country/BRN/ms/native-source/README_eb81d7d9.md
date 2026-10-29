# JBrnOS

현재 Asli ARM64 배포판은 [LICENSE](LICENSE)의 COSL 상업 조건을 유지한다. 제3자 라이선스의 권리는 별도로 보장하며, 배포 시 sumber_pepohon·재연결 자료를 포함하는 절차는 [COSL 배포 README_eb81d7d9](platforms/rpi4-native/COSL배포안내.md)에 있다.

Asli ARM64 판의 `ipconfig`/`ip`, `ping`, `ps`/`top`, `free`/`df`, `poweroff`와 Melayu 명령은 [네트워크·sistem_pengendalian_VALUE Perintah README_eb81d7d9](platforms/rpi4-native/네트워크와체계명령.md)를 참고한다. 새 커널을 부팅한 BACK_VALUE `help system`으로 볼 수 있다.

Raspberry Pi 4 **Asli Java ARM64 kernel_VALUE**은 [Asli Pi4 README_eb81d7d9](platforms/rpi4-native/README_eb81d7d9.md)에 있다. Linux 없이 부팅하며 GUI Terminal·vi, Asli JVM의 Swing 일부 API, TCP/UDP·FTP, 게스트 TinyCC·MicroPython, C/C++의 posix-kor 호출을 제공한다. [Melayu Java 통신·pengecualian API](platforms/rpi4-native/한국어자바/README_eb81d7d9.md)와 [Melayu sumber_pepohon 명명](platforms/rpi4-native/명명/README_eb81d7d9.md)을 지원한다. [Asli SSH·VNC 및 GENET 드라이버](platforms/rpi4-native/외부접속안내.md)를 포함하며, 네트워크는 QEMU의 UART SLIP 경로로 검증했다. sebenar_data Pi 4 GENET 동작은 미검증이고, USB 입력·영속 저장과 전체 OpenJDK·Swing은 아직 Sokongan_VALUE klip 밖이다.

Raspberry Pi 4용 Linux·OpenJDK 실행판과 ruang_pengguna persekitaran alih_VALUE 기능은 [라즈베리파이 실행판](platforms/rpi4/README.md)에 있다. sebenar_data ARM64 JDK/JRE와 시스템·ruang_pengguna bina_imej bina_sistem 경로를 제공한다. 기존 Asli x86 커널과는 별도 laksanakan_perintah 기반이다. 일반 Java `.class`/JAR의 laksanakan_perintah Fail 생성은 [OpenJDK laksanakan_perintah Fail](compiler/OpenJDK-fail_boleh_laku.md), Melayu API는 [Melayu Java pustaka](한국어자바/README_eb81d7d9.md)를 참고한다.

`jkoros`는 `engos`의 기능을 Java 관리 커널로 옮기는 프로젝트다. 프로젝트가 소유하는 Java fungsi_VALUE, pemboleh_ubah_VALUE, format_VALUE 및 Java Fail 이름은 한국어로 작성한다. 표준 Java 실행기의 `main`, Java 표준 pustaka format_VALUE, x86 부트 ABI 등 외부 계약은 보존한다. Asli ARM64 실행기는 Melayu `Jalan()`도 진입점으로 지원하며, Melayu GUI·작업 가닥을 JVM에 직접 구현했다. Asli ARM64 C 연결부·Python 도구와 공용 x86·ARM64 AOT 번역기의 Asli 이름도 한국어로 작성한다. 이전 경로의 호환 titik_permulaan, OpenJDK 보조 도구와 Linux versi_VALUE 도구에는 영어 이름이 남아 있고 [명명 원칙·말의 근거·전체 SUMBER 검토 klip](platforms/rpi4-native/명명/README_eb81d7d9.md)를 별도로 기록한다.

## 현재 pelaksanaan

아래 목록은 기존 `legasi_sumber/`의 JVM 관리 커널에 대한 것이다. sebenar_data 네이티브 커널의 범위는 `os/README_eb81d7d9.md`에서 별도로 설명한다.

- jajar_VALUE 할당과 해제를 지원하는 Memori_rantau pengurus_VALUE
- e_mel e_mel_rantau, halaman_VALUE Sambung, Tulis 시 tika_VALUE(COW)
- Proses_VALUE 식별자, Sediakan 대기열, fork/wait status_VALUE
- 과정별 Fail 서술자, open/read/seek/dup/close
- ELF32 식별 및 seksyen_VALUE 검사
- 키보드·마우스 입력 Peristiwa 대기열
- 직렬 단말과 네이티브 하드웨어 경계
- 관리 kernel_VALUE 전체 자동 ujian

세부 대응 범위와 아직 필요한 네이티브 연결은 [기능 대응표](문서/기능대응.md)에 기록한다.

## 빌드와 ujian

새 네이티브 구현은 `compiler/`와 `os/`에 있다. 기존 `legasi_sumber/`의 JVM 관리 커널은 그대로 보존하며, 두 구현의 시험과 기능 범위는 서로 다르다.

```sh
cd /home/user/jkoros
make                 # 네이티브 계산 예제 + Java kernel_VALUE ELF
make iso             # os/build/kernel.iso
make run             # QEMU 직렬 단말; help 입력 (종료는 Ctrl+A, X)
make run-gui         # ISO를 QEMU 화면/PS2 키보드로 laksanakan_perintah
make vbox            # 전용 VirtualBox VM 자동 jana·laksanakan_perintah (GUI)
make vbox-status     # VirtualBox status_VALUE·ISO·직렬 LOG_baris LALUAN tentu_sahkan
make test-vbox       # VirtualBox aplikasi_pelancar status_VALUE Proses_VALUE_pemasukan ujian (sebenar_data VM ubah_VALUE 없음)
make test            # 컴파일러 ujian + ELF/ISO permulaan_mesin 및 Perintah 입력 ujian
make apps            # 독립 ruang_pengguna ELF aplikasi_f5044b9b bina_sistem
make test-network    # ruang_pengguna mod_VALUE·UDP 왕복·Memori_data lindung_VALUE ujian
make test-java       # 게스트 javac/JVM + OpenJDK 양방향 교차 laksanakan_perintah ujian
make posix-kor       # Melayu C 헤더와 sebenar_data kernel_VALUE 호출 pustaka
make test-posix      # Fail/UDP/stor_VALUE/Java Fail I_O ujian
make -C os run-store # 전용 stor_VALUE 매체로 QEMU permulaan_mesin
make legacy-test     # 아래 기존 JVM 관리 커널의 47개 ujian
```

`compiler/`는 호스트의 `javac`를 문법·TYPE_VALUE 검사 전단으로 사용하고 Asli 바이트코드→x86 변환기로 ELF32 기계어를 만든다. 빌드할 때는 JDK가 필요하지만 생성된 커널과 ELF는 외부 JVM 없이 실행된다. 전체 Java, objek_VALUE 모델, 표준 라이브러리와 기존 관리 kernel_VALUE 전체의 AOT 변환은 아직 지원하지 않는다. 자세한 Sokongan_VALUE 문법과 명령은 [컴파일러 README_eb81d7d9](compiler/README_eb81d7d9.md), sebenar_data permulaan_mesin 기능과 한계는 [네이티브 sistem_pengendalian README_eb81d7d9](os/README_eb81d7d9.md)를 참고한다.

네이티브 셸에 Asli 제한형 `javac`와 `java`를 추가했다. `edit Demo.java`로 소스를 입력하고 `.save`로 저장한 BACK_VALUE `javac Demo.java`, `java Demo`로 **게스트 내부에서 컴파일하고 laksanakan_perintah**할 수 있다. nilai_lalai 예제는 `javac Hello.java`, `java Hello`다. 파일은 RAM에서 동작하며, 전용 stor_VALUE 매체를 연결하면 `sync`로 재부팅 후에도 보존할 수 있다. **OpenJDK/JDK 전체 이식은 아니며**, 단일 Kelas_VALUE·statik_VALUE fungsi_VALUE·integer·rentetan_VALUE·syarat/반복문과 일부 표준 호출을 지원한다. Sokongan_VALUE klip, 외부 Fail 적재와 시험은 [Java 개발 persekitaran README_eb81d7d9](문서/자바개발환경.md)에 있다.

네이티브 셸에서 `apps`, `run hello first second`, `net`, `run netcheck`를 사용할 수 있다. 독립 ELF를 ring 3에 적재하고 `int 0x80` 호출을 통해 출력·인수·UDP 네트워크를 제공한다. 별도 hos 터미널에서 `python3 os/alat/자료되돌리기.py --port 9000`을 실행한 BACK_VALUE 게스트에서 `run udp 10.0.2.2 9000 hello`로 sebenar_data 왕복을 확인한다. 새 aplikasi_f5044b9b daftar_pemasukan, API 및 제한은 [ruang_pengguna laksanakan_perintah·네트워크 README_eb81d7d9](os/ruang_pengguna/README_eb81d7d9.md)를 참고한다. 현재 QEMU RTL8139·statik_VALUE IPv4·UDP 전용이며 TCP/DNS는 미지원이며, 전용 IDE stor_VALUE 형식과 POSIX Fail/UDP 일부 기능을 추가했다.

`make vbox`는 `jkoros operating system` 전용 VM을 만들고 디스크 없이 ISO로 부팅한다. laksanakan_perintah 중이면 유지하고, stor_VALUE·일시정지 상태이면 재개하며, 꺼져 있을 때만 새 ISO를 빌드해 연결한다. VirtualBox에서 부팅과 셸의 ruang_pengguna aplikasi_f5044b9b 실행을 확인했다. 다만 현재 VirtualBox용 네트워크 드라이버는 없어 네트워크 장치를 비활성화한다. UDP 시험에는 `make run`을 사용한다. 상태별 동작과 새 bina_sistem 반영 방법은 [VirtualBox laksanakan_perintah README_eb81d7d9](문서/가상상자실행.md)에 있다.

기존 관리 커널만 시험하려면:

```sh
cd /home/user/jkoros
make -f cipta_pemasukan.mk 검사
make -f cipta_pemasukan.mk hos
```

`hos`는 여전히 JVM 관리 계층의 Aksi 시험이다. `make -f cipta_pemasukan.mk bina_imej`는 새 `os/`의 제한형 네이티브 kernel_VALUE ISO를 만든다. 기존 `legasi_sumber/`의 sistem_fail·Proses_VALUE·rangkaian_tindan pelaksanaan 전체를 이 ISO에 이식했다는 의미는 아니다.

Melayu fungsi_VALUE·pemboleh_ubah_VALUE·Fail 이름과 sebenar_data C API는 [posix-kor](posix-kor/README_eb81d7d9.md)에 있다. 게스트 Java에서는 `FileInputStream`·`FileOutputStream`의 단일 bait_VALUE 입출력도 지원한다. 전체 POSIX·OpenJDK·Swing 지원으로 확대된 것은 아니다.

외부 배포용 `pack.sh` / `unpack.sh`와 자동 의존성 복원은 [배포 README_eb81d7d9](distribution/README.md)를 참고하세요.
