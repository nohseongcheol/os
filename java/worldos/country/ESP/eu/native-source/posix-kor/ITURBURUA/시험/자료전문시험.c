#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

#define egiaztatu(baldintza) do { if (!(baldintza)) { puts("POSIX UDP CHECK FAILED: " #baldintza); return 1; } } while (0)
int main(int 인수개수, char **arg_Zerrenda) {
    egiaztatu(인수개수 == 2);
    int ataka_zenbaki = 0;
    for (int 칸 = 0; arg_Zerrenda[1][칸]; 칸++) {
        egiaztatu(arg_Zerrenda[1][칸] >= '0' && arg_Zerrenda[1][칸] <= '9');
        ataka_zenbaki = ataka_zenbaki * 10 + arg_Zerrenda[1][칸] - '0';
        egiaztatu(ataka_zenbaki <= 65535);
    }
    int amaiera_puntu_balio = sortu_amaiera_puntu(AF_INET, SOCK_DGRAM, 0);
    egiaztatu(amaiera_puntu_balio == 3);
    struct sockaddr_in lokal_esparru = {0}, pareko_balio = {0}, RECEIVED_helbide = {0};
    lokal_esparru.sin_family = AF_INET;
    socklen_t luzera_balio = sizeof lokal_esparru;
    egiaztatu(통신주소읽기(amaiera_puntu_balio, (struct sockaddr *)&lokal_esparru, &luzera_balio) == 0 && lokal_esparru.sin_port == 0);
    egiaztatu(lotu_helbide(amaiera_puntu_balio, (struct sockaddr *)&lokal_esparru, sizeof lokal_esparru) == 0);
    egiaztatu(통신주소읽기(amaiera_puntu_balio, (struct sockaddr *)&lokal_esparru, &luzera_balio) == 0 && ntohs(lokal_esparru.sin_port) >= 49152);
    egiaztatu(lotu_helbide(amaiera_puntu_balio, (struct sockaddr *)&lokal_esparru, sizeof lokal_esparru) == -1 && errno == EINVAL);
    int 둘째 = socket(AF_INET, SOCK_DGRAM, 0);
    egiaztatu(bind(둘째, (struct sockaddr *)&lokal_esparru, sizeof lokal_esparru) == -1 && errno == EADDRINUSE);
    egiaztatu(close(둘째) == 0);
    둘째 = dup(amaiera_puntu_balio);
    egiaztatu(close(amaiera_puntu_balio) == 0); amaiera_puntu_balio = 둘째;
    pareko_balio.sin_family = AF_INET; pareko_balio.sin_port = 망차례짧은수(ataka_zenbaki);
    egiaztatu(analizatu_sare_helbide(AF_INET, "10.0.2.2", &pareko_balio.sin_addr) == 1);
    struct timeval itxaron_balio = {0, 200000};
    egiaztatu(aldatu_sare_Ezarpenak(amaiera_puntu_balio, SOL_SOCKET, SO_RCVTIMEO, &itxaron_balio, sizeof itxaron_balio) == 0);
    char datuak[32];
    egiaztatu(자료전문받기(amaiera_puntu_balio, datuak, sizeof datuak, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    egiaztatu(자료전문보내기(amaiera_puntu_balio, "posix-udp", 9, 0, (struct sockaddr *)&pareko_balio, sizeof pareko_balio) == 9);
    luzera_balio = sizeof RECEIVED_helbide;
    egiaztatu(recvfrom(amaiera_puntu_balio, (void *)0x00100000, 9, 0, NULL, NULL) == -1 && errno == EFAULT);
    egiaztatu(자료전문받기(amaiera_puntu_balio, datuak, sizeof datuak, 0, (struct sockaddr *)&RECEIVED_helbide, &luzera_balio) == 9);
    egiaztatu(memcmp(datuak, "posix-udp", 9) == 0 && luzera_balio == 16);
    egiaztatu(RECEIVED_helbide.sin_port == pareko_balio.sin_port && RECEIVED_helbide.sin_addr.s_addr == pareko_balio.sin_addr.s_addr);
    egiaztatu(sendto(amaiera_puntu_balio, "truncate", 8, 0, (struct sockaddr *)&pareko_balio, sizeof pareko_balio) == 8);
    egiaztatu(recvfrom(amaiera_puntu_balio, datuak, 3, 0, NULL, NULL) == 3 && memcmp(datuak, "tru", 3) == 0);
    egiaztatu(recvfrom(amaiera_puntu_balio, datuak, sizeof datuak, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    egiaztatu(sendto(amaiera_puntu_balio, NULL, 0, 0, (struct sockaddr *)&pareko_balio, sizeof pareko_balio) == 0);
    egiaztatu(recvfrom(amaiera_puntu_balio, NULL, 0, 0, NULL, NULL) == 0);
    egiaztatu(recvfrom(amaiera_puntu_balio, datuak, sizeof datuak, 0, NULL, NULL) == -1 && errno == EAGAIN);
    egiaztatu(close(amaiera_puntu_balio) == 0);
    puts("POSIX UDP CHECK PASS");
    return 0;
}
