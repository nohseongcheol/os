#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

#define kgonthiša(seemo) do { if (!(seemo)) { puts("POSIX UDP CHECK FAILED: " #seemo); return 1; } } while (0)
int main(int 인수개수, char **akumente_Lenaneo) {
    kgonthiša(인수개수 == 2);
    int 접속번호 = 0;
    for (int sekgobana_go_tsenya_tshedimošo = 0; akumente_Lenaneo[1][sekgobana_go_tsenya_tshedimošo]; sekgobana_go_tsenya_tshedimošo++) {
        kgonthiša(akumente_Lenaneo[1][sekgobana_go_tsenya_tshedimošo] >= '0' && akumente_Lenaneo[1][sekgobana_go_tsenya_tshedimošo] <= '9');
        접속번호 = 접속번호 * 10 + akumente_Lenaneo[1][sekgobana_go_tsenya_tshedimošo] - '0';
        kgonthiša(접속번호 <= 65535);
    }
    int 종단점 = 통신종단점만들기(AF_INET, SOCK_DGRAM, 0);
    kgonthiša(종단점 == 3);
    struct sockaddr_in kgauswi_skoupo = {0}, sedirišwa_sa_legoro_le_tee_boleng = {0}, 받은주소 = {0};
    kgauswi_skoupo.sin_family = AF_INET;
    socklen_t botelele_boleng = sizeof kgauswi_skoupo;
    kgonthiša(통신주소읽기(종단점, (struct sockaddr *)&kgauswi_skoupo, &botelele_boleng) == 0 && kgauswi_skoupo.sin_port == 0);
    kgonthiša(tlama_atrese(종단점, (struct sockaddr *)&kgauswi_skoupo, sizeof kgauswi_skoupo) == 0);
    kgonthiša(통신주소읽기(종단점, (struct sockaddr *)&kgauswi_skoupo, &botelele_boleng) == 0 && ntohs(kgauswi_skoupo.sin_port) >= 49152);
    kgonthiša(tlama_atrese(종단점, (struct sockaddr *)&kgauswi_skoupo, sizeof kgauswi_skoupo) == -1 && errno == EINVAL);
    int 둘째 = socket(AF_INET, SOCK_DGRAM, 0);
    kgonthiša(bind(둘째, (struct sockaddr *)&kgauswi_skoupo, sizeof kgauswi_skoupo) == -1 && errno == EADDRINUSE);
    kgonthiša(close(둘째) == 0);
    둘째 = dup(종단점);
    kgonthiša(close(종단점) == 0); 종단점 = 둘째;
    sedirišwa_sa_legoro_le_tee_boleng.sin_family = AF_INET; sedirišwa_sa_legoro_le_tee_boleng.sin_port = 망차례짧은수(접속번호);
    kgonthiša(ripaganya_Netweke_atrese(AF_INET, "10.0.2.2", &sedirišwa_sa_legoro_le_tee_boleng.sin_addr) == 1);
    struct timeval 대기 = {0, 200000};
    kgonthiša(fetoša_Netweke_Dipeakanyo(종단점, SOL_SOCKET, SO_RCVTIMEO, &대기, sizeof 대기) == 0);
    char data[32];
    kgonthiša(자료전문받기(종단점, data, sizeof data, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    kgonthiša(자료전문보내기(종단점, "posix-udp", 9, 0, (struct sockaddr *)&sedirišwa_sa_legoro_le_tee_boleng, sizeof sedirišwa_sa_legoro_le_tee_boleng) == 9);
    botelele_boleng = sizeof 받은주소;
    kgonthiša(recvfrom(종단점, (void *)0x00100000, 9, 0, NULL, NULL) == -1 && errno == EFAULT);
    kgonthiša(자료전문받기(종단점, data, sizeof data, 0, (struct sockaddr *)&받은주소, &botelele_boleng) == 9);
    kgonthiša(memcmp(data, "posix-udp", 9) == 0 && botelele_boleng == 16);
    kgonthiša(받은주소.sin_port == sedirišwa_sa_legoro_le_tee_boleng.sin_port && 받은주소.sin_addr.s_addr == sedirišwa_sa_legoro_le_tee_boleng.sin_addr.s_addr);
    kgonthiša(sendto(종단점, "truncate", 8, 0, (struct sockaddr *)&sedirišwa_sa_legoro_le_tee_boleng, sizeof sedirišwa_sa_legoro_le_tee_boleng) == 8);
    kgonthiša(recvfrom(종단점, data, 3, 0, NULL, NULL) == 3 && memcmp(data, "tru", 3) == 0);
    kgonthiša(recvfrom(종단점, data, sizeof data, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    kgonthiša(sendto(종단점, NULL, 0, 0, (struct sockaddr *)&sedirišwa_sa_legoro_le_tee_boleng, sizeof sedirišwa_sa_legoro_le_tee_boleng) == 0);
    kgonthiša(recvfrom(종단점, NULL, 0, 0, NULL, NULL) == 0);
    kgonthiša(recvfrom(종단점, data, sizeof data, 0, NULL, NULL) == -1 && errno == EAGAIN);
    kgonthiša(close(종단점) == 0);
    puts("POSIX UDP CHECK PASS");
    return 0;
}
