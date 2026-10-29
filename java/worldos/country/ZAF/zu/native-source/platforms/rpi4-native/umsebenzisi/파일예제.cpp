#include "파일규약.h"
#include "호출.h"
static int 초기화값;
static volatile int 초기화씨 = 72;
static volatile double 실수씨 = 1.25;
static int 소멸횟수;
struct 초기화시험 { 초기화시험() { 초기화값 = 초기화씨 + 1; } } 정적초기화;
class okuzenzelayo_ifayela {
    int thola_inkomba;
public:
    explicit okuzenzelayo_ifayela(const char *Igama) : thola_inkomba(vula_ifayela(Igama, fundeka_bhaleka | 없으면만들기 | 내용비우기, 0600)) {}
    ~okuzenzelayo_ifayela() { if (thola_inkomba >= 0) vala_ifayela(thola_inkomba); 소멸횟수++; }
    int 서술자() const { return thola_inkomba; }
};
extern "C" int qala_umsebenzisi_i_app(int) {
    if (초기화값 != 73 || 사용자호출(0, 0, 0, 0, 0, 0, 0) != 1) return 1;
    double 실수 = 실수씨 * 2.0 + 0.5;
    if (사용자호출(0, 0, 0, 0, 0, 0, 0) != 1 || 실수 != 3.0) return 16;
    static const char Okuqukethwe_inani[] = "EL0 C++ → posix-kor → Java Ihele · 안녕하세요 😀\n";
    char 읽은값[sizeof(Okuqukethwe_inani)] = {};
    {
        okuzenzelayo_ifayela Ihele("umsebenzisi.txt");
        int thola_inkomba = Ihele.서술자();
        if (thola_inkomba < 0 || bhala_ifayela_imininingwane(thola_inkomba, Okuqukethwe_inani, sizeof(Okuqukethwe_inani)) != sizeof(Okuqukethwe_inani)) return 2;
        if (cinga_ifayela(thola_inkomba, 0, 처음기준) || 파일자료읽기(thola_inkomba, 읽은값, sizeof(읽은값)) != sizeof(읽은값)) return 3;
        for (unsigned 순번 = 0; 순번 < sizeof(Okuqukethwe_inani); 순번++) if (읽은값[순번] != Okuqukethwe_inani[순번]) return 4;
    }
    if (소멸횟수 != 1) return 5;
    if (bhala_ifayela_imininingwane(1, Okuqukethwe_inani, sizeof(Okuqukethwe_inani) - 1) != sizeof(Okuqukethwe_inani) - 1) return 6;
    uintptr_t 바닥 = umsebenzisi_inkumbulo_yekisa(0);
    if (바닥 != 0x02c00000 || umsebenzisi_inkumbulo_yekisa(바닥 + 8192) != (intptr_t)(바닥 + 8192)) return 7;
    volatile unsigned char *inkumbulo_inani = (volatile unsigned char *)바닥;
    if (inkumbulo_inani[0] || inkumbulo_inani[8191]) return 8;
    inkumbulo_inani[8191] = 137;
    if (umsebenzisi_inkumbulo_yekisa(바닥) != (intptr_t)바닥 || umsebenzisi_inkumbulo_yekisa(바닥 + 8192) != (intptr_t)(바닥 + 8192) || inkumbulo_inani[8191]) return 9;
    // 잘못된 umsebenzisi isikhombi/번호는 오류이며 커널을 중단하지 않는다.
    if (bhala_ifayela_imininingwane(1, (const void *)0x80000, 8) != -1 || 오류번호 != 14) return 10;
    if (파일자료읽기(0, (void *)Okuqukethwe_inani, 1) != -1 || 오류번호 != 14) return 11;
    if (사용자호출(999, 0, 0, 0, 0, 0, 0) != -38) return 12;
    intptr_t 화면폭 = 화면너비읽기(), 화면길이 = 화면높이읽기();
    if (화면폭 <= 0 || 화면길이 <= 0 || 사용자호출(13, 화면폭-1, 화면길이-1, 0, 2, 2, 0) != -22) return 13;
    if (화면사각형(470, 310, 80, 60, 0x40c050)) return 14;
    // 프로세스 phuma_i_app 시 열린 서술자가 자동 정리되어야 한다.
    if (vula_ifayela("umsebenzisi.txt", fundwayo_kuphela_inani) < 0) return 15;
    return 0;
}
