#include "파일규약.h"
#include "호출.h"
static int 초기화값;
static volatile int 초기화씨 = 72;
static volatile double 실수씨 = 1.25;
static int 소멸횟수;
struct 초기화시험 { 초기화시험() { 초기화값 = 초기화씨 + 1; } } 정적초기화;
class 자동파일 {
    int 번호;
public:
    explicit 자동파일(const char *Anarana) : 번호(파일열기(Anarana, 읽고쓰기 | 없으면만들기 | 내용비우기, 0600)) {}
    ~자동파일() { if (번호 >= 0) 파일닫기(번호); 소멸횟수++; }
    int 서술자() const { return 번호; }
};
extern "C" int 사용자시작(int) {
    if (초기화값 != 73 || 사용자호출(0, 0, 0, 0, 0, 0, 0) != 1) return 1;
    double 실수 = 실수씨 * 2.0 + 0.5;
    if (사용자호출(0, 0, 0, 0, 0, 0, 0) != 1 || 실수 != 3.0) return 16;
    static const char 내용[] = "EL0 C++ → posix-kor → Java Rakitra · 안녕하세요 😀\n";
    char 읽은값[sizeof(내용)] = {};
    {
        자동파일 Rakitra("사용자.txt");
        int 번호 = Rakitra.서술자();
        if (번호 < 0 || 파일자료쓰기(번호, 내용, sizeof(내용)) != sizeof(내용)) return 2;
        if (파일위치옮기기(번호, 0, 처음기준) || 파일자료읽기(번호, 읽은값, sizeof(읽은값)) != sizeof(읽은값)) return 3;
        for (unsigned 순번 = 0; 순번 < sizeof(내용); 순번++) if (읽은값[순번] != 내용[순번]) return 4;
    }
    if (소멸횟수 != 1) return 5;
    if (파일자료쓰기(1, 내용, sizeof(내용) - 1) != sizeof(내용) - 1) return 6;
    uintptr_t 바닥 = 사용자기억끝(0);
    if (바닥 != 0x02c00000 || 사용자기억끝(바닥 + 8192) != (intptr_t)(바닥 + 8192)) return 7;
    volatile unsigned char *기억 = (volatile unsigned char *)바닥;
    if (기억[0] || 기억[8191]) return 8;
    기억[8191] = 137;
    if (사용자기억끝(바닥) != (intptr_t)바닥 || 사용자기억끝(바닥 + 8192) != (intptr_t)(바닥 + 8192) || 기억[8191]) return 9;
    // 잘못된 사용자 포인터/번호는 오류이며 커널을 중단하지 않는다.
    if (파일자료쓰기(1, (const void *)0x80000, 8) != -1 || 오류번호 != 14) return 10;
    if (파일자료읽기(0, (void *)내용, 1) != -1 || 오류번호 != 14) return 11;
    if (사용자호출(999, 0, 0, 0, 0, 0, 0) != -38) return 12;
    intptr_t 화면폭 = 화면너비읽기(), 화면길이 = 화면높이읽기();
    if (화면폭 <= 0 || 화면길이 <= 0 || 사용자호출(13, 화면폭-1, 화면길이-1, 0, 2, 2, 0) != -22) return 13;
    if (화면사각형(470, 310, 80, 60, 0x40c050)) return 14;
    // 프로세스 종료 시 열린 서술자가 자동 정리되어야 한다.
    if (파일열기("사용자.txt", 읽기전용) < 0) return 15;
    return 0;
}
