#include "파일규약.h"
class dok_Manajer {
    int INDEX;
public:
    dok_Manajer(const char *Nama_2) : INDEX(buat_file(Nama_2, baca_tulis | 없으면만들기 | 내용비우기, 0600)) {}
    ~dok_Manajer() { if (INDEX >= 0) Tutup_file(INDEX); }
    입출력결과형 Tulis(const char *data, byte_COUNT_TYPE Ukuran) { return tulis_file_data(INDEX, data, Ukuran); }
};
extern "C" int Mulai_pengguna_apl(int argumen) {
    (void)argumen;
    const char 인사말[] = "C++에서 한글 클래스와 posix-kor 호출\n";
    dok_Manajer 문서("C++인사.txt");
    tulis_file_data(1, 인사말, sizeof(인사말) - 1);
    return 문서.Tulis(인사말, sizeof(인사말) - 1) == sizeof(인사말) - 1 ? 0 : 1;
}
