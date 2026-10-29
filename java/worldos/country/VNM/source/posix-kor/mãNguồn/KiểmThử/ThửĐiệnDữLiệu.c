#include <ABITệp.h>
#include <ABIMạng.h>
#include <string.h>
#include <stdio.h>

#define xácMinh(điềuKiện) do { if (!(điềuKiện)) { puts("POSIX UDP CHECK FAILED: " #điềuKiện); return 1; } } while (0)
int main(int sốLượngCácĐốiSố, char **danhSáchĐốiSố) {
    xácMinh(sốLượngCácĐốiSố == 2);
    int sốCổng = 0;
    for (int mụcÔ = 0; danhSáchĐốiSố[1][mụcÔ]; mụcÔ++) {
        xácMinh(danhSáchĐốiSố[1][mụcÔ] >= '0' && danhSáchĐốiSố[1][mụcÔ] <= '9');
        sốCổng = sốCổng * 10 + danhSáchĐốiSố[1][mụcÔ] - '0';
        xácMinh(sốCổng <= 65535);
    }
    int giáTrịĐiểmCuối = tạoĐiểmCuối(AF_INET, SOCK_DGRAM, 0);
    xácMinh(giáTrịĐiểmCuối == 3);
    struct sockaddr_in phạmViCụcBộ = {0}, giáTrịĐốiTác = {0}, địaChỉĐãNhận = {0};
    phạmViCụcBộ.sin_family = AF_INET;
    socklen_t độDài = sizeof phạmViCụcBộ;
    xácMinh(đọcĐịaChỉỔCắmMạng(giáTrịĐiểmCuối, (struct sockaddr *)&phạmViCụcBộ, &độDài) == 0 && phạmViCụcBộ.sin_port == 0);
    xácMinh(ràngBuộcĐịaChỉ(giáTrịĐiểmCuối, (struct sockaddr *)&phạmViCụcBộ, sizeof phạmViCụcBộ) == 0);
    xácMinh(đọcĐịaChỉỔCắmMạng(giáTrịĐiểmCuối, (struct sockaddr *)&phạmViCụcBộ, &độDài) == 0 && ntohs(phạmViCụcBộ.sin_port) >= 49152);
    xácMinh(ràngBuộcĐịaChỉ(giáTrịĐiểmCuối, (struct sockaddr *)&phạmViCụcBộ, sizeof phạmViCụcBộ) == -1 && errno == EINVAL);
    int thứBậcThứHai = socket(AF_INET, SOCK_DGRAM, 0);
    xácMinh(bind(thứBậcThứHai, (struct sockaddr *)&phạmViCụcBộ, sizeof phạmViCụcBộ) == -1 && errno == EADDRINUSE);
    xácMinh(close(thứBậcThứHai) == 0);
    thứBậcThứHai = dup(giáTrịĐiểmCuối);
    xácMinh(close(giáTrịĐiểmCuối) == 0); giáTrịĐiểmCuối = thứBậcThứHai;
    giáTrịĐốiTác.sin_family = AF_INET; giáTrịĐốiTác.sin_port = ngắnKiểuMạng(sốCổng);
    xácMinh(phânTíchCúPhápĐịaChỉMạng(AF_INET, "10.0.2.2", &giáTrịĐốiTác.sin_addr) == 1);
    struct timeval chờGiáTrị = {0, 200000};
    xácMinh(đổiCácThiếtLậpMạng(giáTrịĐiểmCuối, SOL_SOCKET, SO_RCVTIMEO, &chờGiáTrị, sizeof chờGiáTrị) == 0);
    char DữLiệu[32];
    xácMinh(nhậnDữLiệuĐiệnDữLiệu(giáTrịĐiểmCuối, DữLiệu, sizeof DữLiệu, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    xácMinh(gửiDữLiệuĐiệnDữLiệu(giáTrịĐiểmCuối, "posix-udp", 9, 0, (struct sockaddr *)&giáTrịĐốiTác, sizeof giáTrịĐốiTác) == 9);
    độDài = sizeof địaChỉĐãNhận;
    xácMinh(recvfrom(giáTrịĐiểmCuối, (void *)0x00100000, 9, 0, NULL, NULL) == -1 && errno == EFAULT);
    xácMinh(nhậnDữLiệuĐiệnDữLiệu(giáTrịĐiểmCuối, DữLiệu, sizeof DữLiệu, 0, (struct sockaddr *)&địaChỉĐãNhận, &độDài) == 9);
    xácMinh(memcmp(DữLiệu, "posix-udp", 9) == 0 && độDài == 16);
    xácMinh(địaChỉĐãNhận.sin_port == giáTrịĐốiTác.sin_port && địaChỉĐãNhận.sin_addr.s_addr == giáTrịĐốiTác.sin_addr.s_addr);
    xácMinh(sendto(giáTrịĐiểmCuối, "truncate", 8, 0, (struct sockaddr *)&giáTrịĐốiTác, sizeof giáTrịĐốiTác) == 8);
    xácMinh(recvfrom(giáTrịĐiểmCuối, DữLiệu, 3, 0, NULL, NULL) == 3 && memcmp(DữLiệu, "tru", 3) == 0);
    xácMinh(recvfrom(giáTrịĐiểmCuối, DữLiệu, sizeof DữLiệu, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    xácMinh(sendto(giáTrịĐiểmCuối, NULL, 0, 0, (struct sockaddr *)&giáTrịĐốiTác, sizeof giáTrịĐốiTác) == 0);
    xácMinh(recvfrom(giáTrịĐiểmCuối, NULL, 0, 0, NULL, NULL) == 0);
    xácMinh(recvfrom(giáTrịĐiểmCuối, DữLiệu, sizeof DữLiệu, 0, NULL, NULL) == -1 && errno == EAGAIN);
    xácMinh(close(giáTrịĐiểmCuối) == 0);
    puts("POSIX UDP CHECK PASS");
    return 0;
}
