#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

#define තහවුරු_කරන්න(තත්වය) do { if (!(තත්වය)) { puts("POSIX UDP CHECK FAILED: " #තත්වය); return 1; } } while (0)
int main(int 인수개수, char **විස්තාරකය_ලැයිස්තුව) {
    තහවුරු_කරන්න(인수개수 == 2);
    int 접속번호 = 0;
    for (int විවරය_පිවිසුම = 0; විස්තාරකය_ලැයිස්තුව[1][විවරය_පිවිසුම]; විවරය_පිවිසුම++) {
        තහවුරු_කරන්න(විස්තාරකය_ලැයිස්තුව[1][විවරය_පිවිසුම] >= '0' && විස්තාරකය_ලැයිස්තුව[1][විවරය_පිවිසුම] <= '9');
        접속번호 = 접속번호 * 10 + විස්තාරකය_ලැයිස්තුව[1][විවරය_පිවිසුම] - '0';
        තහවුරු_කරන්න(접속번호 <= 65535);
    }
    int 종단점 = 통신종단점만들기(AF_INET, SOCK_DGRAM, 0);
    තහවුරු_කරන්න(종단점 == 3);
    struct sockaddr_in ස්ව_විෂය_පථය = {0}, සමානයා_අගය = {0}, 받은주소 = {0};
    ස්ව_විෂය_පථය.sin_family = AF_INET;
    socklen_t දිග_අගය = sizeof ස්ව_විෂය_පථය;
    තහවුරු_කරන්න(통신주소읽기(종단점, (struct sockaddr *)&ස්ව_විෂය_පථය, &දිග_අගය) == 0 && ස්ව_විෂය_පථය.sin_port == 0);
    තහවුරු_කරන්න(බඳින්න_යොමුව(종단점, (struct sockaddr *)&ස්ව_විෂය_පථය, sizeof ස්ව_විෂය_පථය) == 0);
    තහවුරු_කරන්න(통신주소읽기(종단점, (struct sockaddr *)&ස්ව_විෂය_පථය, &දිග_අගය) == 0 && ntohs(ස්ව_විෂය_පථය.sin_port) >= 49152);
    තහවුරු_කරන්න(බඳින්න_යොමුව(종단점, (struct sockaddr *)&ස්ව_විෂය_පථය, sizeof ස්ව_විෂය_පථය) == -1 && errno == EINVAL);
    int 둘째 = socket(AF_INET, SOCK_DGRAM, 0);
    තහවුරු_කරන්න(bind(둘째, (struct sockaddr *)&ස්ව_විෂය_පථය, sizeof ස්ව_විෂය_පථය) == -1 && errno == EADDRINUSE);
    තහවුරු_කරන්න(close(둘째) == 0);
    둘째 = dup(종단점);
    තහවුරු_කරන්න(close(종단점) == 0); 종단점 = 둘째;
    සමානයා_අගය.sin_family = AF_INET; සමානයා_අගය.sin_port = 망차례짧은수(접속번호);
    තහවුරු_කරන්න(විශ්ලේෂණය_කරන්න_ජාලය_යොමුව(AF_INET, "10.0.2.2", &සමානයා_අගය.sin_addr) == 1);
    struct timeval 대기 = {0, 200000};
    තහවුරු_කරන්න(වෙනස්_කරන්න_ජාලය_පසුතල(종단점, SOL_SOCKET, SO_RCVTIMEO, &대기, sizeof 대기) == 0);
    char දත්ත[32];
    තහවුරු_කරන්න(자료전문받기(종단점, දත්ත, sizeof දත්ත, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    තහවුරු_කරන්න(자료전문보내기(종단점, "posix-udp", 9, 0, (struct sockaddr *)&සමානයා_අගය, sizeof සමානයා_අගය) == 9);
    දිග_අගය = sizeof 받은주소;
    තහවුරු_කරන්න(recvfrom(종단점, (void *)0x00100000, 9, 0, NULL, NULL) == -1 && errno == EFAULT);
    තහවුරු_කරන්න(자료전문받기(종단점, දත්ත, sizeof දත්ත, 0, (struct sockaddr *)&받은주소, &දිග_අගය) == 9);
    තහවුරු_කරන්න(memcmp(දත්ත, "posix-udp", 9) == 0 && දිග_අගය == 16);
    තහවුරු_කරන්න(받은주소.sin_port == සමානයා_අගය.sin_port && 받은주소.sin_addr.s_addr == සමානයා_අගය.sin_addr.s_addr);
    තහවුරු_කරන්න(sendto(종단점, "truncate", 8, 0, (struct sockaddr *)&සමානයා_අගය, sizeof සමානයා_අගය) == 8);
    තහවුරු_කරන්න(recvfrom(종단점, දත්ත, 3, 0, NULL, NULL) == 3 && memcmp(දත්ත, "tru", 3) == 0);
    තහවුරු_කරන්න(recvfrom(종단점, දත්ත, sizeof දත්ත, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    තහවුරු_කරන්න(sendto(종단점, NULL, 0, 0, (struct sockaddr *)&සමානයා_අගය, sizeof සමානයා_අගය) == 0);
    තහවුරු_කරන්න(recvfrom(종단점, NULL, 0, 0, NULL, NULL) == 0);
    තහවුරු_කරන්න(recvfrom(종단점, දත්ත, sizeof දත්ත, 0, NULL, NULL) == -1 && errno == EAGAIN);
    තහවුරු_කරන්න(close(종단점) == 0);
    puts("POSIX UDP CHECK PASS");
    return 0;
}
