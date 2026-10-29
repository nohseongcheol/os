#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

#define fíoraigh(coinníoll) do { if (!(coinníoll)) { puts("POSIX UDP CHECK FAILED: " #coinníoll); return 1; } } while (0)
int main(int 인수개수, char **argóint_Liosta) {
    fíoraigh(인수개수 == 2);
    int uimhir_phoirt = 0;
    for (int spás_iontráil = 0; argóint_Liosta[1][spás_iontráil]; spás_iontráil++) {
        fíoraigh(argóint_Liosta[1][spás_iontráil] >= '0' && argóint_Liosta[1][spás_iontráil] <= '9');
        uimhir_phoirt = uimhir_phoirt * 10 + argóint_Liosta[1][spás_iontráil] - '0';
        fíoraigh(uimhir_phoirt <= 65535);
    }
    int 종단점 = 통신종단점만들기(AF_INET, SOCK_DGRAM, 0);
    fíoraigh(종단점 == 3);
    struct sockaddr_in logánta_scóip = {0}, piara_VALUE = {0}, RECEIVED_ADDRESS = {0};
    logánta_scóip.sin_family = AF_INET;
    socklen_t fad_VALUE = sizeof logánta_scóip;
    fíoraigh(통신주소읽기(종단점, (struct sockaddr *)&logánta_scóip, &fad_VALUE) == 0 && logánta_scóip.sin_port == 0);
    fíoraigh(BIND_ADDRESS(종단점, (struct sockaddr *)&logánta_scóip, sizeof logánta_scóip) == 0);
    fíoraigh(통신주소읽기(종단점, (struct sockaddr *)&logánta_scóip, &fad_VALUE) == 0 && ntohs(logánta_scóip.sin_port) >= 49152);
    fíoraigh(BIND_ADDRESS(종단점, (struct sockaddr *)&logánta_scóip, sizeof logánta_scóip) == -1 && errno == EINVAL);
    int 둘째 = socket(AF_INET, SOCK_DGRAM, 0);
    fíoraigh(bind(둘째, (struct sockaddr *)&logánta_scóip, sizeof logánta_scóip) == -1 && errno == EADDRINUSE);
    fíoraigh(close(둘째) == 0);
    둘째 = dup(종단점);
    fíoraigh(close(종단점) == 0); 종단점 = 둘째;
    piara_VALUE.sin_family = AF_INET; piara_VALUE.sin_port = 망차례짧은수(uimhir_phoirt);
    fíoraigh(parsáil_Líonra_ADDRESS(AF_INET, "10.0.2.2", &piara_VALUE.sin_addr) == 1);
    struct timeval 대기 = {0, 200000};
    fíoraigh(athraigh_Líonra_Socruithe(종단점, SOL_SOCKET, SO_RCVTIMEO, &대기, sizeof 대기) == 0);
    char sonraí[32];
    fíoraigh(자료전문받기(종단점, sonraí, sizeof sonraí, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    fíoraigh(자료전문보내기(종단점, "posix-udp", 9, 0, (struct sockaddr *)&piara_VALUE, sizeof piara_VALUE) == 9);
    fad_VALUE = sizeof RECEIVED_ADDRESS;
    fíoraigh(recvfrom(종단점, (void *)0x00100000, 9, 0, NULL, NULL) == -1 && errno == EFAULT);
    fíoraigh(자료전문받기(종단점, sonraí, sizeof sonraí, 0, (struct sockaddr *)&RECEIVED_ADDRESS, &fad_VALUE) == 9);
    fíoraigh(memcmp(sonraí, "posix-udp", 9) == 0 && fad_VALUE == 16);
    fíoraigh(RECEIVED_ADDRESS.sin_port == piara_VALUE.sin_port && RECEIVED_ADDRESS.sin_addr.s_addr == piara_VALUE.sin_addr.s_addr);
    fíoraigh(sendto(종단점, "truncate", 8, 0, (struct sockaddr *)&piara_VALUE, sizeof piara_VALUE) == 8);
    fíoraigh(recvfrom(종단점, sonraí, 3, 0, NULL, NULL) == 3 && memcmp(sonraí, "tru", 3) == 0);
    fíoraigh(recvfrom(종단점, sonraí, sizeof sonraí, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    fíoraigh(sendto(종단점, NULL, 0, 0, (struct sockaddr *)&piara_VALUE, sizeof piara_VALUE) == 0);
    fíoraigh(recvfrom(종단점, NULL, 0, 0, NULL, NULL) == 0);
    fíoraigh(recvfrom(종단점, sonraí, sizeof sonraí, 0, NULL, NULL) == -1 && errno == EAGAIN);
    fíoraigh(close(종단점) == 0);
    puts("POSIX UDP CHECK PASS");
    return 0;
}
