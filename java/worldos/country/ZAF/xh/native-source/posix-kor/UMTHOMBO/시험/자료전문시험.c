#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

#define ngqinisisa(imo) do { if (!(imo)) { puts("POSIX UDP CHECK FAILED: " #imo); return 1; } } while (0)
int main(int 인수개수, char **isiniki_myalelo_uludwe) {
    ngqinisisa(인수개수 == 2);
    int 접속번호 = 0;
    for (int isithuba_ufako_nkcukacha = 0; isiniki_myalelo_uludwe[1][isithuba_ufako_nkcukacha]; isithuba_ufako_nkcukacha++) {
        ngqinisisa(isiniki_myalelo_uludwe[1][isithuba_ufako_nkcukacha] >= '0' && isiniki_myalelo_uludwe[1][isithuba_ufako_nkcukacha] <= '9');
        접속번호 = 접속번호 * 10 + isiniki_myalelo_uludwe[1][isithuba_ufako_nkcukacha] - '0';
        ngqinisisa(접속번호 <= 65535);
    }
    int 종단점 = 통신종단점만들기(AF_INET, SOCK_DGRAM, 0);
    ngqinisisa(종단점 == 3);
    struct sockaddr_in eyale_ndawo_umda = {0}, untanga_ixabiso = {0}, 받은주소 = {0};
    eyale_ndawo_umda.sin_family = AF_INET;
    socklen_t ubude_ixabiso = sizeof eyale_ndawo_umda;
    ngqinisisa(통신주소읽기(종단점, (struct sockaddr *)&eyale_ndawo_umda, &ubude_ixabiso) == 0 && eyale_ndawo_umda.sin_port == 0);
    ngqinisisa(BOPHELELA_idilesi(종단점, (struct sockaddr *)&eyale_ndawo_umda, sizeof eyale_ndawo_umda) == 0);
    ngqinisisa(통신주소읽기(종단점, (struct sockaddr *)&eyale_ndawo_umda, &ubude_ixabiso) == 0 && ntohs(eyale_ndawo_umda.sin_port) >= 49152);
    ngqinisisa(BOPHELELA_idilesi(종단점, (struct sockaddr *)&eyale_ndawo_umda, sizeof eyale_ndawo_umda) == -1 && errno == EINVAL);
    int 둘째 = socket(AF_INET, SOCK_DGRAM, 0);
    ngqinisisa(bind(둘째, (struct sockaddr *)&eyale_ndawo_umda, sizeof eyale_ndawo_umda) == -1 && errno == EADDRINUSE);
    ngqinisisa(close(둘째) == 0);
    둘째 = dup(종단점);
    ngqinisisa(close(종단점) == 0); 종단점 = 둘째;
    untanga_ixabiso.sin_family = AF_INET; untanga_ixabiso.sin_port = 망차례짧은수(접속번호);
    ngqinisisa(ingcaciso_yegama_Inethiwekhi_idilesi(AF_INET, "10.0.2.2", &untanga_ixabiso.sin_addr) == 1);
    struct timeval 대기 = {0, 200000};
    ngqinisisa(tshintsha_Inethiwekhi_Iisetingi(종단점, SOL_SOCKET, SO_RCVTIMEO, &대기, sizeof 대기) == 0);
    char iingcombolo[32];
    ngqinisisa(자료전문받기(종단점, iingcombolo, sizeof iingcombolo, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    ngqinisisa(자료전문보내기(종단점, "posix-udp", 9, 0, (struct sockaddr *)&untanga_ixabiso, sizeof untanga_ixabiso) == 9);
    ubude_ixabiso = sizeof 받은주소;
    ngqinisisa(recvfrom(종단점, (void *)0x00100000, 9, 0, NULL, NULL) == -1 && errno == EFAULT);
    ngqinisisa(자료전문받기(종단점, iingcombolo, sizeof iingcombolo, 0, (struct sockaddr *)&받은주소, &ubude_ixabiso) == 9);
    ngqinisisa(memcmp(iingcombolo, "posix-udp", 9) == 0 && ubude_ixabiso == 16);
    ngqinisisa(받은주소.sin_port == untanga_ixabiso.sin_port && 받은주소.sin_addr.s_addr == untanga_ixabiso.sin_addr.s_addr);
    ngqinisisa(sendto(종단점, "truncate", 8, 0, (struct sockaddr *)&untanga_ixabiso, sizeof untanga_ixabiso) == 8);
    ngqinisisa(recvfrom(종단점, iingcombolo, 3, 0, NULL, NULL) == 3 && memcmp(iingcombolo, "tru", 3) == 0);
    ngqinisisa(recvfrom(종단점, iingcombolo, sizeof iingcombolo, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    ngqinisisa(sendto(종단점, NULL, 0, 0, (struct sockaddr *)&untanga_ixabiso, sizeof untanga_ixabiso) == 0);
    ngqinisisa(recvfrom(종단점, NULL, 0, 0, NULL, NULL) == 0);
    ngqinisisa(recvfrom(종단점, iingcombolo, sizeof iingcombolo, 0, NULL, NULL) == -1 && errno == EAGAIN);
    ngqinisisa(close(종단점) == 0);
    puts("POSIX UDP CHECK PASS");
    return 0;
}
