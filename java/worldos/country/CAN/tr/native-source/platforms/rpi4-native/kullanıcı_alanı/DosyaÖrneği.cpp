#include "Dosya_ABI.h"
#include "호출.h"
static int başlatıcı_değer;
static volatile int başlatıcı_çekirdek_değer = 72;
static volatile double kayan_nokta_çekirdek_değer = 1.25;
static int 소멸횟수;
struct test_başlatma { test_başlatma() { başlatıcı_değer = başlatıcı_çekirdek_değer + 1; } } 정적초기화;
class Otomatik_Dosya {
    int Dizin;
public:
    explicit Otomatik_Dosya(const char *İsim) : Dizin(açık_Dosya(İsim, R_W | 없으면만들기 | kesmek_içindekiler, 0600)) {}
    ~Otomatik_Dosya() { if (Dizin >= 0) Kapat_Dosya(Dizin); 소멸횟수++; }
    int tanımlayıcı_girdi() const { return Dizin; }
};
extern "C" int Start_kullanıcı_program(int) {
    if (başlatıcı_değer != 73 || 사용자호출(0, 0, 0, 0, 0, 0, 0) != 1) return 1;
    double kayan_nokta_değer = kayan_nokta_çekirdek_değer * 2.0 + 0.5;
    if (사용자호출(0, 0, 0, 0, 0, 0, 0) != 1 || kayan_nokta_değer != 3.0) return 16;
    static const char içerik_değer[] = "EL0 C++ → posix-kor → Java dosya · 안녕하세요 😀\n";
    char 읽은값[sizeof(içerik_değer)] = {};
    {
        Otomatik_Dosya dosya("kullanıcı_alanı.txt");
        int Dizin = dosya.tanımlayıcı_girdi();
        if (Dizin < 0 || yazma_Dosya_veri(Dizin, içerik_değer, sizeof(içerik_değer)) != sizeof(içerik_değer)) return 2;
        if (arama_Dosya(Dizin, 0, 처음기준) || 파일자료읽기(Dizin, 읽은값, sizeof(읽은값)) != sizeof(읽은값)) return 3;
        for (unsigned 순번 = 0; 순번 < sizeof(içerik_değer); 순번++) if (읽은값[순번] != içerik_değer[순번]) return 4;
    }
    if (소멸횟수 != 1) return 5;
    if (yazma_Dosya_veri(1, içerik_değer, sizeof(içerik_değer) - 1) != sizeof(içerik_değer) - 1) return 6;
    uintptr_t 바닥 = kullanıcı_Bellek_Bitiş(0);
    if (바닥 != 0x02c00000 || kullanıcı_Bellek_Bitiş(바닥 + 8192) != (intptr_t)(바닥 + 8192)) return 7;
    volatile unsigned char *Bellek_değer = (volatile unsigned char *)바닥;
    if (Bellek_değer[0] || Bellek_değer[8191]) return 8;
    Bellek_değer[8191] = 137;
    if (kullanıcı_Bellek_Bitiş(바닥) != (intptr_t)바닥 || kullanıcı_Bellek_Bitiş(바닥 + 8192) != (intptr_t)(바닥 + 8192) || Bellek_değer[8191]) return 9;
    // 잘못된 kullanıcı_alanı işaretçi/번호는 오류이며 커널을 중단하지 않는다.
    if (yazma_Dosya_veri(1, (const void *)0x80000, 8) != -1 || hata_numarası != 14) return 10;
    if (파일자료읽기(0, (void *)içerik_değer, 1) != -1 || hata_numarası != 14) return 11;
    if (사용자호출(999, 0, 0, 0, 0, 0, 0) != -38) return 12;
    intptr_t 화면폭 = 화면너비읽기(), 화면길이 = 화면높이읽기();
    if (화면폭 <= 0 || 화면길이 <= 0 || 사용자호출(13, 화면폭-1, 화면길이-1, 0, 2, 2, 0) != -22) return 13;
    if (화면사각형(470, 310, 80, 60, 0x40c050)) return 14;
    // 프로세스 Çıkış_program 시 열린 서술자가 자동 정리되어야 한다.
    if (açık_Dosya("kullanıcı_alanı.txt", salt_okunur_değer) < 0) return 15;
    return 0;
}
