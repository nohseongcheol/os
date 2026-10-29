#include "파일규약.h"
#include "호출.h"
static int 초기화값;
static volatile int 초기화씨 = 72;
static volatile double 실수씨 = 1.25;
static int 소멸횟수;
struct 초기화시험 { 초기화시험() { 초기화값 = 초기화씨 + 1; } } 정적초기화;
class dox_biir_bara_denc {
    int àlluwa_tur;
public:
    explicit dox_biir_bara_denc(const char *tur_253d1510) : àlluwa_tur(sos_bara_denc(tur_253d1510, jàng_bind | 없으면만들기 | 내용비우기, 0600)) {}
    ~dox_biir_bara_denc() { if (àlluwa_tur >= 0) Tej_bara_denc(àlluwa_tur); 소멸횟수++; }
    int 서술자() const { return àlluwa_tur; }
};
extern "C" int Door_kiy_jariñoo_internet_jëfekaay(int) {
    if (초기화값 != 73 || 사용자호출(0, 0, 0, 0, 0, 0, 0) != 1) return 1;
    double 실수 = 실수씨 * 2.0 + 0.5;
    if (사용자호출(0, 0, 0, 0, 0, 0, 0) != 1 || 실수 != 3.0) return 16;
    static const char Këmb_xëyma[] = "EL0 C++ → posix-kor → Java bara_denc · 안녕하세요 😀\n";
    char 읽은값[sizeof(Këmb_xëyma)] = {};
    {
        dox_biir_bara_denc bara_denc("kiy_jariñoo_internet.txt");
        int àlluwa_tur = bara_denc.서술자();
        if (àlluwa_tur < 0 || biir_bara_denc_mbir(àlluwa_tur, Këmb_xëyma, sizeof(Këmb_xëyma)) != sizeof(Këmb_xëyma)) return 2;
        if (seet_bara_denc(àlluwa_tur, 0, 처음기준) || 파일자료읽기(àlluwa_tur, 읽은값, sizeof(읽은값)) != sizeof(읽은값)) return 3;
        for (unsigned 순번 = 0; 순번 < sizeof(Këmb_xëyma); 순번++) if (읽은값[순번] != Këmb_xëyma[순번]) return 4;
    }
    if (소멸횟수 != 1) return 5;
    if (biir_bara_denc_mbir(1, Këmb_xëyma, sizeof(Këmb_xëyma) - 1) != sizeof(Këmb_xëyma) - 1) return 6;
    uintptr_t 바닥 = kiy_jariñoo_internet_fatlekookaay_jeexal(0);
    if (바닥 != 0x02c00000 || kiy_jariñoo_internet_fatlekookaay_jeexal(바닥 + 8192) != (intptr_t)(바닥 + 8192)) return 7;
    volatile unsigned char *fatlekookaay_xëyma = (volatile unsigned char *)바닥;
    if (fatlekookaay_xëyma[0] || fatlekookaay_xëyma[8191]) return 8;
    fatlekookaay_xëyma[8191] = 137;
    if (kiy_jariñoo_internet_fatlekookaay_jeexal(바닥) != (intptr_t)바닥 || kiy_jariñoo_internet_fatlekookaay_jeexal(바닥 + 8192) != (intptr_t)(바닥 + 8192) || fatlekookaay_xëyma[8191]) return 9;
    // 잘못된 kiy_jariñoo_internet joxañukaay/번호는 오류이며 커널을 중단하지 않는다.
    if (biir_bara_denc_mbir(1, (const void *)0x80000, 8) != -1 || 오류번호 != 14) return 10;
    if (파일자료읽기(0, (void *)Këmb_xëyma, 1) != -1 || 오류번호 != 14) return 11;
    if (사용자호출(999, 0, 0, 0, 0, 0, 0) != -38) return 12;
    intptr_t 화면폭 = 화면너비읽기(), 화면길이 = 화면높이읽기();
    if (화면폭 <= 0 || 화면길이 <= 0 || 사용자호출(13, 화면폭-1, 화면길이-1, 0, 2, 2, 0) != -22) return 13;
    if (화면사각형(470, 310, 80, 60, 0x40c050)) return 14;
    // 프로세스 Génn_jëfekaay 시 열린 서술자가 자동 정리되어야 한다.
    if (sos_bara_denc("kiy_jariñoo_internet.txt", ngir_jaŋarek_la_xëyma) < 0) return 15;
    return 0;
}
