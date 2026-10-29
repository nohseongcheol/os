#include "../명명/기계연결이름.h"
#include "파일규약.h"
// 표준 C++ pustaka 없는 freestanding C++11 aplikasi_f5044b9b. 커널에 statik_VALUE 링크한다.
extern "C" uintptr_t 시플플시험(void) {
    const char Kandungan_VALUE[] = "C++ → Java kernel_VALUE · 한글 😀";
    unsigned char 읽은값[sizeof(Kandungan_VALUE)] = {};
    int Fail = buka_fail("ujian.txt", baca_tulis | 없으면만들기 | potong_TOC, 0600);
    if (Fail < 0) return 1;
    if (tulis_fail_data(Fail, Kandungan_VALUE, sizeof(Kandungan_VALUE)) != sizeof(Kandungan_VALUE)) return 2;
    if (cari_fail(Fail, 0, 처음기준) != 0) return 3;
    if (파일자료읽기(Fail, 읽은값, sizeof(읽은값)) != sizeof(읽은값)) return 4;
    for (size_t 순번 = 0; 순번 < sizeof(Kandungan_VALUE); 순번++) if (읽은값[순번] != (unsigned char)Kandungan_VALUE[순번]) return 5;
    if (파일자료읽기(Fail, 읽은값, 1) != 0) return 6;
    if (lakukan_storan_fail(Fail) != -1 || 오류번호 != 38) return 7;
    if (Tutup_fail(Fail) || Tutup_fail(Fail) != -1 || 오류번호 != 9) return 8;
    Fail = buka_fail("ujian.txt", baca_sahaja_VALUE);
    if (Fail < 0 || tulis_fail_data(Fail, Kandungan_VALUE, 1) != -1 || 오류번호 != 9) return 9;
    if (Tutup_fail(Fail)) return 10;
    Fail = buka_fail("ujian.txt", baca_tulis | 끝에이어쓰기);
    if (Fail < 0 || cari_fail(Fail, 0, 처음기준) != 0 || tulis_fail_data(Fail, "!", 1) != 1 || saiz_fail(Fail) != sizeof(Kandungan_VALUE) + 1) return 11;
    if (set_fail_kepanjangan(Fail, 2) || cari_fail(Fail, 4, 처음기준) != 4) return 12;
    // append는 매 write 때 EOF를 사용한다.
    if (tulis_fail_data(Fail, "x", 1) != 1 || saiz_fail(Fail) != 3 || Tutup_fail(Fail)) return 13;
    Fail = buka_fail("구멍.bin", baca_tulis | 없으면만들기 | potong_TOC, 0600);
    if (Fail < 0 || cari_fail(Fail, 3, 처음기준) != 3 || tulis_fail_data(Fail, "z", 1) != 1) return 14;
    if (cari_fail(Fail, 0, 처음기준) != 0 || 파일자료읽기(Fail, 읽은값, 4) != 4 || 읽은값[0] || 읽은값[1] || 읽은값[2] || 읽은값[3] != 'z') return 15;
    if (alih_keluar_fail_pemasukan_nama("구멍.bin") || saiz_fail(Fail) != 4 || Tutup_fail(Fail)) return 16;
    if (buka_fail("구멍.bin", baca_sahaja_VALUE) != -1 || 오류번호 != 2) return 17;
    if (buka_fail("ujian.txt", baca_tulis | 새파일만들기, 0600) != -1 || 오류번호 != 17) return 18;
    if (buka_fail("../금지", baca_sahaja_VALUE) != -1) return 19;
    return 0;
}
