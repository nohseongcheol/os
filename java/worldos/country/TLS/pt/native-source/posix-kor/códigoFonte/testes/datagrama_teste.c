#include <Arquivo_ABI.h>
#include <rede_ABI.h>
#include <string.h>
#include <stdio.h>

#define verificar(doença) do { if (!(doença)) { puts("POSIX UDP CHECK FAILED: " #doença); return 1; } } while (0)
int main(int 인수개수, char **argumento_Lista) {
    verificar(인수개수 == 2);
    int número_da_porta = 0;
    for (int slot_entrada = 0; argumento_Lista[1][slot_entrada]; slot_entrada++) {
        verificar(argumento_Lista[1][slot_entrada] >= '0' && argumento_Lista[1][slot_entrada] <= '9');
        número_da_porta = número_da_porta * 10 + argumento_Lista[1][slot_entrada] - '0';
        verificar(número_da_porta <= 65535);
    }
    int empresa_VALOR = Criar_empresa(AF_INET, SOCK_DGRAM, 0);
    verificar(empresa_VALOR == 3);
    struct sockaddr_in local_Scope = {0}, par_VALOR = {0}, RECEBER_email = {0};
    local_Scope.sin_family = AF_INET;
    socklen_t duração_VALOR = sizeof local_Scope;
    verificar(leitura_soquete_email(empresa_VALOR, (struct sockaddr *)&local_Scope, &duração_VALOR) == 0 && local_Scope.sin_port == 0);
    verificar(BIND_email(empresa_VALOR, (struct sockaddr *)&local_Scope, sizeof local_Scope) == 0);
    verificar(leitura_soquete_email(empresa_VALOR, (struct sockaddr *)&local_Scope, &duração_VALOR) == 0 && ntohs(local_Scope.sin_port) >= 49152);
    verificar(BIND_email(empresa_VALOR, (struct sockaddr *)&local_Scope, sizeof local_Scope) == -1 && errno == EINVAL);
    int 둘째 = socket(AF_INET, SOCK_DGRAM, 0);
    verificar(bind(둘째, (struct sockaddr *)&local_Scope, sizeof local_Scope) == -1 && errno == EADDRINUSE);
    verificar(close(둘째) == 0);
    둘째 = dup(empresa_VALOR);
    verificar(close(empresa_VALOR) == 0); empresa_VALOR = 둘째;
    par_VALOR.sin_family = AF_INET; par_VALOR.sin_port = 망차례짧은수(número_da_porta);
    verificar(analisar_ID_de_rede(AF_INET, "10.0.2.2", &par_VALOR.sin_addr) == 1);
    struct timeval aguarde_VALOR = {0, 200000};
    verificar(alterar_rede_Configurações(empresa_VALOR, SOL_SOCKET, SO_RCVTIMEO, &aguarde_VALOR, sizeof aguarde_VALOR) == 0);
    char dados[32];
    verificar(receber_datagrama_dados(empresa_VALOR, dados, sizeof dados, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    verificar(enviar_datagrama_dados(empresa_VALOR, "posix-udp", 9, 0, (struct sockaddr *)&par_VALOR, sizeof par_VALOR) == 9);
    duração_VALOR = sizeof RECEBER_email;
    verificar(recvfrom(empresa_VALOR, (void *)0x00100000, 9, 0, NULL, NULL) == -1 && errno == EFAULT);
    verificar(receber_datagrama_dados(empresa_VALOR, dados, sizeof dados, 0, (struct sockaddr *)&RECEBER_email, &duração_VALOR) == 9);
    verificar(memcmp(dados, "posix-udp", 9) == 0 && duração_VALOR == 16);
    verificar(RECEBER_email.sin_port == par_VALOR.sin_port && RECEBER_email.sin_addr.s_addr == par_VALOR.sin_addr.s_addr);
    verificar(sendto(empresa_VALOR, "truncate", 8, 0, (struct sockaddr *)&par_VALOR, sizeof par_VALOR) == 8);
    verificar(recvfrom(empresa_VALOR, dados, 3, 0, NULL, NULL) == 3 && memcmp(dados, "tru", 3) == 0);
    verificar(recvfrom(empresa_VALOR, dados, sizeof dados, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    verificar(sendto(empresa_VALOR, NULL, 0, 0, (struct sockaddr *)&par_VALOR, sizeof par_VALOR) == 0);
    verificar(recvfrom(empresa_VALOR, NULL, 0, 0, NULL, NULL) == 0);
    verificar(recvfrom(empresa_VALOR, dados, sizeof dados, 0, NULL, NULL) == -1 && errno == EAGAIN);
    verificar(close(empresa_VALOR) == 0);
    puts("POSIX UDP CHECK PASS");
    return 0;
}
