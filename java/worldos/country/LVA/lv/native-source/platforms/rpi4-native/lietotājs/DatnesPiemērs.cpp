#include "파일규약.h"
#include "호출.h"
static int 초기화값;
static volatile int 초기화씨 = 72;
static volatile double peldošs_p_dēstīt = 1.25;
static int 소멸횟수;
struct 초기화시험 { 초기화시험() { 초기화값 = 초기화씨 + 1; } } 정적초기화;
class Automātiski_Fails {
    int INDEX;
public:
    explicit Automātiski_Fails(const char *Nosaukums) : INDEX(atvērt_Fails(Nosaukums, 읽고쓰기 | 없으면만들기 | apraut_Satura_rādītājs, 0600)) {}
    ~Automātiski_Fails() { if (INDEX >= 0) Aizvērt_Fails(INDEX); 소멸횟수++; }
    int 서술자() const { return INDEX; }
};
extern "C" int Sākt_lietotājs_programma(int) {
    if (초기화값 != 73 || 사용자호출(0, 0, 0, 0, 0, 0, 0) != 1) return 1;
    double peldošs_p_VALUE = peldošs_p_dēstīt * 2.0 + 0.5;
    if (사용자호출(0, 0, 0, 0, 0, 0, 0) != 1 || peldošs_p_VALUE != 3.0) return 16;
    static const char Saturs_VALUE[] = "EL0 C++ → posix-kor → Java Fails · 안녕하세요 😀\n";
    char 읽은값[sizeof(Saturs_VALUE)] = {};
    {
        Automātiski_Fails Fails("lietotājs.txt");
        int INDEX = Fails.서술자();
        if (INDEX < 0 || rakstīšana_Fails_dati(INDEX, Saturs_VALUE, sizeof(Saturs_VALUE)) != sizeof(Saturs_VALUE)) return 2;
        if (meklēt_Fails(INDEX, 0, 처음기준) || 파일자료읽기(INDEX, 읽은값, sizeof(읽은값)) != sizeof(읽은값)) return 3;
        for (unsigned 순번 = 0; 순번 < sizeof(Saturs_VALUE); 순번++) if (읽은값[순번] != Saturs_VALUE[순번]) return 4;
    }
    if (소멸횟수 != 1) return 5;
    if (rakstīšana_Fails_dati(1, Saturs_VALUE, sizeof(Saturs_VALUE) - 1) != sizeof(Saturs_VALUE) - 1) return 6;
    uintptr_t 바닥 = lietotājs_atmiņa_beigt_zvanu(0);
    if (바닥 != 0x02c00000 || lietotājs_atmiņa_beigt_zvanu(바닥 + 8192) != (intptr_t)(바닥 + 8192)) return 7;
    volatile unsigned char *atmiņa_VALUE = (volatile unsigned char *)바닥;
    if (atmiņa_VALUE[0] || atmiņa_VALUE[8191]) return 8;
    atmiņa_VALUE[8191] = 137;
    if (lietotājs_atmiņa_beigt_zvanu(바닥) != (intptr_t)바닥 || lietotājs_atmiņa_beigt_zvanu(바닥 + 8192) != (intptr_t)(바닥 + 8192) || atmiņa_VALUE[8191]) return 9;
    // 잘못된 lietotājs rādītājs/번호는 오류이며 커널을 중단하지 않는다.
    if (rakstīšana_Fails_dati(1, (const void *)0x80000, 8) != -1 || kļūdas_numurs != 14) return 10;
    if (파일자료읽기(0, (void *)Saturs_VALUE, 1) != -1 || kļūdas_numurs != 14) return 11;
    if (사용자호출(999, 0, 0, 0, 0, 0, 0) != -38) return 12;
    intptr_t 화면폭 = 화면너비읽기(), 화면길이 = 화면높이읽기();
    if (화면폭 <= 0 || 화면길이 <= 0 || 사용자호출(13, 화면폭-1, 화면길이-1, 0, 2, 2, 0) != -22) return 13;
    if (화면사각형(470, 310, 80, 60, 0x40c050)) return 14;
    // 프로세스 Iziet_programma 시 열린 서술자가 자동 정리되어야 한다.
    if (atvērt_Fails("lietotājs.txt", tikai_lasāms_VALUE) < 0) return 15;
    return 0;
}
