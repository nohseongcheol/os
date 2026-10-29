#include "파일규약.h"
#include "호출.h"
static int 초기화값;
static volatile int 초기화씨 = 72;
static volatile double 실수씨 = 1.25;
static int 소멸횟수;
struct 초기화시험 { 초기화시험() { 초기화값 = 초기화씨 + 1; } } 정적초기화;
class otomatiki_faili {
    int kielezo;
public:
    explicit otomatiki_faili(const char *Jina) : kielezo(unda_faili(Jina, soma_andika | 없으면만들기 | 내용비우기, 0600)) {}
    ~otomatiki_faili() { if (kielezo >= 0) funga_faili(kielezo); 소멸횟수++; }
    int 서술자() const { return kielezo; }
};
extern "C" int Anza_mtumiaji_programu(int) {
    if (초기화값 != 73 || 사용자호출(0, 0, 0, 0, 0, 0, 0) != 1) return 1;
    double 실수 = 실수씨 * 2.0 + 0.5;
    if (사용자호출(0, 0, 0, 0, 0, 0, 0) != 1 || 실수 != 3.0) return 16;
    static const char maudhui_thamani[] = "EL0 C++ → posix-kor → Java faili · 안녕하세요 😀\n";
    char 읽은값[sizeof(maudhui_thamani)] = {};
    {
        otomatiki_faili faili("mtumiaji.txt");
        int kielezo = faili.서술자();
        if (kielezo < 0 || andika_faili_data(kielezo, maudhui_thamani, sizeof(maudhui_thamani)) != sizeof(maudhui_thamani)) return 2;
        if (tafuta_faili(kielezo, 0, 처음기준) || 파일자료읽기(kielezo, 읽은값, sizeof(읽은값)) != sizeof(읽은값)) return 3;
        for (unsigned 순번 = 0; 순번 < sizeof(maudhui_thamani); 순번++) if (읽은값[순번] != maudhui_thamani[순번]) return 4;
    }
    if (소멸횟수 != 1) return 5;
    if (andika_faili_data(1, maudhui_thamani, sizeof(maudhui_thamani) - 1) != sizeof(maudhui_thamani) - 1) return 6;
    uintptr_t 바닥 = mtumiaji_kumbukumbu_tamatia(0);
    if (바닥 != 0x02c00000 || mtumiaji_kumbukumbu_tamatia(바닥 + 8192) != (intptr_t)(바닥 + 8192)) return 7;
    volatile unsigned char *kumbukumbu_thamani_603669bd = (volatile unsigned char *)바닥;
    if (kumbukumbu_thamani_603669bd[0] || kumbukumbu_thamani_603669bd[8191]) return 8;
    kumbukumbu_thamani_603669bd[8191] = 137;
    if (mtumiaji_kumbukumbu_tamatia(바닥) != (intptr_t)바닥 || mtumiaji_kumbukumbu_tamatia(바닥 + 8192) != (intptr_t)(바닥 + 8192) || kumbukumbu_thamani_603669bd[8191]) return 9;
    // 잘못된 mtumiaji kielekezi/번호는 오류이며 커널을 중단하지 않는다.
    if (andika_faili_data(1, (const void *)0x80000, 8) != -1 || 오류번호 != 14) return 10;
    if (파일자료읽기(0, (void *)maudhui_thamani, 1) != -1 || 오류번호 != 14) return 11;
    if (사용자호출(999, 0, 0, 0, 0, 0, 0) != -38) return 12;
    intptr_t 화면폭 = 화면너비읽기(), 화면길이 = 화면높이읽기();
    if (화면폭 <= 0 || 화면길이 <= 0 || 사용자호출(13, 화면폭-1, 화면길이-1, 0, 2, 2, 0) != -22) return 13;
    if (화면사각형(470, 310, 80, 60, 0x40c050)) return 14;
    // 프로세스 toka_programu 시 열린 서술자가 자동 정리되어야 한다.
    if (unda_faili("mtumiaji.txt", soma_tu_thamani) < 0) return 15;
    return 0;
}
