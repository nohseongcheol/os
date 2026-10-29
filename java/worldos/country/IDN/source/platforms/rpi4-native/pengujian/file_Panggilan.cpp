#include "../명명/기계연결이름.h"
#include "파일규약.h"
// 표준 C++ pustaka 없는 freestanding C++11 apl_f5044b9b. 커널에 statik_VALUE 링크한다.
extern "C" uintptr_t 시플플시험(void) {
    const char Isi_VALUE[] = "C++ → Java kernel_VALUE · 한글 😀";
    unsigned char 읽은값[sizeof(Isi_VALUE)] = {};
    int berkas = buat_file("pengujian.txt", baca_tulis | 없으면만들기 | 내용비우기, 0600);
    if (berkas < 0) return 1;
    if (tulis_file_data(berkas, Isi_VALUE, sizeof(Isi_VALUE)) != sizeof(Isi_VALUE)) return 2;
    if (cari_file(berkas, 0, 처음기준) != 0) return 3;
    if (파일자료읽기(berkas, 읽은값, sizeof(읽은값)) != sizeof(읽은값)) return 4;
    for (size_t 순번 = 0; 순번 < sizeof(Isi_VALUE); 순번++) if (읽은값[순번] != (unsigned char)Isi_VALUE[순번]) return 5;
    if (파일자료읽기(berkas, 읽은값, 1) != 0) return 6;
    if (penerapan_Files(berkas) != -1 || nomor_kesalahan != 38) return 7;
    if (Tutup_file(berkas) || Tutup_file(berkas) != -1 || nomor_kesalahan != 9) return 8;
    berkas = buat_file("pengujian.txt", baca_saja_VALUE);
    if (berkas < 0 || tulis_file_data(berkas, Isi_VALUE, 1) != -1 || nomor_kesalahan != 9) return 9;
    if (Tutup_file(berkas)) return 10;
    berkas = buat_file("pengujian.txt", baca_tulis | 끝에이어쓰기);
    if (berkas < 0 || cari_file(berkas, 0, 처음기준) != 0 || tulis_file_data(berkas, "!", 1) != 1 || ukuran_file(berkas) != sizeof(Isi_VALUE) + 1) return 11;
    if (set_file_panjang(berkas, 2) || cari_file(berkas, 4, 처음기준) != 4) return 12;
    // append는 매 write 때 EOF를 사용한다.
    if (tulis_file_data(berkas, "x", 1) != 1 || ukuran_file(berkas) != 3 || Tutup_file(berkas)) return 13;
    berkas = buat_file("구멍.bin", baca_tulis | 없으면만들기 | 내용비우기, 0600);
    if (berkas < 0 || cari_file(berkas, 3, 처음기준) != 3 || tulis_file_data(berkas, "z", 1) != 1) return 14;
    if (cari_file(berkas, 0, 처음기준) != 0 || 파일자료읽기(berkas, 읽은값, 4) != 4 || 읽은값[0] || 읽은값[1] || 읽은값[2] || 읽은값[3] != 'z') return 15;
    if (hapus_file_entri_nama("구멍.bin") || ukuran_file(berkas) != 4 || Tutup_file(berkas)) return 16;
    if (buat_file("구멍.bin", baca_saja_VALUE) != -1 || nomor_kesalahan != 2) return 17;
    if (buat_file("pengujian.txt", baca_tulis | 새파일만들기, 0600) != -1 || nomor_kesalahan != 17) return 18;
    if (buat_file("../금지", baca_saja_VALUE) != -1) return 19;
    return 0;
}
