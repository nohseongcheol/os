#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

#define igazol(állapot) do { if (!(állapot)) { puts("POSIX UDP CHECK FAILED: " #állapot); return 1; } } while (0)
int main(int 인수개수, char **argumentum_Lista) {
    igazol(인수개수 == 2);
    int portszám = 0;
    for (int tárolóhely_bejegyzés = 0; argumentum_Lista[1][tárolóhely_bejegyzés]; tárolóhely_bejegyzés++) {
        igazol(argumentum_Lista[1][tárolóhely_bejegyzés] >= '0' && argumentum_Lista[1][tárolóhely_bejegyzés] <= '9');
        portszám = portszám * 10 + argumentum_Lista[1][tárolóhely_bejegyzés] - '0';
        igazol(portszám <= 65535);
    }
    int végpont_ÉRTÉK = készít_végpont(AF_INET, SOCK_DGRAM, 0);
    igazol(végpont_ÉRTÉK == 3);
    struct sockaddr_in helyi_hatókör = {0}, társ_ÉRTÉK = {0}, KAPOTT_CÍM = {0};
    helyi_hatókör.sin_family = AF_INET;
    socklen_t hossz_ÉRTÉK = sizeof helyi_hatókör;
    igazol(통신주소읽기(végpont_ÉRTÉK, (struct sockaddr *)&helyi_hatókör, &hossz_ÉRTÉK) == 0 && helyi_hatókör.sin_port == 0);
    igazol(BIND_CÍM(végpont_ÉRTÉK, (struct sockaddr *)&helyi_hatókör, sizeof helyi_hatókör) == 0);
    igazol(통신주소읽기(végpont_ÉRTÉK, (struct sockaddr *)&helyi_hatókör, &hossz_ÉRTÉK) == 0 && ntohs(helyi_hatókör.sin_port) >= 49152);
    igazol(BIND_CÍM(végpont_ÉRTÉK, (struct sockaddr *)&helyi_hatókör, sizeof helyi_hatókör) == -1 && errno == EINVAL);
    int 둘째 = socket(AF_INET, SOCK_DGRAM, 0);
    igazol(bind(둘째, (struct sockaddr *)&helyi_hatókör, sizeof helyi_hatókör) == -1 && errno == EADDRINUSE);
    igazol(close(둘째) == 0);
    둘째 = dup(végpont_ÉRTÉK);
    igazol(close(végpont_ÉRTÉK) == 0); végpont_ÉRTÉK = 둘째;
    társ_ÉRTÉK.sin_family = AF_INET; társ_ÉRTÉK.sin_port = 망차례짧은수(portszám);
    igazol(elemez_hálózati_azonosító(AF_INET, "10.0.2.2", &társ_ÉRTÉK.sin_addr) == 1);
    struct timeval várj_ÉRTÉK = {0, 200000};
    igazol(módosítás_hálózat_Gépház(végpont_ÉRTÉK, SOL_SOCKET, SO_RCVTIMEO, &várj_ÉRTÉK, sizeof várj_ÉRTÉK) == 0);
    char adat[32];
    igazol(fogad_datagram_adat(végpont_ÉRTÉK, adat, sizeof adat, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    igazol(küld_datagram_adat(végpont_ÉRTÉK, "posix-udp", 9, 0, (struct sockaddr *)&társ_ÉRTÉK, sizeof társ_ÉRTÉK) == 9);
    hossz_ÉRTÉK = sizeof KAPOTT_CÍM;
    igazol(recvfrom(végpont_ÉRTÉK, (void *)0x00100000, 9, 0, NULL, NULL) == -1 && errno == EFAULT);
    igazol(fogad_datagram_adat(végpont_ÉRTÉK, adat, sizeof adat, 0, (struct sockaddr *)&KAPOTT_CÍM, &hossz_ÉRTÉK) == 9);
    igazol(memcmp(adat, "posix-udp", 9) == 0 && hossz_ÉRTÉK == 16);
    igazol(KAPOTT_CÍM.sin_port == társ_ÉRTÉK.sin_port && KAPOTT_CÍM.sin_addr.s_addr == társ_ÉRTÉK.sin_addr.s_addr);
    igazol(sendto(végpont_ÉRTÉK, "truncate", 8, 0, (struct sockaddr *)&társ_ÉRTÉK, sizeof társ_ÉRTÉK) == 8);
    igazol(recvfrom(végpont_ÉRTÉK, adat, 3, 0, NULL, NULL) == 3 && memcmp(adat, "tru", 3) == 0);
    igazol(recvfrom(végpont_ÉRTÉK, adat, sizeof adat, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    igazol(sendto(végpont_ÉRTÉK, NULL, 0, 0, (struct sockaddr *)&társ_ÉRTÉK, sizeof társ_ÉRTÉK) == 0);
    igazol(recvfrom(végpont_ÉRTÉK, NULL, 0, 0, NULL, NULL) == 0);
    igazol(recvfrom(végpont_ÉRTÉK, adat, sizeof adat, 0, NULL, NULL) == -1 && errno == EAGAIN);
    igazol(close(végpont_ÉRTÉK) == 0);
    puts("POSIX UDP CHECK PASS");
    return 0;
}
