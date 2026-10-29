#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

#define रुजू_गर्नुहोस्(सर्त) do { if (!(सर्त)) { puts("POSIX UDP CHECK FAILED: " #सर्त); return 1; } } while (0)
int main(int 인수개수, char **तर्क_सूची) {
    रुजू_गर्नुहोस्(인수개수 == 2);
    int 접속번호 = 0;
    for (int स्लट_प्रविष्टि = 0; तर्क_सूची[1][स्लट_प्रविष्टि]; स्लट_प्रविष्टि++) {
        रुजू_गर्नुहोस्(तर्क_सूची[1][स्लट_प्रविष्टि] >= '0' && तर्क_सूची[1][स्लट_प्रविष्टि] <= '9');
        접속번호 = 접속번호 * 10 + तर्क_सूची[1][स्लट_प्रविष्टि] - '0';
        रुजू_गर्नुहोस्(접속번호 <= 65535);
    }
    int 종단점 = 통신종단점만들기(AF_INET, SOCK_DGRAM, 0);
    रुजू_गर्नुहोस्(종단점 == 3);
    struct sockaddr_in स्थानीय_क्षेत्र = {0}, समान_मान = {0}, 받은주소 = {0};
    स्थानीय_क्षेत्र.sin_family = AF_INET;
    socklen_t लम्बाइ_मान = sizeof स्थानीय_क्षेत्र;
    रुजू_गर्नुहोस्(통신주소읽기(종단점, (struct sockaddr *)&स्थानीय_क्षेत्र, &लम्बाइ_मान) == 0 && स्थानीय_क्षेत्र.sin_port == 0);
    रुजू_गर्नुहोस्(बाँध्नु_ठेगाना(종단점, (struct sockaddr *)&स्थानीय_क्षेत्र, sizeof स्थानीय_क्षेत्र) == 0);
    रुजू_गर्नुहोस्(통신주소읽기(종단점, (struct sockaddr *)&स्थानीय_क्षेत्र, &लम्बाइ_मान) == 0 && ntohs(स्थानीय_क्षेत्र.sin_port) >= 49152);
    रुजू_गर्नुहोस्(बाँध्नु_ठेगाना(종단점, (struct sockaddr *)&स्थानीय_क्षेत्र, sizeof स्थानीय_क्षेत्र) == -1 && errno == EINVAL);
    int 둘째 = socket(AF_INET, SOCK_DGRAM, 0);
    रुजू_गर्नुहोस्(bind(둘째, (struct sockaddr *)&स्थानीय_क्षेत्र, sizeof स्थानीय_क्षेत्र) == -1 && errno == EADDRINUSE);
    रुजू_गर्नुहोस्(close(둘째) == 0);
    둘째 = dup(종단점);
    रुजू_गर्नुहोस्(close(종단점) == 0); 종단점 = 둘째;
    समान_मान.sin_family = AF_INET; समान_मान.sin_port = 망차례짧은수(접속번호);
    रुजू_गर्नुहोस्(पदच्छेद_गर्नुहोस्_सञ्जाल_ठेगाना(AF_INET, "10.0.2.2", &समान_मान.sin_addr) == 1);
    struct timeval 대기 = {0, 200000};
    रुजू_गर्नुहोस्(परिवर्तन_सञ्जाल_सेटिङहरू(종단점, SOL_SOCKET, SO_RCVTIMEO, &대기, sizeof 대기) == 0);
    char लगत[32];
    रुजू_गर्नुहोस्(자료전문받기(종단점, लगत, sizeof लगत, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    रुजू_गर्नुहोस्(자료전문보내기(종단점, "posix-udp", 9, 0, (struct sockaddr *)&समान_मान, sizeof समान_मान) == 9);
    लम्बाइ_मान = sizeof 받은주소;
    रुजू_गर्नुहोस्(recvfrom(종단점, (void *)0x00100000, 9, 0, NULL, NULL) == -1 && errno == EFAULT);
    रुजू_गर्नुहोस्(자료전문받기(종단점, लगत, sizeof लगत, 0, (struct sockaddr *)&받은주소, &लम्बाइ_मान) == 9);
    रुजू_गर्नुहोस्(memcmp(लगत, "posix-udp", 9) == 0 && लम्बाइ_मान == 16);
    रुजू_गर्नुहोस्(받은주소.sin_port == समान_मान.sin_port && 받은주소.sin_addr.s_addr == समान_मान.sin_addr.s_addr);
    रुजू_गर्नुहोस्(sendto(종단점, "truncate", 8, 0, (struct sockaddr *)&समान_मान, sizeof समान_मान) == 8);
    रुजू_गर्नुहोस्(recvfrom(종단점, लगत, 3, 0, NULL, NULL) == 3 && memcmp(लगत, "tru", 3) == 0);
    रुजू_गर्नुहोस्(recvfrom(종단점, लगत, sizeof लगत, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    रुजू_गर्नुहोस्(sendto(종단점, NULL, 0, 0, (struct sockaddr *)&समान_मान, sizeof समान_मान) == 0);
    रुजू_गर्नुहोस्(recvfrom(종단점, NULL, 0, 0, NULL, NULL) == 0);
    रुजू_गर्नुहोस्(recvfrom(종단점, लगत, sizeof लगत, 0, NULL, NULL) == -1 && errno == EAGAIN);
    रुजू_गर्नुहोस्(close(종단점) == 0);
    puts("POSIX UDP CHECK PASS");
    return 0;
}
