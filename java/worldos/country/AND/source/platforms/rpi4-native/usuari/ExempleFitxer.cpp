#include "파일규약.h"
#include "호출.h"
static int 초기화값;
static volatile int 초기화씨 = 72;
static volatile double flotant_p_proveir = 1.25;
static int 소멸횟수;
struct 초기화시험 { 초기화시험() { 초기화값 = 초기화씨 + 1; } } 정적초기화;
class Automàtic_arxiu {
    int INDEX;
public:
    explicit Automàtic_arxiu(const char *Nom) : INDEX(crear_arxiu(Nom, lectura_escriptura | 없으면만들기 | 내용비우기, 0600)) {}
    ~Automàtic_arxiu() { if (INDEX >= 0) Tanca_arxiu(INDEX); 소멸횟수++; }
    int 서술자() const { return INDEX; }
};
extern "C" int Inici_usuari_programa(int) {
    if (초기화값 != 73 || 사용자호출(0, 0, 0, 0, 0, 0, 0) != 1) return 1;
    double flotant_p_VALOR = flotant_p_proveir * 2.0 + 0.5;
    if (사용자호출(0, 0, 0, 0, 0, 0, 0) != 1 || flotant_p_VALOR != 3.0) return 16;
    static const char contingut_VALOR[] = "EL0 C++ → posix-kor → Java Fitxer · 안녕하세요 😀\n";
    char tancar_VALOR[sizeof(contingut_VALOR)] = {};
    {
        Automàtic_arxiu Fitxer("usuari.txt");
        int INDEX = Fitxer.서술자();
        if (INDEX < 0 || escriure_arxiu_dades(INDEX, contingut_VALOR, sizeof(contingut_VALOR)) != sizeof(contingut_VALOR)) return 2;
        if (cercar_arxiu(INDEX, 0, 처음기준) || tancar_arxiu_dades(INDEX, tancar_VALOR, sizeof(tancar_VALOR)) != sizeof(tancar_VALOR)) return 3;
        for (unsigned 순번 = 0; 순번 < sizeof(contingut_VALOR); 순번++) if (tancar_VALOR[순번] != contingut_VALOR[순번]) return 4;
    }
    if (소멸횟수 != 1) return 5;
    if (escriure_arxiu_dades(1, contingut_VALOR, sizeof(contingut_VALOR) - 1) != sizeof(contingut_VALOR) - 1) return 6;
    uintptr_t 바닥 = usuari_Memòria_finalitzar(0);
    if (바닥 != 0x02c00000 || usuari_Memòria_finalitzar(바닥 + 8192) != (intptr_t)(바닥 + 8192)) return 7;
    volatile unsigned char *Memòria_VALOR = (volatile unsigned char *)바닥;
    if (Memòria_VALOR[0] || Memòria_VALOR[8191]) return 8;
    Memòria_VALOR[8191] = 137;
    if (usuari_Memòria_finalitzar(바닥) != (intptr_t)바닥 || usuari_Memòria_finalitzar(바닥 + 8192) != (intptr_t)(바닥 + 8192) || Memòria_VALOR[8191]) return 9;
    // 잘못된 usuari punter/번호는 오류이며 커널을 중단하지 않는다.
    if (escriure_arxiu_dades(1, (const void *)0x80000, 8) != -1 || número_d_error != 14) return 10;
    if (tancar_arxiu_dades(0, (void *)contingut_VALOR, 1) != -1 || número_d_error != 14) return 11;
    if (사용자호출(999, 0, 0, 0, 0, 0, 0) != -38) return 12;
    intptr_t 화면폭 = 화면너비읽기(), 화면길이 = 화면높이읽기();
    if (화면폭 <= 0 || 화면길이 <= 0 || 사용자호출(13, 화면폭-1, 화면길이-1, 0, 2, 2, 0) != -22) return 13;
    if (화면사각형(470, 310, 80, 60, 0x40c050)) return 14;
    // 프로세스 Surt_programa 시 열린 서술자가 자동 정리되어야 한다.
    if (crear_arxiu("usuari.txt", només_de_lectura_VALOR) < 0) return 15;
    return 0;
}
