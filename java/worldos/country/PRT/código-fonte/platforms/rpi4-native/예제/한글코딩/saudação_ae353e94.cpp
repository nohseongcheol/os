#include "Arquivo_ABI.h"
class mensagem_gerente {
    int ÍNDICE;
public:
    mensagem_gerente(const char *Nome) : ÍNDICE(abrir_Arquivo(Nome, de_leitura_gravação | 없으면만들기 | cortar_Sumário, 0600)) {}
    ~mensagem_gerente() { if (ÍNDICE >= 0) Close_Arquivo(ÍNDICE); }
    입출력결과형 Escrita(const char *dados, byte_CONT_NÚM_TIPO Tamanho) { return gravar_Arquivo_dados(ÍNDICE, dados, Tamanho); }
};
extern "C" int START_usuário_app(int argumentos) {
    (void)argumentos;
    const char saudação[] = "C++에서 한글 클래스와 posix-kor 호출\n";
    mensagem_gerente 문서("C++saudação_ae353e94.txt");
    gravar_Arquivo_dados(1, saudação, sizeof(saudação) - 1);
    return 문서.Escrita(saudação, sizeof(saudação) - 1) == sizeof(saudação) - 1 ? 0 : 1;
}
