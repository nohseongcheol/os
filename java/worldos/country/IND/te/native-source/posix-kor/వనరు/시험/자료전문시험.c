#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

#define సరిచూడు(నిబంధన) do { if (!(నిబంధన)) { puts("POSIX UDP CHECK FAILED: " #నిబంధన); return 1; } } while (0)
int main(int 인수개수, char **కారకం_జాబితా) {
    సరిచూడు(인수개수 == 2);
    int పోర్ట్_సంఖ్య = 0;
    for (int స్లాట్_ప్రవేశం = 0; కారకం_జాబితా[1][స్లాట్_ప్రవేశం]; స్లాట్_ప్రవేశం++) {
        సరిచూడు(కారకం_జాబితా[1][స్లాట్_ప్రవేశం] >= '0' && కారకం_జాబితా[1][స్లాట్_ప్రవేశం] <= '9');
        పోర్ట్_సంఖ్య = పోర్ట్_సంఖ్య * 10 + కారకం_జాబితా[1][స్లాట్_ప్రవేశం] - '0';
        సరిచూడు(పోర్ట్_సంఖ్య <= 65535);
    }
    int 종단점 = 통신종단점만들기(AF_INET, SOCK_DGRAM, 0);
    సరిచూడు(종단점 == 3);
    struct sockaddr_in స్థానిక_పరిధి = {0}, పియర్_మూల్యం = {0}, 받은주소 = {0};
    స్థానిక_పరిధి.sin_family = AF_INET;
    socklen_t పొడవు_మూల్యం = sizeof స్థానిక_పరిధి;
    సరిచూడు(통신주소읽기(종단점, (struct sockaddr *)&స్థానిక_పరిధి, &పొడవు_మూల్యం) == 0 && స్థానిక_పరిధి.sin_port == 0);
    సరిచూడు(బైండ్_చేయి_ఇమెయిల్(종단점, (struct sockaddr *)&స్థానిక_పరిధి, sizeof స్థానిక_పరిధి) == 0);
    సరిచూడు(통신주소읽기(종단점, (struct sockaddr *)&స్థానిక_పరిధి, &పొడవు_మూల్యం) == 0 && ntohs(స్థానిక_పరిధి.sin_port) >= 49152);
    సరిచూడు(బైండ్_చేయి_ఇమెయిల్(종단점, (struct sockaddr *)&స్థానిక_పరిధి, sizeof స్థానిక_పరిధి) == -1 && errno == EINVAL);
    int 둘째 = socket(AF_INET, SOCK_DGRAM, 0);
    సరిచూడు(bind(둘째, (struct sockaddr *)&స్థానిక_పరిధి, sizeof స్థానిక_పరిధి) == -1 && errno == EADDRINUSE);
    సరిచూడు(close(둘째) == 0);
    둘째 = dup(종단점);
    సరిచూడు(close(종단점) == 0); 종단점 = 둘째;
    పియర్_మూల్యం.sin_family = AF_INET; పియర్_మూల్యం.sin_port = 망차례짧은수(పోర్ట్_సంఖ్య);
    సరిచూడు(పార్స్_నెట్_వర్క్_ఇమెయిల్(AF_INET, "10.0.2.2", &పియర్_మూల్యం.sin_addr) == 1);
    struct timeval వేచియుండు_మూల్యం = {0, 200000};
    సరిచూడు(మార్చు_నెట్_వర్క్_సెట్టింగ్_లు(종단점, SOL_SOCKET, SO_RCVTIMEO, &వేచియుండు_మూల్యం, sizeof వేచియుండు_మూల్యం) == 0);
    char డేటా[32];
    సరిచూడు(자료전문받기(종단점, డేటా, sizeof డేటా, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    సరిచూడు(자료전문보내기(종단점, "posix-udp", 9, 0, (struct sockaddr *)&పియర్_మూల్యం, sizeof పియర్_మూల్యం) == 9);
    పొడవు_మూల్యం = sizeof 받은주소;
    సరిచూడు(recvfrom(종단점, (void *)0x00100000, 9, 0, NULL, NULL) == -1 && errno == EFAULT);
    సరిచూడు(자료전문받기(종단점, డేటా, sizeof డేటా, 0, (struct sockaddr *)&받은주소, &పొడవు_మూల్యం) == 9);
    సరిచూడు(memcmp(డేటా, "posix-udp", 9) == 0 && పొడవు_మూల్యం == 16);
    సరిచూడు(받은주소.sin_port == పియర్_మూల్యం.sin_port && 받은주소.sin_addr.s_addr == పియర్_మూల్యం.sin_addr.s_addr);
    సరిచూడు(sendto(종단점, "truncate", 8, 0, (struct sockaddr *)&పియర్_మూల్యం, sizeof పియర్_మూల్యం) == 8);
    సరిచూడు(recvfrom(종단점, డేటా, 3, 0, NULL, NULL) == 3 && memcmp(డేటా, "tru", 3) == 0);
    సరిచూడు(recvfrom(종단점, డేటా, sizeof డేటా, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    సరిచూడు(sendto(종단점, NULL, 0, 0, (struct sockaddr *)&పియర్_మూల్యం, sizeof పియర్_మూల్యం) == 0);
    సరిచూడు(recvfrom(종단점, NULL, 0, 0, NULL, NULL) == 0);
    సరిచూడు(recvfrom(종단점, డేటా, sizeof డేటా, 0, NULL, NULL) == -1 && errno == EAGAIN);
    సరిచూడు(close(종단점) == 0);
    puts("POSIX UDP CHECK PASS");
    return 0;
}
