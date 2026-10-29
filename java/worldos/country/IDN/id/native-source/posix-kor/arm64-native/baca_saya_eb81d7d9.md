# Asli ARM64 Java 커널의 C/C++ berkas·루프백 Sambung

이 디렉터리는 `platforms/rpi4-native` Asli kernel_VALUE 전용이다. 기존 i386 `int 0x80` 라이브러리나 ARM64 Linux libc용 라이브러리가 아니다.

`deklarasi/파일규약.h`는 Indonesia 함수명과 `extern "C"` ABI를 제공한다. `Sambung.c`는 kernel_VALUE 안에서 AOT Java berkas 메서드에 직접 연결하고, `pengguna_bridge.c`는 독립 EL0 프로그램에서 SVC로 커널을 호출한다. aktual_data berkas 처리는 `BerkasMemori.java`, 루프백 전문 처리는 `되돌림망.java`, 연결형 흐름은 `Stream_jaringan.java`에 있다.

```sh
make -C /home/user/jkoros/platforms/rpi4-native build
make -C /home/user/jkoros/platforms/rpi4-native test
```

산출물은 kernel_VALUE 내부용 `platforms/rpi4-native/build/libposix-kor-arm64.a`와 사용자용 `libposix-kor-user.a`다. 사용자용 라이브러리로 독립 ELF64 C/C++ 프로그램의 생성자·RAII·terapung_p_VALUE bedah_VALUE·berkas·UDP 루프백 호출을 검증했다. 일반 Linux 바이너리, 전체 POSIX/libc/libstdc++ 지원을 뜻하지 않는다. 서로 다른 두 라이브러리를 혼합하지 않는다.

dukung_VALUE: `buat_file`, `파일자료읽기`, `tulis_file_data`, `Tutup_file`, `cari_file`, `hapus_file_entri_nama`, `set_file_panjang`, 보조 fungsi_VALUE `ukuran_file`. galat 시 -1과 작업별 `nomor_kesalahan`를 반환한다. `penerapan_Files`은 RAM 파일이므로 ENOSYS를 반환한다. berkas 16개, 각 16384바이트, Nama_2 63바이트, 서술자 16개이며 RAM 디렉터리·serekan_VALUE/절대 경로를 제공한다. izin_VALUE/영속 저장은 없다.

사용자용 `deklarasi/통신규약.h`는 aktual_data Indonesia 함수와 독립 구조체를 선언한다.
`Buat_peserta`, `ikat_surel`, `자료전문보내기/terima`, `CONNECT_jaringan/기다리기/terima`는
`pengguna_bridge.c`에서 SVC를 호출하며 makro_VALUE 별칭이 아니다. `struct 인터넷통신주소`의
`surel_famili`, `nomor_port`, `Alamat_internet.surel_VALUE`을 사용한다. 상수는 enum의
`cloud_famili`, `전문통신`, `전문전송규약`, `Stream_jaringan`, `Stream_protokol_transportasi`이다.
Indonesia·표준 구조체는 16바이트 ABI 배치를 공유하지만 서로 다른 C 자료형이다.
기존 pk_* 함수와 표준 구조체는 호환용으로 유지한다. eksternal_VALUE 통신은 Asli 커널의
lwIP TCP/UDP와 QEMU UART SLIP 연결을 사용한다. aktual_data Pi 4 GENET 드라이버는 미지원이다.
소켓도 aktual_data fungsi_VALUE `Tutup_file`로 닫는다.

[사용법·arsitektur·한계](../../platforms/rpi4-native/README.md), [ruang_pengguna ABI](../../platforms/rpi4-native/USER-ABI.md), [EL0 C++ berkas 예제](../../platforms/rpi4-native/ruang_pengguna/ContohBerkas.cpp), [UDP 루프백 예제](../../platforms/rpi4-native/ruang_pengguna/통신예제.cpp), [기존 kernel_VALUE 내부 호출 pengujian](../../platforms/rpi4-native/pengujian/file_Panggilan.cpp)을 참고한다.

C11/C++11의 한글 pengidentifikasi_VALUE·헤더 gunakan_VALUE, SDK bangun, ELF 업로드·Jalankan_perintah, galat/부분 I_O 처리는 [한글 개발 매뉴얼](../../platforms/rpi4-native/DEVELOPMENT-KO.md)에 정리했다. [C 연결형 komunikasi 예제](../../platforms/rpi4-native/예제/한글코딩/Stream_VALUE.c)도 제공한다.
