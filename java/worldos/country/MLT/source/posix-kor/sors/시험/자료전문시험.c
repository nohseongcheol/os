#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

#define vverifika(kondizzjoni) do { if (!(kondizzjoni)) { puts("POSIX UDP CHECK FAILED: " #kondizzjoni); return 1; } } while (0)
int main(int 인수개수, char **argument_Lista) {
    vverifika(인수개수 == 2);
    int 접속번호 = 0;
    for (int slott_entrata = 0; argument_Lista[1][slott_entrata]; slott_entrata++) {
        vverifika(argument_Lista[1][slott_entrata] >= '0' && argument_Lista[1][slott_entrata] <= '9');
        접속번호 = 접속번호 * 10 + argument_Lista[1][slott_entrata] - '0';
        vverifika(접속번호 <= 65535);
    }
    int 종단점 = 통신종단점만들기(AF_INET, SOCK_DGRAM, 0);
    vverifika(종단점 == 3);
    struct sockaddr_in lokali_ambitu = {0}, peer_VALUE = {0}, RECEIVED_ADDRESS = {0};
    lokali_ambitu.sin_family = AF_INET;
    socklen_t tul_VALUE = sizeof lokali_ambitu;
    vverifika(통신주소읽기(종단점, (struct sockaddr *)&lokali_ambitu, &tul_VALUE) == 0 && lokali_ambitu.sin_port == 0);
    vverifika(BIND_ADDRESS(종단점, (struct sockaddr *)&lokali_ambitu, sizeof lokali_ambitu) == 0);
    vverifika(통신주소읽기(종단점, (struct sockaddr *)&lokali_ambitu, &tul_VALUE) == 0 && ntohs(lokali_ambitu.sin_port) >= 49152);
    vverifika(BIND_ADDRESS(종단점, (struct sockaddr *)&lokali_ambitu, sizeof lokali_ambitu) == -1 && errno == EINVAL);
    int 둘째 = socket(AF_INET, SOCK_DGRAM, 0);
    vverifika(bind(둘째, (struct sockaddr *)&lokali_ambitu, sizeof lokali_ambitu) == -1 && errno == EADDRINUSE);
    vverifika(close(둘째) == 0);
    둘째 = dup(종단점);
    vverifika(close(종단점) == 0); 종단점 = 둘째;
    peer_VALUE.sin_family = AF_INET; peer_VALUE.sin_port = 망차례짧은수(접속번호);
    vverifika(analizza_netwerk_ADDRESS(AF_INET, "10.0.2.2", &peer_VALUE.sin_addr) == 1);
    struct timeval 대기 = {0, 200000};
    vverifika(bidel_netwerk_Settings(종단점, SOL_SOCKET, SO_RCVTIMEO, &대기, sizeof 대기) == 0);
    char data[32];
    vverifika(자료전문받기(종단점, data, sizeof data, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    vverifika(자료전문보내기(종단점, "posix-udp", 9, 0, (struct sockaddr *)&peer_VALUE, sizeof peer_VALUE) == 9);
    tul_VALUE = sizeof RECEIVED_ADDRESS;
    vverifika(recvfrom(종단점, (void *)0x00100000, 9, 0, NULL, NULL) == -1 && errno == EFAULT);
    vverifika(자료전문받기(종단점, data, sizeof data, 0, (struct sockaddr *)&RECEIVED_ADDRESS, &tul_VALUE) == 9);
    vverifika(memcmp(data, "posix-udp", 9) == 0 && tul_VALUE == 16);
    vverifika(RECEIVED_ADDRESS.sin_port == peer_VALUE.sin_port && RECEIVED_ADDRESS.sin_addr.s_addr == peer_VALUE.sin_addr.s_addr);
    vverifika(sendto(종단점, "truncate", 8, 0, (struct sockaddr *)&peer_VALUE, sizeof peer_VALUE) == 8);
    vverifika(recvfrom(종단점, data, 3, 0, NULL, NULL) == 3 && memcmp(data, "tru", 3) == 0);
    vverifika(recvfrom(종단점, data, sizeof data, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    vverifika(sendto(종단점, NULL, 0, 0, (struct sockaddr *)&peer_VALUE, sizeof peer_VALUE) == 0);
    vverifika(recvfrom(종단점, NULL, 0, 0, NULL, NULL) == 0);
    vverifika(recvfrom(종단점, data, sizeof data, 0, NULL, NULL) == -1 && errno == EAGAIN);
    vverifika(close(종단점) == 0);
    puts("POSIX UDP CHECK PASS");
    return 0;
}
