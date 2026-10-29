#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

#define nalunairli_1aacb54c(qanuinniq) do { if (!(qanuinniq)) { puts("POSIX UDP CHECK FAILED: " #qanuinniq); return 1; } } while (0)
int main(int 인수개수, char **aturniqarnirainiq_Titiqpalliagaq) {
    nalunairli_1aacb54c(인수개수 == 2);
    int 접속번호 = 0;
    for (int 칸 = 0; aturniqarnirainiq_Titiqpalliagaq[1][칸]; 칸++) {
        nalunairli_1aacb54c(aturniqarnirainiq_Titiqpalliagaq[1][칸] >= '0' && aturniqarnirainiq_Titiqpalliagaq[1][칸] <= '9');
        접속번호 = 접속번호 * 10 + aturniqarnirainiq_Titiqpalliagaq[1][칸] - '0';
        nalunairli_1aacb54c(접속번호 <= 65535);
    }
    int 종단점 = 통신종단점만들기(AF_INET, SOCK_DGRAM, 0);
    nalunairli_1aacb54c(종단점 == 3);
    struct sockaddr_in tamaani_qinirvik = {0}, ilagijaujuq_atuutilik = {0}, 받은주소 = {0};
    tamaani_qinirvik.sin_family = AF_INET;
    socklen_t takininga_atuutilik = sizeof tamaani_qinirvik;
    nalunairli_1aacb54c(통신주소읽기(종단점, (struct sockaddr *)&tamaani_qinirvik, &takininga_atuutilik) == 0 && tamaani_qinirvik.sin_port == 0);
    nalunairli_1aacb54c(unittilli_turaarut(종단점, (struct sockaddr *)&tamaani_qinirvik, sizeof tamaani_qinirvik) == 0);
    nalunairli_1aacb54c(통신주소읽기(종단점, (struct sockaddr *)&tamaani_qinirvik, &takininga_atuutilik) == 0 && ntohs(tamaani_qinirvik.sin_port) >= 49152);
    nalunairli_1aacb54c(unittilli_turaarut(종단점, (struct sockaddr *)&tamaani_qinirvik, sizeof tamaani_qinirvik) == -1 && errno == EINVAL);
    int 둘째 = socket(AF_INET, SOCK_DGRAM, 0);
    nalunairli_1aacb54c(bind(둘째, (struct sockaddr *)&tamaani_qinirvik, sizeof tamaani_qinirvik) == -1 && errno == EADDRINUSE);
    nalunairli_1aacb54c(close(둘째) == 0);
    둘째 = dup(종단점);
    nalunairli_1aacb54c(close(종단점) == 0); 종단점 = 둘째;
    ilagijaujuq_atuutilik.sin_family = AF_INET; ilagijaujuq_atuutilik.sin_port = 망차례짧은수(접속번호);
    nalunairli_1aacb54c(agguqtuut_Kasuqatigiitsimajut_turaarut(AF_INET, "10.0.2.2", &ilagijaujuq_atuutilik.sin_addr) == 1);
    struct timeval 대기 = {0, 200000};
    nalunairli_1aacb54c(통신설정바꾸기(종단점, SOL_SOCKET, SO_RCVTIMEO, &대기, sizeof 대기) == 0);
    char titiqqat[32];
    nalunairli_1aacb54c(자료전문받기(종단점, titiqqat, sizeof titiqqat, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    nalunairli_1aacb54c(자료전문보내기(종단점, "posix-udp", 9, 0, (struct sockaddr *)&ilagijaujuq_atuutilik, sizeof ilagijaujuq_atuutilik) == 9);
    takininga_atuutilik = sizeof 받은주소;
    nalunairli_1aacb54c(recvfrom(종단점, (void *)0x00100000, 9, 0, NULL, NULL) == -1 && errno == EFAULT);
    nalunairli_1aacb54c(자료전문받기(종단점, titiqqat, sizeof titiqqat, 0, (struct sockaddr *)&받은주소, &takininga_atuutilik) == 9);
    nalunairli_1aacb54c(memcmp(titiqqat, "posix-udp", 9) == 0 && takininga_atuutilik == 16);
    nalunairli_1aacb54c(받은주소.sin_port == ilagijaujuq_atuutilik.sin_port && 받은주소.sin_addr.s_addr == ilagijaujuq_atuutilik.sin_addr.s_addr);
    nalunairli_1aacb54c(sendto(종단점, "truncate", 8, 0, (struct sockaddr *)&ilagijaujuq_atuutilik, sizeof ilagijaujuq_atuutilik) == 8);
    nalunairli_1aacb54c(recvfrom(종단점, titiqqat, 3, 0, NULL, NULL) == 3 && memcmp(titiqqat, "tru", 3) == 0);
    nalunairli_1aacb54c(recvfrom(종단점, titiqqat, sizeof titiqqat, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    nalunairli_1aacb54c(sendto(종단점, NULL, 0, 0, (struct sockaddr *)&ilagijaujuq_atuutilik, sizeof ilagijaujuq_atuutilik) == 0);
    nalunairli_1aacb54c(recvfrom(종단점, NULL, 0, 0, NULL, NULL) == 0);
    nalunairli_1aacb54c(recvfrom(종단점, titiqqat, sizeof titiqqat, 0, NULL, NULL) == -1 && errno == EAGAIN);
    nalunairli_1aacb54c(close(종단점) == 0);
    puts("POSIX UDP CHECK PASS");
    return 0;
}
