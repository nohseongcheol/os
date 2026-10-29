#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

#define netefatsa(boemo) do { if (!(boemo)) { puts("POSIX UDP CHECK FAILED: " #boemo); return 1; } } while (0)
int main(int 인수개수, char **Thulaganyo_lenaane) {
    netefatsa(인수개수 == 2);
    int 접속번호 = 0;
    for (int sebaka_tsenyo = 0; Thulaganyo_lenaane[1][sebaka_tsenyo]; sebaka_tsenyo++) {
        netefatsa(Thulaganyo_lenaane[1][sebaka_tsenyo] >= '0' && Thulaganyo_lenaane[1][sebaka_tsenyo] <= '9');
        접속번호 = 접속번호 * 10 + Thulaganyo_lenaane[1][sebaka_tsenyo] - '0';
        netefatsa(접속번호 <= 65535);
    }
    int 종단점 = 통신종단점만들기(AF_INET, SOCK_DGRAM, 0);
    netefatsa(종단점 == 3);
    struct sockaddr_in e_e_gaufi_Mothamo = {0}, semphato_Boleng = {0}, 받은주소 = {0};
    e_e_gaufi_Mothamo.sin_family = AF_INET;
    socklen_t boleele_Boleng = sizeof e_e_gaufi_Mothamo;
    netefatsa(통신주소읽기(종단점, (struct sockaddr *)&e_e_gaufi_Mothamo, &boleele_Boleng) == 0 && e_e_gaufi_Mothamo.sin_port == 0);
    netefatsa(BIND_aterese(종단점, (struct sockaddr *)&e_e_gaufi_Mothamo, sizeof e_e_gaufi_Mothamo) == 0);
    netefatsa(통신주소읽기(종단점, (struct sockaddr *)&e_e_gaufi_Mothamo, &boleele_Boleng) == 0 && ntohs(e_e_gaufi_Mothamo.sin_port) >= 49152);
    netefatsa(BIND_aterese(종단점, (struct sockaddr *)&e_e_gaufi_Mothamo, sizeof e_e_gaufi_Mothamo) == -1 && errno == EINVAL);
    int 둘째 = socket(AF_INET, SOCK_DGRAM, 0);
    netefatsa(bind(둘째, (struct sockaddr *)&e_e_gaufi_Mothamo, sizeof e_e_gaufi_Mothamo) == -1 && errno == EADDRINUSE);
    netefatsa(close(둘째) == 0);
    둘째 = dup(종단점);
    netefatsa(close(종단점) == 0); 종단점 = 둘째;
    semphato_Boleng.sin_family = AF_INET; semphato_Boleng.sin_port = 망차례짧은수(접속번호);
    netefatsa(go_lokolola_Neteweke_aterese(AF_INET, "10.0.2.2", &semphato_Boleng.sin_addr) == 1);
    struct timeval 대기 = {0, 200000};
    netefatsa(fetola_Neteweke_Diseting(종단점, SOL_SOCKET, SO_RCVTIMEO, &대기, sizeof 대기) == 0);
    char tshedimosetso[32];
    netefatsa(자료전문받기(종단점, tshedimosetso, sizeof tshedimosetso, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    netefatsa(자료전문보내기(종단점, "posix-udp", 9, 0, (struct sockaddr *)&semphato_Boleng, sizeof semphato_Boleng) == 9);
    boleele_Boleng = sizeof 받은주소;
    netefatsa(recvfrom(종단점, (void *)0x00100000, 9, 0, NULL, NULL) == -1 && errno == EFAULT);
    netefatsa(자료전문받기(종단점, tshedimosetso, sizeof tshedimosetso, 0, (struct sockaddr *)&받은주소, &boleele_Boleng) == 9);
    netefatsa(memcmp(tshedimosetso, "posix-udp", 9) == 0 && boleele_Boleng == 16);
    netefatsa(받은주소.sin_port == semphato_Boleng.sin_port && 받은주소.sin_addr.s_addr == semphato_Boleng.sin_addr.s_addr);
    netefatsa(sendto(종단점, "truncate", 8, 0, (struct sockaddr *)&semphato_Boleng, sizeof semphato_Boleng) == 8);
    netefatsa(recvfrom(종단점, tshedimosetso, 3, 0, NULL, NULL) == 3 && memcmp(tshedimosetso, "tru", 3) == 0);
    netefatsa(recvfrom(종단점, tshedimosetso, sizeof tshedimosetso, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    netefatsa(sendto(종단점, NULL, 0, 0, (struct sockaddr *)&semphato_Boleng, sizeof semphato_Boleng) == 0);
    netefatsa(recvfrom(종단점, NULL, 0, 0, NULL, NULL) == 0);
    netefatsa(recvfrom(종단점, tshedimosetso, sizeof tshedimosetso, 0, NULL, NULL) == -1 && errno == EAGAIN);
    netefatsa(close(종단점) == 0);
    puts("POSIX UDP CHECK PASS");
    return 0;
}
