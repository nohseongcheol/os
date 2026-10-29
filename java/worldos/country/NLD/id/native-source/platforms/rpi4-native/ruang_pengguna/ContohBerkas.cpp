#include "파일규약.h"
#include "호출.h"
static int 초기화값;
static volatile int 초기화씨 = 72;
static volatile double terapung_p_seed = 1.25;
static int 소멸횟수;
struct 초기화시험 { 초기화시험() { 초기화값 = 초기화씨 + 1; } } 정적초기화;
class Otomatis_file {
    int INDEX;
public:
    explicit Otomatis_file(const char *Nama_2) : INDEX(buat_file(Nama_2, baca_tulis | 없으면만들기 | 내용비우기, 0600)) {}
    ~Otomatis_file() { if (INDEX >= 0) Tutup_file(INDEX); 소멸횟수++; }
    int 서술자() const { return INDEX; }
};
extern "C" int Mulai_pengguna_apl(int) {
    if (초기화값 != 73 || 사용자호출(0, 0, 0, 0, 0, 0, 0) != 1) return 1;
    double terapung_p_VALUE = terapung_p_seed * 2.0 + 0.5;
    if (사용자호출(0, 0, 0, 0, 0, 0, 0) != 1 || terapung_p_VALUE != 3.0) return 16;
    static const char Isi_VALUE[] = "EL0 C++ → posix-kor → Java berkas · 안녕하세요 😀\n";
    char 읽은값[sizeof(Isi_VALUE)] = {};
    {
        Otomatis_file berkas("ruang_pengguna.txt");
        int INDEX = berkas.서술자();
        if (INDEX < 0 || tulis_file_data(INDEX, Isi_VALUE, sizeof(Isi_VALUE)) != sizeof(Isi_VALUE)) return 2;
        if (cari_file(INDEX, 0, 처음기준) || 파일자료읽기(INDEX, 읽은값, sizeof(읽은값)) != sizeof(읽은값)) return 3;
        for (unsigned 순번 = 0; 순번 < sizeof(Isi_VALUE); 순번++) if (읽은값[순번] != Isi_VALUE[순번]) return 4;
    }
    if (소멸횟수 != 1) return 5;
    if (tulis_file_data(1, Isi_VALUE, sizeof(Isi_VALUE) - 1) != sizeof(Isi_VALUE) - 1) return 6;
    uintptr_t 바닥 = pengguna_Memori_mengakhiri(0);
    if (바닥 != 0x02c00000 || pengguna_Memori_mengakhiri(바닥 + 8192) != (intptr_t)(바닥 + 8192)) return 7;
    volatile unsigned char *Memori_VALUE = (volatile unsigned char *)바닥;
    if (Memori_VALUE[0] || Memori_VALUE[8191]) return 8;
    Memori_VALUE[8191] = 137;
    if (pengguna_Memori_mengakhiri(바닥) != (intptr_t)바닥 || pengguna_Memori_mengakhiri(바닥 + 8192) != (intptr_t)(바닥 + 8192) || Memori_VALUE[8191]) return 9;
    // 잘못된 ruang_pengguna pointer/번호는 오류이며 커널을 중단하지 않는다.
    if (tulis_file_data(1, (const void *)0x80000, 8) != -1 || nomor_kesalahan != 14) return 10;
    if (파일자료읽기(0, (void *)Isi_VALUE, 1) != -1 || nomor_kesalahan != 14) return 11;
    if (사용자호출(999, 0, 0, 0, 0, 0, 0) != -38) return 12;
    intptr_t 화면폭 = 화면너비읽기(), 화면길이 = 화면높이읽기();
    if (화면폭 <= 0 || 화면길이 <= 0 || 사용자호출(13, 화면폭-1, 화면길이-1, 0, 2, 2, 0) != -22) return 13;
    if (화면사각형(470, 310, 80, 60, 0x40c050)) return 14;
    // 프로세스 Keluar_apl 시 열린 서술자가 자동 정리되어야 한다.
    if (buat_file("ruang_pengguna.txt", baca_saja_VALUE) < 0) return 15;
    return 0;
}
