#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

#define ኣረጋግጽ(ኩነታት) do { if (!(ኩነታት)) { puts("POSIX UDP CHECK FAILED: " #ኩነታት); return 1; } } while (0)
int main(int 인수개수, char **ሓባሪ_ቁጽሪ_ዝርዝር) {
    ኣረጋግጽ(인수개수 == 2);
    int 접속번호 = 0;
    for (int መሰኩዒ_ምእታው = 0; ሓባሪ_ቁጽሪ_ዝርዝር[1][መሰኩዒ_ምእታው]; መሰኩዒ_ምእታው++) {
        ኣረጋግጽ(ሓባሪ_ቁጽሪ_ዝርዝር[1][መሰኩዒ_ምእታው] >= '0' && ሓባሪ_ቁጽሪ_ዝርዝር[1][መሰኩዒ_ምእታው] <= '9');
        접속번호 = 접속번호 * 10 + ሓባሪ_ቁጽሪ_ዝርዝር[1][መሰኩዒ_ምእታው] - '0';
        ኣረጋግጽ(접속번호 <= 65535);
    }
    int 종단점 = 통신종단점만들기(AF_INET, SOCK_DGRAM, 0);
    ኣረጋግጽ(종단점 == 3);
    struct sockaddr_in ኣካባብያዊ_ዕምቆት = {0}, መዘና_ዋጋ = {0}, 받은주소 = {0};
    ኣካባብያዊ_ዕምቆት.sin_family = AF_INET;
    socklen_t ንውሓት_ዋጋ = sizeof ኣካባብያዊ_ዕምቆት;
    ኣረጋግጽ(통신주소읽기(종단점, (struct sockaddr *)&ኣካባብያዊ_ዕምቆት, &ንውሓት_ዋጋ) == 0 && ኣካባብያዊ_ዕምቆት.sin_port == 0);
    ኣረጋግጽ(ኣጣምር_ኣድራሻ(종단점, (struct sockaddr *)&ኣካባብያዊ_ዕምቆት, sizeof ኣካባብያዊ_ዕምቆት) == 0);
    ኣረጋግጽ(통신주소읽기(종단점, (struct sockaddr *)&ኣካባብያዊ_ዕምቆት, &ንውሓት_ዋጋ) == 0 && ntohs(ኣካባብያዊ_ዕምቆት.sin_port) >= 49152);
    ኣረጋግጽ(ኣጣምር_ኣድራሻ(종단점, (struct sockaddr *)&ኣካባብያዊ_ዕምቆት, sizeof ኣካባብያዊ_ዕምቆት) == -1 && errno == EINVAL);
    int 둘째 = socket(AF_INET, SOCK_DGRAM, 0);
    ኣረጋግጽ(bind(둘째, (struct sockaddr *)&ኣካባብያዊ_ዕምቆት, sizeof ኣካባብያዊ_ዕምቆት) == -1 && errno == EADDRINUSE);
    ኣረጋግጽ(close(둘째) == 0);
    둘째 = dup(종단점);
    ኣረጋግጽ(close(종단점) == 0); 종단점 = 둘째;
    መዘና_ዋጋ.sin_family = AF_INET; መዘና_ዋጋ.sin_port = 망차례짧은수(접속번호);
    ኣረጋግጽ(망주소해석하기(AF_INET, "10.0.2.2", &መዘና_ዋጋ.sin_addr) == 1);
    struct timeval 대기 = {0, 200000};
    ኣረጋግጽ(ለውጥ_ማሕበራዊ_ኔትወርክ_ኣቀማምጣታት(종단점, SOL_SOCKET, SO_RCVTIMEO, &대기, sizeof 대기) == 0);
    char ሓበሬታ[32];
    ኣረጋግጽ(자료전문받기(종단점, ሓበሬታ, sizeof ሓበሬታ, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    ኣረጋግጽ(자료전문보내기(종단점, "posix-udp", 9, 0, (struct sockaddr *)&መዘና_ዋጋ, sizeof መዘና_ዋጋ) == 9);
    ንውሓት_ዋጋ = sizeof 받은주소;
    ኣረጋግጽ(recvfrom(종단점, (void *)0x00100000, 9, 0, NULL, NULL) == -1 && errno == EFAULT);
    ኣረጋግጽ(자료전문받기(종단점, ሓበሬታ, sizeof ሓበሬታ, 0, (struct sockaddr *)&받은주소, &ንውሓት_ዋጋ) == 9);
    ኣረጋግጽ(memcmp(ሓበሬታ, "posix-udp", 9) == 0 && ንውሓት_ዋጋ == 16);
    ኣረጋግጽ(받은주소.sin_port == መዘና_ዋጋ.sin_port && 받은주소.sin_addr.s_addr == መዘና_ዋጋ.sin_addr.s_addr);
    ኣረጋግጽ(sendto(종단점, "truncate", 8, 0, (struct sockaddr *)&መዘና_ዋጋ, sizeof መዘና_ዋጋ) == 8);
    ኣረጋግጽ(recvfrom(종단점, ሓበሬታ, 3, 0, NULL, NULL) == 3 && memcmp(ሓበሬታ, "tru", 3) == 0);
    ኣረጋግጽ(recvfrom(종단점, ሓበሬታ, sizeof ሓበሬታ, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    ኣረጋግጽ(sendto(종단점, NULL, 0, 0, (struct sockaddr *)&መዘና_ዋጋ, sizeof መዘና_ዋጋ) == 0);
    ኣረጋግጽ(recvfrom(종단점, NULL, 0, 0, NULL, NULL) == 0);
    ኣረጋግጽ(recvfrom(종단점, ሓበሬታ, sizeof ሓበሬታ, 0, NULL, NULL) == -1 && errno == EAGAIN);
    ኣረጋግጽ(close(종단점) == 0);
    puts("POSIX UDP CHECK PASS");
    return 0;
}
