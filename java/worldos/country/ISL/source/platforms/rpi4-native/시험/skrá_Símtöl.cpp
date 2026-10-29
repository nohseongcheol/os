#include "../명명/기계연결이름.h"
#include "파일규약.h"
// 표준 C++ safn 없는 freestanding C++11 forrit_f5044b9b. 커널에 fast_VALUE 링크한다.
extern "C" uintptr_t 시플플시험(void) {
    const char Efni_VALUE[] = "C++ → Java kjarni_VALUE · 한글 😀";
    unsigned char 읽은값[sizeof(Efni_VALUE)] = {};
    int Skrá = opið_skrá("시험.txt", les_skrifheimild | 없으면만들기 | 내용비우기, 0600);
    if (Skrá < 0) return 1;
    if (skrifa_skrá_gögn(Skrá, Efni_VALUE, sizeof(Efni_VALUE)) != sizeof(Efni_VALUE)) return 2;
    if (leita_skrá(Skrá, 0, 처음기준) != 0) return 3;
    if (파일자료읽기(Skrá, 읽은값, sizeof(읽은값)) != sizeof(읽은값)) return 4;
    for (size_t 순번 = 0; 순번 < sizeof(Efni_VALUE); 순번++) if (읽은값[순번] != (unsigned char)Efni_VALUE[순번]) return 5;
    if (파일자료읽기(Skrá, 읽은값, 1) != 0) return 6;
    if (파일저장확정(Skrá) != -1 || villa_númer != 38) return 7;
    if (loka_skrá(Skrá) || loka_skrá(Skrá) != -1 || villa_númer != 9) return 8;
    Skrá = opið_skrá("시험.txt", skrifvarið_VALUE);
    if (Skrá < 0 || skrifa_skrá_gögn(Skrá, Efni_VALUE, 1) != -1 || villa_númer != 9) return 9;
    if (loka_skrá(Skrá)) return 10;
    Skrá = opið_skrá("시험.txt", les_skrifheimild | 끝에이어쓰기);
    if (Skrá < 0 || leita_skrá(Skrá, 0, 처음기준) != 0 || skrifa_skrá_gögn(Skrá, "!", 1) != 1 || skrá_breyta_stærð(Skrá) != sizeof(Efni_VALUE) + 1) return 11;
    if (sett_skrá_lengd(Skrá, 2) || leita_skrá(Skrá, 4, 처음기준) != 4) return 12;
    // append는 매 write 때 EOF를 사용한다.
    if (skrifa_skrá_gögn(Skrá, "x", 1) != 1 || skrá_breyta_stærð(Skrá) != 3 || loka_skrá(Skrá)) return 13;
    Skrá = opið_skrá("구멍.bin", les_skrifheimild | 없으면만들기 | 내용비우기, 0600);
    if (Skrá < 0 || leita_skrá(Skrá, 3, 처음기준) != 3 || skrifa_skrá_gögn(Skrá, "z", 1) != 1) return 14;
    if (leita_skrá(Skrá, 0, 처음기준) != 0 || 파일자료읽기(Skrá, 읽은값, 4) != 4 || 읽은값[0] || 읽은값[1] || 읽은값[2] || 읽은값[3] != 'z') return 15;
    if (fjarlægja_skrá_færsla_heiti("구멍.bin") || skrá_breyta_stærð(Skrá) != 4 || loka_skrá(Skrá)) return 16;
    if (opið_skrá("구멍.bin", skrifvarið_VALUE) != -1 || villa_númer != 2) return 17;
    if (opið_skrá("시험.txt", les_skrifheimild | 새파일만들기, 0600) != -1 || villa_númer != 17) return 18;
    if (opið_skrá("../금지", skrifvarið_VALUE) != -1) return 19;
    return 0;
}
