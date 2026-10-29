#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

#define dilysu(cyflwr) do { if (!(cyflwr)) { puts("POSIX UDP CHECK FAILED: " #cyflwr); return 1; } } while (0)
int main(int 인수개수, char **arg_Rhestr) {
    dilysu(인수개수 == 2);
    int rhif_porth = 0;
    for (int slot_cofnod = 0; arg_Rhestr[1][slot_cofnod]; slot_cofnod++) {
        dilysu(arg_Rhestr[1][slot_cofnod] >= '0' && arg_Rhestr[1][slot_cofnod] <= '9');
        rhif_porth = rhif_porth * 10 + arg_Rhestr[1][slot_cofnod] - '0';
        dilysu(rhif_porth <= 65535);
    }
    int 종단점 = 통신종단점만들기(AF_INET, SOCK_DGRAM, 0);
    dilysu(종단점 == 3);
    struct sockaddr_in lleol_cwmpas = {0}, cymar_VALUE = {0}, RECEIVED_ADDRESS = {0};
    lleol_cwmpas.sin_family = AF_INET;
    socklen_t hyd_VALUE = sizeof lleol_cwmpas;
    dilysu(통신주소읽기(종단점, (struct sockaddr *)&lleol_cwmpas, &hyd_VALUE) == 0 && lleol_cwmpas.sin_port == 0);
    dilysu(BIND_ADDRESS(종단점, (struct sockaddr *)&lleol_cwmpas, sizeof lleol_cwmpas) == 0);
    dilysu(통신주소읽기(종단점, (struct sockaddr *)&lleol_cwmpas, &hyd_VALUE) == 0 && ntohs(lleol_cwmpas.sin_port) >= 49152);
    dilysu(BIND_ADDRESS(종단점, (struct sockaddr *)&lleol_cwmpas, sizeof lleol_cwmpas) == -1 && errno == EINVAL);
    int 둘째 = socket(AF_INET, SOCK_DGRAM, 0);
    dilysu(bind(둘째, (struct sockaddr *)&lleol_cwmpas, sizeof lleol_cwmpas) == -1 && errno == EADDRINUSE);
    dilysu(close(둘째) == 0);
    둘째 = dup(종단점);
    dilysu(close(종단점) == 0); 종단점 = 둘째;
    cymar_VALUE.sin_family = AF_INET; cymar_VALUE.sin_port = 망차례짧은수(rhif_porth);
    dilysu(dosrannu_Rhwydwaith_ADDRESS(AF_INET, "10.0.2.2", &cymar_VALUE.sin_addr) == 1);
    struct timeval aros_VALUE = {0, 200000};
    dilysu(newid_Rhwydwaith_Gosodiadau(종단점, SOL_SOCKET, SO_RCVTIMEO, &aros_VALUE, sizeof aros_VALUE) == 0);
    char data[32];
    dilysu(자료전문받기(종단점, data, sizeof data, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    dilysu(자료전문보내기(종단점, "posix-udp", 9, 0, (struct sockaddr *)&cymar_VALUE, sizeof cymar_VALUE) == 9);
    hyd_VALUE = sizeof RECEIVED_ADDRESS;
    dilysu(recvfrom(종단점, (void *)0x00100000, 9, 0, NULL, NULL) == -1 && errno == EFAULT);
    dilysu(자료전문받기(종단점, data, sizeof data, 0, (struct sockaddr *)&RECEIVED_ADDRESS, &hyd_VALUE) == 9);
    dilysu(memcmp(data, "posix-udp", 9) == 0 && hyd_VALUE == 16);
    dilysu(RECEIVED_ADDRESS.sin_port == cymar_VALUE.sin_port && RECEIVED_ADDRESS.sin_addr.s_addr == cymar_VALUE.sin_addr.s_addr);
    dilysu(sendto(종단점, "truncate", 8, 0, (struct sockaddr *)&cymar_VALUE, sizeof cymar_VALUE) == 8);
    dilysu(recvfrom(종단점, data, 3, 0, NULL, NULL) == 3 && memcmp(data, "tru", 3) == 0);
    dilysu(recvfrom(종단점, data, sizeof data, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    dilysu(sendto(종단점, NULL, 0, 0, (struct sockaddr *)&cymar_VALUE, sizeof cymar_VALUE) == 0);
    dilysu(recvfrom(종단점, NULL, 0, 0, NULL, NULL) == 0);
    dilysu(recvfrom(종단점, data, sizeof data, 0, NULL, NULL) == -1 && errno == EAGAIN);
    dilysu(close(종단점) == 0);
    puts("POSIX UDP CHECK PASS");
    return 0;
}
