#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

#define qiniseka(isimo) do { if (!(isimo)) { puts("POSIX UDP CHECK FAILED: " #isimo); return 1; } } while (0)
int main(int 인수개수, char **i_agumenti_Uhlu) {
    qiniseka(인수개수 == 2);
    int 접속번호 = 0;
    for (int isikhala_okufakwayo = 0; i_agumenti_Uhlu[1][isikhala_okufakwayo]; isikhala_okufakwayo++) {
        qiniseka(i_agumenti_Uhlu[1][isikhala_okufakwayo] >= '0' && i_agumenti_Uhlu[1][isikhala_okufakwayo] <= '9');
        접속번호 = 접속번호 * 10 + i_agumenti_Uhlu[1][isikhala_okufakwayo] - '0';
        qiniseka(접속번호 <= 65535);
    }
    int 종단점 = 통신종단점만들기(AF_INET, SOCK_DGRAM, 0);
    qiniseka(종단점 == 3);
    struct sockaddr_in endaweni_umklamo = {0}, untanga_inani = {0}, 받은주소 = {0};
    endaweni_umklamo.sin_family = AF_INET;
    socklen_t ubude_inani = sizeof endaweni_umklamo;
    qiniseka(통신주소읽기(종단점, (struct sockaddr *)&endaweni_umklamo, &ubude_inani) == 0 && endaweni_umklamo.sin_port == 0);
    qiniseka(i_BIND_ikheli(종단점, (struct sockaddr *)&endaweni_umklamo, sizeof endaweni_umklamo) == 0);
    qiniseka(통신주소읽기(종단점, (struct sockaddr *)&endaweni_umklamo, &ubude_inani) == 0 && ntohs(endaweni_umklamo.sin_port) >= 49152);
    qiniseka(i_BIND_ikheli(종단점, (struct sockaddr *)&endaweni_umklamo, sizeof endaweni_umklamo) == -1 && errno == EINVAL);
    int 둘째 = socket(AF_INET, SOCK_DGRAM, 0);
    qiniseka(bind(둘째, (struct sockaddr *)&endaweni_umklamo, sizeof endaweni_umklamo) == -1 && errno == EADDRINUSE);
    qiniseka(close(둘째) == 0);
    둘째 = dup(종단점);
    qiniseka(close(종단점) == 0); 종단점 = 둘째;
    untanga_inani.sin_family = AF_INET; untanga_inani.sin_port = 망차례짧은수(접속번호);
    qiniseka(zawula_iNethiwekhi_ikheli(AF_INET, "10.0.2.2", &untanga_inani.sin_addr) == 1);
    struct timeval 대기 = {0, 200000};
    qiniseka(guqula_iNethiwekhi_Amasethingi(종단점, SOL_SOCKET, SO_RCVTIMEO, &대기, sizeof 대기) == 0);
    char imininingwane[32];
    qiniseka(자료전문받기(종단점, imininingwane, sizeof imininingwane, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    qiniseka(자료전문보내기(종단점, "posix-udp", 9, 0, (struct sockaddr *)&untanga_inani, sizeof untanga_inani) == 9);
    ubude_inani = sizeof 받은주소;
    qiniseka(recvfrom(종단점, (void *)0x00100000, 9, 0, NULL, NULL) == -1 && errno == EFAULT);
    qiniseka(자료전문받기(종단점, imininingwane, sizeof imininingwane, 0, (struct sockaddr *)&받은주소, &ubude_inani) == 9);
    qiniseka(memcmp(imininingwane, "posix-udp", 9) == 0 && ubude_inani == 16);
    qiniseka(받은주소.sin_port == untanga_inani.sin_port && 받은주소.sin_addr.s_addr == untanga_inani.sin_addr.s_addr);
    qiniseka(sendto(종단점, "truncate", 8, 0, (struct sockaddr *)&untanga_inani, sizeof untanga_inani) == 8);
    qiniseka(recvfrom(종단점, imininingwane, 3, 0, NULL, NULL) == 3 && memcmp(imininingwane, "tru", 3) == 0);
    qiniseka(recvfrom(종단점, imininingwane, sizeof imininingwane, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    qiniseka(sendto(종단점, NULL, 0, 0, (struct sockaddr *)&untanga_inani, sizeof untanga_inani) == 0);
    qiniseka(recvfrom(종단점, NULL, 0, 0, NULL, NULL) == 0);
    qiniseka(recvfrom(종단점, imininingwane, sizeof imininingwane, 0, NULL, NULL) == -1 && errno == EAGAIN);
    qiniseka(close(종단점) == 0);
    puts("POSIX UDP CHECK PASS");
    return 0;
}
