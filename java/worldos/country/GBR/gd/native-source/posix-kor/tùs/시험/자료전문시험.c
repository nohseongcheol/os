#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

#define dearbh(cumha) do { if (!(cumha)) { puts("POSIX UDP CHECK FAILED: " #cumha); return 1; } } while (0)
int main(int 인수개수, char **argamaid_Liosta) {
    dearbh(인수개수 == 2);
    int 접속번호 = 0;
    for (int slot_cur_a_steach = 0; argamaid_Liosta[1][slot_cur_a_steach]; slot_cur_a_steach++) {
        dearbh(argamaid_Liosta[1][slot_cur_a_steach] >= '0' && argamaid_Liosta[1][slot_cur_a_steach] <= '9');
        접속번호 = 접속번호 * 10 + argamaid_Liosta[1][slot_cur_a_steach] - '0';
        dearbh(접속번호 <= 65535);
    }
    int 종단점 = 통신종단점만들기(AF_INET, SOCK_DGRAM, 0);
    dearbh(종단점 == 3);
    struct sockaddr_in ionadail_sgòp = {0}, seise_VALUE = {0}, RECEIVED_ADDRESS = {0};
    ionadail_sgòp.sin_family = AF_INET;
    socklen_t faid_VALUE = sizeof ionadail_sgòp;
    dearbh(통신주소읽기(종단점, (struct sockaddr *)&ionadail_sgòp, &faid_VALUE) == 0 && ionadail_sgòp.sin_port == 0);
    dearbh(BIND_ADDRESS(종단점, (struct sockaddr *)&ionadail_sgòp, sizeof ionadail_sgòp) == 0);
    dearbh(통신주소읽기(종단점, (struct sockaddr *)&ionadail_sgòp, &faid_VALUE) == 0 && ntohs(ionadail_sgòp.sin_port) >= 49152);
    dearbh(BIND_ADDRESS(종단점, (struct sockaddr *)&ionadail_sgòp, sizeof ionadail_sgòp) == -1 && errno == EINVAL);
    int 둘째 = socket(AF_INET, SOCK_DGRAM, 0);
    dearbh(bind(둘째, (struct sockaddr *)&ionadail_sgòp, sizeof ionadail_sgòp) == -1 && errno == EADDRINUSE);
    dearbh(close(둘째) == 0);
    둘째 = dup(종단점);
    dearbh(close(종단점) == 0); 종단점 = 둘째;
    seise_VALUE.sin_family = AF_INET; seise_VALUE.sin_port = 망차례짧은수(접속번호);
    dearbh(망주소해석하기(AF_INET, "10.0.2.2", &seise_VALUE.sin_addr) == 1);
    struct timeval fuirich_VALUE = {0, 200000};
    dearbh(atharraich_lìonra_roghainnean(종단점, SOL_SOCKET, SO_RCVTIMEO, &fuirich_VALUE, sizeof fuirich_VALUE) == 0);
    char dàta[32];
    dearbh(자료전문받기(종단점, dàta, sizeof dàta, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    dearbh(자료전문보내기(종단점, "posix-udp", 9, 0, (struct sockaddr *)&seise_VALUE, sizeof seise_VALUE) == 9);
    faid_VALUE = sizeof RECEIVED_ADDRESS;
    dearbh(recvfrom(종단점, (void *)0x00100000, 9, 0, NULL, NULL) == -1 && errno == EFAULT);
    dearbh(자료전문받기(종단점, dàta, sizeof dàta, 0, (struct sockaddr *)&RECEIVED_ADDRESS, &faid_VALUE) == 9);
    dearbh(memcmp(dàta, "posix-udp", 9) == 0 && faid_VALUE == 16);
    dearbh(RECEIVED_ADDRESS.sin_port == seise_VALUE.sin_port && RECEIVED_ADDRESS.sin_addr.s_addr == seise_VALUE.sin_addr.s_addr);
    dearbh(sendto(종단점, "truncate", 8, 0, (struct sockaddr *)&seise_VALUE, sizeof seise_VALUE) == 8);
    dearbh(recvfrom(종단점, dàta, 3, 0, NULL, NULL) == 3 && memcmp(dàta, "tru", 3) == 0);
    dearbh(recvfrom(종단점, dàta, sizeof dàta, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    dearbh(sendto(종단점, NULL, 0, 0, (struct sockaddr *)&seise_VALUE, sizeof seise_VALUE) == 0);
    dearbh(recvfrom(종단점, NULL, 0, 0, NULL, NULL) == 0);
    dearbh(recvfrom(종단점, dàta, sizeof dàta, 0, NULL, NULL) == -1 && errno == EAGAIN);
    dearbh(close(종단점) == 0);
    puts("POSIX UDP CHECK PASS");
    return 0;
}
