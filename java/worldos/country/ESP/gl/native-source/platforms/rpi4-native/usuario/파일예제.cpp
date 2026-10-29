#include "파일규약.h"
#include "호출.h"
static int 초기화값;
static volatile int 초기화씨 = 72;
static volatile double flotante_p_fornecer = 1.25;
static int 소멸횟수;
struct 초기화시험 { 초기화시험() { 초기화값 = 초기화씨 + 1; } } 정적초기화;
class Automático_Ficheiro {
    int ÍNDICE;
public:
    explicit Automático_Ficheiro(const char *Nome) : ÍNDICE(abrir_Ficheiro(Nome, de_lectura_e_escrita | 없으면만들기 | 내용비우기, 0600)) {}
    ~Automático_Ficheiro() { if (ÍNDICE >= 0) peche_Ficheiro(ÍNDICE); 소멸횟수++; }
    int 서술자() const { return ÍNDICE; }
};
extern "C" int START_usuario_apl(int) {
    if (초기화값 != 73 || 사용자호출(0, 0, 0, 0, 0, 0, 0) != 1) return 1;
    double flotante_p_VALOR = flotante_p_fornecer * 2.0 + 0.5;
    if (사용자호출(0, 0, 0, 0, 0, 0, 0) != 1 || flotante_p_VALOR != 3.0) return 16;
    static const char Contido_VALOR[] = "EL0 C++ → posix-kor → Java Ficheiro · 안녕하세요 😀\n";
    char 읽은값[sizeof(Contido_VALOR)] = {};
    {
        Automático_Ficheiro Ficheiro("usuario.txt");
        int ÍNDICE = Ficheiro.서술자();
        if (ÍNDICE < 0 || escribir_Ficheiro_datos(ÍNDICE, Contido_VALOR, sizeof(Contido_VALOR)) != sizeof(Contido_VALOR)) return 2;
        if (buscar_Ficheiro(ÍNDICE, 0, 처음기준) || 파일자료읽기(ÍNDICE, 읽은값, sizeof(읽은값)) != sizeof(읽은값)) return 3;
        for (unsigned 순번 = 0; 순번 < sizeof(Contido_VALOR); 순번++) if (읽은값[순번] != Contido_VALOR[순번]) return 4;
    }
    if (소멸횟수 != 1) return 5;
    if (escribir_Ficheiro_datos(1, Contido_VALOR, sizeof(Contido_VALOR) - 1) != sizeof(Contido_VALOR) - 1) return 6;
    uintptr_t 바닥 = usuario_Memoria_finalizar(0);
    if (바닥 != 0x02c00000 || usuario_Memoria_finalizar(바닥 + 8192) != (intptr_t)(바닥 + 8192)) return 7;
    volatile unsigned char *Memoria_VALOR = (volatile unsigned char *)바닥;
    if (Memoria_VALOR[0] || Memoria_VALOR[8191]) return 8;
    Memoria_VALOR[8191] = 137;
    if (usuario_Memoria_finalizar(바닥) != (intptr_t)바닥 || usuario_Memoria_finalizar(바닥 + 8192) != (intptr_t)(바닥 + 8192) || Memoria_VALOR[8191]) return 9;
    // 잘못된 usuario punteiro/번호는 오류이며 커널을 중단하지 않는다.
    if (escribir_Ficheiro_datos(1, (const void *)0x80000, 8) != -1 || número_de_erro != 14) return 10;
    if (파일자료읽기(0, (void *)Contido_VALOR, 1) != -1 || número_de_erro != 14) return 11;
    if (사용자호출(999, 0, 0, 0, 0, 0, 0) != -38) return 12;
    intptr_t 화면폭 = 화면너비읽기(), 화면길이 = 화면높이읽기();
    if (화면폭 <= 0 || 화면길이 <= 0 || 사용자호출(13, 화면폭-1, 화면길이-1, 0, 2, 2, 0) != -22) return 13;
    if (화면사각형(470, 310, 80, 60, 0x40c050)) return 14;
    // 프로세스 saír_apl 시 열린 서술자가 자동 정리되어야 한다.
    if (abrir_Ficheiro("usuario.txt", só_de_lectura_VALOR) < 0) return 15;
    return 0;
}
