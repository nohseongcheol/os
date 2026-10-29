#include "파일규약.h"
class documento_xefe {
    int ÍNDICE;
public:
    documento_xefe(const char *Nome) : ÍNDICE(abrir_Ficheiro(Nome, de_lectura_e_escrita | 없으면만들기 | 내용비우기, 0600)) {}
    ~documento_xefe() { if (ÍNDICE >= 0) peche_Ficheiro(ÍNDICE); }
    입출력결과형 Escritura(const char *datos, byte_CONTAR_TIPO Tamaño) { return escribir_Ficheiro_datos(ÍNDICE, datos, Tamaño); }
};
extern "C" int START_usuario_apl(int Argumentos) {
    (void)Argumentos;
    const char 인사말[] = "C++에서 한글 클래스와 posix-kor 호출\n";
    documento_xefe 문서("C++인사.txt");
    escribir_Ficheiro_datos(1, 인사말, sizeof(인사말) - 1);
    return 문서.Escritura(인사말, sizeof(인사말) - 1) == sizeof(인사말) - 1 ? 0 : 1;
}
