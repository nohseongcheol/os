#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

#define thibitisha(sharti) do { if (!(sharti)) { puts("POSIX UDP CHECK FAILED: " #sharti); return 1; } } while (0)
int main(int 인수개수, char **hoja_Orodha) {
    thibitisha(인수개수 == 2);
    int namba_ya_kituo = 0;
    for (int Sloti_ingizo = 0; hoja_Orodha[1][Sloti_ingizo]; Sloti_ingizo++) {
        thibitisha(hoja_Orodha[1][Sloti_ingizo] >= '0' && hoja_Orodha[1][Sloti_ingizo] <= '9');
        namba_ya_kituo = namba_ya_kituo * 10 + hoja_Orodha[1][Sloti_ingizo] - '0';
        thibitisha(namba_ya_kituo <= 65535);
    }
    int 종단점 = 통신종단점만들기(AF_INET, SOCK_DGRAM, 0);
    thibitisha(종단점 == 3);
    struct sockaddr_in jirani_upeo = {0}, kompyuta_rika_thamani = {0}, 받은주소 = {0};
    jirani_upeo.sin_family = AF_INET;
    socklen_t urefu_thamani = sizeof jirani_upeo;
    thibitisha(통신주소읽기(종단점, (struct sockaddr *)&jirani_upeo, &urefu_thamani) == 0 && jirani_upeo.sin_port == 0);
    thibitisha(FUNGA_anwani(종단점, (struct sockaddr *)&jirani_upeo, sizeof jirani_upeo) == 0);
    thibitisha(통신주소읽기(종단점, (struct sockaddr *)&jirani_upeo, &urefu_thamani) == 0 && ntohs(jirani_upeo.sin_port) >= 49152);
    thibitisha(FUNGA_anwani(종단점, (struct sockaddr *)&jirani_upeo, sizeof jirani_upeo) == -1 && errno == EINVAL);
    int 둘째 = socket(AF_INET, SOCK_DGRAM, 0);
    thibitisha(bind(둘째, (struct sockaddr *)&jirani_upeo, sizeof jirani_upeo) == -1 && errno == EADDRINUSE);
    thibitisha(close(둘째) == 0);
    둘째 = dup(종단점);
    thibitisha(close(종단점) == 0); 종단점 = 둘째;
    kompyuta_rika_thamani.sin_family = AF_INET; kompyuta_rika_thamani.sin_port = 망차례짧은수(namba_ya_kituo);
    thibitisha(changanua_Mtandao_anwani(AF_INET, "10.0.2.2", &kompyuta_rika_thamani.sin_addr) == 1);
    struct timeval subiri_thamani = {0, 200000};
    thibitisha(badilisha_Mtandao_Mipangilio(종단점, SOL_SOCKET, SO_RCVTIMEO, &subiri_thamani, sizeof subiri_thamani) == 0);
    char data[32];
    thibitisha(자료전문받기(종단점, data, sizeof data, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    thibitisha(자료전문보내기(종단점, "posix-udp", 9, 0, (struct sockaddr *)&kompyuta_rika_thamani, sizeof kompyuta_rika_thamani) == 9);
    urefu_thamani = sizeof 받은주소;
    thibitisha(recvfrom(종단점, (void *)0x00100000, 9, 0, NULL, NULL) == -1 && errno == EFAULT);
    thibitisha(자료전문받기(종단점, data, sizeof data, 0, (struct sockaddr *)&받은주소, &urefu_thamani) == 9);
    thibitisha(memcmp(data, "posix-udp", 9) == 0 && urefu_thamani == 16);
    thibitisha(받은주소.sin_port == kompyuta_rika_thamani.sin_port && 받은주소.sin_addr.s_addr == kompyuta_rika_thamani.sin_addr.s_addr);
    thibitisha(sendto(종단점, "truncate", 8, 0, (struct sockaddr *)&kompyuta_rika_thamani, sizeof kompyuta_rika_thamani) == 8);
    thibitisha(recvfrom(종단점, data, 3, 0, NULL, NULL) == 3 && memcmp(data, "tru", 3) == 0);
    thibitisha(recvfrom(종단점, data, sizeof data, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    thibitisha(sendto(종단점, NULL, 0, 0, (struct sockaddr *)&kompyuta_rika_thamani, sizeof kompyuta_rika_thamani) == 0);
    thibitisha(recvfrom(종단점, NULL, 0, 0, NULL, NULL) == 0);
    thibitisha(recvfrom(종단점, data, sizeof data, 0, NULL, NULL) == -1 && errno == EAGAIN);
    thibitisha(close(종단점) == 0);
    puts("POSIX UDP CHECK PASS");
    return 0;
}
