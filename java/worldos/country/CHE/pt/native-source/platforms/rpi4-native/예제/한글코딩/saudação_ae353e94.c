#include "Arquivo_ABI.h"
int START_usuário_app(int argumentos) {
    (void)argumentos;
    const char saudação[] = "C에서 한글 이름과 posix-kor 호출\n";
    int 문서 = abrir_Arquivo("C인사.txt", de_leitura_gravação | 없으면만들기 | cortar_Sumário, 0600);
    if (문서 < 0) return 1;
    입출력결과형 기록한수 = gravar_Arquivo_dados(문서, saudação, sizeof(saudação) - 1);
    Close_Arquivo(문서);
    gravar_Arquivo_dados(1, saudação, sizeof(saudação) - 1);
    return 기록한수 == sizeof(saudação) - 1 ? 0 : 2;
}
