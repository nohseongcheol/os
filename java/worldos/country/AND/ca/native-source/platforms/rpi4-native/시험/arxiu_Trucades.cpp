#include "../명명/기계연결이름.h"
#include "파일규약.h"
// 표준 C++ biblioteca 없는 freestanding C++11 programa_f5044b9b. 커널에 estàtic_VALOR 링크한다.
extern "C" uintptr_t 시플플시험(void) {
    const char contingut_VALOR[] = "C++ → Java nucli_VALOR · 한글 😀";
    unsigned char tancar_VALOR[sizeof(contingut_VALOR)] = {};
    int Fitxer = crear_arxiu("시험.txt", lectura_escriptura | 없으면만들기 | 내용비우기, 0600);
    if (Fitxer < 0) return 1;
    if (escriure_arxiu_dades(Fitxer, contingut_VALOR, sizeof(contingut_VALOR)) != sizeof(contingut_VALOR)) return 2;
    if (cercar_arxiu(Fitxer, 0, 처음기준) != 0) return 3;
    if (tancar_arxiu_dades(Fitxer, tancar_VALOR, sizeof(tancar_VALOR)) != sizeof(tancar_VALOR)) return 4;
    for (size_t 순번 = 0; 순번 < sizeof(contingut_VALOR); 순번++) if (tancar_VALOR[순번] != (unsigned char)contingut_VALOR[순번]) return 5;
    if (tancar_arxiu_dades(Fitxer, tancar_VALOR, 1) != 0) return 6;
    if (파일저장확정(Fitxer) != -1 || número_d_error != 38) return 7;
    if (Tanca_arxiu(Fitxer) || Tanca_arxiu(Fitxer) != -1 || número_d_error != 9) return 8;
    Fitxer = crear_arxiu("시험.txt", només_de_lectura_VALOR);
    if (Fitxer < 0 || escriure_arxiu_dades(Fitxer, contingut_VALOR, 1) != -1 || número_d_error != 9) return 9;
    if (Tanca_arxiu(Fitxer)) return 10;
    Fitxer = crear_arxiu("시험.txt", lectura_escriptura | 끝에이어쓰기);
    if (Fitxer < 0 || cercar_arxiu(Fitxer, 0, 처음기준) != 0 || escriure_arxiu_dades(Fitxer, "!", 1) != 1 || arxiu_canviar_la_mida(Fitxer) != sizeof(contingut_VALOR) + 1) return 11;
    if (conjunt_arxiu_durada(Fitxer, 2) || cercar_arxiu(Fitxer, 4, 처음기준) != 4) return 12;
    // append는 매 write 때 EOF를 사용한다.
    if (escriure_arxiu_dades(Fitxer, "x", 1) != 1 || arxiu_canviar_la_mida(Fitxer) != 3 || Tanca_arxiu(Fitxer)) return 13;
    Fitxer = crear_arxiu("구멍.bin", lectura_escriptura | 없으면만들기 | 내용비우기, 0600);
    if (Fitxer < 0 || cercar_arxiu(Fitxer, 3, 처음기준) != 3 || escriure_arxiu_dades(Fitxer, "z", 1) != 1) return 14;
    if (cercar_arxiu(Fitxer, 0, 처음기준) != 0 || tancar_arxiu_dades(Fitxer, tancar_VALOR, 4) != 4 || tancar_VALOR[0] || tancar_VALOR[1] || tancar_VALOR[2] || tancar_VALOR[3] != 'z') return 15;
    if (suprimir_arxiu_introducció_nom("구멍.bin") || arxiu_canviar_la_mida(Fitxer) != 4 || Tanca_arxiu(Fitxer)) return 16;
    if (crear_arxiu("구멍.bin", només_de_lectura_VALOR) != -1 || número_d_error != 2) return 17;
    if (crear_arxiu("시험.txt", lectura_escriptura | 새파일만들기, 0600) != -1 || número_d_error != 17) return 18;
    if (crear_arxiu("../금지", només_de_lectura_VALOR) != -1) return 19;
    return 0;
}
