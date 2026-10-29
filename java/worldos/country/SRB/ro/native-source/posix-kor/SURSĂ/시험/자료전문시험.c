#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

#define verifica(condiție) do { if (!(condiție)) { puts("POSIX UDP CHECK FAILED: " #condiție); return 1; } } while (0)
int main(int 인수개수, char **argument_Listă) {
    verifica(인수개수 == 2);
    int număr_port = 0;
    for (int 칸 = 0; argument_Listă[1][칸]; 칸++) {
        verifica(argument_Listă[1][칸] >= '0' && argument_Listă[1][칸] <= '9');
        număr_port = număr_port * 10 + argument_Listă[1][칸] - '0';
        verifica(număr_port <= 65535);
    }
    int participant_VALUE = crea_participant(AF_INET, SOCK_DGRAM, 0);
    verifica(participant_VALUE == 3);
    struct sockaddr_in local_gamă = {0}, pereche_VALUE = {0}, RECEIVED_adresa = {0};
    local_gamă.sin_family = AF_INET;
    socklen_t lungime_VALUE = sizeof local_gamă;
    verifica(통신주소읽기(participant_VALUE, (struct sockaddr *)&local_gamă, &lungime_VALUE) == 0 && local_gamă.sin_port == 0);
    verifica(BIND_adresa(participant_VALUE, (struct sockaddr *)&local_gamă, sizeof local_gamă) == 0);
    verifica(통신주소읽기(participant_VALUE, (struct sockaddr *)&local_gamă, &lungime_VALUE) == 0 && ntohs(local_gamă.sin_port) >= 49152);
    verifica(BIND_adresa(participant_VALUE, (struct sockaddr *)&local_gamă, sizeof local_gamă) == -1 && errno == EINVAL);
    int 둘째 = socket(AF_INET, SOCK_DGRAM, 0);
    verifica(bind(둘째, (struct sockaddr *)&local_gamă, sizeof local_gamă) == -1 && errno == EADDRINUSE);
    verifica(close(둘째) == 0);
    둘째 = dup(participant_VALUE);
    verifica(close(participant_VALUE) == 0); participant_VALUE = 둘째;
    pereche_VALUE.sin_family = AF_INET; pereche_VALUE.sin_port = 망차례짧은수(număr_port);
    verifica(analiza_ID_rețea(AF_INET, "10.0.2.2", &pereche_VALUE.sin_addr) == 1);
    struct timeval 대기 = {0, 200000};
    verifica(schimba_rețea_Setări(participant_VALUE, SOL_SOCKET, SO_RCVTIMEO, &대기, sizeof 대기) == 0);
    char date[32];
    verifica(primi_diagramă_informații_date(participant_VALUE, date, sizeof date, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    verifica(trimite_diagramă_informații_date(participant_VALUE, "posix-udp", 9, 0, (struct sockaddr *)&pereche_VALUE, sizeof pereche_VALUE) == 9);
    lungime_VALUE = sizeof RECEIVED_adresa;
    verifica(recvfrom(participant_VALUE, (void *)0x00100000, 9, 0, NULL, NULL) == -1 && errno == EFAULT);
    verifica(primi_diagramă_informații_date(participant_VALUE, date, sizeof date, 0, (struct sockaddr *)&RECEIVED_adresa, &lungime_VALUE) == 9);
    verifica(memcmp(date, "posix-udp", 9) == 0 && lungime_VALUE == 16);
    verifica(RECEIVED_adresa.sin_port == pereche_VALUE.sin_port && RECEIVED_adresa.sin_addr.s_addr == pereche_VALUE.sin_addr.s_addr);
    verifica(sendto(participant_VALUE, "truncate", 8, 0, (struct sockaddr *)&pereche_VALUE, sizeof pereche_VALUE) == 8);
    verifica(recvfrom(participant_VALUE, date, 3, 0, NULL, NULL) == 3 && memcmp(date, "tru", 3) == 0);
    verifica(recvfrom(participant_VALUE, date, sizeof date, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    verifica(sendto(participant_VALUE, NULL, 0, 0, (struct sockaddr *)&pereche_VALUE, sizeof pereche_VALUE) == 0);
    verifica(recvfrom(participant_VALUE, NULL, 0, 0, NULL, NULL) == 0);
    verifica(recvfrom(participant_VALUE, date, sizeof date, 0, NULL, NULL) == -1 && errno == EAGAIN);
    verifica(close(participant_VALUE) == 0);
    puts("POSIX UDP CHECK PASS");
    return 0;
}
