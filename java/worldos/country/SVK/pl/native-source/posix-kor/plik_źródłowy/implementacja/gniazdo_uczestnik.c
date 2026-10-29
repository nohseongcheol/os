#include <sieć_ABI.h>
#include <errno.h>
#include "Połącz_granica.h"

int socket(int 주소체계, int sieć_Rodzaj, int sprawa_identyfikator) {
    return 호출결과(jkoros_syscall(41, 주소체계, sieć_Rodzaj, sprawa_identyfikator, 0, 0));
}
int bind(int Plik_deskryptor, const struct sockaddr *Adres, socklen_t ADRES_długość) {
    return 호출결과(jkoros_syscall(42, Plik_deskryptor, (int)Adres, ADRES_długość, 0, 0));
}
ssize_t sendto(int Plik_deskryptor, const void *dane, size_t bajt_ILE_LICZB, int Ustawienia,
               const struct sockaddr *Adres, socklen_t ADRES_długość) {
    int żądanie[2] = {(int)Adres, ADRES_długość};
    return 호출결과(jkoros_syscall(43, Plik_deskryptor, (int)dane, bajt_ILE_LICZB, Ustawienia, (int)żądanie));
}
ssize_t recvfrom(int Plik_deskryptor, void *dane, size_t bajt_ILE_LICZB, int Ustawienia,
                 struct sockaddr *Adres, socklen_t *ADRES_długość) {
    int żądanie[2] = {(int)Adres, (int)ADRES_długość};
    return 호출결과(jkoros_syscall(44, Plik_deskryptor, (int)dane, bajt_ILE_LICZB, Ustawienia, (int)żądanie));
}
int getsockname(int Plik_deskryptor, struct sockaddr *Adres, socklen_t *ADRES_długość) {
    return 호출결과(jkoros_syscall(45, Plik_deskryptor, (int)Adres, (int)ADRES_długość, 0, 0));
}
int setsockopt(int Plik_deskryptor, int warstwa_WARTOŚĆ, int Ustawienia_nazwa, const void *WARTOŚĆ, socklen_t WARTOŚĆ_długość) {
    if (warstwa_WARTOŚĆ != SOL_SOCKET || Ustawienia_nazwa != SO_RCVTIMEO) { errno = ENOPROTOOPT; return -1; }
    if (!WARTOŚĆ) { errno = EFAULT; return -1; }
    if (WARTOŚĆ_długość != sizeof(struct timeval)) { errno = EINVAL; return -1; }
    const struct timeval *wartość_czasu = WARTOŚĆ;
    if (wartość_czasu->tv_sec < 0 || wartość_czasu->tv_sec > 2 || wartość_czasu->tv_usec < 0 || wartość_czasu->tv_usec >= 1000000) {
        errno = EINVAL; return -1;
    }
    int 밀리초 = wartość_czasu->tv_sec * 1000 + (wartość_czasu->tv_usec + 999) / 1000;
    return 호출결과(jkoros_syscall(46, Plik_deskryptor, 밀리초, 0, 0, 0));
}
uint16_t htons(uint16_t WARTOŚĆ) { return (WARTOŚĆ << 8) | (WARTOŚĆ >> 8); }
uint16_t ntohs(uint16_t WARTOŚĆ) { return htons(WARTOŚĆ); }
uint32_t htonl(uint32_t WARTOŚĆ) {
    return (WARTOŚĆ << 24) | ((WARTOŚĆ << 8) & 0xff0000U) | ((WARTOŚĆ >> 8) & 0xff00U) | (WARTOŚĆ >> 24);
}
uint32_t ntohl(uint32_t WARTOŚĆ) { return htonl(WARTOŚĆ); }
int inet_pton(int 주소체계, const char *ciąg_WARTOŚĆ, void *Adres) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return -1; }
    if (!ciąg_WARTOŚĆ || !Adres) { errno = EFAULT; return -1; }
    unsigned char 임시[4];
    for (int gniazdo_wpis = 0; gniazdo_wpis < 4; gniazdo_wpis++) {
        int WARTOŚĆ = 0, 자릿수 = 0;
        const char *Uruchom_2 = ciąg_WARTOŚĆ;
        while (*ciąg_WARTOŚĆ >= '0' && *ciąg_WARTOŚĆ <= '9') {
            if (++자릿수 > 3) return 0;
            WARTOŚĆ = WARTOŚĆ * 10 + *ciąg_WARTOŚĆ++ - '0';
        }
        if (!자릿수 || WARTOŚĆ > 255 || (자릿수 > 1 && *Uruchom_2 == '0')) return 0;
        임시[gniazdo_wpis] = WARTOŚĆ;
        if (gniazdo_wpis < 3) { if (*ciąg_WARTOŚĆ++ != '.') return 0; }
        else if (*ciąg_WARTOŚĆ) return 0;
    }
    for (int gniazdo_wpis = 0; gniazdo_wpis < 4; gniazdo_wpis++) ((unsigned char *)Adres)[gniazdo_wpis] = 임시[gniazdo_wpis];
    return 1;
}
const char *inet_ntop(int 주소체계, const void *Adres, char *ciąg_WARTOŚĆ, socklen_t pojemność_WARTOŚĆ) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return 0; }
    if (!Adres || !ciąg_WARTOŚĆ) { errno = EFAULT; return 0; }
    const unsigned char *identyfikator = Adres;
    char 임시[16]; unsigned int długość_WARTOŚĆ = 0;
    for (int gniazdo_wpis = 0; gniazdo_wpis < 4; gniazdo_wpis++) {
        unsigned int WARTOŚĆ = identyfikator[gniazdo_wpis];
        if (WARTOŚĆ >= 100) 임시[długość_WARTOŚĆ++] = '0' + WARTOŚĆ / 100;
        if (WARTOŚĆ >= 10) 임시[długość_WARTOŚĆ++] = '0' + WARTOŚĆ / 10 % 10;
        임시[długość_WARTOŚĆ++] = '0' + WARTOŚĆ % 10;
        if (gniazdo_wpis < 3) 임시[długość_WARTOŚĆ++] = '.';
    }
    임시[długość_WARTOŚĆ++] = 0;
    if (pojemność_WARTOŚĆ < długość_WARTOŚĆ) { errno = ENOSPC; return 0; }
    for (unsigned int gniazdo_wpis = 0; gniazdo_wpis < długość_WARTOŚĆ; gniazdo_wpis++) ciąg_WARTOŚĆ[gniazdo_wpis] = 임시[gniazdo_wpis];
    return ciąg_WARTOŚĆ;
}
