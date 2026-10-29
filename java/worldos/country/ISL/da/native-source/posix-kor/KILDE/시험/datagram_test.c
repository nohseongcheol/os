#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

#define bekræfte(lidelse) do { if (!(lidelse)) { puts("POSIX UDP CHECK FAILED: " #lidelse); return 1; } } while (0)
int main(int 인수개수, char **argument_Liste) {
    bekræfte(인수개수 == 2);
    int portnummer = 0;
    for (int udvidelsesstik_post = 0; argument_Liste[1][udvidelsesstik_post]; udvidelsesstik_post++) {
        bekræfte(argument_Liste[1][udvidelsesstik_post] >= '0' && argument_Liste[1][udvidelsesstik_post] <= '9');
        portnummer = portnummer * 10 + argument_Liste[1][udvidelsesstik_post] - '0';
        bekræfte(portnummer <= 65535);
    }
    int slutpunkt_VÆRDI = åbne_slutpunkt(AF_INET, SOCK_DGRAM, 0);
    bekræfte(slutpunkt_VÆRDI == 3);
    struct sockaddr_in lokal_Omfang = {0}, peer_VÆRDI = {0}, MODTAGET_VED_UDLØB_mail = {0};
    lokal_Omfang.sin_family = AF_INET;
    socklen_t varighed_VÆRDI = sizeof lokal_Omfang;
    bekræfte(통신주소읽기(slutpunkt_VÆRDI, (struct sockaddr *)&lokal_Omfang, &varighed_VÆRDI) == 0 && lokal_Omfang.sin_port == 0);
    bekræfte(BIND_mail(slutpunkt_VÆRDI, (struct sockaddr *)&lokal_Omfang, sizeof lokal_Omfang) == 0);
    bekræfte(통신주소읽기(slutpunkt_VÆRDI, (struct sockaddr *)&lokal_Omfang, &varighed_VÆRDI) == 0 && ntohs(lokal_Omfang.sin_port) >= 49152);
    bekræfte(BIND_mail(slutpunkt_VÆRDI, (struct sockaddr *)&lokal_Omfang, sizeof lokal_Omfang) == -1 && errno == EINVAL);
    int 둘째 = socket(AF_INET, SOCK_DGRAM, 0);
    bekræfte(bind(둘째, (struct sockaddr *)&lokal_Omfang, sizeof lokal_Omfang) == -1 && errno == EADDRINUSE);
    bekræfte(close(둘째) == 0);
    둘째 = dup(slutpunkt_VÆRDI);
    bekræfte(close(slutpunkt_VÆRDI) == 0); slutpunkt_VÆRDI = 둘째;
    peer_VÆRDI.sin_family = AF_INET; peer_VÆRDI.sin_port = 망차례짧은수(portnummer);
    bekræfte(opdele_tekst_netværks_id(AF_INET, "10.0.2.2", &peer_VÆRDI.sin_addr) == 1);
    struct timeval vent_VÆRDI = {0, 200000};
    bekræfte(ændre_netværk_Indstillinger(slutpunkt_VÆRDI, SOL_SOCKET, SO_RCVTIMEO, &vent_VÆRDI, sizeof vent_VÆRDI) == 0);
    char data[32];
    bekræfte(modtage_datagram_data(slutpunkt_VÆRDI, data, sizeof data, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    bekræfte(maile_datagram_data(slutpunkt_VÆRDI, "posix-udp", 9, 0, (struct sockaddr *)&peer_VÆRDI, sizeof peer_VÆRDI) == 9);
    varighed_VÆRDI = sizeof MODTAGET_VED_UDLØB_mail;
    bekræfte(recvfrom(slutpunkt_VÆRDI, (void *)0x00100000, 9, 0, NULL, NULL) == -1 && errno == EFAULT);
    bekræfte(modtage_datagram_data(slutpunkt_VÆRDI, data, sizeof data, 0, (struct sockaddr *)&MODTAGET_VED_UDLØB_mail, &varighed_VÆRDI) == 9);
    bekræfte(memcmp(data, "posix-udp", 9) == 0 && varighed_VÆRDI == 16);
    bekræfte(MODTAGET_VED_UDLØB_mail.sin_port == peer_VÆRDI.sin_port && MODTAGET_VED_UDLØB_mail.sin_addr.s_addr == peer_VÆRDI.sin_addr.s_addr);
    bekræfte(sendto(slutpunkt_VÆRDI, "truncate", 8, 0, (struct sockaddr *)&peer_VÆRDI, sizeof peer_VÆRDI) == 8);
    bekræfte(recvfrom(slutpunkt_VÆRDI, data, 3, 0, NULL, NULL) == 3 && memcmp(data, "tru", 3) == 0);
    bekræfte(recvfrom(slutpunkt_VÆRDI, data, sizeof data, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    bekræfte(sendto(slutpunkt_VÆRDI, NULL, 0, 0, (struct sockaddr *)&peer_VÆRDI, sizeof peer_VÆRDI) == 0);
    bekræfte(recvfrom(slutpunkt_VÆRDI, NULL, 0, 0, NULL, NULL) == 0);
    bekræfte(recvfrom(slutpunkt_VÆRDI, data, sizeof data, 0, NULL, NULL) == -1 && errno == EAGAIN);
    bekræfte(close(slutpunkt_VÆRDI) == 0);
    puts("POSIX UDP CHECK PASS");
    return 0;
}
