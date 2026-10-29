#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

#define ચકાસવું(શરત) do { if (!(શરત)) { puts("POSIX UDP CHECK FAILED: " #શરત); return 1; } } while (0)
int main(int 인수개수, char **દલીલ_સૂચી) {
    ચકાસવું(인수개수 == 2);
    int પોર્ટ_નંબર = 0;
    for (int સ્લૉટ_પ્રવેશ = 0; દલીલ_સૂચી[1][સ્લૉટ_પ્રવેશ]; સ્લૉટ_પ્રવેશ++) {
        ચકાસવું(દલીલ_સૂચી[1][સ્લૉટ_પ્રવેશ] >= '0' && દલીલ_સૂચી[1][સ્લૉટ_પ્રવેશ] <= '9');
        પોર્ટ_નંબર = પોર્ટ_નંબર * 10 + દલીલ_સૂચી[1][સ્લૉટ_પ્રવેશ] - '0';
        ચકાસવું(પોર્ટ_નંબર <= 65535);
    }
    int 종단점 = 통신종단점만들기(AF_INET, SOCK_DGRAM, 0);
    ચકાસવું(종단점 == 3);
    struct sockaddr_in સ્થાનિક_અવકાશ = {0}, પીઅર_મૂલ્ય = {0}, 받은주소 = {0};
    સ્થાનિક_અવકાશ.sin_family = AF_INET;
    socklen_t લંબાઈ_મૂલ્ય = sizeof સ્થાનિક_અવકાશ;
    ચકાસવું(통신주소읽기(종단점, (struct sockaddr *)&સ્થાનિક_અવકાશ, &લંબાઈ_મૂલ્ય) == 0 && સ્થાનિક_અવકાશ.sin_port == 0);
    ચકાસવું(બાઇંડ_કરો_સરનામું(종단점, (struct sockaddr *)&સ્થાનિક_અવકાશ, sizeof સ્થાનિક_અવકાશ) == 0);
    ચકાસવું(통신주소읽기(종단점, (struct sockaddr *)&સ્થાનિક_અવકાશ, &લંબાઈ_મૂલ્ય) == 0 && ntohs(સ્થાનિક_અવકાશ.sin_port) >= 49152);
    ચકાસવું(બાઇંડ_કરો_સરનામું(종단점, (struct sockaddr *)&સ્થાનિક_અવકાશ, sizeof સ્થાનિક_અવકાશ) == -1 && errno == EINVAL);
    int 둘째 = socket(AF_INET, SOCK_DGRAM, 0);
    ચકાસવું(bind(둘째, (struct sockaddr *)&સ્થાનિક_અવકાશ, sizeof સ્થાનિક_અવકાશ) == -1 && errno == EADDRINUSE);
    ચકાસવું(close(둘째) == 0);
    둘째 = dup(종단점);
    ચકાસવું(close(종단점) == 0); 종단점 = 둘째;
    પીઅર_મૂલ્ય.sin_family = AF_INET; પીઅર_મૂલ્ય.sin_port = 망차례짧은수(પોર્ટ_નંબર);
    ચકાસવું(પાર્સ_કરો_નેટવર્ક_સરનામું(AF_INET, "10.0.2.2", &પીઅર_મૂલ્ય.sin_addr) == 1);
    struct timeval પ્રતીક્ષા_મૂલ્ય = {0, 200000};
    ચકાસવું(પરિવર્તન_કરો_નેટવર્ક_સેટિંગ્સ(종단점, SOL_SOCKET, SO_RCVTIMEO, &પ્રતીક્ષા_મૂલ્ય, sizeof પ્રતીક્ષા_મૂલ્ય) == 0);
    char ડેટા[32];
    ચકાસવું(자료전문받기(종단점, ડેટા, sizeof ડેટા, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    ચકાસવું(자료전문보내기(종단점, "posix-udp", 9, 0, (struct sockaddr *)&પીઅર_મૂલ્ય, sizeof પીઅર_મૂલ્ય) == 9);
    લંબાઈ_મૂલ્ય = sizeof 받은주소;
    ચકાસવું(recvfrom(종단점, (void *)0x00100000, 9, 0, NULL, NULL) == -1 && errno == EFAULT);
    ચકાસવું(자료전문받기(종단점, ડેટા, sizeof ડેટા, 0, (struct sockaddr *)&받은주소, &લંબાઈ_મૂલ્ય) == 9);
    ચકાસવું(memcmp(ડેટા, "posix-udp", 9) == 0 && લંબાઈ_મૂલ્ય == 16);
    ચકાસવું(받은주소.sin_port == પીઅર_મૂલ્ય.sin_port && 받은주소.sin_addr.s_addr == પીઅર_મૂલ્ય.sin_addr.s_addr);
    ચકાસવું(sendto(종단점, "truncate", 8, 0, (struct sockaddr *)&પીઅર_મૂલ્ય, sizeof પીઅર_મૂલ્ય) == 8);
    ચકાસવું(recvfrom(종단점, ડેટા, 3, 0, NULL, NULL) == 3 && memcmp(ડેટા, "tru", 3) == 0);
    ચકાસવું(recvfrom(종단점, ડેટા, sizeof ડેટા, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    ચકાસવું(sendto(종단점, NULL, 0, 0, (struct sockaddr *)&પીઅર_મૂલ્ય, sizeof પીઅર_મૂલ્ય) == 0);
    ચકાસવું(recvfrom(종단점, NULL, 0, 0, NULL, NULL) == 0);
    ચકાસવું(recvfrom(종단점, ડેટા, sizeof ડેટા, 0, NULL, NULL) == -1 && errno == EAGAIN);
    ચકાસવું(close(종단점) == 0);
    puts("POSIX UDP CHECK PASS");
    return 0;
}
