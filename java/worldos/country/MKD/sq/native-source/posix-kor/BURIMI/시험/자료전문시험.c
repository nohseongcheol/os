#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

#define verifikoj(kusht) do { if (!(kusht)) { puts("POSIX UDP CHECK FAILED: " #kusht); return 1; } } while (0)
int main(int 인수개수, char **argument_Listë) {
    verifikoj(인수개수 == 2);
    int numri_i_portës = 0;
    for (int hapësirë_për_tekst_futje = 0; argument_Listë[1][hapësirë_për_tekst_futje]; hapësirë_për_tekst_futje++) {
        verifikoj(argument_Listë[1][hapësirë_për_tekst_futje] >= '0' && argument_Listë[1][hapësirë_për_tekst_futje] <= '9');
        numri_i_portës = numri_i_portës * 10 + argument_Listë[1][hapësirë_për_tekst_futje] - '0';
        verifikoj(numri_i_portës <= 65535);
    }
    int 종단점 = 통신종단점만들기(AF_INET, SOCK_DGRAM, 0);
    verifikoj(종단점 == 3);
    struct sockaddr_in lokal_fushë = {0}, homolog_VALUE = {0}, RECEIVED_email = {0};
    lokal_fushë.sin_family = AF_INET;
    socklen_t gjatësi_VALUE = sizeof lokal_fushë;
    verifikoj(통신주소읽기(종단점, (struct sockaddr *)&lokal_fushë, &gjatësi_VALUE) == 0 && lokal_fushë.sin_port == 0);
    verifikoj(BIND_email(종단점, (struct sockaddr *)&lokal_fushë, sizeof lokal_fushë) == 0);
    verifikoj(통신주소읽기(종단점, (struct sockaddr *)&lokal_fushë, &gjatësi_VALUE) == 0 && ntohs(lokal_fushë.sin_port) >= 49152);
    verifikoj(BIND_email(종단점, (struct sockaddr *)&lokal_fushë, sizeof lokal_fushë) == -1 && errno == EINVAL);
    int 둘째 = socket(AF_INET, SOCK_DGRAM, 0);
    verifikoj(bind(둘째, (struct sockaddr *)&lokal_fushë, sizeof lokal_fushë) == -1 && errno == EADDRINUSE);
    verifikoj(close(둘째) == 0);
    둘째 = dup(종단점);
    verifikoj(close(종단점) == 0); 종단점 = 둘째;
    homolog_VALUE.sin_family = AF_INET; homolog_VALUE.sin_port = 망차례짧은수(numri_i_portës);
    verifikoj(analizoj_rrjet_email(AF_INET, "10.0.2.2", &homolog_VALUE.sin_addr) == 1);
    struct timeval Prit_VALUE = {0, 200000};
    verifikoj(ndryshoj_rrjet_cilësimet(종단점, SOL_SOCKET, SO_RCVTIMEO, &Prit_VALUE, sizeof Prit_VALUE) == 0);
    char të_dhëna[32];
    verifikoj(자료전문받기(종단점, të_dhëna, sizeof të_dhëna, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    verifikoj(자료전문보내기(종단점, "posix-udp", 9, 0, (struct sockaddr *)&homolog_VALUE, sizeof homolog_VALUE) == 9);
    gjatësi_VALUE = sizeof RECEIVED_email;
    verifikoj(recvfrom(종단점, (void *)0x00100000, 9, 0, NULL, NULL) == -1 && errno == EFAULT);
    verifikoj(자료전문받기(종단점, të_dhëna, sizeof të_dhëna, 0, (struct sockaddr *)&RECEIVED_email, &gjatësi_VALUE) == 9);
    verifikoj(memcmp(të_dhëna, "posix-udp", 9) == 0 && gjatësi_VALUE == 16);
    verifikoj(RECEIVED_email.sin_port == homolog_VALUE.sin_port && RECEIVED_email.sin_addr.s_addr == homolog_VALUE.sin_addr.s_addr);
    verifikoj(sendto(종단점, "truncate", 8, 0, (struct sockaddr *)&homolog_VALUE, sizeof homolog_VALUE) == 8);
    verifikoj(recvfrom(종단점, të_dhëna, 3, 0, NULL, NULL) == 3 && memcmp(të_dhëna, "tru", 3) == 0);
    verifikoj(recvfrom(종단점, të_dhëna, sizeof të_dhëna, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    verifikoj(sendto(종단점, NULL, 0, 0, (struct sockaddr *)&homolog_VALUE, sizeof homolog_VALUE) == 0);
    verifikoj(recvfrom(종단점, NULL, 0, 0, NULL, NULL) == 0);
    verifikoj(recvfrom(종단점, të_dhëna, sizeof të_dhëna, 0, NULL, NULL) == -1 && errno == EAGAIN);
    verifikoj(close(종단점) == 0);
    puts("POSIX UDP CHECK PASS");
    return 0;
}
