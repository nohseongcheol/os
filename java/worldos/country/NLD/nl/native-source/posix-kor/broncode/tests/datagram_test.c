#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

#define bevestigen(toestand) do { if (!(toestand)) { puts("POSIX UDP CHECK FAILED: " #toestand); return 1; } } while (0)
int main(int 인수개수, char **argument_Lijst) {
    bevestigen(인수개수 == 2);
    int poortnummer = 0;
    for (int sleuf_invoer = 0; argument_Lijst[1][sleuf_invoer]; sleuf_invoer++) {
        bevestigen(argument_Lijst[1][sleuf_invoer] >= '0' && argument_Lijst[1][sleuf_invoer] <= '9');
        poortnummer = poortnummer * 10 + argument_Lijst[1][sleuf_invoer] - '0';
        bevestigen(poortnummer <= 65535);
    }
    int eindpunt_WAARDE = maken_eindpunt(AF_INET, SOCK_DGRAM, 0);
    bevestigen(eindpunt_WAARDE == 3);
    struct sockaddr_in lokaal_scope = {0}, peer_WAARDE = {0}, OPBRENGST_ADRES = {0};
    lokaal_scope.sin_family = AF_INET;
    socklen_t tijdsduur_WAARDE = sizeof lokaal_scope;
    bevestigen(통신주소읽기(eindpunt_WAARDE, (struct sockaddr *)&lokaal_scope, &tijdsduur_WAARDE) == 0 && lokaal_scope.sin_port == 0);
    bevestigen(BIND_ADRES(eindpunt_WAARDE, (struct sockaddr *)&lokaal_scope, sizeof lokaal_scope) == 0);
    bevestigen(통신주소읽기(eindpunt_WAARDE, (struct sockaddr *)&lokaal_scope, &tijdsduur_WAARDE) == 0 && ntohs(lokaal_scope.sin_port) >= 49152);
    bevestigen(BIND_ADRES(eindpunt_WAARDE, (struct sockaddr *)&lokaal_scope, sizeof lokaal_scope) == -1 && errno == EINVAL);
    int 둘째 = socket(AF_INET, SOCK_DGRAM, 0);
    bevestigen(bind(둘째, (struct sockaddr *)&lokaal_scope, sizeof lokaal_scope) == -1 && errno == EADDRINUSE);
    bevestigen(close(둘째) == 0);
    둘째 = dup(eindpunt_WAARDE);
    bevestigen(close(eindpunt_WAARDE) == 0); eindpunt_WAARDE = 둘째;
    peer_WAARDE.sin_family = AF_INET; peer_WAARDE.sin_port = 망차례짧은수(poortnummer);
    bevestigen(parseren_netwerk_id(AF_INET, "10.0.2.2", &peer_WAARDE.sin_addr) == 1);
    struct timeval wachten_WAARDE = {0, 200000};
    bevestigen(wijzigen_net_Instellingen(eindpunt_WAARDE, SOL_SOCKET, SO_RCVTIMEO, &wachten_WAARDE, sizeof wachten_WAARDE) == 0);
    char gegevens[32];
    bevestigen(ontvangen_datagram_gegevens(eindpunt_WAARDE, gegevens, sizeof gegevens, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    bevestigen(e_mailen_datagram_gegevens(eindpunt_WAARDE, "posix-udp", 9, 0, (struct sockaddr *)&peer_WAARDE, sizeof peer_WAARDE) == 9);
    tijdsduur_WAARDE = sizeof OPBRENGST_ADRES;
    bevestigen(recvfrom(eindpunt_WAARDE, (void *)0x00100000, 9, 0, NULL, NULL) == -1 && errno == EFAULT);
    bevestigen(ontvangen_datagram_gegevens(eindpunt_WAARDE, gegevens, sizeof gegevens, 0, (struct sockaddr *)&OPBRENGST_ADRES, &tijdsduur_WAARDE) == 9);
    bevestigen(memcmp(gegevens, "posix-udp", 9) == 0 && tijdsduur_WAARDE == 16);
    bevestigen(OPBRENGST_ADRES.sin_port == peer_WAARDE.sin_port && OPBRENGST_ADRES.sin_addr.s_addr == peer_WAARDE.sin_addr.s_addr);
    bevestigen(sendto(eindpunt_WAARDE, "truncate", 8, 0, (struct sockaddr *)&peer_WAARDE, sizeof peer_WAARDE) == 8);
    bevestigen(recvfrom(eindpunt_WAARDE, gegevens, 3, 0, NULL, NULL) == 3 && memcmp(gegevens, "tru", 3) == 0);
    bevestigen(recvfrom(eindpunt_WAARDE, gegevens, sizeof gegevens, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    bevestigen(sendto(eindpunt_WAARDE, NULL, 0, 0, (struct sockaddr *)&peer_WAARDE, sizeof peer_WAARDE) == 0);
    bevestigen(recvfrom(eindpunt_WAARDE, NULL, 0, 0, NULL, NULL) == 0);
    bevestigen(recvfrom(eindpunt_WAARDE, gegevens, sizeof gegevens, 0, NULL, NULL) == -1 && errno == EAGAIN);
    bevestigen(close(eindpunt_WAARDE) == 0);
    puts("POSIX UDP CHECK PASS");
    return 0;
}
