#include "파일규약.h"
#include "호출.h"
static int 초기화값;
static volatile int 초기화씨 = 72;
static volatile double 실수씨 = 1.25;
static int 소멸횟수;
struct 초기화시험 { 초기화시험() { 초기화값 = 초기화씨 + 1; } } 정적초기화;
class автоматски_датотека {
    int INDEX;
public:
    explicit автоматски_датотека(const char *Име) : INDEX(отвори_датотека(Име, чита_пишува | 없으면만들기 | 내용비우기, 0600)) {}
    ~автоматски_датотека() { if (INDEX >= 0) затвори_датотека(INDEX); 소멸횟수++; }
    int 서술자() const { return INDEX; }
};
extern "C" int Start_корисник_програма(int) {
    if (초기화값 != 73 || 사용자호출(0, 0, 0, 0, 0, 0, 0) != 1) return 1;
    double 실수 = 실수씨 * 2.0 + 0.5;
    if (사용자호출(0, 0, 0, 0, 0, 0, 0) != 1 || 실수 != 3.0) return 16;
    static const char Содржина_VALUE[] = "EL0 C++ → posix-kor → Java Датотека · 안녕하세요 😀\n";
    char 읽은값[sizeof(Содржина_VALUE)] = {};
    {
        автоматски_датотека Датотека("корисник.txt");
        int INDEX = Датотека.서술자();
        if (INDEX < 0 || запиши_датотека_податоци(INDEX, Содржина_VALUE, sizeof(Содржина_VALUE)) != sizeof(Содржина_VALUE)) return 2;
        if (пребарај_датотека(INDEX, 0, 처음기준) || 파일자료읽기(INDEX, 읽은값, sizeof(읽은값)) != sizeof(읽은값)) return 3;
        for (unsigned 순번 = 0; 순번 < sizeof(Содржина_VALUE); 순번++) if (읽은값[순번] != Содржина_VALUE[순번]) return 4;
    }
    if (소멸횟수 != 1) return 5;
    if (запиши_датотека_податоци(1, Содржина_VALUE, sizeof(Содржина_VALUE) - 1) != sizeof(Содржина_VALUE) - 1) return 6;
    uintptr_t 바닥 = корисник_Меморија_крај(0);
    if (바닥 != 0x02c00000 || корисник_Меморија_крај(바닥 + 8192) != (intptr_t)(바닥 + 8192)) return 7;
    volatile unsigned char *Меморија_VALUE = (volatile unsigned char *)바닥;
    if (Меморија_VALUE[0] || Меморија_VALUE[8191]) return 8;
    Меморија_VALUE[8191] = 137;
    if (корисник_Меморија_крај(바닥) != (intptr_t)바닥 || корисник_Меморија_крај(바닥 + 8192) != (intptr_t)(바닥 + 8192) || Меморија_VALUE[8191]) return 9;
    // 잘못된 корисник покажувач/번호는 오류이며 커널을 중단하지 않는다.
    if (запиши_датотека_податоци(1, (const void *)0x80000, 8) != -1 || 오류번호 != 14) return 10;
    if (파일자료읽기(0, (void *)Содржина_VALUE, 1) != -1 || 오류번호 != 14) return 11;
    if (사용자호출(999, 0, 0, 0, 0, 0, 0) != -38) return 12;
    intptr_t 화면폭 = 화면너비읽기(), 화면길이 = 화면높이읽기();
    if (화면폭 <= 0 || 화면길이 <= 0 || 사용자호출(13, 화면폭-1, 화면길이-1, 0, 2, 2, 0) != -22) return 13;
    if (화면사각형(470, 310, 80, 60, 0x40c050)) return 14;
    // 프로세스 Излез_програма 시 열린 서술자가 자동 정리되어야 한다.
    if (отвори_датотека("корисник.txt", само_за_читање_VALUE) < 0) return 15;
    return 0;
}
