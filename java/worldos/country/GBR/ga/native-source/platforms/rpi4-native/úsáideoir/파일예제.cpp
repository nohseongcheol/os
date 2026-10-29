#include "파일규약.h"
#include "호출.h"
static int 초기화값;
static volatile int 초기화씨 = 72;
static volatile double 실수씨 = 1.25;
static int 소멸횟수;
struct 초기화시험 { 초기화시험() { 초기화값 = 초기화씨 + 1; } } 정적초기화;
class uathoibríoch_comhad {
    int INDEX;
public:
    explicit uathoibríoch_comhad(const char *Ainm) : INDEX(oscail_comhad(Ainm, inléite_inscríofa | 없으면만들기 | 내용비우기, 0600)) {}
    ~uathoibríoch_comhad() { if (INDEX >= 0) dún_comhad(INDEX); 소멸횟수++; }
    int 서술자() const { return INDEX; }
};
extern "C" int Start_úsáideoir_clár(int) {
    if (초기화값 != 73 || 사용자호출(0, 0, 0, 0, 0, 0, 0) != 1) return 1;
    double 실수 = 실수씨 * 2.0 + 0.5;
    if (사용자호출(0, 0, 0, 0, 0, 0, 0) != 1 || 실수 != 3.0) return 16;
    static const char Inneachar_VALUE[] = "EL0 C++ → posix-kor → Java Comhad · 안녕하세요 😀\n";
    char 읽은값[sizeof(Inneachar_VALUE)] = {};
    {
        uathoibríoch_comhad Comhad("úsáideoir.txt");
        int INDEX = Comhad.서술자();
        if (INDEX < 0 || scríobh_comhad_sonraí(INDEX, Inneachar_VALUE, sizeof(Inneachar_VALUE)) != sizeof(Inneachar_VALUE)) return 2;
        if (lorg_comhad(INDEX, 0, 처음기준) || 파일자료읽기(INDEX, 읽은값, sizeof(읽은값)) != sizeof(읽은값)) return 3;
        for (unsigned 순번 = 0; 순번 < sizeof(Inneachar_VALUE); 순번++) if (읽은값[순번] != Inneachar_VALUE[순번]) return 4;
    }
    if (소멸횟수 != 1) return 5;
    if (scríobh_comhad_sonraí(1, Inneachar_VALUE, sizeof(Inneachar_VALUE) - 1) != sizeof(Inneachar_VALUE) - 1) return 6;
    uintptr_t 바닥 = úsáideoir_Cuimhne_cuir_deireadh_le(0);
    if (바닥 != 0x02c00000 || úsáideoir_Cuimhne_cuir_deireadh_le(바닥 + 8192) != (intptr_t)(바닥 + 8192)) return 7;
    volatile unsigned char *Cuimhne_VALUE = (volatile unsigned char *)바닥;
    if (Cuimhne_VALUE[0] || Cuimhne_VALUE[8191]) return 8;
    Cuimhne_VALUE[8191] = 137;
    if (úsáideoir_Cuimhne_cuir_deireadh_le(바닥) != (intptr_t)바닥 || úsáideoir_Cuimhne_cuir_deireadh_le(바닥 + 8192) != (intptr_t)(바닥 + 8192) || Cuimhne_VALUE[8191]) return 9;
    // 잘못된 úsáideoir pointeoir/번호는 오류이며 커널을 중단하지 않는다.
    if (scríobh_comhad_sonraí(1, (const void *)0x80000, 8) != -1 || 오류번호 != 14) return 10;
    if (파일자료읽기(0, (void *)Inneachar_VALUE, 1) != -1 || 오류번호 != 14) return 11;
    if (사용자호출(999, 0, 0, 0, 0, 0, 0) != -38) return 12;
    intptr_t 화면폭 = 화면너비읽기(), 화면길이 = 화면높이읽기();
    if (화면폭 <= 0 || 화면길이 <= 0 || 사용자호출(13, 화면폭-1, 화면길이-1, 0, 2, 2, 0) != -22) return 13;
    if (화면사각형(470, 310, 80, 60, 0x40c050)) return 14;
    // 프로세스 scoir_clár 시 열린 서술자가 자동 정리되어야 한다.
    if (oscail_comhad("úsáideoir.txt", inléite_amháin_VALUE) < 0) return 15;
    return 0;
}
