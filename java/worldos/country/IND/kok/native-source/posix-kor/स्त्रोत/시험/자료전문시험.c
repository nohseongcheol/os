#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

#define पुनर्तपासणी_करची(स्थिती_291ac971) do { if (!(स्थिती_291ac971)) { puts("POSIX UDP CHECK FAILED: " #स्थिती_291ac971); return 1; } } while (0)
int main(int 인수개수, char **युक्तीवाद_सुची) {
    पुनर्तपासणी_करची(인수개수 == 2);
    int 접속번호 = 0;
    for (int स्लॉट_प्रवेश = 0; युक्तीवाद_सुची[1][स्लॉट_प्रवेश]; स्लॉट_प्रवेश++) {
        पुनर्तपासणी_करची(युक्तीवाद_सुची[1][स्लॉट_प्रवेश] >= '0' && युक्तीवाद_सुची[1][स्लॉट_प्रवेश] <= '9');
        접속번호 = 접속번호 * 10 + युक्तीवाद_सुची[1][स्लॉट_प्रवेश] - '0';
        पुनर्तपासणी_करची(접속번호 <= 65535);
    }
    int 종단점 = 통신종단점만들기(AF_INET, SOCK_DGRAM, 0);
    पुनर्तपासणी_करची(종단점 == 3);
    struct sockaddr_in थळावो_मळ = {0}, पीयर_मोल = {0}, RECEIVED_नामो = {0};
    थळावो_मळ.sin_family = AF_INET;
    socklen_t लांबाय_मोल = sizeof थळावो_मळ;
    पुनर्तपासणी_करची(통신주소읽기(종단점, (struct sockaddr *)&थळावो_मळ, &लांबाय_मोल) == 0 && थळावो_मळ.sin_port == 0);
    पुनर्तपासणी_करची(BIND_नामो(종단점, (struct sockaddr *)&थळावो_मळ, sizeof थळावो_मळ) == 0);
    पुनर्तपासणी_करची(통신주소읽기(종단점, (struct sockaddr *)&थळावो_मळ, &लांबाय_मोल) == 0 && ntohs(थळावो_मळ.sin_port) >= 49152);
    पुनर्तपासणी_करची(BIND_नामो(종단점, (struct sockaddr *)&थळावो_मळ, sizeof थळावो_मळ) == -1 && errno == EINVAL);
    int 둘째 = socket(AF_INET, SOCK_DGRAM, 0);
    पुनर्तपासणी_करची(bind(둘째, (struct sockaddr *)&थळावो_मळ, sizeof थळावो_मळ) == -1 && errno == EADDRINUSE);
    पुनर्तपासणी_करची(close(둘째) == 0);
    둘째 = dup(종단점);
    पुनर्तपासणी_करची(close(종단점) == 0); 종단점 = 둘째;
    पीयर_मोल.sin_family = AF_INET; पीयर_मोल.sin_port = 망차례짧은수(접속번호);
    पुनर्तपासणी_करची(व्याकरणी_फोडणिशी_नॅटवर्क_नामो(AF_INET, "10.0.2.2", &पीयर_मोल.sin_addr) == 1);
    struct timeval 대기 = {0, 200000};
    पुनर्तपासणी_करची(बदलचें_नॅटवर्क_मांडावळी(종단점, SOL_SOCKET, SO_RCVTIMEO, &대기, sizeof 대기) == 0);
    char डेटा[32];
    पुनर्तपासणी_करची(자료전문받기(종단점, डेटा, sizeof डेटा, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    पुनर्तपासणी_करची(자료전문보내기(종단점, "posix-udp", 9, 0, (struct sockaddr *)&पीयर_मोल, sizeof पीयर_मोल) == 9);
    लांबाय_मोल = sizeof RECEIVED_नामो;
    पुनर्तपासणी_करची(recvfrom(종단점, (void *)0x00100000, 9, 0, NULL, NULL) == -1 && errno == EFAULT);
    पुनर्तपासणी_करची(자료전문받기(종단점, डेटा, sizeof डेटा, 0, (struct sockaddr *)&RECEIVED_नामो, &लांबाय_मोल) == 9);
    पुनर्तपासणी_करची(memcmp(डेटा, "posix-udp", 9) == 0 && लांबाय_मोल == 16);
    पुनर्तपासणी_करची(RECEIVED_नामो.sin_port == पीयर_मोल.sin_port && RECEIVED_नामो.sin_addr.s_addr == पीयर_मोल.sin_addr.s_addr);
    पुनर्तपासणी_करची(sendto(종단점, "truncate", 8, 0, (struct sockaddr *)&पीयर_मोल, sizeof पीयर_मोल) == 8);
    पुनर्तपासणी_करची(recvfrom(종단점, डेटा, 3, 0, NULL, NULL) == 3 && memcmp(डेटा, "tru", 3) == 0);
    पुनर्तपासणी_करची(recvfrom(종단점, डेटा, sizeof डेटा, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    पुनर्तपासणी_करची(sendto(종단점, NULL, 0, 0, (struct sockaddr *)&पीयर_मोल, sizeof पीयर_मोल) == 0);
    पुनर्तपासणी_करची(recvfrom(종단점, NULL, 0, 0, NULL, NULL) == 0);
    पुनर्तपासणी_करची(recvfrom(종단점, डेटा, sizeof डेटा, 0, NULL, NULL) == -1 && errno == EAGAIN);
    पुनर्तपासणी_करची(close(종단점) == 0);
    puts("POSIX UDP CHECK PASS");
    return 0;
}
