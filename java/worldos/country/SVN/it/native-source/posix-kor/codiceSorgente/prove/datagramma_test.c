#include <File_ABI.h>
#include <rete_ABI.h>
#include <string.h>
#include <stdio.h>

#define verificare(condizione) do { if (!(condizione)) { puts("POSIX UDP CHECK FAILED: " #condizione); return 1; } } while (0)
int main(int 인수개수, char **argomento_elenco) {
    verificare(인수개수 == 2);
    int numero_di_porta = 0;
    for (int slot_voce = 0; argomento_elenco[1][slot_voce]; slot_voce++) {
        verificare(argomento_elenco[1][slot_voce] >= '0' && argomento_elenco[1][slot_voce] <= '9');
        numero_di_porta = numero_di_porta * 10 + argomento_elenco[1][slot_voce] - '0';
        verificare(numero_di_porta <= 65535);
    }
    int endpoint_VALORE = Crea_endpoint(AF_INET, SOCK_DGRAM, 0);
    verificare(endpoint_VALORE == 3);
    struct sockaddr_in locale_Scope = {0}, peer_VALORE = {0}, RICEV_SCAD_e_mail = {0};
    locale_Scope.sin_family = AF_INET;
    socklen_t durata_VALORE = sizeof locale_Scope;
    verificare(통신주소읽기(endpoint_VALORE, (struct sockaddr *)&locale_Scope, &durata_VALORE) == 0 && locale_Scope.sin_port == 0);
    verificare(BIND_e_mail(endpoint_VALORE, (struct sockaddr *)&locale_Scope, sizeof locale_Scope) == 0);
    verificare(통신주소읽기(endpoint_VALORE, (struct sockaddr *)&locale_Scope, &durata_VALORE) == 0 && ntohs(locale_Scope.sin_port) >= 49152);
    verificare(BIND_e_mail(endpoint_VALORE, (struct sockaddr *)&locale_Scope, sizeof locale_Scope) == -1 && errno == EINVAL);
    int 둘째 = socket(AF_INET, SOCK_DGRAM, 0);
    verificare(bind(둘째, (struct sockaddr *)&locale_Scope, sizeof locale_Scope) == -1 && errno == EADDRINUSE);
    verificare(close(둘째) == 0);
    둘째 = dup(endpoint_VALORE);
    verificare(close(endpoint_VALORE) == 0); endpoint_VALORE = 둘째;
    peer_VALORE.sin_family = AF_INET; peer_VALORE.sin_port = 망차례짧은수(numero_di_porta);
    verificare(analizzare_ID_rete(AF_INET, "10.0.2.2", &peer_VALORE.sin_addr) == 1);
    struct timeval aspetta_VALORE = {0, 200000};
    verificare(cambiare_rete_Impostazioni(endpoint_VALORE, SOL_SOCKET, SO_RCVTIMEO, &aspetta_VALORE, sizeof aspetta_VALORE) == 0);
    char dati[32];
    verificare(ricevere_datagramma_dati(endpoint_VALORE, dati, sizeof dati, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    verificare(inviare_datagramma_dati(endpoint_VALORE, "posix-udp", 9, 0, (struct sockaddr *)&peer_VALORE, sizeof peer_VALORE) == 9);
    durata_VALORE = sizeof RICEV_SCAD_e_mail;
    verificare(recvfrom(endpoint_VALORE, (void *)0x00100000, 9, 0, NULL, NULL) == -1 && errno == EFAULT);
    verificare(ricevere_datagramma_dati(endpoint_VALORE, dati, sizeof dati, 0, (struct sockaddr *)&RICEV_SCAD_e_mail, &durata_VALORE) == 9);
    verificare(memcmp(dati, "posix-udp", 9) == 0 && durata_VALORE == 16);
    verificare(RICEV_SCAD_e_mail.sin_port == peer_VALORE.sin_port && RICEV_SCAD_e_mail.sin_addr.s_addr == peer_VALORE.sin_addr.s_addr);
    verificare(sendto(endpoint_VALORE, "truncate", 8, 0, (struct sockaddr *)&peer_VALORE, sizeof peer_VALORE) == 8);
    verificare(recvfrom(endpoint_VALORE, dati, 3, 0, NULL, NULL) == 3 && memcmp(dati, "tru", 3) == 0);
    verificare(recvfrom(endpoint_VALORE, dati, sizeof dati, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    verificare(sendto(endpoint_VALORE, NULL, 0, 0, (struct sockaddr *)&peer_VALORE, sizeof peer_VALORE) == 0);
    verificare(recvfrom(endpoint_VALORE, NULL, 0, 0, NULL, NULL) == 0);
    verificare(recvfrom(endpoint_VALORE, dati, sizeof dati, 0, NULL, NULL) == -1 && errno == EAGAIN);
    verificare(close(endpoint_VALORE) == 0);
    puts("POSIX UDP CHECK PASS");
    return 0;
}
