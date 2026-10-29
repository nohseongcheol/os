#include "../명명/기계연결이름.h"
#include "Arquivo_ABI.h"
// 표준 C++ biblioteca 없는 freestanding C++11 app_f5044b9b. 커널에 estático_VALOR 링크한다.
extern "C" uintptr_t 시플플시험(void) {
    const char Conteúdo_VALOR[] = "C++ → Java kernel_VALOR · 한글 😀";
    unsigned char leitura_VALOR[sizeof(Conteúdo_VALOR)] = {};
    int ficheiro = abrir_Arquivo("testes.txt", de_leitura_gravação | 없으면만들기 | cortar_Sumário, 0600);
    if (ficheiro < 0) return 1;
    if (gravar_Arquivo_dados(ficheiro, Conteúdo_VALOR, sizeof(Conteúdo_VALOR)) != sizeof(Conteúdo_VALOR)) return 2;
    if (busca_Arquivo(ficheiro, 0, 처음기준) != 0) return 3;
    if (leitura_Arquivo_dados(ficheiro, leitura_VALOR, sizeof(leitura_VALOR)) != sizeof(leitura_VALOR)) return 4;
    for (size_t 순번 = 0; 순번 < sizeof(Conteúdo_VALOR); 순번++) if (leitura_VALOR[순번] != (unsigned char)Conteúdo_VALOR[순번]) return 5;
    if (leitura_Arquivo_dados(ficheiro, leitura_VALOR, 1) != 0) return 6;
    if (commit_Arquivos(ficheiro) != -1 || número_do_erro != 38) return 7;
    if (Close_Arquivo(ficheiro) || Close_Arquivo(ficheiro) != -1 || número_do_erro != 9) return 8;
    ficheiro = abrir_Arquivo("testes.txt", somente_leitura_VALOR);
    if (ficheiro < 0 || gravar_Arquivo_dados(ficheiro, Conteúdo_VALOR, 1) != -1 || número_do_erro != 9) return 9;
    if (Close_Arquivo(ficheiro)) return 10;
    ficheiro = abrir_Arquivo("testes.txt", de_leitura_gravação | 끝에이어쓰기);
    if (ficheiro < 0 || busca_Arquivo(ficheiro, 0, 처음기준) != 0 || gravar_Arquivo_dados(ficheiro, "!", 1) != 1 || tamanho_do_arquivo(ficheiro) != sizeof(Conteúdo_VALOR) + 1) return 11;
    if (set_Arquivo_duração(ficheiro, 2) || busca_Arquivo(ficheiro, 4, 처음기준) != 4) return 12;
    // append는 매 write 때 EOF를 사용한다.
    if (gravar_Arquivo_dados(ficheiro, "x", 1) != 1 || tamanho_do_arquivo(ficheiro) != 3 || Close_Arquivo(ficheiro)) return 13;
    ficheiro = abrir_Arquivo("구멍.bin", de_leitura_gravação | 없으면만들기 | cortar_Sumário, 0600);
    if (ficheiro < 0 || busca_Arquivo(ficheiro, 3, 처음기준) != 3 || gravar_Arquivo_dados(ficheiro, "z", 1) != 1) return 14;
    if (busca_Arquivo(ficheiro, 0, 처음기준) != 0 || leitura_Arquivo_dados(ficheiro, leitura_VALOR, 4) != 4 || leitura_VALOR[0] || leitura_VALOR[1] || leitura_VALOR[2] || leitura_VALOR[3] != 'z') return 15;
    if (remover_Arquivo_entrada_nome("구멍.bin") || tamanho_do_arquivo(ficheiro) != 4 || Close_Arquivo(ficheiro)) return 16;
    if (abrir_Arquivo("구멍.bin", somente_leitura_VALOR) != -1 || número_do_erro != 2) return 17;
    if (abrir_Arquivo("testes.txt", de_leitura_gravação | 새파일만들기, 0600) != -1 || número_do_erro != 17) return 18;
    if (abrir_Arquivo("../금지", somente_leitura_VALOR) != -1) return 19;
    return 0;
}
