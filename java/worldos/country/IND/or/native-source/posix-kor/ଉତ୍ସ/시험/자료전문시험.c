#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

#define ଯାଞ୍ଚ୍_କରିବା(ସର୍ତ୍ତ) do { if (!(ସର୍ତ୍ତ)) { puts("POSIX UDP CHECK FAILED: " #ସର୍ତ୍ତ); return 1; } } while (0)
int main(int 인수개수, char **ଯୁକ୍ତି_ତାଲିକା) {
    ଯାଞ୍ଚ୍_କରିବା(인수개수 == 2);
    int ପୋର୍ଟ୍_ନମ୍ଵର୍ = 0;
    for (int ସ୍ଲଟ୍_ଏଣ୍ଟ୍ରି = 0; ଯୁକ୍ତି_ତାଲିକା[1][ସ୍ଲଟ୍_ଏଣ୍ଟ୍ରି]; ସ୍ଲଟ୍_ଏଣ୍ଟ୍ରି++) {
        ଯାଞ୍ଚ୍_କରିବା(ଯୁକ୍ତି_ତାଲିକା[1][ସ୍ଲଟ୍_ଏଣ୍ଟ୍ରି] >= '0' && ଯୁକ୍ତି_ତାଲିକା[1][ସ୍ଲଟ୍_ଏଣ୍ଟ୍ରି] <= '9');
        ପୋର୍ଟ୍_ନମ୍ଵର୍ = ପୋର୍ଟ୍_ନମ୍ଵର୍ * 10 + ଯୁକ୍ତି_ତାଲିକା[1][ସ୍ଲଟ୍_ଏଣ୍ଟ୍ରି] - '0';
        ଯାଞ୍ଚ୍_କରିବା(ପୋର୍ଟ୍_ନମ୍ଵର୍ <= 65535);
    }
    int 종단점 = 통신종단점만들기(AF_INET, SOCK_DGRAM, 0);
    ଯାଞ୍ଚ୍_କରିବା(종단점 == 3);
    struct sockaddr_in ସ୍ଥାନୀୟ_ପରିସର = {0}, ସମକକ୍ଷ_ମୂଲ୍ୟ = {0}, 받은주소 = {0};
    ସ୍ଥାନୀୟ_ପରିସର.sin_family = AF_INET;
    socklen_t ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ = sizeof ସ୍ଥାନୀୟ_ପରିସର;
    ଯାଞ୍ଚ୍_କରିବା(통신주소읽기(종단점, (struct sockaddr *)&ସ୍ଥାନୀୟ_ପରିସର, &ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ) == 0 && ସ୍ଥାନୀୟ_ପରିସର.sin_port == 0);
    ଯାଞ୍ଚ୍_କରିବା(ବନ୍ଧନ_ଠିକଣା(종단점, (struct sockaddr *)&ସ୍ଥାନୀୟ_ପରିସର, sizeof ସ୍ଥାନୀୟ_ପରିସର) == 0);
    ଯାଞ୍ଚ୍_କରିବା(통신주소읽기(종단점, (struct sockaddr *)&ସ୍ଥାନୀୟ_ପରିସର, &ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ) == 0 && ntohs(ସ୍ଥାନୀୟ_ପରିସର.sin_port) >= 49152);
    ଯାଞ୍ଚ୍_କରିବା(ବନ୍ଧନ_ଠିକଣା(종단점, (struct sockaddr *)&ସ୍ଥାନୀୟ_ପରିସର, sizeof ସ୍ଥାନୀୟ_ପରିସର) == -1 && errno == EINVAL);
    int 둘째 = socket(AF_INET, SOCK_DGRAM, 0);
    ଯାଞ୍ଚ୍_କରିବା(bind(둘째, (struct sockaddr *)&ସ୍ଥାନୀୟ_ପରିସର, sizeof ସ୍ଥାନୀୟ_ପରିସର) == -1 && errno == EADDRINUSE);
    ଯାଞ୍ଚ୍_କରିବା(close(둘째) == 0);
    둘째 = dup(종단점);
    ଯାଞ୍ଚ୍_କରିବା(close(종단점) == 0); 종단점 = 둘째;
    ସମକକ୍ଷ_ମୂଲ୍ୟ.sin_family = AF_INET; ସମକକ୍ଷ_ମୂଲ୍ୟ.sin_port = 망차례짧은수(ପୋର୍ଟ୍_ନମ୍ଵର୍);
    ଯାଞ୍ଚ୍_କରିବା(ପାର୍ସ_ନେଟ୍_ୱାର୍କ୍_ଠିକଣା(AF_INET, "10.0.2.2", &ସମକକ୍ଷ_ମୂଲ୍ୟ.sin_addr) == 1);
    struct timeval ଅପେକ୍ଷା_ମୂଲ୍ୟ = {0, 200000};
    ଯାଞ୍ଚ୍_କରିବା(ପରିବର୍ତ୍ତନ_ନେଟ୍_ୱାର୍କ୍_ସେଟିଂସ୍(종단점, SOL_SOCKET, SO_RCVTIMEO, &ଅପେକ୍ଷା_ମୂଲ୍ୟ, sizeof ଅପେକ୍ଷା_ମୂଲ୍ୟ) == 0);
    char ଡାଟା[32];
    ଯାଞ୍ଚ୍_କରିବା(자료전문받기(종단점, ଡାଟା, sizeof ଡାଟା, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    ଯାଞ୍ଚ୍_କରିବା(자료전문보내기(종단점, "posix-udp", 9, 0, (struct sockaddr *)&ସମକକ୍ଷ_ମୂଲ୍ୟ, sizeof ସମକକ୍ଷ_ମୂଲ୍ୟ) == 9);
    ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ = sizeof 받은주소;
    ଯାଞ୍ଚ୍_କରିବା(recvfrom(종단점, (void *)0x00100000, 9, 0, NULL, NULL) == -1 && errno == EFAULT);
    ଯାଞ୍ଚ୍_କରିବା(자료전문받기(종단점, ଡାଟା, sizeof ଡାଟା, 0, (struct sockaddr *)&받은주소, &ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ) == 9);
    ଯାଞ୍ଚ୍_କରିବା(memcmp(ଡାଟା, "posix-udp", 9) == 0 && ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ == 16);
    ଯାଞ୍ଚ୍_କରିବା(받은주소.sin_port == ସମକକ୍ଷ_ମୂଲ୍ୟ.sin_port && 받은주소.sin_addr.s_addr == ସମକକ୍ଷ_ମୂଲ୍ୟ.sin_addr.s_addr);
    ଯାଞ୍ଚ୍_କରିବା(sendto(종단점, "truncate", 8, 0, (struct sockaddr *)&ସମକକ୍ଷ_ମୂଲ୍ୟ, sizeof ସମକକ୍ଷ_ମୂଲ୍ୟ) == 8);
    ଯାଞ୍ଚ୍_କରିବା(recvfrom(종단점, ଡାଟା, 3, 0, NULL, NULL) == 3 && memcmp(ଡାଟା, "tru", 3) == 0);
    ଯାଞ୍ଚ୍_କରିବା(recvfrom(종단점, ଡାଟା, sizeof ଡାଟା, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    ଯାଞ୍ଚ୍_କରିବା(sendto(종단점, NULL, 0, 0, (struct sockaddr *)&ସମକକ୍ଷ_ମୂଲ୍ୟ, sizeof ସମକକ୍ଷ_ମୂଲ୍ୟ) == 0);
    ଯାଞ୍ଚ୍_କରିବା(recvfrom(종단점, NULL, 0, 0, NULL, NULL) == 0);
    ଯାଞ୍ଚ୍_କରିବା(recvfrom(종단점, ଡାଟା, sizeof ଡାଟା, 0, NULL, NULL) == -1 && errno == EAGAIN);
    ଯାଞ୍ଚ୍_କରିବା(close(종단점) == 0);
    puts("POSIX UDP CHECK PASS");
    return 0;
}
