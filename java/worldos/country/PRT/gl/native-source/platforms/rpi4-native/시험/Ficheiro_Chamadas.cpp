#include "../명명/기계연결이름.h"
#include "파일규약.h"
// 표준 C++ biblioteca 없는 freestanding C++11 apl_f5044b9b. 커널에 estático_VALOR 링크한다.
extern "C" uintptr_t 시플플시험(void) {
    const char Contido_VALOR[] = "C++ → Java kernel_VALOR · 한글 😀";
    unsigned char 읽은값[sizeof(Contido_VALOR)] = {};
    int Ficheiro = abrir_Ficheiro("시험.txt", de_lectura_e_escrita | 없으면만들기 | 내용비우기, 0600);
    if (Ficheiro < 0) return 1;
    if (escribir_Ficheiro_datos(Ficheiro, Contido_VALOR, sizeof(Contido_VALOR)) != sizeof(Contido_VALOR)) return 2;
    if (buscar_Ficheiro(Ficheiro, 0, 처음기준) != 0) return 3;
    if (파일자료읽기(Ficheiro, 읽은값, sizeof(읽은값)) != sizeof(읽은값)) return 4;
    for (size_t 순번 = 0; 순번 < sizeof(Contido_VALOR); 순번++) if (읽은값[순번] != (unsigned char)Contido_VALOR[순번]) return 5;
    if (파일자료읽기(Ficheiro, 읽은값, 1) != 0) return 6;
    if (파일저장확정(Ficheiro) != -1 || número_de_erro != 38) return 7;
    if (peche_Ficheiro(Ficheiro) || peche_Ficheiro(Ficheiro) != -1 || número_de_erro != 9) return 8;
    Ficheiro = abrir_Ficheiro("시험.txt", só_de_lectura_VALOR);
    if (Ficheiro < 0 || escribir_Ficheiro_datos(Ficheiro, Contido_VALOR, 1) != -1 || número_de_erro != 9) return 9;
    if (peche_Ficheiro(Ficheiro)) return 10;
    Ficheiro = abrir_Ficheiro("시험.txt", de_lectura_e_escrita | 끝에이어쓰기);
    if (Ficheiro < 0 || buscar_Ficheiro(Ficheiro, 0, 처음기준) != 0 || escribir_Ficheiro_datos(Ficheiro, "!", 1) != 1 || 파일크기(Ficheiro) != sizeof(Contido_VALOR) + 1) return 11;
    if (conxunto_Ficheiro_duración(Ficheiro, 2) || buscar_Ficheiro(Ficheiro, 4, 처음기준) != 4) return 12;
    // append는 매 write 때 EOF를 사용한다.
    if (escribir_Ficheiro_datos(Ficheiro, "x", 1) != 1 || 파일크기(Ficheiro) != 3 || peche_Ficheiro(Ficheiro)) return 13;
    Ficheiro = abrir_Ficheiro("구멍.bin", de_lectura_e_escrita | 없으면만들기 | 내용비우기, 0600);
    if (Ficheiro < 0 || buscar_Ficheiro(Ficheiro, 3, 처음기준) != 3 || escribir_Ficheiro_datos(Ficheiro, "z", 1) != 1) return 14;
    if (buscar_Ficheiro(Ficheiro, 0, 처음기준) != 0 || 파일자료읽기(Ficheiro, 읽은값, 4) != 4 || 읽은값[0] || 읽은값[1] || 읽은값[2] || 읽은값[3] != 'z') return 15;
    if (eliminar_Ficheiro_introdución_nome("구멍.bin") || 파일크기(Ficheiro) != 4 || peche_Ficheiro(Ficheiro)) return 16;
    if (abrir_Ficheiro("구멍.bin", só_de_lectura_VALOR) != -1 || número_de_erro != 2) return 17;
    if (abrir_Ficheiro("시험.txt", de_lectura_e_escrita | 새파일만들기, 0600) != -1 || número_de_erro != 17) return 18;
    if (abrir_Ficheiro("../금지", só_de_lectura_VALOR) != -1) return 19;
    return 0;
}
