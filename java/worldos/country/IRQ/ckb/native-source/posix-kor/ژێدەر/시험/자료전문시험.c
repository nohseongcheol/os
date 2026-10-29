#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

#define سەلماندن(دۆخ) do { if (!(دۆخ)) { puts("POSIX UDP CHECK FAILED: " #دۆخ); return 1; } } while (0)
int main(int 인수개수, char **ئارگیومێنت_لیست) {
    سەلماندن(인수개수 == 2);
    int 접속번호 = 0;
    for (int کەلێن_بۆ_نووسین_یان_رەمز_تێنووسین = 0; ئارگیومێنت_لیست[1][کەلێن_بۆ_نووسین_یان_رەمز_تێنووسین]; کەلێن_بۆ_نووسین_یان_رەمز_تێنووسین++) {
        سەلماندن(ئارگیومێنت_لیست[1][کەلێن_بۆ_نووسین_یان_رەمز_تێنووسین] >= '0' && ئارگیومێنت_لیست[1][کەلێن_بۆ_نووسین_یان_رەمز_تێنووسین] <= '9');
        접속번호 = 접속번호 * 10 + ئارگیومێنت_لیست[1][کەلێن_بۆ_نووسین_یان_رەمز_تێنووسین] - '0';
        سەلماندن(접속번호 <= 65535);
    }
    int 종단점 = 통신종단점만들기(AF_INET, SOCK_DGRAM, 0);
    سەلماندن(종단점 == 3);
    struct sockaddr_in مەحەلی_داوێنە = {0}, هاوتا_نرخ = {0}, 받은주소 = {0};
    مەحەلی_داوێنە.sin_family = AF_INET;
    socklen_t درێژی_نرخ = sizeof مەحەلی_داوێنە;
    سەلماندن(통신주소읽기(종단점, (struct sockaddr *)&مەحەلی_داوێنە, &درێژی_نرخ) == 0 && مەحەلی_داوێنە.sin_port == 0);
    سەلماندن(BIND_ناونیشان(종단점, (struct sockaddr *)&مەحەلی_داوێنە, sizeof مەحەلی_داوێنە) == 0);
    سەلماندن(통신주소읽기(종단점, (struct sockaddr *)&مەحەلی_داوێنە, &درێژی_نرخ) == 0 && ntohs(مەحەلی_داوێنە.sin_port) >= 49152);
    سەلماندن(BIND_ناونیشان(종단점, (struct sockaddr *)&مەحەلی_داوێنە, sizeof مەحەلی_داوێنە) == -1 && errno == EINVAL);
    int 둘째 = socket(AF_INET, SOCK_DGRAM, 0);
    سەلماندن(bind(둘째, (struct sockaddr *)&مەحەلی_داوێنە, sizeof مەحەلی_داوێنە) == -1 && errno == EADDRINUSE);
    سەلماندن(close(둘째) == 0);
    둘째 = dup(종단점);
    سەلماندن(close(종단점) == 0); 종단점 = 둘째;
    هاوتا_نرخ.sin_family = AF_INET; هاوتا_نرخ.sin_port = 망차례짧은수(접속번호);
    سەلماندن(망주소해석하기(AF_INET, "10.0.2.2", &هاوتا_نرخ.sin_addr) == 1);
    struct timeval چاوەڕوان_کردن_نرخ = {0, 200000};
    سەلماندن(گۆڕین_تۆڕ_ڕێكبەندەكان(종단점, SOL_SOCKET, SO_RCVTIMEO, &چاوەڕوان_کردن_نرخ, sizeof چاوەڕوان_کردن_نرخ) == 0);
    char دەیتا[32];
    سەلماندن(자료전문받기(종단점, دەیتا, sizeof دەیتا, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    سەلماندن(자료전문보내기(종단점, "posix-udp", 9, 0, (struct sockaddr *)&هاوتا_نرخ, sizeof هاوتا_نرخ) == 9);
    درێژی_نرخ = sizeof 받은주소;
    سەلماندن(recvfrom(종단점, (void *)0x00100000, 9, 0, NULL, NULL) == -1 && errno == EFAULT);
    سەلماندن(자료전문받기(종단점, دەیتا, sizeof دەیتا, 0, (struct sockaddr *)&받은주소, &درێژی_نرخ) == 9);
    سەلماندن(memcmp(دەیتا, "posix-udp", 9) == 0 && درێژی_نرخ == 16);
    سەلماندن(받은주소.sin_port == هاوتا_نرخ.sin_port && 받은주소.sin_addr.s_addr == هاوتا_نرخ.sin_addr.s_addr);
    سەلماندن(sendto(종단점, "truncate", 8, 0, (struct sockaddr *)&هاوتا_نرخ, sizeof هاوتا_نرخ) == 8);
    سەلماندن(recvfrom(종단점, دەیتا, 3, 0, NULL, NULL) == 3 && memcmp(دەیتا, "tru", 3) == 0);
    سەلماندن(recvfrom(종단점, دەیتا, sizeof دەیتا, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    سەلماندن(sendto(종단점, NULL, 0, 0, (struct sockaddr *)&هاوتا_نرخ, sizeof هاوتا_نرخ) == 0);
    سەلماندن(recvfrom(종단점, NULL, 0, 0, NULL, NULL) == 0);
    سەلماندن(recvfrom(종단점, دەیتا, sizeof دەیتا, 0, NULL, NULL) == -1 && errno == EAGAIN);
    سەلماندن(close(종단점) == 0);
    puts("POSIX UDP CHECK PASS");
    return 0;
}
