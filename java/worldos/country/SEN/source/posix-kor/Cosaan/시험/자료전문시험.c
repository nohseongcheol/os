#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

#define luñutu(anam) do { if (!(anam)) { puts("POSIX UDP CHECK FAILED: " #anam); return 1; } } while (0)
int main(int 인수개수, char **Tegtal_lim) {
    luñutu(인수개수 == 2);
    int 접속번호 = 0;
    for (int xar_xar_dugal_xabaar = 0; Tegtal_lim[1][xar_xar_dugal_xabaar]; xar_xar_dugal_xabaar++) {
        luñutu(Tegtal_lim[1][xar_xar_dugal_xabaar] >= '0' && Tegtal_lim[1][xar_xar_dugal_xabaar] <= '9');
        접속번호 = 접속번호 * 10 + Tegtal_lim[1][xar_xar_dugal_xabaar] - '0';
        luñutu(접속번호 <= 65535);
    }
    int 종단점 = 통신종단점만들기(AF_INET, SOCK_DGRAM, 0);
    luñutu(종단점 == 3);
    struct sockaddr_in dënnd_nameef = {0}, Nàttangoo_xëyma = {0}, 받은주소 = {0};
    dënnd_nameef.sin_family = AF_INET;
    socklen_t diir_xëyma = sizeof dënnd_nameef;
    luñutu(통신주소읽기(종단점, (struct sockaddr *)&dënnd_nameef, &diir_xëyma) == 0 && dënnd_nameef.sin_port == 0);
    luñutu(BIND_dëkkuwaay(종단점, (struct sockaddr *)&dënnd_nameef, sizeof dënnd_nameef) == 0);
    luñutu(통신주소읽기(종단점, (struct sockaddr *)&dënnd_nameef, &diir_xëyma) == 0 && ntohs(dënnd_nameef.sin_port) >= 49152);
    luñutu(BIND_dëkkuwaay(종단점, (struct sockaddr *)&dënnd_nameef, sizeof dënnd_nameef) == -1 && errno == EINVAL);
    int 둘째 = socket(AF_INET, SOCK_DGRAM, 0);
    luñutu(bind(둘째, (struct sockaddr *)&dënnd_nameef, sizeof dënnd_nameef) == -1 && errno == EADDRINUSE);
    luñutu(close(둘째) == 0);
    둘째 = dup(종단점);
    luñutu(close(종단점) == 0); 종단점 = 둘째;
    Nàttangoo_xëyma.sin_family = AF_INET; Nàttangoo_xëyma.sin_port = 망차례짧은수(접속번호);
    luñutu(Segg_mbaal_dëkkuwaay(AF_INET, "10.0.2.2", &Nàttangoo_xëyma.sin_addr) == 1);
    struct timeval 대기 = {0, 200000};
    luñutu(soppi_mbaal_Jekkal_yi(종단점, SOL_SOCKET, SO_RCVTIMEO, &대기, sizeof 대기) == 0);
    char mbir[32];
    luñutu(자료전문받기(종단점, mbir, sizeof mbir, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    luñutu(자료전문보내기(종단점, "posix-udp", 9, 0, (struct sockaddr *)&Nàttangoo_xëyma, sizeof Nàttangoo_xëyma) == 9);
    diir_xëyma = sizeof 받은주소;
    luñutu(recvfrom(종단점, (void *)0x00100000, 9, 0, NULL, NULL) == -1 && errno == EFAULT);
    luñutu(자료전문받기(종단점, mbir, sizeof mbir, 0, (struct sockaddr *)&받은주소, &diir_xëyma) == 9);
    luñutu(memcmp(mbir, "posix-udp", 9) == 0 && diir_xëyma == 16);
    luñutu(받은주소.sin_port == Nàttangoo_xëyma.sin_port && 받은주소.sin_addr.s_addr == Nàttangoo_xëyma.sin_addr.s_addr);
    luñutu(sendto(종단점, "truncate", 8, 0, (struct sockaddr *)&Nàttangoo_xëyma, sizeof Nàttangoo_xëyma) == 8);
    luñutu(recvfrom(종단점, mbir, 3, 0, NULL, NULL) == 3 && memcmp(mbir, "tru", 3) == 0);
    luñutu(recvfrom(종단점, mbir, sizeof mbir, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    luñutu(sendto(종단점, NULL, 0, 0, (struct sockaddr *)&Nàttangoo_xëyma, sizeof Nàttangoo_xëyma) == 0);
    luñutu(recvfrom(종단점, NULL, 0, 0, NULL, NULL) == 0);
    luñutu(recvfrom(종단점, mbir, sizeof mbir, 0, NULL, NULL) == -1 && errno == EAGAIN);
    luñutu(close(종단점) == 0);
    puts("POSIX UDP CHECK PASS");
    return 0;
}
