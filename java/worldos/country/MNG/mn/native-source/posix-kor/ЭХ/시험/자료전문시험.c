#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

#define шалгах(нөхцөл) do { if (!(нөхцөл)) { puts("POSIX UDP CHECK FAILED: " #нөхцөл); return 1; } } while (0)
int main(int 인수개수, char **аргумент_Жагсаалт) {
    шалгах(인수개수 == 2);
    int 접속번호 = 0;
    for (int зай_оролт = 0; аргумент_Жагсаалт[1][зай_оролт]; зай_оролт++) {
        шалгах(аргумент_Жагсаалт[1][зай_оролт] >= '0' && аргумент_Жагсаалт[1][зай_оролт] <= '9');
        접속번호 = 접속번호 * 10 + аргумент_Жагсаалт[1][зай_оролт] - '0';
        шалгах(접속번호 <= 65535);
    }
    int 종단점 = 통신종단점만들기(AF_INET, SOCK_DGRAM, 0);
    шалгах(종단점 == 3);
    struct sockaddr_in локал_хамрах_хүрээ = {0}, ижил_түвшин_утга = {0}, 받은주소 = {0};
    локал_хамрах_хүрээ.sin_family = AF_INET;
    socklen_t урт_утга = sizeof локал_хамрах_хүрээ;
    шалгах(통신주소읽기(종단점, (struct sockaddr *)&локал_хамрах_хүрээ, &урт_утга) == 0 && локал_хамрах_хүрээ.sin_port == 0);
    шалгах(холбох_хаяг(종단점, (struct sockaddr *)&локал_хамрах_хүрээ, sizeof локал_хамрах_хүрээ) == 0);
    шалгах(통신주소읽기(종단점, (struct sockaddr *)&локал_хамрах_хүрээ, &урт_утга) == 0 && ntohs(локал_хамрах_хүрээ.sin_port) >= 49152);
    шалгах(холбох_хаяг(종단점, (struct sockaddr *)&локал_хамрах_хүрээ, sizeof локал_хамрах_хүрээ) == -1 && errno == EINVAL);
    int 둘째 = socket(AF_INET, SOCK_DGRAM, 0);
    шалгах(bind(둘째, (struct sockaddr *)&локал_хамрах_хүрээ, sizeof локал_хамрах_хүрээ) == -1 && errno == EADDRINUSE);
    шалгах(close(둘째) == 0);
    둘째 = dup(종단점);
    шалгах(close(종단점) == 0); 종단점 = 둘째;
    ижил_түвшин_утга.sin_family = AF_INET; ижил_түвшин_утга.sin_port = 망차례짧은수(접속번호);
    шалгах(задлан_ялгал_хийх_Сүлжээ_хаяг(AF_INET, "10.0.2.2", &ижил_түвшин_утга.sin_addr) == 1);
    struct timeval 대기 = {0, 200000};
    шалгах(өөрчлөх_Сүлжээ_Тохиргоо(종단점, SOL_SOCKET, SO_RCVTIMEO, &대기, sizeof 대기) == 0);
    char өгөгдөл[32];
    шалгах(자료전문받기(종단점, өгөгдөл, sizeof өгөгдөл, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    шалгах(자료전문보내기(종단점, "posix-udp", 9, 0, (struct sockaddr *)&ижил_түвшин_утга, sizeof ижил_түвшин_утга) == 9);
    урт_утга = sizeof 받은주소;
    шалгах(recvfrom(종단점, (void *)0x00100000, 9, 0, NULL, NULL) == -1 && errno == EFAULT);
    шалгах(자료전문받기(종단점, өгөгдөл, sizeof өгөгдөл, 0, (struct sockaddr *)&받은주소, &урт_утга) == 9);
    шалгах(memcmp(өгөгдөл, "posix-udp", 9) == 0 && урт_утга == 16);
    шалгах(받은주소.sin_port == ижил_түвшин_утга.sin_port && 받은주소.sin_addr.s_addr == ижил_түвшин_утга.sin_addr.s_addr);
    шалгах(sendto(종단점, "truncate", 8, 0, (struct sockaddr *)&ижил_түвшин_утга, sizeof ижил_түвшин_утга) == 8);
    шалгах(recvfrom(종단점, өгөгдөл, 3, 0, NULL, NULL) == 3 && memcmp(өгөгдөл, "tru", 3) == 0);
    шалгах(recvfrom(종단점, өгөгдөл, sizeof өгөгдөл, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    шалгах(sendto(종단점, NULL, 0, 0, (struct sockaddr *)&ижил_түвшин_утга, sizeof ижил_түвшин_утга) == 0);
    шалгах(recvfrom(종단점, NULL, 0, 0, NULL, NULL) == 0);
    шалгах(recvfrom(종단점, өгөгдөл, sizeof өгөгдөл, 0, NULL, NULL) == -1 && errno == EAGAIN);
    шалгах(close(종단점) == 0);
    puts("POSIX UDP CHECK PASS");
    return 0;
}
