#include "파일규약.h"
#include "호출.h"
static int 초기화값;
static volatile int 초기화씨 = 72;
static volatile double 실수씨 = 1.25;
static int 소멸횟수;
struct 초기화시험 { 초기화시험() { 초기화값 = 초기화씨 + 1; } } 정적초기화;
class aládàáṣiṣẹ́_fáìlì {
    int wá_atọ̀ka_àkóónú;
public:
    explicit aládàáṣiṣẹ́_fáìlì(const char *Orúkọ) : wá_atọ̀ka_àkóónú(ṣí_fáìlì(Orúkọ, tí_a_lè_kà_tí_a_lè_kọ | 없으면만들기 | 내용비우기, 0600)) {}
    ~aládàáṣiṣẹ́_fáìlì() { if (wá_atọ̀ka_àkóónú >= 0) pa_dé_fáìlì(wá_atọ̀ka_àkóónú); 소멸횟수++; }
    int 서술자() const { return wá_atọ̀ka_àkóónú; }
};
extern "C" int bẹ̀rẹ̀_aṣàmúlò_àtòjọ_ètò(int) {
    if (초기화값 != 73 || 사용자호출(0, 0, 0, 0, 0, 0, 0) != 1) return 1;
    double 실수 = 실수씨 * 2.0 + 0.5;
    if (사용자호출(0, 0, 0, 0, 0, 0, 0) != 1 || 실수 != 3.0) return 16;
    static const char Àkóónú_iye[] = "EL0 C++ → posix-kor → Java Fáìlì · 안녕하세요 😀\n";
    char 읽은값[sizeof(Àkóónú_iye)] = {};
    {
        aládàáṣiṣẹ́_fáìlì Fáìlì("aṣàmúlò.txt");
        int wá_atọ̀ka_àkóónú = Fáìlì.서술자();
        if (wá_atọ̀ka_àkóónú < 0 || kọ_fáìlì_détà(wá_atọ̀ka_àkóónú, Àkóónú_iye, sizeof(Àkóónú_iye)) != sizeof(Àkóónú_iye)) return 2;
        if (ṣàwárí_fáìlì(wá_atọ̀ka_àkóónú, 0, 처음기준) || 파일자료읽기(wá_atọ̀ka_àkóónú, 읽은값, sizeof(읽은값)) != sizeof(읽은값)) return 3;
        for (unsigned 순번 = 0; 순번 < sizeof(Àkóónú_iye); 순번++) if (읽은값[순번] != Àkóónú_iye[순번]) return 4;
    }
    if (소멸횟수 != 1) return 5;
    if (kọ_fáìlì_détà(1, Àkóónú_iye, sizeof(Àkóónú_iye) - 1) != sizeof(Àkóónú_iye) - 1) return 6;
    uintptr_t 바닥 = aṣàmúlò_ibi_ìpamọ́_parí(0);
    if (바닥 != 0x02c00000 || aṣàmúlò_ibi_ìpamọ́_parí(바닥 + 8192) != (intptr_t)(바닥 + 8192)) return 7;
    volatile unsigned char *ibi_ìpamọ́_iye = (volatile unsigned char *)바닥;
    if (ibi_ìpamọ́_iye[0] || ibi_ìpamọ́_iye[8191]) return 8;
    ibi_ìpamọ́_iye[8191] = 137;
    if (aṣàmúlò_ibi_ìpamọ́_parí(바닥) != (intptr_t)바닥 || aṣàmúlò_ibi_ìpamọ́_parí(바닥 + 8192) != (intptr_t)(바닥 + 8192) || ibi_ìpamọ́_iye[8191]) return 9;
    // 잘못된 aṣàmúlò ìtọ́ka/번호는 오류이며 커널을 중단하지 않는다.
    if (kọ_fáìlì_détà(1, (const void *)0x80000, 8) != -1 || 오류번호 != 14) return 10;
    if (파일자료읽기(0, (void *)Àkóónú_iye, 1) != -1 || 오류번호 != 14) return 11;
    if (사용자호출(999, 0, 0, 0, 0, 0, 0) != -38) return 12;
    intptr_t 화면폭 = 화면너비읽기(), 화면길이 = 화면높이읽기();
    if (화면폭 <= 0 || 화면길이 <= 0 || 사용자호출(13, 화면폭-1, 화면길이-1, 0, 2, 2, 0) != -22) return 13;
    if (화면사각형(470, 310, 80, 60, 0x40c050)) return 14;
    // 프로세스 jáde_àtòjọ_ètò 시 열린 서술자가 자동 정리되어야 한다.
    if (ṣí_fáìlì("aṣàmúlò.txt", kàn_kàá_iye) < 0) return 15;
    return 0;
}
