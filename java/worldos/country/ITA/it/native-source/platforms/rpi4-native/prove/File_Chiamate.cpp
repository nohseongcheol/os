#include "../명명/기계연결이름.h"
#include "File_ABI.h"
// 표준 C++ Catalogo 없는 freestanding C++11 app_f5044b9b. 커널에 statico_VALORE 링크한다.
extern "C" uintptr_t 시플플시험(void) {
    const char Contenuto_VALORE[] = "C++ → Java kernel_VALORE · 한글 😀";
    unsigned char 읽은값[sizeof(Contenuto_VALORE)] = {};
    int file = aperto_File("prove.txt", in_lettura_scrittura | 없으면만들기 | tagliare_Sommario, 0600);
    if (file < 0) return 1;
    if (scrivere_File_dati(file, Contenuto_VALORE, sizeof(Contenuto_VALORE)) != sizeof(Contenuto_VALORE)) return 2;
    if (cercare_File(file, 0, 처음기준) != 0) return 3;
    if (파일자료읽기(file, 읽은값, sizeof(읽은값)) != sizeof(읽은값)) return 4;
    for (size_t 순번 = 0; 순번 < sizeof(Contenuto_VALORE); 순번++) if (읽은값[순번] != (unsigned char)Contenuto_VALORE[순번]) return 5;
    if (파일자료읽기(file, 읽은값, 1) != 0) return 6;
    if (commit_File(file) != -1 || numero_errore != 38) return 7;
    if (Chiudi_File(file) || Chiudi_File(file) != -1 || numero_errore != 9) return 8;
    file = aperto_File("prove.txt", di_sola_lettura_VALORE);
    if (file < 0 || scrivere_File_dati(file, Contenuto_VALORE, 1) != -1 || numero_errore != 9) return 9;
    if (Chiudi_File(file)) return 10;
    file = aperto_File("prove.txt", in_lettura_scrittura | 끝에이어쓰기);
    if (file < 0 || cercare_File(file, 0, 처음기준) != 0 || scrivere_File_dati(file, "!", 1) != 1 || dimensioni_del_file(file) != sizeof(Contenuto_VALORE) + 1) return 11;
    if (set_File_durata(file, 2) || cercare_File(file, 4, 처음기준) != 4) return 12;
    // append는 매 write 때 EOF를 사용한다.
    if (scrivere_File_dati(file, "x", 1) != 1 || dimensioni_del_file(file) != 3 || Chiudi_File(file)) return 13;
    file = aperto_File("구멍.bin", in_lettura_scrittura | 없으면만들기 | tagliare_Sommario, 0600);
    if (file < 0 || cercare_File(file, 3, 처음기준) != 3 || scrivere_File_dati(file, "z", 1) != 1) return 14;
    if (cercare_File(file, 0, 처음기준) != 0 || 파일자료읽기(file, 읽은값, 4) != 4 || 읽은값[0] || 읽은값[1] || 읽은값[2] || 읽은값[3] != 'z') return 15;
    if (rimuovere_File_voce_nome("구멍.bin") || dimensioni_del_file(file) != 4 || Chiudi_File(file)) return 16;
    if (aperto_File("구멍.bin", di_sola_lettura_VALORE) != -1 || numero_errore != 2) return 17;
    if (aperto_File("prove.txt", in_lettura_scrittura | 새파일만들기, 0600) != -1 || numero_errore != 17) return 18;
    if (aperto_File("../금지", di_sola_lettura_VALORE) != -1) return 19;
    return 0;
}
