#include "../명명/기계연결이름.h"
#include "파일규약.h"
// 표준 C++ biblioteka 없는 freestanding C++11 programa_f5044b9b. 커널에 정적 링크한다.
extern "C" uintptr_t 시플플시험(void) {
    const char Turinys_VALUE[] = "C++ → Java branduolys_VALUE · 한글 😀";
    unsigned char 읽은값[sizeof(Turinys_VALUE)] = {};
    int Failas = kurti_Failas("시험.txt", 읽고쓰기 | 없으면만들기 | trumpinti_Turinys, 0600);
    if (Failas < 0) return 1;
    if (rašymas_Failas_duomenys(Failas, Turinys_VALUE, sizeof(Turinys_VALUE)) != sizeof(Turinys_VALUE)) return 2;
    if (ieškoti_Failas(Failas, 0, 처음기준) != 0) return 3;
    if (파일자료읽기(Failas, 읽은값, sizeof(읽은값)) != sizeof(읽은값)) return 4;
    for (size_t 순번 = 0; 순번 < sizeof(Turinys_VALUE); 순번++) if (읽은값[순번] != (unsigned char)Turinys_VALUE[순번]) return 5;
    if (파일자료읽기(Failas, 읽은값, 1) != 0) return 6;
    if (vykdymas_failų_saugykla(Failas) != -1 || klaidos_numeris != 38) return 7;
    if (Uždaryti_Failas(Failas) || Uždaryti_Failas(Failas) != -1 || klaidos_numeris != 9) return 8;
    Failas = kurti_Failas("시험.txt", tik_skaitomas_VALUE);
    if (Failas < 0 || rašymas_Failas_duomenys(Failas, Turinys_VALUE, 1) != -1 || klaidos_numeris != 9) return 9;
    if (Uždaryti_Failas(Failas)) return 10;
    Failas = kurti_Failas("시험.txt", 읽고쓰기 | 끝에이어쓰기);
    if (Failas < 0 || ieškoti_Failas(Failas, 0, 처음기준) != 0 || rašymas_Failas_duomenys(Failas, "!", 1) != 1 || failo_dydis(Failas) != sizeof(Turinys_VALUE) + 1) return 11;
    if (파일길이정하기(Failas, 2) || ieškoti_Failas(Failas, 4, 처음기준) != 4) return 12;
    // append는 매 write 때 EOF를 사용한다.
    if (rašymas_Failas_duomenys(Failas, "x", 1) != 1 || failo_dydis(Failas) != 3 || Uždaryti_Failas(Failas)) return 13;
    Failas = kurti_Failas("구멍.bin", 읽고쓰기 | 없으면만들기 | trumpinti_Turinys, 0600);
    if (Failas < 0 || ieškoti_Failas(Failas, 3, 처음기준) != 3 || rašymas_Failas_duomenys(Failas, "z", 1) != 1) return 14;
    if (ieškoti_Failas(Failas, 0, 처음기준) != 0 || 파일자료읽기(Failas, 읽은값, 4) != 4 || 읽은값[0] || 읽은값[1] || 읽은값[2] || 읽은값[3] != 'z') return 15;
    if (pašalinti_Failas_įrašas_pavadinimas("구멍.bin") || failo_dydis(Failas) != 4 || Uždaryti_Failas(Failas)) return 16;
    if (kurti_Failas("구멍.bin", tik_skaitomas_VALUE) != -1 || klaidos_numeris != 2) return 17;
    if (kurti_Failas("시험.txt", 읽고쓰기 | 새파일만들기, 0600) != -1 || klaidos_numeris != 17) return 18;
    if (kurti_Failas("../금지", tik_skaitomas_VALUE) != -1) return 19;
    return 0;
}
