#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

#define ਤਸਦੀਕ(ਸ਼ਰਤ) do { if (!(ਸ਼ਰਤ)) { puts("POSIX UDP CHECK FAILED: " #ਸ਼ਰਤ); return 1; } } while (0)
int main(int 인수개수, char **ਦਲੀਲ_ਸੂਚੀ) {
    ਤਸਦੀਕ(인수개수 == 2);
    int 접속번호 = 0;
    for (int ਸਲੌਟ_ਦਾਖਲਾ = 0; ਦਲੀਲ_ਸੂਚੀ[1][ਸਲੌਟ_ਦਾਖਲਾ]; ਸਲੌਟ_ਦਾਖਲਾ++) {
        ਤਸਦੀਕ(ਦਲੀਲ_ਸੂਚੀ[1][ਸਲੌਟ_ਦਾਖਲਾ] >= '0' && ਦਲੀਲ_ਸੂਚੀ[1][ਸਲੌਟ_ਦਾਖਲਾ] <= '9');
        접속번호 = 접속번호 * 10 + ਦਲੀਲ_ਸੂਚੀ[1][ਸਲੌਟ_ਦਾਖਲਾ] - '0';
        ਤਸਦੀਕ(접속번호 <= 65535);
    }
    int 종단점 = 통신종단점만들기(AF_INET, SOCK_DGRAM, 0);
    ਤਸਦੀਕ(종단점 == 3);
    struct sockaddr_in ਲੋਕਲ_ਗੁੰਜਾਇਸ਼ = {0}, ਪਿਅਰ_ਕੀਮਤ = {0}, 받은주소 = {0};
    ਲੋਕਲ_ਗੁੰਜਾਇਸ਼.sin_family = AF_INET;
    socklen_t ਲੰਬਾਈ_ਕੀਮਤ = sizeof ਲੋਕਲ_ਗੁੰਜਾਇਸ਼;
    ਤਸਦੀਕ(통신주소읽기(종단점, (struct sockaddr *)&ਲੋਕਲ_ਗੁੰਜਾਇਸ਼, &ਲੰਬਾਈ_ਕੀਮਤ) == 0 && ਲੋਕਲ_ਗੁੰਜਾਇਸ਼.sin_port == 0);
    ਤਸਦੀਕ(ਜ਼ਿਲਦਬੰਦੀ_ਪਤਾ(종단점, (struct sockaddr *)&ਲੋਕਲ_ਗੁੰਜਾਇਸ਼, sizeof ਲੋਕਲ_ਗੁੰਜਾਇਸ਼) == 0);
    ਤਸਦੀਕ(통신주소읽기(종단점, (struct sockaddr *)&ਲੋਕਲ_ਗੁੰਜਾਇਸ਼, &ਲੰਬਾਈ_ਕੀਮਤ) == 0 && ntohs(ਲੋਕਲ_ਗੁੰਜਾਇਸ਼.sin_port) >= 49152);
    ਤਸਦੀਕ(ਜ਼ਿਲਦਬੰਦੀ_ਪਤਾ(종단점, (struct sockaddr *)&ਲੋਕਲ_ਗੁੰਜਾਇਸ਼, sizeof ਲੋਕਲ_ਗੁੰਜਾਇਸ਼) == -1 && errno == EINVAL);
    int 둘째 = socket(AF_INET, SOCK_DGRAM, 0);
    ਤਸਦੀਕ(bind(둘째, (struct sockaddr *)&ਲੋਕਲ_ਗੁੰਜਾਇਸ਼, sizeof ਲੋਕਲ_ਗੁੰਜਾਇਸ਼) == -1 && errno == EADDRINUSE);
    ਤਸਦੀਕ(close(둘째) == 0);
    둘째 = dup(종단점);
    ਤਸਦੀਕ(close(종단점) == 0); 종단점 = 둘째;
    ਪਿਅਰ_ਕੀਮਤ.sin_family = AF_INET; ਪਿਅਰ_ਕੀਮਤ.sin_port = 망차례짧은수(접속번호);
    ਤਸਦੀਕ(ਪਦ_ਵਿਆਖਿਆ_ਕਰੋ_ਨੈਟਵਰਕ_ਪਤਾ(AF_INET, "10.0.2.2", &ਪਿਅਰ_ਕੀਮਤ.sin_addr) == 1);
    struct timeval 대기 = {0, 200000};
    ਤਸਦੀਕ(ਬਦਲੋ_ਨੈਟਵਰਕ_ਸੈਟਿੰਗਾਂ(종단점, SOL_SOCKET, SO_RCVTIMEO, &대기, sizeof 대기) == 0);
    char ਸਮੱਗਰੀ[32];
    ਤਸਦੀਕ(자료전문받기(종단점, ਸਮੱਗਰੀ, sizeof ਸਮੱਗਰੀ, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    ਤਸਦੀਕ(자료전문보내기(종단점, "posix-udp", 9, 0, (struct sockaddr *)&ਪਿਅਰ_ਕੀਮਤ, sizeof ਪਿਅਰ_ਕੀਮਤ) == 9);
    ਲੰਬਾਈ_ਕੀਮਤ = sizeof 받은주소;
    ਤਸਦੀਕ(recvfrom(종단점, (void *)0x00100000, 9, 0, NULL, NULL) == -1 && errno == EFAULT);
    ਤਸਦੀਕ(자료전문받기(종단점, ਸਮੱਗਰੀ, sizeof ਸਮੱਗਰੀ, 0, (struct sockaddr *)&받은주소, &ਲੰਬਾਈ_ਕੀਮਤ) == 9);
    ਤਸਦੀਕ(memcmp(ਸਮੱਗਰੀ, "posix-udp", 9) == 0 && ਲੰਬਾਈ_ਕੀਮਤ == 16);
    ਤਸਦੀਕ(받은주소.sin_port == ਪਿਅਰ_ਕੀਮਤ.sin_port && 받은주소.sin_addr.s_addr == ਪਿਅਰ_ਕੀਮਤ.sin_addr.s_addr);
    ਤਸਦੀਕ(sendto(종단점, "truncate", 8, 0, (struct sockaddr *)&ਪਿਅਰ_ਕੀਮਤ, sizeof ਪਿਅਰ_ਕੀਮਤ) == 8);
    ਤਸਦੀਕ(recvfrom(종단점, ਸਮੱਗਰੀ, 3, 0, NULL, NULL) == 3 && memcmp(ਸਮੱਗਰੀ, "tru", 3) == 0);
    ਤਸਦੀਕ(recvfrom(종단점, ਸਮੱਗਰੀ, sizeof ਸਮੱਗਰੀ, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    ਤਸਦੀਕ(sendto(종단점, NULL, 0, 0, (struct sockaddr *)&ਪਿਅਰ_ਕੀਮਤ, sizeof ਪਿਅਰ_ਕੀਮਤ) == 0);
    ਤਸਦੀਕ(recvfrom(종단점, NULL, 0, 0, NULL, NULL) == 0);
    ਤਸਦੀਕ(recvfrom(종단점, ਸਮੱਗਰੀ, sizeof ਸਮੱਗਰੀ, 0, NULL, NULL) == -1 && errno == EAGAIN);
    ਤਸਦੀਕ(close(종단점) == 0);
    puts("POSIX UDP CHECK PASS");
    return 0;
}
