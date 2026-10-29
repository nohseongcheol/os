#include "파일규약.h"
#include "호출.h"
static int 초기화값;
static volatile int 초기화씨 = 72;
static volatile double 실수씨 = 1.25;
static int 소멸횟수;
struct 초기화시험 { 초기화시험() { 초기화값 = 초기화씨 + 1; } } 정적초기화;
class Imminiinnaaqtuq_ini {
    int nalunaiqsimavik;
public:
    explicit Imminiinnaaqtuq_ini(const char *atiq) : nalunaiqsimavik(matuirli_ini(atiq, uqalimaarli_titirarli | 없으면만들기 | 내용비우기, 0600)) {}
    ~Imminiinnaaqtuq_ini() { if (nalunaiqsimavik >= 0) matuli_ini(nalunaiqsimavik); 소멸횟수++; }
    int 서술자() const { return nalunaiqsimavik; }
};
extern "C" int pigiarli_atuqtuq_pilirijjut(int) {
    if (초기화값 != 73 || 사용자호출(0, 0, 0, 0, 0, 0, 0) != 1) return 1;
    double 실수 = 실수씨 * 2.0 + 0.5;
    if (사용자호출(0, 0, 0, 0, 0, 0, 0) != 1 || 실수 != 3.0) return 16;
    static const char Ilulingit_atuutilik[] = "EL0 C++ → posix-kor → Java ini · 안녕하세요 😀\n";
    char 읽은값[sizeof(Ilulingit_atuutilik)] = {};
    {
        Imminiinnaaqtuq_ini ini("atuqtuq.txt");
        int nalunaiqsimavik = ini.서술자();
        if (nalunaiqsimavik < 0 || titiraq_ini_titiqqat(nalunaiqsimavik, Ilulingit_atuutilik, sizeof(Ilulingit_atuutilik)) != sizeof(Ilulingit_atuutilik)) return 2;
        if (qinirli_ini(nalunaiqsimavik, 0, 처음기준) || 파일자료읽기(nalunaiqsimavik, 읽은값, sizeof(읽은값)) != sizeof(읽은값)) return 3;
        for (unsigned 순번 = 0; 순번 < sizeof(Ilulingit_atuutilik); 순번++) if (읽은값[순번] != Ilulingit_atuutilik[순번]) return 4;
    }
    if (소멸횟수 != 1) return 5;
    if (titiraq_ini_titiqqat(1, Ilulingit_atuutilik, sizeof(Ilulingit_atuutilik) - 1) != sizeof(Ilulingit_atuutilik) - 1) return 6;
    uintptr_t 바닥 = atuqtuq_puigujjaikkut_isulittuq(0);
    if (바닥 != 0x02c00000 || atuqtuq_puigujjaikkut_isulittuq(바닥 + 8192) != (intptr_t)(바닥 + 8192)) return 7;
    volatile unsigned char *puigujjaikkut_atuutilik = (volatile unsigned char *)바닥;
    if (puigujjaikkut_atuutilik[0] || puigujjaikkut_atuutilik[8191]) return 8;
    puigujjaikkut_atuutilik[8191] = 137;
    if (atuqtuq_puigujjaikkut_isulittuq(바닥) != (intptr_t)바닥 || atuqtuq_puigujjaikkut_isulittuq(바닥 + 8192) != (intptr_t)(바닥 + 8192) || puigujjaikkut_atuutilik[8191]) return 9;
    // 잘못된 atuqtuq 포인터/번호는 오류이며 커널을 중단하지 않는다.
    if (titiraq_ini_titiqqat(1, (const void *)0x80000, 8) != -1 || 오류번호 != 14) return 10;
    if (파일자료읽기(0, (void *)Ilulingit_atuutilik, 1) != -1 || 오류번호 != 14) return 11;
    if (사용자호출(999, 0, 0, 0, 0, 0, 0) != -38) return 12;
    intptr_t 화면폭 = 화면너비읽기(), 화면길이 = 화면높이읽기();
    if (화면폭 <= 0 || 화면길이 <= 0 || 사용자호출(13, 화면폭-1, 화면길이-1, 0, 2, 2, 0) != -22) return 13;
    if (화면사각형(470, 310, 80, 60, 0x40c050)) return 14;
    // 프로세스 taima_pilirijjut 시 열린 서술자가 자동 정리되어야 한다.
    if (matuirli_ini("atuqtuq.txt", takugatuinnaq_atuutilik) < 0) return 15;
    return 0;
}
