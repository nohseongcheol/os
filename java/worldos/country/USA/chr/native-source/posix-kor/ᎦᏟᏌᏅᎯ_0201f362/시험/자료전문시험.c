#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

#define ᎰᎯᏳᏓ(ᎤᏍᏗᏓᏅ) do { if (!(ᎤᏍᏗᏓᏅ)) { puts("POSIX UDP CHECK FAILED: " #ᎤᏍᏗᏓᏅ); return 1; } } while (0)
int main(int 인수개수, char **ᏗᏓᎦᏘᎸᏍᏗ_ᏕᎦᏅᏅᏛ) {
    ᎰᎯᏳᏓ(인수개수 == 2);
    int 접속번호 = 0;
    for (int 칸 = 0; ᏗᏓᎦᏘᎸᏍᏗ_ᏕᎦᏅᏅᏛ[1][칸]; 칸++) {
        ᎰᎯᏳᏓ(ᏗᏓᎦᏘᎸᏍᏗ_ᏕᎦᏅᏅᏛ[1][칸] >= '0' && ᏗᏓᎦᏘᎸᏍᏗ_ᏕᎦᏅᏅᏛ[1][칸] <= '9');
        접속번호 = 접속번호 * 10 + ᏗᏓᎦᏘᎸᏍᏗ_ᏕᎦᏅᏅᏛ[1][칸] - '0';
        ᎰᎯᏳᏓ(접속번호 <= 65535);
    }
    int 종단점 = 통신종단점만들기(AF_INET, SOCK_DGRAM, 0);
    ᎰᎯᏳᏓ(종단점 == 3);
    struct sockaddr_in ᎡᏍᎦᏂ_ᎢᎦᎢ = {0}, ᏱᎦᏲᎩᎾᏛᏂ_ᏧᎬᏩᎶᏗᏯ = {0}, 받은주소 = {0};
    ᎡᏍᎦᏂ_ᎢᎦᎢ.sin_family = AF_INET;
    socklen_t ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ = sizeof ᎡᏍᎦᏂ_ᎢᎦᎢ;
    ᎰᎯᏳᏓ(통신주소읽기(종단점, (struct sockaddr *)&ᎡᏍᎦᏂ_ᎢᎦᎢ, &ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ) == 0 && ᎡᏍᎦᏂ_ᎢᎦᎢ.sin_port == 0);
    ᎰᎯᏳᏓ(BIND_ᎪᏪᎵ_ᏫᏗᎦᏅᏗ(종단점, (struct sockaddr *)&ᎡᏍᎦᏂ_ᎢᎦᎢ, sizeof ᎡᏍᎦᏂ_ᎢᎦᎢ) == 0);
    ᎰᎯᏳᏓ(통신주소읽기(종단점, (struct sockaddr *)&ᎡᏍᎦᏂ_ᎢᎦᎢ, &ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ) == 0 && ntohs(ᎡᏍᎦᏂ_ᎢᎦᎢ.sin_port) >= 49152);
    ᎰᎯᏳᏓ(BIND_ᎪᏪᎵ_ᏫᏗᎦᏅᏗ(종단점, (struct sockaddr *)&ᎡᏍᎦᏂ_ᎢᎦᎢ, sizeof ᎡᏍᎦᏂ_ᎢᎦᎢ) == -1 && errno == EINVAL);
    int 둘째 = socket(AF_INET, SOCK_DGRAM, 0);
    ᎰᎯᏳᏓ(bind(둘째, (struct sockaddr *)&ᎡᏍᎦᏂ_ᎢᎦᎢ, sizeof ᎡᏍᎦᏂ_ᎢᎦᎢ) == -1 && errno == EADDRINUSE);
    ᎰᎯᏳᏓ(close(둘째) == 0);
    둘째 = dup(종단점);
    ᎰᎯᏳᏓ(close(종단점) == 0); 종단점 = 둘째;
    ᏱᎦᏲᎩᎾᏛᏂ_ᏧᎬᏩᎶᏗᏯ.sin_family = AF_INET; ᏱᎦᏲᎩᎾᏛᏂ_ᏧᎬᏩᎶᏗᏯ.sin_port = 망차례짧은수(접속번호);
    ᎰᎯᏳᏓ(망주소해석하기(AF_INET, "10.0.2.2", &ᏱᎦᏲᎩᎾᏛᏂ_ᏧᎬᏩᎶᏗᏯ.sin_addr) == 1);
    struct timeval 대기 = {0, 200000};
    ᎰᎯᏳᏓ(ᎯᏁᏟᏴᎾ_ᏧᎾᏚᏓᎵ_ᏕᎦᎧᎲᎢ(종단점, SOL_SOCKET, SO_RCVTIMEO, &대기, sizeof 대기) == 0);
    char ᎦᏟᏌᏅᎯ[32];
    ᎰᎯᏳᏓ(자료전문받기(종단점, ᎦᏟᏌᏅᎯ, sizeof ᎦᏟᏌᏅᎯ, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    ᎰᎯᏳᏓ(자료전문보내기(종단점, "posix-udp", 9, 0, (struct sockaddr *)&ᏱᎦᏲᎩᎾᏛᏂ_ᏧᎬᏩᎶᏗᏯ, sizeof ᏱᎦᏲᎩᎾᏛᏂ_ᏧᎬᏩᎶᏗᏯ) == 9);
    ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ = sizeof 받은주소;
    ᎰᎯᏳᏓ(recvfrom(종단점, (void *)0x00100000, 9, 0, NULL, NULL) == -1 && errno == EFAULT);
    ᎰᎯᏳᏓ(자료전문받기(종단점, ᎦᏟᏌᏅᎯ, sizeof ᎦᏟᏌᏅᎯ, 0, (struct sockaddr *)&받은주소, &ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ) == 9);
    ᎰᎯᏳᏓ(memcmp(ᎦᏟᏌᏅᎯ, "posix-udp", 9) == 0 && ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ == 16);
    ᎰᎯᏳᏓ(받은주소.sin_port == ᏱᎦᏲᎩᎾᏛᏂ_ᏧᎬᏩᎶᏗᏯ.sin_port && 받은주소.sin_addr.s_addr == ᏱᎦᏲᎩᎾᏛᏂ_ᏧᎬᏩᎶᏗᏯ.sin_addr.s_addr);
    ᎰᎯᏳᏓ(sendto(종단점, "truncate", 8, 0, (struct sockaddr *)&ᏱᎦᏲᎩᎾᏛᏂ_ᏧᎬᏩᎶᏗᏯ, sizeof ᏱᎦᏲᎩᎾᏛᏂ_ᏧᎬᏩᎶᏗᏯ) == 8);
    ᎰᎯᏳᏓ(recvfrom(종단점, ᎦᏟᏌᏅᎯ, 3, 0, NULL, NULL) == 3 && memcmp(ᎦᏟᏌᏅᎯ, "tru", 3) == 0);
    ᎰᎯᏳᏓ(recvfrom(종단점, ᎦᏟᏌᏅᎯ, sizeof ᎦᏟᏌᏅᎯ, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    ᎰᎯᏳᏓ(sendto(종단점, NULL, 0, 0, (struct sockaddr *)&ᏱᎦᏲᎩᎾᏛᏂ_ᏧᎬᏩᎶᏗᏯ, sizeof ᏱᎦᏲᎩᎾᏛᏂ_ᏧᎬᏩᎶᏗᏯ) == 0);
    ᎰᎯᏳᏓ(recvfrom(종단점, NULL, 0, 0, NULL, NULL) == 0);
    ᎰᎯᏳᏓ(recvfrom(종단점, ᎦᏟᏌᏅᎯ, sizeof ᎦᏟᏌᏅᎯ, 0, NULL, NULL) == -1 && errno == EAGAIN);
    ᎰᎯᏳᏓ(close(종단점) == 0);
    puts("POSIX UDP CHECK PASS");
    return 0;
}
