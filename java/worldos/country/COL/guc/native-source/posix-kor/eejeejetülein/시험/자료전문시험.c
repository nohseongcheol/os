#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

#define 확인(mülein) do { if (!(mülein)) { puts("POSIX UDP CHECK FAILED: " #mülein); return 1; } } while (0)
int main(int 인수개수, char **인수목록) {
    확인(인수개수 == 2);
    int 접속번호 = 0;
    for (int 칸 = 0; 인수목록[1][칸]; 칸++) {
        확인(인수목록[1][칸] >= '0' && 인수목록[1][칸] <= '9');
        접속번호 = 접속번호 * 10 + 인수목록[1][칸] - '0';
        확인(접속번호 <= 65535);
    }
    int 종단점 = 통신종단점만들기(AF_INET, SOCK_DGRAM, 0);
    확인(종단점 == 3);
    struct sockaddr_in 지역 = {0}, wanaawasü_ajutuu = {0}, 받은주소 = {0};
    지역.sin_family = AF_INET;
    socklen_t akaliaa_ajutuu = sizeof 지역;
    확인(통신주소읽기(종단점, (struct sockaddr *)&지역, &akaliaa_ajutuu) == 0 && 지역.sin_port == 0);
    확인(alaasajaa_ejepüsee(종단점, (struct sockaddr *)&지역, sizeof 지역) == 0);
    확인(통신주소읽기(종단점, (struct sockaddr *)&지역, &akaliaa_ajutuu) == 0 && ntohs(지역.sin_port) >= 49152);
    확인(alaasajaa_ejepüsee(종단점, (struct sockaddr *)&지역, sizeof 지역) == -1 && errno == EINVAL);
    int 둘째 = socket(AF_INET, SOCK_DGRAM, 0);
    확인(bind(둘째, (struct sockaddr *)&지역, sizeof 지역) == -1 && errno == EADDRINUSE);
    확인(close(둘째) == 0);
    둘째 = dup(종단점);
    확인(close(종단점) == 0); 종단점 = 둘째;
    wanaawasü_ajutuu.sin_family = AF_INET; wanaawasü_ajutuu.sin_port = 망차례짧은수(접속번호);
    확인(akatajaa_kusu_ejepüsee(AF_INET, "10.0.2.2", &wanaawasü_ajutuu.sin_addr) == 1);
    struct timeval 대기 = {0, 200000};
    확인(통신설정바꾸기(종단점, SOL_SOCKET, SO_RCVTIMEO, &대기, sizeof 대기) == 0);
    char atijaaya[32];
    확인(자료전문받기(종단점, atijaaya, sizeof atijaaya, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    확인(자료전문보내기(종단점, "posix-udp", 9, 0, (struct sockaddr *)&wanaawasü_ajutuu, sizeof wanaawasü_ajutuu) == 9);
    akaliaa_ajutuu = sizeof 받은주소;
    확인(recvfrom(종단점, (void *)0x00100000, 9, 0, NULL, NULL) == -1 && errno == EFAULT);
    확인(자료전문받기(종단점, atijaaya, sizeof atijaaya, 0, (struct sockaddr *)&받은주소, &akaliaa_ajutuu) == 9);
    확인(memcmp(atijaaya, "posix-udp", 9) == 0 && akaliaa_ajutuu == 16);
    확인(받은주소.sin_port == wanaawasü_ajutuu.sin_port && 받은주소.sin_addr.s_addr == wanaawasü_ajutuu.sin_addr.s_addr);
    확인(sendto(종단점, "truncate", 8, 0, (struct sockaddr *)&wanaawasü_ajutuu, sizeof wanaawasü_ajutuu) == 8);
    확인(recvfrom(종단점, atijaaya, 3, 0, NULL, NULL) == 3 && memcmp(atijaaya, "tru", 3) == 0);
    확인(recvfrom(종단점, atijaaya, sizeof atijaaya, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    확인(sendto(종단점, NULL, 0, 0, (struct sockaddr *)&wanaawasü_ajutuu, sizeof wanaawasü_ajutuu) == 0);
    확인(recvfrom(종단점, NULL, 0, 0, NULL, NULL) == 0);
    확인(recvfrom(종단점, atijaaya, sizeof atijaaya, 0, NULL, NULL) == -1 && errno == EAGAIN);
    확인(close(종단점) == 0);
    puts("POSIX UDP CHECK PASS");
    return 0;
}
