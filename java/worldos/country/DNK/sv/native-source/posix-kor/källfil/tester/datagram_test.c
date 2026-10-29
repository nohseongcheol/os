#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

#define verifiera(villkor) do { if (!(villkor)) { puts("POSIX UDP CHECK FAILED: " #villkor); return 1; } } while (0)
int main(int 인수개수, char **argument_ange) {
    verifiera(인수개수 == 2);
    int portnummer = 0;
    for (int fack_post = 0; argument_ange[1][fack_post]; fack_post++) {
        verifiera(argument_ange[1][fack_post] >= '0' && argument_ange[1][fack_post] <= '9');
        portnummer = portnummer * 10 + argument_ange[1][fack_post] - '0';
        verifiera(portnummer <= 65535);
    }
    int deltagare_värde = Skapa_deltagare(AF_INET, SOCK_DGRAM, 0);
    verifiera(deltagare_värde == 3);
    struct sockaddr_in lokal_scope = {0}, peer_värde = {0}, BELOPP_ADRESS = {0};
    lokal_scope.sin_family = AF_INET;
    socklen_t längd_värde = sizeof lokal_scope;
    verifiera(läsa_socket_ADRESS(deltagare_värde, (struct sockaddr *)&lokal_scope, &längd_värde) == 0 && lokal_scope.sin_port == 0);
    verifiera(BIND_ADRESS(deltagare_värde, (struct sockaddr *)&lokal_scope, sizeof lokal_scope) == 0);
    verifiera(läsa_socket_ADRESS(deltagare_värde, (struct sockaddr *)&lokal_scope, &längd_värde) == 0 && ntohs(lokal_scope.sin_port) >= 49152);
    verifiera(BIND_ADRESS(deltagare_värde, (struct sockaddr *)&lokal_scope, sizeof lokal_scope) == -1 && errno == EINVAL);
    int 둘째 = socket(AF_INET, SOCK_DGRAM, 0);
    verifiera(bind(둘째, (struct sockaddr *)&lokal_scope, sizeof lokal_scope) == -1 && errno == EADDRINUSE);
    verifiera(close(둘째) == 0);
    둘째 = dup(deltagare_värde);
    verifiera(close(deltagare_värde) == 0); deltagare_värde = 둘째;
    peer_värde.sin_family = AF_INET; peer_värde.sin_port = 망차례짧은수(portnummer);
    verifiera(parsa_Nätverks_ID(AF_INET, "10.0.2.2", &peer_värde.sin_addr) == 1);
    struct timeval vänta_värde = {0, 200000};
    verifiera(ändra_nätverk_Inställningar(deltagare_värde, SOL_SOCKET, SO_RCVTIMEO, &vänta_värde, sizeof vänta_värde) == 0);
    char data[32];
    verifiera(få_datagram_data(deltagare_värde, data, sizeof data, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    verifiera(skicka_datagram_data(deltagare_värde, "posix-udp", 9, 0, (struct sockaddr *)&peer_värde, sizeof peer_värde) == 9);
    längd_värde = sizeof BELOPP_ADRESS;
    verifiera(recvfrom(deltagare_värde, (void *)0x00100000, 9, 0, NULL, NULL) == -1 && errno == EFAULT);
    verifiera(få_datagram_data(deltagare_värde, data, sizeof data, 0, (struct sockaddr *)&BELOPP_ADRESS, &längd_värde) == 9);
    verifiera(memcmp(data, "posix-udp", 9) == 0 && längd_värde == 16);
    verifiera(BELOPP_ADRESS.sin_port == peer_värde.sin_port && BELOPP_ADRESS.sin_addr.s_addr == peer_värde.sin_addr.s_addr);
    verifiera(sendto(deltagare_värde, "truncate", 8, 0, (struct sockaddr *)&peer_värde, sizeof peer_värde) == 8);
    verifiera(recvfrom(deltagare_värde, data, 3, 0, NULL, NULL) == 3 && memcmp(data, "tru", 3) == 0);
    verifiera(recvfrom(deltagare_värde, data, sizeof data, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    verifiera(sendto(deltagare_värde, NULL, 0, 0, (struct sockaddr *)&peer_värde, sizeof peer_värde) == 0);
    verifiera(recvfrom(deltagare_värde, NULL, 0, 0, NULL, NULL) == 0);
    verifiera(recvfrom(deltagare_värde, data, sizeof data, 0, NULL, NULL) == -1 && errno == EAGAIN);
    verifiera(close(deltagare_värde) == 0);
    puts("POSIX UDP CHECK PASS");
    return 0;
}
