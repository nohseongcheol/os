#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

#define gusuzuma(icyangombwa) do { if (!(icyangombwa)) { puts("POSIX UDP CHECK FAILED: " #icyangombwa); return 1; } } while (0)
int main(int 인수개수, char **ingingo_Urutonde) {
    gusuzuma(인수개수 == 2);
    int 접속번호 = 0;
    for (int umwanya_icyinjizwa = 0; ingingo_Urutonde[1][umwanya_icyinjizwa]; umwanya_icyinjizwa++) {
        gusuzuma(ingingo_Urutonde[1][umwanya_icyinjizwa] >= '0' && ingingo_Urutonde[1][umwanya_icyinjizwa] <= '9');
        접속번호 = 접속번호 * 10 + ingingo_Urutonde[1][umwanya_icyinjizwa] - '0';
        gusuzuma(접속번호 <= 65535);
    }
    int 종단점 = 통신종단점만들기(AF_INET, SOCK_DGRAM, 0);
    gusuzuma(종단점 == 3);
    struct sockaddr_in mu_gace_urwego = {0}, Mugenzi_agaciro = {0}, 받은주소 = {0};
    mu_gace_urwego.sin_family = AF_INET;
    socklen_t uburebure_agaciro = sizeof mu_gace_urwego;
    gusuzuma(통신주소읽기(종단점, (struct sockaddr *)&mu_gace_urwego, &uburebure_agaciro) == 0 && mu_gace_urwego.sin_port == 0);
    gusuzuma(BIND_aderesi(종단점, (struct sockaddr *)&mu_gace_urwego, sizeof mu_gace_urwego) == 0);
    gusuzuma(통신주소읽기(종단점, (struct sockaddr *)&mu_gace_urwego, &uburebure_agaciro) == 0 && ntohs(mu_gace_urwego.sin_port) >= 49152);
    gusuzuma(BIND_aderesi(종단점, (struct sockaddr *)&mu_gace_urwego, sizeof mu_gace_urwego) == -1 && errno == EINVAL);
    int 둘째 = socket(AF_INET, SOCK_DGRAM, 0);
    gusuzuma(bind(둘째, (struct sockaddr *)&mu_gace_urwego, sizeof mu_gace_urwego) == -1 && errno == EADDRINUSE);
    gusuzuma(close(둘째) == 0);
    둘째 = dup(종단점);
    gusuzuma(close(종단점) == 0); 종단점 = 둘째;
    Mugenzi_agaciro.sin_family = AF_INET; Mugenzi_agaciro.sin_port = 망차례짧은수(접속번호);
    gusuzuma(gusesengura_Urusobemiyoboro_aderesi(AF_INET, "10.0.2.2", &Mugenzi_agaciro.sin_addr) == 1);
    struct timeval 대기 = {0, 200000};
    gusuzuma(guhindura_Urusobemiyoboro_Amagenamiterere(종단점, SOL_SOCKET, SO_RCVTIMEO, &대기, sizeof 대기) == 0);
    char amakurushingiro[32];
    gusuzuma(자료전문받기(종단점, amakurushingiro, sizeof amakurushingiro, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    gusuzuma(자료전문보내기(종단점, "posix-udp", 9, 0, (struct sockaddr *)&Mugenzi_agaciro, sizeof Mugenzi_agaciro) == 9);
    uburebure_agaciro = sizeof 받은주소;
    gusuzuma(recvfrom(종단점, (void *)0x00100000, 9, 0, NULL, NULL) == -1 && errno == EFAULT);
    gusuzuma(자료전문받기(종단점, amakurushingiro, sizeof amakurushingiro, 0, (struct sockaddr *)&받은주소, &uburebure_agaciro) == 9);
    gusuzuma(memcmp(amakurushingiro, "posix-udp", 9) == 0 && uburebure_agaciro == 16);
    gusuzuma(받은주소.sin_port == Mugenzi_agaciro.sin_port && 받은주소.sin_addr.s_addr == Mugenzi_agaciro.sin_addr.s_addr);
    gusuzuma(sendto(종단점, "truncate", 8, 0, (struct sockaddr *)&Mugenzi_agaciro, sizeof Mugenzi_agaciro) == 8);
    gusuzuma(recvfrom(종단점, amakurushingiro, 3, 0, NULL, NULL) == 3 && memcmp(amakurushingiro, "tru", 3) == 0);
    gusuzuma(recvfrom(종단점, amakurushingiro, sizeof amakurushingiro, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    gusuzuma(sendto(종단점, NULL, 0, 0, (struct sockaddr *)&Mugenzi_agaciro, sizeof Mugenzi_agaciro) == 0);
    gusuzuma(recvfrom(종단점, NULL, 0, 0, NULL, NULL) == 0);
    gusuzuma(recvfrom(종단점, amakurushingiro, sizeof amakurushingiro, 0, NULL, NULL) == -1 && errno == EAGAIN);
    gusuzuma(close(종단점) == 0);
    puts("POSIX UDP CHECK PASS");
    return 0;
}
