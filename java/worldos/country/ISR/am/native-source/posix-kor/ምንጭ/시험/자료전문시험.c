#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

#define አረጋግጥ(ሁኔታ) do { if (!(ሁኔታ)) { puts("POSIX UDP CHECK FAILED: " #ሁኔታ); return 1; } } while (0)
int main(int 인수개수, char **ነጋሪ_እሴት_ዝርዝር) {
    አረጋግጥ(인수개수 == 2);
    int የወደብ_ቁጥር = 0;
    for (int ማስገቢያ_ቀዳዳ_ምዝግብ = 0; ነጋሪ_እሴት_ዝርዝር[1][ማስገቢያ_ቀዳዳ_ምዝግብ]; ማስገቢያ_ቀዳዳ_ምዝግብ++) {
        አረጋግጥ(ነጋሪ_እሴት_ዝርዝር[1][ማስገቢያ_ቀዳዳ_ምዝግብ] >= '0' && ነጋሪ_እሴት_ዝርዝር[1][ማስገቢያ_ቀዳዳ_ምዝግብ] <= '9');
        የወደብ_ቁጥር = የወደብ_ቁጥር * 10 + ነጋሪ_እሴት_ዝርዝር[1][ማስገቢያ_ቀዳዳ_ምዝግብ] - '0';
        አረጋግጥ(የወደብ_ቁጥር <= 65535);
    }
    int 종단점 = 통신종단점만들기(AF_INET, SOCK_DGRAM, 0);
    አረጋግጥ(종단점 == 3);
    struct sockaddr_in የአካባቢ_ስፋት = {0}, አቻ_እሴት = {0}, 받은주소 = {0};
    የአካባቢ_ስፋት.sin_family = AF_INET;
    socklen_t ርዝመት_እሴት = sizeof የአካባቢ_ስፋት;
    አረጋግጥ(통신주소읽기(종단점, (struct sockaddr *)&የአካባቢ_ስፋት, &ርዝመት_እሴት) == 0 && የአካባቢ_ስፋት.sin_port == 0);
    አረጋግጥ(አጣምር_አድራሻ(종단점, (struct sockaddr *)&የአካባቢ_ስፋት, sizeof የአካባቢ_ስፋት) == 0);
    አረጋግጥ(통신주소읽기(종단점, (struct sockaddr *)&የአካባቢ_ስፋት, &ርዝመት_እሴት) == 0 && ntohs(የአካባቢ_ስፋት.sin_port) >= 49152);
    አረጋግጥ(አጣምር_አድራሻ(종단점, (struct sockaddr *)&የአካባቢ_ስፋት, sizeof የአካባቢ_ስፋት) == -1 && errno == EINVAL);
    int 둘째 = socket(AF_INET, SOCK_DGRAM, 0);
    አረጋግጥ(bind(둘째, (struct sockaddr *)&የአካባቢ_ስፋት, sizeof የአካባቢ_ስፋት) == -1 && errno == EADDRINUSE);
    አረጋግጥ(close(둘째) == 0);
    둘째 = dup(종단점);
    አረጋግጥ(close(종단점) == 0); 종단점 = 둘째;
    አቻ_እሴት.sin_family = AF_INET; አቻ_እሴት.sin_port = 망차례짧은수(የወደብ_ቁጥር);
    አረጋግጥ(ተንትን_መረብ_አድራሻ(AF_INET, "10.0.2.2", &አቻ_እሴት.sin_addr) == 1);
    struct timeval መጠበቅ_እሴት = {0, 200000};
    አረጋግጥ(ለውጥ_መረብ_ቅንብሮች(종단점, SOL_SOCKET, SO_RCVTIMEO, &መጠበቅ_እሴት, sizeof መጠበቅ_እሴት) == 0);
    char ውሂብ[32];
    አረጋግጥ(자료전문받기(종단점, ውሂብ, sizeof ውሂብ, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    አረጋግጥ(자료전문보내기(종단점, "posix-udp", 9, 0, (struct sockaddr *)&አቻ_እሴት, sizeof አቻ_እሴት) == 9);
    ርዝመት_እሴት = sizeof 받은주소;
    አረጋግጥ(recvfrom(종단점, (void *)0x00100000, 9, 0, NULL, NULL) == -1 && errno == EFAULT);
    አረጋግጥ(자료전문받기(종단점, ውሂብ, sizeof ውሂብ, 0, (struct sockaddr *)&받은주소, &ርዝመት_እሴት) == 9);
    አረጋግጥ(memcmp(ውሂብ, "posix-udp", 9) == 0 && ርዝመት_እሴት == 16);
    አረጋግጥ(받은주소.sin_port == አቻ_እሴት.sin_port && 받은주소.sin_addr.s_addr == አቻ_እሴት.sin_addr.s_addr);
    አረጋግጥ(sendto(종단점, "truncate", 8, 0, (struct sockaddr *)&አቻ_እሴት, sizeof አቻ_እሴት) == 8);
    አረጋግጥ(recvfrom(종단점, ውሂብ, 3, 0, NULL, NULL) == 3 && memcmp(ውሂብ, "tru", 3) == 0);
    አረጋግጥ(recvfrom(종단점, ውሂብ, sizeof ውሂብ, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    አረጋግጥ(sendto(종단점, NULL, 0, 0, (struct sockaddr *)&አቻ_እሴት, sizeof አቻ_እሴት) == 0);
    አረጋግጥ(recvfrom(종단점, NULL, 0, 0, NULL, NULL) == 0);
    አረጋግጥ(recvfrom(종단점, ውሂብ, sizeof ውሂብ, 0, NULL, NULL) == -1 && errno == EAGAIN);
    አረጋግጥ(close(종단점) == 0);
    puts("POSIX UDP CHECK PASS");
    return 0;
}
