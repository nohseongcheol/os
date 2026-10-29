#include <Arquivo_ABI.h>
#if defined(__linux__) || !defined(__JKOROS__) || __STDC_HOSTED__
#error This sample must be compiled with the native guest cc command.
#endif

int main(int 인수개수, char **argumento_Lista) {
    if (인수개수 < 1 || !argumento_Lista[0]) return 2;
    const char saudação[] = "nativo 커널의 C와 Português POSIX\n";
    int 문서 = abrir_Arquivo("saudação_ae353e94.txt", de_leitura_gravação | 없으면만들기 | cortar_Sumário, 0600);
    if (문서 < 0) return 1;
    입출력결과형 duração_VALOR = gravar_Arquivo_dados(문서, saudação, sizeof(saudação) - 1);
    Close_Arquivo(문서);
    gravar_Arquivo_dados(1, saudação, sizeof(saudação) - 1);
    return duração_VALOR == sizeof(saudação) - 1 ? 0 : 3;
}
