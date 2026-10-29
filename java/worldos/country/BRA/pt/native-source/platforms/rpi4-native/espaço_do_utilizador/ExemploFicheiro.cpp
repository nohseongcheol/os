#include "Arquivo_ABI.h"
#include "호출.h"
static int inicializador_VALOR;
static volatile int inicializador_semente = 72;
static volatile double ponto_flutuante_semente = 1.25;
static int 소멸횟수;
struct teste_inicialização { teste_inicialização() { inicializador_VALOR = inicializador_semente + 1; } } 정적초기화;
class Automático_Arquivo {
    int ÍNDICE;
public:
    explicit Automático_Arquivo(const char *Nome) : ÍNDICE(abrir_Arquivo(Nome, de_leitura_gravação | 없으면만들기 | cortar_Sumário, 0600)) {}
    ~Automático_Arquivo() { if (ÍNDICE >= 0) Close_Arquivo(ÍNDICE); 소멸횟수++; }
    int descritor_entrada() const { return ÍNDICE; }
};
extern "C" int START_usuário_app(int) {
    if (inicializador_VALOR != 73 || 사용자호출(0, 0, 0, 0, 0, 0, 0) != 1) return 1;
    double ponto_flutuante_VALOR = ponto_flutuante_semente * 2.0 + 0.5;
    if (사용자호출(0, 0, 0, 0, 0, 0, 0) != 1 || ponto_flutuante_VALOR != 3.0) return 16;
    static const char Conteúdo_VALOR[] = "EL0 C++ → posix-kor → Java ficheiro · 안녕하세요 😀\n";
    char leitura_VALOR[sizeof(Conteúdo_VALOR)] = {};
    {
        Automático_Arquivo ficheiro("espaço_do_utilizador.txt");
        int ÍNDICE = ficheiro.descritor_entrada();
        if (ÍNDICE < 0 || gravar_Arquivo_dados(ÍNDICE, Conteúdo_VALOR, sizeof(Conteúdo_VALOR)) != sizeof(Conteúdo_VALOR)) return 2;
        if (busca_Arquivo(ÍNDICE, 0, 처음기준) || leitura_Arquivo_dados(ÍNDICE, leitura_VALOR, sizeof(leitura_VALOR)) != sizeof(leitura_VALOR)) return 3;
        for (unsigned 순번 = 0; 순번 < sizeof(Conteúdo_VALOR); 순번++) if (leitura_VALOR[순번] != Conteúdo_VALOR[순번]) return 4;
    }
    if (소멸횟수 != 1) return 5;
    if (gravar_Arquivo_dados(1, Conteúdo_VALOR, sizeof(Conteúdo_VALOR) - 1) != sizeof(Conteúdo_VALOR) - 1) return 6;
    uintptr_t 바닥 = usuário_Memória_encerrar(0);
    if (바닥 != 0x02c00000 || usuário_Memória_encerrar(바닥 + 8192) != (intptr_t)(바닥 + 8192)) return 7;
    volatile unsigned char *Memória_VALOR = (volatile unsigned char *)바닥;
    if (Memória_VALOR[0] || Memória_VALOR[8191]) return 8;
    Memória_VALOR[8191] = 137;
    if (usuário_Memória_encerrar(바닥) != (intptr_t)바닥 || usuário_Memória_encerrar(바닥 + 8192) != (intptr_t)(바닥 + 8192) || Memória_VALOR[8191]) return 9;
    // 잘못된 espaço_do_utilizador ponteiro/번호는 오류이며 커널을 중단하지 않는다.
    if (gravar_Arquivo_dados(1, (const void *)0x80000, 8) != -1 || número_do_erro != 14) return 10;
    if (leitura_Arquivo_dados(0, (void *)Conteúdo_VALOR, 1) != -1 || número_do_erro != 14) return 11;
    if (사용자호출(999, 0, 0, 0, 0, 0, 0) != -38) return 12;
    intptr_t 화면폭 = 화면너비읽기(), tela_duração = leitura_tela_altura();
    if (화면폭 <= 0 || tela_duração <= 0 || 사용자호출(13, 화면폭-1, tela_duração-1, 0, 2, 2, 0) != -22) return 13;
    if (tela_retângulo(470, 310, 80, 60, 0x40c050)) return 14;
    // 프로세스 sair_app 시 열린 서술자가 자동 정리되어야 한다.
    if (abrir_Arquivo("espaço_do_utilizador.txt", somente_leitura_VALOR) < 0) return 15;
    return 0;
}
