#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

#define yoxlamaq(şərt) do { if (!(şərt)) { puts("POSIX UDP CHECK FAILED: " #şərt); return 1; } } while (0)
int main(int 인수개수, char **arqument_Siyahı) {
    yoxlamaq(인수개수 == 2);
    int 접속번호 = 0;
    for (int slot_daxiletmə = 0; arqument_Siyahı[1][slot_daxiletmə]; slot_daxiletmə++) {
        yoxlamaq(arqument_Siyahı[1][slot_daxiletmə] >= '0' && arqument_Siyahı[1][slot_daxiletmə] <= '9');
        접속번호 = 접속번호 * 10 + arqument_Siyahı[1][slot_daxiletmə] - '0';
        yoxlamaq(접속번호 <= 65535);
    }
    int 종단점 = 통신종단점만들기(AF_INET, SOCK_DGRAM, 0);
    yoxlamaq(종단점 == 3);
    struct sockaddr_in lokal_miqyas = {0}, eynisəviyyəli_VALUE = {0}, RECEIVED_ünvan = {0};
    lokal_miqyas.sin_family = AF_INET;
    socklen_t uzunluq_VALUE = sizeof lokal_miqyas;
    yoxlamaq(통신주소읽기(종단점, (struct sockaddr *)&lokal_miqyas, &uzunluq_VALUE) == 0 && lokal_miqyas.sin_port == 0);
    yoxlamaq(BIND_ünvan(종단점, (struct sockaddr *)&lokal_miqyas, sizeof lokal_miqyas) == 0);
    yoxlamaq(통신주소읽기(종단점, (struct sockaddr *)&lokal_miqyas, &uzunluq_VALUE) == 0 && ntohs(lokal_miqyas.sin_port) >= 49152);
    yoxlamaq(BIND_ünvan(종단점, (struct sockaddr *)&lokal_miqyas, sizeof lokal_miqyas) == -1 && errno == EINVAL);
    int 둘째 = socket(AF_INET, SOCK_DGRAM, 0);
    yoxlamaq(bind(둘째, (struct sockaddr *)&lokal_miqyas, sizeof lokal_miqyas) == -1 && errno == EADDRINUSE);
    yoxlamaq(close(둘째) == 0);
    둘째 = dup(종단점);
    yoxlamaq(close(종단점) == 0); 종단점 = 둘째;
    eynisəviyyəli_VALUE.sin_family = AF_INET; eynisəviyyəli_VALUE.sin_port = 망차례짧은수(접속번호);
    yoxlamaq(parselləmək_Şəbəkə_ünvan(AF_INET, "10.0.2.2", &eynisəviyyəli_VALUE.sin_addr) == 1);
    struct timeval gözlə_VALUE = {0, 200000};
    yoxlamaq(dəyişdirmək_Şəbəkə_Parametrlər(종단점, SOL_SOCKET, SO_RCVTIMEO, &gözlə_VALUE, sizeof gözlə_VALUE) == 0);
    char verilənlər[32];
    yoxlamaq(자료전문받기(종단점, verilənlər, sizeof verilənlər, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    yoxlamaq(자료전문보내기(종단점, "posix-udp", 9, 0, (struct sockaddr *)&eynisəviyyəli_VALUE, sizeof eynisəviyyəli_VALUE) == 9);
    uzunluq_VALUE = sizeof RECEIVED_ünvan;
    yoxlamaq(recvfrom(종단점, (void *)0x00100000, 9, 0, NULL, NULL) == -1 && errno == EFAULT);
    yoxlamaq(자료전문받기(종단점, verilənlər, sizeof verilənlər, 0, (struct sockaddr *)&RECEIVED_ünvan, &uzunluq_VALUE) == 9);
    yoxlamaq(memcmp(verilənlər, "posix-udp", 9) == 0 && uzunluq_VALUE == 16);
    yoxlamaq(RECEIVED_ünvan.sin_port == eynisəviyyəli_VALUE.sin_port && RECEIVED_ünvan.sin_addr.s_addr == eynisəviyyəli_VALUE.sin_addr.s_addr);
    yoxlamaq(sendto(종단점, "truncate", 8, 0, (struct sockaddr *)&eynisəviyyəli_VALUE, sizeof eynisəviyyəli_VALUE) == 8);
    yoxlamaq(recvfrom(종단점, verilənlər, 3, 0, NULL, NULL) == 3 && memcmp(verilənlər, "tru", 3) == 0);
    yoxlamaq(recvfrom(종단점, verilənlər, sizeof verilənlər, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    yoxlamaq(sendto(종단점, NULL, 0, 0, (struct sockaddr *)&eynisəviyyəli_VALUE, sizeof eynisəviyyəli_VALUE) == 0);
    yoxlamaq(recvfrom(종단점, NULL, 0, 0, NULL, NULL) == 0);
    yoxlamaq(recvfrom(종단점, verilənlər, sizeof verilənlər, 0, NULL, NULL) == -1 && errno == EAGAIN);
    yoxlamaq(close(종단점) == 0);
    puts("POSIX UDP CHECK PASS");
    return 0;
}
