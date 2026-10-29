#include <Plik_ABI.h>
#include <sieć_ABI.h>
#include <string.h>
#include <stdio.h>

#define 확인(choroba) do { if (!(choroba)) { puts("POSIX UDP CHECK FAILED: " #choroba); return 1; } } while (0)
int main(int 인수개수, char **argument_Lista) {
    확인(인수개수 == 2);
    int numer_portu = 0;
    for (int gniazdo_wpis = 0; argument_Lista[1][gniazdo_wpis]; gniazdo_wpis++) {
        확인(argument_Lista[1][gniazdo_wpis] >= '0' && argument_Lista[1][gniazdo_wpis] <= '9');
        numer_portu = numer_portu * 10 + argument_Lista[1][gniazdo_wpis] - '0';
        확인(numer_portu <= 65535);
    }
    int uczestnik_WARTOŚĆ = Twórca_uczestnik(AF_INET, SOCK_DGRAM, 0);
    확인(uczestnik_WARTOŚĆ == 3);
    struct sockaddr_in lokalny_Scope = {0}, węzeł_równorzędny_WARTOŚĆ = {0}, KWOTA_WYKUP_ADRES = {0};
    lokalny_Scope.sin_family = AF_INET;
    socklen_t długość_WARTOŚĆ = sizeof lokalny_Scope;
    확인(통신주소읽기(uczestnik_WARTOŚĆ, (struct sockaddr *)&lokalny_Scope, &długość_WARTOŚĆ) == 0 && lokalny_Scope.sin_port == 0);
    확인(BIND_ADRES(uczestnik_WARTOŚĆ, (struct sockaddr *)&lokalny_Scope, sizeof lokalny_Scope) == 0);
    확인(통신주소읽기(uczestnik_WARTOŚĆ, (struct sockaddr *)&lokalny_Scope, &długość_WARTOŚĆ) == 0 && ntohs(lokalny_Scope.sin_port) >= 49152);
    확인(BIND_ADRES(uczestnik_WARTOŚĆ, (struct sockaddr *)&lokalny_Scope, sizeof lokalny_Scope) == -1 && errno == EINVAL);
    int 둘째 = socket(AF_INET, SOCK_DGRAM, 0);
    확인(bind(둘째, (struct sockaddr *)&lokalny_Scope, sizeof lokalny_Scope) == -1 && errno == EADDRINUSE);
    확인(close(둘째) == 0);
    둘째 = dup(uczestnik_WARTOŚĆ);
    확인(close(uczestnik_WARTOŚĆ) == 0); uczestnik_WARTOŚĆ = 둘째;
    węzeł_równorzędny_WARTOŚĆ.sin_family = AF_INET; węzeł_równorzędny_WARTOŚĆ.sin_port = 망차례짧은수(numer_portu);
    확인(analizować_identyfikator_sieciowy(AF_INET, "10.0.2.2", &węzeł_równorzędny_WARTOŚĆ.sin_addr) == 1);
    struct timeval chwileczkę_WARTOŚĆ = {0, 200000};
    확인(zmienić_sieć_Ustawienia(uczestnik_WARTOŚĆ, SOL_SOCKET, SO_RCVTIMEO, &chwileczkę_WARTOŚĆ, sizeof chwileczkę_WARTOŚĆ) == 0);
    char dane[32];
    확인(odbierać_datagram_dane(uczestnik_WARTOŚĆ, dane, sizeof dane, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    확인(wysłać_datagram_dane(uczestnik_WARTOŚĆ, "posix-udp", 9, 0, (struct sockaddr *)&węzeł_równorzędny_WARTOŚĆ, sizeof węzeł_równorzędny_WARTOŚĆ) == 9);
    długość_WARTOŚĆ = sizeof KWOTA_WYKUP_ADRES;
    확인(recvfrom(uczestnik_WARTOŚĆ, (void *)0x00100000, 9, 0, NULL, NULL) == -1 && errno == EFAULT);
    확인(odbierać_datagram_dane(uczestnik_WARTOŚĆ, dane, sizeof dane, 0, (struct sockaddr *)&KWOTA_WYKUP_ADRES, &długość_WARTOŚĆ) == 9);
    확인(memcmp(dane, "posix-udp", 9) == 0 && długość_WARTOŚĆ == 16);
    확인(KWOTA_WYKUP_ADRES.sin_port == węzeł_równorzędny_WARTOŚĆ.sin_port && KWOTA_WYKUP_ADRES.sin_addr.s_addr == węzeł_równorzędny_WARTOŚĆ.sin_addr.s_addr);
    확인(sendto(uczestnik_WARTOŚĆ, "truncate", 8, 0, (struct sockaddr *)&węzeł_równorzędny_WARTOŚĆ, sizeof węzeł_równorzędny_WARTOŚĆ) == 8);
    확인(recvfrom(uczestnik_WARTOŚĆ, dane, 3, 0, NULL, NULL) == 3 && memcmp(dane, "tru", 3) == 0);
    확인(recvfrom(uczestnik_WARTOŚĆ, dane, sizeof dane, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    확인(sendto(uczestnik_WARTOŚĆ, NULL, 0, 0, (struct sockaddr *)&węzeł_równorzędny_WARTOŚĆ, sizeof węzeł_równorzędny_WARTOŚĆ) == 0);
    확인(recvfrom(uczestnik_WARTOŚĆ, NULL, 0, 0, NULL, NULL) == 0);
    확인(recvfrom(uczestnik_WARTOŚĆ, dane, sizeof dane, 0, NULL, NULL) == -1 && errno == EAGAIN);
    확인(close(uczestnik_WARTOŚĆ) == 0);
    puts("POSIX UDP CHECK PASS");
    return 0;
}
