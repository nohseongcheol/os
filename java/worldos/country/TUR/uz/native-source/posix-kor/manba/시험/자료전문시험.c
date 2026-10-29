#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

#define tasdiqlamoq(holat) do { if (!(holat)) { puts("POSIX UDP CHECK FAILED: " #holat); return 1; } } while (0)
int main(int 인수개수, char **dalil_Ro_yxat) {
    tasdiqlamoq(인수개수 == 2);
    int 접속번호 = 0;
    for (int in_kiritish = 0; dalil_Ro_yxat[1][in_kiritish]; in_kiritish++) {
        tasdiqlamoq(dalil_Ro_yxat[1][in_kiritish] >= '0' && dalil_Ro_yxat[1][in_kiritish] <= '9');
        접속번호 = 접속번호 * 10 + dalil_Ro_yxat[1][in_kiritish] - '0';
        tasdiqlamoq(접속번호 <= 65535);
    }
    int 종단점 = 통신종단점만들기(AF_INET, SOCK_DGRAM, 0);
    tasdiqlamoq(종단점 == 3);
    struct sockaddr_in mahalliy_soha = {0}, bir_rangli_VALUE = {0}, RECEIVED_manzil = {0};
    mahalliy_soha.sin_family = AF_INET;
    socklen_t uzunlik_VALUE = sizeof mahalliy_soha;
    tasdiqlamoq(통신주소읽기(종단점, (struct sockaddr *)&mahalliy_soha, &uzunlik_VALUE) == 0 && mahalliy_soha.sin_port == 0);
    tasdiqlamoq(BOG_LAMOQ_manzil(종단점, (struct sockaddr *)&mahalliy_soha, sizeof mahalliy_soha) == 0);
    tasdiqlamoq(통신주소읽기(종단점, (struct sockaddr *)&mahalliy_soha, &uzunlik_VALUE) == 0 && ntohs(mahalliy_soha.sin_port) >= 49152);
    tasdiqlamoq(BOG_LAMOQ_manzil(종단점, (struct sockaddr *)&mahalliy_soha, sizeof mahalliy_soha) == -1 && errno == EINVAL);
    int 둘째 = socket(AF_INET, SOCK_DGRAM, 0);
    tasdiqlamoq(bind(둘째, (struct sockaddr *)&mahalliy_soha, sizeof mahalliy_soha) == -1 && errno == EADDRINUSE);
    tasdiqlamoq(close(둘째) == 0);
    둘째 = dup(종단점);
    tasdiqlamoq(close(종단점) == 0); 종단점 = 둘째;
    bir_rangli_VALUE.sin_family = AF_INET; bir_rangli_VALUE.sin_port = 망차례짧은수(접속번호);
    tasdiqlamoq(tahlil_qilmoq_Tarmoq_manzil(AF_INET, "10.0.2.2", &bir_rangli_VALUE.sin_addr) == 1);
    struct timeval bir_daqiqa_VALUE = {0, 200000};
    tasdiqlamoq(o_zgartirmoq_Tarmoq_Sozlamalar(종단점, SOL_SOCKET, SO_RCVTIMEO, &bir_daqiqa_VALUE, sizeof bir_daqiqa_VALUE) == 0);
    char ma_lumotlar[32];
    tasdiqlamoq(자료전문받기(종단점, ma_lumotlar, sizeof ma_lumotlar, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    tasdiqlamoq(자료전문보내기(종단점, "posix-udp", 9, 0, (struct sockaddr *)&bir_rangli_VALUE, sizeof bir_rangli_VALUE) == 9);
    uzunlik_VALUE = sizeof RECEIVED_manzil;
    tasdiqlamoq(recvfrom(종단점, (void *)0x00100000, 9, 0, NULL, NULL) == -1 && errno == EFAULT);
    tasdiqlamoq(자료전문받기(종단점, ma_lumotlar, sizeof ma_lumotlar, 0, (struct sockaddr *)&RECEIVED_manzil, &uzunlik_VALUE) == 9);
    tasdiqlamoq(memcmp(ma_lumotlar, "posix-udp", 9) == 0 && uzunlik_VALUE == 16);
    tasdiqlamoq(RECEIVED_manzil.sin_port == bir_rangli_VALUE.sin_port && RECEIVED_manzil.sin_addr.s_addr == bir_rangli_VALUE.sin_addr.s_addr);
    tasdiqlamoq(sendto(종단점, "truncate", 8, 0, (struct sockaddr *)&bir_rangli_VALUE, sizeof bir_rangli_VALUE) == 8);
    tasdiqlamoq(recvfrom(종단점, ma_lumotlar, 3, 0, NULL, NULL) == 3 && memcmp(ma_lumotlar, "tru", 3) == 0);
    tasdiqlamoq(recvfrom(종단점, ma_lumotlar, sizeof ma_lumotlar, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    tasdiqlamoq(sendto(종단점, NULL, 0, 0, (struct sockaddr *)&bir_rangli_VALUE, sizeof bir_rangli_VALUE) == 0);
    tasdiqlamoq(recvfrom(종단점, NULL, 0, 0, NULL, NULL) == 0);
    tasdiqlamoq(recvfrom(종단점, ma_lumotlar, sizeof ma_lumotlar, 0, NULL, NULL) == -1 && errno == EAGAIN);
    tasdiqlamoq(close(종단점) == 0);
    puts("POSIX UDP CHECK PASS");
    return 0;
}
