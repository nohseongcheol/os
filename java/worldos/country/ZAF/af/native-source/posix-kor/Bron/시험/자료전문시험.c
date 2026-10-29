#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

#define verifieer(toestand) do { if (!(toestand)) { puts("POSIX UDP CHECK FAILED: " #toestand); return 1; } } while (0)
int main(int 인수개수, char **argument_Lys) {
    verifieer(인수개수 == 2);
    int 접속번호 = 0;
    for (int gleuf_inskrywing = 0; argument_Lys[1][gleuf_inskrywing]; gleuf_inskrywing++) {
        verifieer(argument_Lys[1][gleuf_inskrywing] >= '0' && argument_Lys[1][gleuf_inskrywing] <= '9');
        접속번호 = 접속번호 * 10 + argument_Lys[1][gleuf_inskrywing] - '0';
        verifieer(접속번호 <= 65535);
    }
    int 종단점 = 통신종단점만들기(AF_INET, SOCK_DGRAM, 0);
    verifieer(종단점 == 3);
    struct sockaddr_in lokaal_bestek = {0}, portuur_VALUE = {0}, RECEIVED_adres = {0};
    lokaal_bestek.sin_family = AF_INET;
    socklen_t lengte_VALUE = sizeof lokaal_bestek;
    verifieer(통신주소읽기(종단점, (struct sockaddr *)&lokaal_bestek, &lengte_VALUE) == 0 && lokaal_bestek.sin_port == 0);
    verifieer(BIND_adres(종단점, (struct sockaddr *)&lokaal_bestek, sizeof lokaal_bestek) == 0);
    verifieer(통신주소읽기(종단점, (struct sockaddr *)&lokaal_bestek, &lengte_VALUE) == 0 && ntohs(lokaal_bestek.sin_port) >= 49152);
    verifieer(BIND_adres(종단점, (struct sockaddr *)&lokaal_bestek, sizeof lokaal_bestek) == -1 && errno == EINVAL);
    int 둘째 = socket(AF_INET, SOCK_DGRAM, 0);
    verifieer(bind(둘째, (struct sockaddr *)&lokaal_bestek, sizeof lokaal_bestek) == -1 && errno == EADDRINUSE);
    verifieer(close(둘째) == 0);
    둘째 = dup(종단점);
    verifieer(close(종단점) == 0); 종단점 = 둘째;
    portuur_VALUE.sin_family = AF_INET; portuur_VALUE.sin_port = 망차례짧은수(접속번호);
    verifieer(ontleed_Netwerk_adres(AF_INET, "10.0.2.2", &portuur_VALUE.sin_addr) == 1);
    struct timeval wag_VALUE = {0, 200000};
    verifieer(verander_Netwerk_Instellings(종단점, SOL_SOCKET, SO_RCVTIMEO, &wag_VALUE, sizeof wag_VALUE) == 0);
    char data[32];
    verifieer(자료전문받기(종단점, data, sizeof data, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    verifieer(자료전문보내기(종단점, "posix-udp", 9, 0, (struct sockaddr *)&portuur_VALUE, sizeof portuur_VALUE) == 9);
    lengte_VALUE = sizeof RECEIVED_adres;
    verifieer(recvfrom(종단점, (void *)0x00100000, 9, 0, NULL, NULL) == -1 && errno == EFAULT);
    verifieer(자료전문받기(종단점, data, sizeof data, 0, (struct sockaddr *)&RECEIVED_adres, &lengte_VALUE) == 9);
    verifieer(memcmp(data, "posix-udp", 9) == 0 && lengte_VALUE == 16);
    verifieer(RECEIVED_adres.sin_port == portuur_VALUE.sin_port && RECEIVED_adres.sin_addr.s_addr == portuur_VALUE.sin_addr.s_addr);
    verifieer(sendto(종단점, "truncate", 8, 0, (struct sockaddr *)&portuur_VALUE, sizeof portuur_VALUE) == 8);
    verifieer(recvfrom(종단점, data, 3, 0, NULL, NULL) == 3 && memcmp(data, "tru", 3) == 0);
    verifieer(recvfrom(종단점, data, sizeof data, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    verifieer(sendto(종단점, NULL, 0, 0, (struct sockaddr *)&portuur_VALUE, sizeof portuur_VALUE) == 0);
    verifieer(recvfrom(종단점, NULL, 0, 0, NULL, NULL) == 0);
    verifieer(recvfrom(종단점, data, sizeof data, 0, NULL, NULL) == -1 && errno == EAGAIN);
    verifieer(close(종단점) == 0);
    puts("POSIX UDP CHECK PASS");
    return 0;
}
