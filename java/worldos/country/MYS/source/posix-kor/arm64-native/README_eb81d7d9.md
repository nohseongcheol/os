# Asli ARM64 Java 커널의 C/C++ Fail·루프백 Sambung

이 디렉터리는 `platforms/rpi4-native` Asli kernel_VALUE 전용이다. 기존 i386 `int 0x80` 라이브러리나 ARM64 Linux libc용 라이브러리가 아니다.

`pengisytiharan/파일규약.h`는 Melayu 함수명과 `extern "C"` ABI를 제공한다. `Sambung.c`는 kernel_VALUE 안에서 AOT Java Fail 메서드에 직접 연결하고, `pengguna_penghubung.c`는 독립 EL0 프로그램에서 SVC로 커널을 호출한다. sebenar_data Fail 처리는 `Memori_Fail.java`, 루프백 전문 처리는 `되돌림망.java`, 연결형 흐름은 `strim_rangkaian.java`에 있다.

```sh
make -C /home/user/jkoros/platforms/rpi4-native build
make -C /home/user/jkoros/platforms/rpi4-native test
```

산출물은 kernel_VALUE 내부용 `platforms/rpi4-native/build/libposix-kor-arm64.a`와 사용자용 `libposix-kor-user.a`다. 사용자용 라이브러리로 독립 ELF64 C/C++ 프로그램의 생성자·RAII·실수 operasi_VALUE·Fail·UDP 루프백 호출을 검증했다. 일반 Linux 바이너리, 전체 POSIX/libc/libstdc++ 지원을 뜻하지 않는다. 서로 다른 두 라이브러리를 혼합하지 않는다.

Sokongan_VALUE: `buka_fail`, `파일자료읽기`, `tulis_fail_data`, `Tutup_fail`, `cari_fail`, `alih_keluar_fail_pemasukan_nama`, `set_fail_kepanjangan`, 보조 fungsi_VALUE `saiz_fail`. RALAT 시 -1과 작업별 `오류번호`를 반환한다. `lakukan_storan_fail`은 RAM 파일이므로 ENOSYS를 반환한다. Fail 16개, 각 16384바이트, Nama 63바이트, 서술자 16개이며 RAM 디렉터리·rakan_VALUE/절대 경로를 제공한다. keizinan_VALUE/영속 저장은 없다.

사용자용 `pengisytiharan/통신규약.h`는 sebenar_data Melayu 함수와 독립 구조체를 선언한다.
`cipta_peserta`, `ikat_e_mel`, `자료전문보내기/받기`, `CONNECT_rangkaian/기다리기/받기`는
`pengguna_penghubung.c`에서 SVC를 호출하며 makro_VALUE 별칭이 아니다. `struct 인터넷통신주소`의
`e_mel_Keluarga`, `nombor_port`, `alamat_Internet.e_mel_VALUE`을 사용한다. 상수는 enum의
`awan_Keluarga`, `전문통신`, `전문전송규약`, `strim_rangkaian`, `strim_protokol_pengangkutan`이다.
Melayu·표준 구조체는 16바이트 ABI 배치를 공유하지만 서로 다른 C 자료형이다.
기존 pk_* 함수와 표준 구조체는 호환용으로 유지한다. 외부 통신은 Asli 커널의
lwIP TCP/UDP와 QEMU UART SLIP 연결을 사용한다. sebenar_data Pi 4 GENET 드라이버는 미지원이다.
소켓도 sebenar_data fungsi_VALUE `Tutup_fail`로 닫는다.

[사용법·seni_bina·한계](../../platforms/rpi4-native/README.md), [ruang_pengguna ABI](../../platforms/rpi4-native/USER-ABI.md), [EL0 C++ Fail 예제](../../platforms/rpi4-native/ruang_pengguna/ContohFail.cpp), [UDP 루프백 예제](../../platforms/rpi4-native/ruang_pengguna/통신예제.cpp), [기존 kernel_VALUE 내부 호출 ujian](../../platforms/rpi4-native/ujian/fail_Panggilan.cpp)을 참고한다.

C11/C++11의 한글 식별자·헤더 사용, SDK bina_sistem, ELF 업로드·laksanakan_perintah, RALAT/부분 I_O 처리는 [한글 개발 매뉴얼](../../platforms/rpi4-native/DEVELOPMENT-KO.md)에 정리했다. [C 연결형 통신 예제](../../platforms/rpi4-native/예제/한글코딩/strim_VALUE.c)도 제공한다.
