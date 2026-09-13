#include <conversão_de_endereços/ordem_de_octetos.h>
#include <errno.h>
#include <fcntl.h>
#include <entre_redes/endereço.h>
#include <definições_básicas.h>
#include <sistema/socket.h>
#include <sistema/stat.h>
#include <sistema/identidade_do_sistema.h>
#include <sistema/espera_de_filhos.h>
#include <unistd.h>
#include "shell_locale.h"

/* Adapted from koros4's request interpreter. Private names are localized
 * in each WorldOS edition; main and POSIX ABI names remain unchanged. */

enum { capacidade_da_linha_de_entrada = 512, máximo_de_argumentos = 16, máximo_de_níveis_de_comandos = 4 };
static int profundidade_dos_níveis_de_comandos;
struct fluxo_de_entrada {
    int descritor_de_entrada;
    char memória_intermédia_de_transferência_2[256];
    size_t posição;
    size_t comprimento;
};

static size_t comprimento_do_texto_em_octetos(const char *texto)
{
    size_t comprimento = 0;
    while (texto[comprimento] != '\0')
        comprimento++;
    return comprimento;
}

static int textos_iguais(const char *esquerda, const char *direita)
{
    size_t posição = 0;
    while (esquerda[posição] == direita[posição]) {
        if (esquerda[posição] == '\0')
            return 1;
        posição++;
    }
    return 0;
}

static void escrever_texto(const char *texto)
{
    size_t comprimento = comprimento_do_texto_em_octetos(texto);
    while (comprimento > 0U) {
        ssize_t número_de_octetos_escritos = escrever(STDOUT_FILENO, texto, comprimento);
        if (número_de_octetos_escritos <= 0)
            return;
        texto += número_de_octetos_escritos;
        comprimento -= (size_t)número_de_octetos_escritos;
    }
}

static void escrever_inteiro(int valor)
{
    char caracteres_dos_algarismos[16];
    unsigned int número_de_algarismos;
    unsigned int magnitude_sem_sinal;

    if (valor < 0) {
        escrever_texto("-");
        magnitude_sem_sinal = (unsigned int)(-(valor + 1)) + 1U;
    } else {
        magnitude_sem_sinal = (unsigned int)valor;
    }
    número_de_algarismos = 0;
    do {
        caracteres_dos_algarismos[número_de_algarismos++] = (char)('0' + magnitude_sem_sinal % 10U);
        magnitude_sem_sinal /= 10U;
    } while (magnitude_sem_sinal != 0U);
    while (número_de_algarismos > 0U) {
        número_de_algarismos--;
        (void)escrever(STDOUT_FILENO, &caracteres_dos_algarismos[número_de_algarismos], 1);
    }
}

static void comunicar_erro(const char *operação)
{
    escrever_texto("error: ");
    escrever_texto(operação);
    escrever_texto(" errno=");
    escrever_inteiro(errno);
    escrever_texto("\n");
}

static int ler_linha_de_entrada(struct fluxo_de_entrada *entrada, char *linha_de_entrada, size_t capacidade)
{
    size_t posição = 0;
    int linha_de_entrada_inválida = 0;
    char caráter;
    ssize_t octetos_lidos;
    if (capacidade < 2U)
        return -2;
    for (;;) {
        if (entrada->posição == entrada->comprimento) {
            octetos_lidos = ler(entrada->descritor_de_entrada, entrada->memória_intermédia_de_transferência_2, sizeof(entrada->memória_intermédia_de_transferência_2));
            if (octetos_lidos < 0) {
                if (errno == EINTR)
                    continue;
                return -1;
            }
            if (octetos_lidos == 0) {
                if (posição == 0 && !linha_de_entrada_inválida)
                    return -1;
                break;
            }
            entrada->comprimento = (size_t)octetos_lidos;
            entrada->posição = 0;
        }
        caráter = entrada->memória_intermédia_de_transferência_2[entrada->posição++];
        if (caráter == '\n')
            break;
        if (entrada->descritor_de_entrada == STDIN_FILENO && caráter == 4) {
            if (posição == 0 && !linha_de_entrada_inválida)
                return -1;
            break;
        }
        if (entrada->descritor_de_entrada == STDIN_FILENO && (caráter == 8 || caráter == 127)) {
            if (posição > 0) {
                do {
                    posição--;
                } while (posição > 0 && ((unsigned char)linha_de_entrada[posição] & 0xc0U) == 0x80U);
            }
            continue;
        }
        if (caráter == '\r')
            continue;
        if (caráter == '\0') {
            linha_de_entrada_inválida = 1; /* Reject binary input; do not execute its prefix. */
            continue;
        }
        if (posição + 1U < capacidade)
            linha_de_entrada[posição++] = caráter;
        else
            linha_de_entrada_inválida = 1;
    }
    linha_de_entrada[posição] = '\0';
    return linha_de_entrada_inválida ? -2 : (int)posição;
}

static int separar_argumentos(char *linha_de_entrada, char **argumentos)
{
    int número_de_argumentos = 0;
    char *posição_atual = linha_de_entrada;
    char *posição_de_saída = linha_de_entrada;

    while (*posição_atual != '\0') {
        char aspas = '\0';
        while (*posição_atual == ' ' || *posição_atual == '\t')
            posição_atual++;
        if (*posição_atual == '\0' || *posição_atual == '#')
            break;
        if (número_de_argumentos == máximo_de_argumentos - 1)
            return -1;
        argumentos[número_de_argumentos++] = posição_de_saída;
        while (*posição_atual != '\0') {
            char caráter = *posição_atual++;
            if (aspas == '\0' && (caráter == ' ' || caráter == '\t'))
                break;
            if (caráter == '\\' && aspas != '\'') {
                if (*posição_atual == '\0')
                    return -1;
                *posição_de_saída++ = *posição_atual++;
            } else if (caráter == '\'' || caráter == '"') {
                if (aspas == '\0')
                    aspas = caráter;
                else if (aspas == caráter)
                    aspas = '\0';
                else
                    *posição_de_saída++ = caráter;
            } else {
                *posição_de_saída++ = caráter;
            }
        }
        if (aspas != '\0')
            return -1;
        *posição_de_saída++ = '\0';
    }
    argumentos[número_de_argumentos] = (char *)0;
    return número_de_argumentos;
}

static void mostrar_ajuda(void)
{
    size_t posição;
    escrever_texto(
        "WorldOS command interpreter commands:\n"
        "  help                 show this help\n"
        "  echo TEXT            print text\n"
        "  pwd                  show current directory\n"
        "  cd PATH              change directory\n"
        "  cat FILE             print a FAT file\n"
        "  stat FILE            show file size\n"
        "  pid                  show process identifiers\n"
        "  uname                show operating-system identity\n"
        "  run FILE [ARGS...]   execute a user ELF program\n"
        "  udp [TEXT]           call POSIX UDP and loop back TEXT\n"
        "  source FILE          interpret a UTF-8 command file\n"
        "  exit                 leave the shell\n");
    escrever_texto("Native command proposals (ASCII aliases remain available):\n");
    for (posição = 0; posição < sizeof(comandos_de_referência) / sizeof(comandos_de_referência[0]); posição++) {
        escrever_texto(nomes_locais_dos_comandos[posição]);
        escrever_texto(" = ");
        escrever_texto(comandos_de_referência[posição]);
        escrever_texto("\n");
    }
}

static int comando_corresponde(const char *texto, const char *comando)
{
    size_t posição;
    if (textos_iguais(texto, comando))
        return 1;
    for (posição = 0; posição < sizeof(comandos_de_referência) / sizeof(comandos_de_referência[0]); posição++)
        if (textos_iguais(comando, comandos_de_referência[posição]))
            return textos_iguais(texto, nomes_locais_dos_comandos[posição]);
    return 0;
}

static int interpretar_entrada(int descritor_de_entrada);

static int interpretar_ficheiro_de_comandos(const char *nome_do_ficheiro)
{
    int descritor_do_ficheiro_2;
    int estado;
    if (profundidade_dos_níveis_de_comandos >= máximo_de_níveis_de_comandos) {
        escrever_texto("source: nesting limit\n");
        return 0;
    }
    descritor_do_ficheiro_2 = abrir(nome_do_ficheiro, O_RDONLY);
    if (descritor_do_ficheiro_2 < 0) {
        comunicar_erro(nome_do_ficheiro);
        return 0;
    }
    profundidade_dos_níveis_de_comandos++;
    estado = interpretar_entrada(descritor_do_ficheiro_2);
    profundidade_dos_níveis_de_comandos--;
    (void)fechar(descritor_do_ficheiro_2);
    return estado;
}

static void mostrar_argumentos(int número_de_argumentos, char **argumentos)
{
    int posição;
    for (posição = 1; posição < número_de_argumentos; posição++) {
        if (posição != 1)
            escrever_texto(" ");
        escrever_texto(argumentos[posição]);
    }
    escrever_texto("\n");
}

static void mostrar_diretório_atual(void)
{
    char caminho[128];
    if (obter_caminho_do_diretório_de_trabalho(caminho, sizeof(caminho)) == (char *)0) {
        comunicar_erro("pwd");
        return;
    }
    escrever_texto(caminho);
    escrever_texto("\n");
}

static void mostrar_conteúdo_do_ficheiro(const char *nome_do_ficheiro)
{
    char memória_intermédia_de_transferência_2[128];
    int descritor_do_ficheiro_2 = abrir(nome_do_ficheiro, O_RDONLY);
    ssize_t octetos_lidos;

    if (descritor_do_ficheiro_2 < 0) {
        comunicar_erro("cat");
        return;
    }
    while ((octetos_lidos = ler(descritor_do_ficheiro_2, memória_intermédia_de_transferência_2, sizeof(memória_intermédia_de_transferência_2))) > 0)
        (void)escrever(STDOUT_FILENO, memória_intermédia_de_transferência_2, (size_t)octetos_lidos);
    if (octetos_lidos < 0)
        comunicar_erro("cat/read");
    (void)fechar(descritor_do_ficheiro_2);
    escrever_texto("\n");
}

static void mostrar_informações_do_ficheiro(const char *nome_do_ficheiro)
{
    struct estado_do_ficheiro estado;
    if (estado_do_ficheiro(nome_do_ficheiro, &estado) < 0) {
        comunicar_erro("stat");
        return;
    }
    escrever_texto("size=");
    escrever_inteiro((int)estado.st_size);
    escrever_texto(S_ISDIR(estado.st_mode) ? " type=directory\n" : " type=file\n");
}

static void mostrar_identificadores_de_processos(void)
{
    escrever_texto("pid=");
    escrever_inteiro((int)obter_identificador_do_processo());
    escrever_texto(" ppid=");
    escrever_inteiro((int)obter_identificador_do_processo_pai());
    escrever_texto("\n");
}

static void mostrar_identidade_do_sistema(void)
{
    struct utsname identidade_do_sistema;
    if (obter_informações_do_sistema(&identidade_do_sistema) < 0) {
        comunicar_erro("uname");
        return;
    }
    escrever_texto(identidade_do_sistema.sysname);
    escrever_texto(" ");
    escrever_texto(identidade_do_sistema.release);
    escrever_texto(" ");
    escrever_texto(identidade_do_sistema.machine);
    escrever_texto("\n");
}

static void executar_programa(int número_de_argumentos, char **argumentos)
{
    pid_t identificador_do_processo_filho;
    int estado_de_terminação_do_filho = 0;

    if (número_de_argumentos < 2) {
        escrever_texto("usage: run FILE [ARGS...]\n");
        return;
    }
    identificador_do_processo_filho = bifurcar_processo();
    if (identificador_do_processo_filho < 0) {
        comunicar_erro("fork");
        return;
    }
    if (identificador_do_processo_filho == 0) {
        substituir_programa_em_execução(argumentos[1], &argumentos[1], (char *const *)0);
        comunicar_erro("execve");
        terminar_imediatamente(127);
    }
    if (aguardar_filho_indicado(identificador_do_processo_filho, &estado_de_terminação_do_filho, 0) < 0) {
        comunicar_erro("waitpid");
        return;
    }
    escrever_texto("exit-status=");
    escrever_inteiro(WEXITSTATUS(estado_de_terminação_do_filho));
    escrever_texto("\n");
}

static void testar_retorno_do_datagrama(const char *mensagem)
{
    struct endereço_do_extremo_entre_redes endereço_de_receção = {0};
    struct endereço_do_extremo_entre_redes endereço_do_remetente = {0};
    tipo_do_comprimento_do_endereço comprimento_do_endereço_do_remetente = sizeof(endereço_do_remetente);
    char dados_recebidos[96];
    size_t comprimento_da_mensagem_em_octetos = comprimento_do_texto_em_octetos(mensagem);
    int extremidade_recetora = -1;
    int extremidade_emissora = -1;
    ssize_t número_de_octetos_recebidos;

    if (comprimento_da_mensagem_em_octetos >= sizeof(dados_recebidos)) {
        escrever_texto("udp: message exceeds 95 bytes\n");
        return;
    }
    extremidade_recetora = criar_extremo_de_comunicação(código_da_família_de_endereços_entre_redes, extremo_de_datagramas, protocolo_de_datagramas_do_utilizador);
    extremidade_emissora = criar_extremo_de_comunicação(código_da_família_de_endereços_entre_redes, extremo_de_datagramas, protocolo_de_datagramas_do_utilizador);
    if (extremidade_recetora < 0 || extremidade_emissora < 0) {
        comunicar_erro("socket");
        goto fechar_extremidades_de_comunicação;
    }
    endereço_de_receção.família_de_endereços_entre_redes = código_da_família_de_endereços_entre_redes;
    endereço_de_receção.número_de_porta_de_comunicação = converter_16_bits_para_ordem_da_rede(40404);
    endereço_de_receção.conteúdo_do_endereço_entre_redes.valor_do_endereço = converter_32_bits_para_ordem_da_rede(endereço_de_retorno_local);
    if (associar_endereço_local(extremidade_recetora, (const struct endereço_do_extremo_de_comunicação *)&endereço_de_receção, sizeof(endereço_de_receção)) < 0) {
        comunicar_erro("bind");
        goto fechar_extremidades_de_comunicação;
    }
    if (ligar_ao_extremo_remoto(extremidade_emissora, (const struct endereço_do_extremo_de_comunicação *)&endereço_de_receção, sizeof(endereço_de_receção)) < 0) {
        comunicar_erro("connect");
        goto fechar_extremidades_de_comunicação;
    }
    if (enviar(extremidade_emissora, mensagem, comprimento_da_mensagem_em_octetos, 0) != (ssize_t)comprimento_da_mensagem_em_octetos) {
        comunicar_erro("send");
        goto fechar_extremidades_de_comunicação;
    }
    número_de_octetos_recebidos = receber_com_endereço_de_origem(extremidade_recetora, dados_recebidos, sizeof(dados_recebidos) - 1U, 0,
                         (struct endereço_do_extremo_de_comunicação *)&endereço_do_remetente, &comprimento_do_endereço_do_remetente);
    if (número_de_octetos_recebidos < 0) {
        comunicar_erro("recvfrom");
        goto fechar_extremidades_de_comunicação;
    }
    dados_recebidos[número_de_octetos_recebidos] = '\0';
    escrever_texto("udp-received: ");
    escrever_texto(dados_recebidos);
    escrever_texto("\n");

fechar_extremidades_de_comunicação:
    if (extremidade_emissora >= 0)
        (void)fechar(extremidade_emissora);
    if (extremidade_recetora >= 0)
        (void)fechar(extremidade_recetora);
}

static int interpretar_entrada(int descritor_de_entrada)
{
    char linha_de_entrada[capacidade_da_linha_de_entrada];
    char *argumentos[máximo_de_argumentos];
    struct fluxo_de_entrada entrada = {0};
    entrada.descritor_de_entrada = descritor_de_entrada;

    for (;;) {
        int número_de_argumentos;
        int estado;
        if (descritor_de_entrada == STDIN_FILENO)
            escrever_texto("worldos$ ");
        estado = ler_linha_de_entrada(&entrada, linha_de_entrada, sizeof(linha_de_entrada));
        if (estado == -1)
            return 0;
        if (estado == -2) {
            escrever_texto("input rejected: overlong or binary line\n");
            continue;
        }
        número_de_argumentos = separar_argumentos(linha_de_entrada, argumentos);
        if (número_de_argumentos < 0) {
            escrever_texto("syntax error: quote, escape or argument limit\n");
            continue;
        }
        if (número_de_argumentos == 0)
            continue;
        if (comando_corresponde(argumentos[0], "help"))
            mostrar_ajuda();
        else if (comando_corresponde(argumentos[0], "echo"))
            mostrar_argumentos(número_de_argumentos, argumentos);
        else if (comando_corresponde(argumentos[0], "pwd"))
            mostrar_diretório_atual();
        else if (comando_corresponde(argumentos[0], "cd")) {
            if (número_de_argumentos < 2)
                escrever_texto("usage: cd PATH\n");
            else if (mudar_diretório_de_trabalho(argumentos[1]) < 0)
                comunicar_erro("cd");
        } else if (comando_corresponde(argumentos[0], "cat")) {
            if (número_de_argumentos < 2)
                escrever_texto("usage: cat FILE\n");
            else
                mostrar_conteúdo_do_ficheiro(argumentos[1]);
        } else if (comando_corresponde(argumentos[0], "stat")) {
            if (número_de_argumentos < 2)
                escrever_texto("usage: stat FILE\n");
            else
                mostrar_informações_do_ficheiro(argumentos[1]);
        } else if (comando_corresponde(argumentos[0], "pid"))
            mostrar_identificadores_de_processos();
        else if (comando_corresponde(argumentos[0], "uname"))
            mostrar_identidade_do_sistema();
        else if (comando_corresponde(argumentos[0], "run"))
            executar_programa(número_de_argumentos, argumentos);
        else if (comando_corresponde(argumentos[0], "udp"))
            testar_retorno_do_datagrama(número_de_argumentos >= 2 ? argumentos[1] : "ping");
        else if (comando_corresponde(argumentos[0], "source")) {
            if (número_de_argumentos < 2)
                escrever_texto("usage: source FILE\n");
            else if (interpretar_ficheiro_de_comandos(argumentos[1]))
                return 1;
        } else if (comando_corresponde(argumentos[0], "exit"))
            return 1;
        else
            escrever_texto("unknown command; type help\n");
    }
}

int main(void)
{
    escrever_texto("WORLDOS-SHELL:READY\n");
    (void)interpretar_entrada(STDIN_FILENO);
    escrever_texto("WORLDOS-SHELL:EXIT\n");
    return 0;
}
