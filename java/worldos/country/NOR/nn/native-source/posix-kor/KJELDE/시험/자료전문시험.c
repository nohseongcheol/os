#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

#define stadfeste(tilstand) do { if (!(tilstand)) { puts("POSIX UDP CHECK FAILED: " #tilstand); return 1; } } while (0)
int main(int 인수개수, char **argument_Liste) {
    stadfeste(인수개수 == 2);
    int portnummer = 0;
    for (int felt_oppføring = 0; argument_Liste[1][felt_oppføring]; felt_oppføring++) {
        stadfeste(argument_Liste[1][felt_oppføring] >= '0' && argument_Liste[1][felt_oppføring] <= '9');
        portnummer = portnummer * 10 + argument_Liste[1][felt_oppføring] - '0';
        stadfeste(portnummer <= 65535);
    }
    int endepunkt_VALUE = Opprett_endepunkt(AF_INET, SOCK_DGRAM, 0);
    stadfeste(endepunkt_VALUE == 3);
    struct sockaddr_in lokal_område = {0}, node_VALUE_6a3b6fa7 = {0}, RECEIVED_ADDRESS = {0};
    lokal_område.sin_family = AF_INET;
    socklen_t lengd_VALUE = sizeof lokal_område;
    stadfeste(통신주소읽기(endepunkt_VALUE, (struct sockaddr *)&lokal_område, &lengd_VALUE) == 0 && lokal_område.sin_port == 0);
    stadfeste(BIND_ADDRESS(endepunkt_VALUE, (struct sockaddr *)&lokal_område, sizeof lokal_område) == 0);
    stadfeste(통신주소읽기(endepunkt_VALUE, (struct sockaddr *)&lokal_område, &lengd_VALUE) == 0 && ntohs(lokal_område.sin_port) >= 49152);
    stadfeste(BIND_ADDRESS(endepunkt_VALUE, (struct sockaddr *)&lokal_område, sizeof lokal_område) == -1 && errno == EINVAL);
    int 둘째 = socket(AF_INET, SOCK_DGRAM, 0);
    stadfeste(bind(둘째, (struct sockaddr *)&lokal_område, sizeof lokal_område) == -1 && errno == EADDRINUSE);
    stadfeste(close(둘째) == 0);
    둘째 = dup(endepunkt_VALUE);
    stadfeste(close(endepunkt_VALUE) == 0); endepunkt_VALUE = 둘째;
    node_VALUE_6a3b6fa7.sin_family = AF_INET; node_VALUE_6a3b6fa7.sin_port = 망차례짧은수(portnummer);
    stadfeste(dele_opp_Nettverk_ADDRESS(AF_INET, "10.0.2.2", &node_VALUE_6a3b6fa7.sin_addr) == 1);
    struct timeval vent_VALUE = {0, 200000};
    stadfeste(endre_Nettverk_Innstillingar(endepunkt_VALUE, SOL_SOCKET, SO_RCVTIMEO, &vent_VALUE, sizeof vent_VALUE) == 0);
    char data[32];
    stadfeste(자료전문받기(endepunkt_VALUE, data, sizeof data, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    stadfeste(자료전문보내기(endepunkt_VALUE, "posix-udp", 9, 0, (struct sockaddr *)&node_VALUE_6a3b6fa7, sizeof node_VALUE_6a3b6fa7) == 9);
    lengd_VALUE = sizeof RECEIVED_ADDRESS;
    stadfeste(recvfrom(endepunkt_VALUE, (void *)0x00100000, 9, 0, NULL, NULL) == -1 && errno == EFAULT);
    stadfeste(자료전문받기(endepunkt_VALUE, data, sizeof data, 0, (struct sockaddr *)&RECEIVED_ADDRESS, &lengd_VALUE) == 9);
    stadfeste(memcmp(data, "posix-udp", 9) == 0 && lengd_VALUE == 16);
    stadfeste(RECEIVED_ADDRESS.sin_port == node_VALUE_6a3b6fa7.sin_port && RECEIVED_ADDRESS.sin_addr.s_addr == node_VALUE_6a3b6fa7.sin_addr.s_addr);
    stadfeste(sendto(endepunkt_VALUE, "truncate", 8, 0, (struct sockaddr *)&node_VALUE_6a3b6fa7, sizeof node_VALUE_6a3b6fa7) == 8);
    stadfeste(recvfrom(endepunkt_VALUE, data, 3, 0, NULL, NULL) == 3 && memcmp(data, "tru", 3) == 0);
    stadfeste(recvfrom(endepunkt_VALUE, data, sizeof data, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    stadfeste(sendto(endepunkt_VALUE, NULL, 0, 0, (struct sockaddr *)&node_VALUE_6a3b6fa7, sizeof node_VALUE_6a3b6fa7) == 0);
    stadfeste(recvfrom(endepunkt_VALUE, NULL, 0, 0, NULL, NULL) == 0);
    stadfeste(recvfrom(endepunkt_VALUE, data, sizeof data, 0, NULL, NULL) == -1 && errno == EAGAIN);
    stadfeste(close(endepunkt_VALUE) == 0);
    puts("POSIX UDP CHECK PASS");
    return 0;
}
