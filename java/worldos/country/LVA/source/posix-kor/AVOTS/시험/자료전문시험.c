#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

#define verificēt(nosacījums) do { if (!(nosacījums)) { puts("POSIX UDP CHECK FAILED: " #nosacījums); return 1; } } while (0)
int main(int 인수개수, char **arg_Saraksts) {
    verificēt(인수개수 == 2);
    int porta_numurs = 0;
    for (int 칸 = 0; arg_Saraksts[1][칸]; 칸++) {
        verificēt(arg_Saraksts[1][칸] >= '0' && arg_Saraksts[1][칸] <= '9');
        porta_numurs = porta_numurs * 10 + arg_Saraksts[1][칸] - '0';
        verificēt(porta_numurs <= 65535);
    }
    int dalībnieks_VALUE = atvērt_dalībnieks(AF_INET, SOCK_DGRAM, 0);
    verificēt(dalībnieks_VALUE == 3);
    struct sockaddr_in vietējs_Tvērums = {0}, vienranga_VALUE = {0}, RECEIVED_adrese = {0};
    vietējs_Tvērums.sin_family = AF_INET;
    socklen_t 길이 = sizeof vietējs_Tvērums;
    verificēt(통신주소읽기(dalībnieks_VALUE, (struct sockaddr *)&vietējs_Tvērums, &길이) == 0 && vietējs_Tvērums.sin_port == 0);
    verificēt(BIND_adrese(dalībnieks_VALUE, (struct sockaddr *)&vietējs_Tvērums, sizeof vietējs_Tvērums) == 0);
    verificēt(통신주소읽기(dalībnieks_VALUE, (struct sockaddr *)&vietējs_Tvērums, &길이) == 0 && ntohs(vietējs_Tvērums.sin_port) >= 49152);
    verificēt(BIND_adrese(dalībnieks_VALUE, (struct sockaddr *)&vietējs_Tvērums, sizeof vietējs_Tvērums) == -1 && errno == EINVAL);
    int 둘째 = socket(AF_INET, SOCK_DGRAM, 0);
    verificēt(bind(둘째, (struct sockaddr *)&vietējs_Tvērums, sizeof vietējs_Tvērums) == -1 && errno == EADDRINUSE);
    verificēt(close(둘째) == 0);
    둘째 = dup(dalībnieks_VALUE);
    verificēt(close(dalībnieks_VALUE) == 0); dalībnieks_VALUE = 둘째;
    vienranga_VALUE.sin_family = AF_INET; vienranga_VALUE.sin_port = 망차례짧은수(porta_numurs);
    verificēt(parsēt_tīkla_ID(AF_INET, "10.0.2.2", &vienranga_VALUE.sin_addr) == 1);
    struct timeval pagaidi_VALUE = {0, 200000};
    verificēt(mainīt_tīkls_Iestatījumi(dalībnieks_VALUE, SOL_SOCKET, SO_RCVTIMEO, &pagaidi_VALUE, sizeof pagaidi_VALUE) == 0);
    char dati[32];
    verificēt(saņemt_datogramma_dati(dalībnieks_VALUE, dati, sizeof dati, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    verificēt(sūtīt_datogramma_dati(dalībnieks_VALUE, "posix-udp", 9, 0, (struct sockaddr *)&vienranga_VALUE, sizeof vienranga_VALUE) == 9);
    길이 = sizeof RECEIVED_adrese;
    verificēt(recvfrom(dalībnieks_VALUE, (void *)0x00100000, 9, 0, NULL, NULL) == -1 && errno == EFAULT);
    verificēt(saņemt_datogramma_dati(dalībnieks_VALUE, dati, sizeof dati, 0, (struct sockaddr *)&RECEIVED_adrese, &길이) == 9);
    verificēt(memcmp(dati, "posix-udp", 9) == 0 && 길이 == 16);
    verificēt(RECEIVED_adrese.sin_port == vienranga_VALUE.sin_port && RECEIVED_adrese.sin_addr.s_addr == vienranga_VALUE.sin_addr.s_addr);
    verificēt(sendto(dalībnieks_VALUE, "truncate", 8, 0, (struct sockaddr *)&vienranga_VALUE, sizeof vienranga_VALUE) == 8);
    verificēt(recvfrom(dalībnieks_VALUE, dati, 3, 0, NULL, NULL) == 3 && memcmp(dati, "tru", 3) == 0);
    verificēt(recvfrom(dalībnieks_VALUE, dati, sizeof dati, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    verificēt(sendto(dalībnieks_VALUE, NULL, 0, 0, (struct sockaddr *)&vienranga_VALUE, sizeof vienranga_VALUE) == 0);
    verificēt(recvfrom(dalībnieks_VALUE, NULL, 0, 0, NULL, NULL) == 0);
    verificēt(recvfrom(dalībnieks_VALUE, dati, sizeof dati, 0, NULL, NULL) == -1 && errno == EAGAIN);
    verificēt(close(dalībnieks_VALUE) == 0);
    puts("POSIX UDP CHECK PASS");
    return 0;
}
