#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

#define Tabbatar_da(Yanayi) do { if (!(Yanayi)) { puts("POSIX UDP CHECK FAILED: " #Yanayi); return 1; } } while (0)
int main(int 인수개수, char **Tubalin_aiki_Jeri) {
    Tabbatar_da(인수개수 == 2);
    int lambar_kafa = 0;
    for (int rami_Mashigar_bayanai = 0; Tubalin_aiki_Jeri[1][rami_Mashigar_bayanai]; rami_Mashigar_bayanai++) {
        Tabbatar_da(Tubalin_aiki_Jeri[1][rami_Mashigar_bayanai] >= '0' && Tubalin_aiki_Jeri[1][rami_Mashigar_bayanai] <= '9');
        lambar_kafa = lambar_kafa * 10 + Tubalin_aiki_Jeri[1][rami_Mashigar_bayanai] - '0';
        Tabbatar_da(lambar_kafa <= 65535);
    }
    int 종단점 = 통신종단점만들기(AF_INET, SOCK_DGRAM, 0);
    Tabbatar_da(종단점 == 3);
    struct sockaddr_in na_gida_Kima = {0}, Fiya_Daraja = {0}, 받은주소 = {0};
    na_gida_Kima.sin_family = AF_INET;
    socklen_t Tsawo_Daraja = sizeof na_gida_Kima;
    Tabbatar_da(통신주소읽기(종단점, (struct sockaddr *)&na_gida_Kima, &Tsawo_Daraja) == 0 && na_gida_Kima.sin_port == 0);
    Tabbatar_da(BIND_imel(종단점, (struct sockaddr *)&na_gida_Kima, sizeof na_gida_Kima) == 0);
    Tabbatar_da(통신주소읽기(종단점, (struct sockaddr *)&na_gida_Kima, &Tsawo_Daraja) == 0 && ntohs(na_gida_Kima.sin_port) >= 49152);
    Tabbatar_da(BIND_imel(종단점, (struct sockaddr *)&na_gida_Kima, sizeof na_gida_Kima) == -1 && errno == EINVAL);
    int 둘째 = socket(AF_INET, SOCK_DGRAM, 0);
    Tabbatar_da(bind(둘째, (struct sockaddr *)&na_gida_Kima, sizeof na_gida_Kima) == -1 && errno == EADDRINUSE);
    Tabbatar_da(close(둘째) == 0);
    둘째 = dup(종단점);
    Tabbatar_da(close(종단점) == 0); 종단점 = 둘째;
    Fiya_Daraja.sin_family = AF_INET; Fiya_Daraja.sin_port = 망차례짧은수(lambar_kafa);
    Tabbatar_da(Daddatse_Hanyar_sadarwa_imel(AF_INET, "10.0.2.2", &Fiya_Daraja.sin_addr) == 1);
    struct timeval jira_Daraja = {0, 200000};
    Tabbatar_da(Canza_Hanyar_sadarwa_Saituna(종단점, SOL_SOCKET, SO_RCVTIMEO, &jira_Daraja, sizeof jira_Daraja) == 0);
    char Tarin_bayani[32];
    Tabbatar_da(자료전문받기(종단점, Tarin_bayani, sizeof Tarin_bayani, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    Tabbatar_da(자료전문보내기(종단점, "posix-udp", 9, 0, (struct sockaddr *)&Fiya_Daraja, sizeof Fiya_Daraja) == 9);
    Tsawo_Daraja = sizeof 받은주소;
    Tabbatar_da(recvfrom(종단점, (void *)0x00100000, 9, 0, NULL, NULL) == -1 && errno == EFAULT);
    Tabbatar_da(자료전문받기(종단점, Tarin_bayani, sizeof Tarin_bayani, 0, (struct sockaddr *)&받은주소, &Tsawo_Daraja) == 9);
    Tabbatar_da(memcmp(Tarin_bayani, "posix-udp", 9) == 0 && Tsawo_Daraja == 16);
    Tabbatar_da(받은주소.sin_port == Fiya_Daraja.sin_port && 받은주소.sin_addr.s_addr == Fiya_Daraja.sin_addr.s_addr);
    Tabbatar_da(sendto(종단점, "truncate", 8, 0, (struct sockaddr *)&Fiya_Daraja, sizeof Fiya_Daraja) == 8);
    Tabbatar_da(recvfrom(종단점, Tarin_bayani, 3, 0, NULL, NULL) == 3 && memcmp(Tarin_bayani, "tru", 3) == 0);
    Tabbatar_da(recvfrom(종단점, Tarin_bayani, sizeof Tarin_bayani, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    Tabbatar_da(sendto(종단점, NULL, 0, 0, (struct sockaddr *)&Fiya_Daraja, sizeof Fiya_Daraja) == 0);
    Tabbatar_da(recvfrom(종단점, NULL, 0, 0, NULL, NULL) == 0);
    Tabbatar_da(recvfrom(종단점, Tarin_bayani, sizeof Tarin_bayani, 0, NULL, NULL) == -1 && errno == EAGAIN);
    Tabbatar_da(close(종단점) == 0);
    puts("POSIX UDP CHECK PASS");
    return 0;
}
