#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

#define barla(şert) do { if (!(şert)) { puts("POSIX UDP CHECK FAILED: " #şert); return 1; } } while (0)
int main(int 인수개수, char **argument_Sanaw) {
    barla(인수개수 == 2);
    int 접속번호 = 0;
    for (int ýer_girizmeklik = 0; argument_Sanaw[1][ýer_girizmeklik]; ýer_girizmeklik++) {
        barla(argument_Sanaw[1][ýer_girizmeklik] >= '0' && argument_Sanaw[1][ýer_girizmeklik] <= '9');
        접속번호 = 접속번호 * 10 + argument_Sanaw[1][ýer_girizmeklik] - '0';
        barla(접속번호 <= 65535);
    }
    int 종단점 = 통신종단점만들기(AF_INET, SOCK_DGRAM, 0);
    barla(종단점 == 3);
    struct sockaddr_in ýerli_elýeterli_gor = {0}, deň_derejeli_düwün_baha = {0}, 받은주소 = {0};
    ýerli_elýeterli_gor.sin_family = AF_INET;
    socklen_t dowamlylyk_baha = sizeof ýerli_elýeterli_gor;
    barla(통신주소읽기(종단점, (struct sockaddr *)&ýerli_elýeterli_gor, &dowamlylyk_baha) == 0 && ýerli_elýeterli_gor.sin_port == 0);
    barla(BIND_salgy(종단점, (struct sockaddr *)&ýerli_elýeterli_gor, sizeof ýerli_elýeterli_gor) == 0);
    barla(통신주소읽기(종단점, (struct sockaddr *)&ýerli_elýeterli_gor, &dowamlylyk_baha) == 0 && ntohs(ýerli_elýeterli_gor.sin_port) >= 49152);
    barla(BIND_salgy(종단점, (struct sockaddr *)&ýerli_elýeterli_gor, sizeof ýerli_elýeterli_gor) == -1 && errno == EINVAL);
    int 둘째 = socket(AF_INET, SOCK_DGRAM, 0);
    barla(bind(둘째, (struct sockaddr *)&ýerli_elýeterli_gor, sizeof ýerli_elýeterli_gor) == -1 && errno == EADDRINUSE);
    barla(close(둘째) == 0);
    둘째 = dup(종단점);
    barla(close(종단점) == 0); 종단점 = 둘째;
    deň_derejeli_düwün_baha.sin_family = AF_INET; deň_derejeli_düwün_baha.sin_port = 망차례짧은수(접속번호);
    barla(seljer_Tor_salgy(AF_INET, "10.0.2.2", &deň_derejeli_düwün_baha.sin_addr) == 1);
    struct timeval 대기 = {0, 200000};
    barla(üýtget_Tor_Sazlamalar(종단점, SOL_SOCKET, SO_RCVTIMEO, &대기, sizeof 대기) == 0);
    char maglumat[32];
    barla(자료전문받기(종단점, maglumat, sizeof maglumat, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    barla(자료전문보내기(종단점, "posix-udp", 9, 0, (struct sockaddr *)&deň_derejeli_düwün_baha, sizeof deň_derejeli_düwün_baha) == 9);
    dowamlylyk_baha = sizeof 받은주소;
    barla(recvfrom(종단점, (void *)0x00100000, 9, 0, NULL, NULL) == -1 && errno == EFAULT);
    barla(자료전문받기(종단점, maglumat, sizeof maglumat, 0, (struct sockaddr *)&받은주소, &dowamlylyk_baha) == 9);
    barla(memcmp(maglumat, "posix-udp", 9) == 0 && dowamlylyk_baha == 16);
    barla(받은주소.sin_port == deň_derejeli_düwün_baha.sin_port && 받은주소.sin_addr.s_addr == deň_derejeli_düwün_baha.sin_addr.s_addr);
    barla(sendto(종단점, "truncate", 8, 0, (struct sockaddr *)&deň_derejeli_düwün_baha, sizeof deň_derejeli_düwün_baha) == 8);
    barla(recvfrom(종단점, maglumat, 3, 0, NULL, NULL) == 3 && memcmp(maglumat, "tru", 3) == 0);
    barla(recvfrom(종단점, maglumat, sizeof maglumat, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    barla(sendto(종단점, NULL, 0, 0, (struct sockaddr *)&deň_derejeli_düwün_baha, sizeof deň_derejeli_düwün_baha) == 0);
    barla(recvfrom(종단점, NULL, 0, 0, NULL, NULL) == 0);
    barla(recvfrom(종단점, maglumat, sizeof maglumat, 0, NULL, NULL) == -1 && errno == EAGAIN);
    barla(close(종단점) == 0);
    puts("POSIX UDP CHECK PASS");
    return 0;
}
