#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

#define nkwàdo_eziokwū(ọnọdụ) do { if (!(ọnọdụ)) { puts("POSIX UDP CHECK FAILED: " #ọnọdụ); return 1; } } while (0)
int main(int 인수개수, char **agụment_ndepụta) {
    nkwàdo_eziokwū(인수개수 == 2);
    int 접속번호 = 0;
    for (int oghere_ndebà = 0; agụment_ndepụta[1][oghere_ndebà]; oghere_ndebà++) {
        nkwàdo_eziokwū(agụment_ndepụta[1][oghere_ndebà] >= '0' && agụment_ndepụta[1][oghere_ndebà] <= '9');
        접속번호 = 접속번호 * 10 + agụment_ndepụta[1][oghere_ndebà] - '0';
        nkwàdo_eziokwū(접속번호 <= 65535);
    }
    int 종단점 = 통신종단점만들기(AF_INET, SOCK_DGRAM, 0);
    nkwàdo_eziokwū(종단점 == 3);
    struct sockaddr_in otù_ebe_ọgba = {0}, ibè_valuu = {0}, 받은주소 = {0};
    otù_ebe_ọgba.sin_family = AF_INET;
    socklen_t ogologo_valuu = sizeof otù_ebe_ọgba;
    nkwàdo_eziokwū(통신주소읽기(종단점, (struct sockaddr *)&otù_ebe_ọgba, &ogologo_valuu) == 0 && otù_ebe_ọgba.sin_port == 0);
    nkwàdo_eziokwū(JIKỌNYE_àdreèsì(종단점, (struct sockaddr *)&otù_ebe_ọgba, sizeof otù_ebe_ọgba) == 0);
    nkwàdo_eziokwū(통신주소읽기(종단점, (struct sockaddr *)&otù_ebe_ọgba, &ogologo_valuu) == 0 && ntohs(otù_ebe_ọgba.sin_port) >= 49152);
    nkwàdo_eziokwū(JIKỌNYE_àdreèsì(종단점, (struct sockaddr *)&otù_ebe_ọgba, sizeof otù_ebe_ọgba) == -1 && errno == EINVAL);
    int 둘째 = socket(AF_INET, SOCK_DGRAM, 0);
    nkwàdo_eziokwū(bind(둘째, (struct sockaddr *)&otù_ebe_ọgba, sizeof otù_ebe_ọgba) == -1 && errno == EADDRINUSE);
    nkwàdo_eziokwū(close(둘째) == 0);
    둘째 = dup(종단점);
    nkwàdo_eziokwū(close(종단점) == 0); 종단점 = 둘째;
    ibè_valuu.sin_family = AF_INET; ibè_valuu.sin_port = 망차례짧은수(접속번호);
    nkwàdo_eziokwū(kerìsịa_Netwọọkụ_àdreèsì(AF_INET, "10.0.2.2", &ibè_valuu.sin_addr) == 1);
    struct timeval 대기 = {0, 200000};
    nkwàdo_eziokwū(gbanwèe_Netwọọkụ_Mwube(종단점, SOL_SOCKET, SO_RCVTIMEO, &대기, sizeof 대기) == 0);
    char datà[32];
    nkwàdo_eziokwū(자료전문받기(종단점, datà, sizeof datà, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    nkwàdo_eziokwū(자료전문보내기(종단점, "posix-udp", 9, 0, (struct sockaddr *)&ibè_valuu, sizeof ibè_valuu) == 9);
    ogologo_valuu = sizeof 받은주소;
    nkwàdo_eziokwū(recvfrom(종단점, (void *)0x00100000, 9, 0, NULL, NULL) == -1 && errno == EFAULT);
    nkwàdo_eziokwū(자료전문받기(종단점, datà, sizeof datà, 0, (struct sockaddr *)&받은주소, &ogologo_valuu) == 9);
    nkwàdo_eziokwū(memcmp(datà, "posix-udp", 9) == 0 && ogologo_valuu == 16);
    nkwàdo_eziokwū(받은주소.sin_port == ibè_valuu.sin_port && 받은주소.sin_addr.s_addr == ibè_valuu.sin_addr.s_addr);
    nkwàdo_eziokwū(sendto(종단점, "truncate", 8, 0, (struct sockaddr *)&ibè_valuu, sizeof ibè_valuu) == 8);
    nkwàdo_eziokwū(recvfrom(종단점, datà, 3, 0, NULL, NULL) == 3 && memcmp(datà, "tru", 3) == 0);
    nkwàdo_eziokwū(recvfrom(종단점, datà, sizeof datà, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    nkwàdo_eziokwū(sendto(종단점, NULL, 0, 0, (struct sockaddr *)&ibè_valuu, sizeof ibè_valuu) == 0);
    nkwàdo_eziokwū(recvfrom(종단점, NULL, 0, 0, NULL, NULL) == 0);
    nkwàdo_eziokwū(recvfrom(종단점, datà, sizeof datà, 0, NULL, NULL) == -1 && errno == EAGAIN);
    nkwàdo_eziokwū(close(종단점) == 0);
    puts("POSIX UDP CHECK PASS");
    return 0;
}
