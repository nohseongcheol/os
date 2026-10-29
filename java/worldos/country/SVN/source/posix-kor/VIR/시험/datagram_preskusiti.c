#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

#define 확인(pogoj) do { if (!(pogoj)) { puts("POSIX UDP CHECK FAILED: " #pogoj); return 1; } } while (0)
int main(int 인수개수, char **argument_Seznam) {
    확인(인수개수 == 2);
    int številka_vrat = 0;
    for (int 칸 = 0; argument_Seznam[1][칸]; 칸++) {
        확인(argument_Seznam[1][칸] >= '0' && argument_Seznam[1][칸] <= '9');
        številka_vrat = številka_vrat * 10 + argument_Seznam[1][칸] - '0';
        확인(številka_vrat <= 65535);
    }
    int končna_točka_VALUE = Ustvari_končna_točka(AF_INET, SOCK_DGRAM, 0);
    확인(končna_točka_VALUE == 3);
    struct sockaddr_in lokalen_krajeven_obseg = {0}, enakovreden_VALUE = {0}, RECEIVED_naslov = {0};
    lokalen_krajeven_obseg.sin_family = AF_INET;
    socklen_t 길이 = sizeof lokalen_krajeven_obseg;
    확인(통신주소읽기(končna_točka_VALUE, (struct sockaddr *)&lokalen_krajeven_obseg, &길이) == 0 && lokalen_krajeven_obseg.sin_port == 0);
    확인(BIND_naslov(končna_točka_VALUE, (struct sockaddr *)&lokalen_krajeven_obseg, sizeof lokalen_krajeven_obseg) == 0);
    확인(통신주소읽기(končna_točka_VALUE, (struct sockaddr *)&lokalen_krajeven_obseg, &길이) == 0 && ntohs(lokalen_krajeven_obseg.sin_port) >= 49152);
    확인(BIND_naslov(končna_točka_VALUE, (struct sockaddr *)&lokalen_krajeven_obseg, sizeof lokalen_krajeven_obseg) == -1 && errno == EINVAL);
    int 둘째 = socket(AF_INET, SOCK_DGRAM, 0);
    확인(bind(둘째, (struct sockaddr *)&lokalen_krajeven_obseg, sizeof lokalen_krajeven_obseg) == -1 && errno == EADDRINUSE);
    확인(close(둘째) == 0);
    둘째 = dup(končna_točka_VALUE);
    확인(close(končna_točka_VALUE) == 0); končna_točka_VALUE = 둘째;
    enakovreden_VALUE.sin_family = AF_INET; enakovreden_VALUE.sin_port = 망차례짧은수(številka_vrat);
    확인(razčlenjevati_omrežni_identifikator(AF_INET, "10.0.2.2", &enakovreden_VALUE.sin_addr) == 1);
    struct timeval počakaj_VALUE = {0, 200000};
    확인(spremeniti_mreža_Nastavitve(končna_točka_VALUE, SOL_SOCKET, SO_RCVTIMEO, &počakaj_VALUE, sizeof počakaj_VALUE) == 0);
    char podatki[32];
    확인(sprejeti_sprejemati_prejeti_prejemati_datagram_podatki(končna_točka_VALUE, podatki, sizeof podatki, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    확인(poslati_datagram_podatki(končna_točka_VALUE, "posix-udp", 9, 0, (struct sockaddr *)&enakovreden_VALUE, sizeof enakovreden_VALUE) == 9);
    길이 = sizeof RECEIVED_naslov;
    확인(recvfrom(končna_točka_VALUE, (void *)0x00100000, 9, 0, NULL, NULL) == -1 && errno == EFAULT);
    확인(sprejeti_sprejemati_prejeti_prejemati_datagram_podatki(končna_točka_VALUE, podatki, sizeof podatki, 0, (struct sockaddr *)&RECEIVED_naslov, &길이) == 9);
    확인(memcmp(podatki, "posix-udp", 9) == 0 && 길이 == 16);
    확인(RECEIVED_naslov.sin_port == enakovreden_VALUE.sin_port && RECEIVED_naslov.sin_addr.s_addr == enakovreden_VALUE.sin_addr.s_addr);
    확인(sendto(končna_točka_VALUE, "truncate", 8, 0, (struct sockaddr *)&enakovreden_VALUE, sizeof enakovreden_VALUE) == 8);
    확인(recvfrom(končna_točka_VALUE, podatki, 3, 0, NULL, NULL) == 3 && memcmp(podatki, "tru", 3) == 0);
    확인(recvfrom(končna_točka_VALUE, podatki, sizeof podatki, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    확인(sendto(končna_točka_VALUE, NULL, 0, 0, (struct sockaddr *)&enakovreden_VALUE, sizeof enakovreden_VALUE) == 0);
    확인(recvfrom(končna_točka_VALUE, NULL, 0, 0, NULL, NULL) == 0);
    확인(recvfrom(končna_točka_VALUE, podatki, sizeof podatki, 0, NULL, NULL) == -1 && errno == EAGAIN);
    확인(close(končna_točka_VALUE) == 0);
    puts("POSIX UDP CHECK PASS");
    return 0;
}
