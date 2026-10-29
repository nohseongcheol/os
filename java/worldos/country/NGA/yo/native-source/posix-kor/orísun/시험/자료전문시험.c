#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

#define ridájú(kání) do { if (!(kání)) { puts("POSIX UDP CHECK FAILED: " #kání); return 1; } } while (0)
int main(int 인수개수, char **ágúmẹ́ntì_Àtòkọ) {
    ridájú(인수개수 == 2);
    int 접속번호 = 0;
    for (int ààyè_ìfàyọkàsí_ìgbéwọlé = 0; ágúmẹ́ntì_Àtòkọ[1][ààyè_ìfàyọkàsí_ìgbéwọlé]; ààyè_ìfàyọkàsí_ìgbéwọlé++) {
        ridájú(ágúmẹ́ntì_Àtòkọ[1][ààyè_ìfàyọkàsí_ìgbéwọlé] >= '0' && ágúmẹ́ntì_Àtòkọ[1][ààyè_ìfàyọkàsí_ìgbéwọlé] <= '9');
        접속번호 = 접속번호 * 10 + ágúmẹ́ntì_Àtòkọ[1][ààyè_ìfàyọkàsí_ìgbéwọlé] - '0';
        ridájú(접속번호 <= 65535);
    }
    int 종단점 = 통신종단점만들기(AF_INET, SOCK_DGRAM, 0);
    ridájú(종단점 == 3);
    struct sockaddr_in agbègbè_sàkání = {0}, ọ̀gbà_iye = {0}, 받은주소 = {0};
    agbègbè_sàkání.sin_family = AF_INET;
    socklen_t gígùn_iye = sizeof agbègbè_sàkání;
    ridájú(통신주소읽기(종단점, (struct sockaddr *)&agbègbè_sàkání, &gígùn_iye) == 0 && agbègbè_sàkání.sin_port == 0);
    ridájú(BIND_àdírẹ́ẹ̀sì(종단점, (struct sockaddr *)&agbègbè_sàkání, sizeof agbègbè_sàkání) == 0);
    ridájú(통신주소읽기(종단점, (struct sockaddr *)&agbègbè_sàkání, &gígùn_iye) == 0 && ntohs(agbègbè_sàkání.sin_port) >= 49152);
    ridájú(BIND_àdírẹ́ẹ̀sì(종단점, (struct sockaddr *)&agbègbè_sàkání, sizeof agbègbè_sàkání) == -1 && errno == EINVAL);
    int 둘째 = socket(AF_INET, SOCK_DGRAM, 0);
    ridájú(bind(둘째, (struct sockaddr *)&agbègbè_sàkání, sizeof agbègbè_sàkání) == -1 && errno == EADDRINUSE);
    ridájú(close(둘째) == 0);
    둘째 = dup(종단점);
    ridájú(close(종단점) == 0); 종단점 = 둘째;
    ọ̀gbà_iye.sin_family = AF_INET; ọ̀gbà_iye.sin_port = 망차례짧은수(접속번호);
    ridájú(ìpínsíwẹ́wẹ́_Alásopọ̀_àdírẹ́ẹ̀sì(AF_INET, "10.0.2.2", &ọ̀gbà_iye.sin_addr) == 1);
    struct timeval 대기 = {0, 200000};
    ridájú(ṣàyípadà_Alásopọ̀_Àwọn_ààtò(종단점, SOL_SOCKET, SO_RCVTIMEO, &대기, sizeof 대기) == 0);
    char détà[32];
    ridájú(자료전문받기(종단점, détà, sizeof détà, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    ridájú(자료전문보내기(종단점, "posix-udp", 9, 0, (struct sockaddr *)&ọ̀gbà_iye, sizeof ọ̀gbà_iye) == 9);
    gígùn_iye = sizeof 받은주소;
    ridájú(recvfrom(종단점, (void *)0x00100000, 9, 0, NULL, NULL) == -1 && errno == EFAULT);
    ridájú(자료전문받기(종단점, détà, sizeof détà, 0, (struct sockaddr *)&받은주소, &gígùn_iye) == 9);
    ridájú(memcmp(détà, "posix-udp", 9) == 0 && gígùn_iye == 16);
    ridájú(받은주소.sin_port == ọ̀gbà_iye.sin_port && 받은주소.sin_addr.s_addr == ọ̀gbà_iye.sin_addr.s_addr);
    ridájú(sendto(종단점, "truncate", 8, 0, (struct sockaddr *)&ọ̀gbà_iye, sizeof ọ̀gbà_iye) == 8);
    ridájú(recvfrom(종단점, détà, 3, 0, NULL, NULL) == 3 && memcmp(détà, "tru", 3) == 0);
    ridájú(recvfrom(종단점, détà, sizeof détà, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    ridájú(sendto(종단점, NULL, 0, 0, (struct sockaddr *)&ọ̀gbà_iye, sizeof ọ̀gbà_iye) == 0);
    ridájú(recvfrom(종단점, NULL, 0, 0, NULL, NULL) == 0);
    ridájú(recvfrom(종단점, détà, sizeof détà, 0, NULL, NULL) == -1 && errno == EAGAIN);
    ridájú(close(종단점) == 0);
    puts("POSIX UDP CHECK PASS");
    return 0;
}
