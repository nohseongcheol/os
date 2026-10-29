#include "파일규약.h"
#include "호출.h"
static int 초기화값;
static volatile int 초기화씨 = 72;
static volatile double 실수씨 = 1.25;
static int 소멸횟수;
struct 초기화시험 { 초기화시험() { 초기화값 = 초기화씨 + 1; } } 정적초기화;
class ka_go_itirisa_faele {
    int tshupane;
public:
    explicit ka_go_itirisa_faele(const char *leina) : tshupane(bula_faele(leina, buisa_kwala | 없으면만들기 | 내용비우기, 0600)) {}
    ~ka_go_itirisa_faele() { if (tshupane >= 0) tswala_faele(tshupane); 소멸횟수++; }
    int 서술자() const { return tshupane; }
};
extern "C" int simolola_modirisi_Tiriso(int) {
    if (초기화값 != 73 || 사용자호출(0, 0, 0, 0, 0, 0, 0) != 1) return 1;
    double 실수 = 실수씨 * 2.0 + 0.5;
    if (사용자호출(0, 0, 0, 0, 0, 0, 0) != 1 || 실수 != 3.0) return 16;
    static const char Diteng_Boleng[] = "EL0 C++ → posix-kor → Java faele · 안녕하세요 😀\n";
    char 읽은값[sizeof(Diteng_Boleng)] = {};
    {
        ka_go_itirisa_faele faele("modirisi.txt");
        int tshupane = faele.서술자();
        if (tshupane < 0 || kwala_faele_tshedimosetso(tshupane, Diteng_Boleng, sizeof(Diteng_Boleng)) != sizeof(Diteng_Boleng)) return 2;
        if (batla_faele(tshupane, 0, 처음기준) || 파일자료읽기(tshupane, 읽은값, sizeof(읽은값)) != sizeof(읽은값)) return 3;
        for (unsigned 순번 = 0; 순번 < sizeof(Diteng_Boleng); 순번++) if (읽은값[순번] != Diteng_Boleng[순번]) return 4;
    }
    if (소멸횟수 != 1) return 5;
    if (kwala_faele_tshedimosetso(1, Diteng_Boleng, sizeof(Diteng_Boleng) - 1) != sizeof(Diteng_Boleng) - 1) return 6;
    uintptr_t 바닥 = modirisi_memori_kgaola(0);
    if (바닥 != 0x02c00000 || modirisi_memori_kgaola(바닥 + 8192) != (intptr_t)(바닥 + 8192)) return 7;
    volatile unsigned char *memori_Boleng = (volatile unsigned char *)바닥;
    if (memori_Boleng[0] || memori_Boleng[8191]) return 8;
    memori_Boleng[8191] = 137;
    if (modirisi_memori_kgaola(바닥) != (intptr_t)바닥 || modirisi_memori_kgaola(바닥 + 8192) != (intptr_t)(바닥 + 8192) || memori_Boleng[8191]) return 9;
    // 잘못된 modirisi sesupi/번호는 오류이며 커널을 중단하지 않는다.
    if (kwala_faele_tshedimosetso(1, (const void *)0x80000, 8) != -1 || 오류번호 != 14) return 10;
    if (파일자료읽기(0, (void *)Diteng_Boleng, 1) != -1 || 오류번호 != 14) return 11;
    if (사용자호출(999, 0, 0, 0, 0, 0, 0) != -38) return 12;
    intptr_t 화면폭 = 화면너비읽기(), 화면길이 = 화면높이읽기();
    if (화면폭 <= 0 || 화면길이 <= 0 || 사용자호출(13, 화면폭-1, 화면길이-1, 0, 2, 2, 0) != -22) return 13;
    if (화면사각형(470, 310, 80, 60, 0x40c050)) return 14;
    // 프로세스 tswaya_Tiriso 시 열린 서술자가 자동 정리되어야 한다.
    if (bula_faele("modirisi.txt", puiso_fela_Boleng) < 0) return 15;
    return 0;
}
