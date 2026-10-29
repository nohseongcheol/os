#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

#define manatoko(here) do { if (!(here)) { puts("POSIX UDP CHECK FAILED: " #here); return 1; } } while (0)
int main(int 인수개수, char **tohenga_Rārangi) {
    manatoko(인수개수 == 2);
    int 접속번호 = 0;
    for (int kāniwha_tāurunga = 0; tohenga_Rārangi[1][kāniwha_tāurunga]; kāniwha_tāurunga++) {
        manatoko(tohenga_Rārangi[1][kāniwha_tāurunga] >= '0' && tohenga_Rārangi[1][kāniwha_tāurunga] <= '9');
        접속번호 = 접속번호 * 10 + tohenga_Rārangi[1][kāniwha_tāurunga] - '0';
        manatoko(접속번호 <= 65535);
    }
    int 종단점 = 통신종단점만들기(AF_INET, SOCK_DGRAM, 0);
    manatoko(종단점 == 3);
    struct sockaddr_in paetata_whānuitanga = {0}, hoa_uara = {0}, RECEIVED_ADDRESS = {0};
    paetata_whānuitanga.sin_family = AF_INET;
    socklen_t roa_uara = sizeof paetata_whānuitanga;
    manatoko(통신주소읽기(종단점, (struct sockaddr *)&paetata_whānuitanga, &roa_uara) == 0 && paetata_whānuitanga.sin_port == 0);
    manatoko(BIND_ADDRESS(종단점, (struct sockaddr *)&paetata_whānuitanga, sizeof paetata_whānuitanga) == 0);
    manatoko(통신주소읽기(종단점, (struct sockaddr *)&paetata_whānuitanga, &roa_uara) == 0 && ntohs(paetata_whānuitanga.sin_port) >= 49152);
    manatoko(BIND_ADDRESS(종단점, (struct sockaddr *)&paetata_whānuitanga, sizeof paetata_whānuitanga) == -1 && errno == EINVAL);
    int 둘째 = socket(AF_INET, SOCK_DGRAM, 0);
    manatoko(bind(둘째, (struct sockaddr *)&paetata_whānuitanga, sizeof paetata_whānuitanga) == -1 && errno == EADDRINUSE);
    manatoko(close(둘째) == 0);
    둘째 = dup(종단점);
    manatoko(close(종단점) == 0); 종단점 = 둘째;
    hoa_uara.sin_family = AF_INET; hoa_uara.sin_port = 망차례짧은수(접속번호);
    manatoko(poroporo_whatunga_ADDRESS(AF_INET, "10.0.2.2", &hoa_uara.sin_addr) == 1);
    struct timeval 대기 = {0, 200000};
    manatoko(huri_whatunga_Ngā_Tautuhinga(종단점, SOL_SOCKET, SO_RCVTIMEO, &대기, sizeof 대기) == 0);
    char raraunga[32];
    manatoko(자료전문받기(종단점, raraunga, sizeof raraunga, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    manatoko(자료전문보내기(종단점, "posix-udp", 9, 0, (struct sockaddr *)&hoa_uara, sizeof hoa_uara) == 9);
    roa_uara = sizeof RECEIVED_ADDRESS;
    manatoko(recvfrom(종단점, (void *)0x00100000, 9, 0, NULL, NULL) == -1 && errno == EFAULT);
    manatoko(자료전문받기(종단점, raraunga, sizeof raraunga, 0, (struct sockaddr *)&RECEIVED_ADDRESS, &roa_uara) == 9);
    manatoko(memcmp(raraunga, "posix-udp", 9) == 0 && roa_uara == 16);
    manatoko(RECEIVED_ADDRESS.sin_port == hoa_uara.sin_port && RECEIVED_ADDRESS.sin_addr.s_addr == hoa_uara.sin_addr.s_addr);
    manatoko(sendto(종단점, "truncate", 8, 0, (struct sockaddr *)&hoa_uara, sizeof hoa_uara) == 8);
    manatoko(recvfrom(종단점, raraunga, 3, 0, NULL, NULL) == 3 && memcmp(raraunga, "tru", 3) == 0);
    manatoko(recvfrom(종단점, raraunga, sizeof raraunga, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    manatoko(sendto(종단점, NULL, 0, 0, (struct sockaddr *)&hoa_uara, sizeof hoa_uara) == 0);
    manatoko(recvfrom(종단점, NULL, 0, 0, NULL, NULL) == 0);
    manatoko(recvfrom(종단점, raraunga, sizeof raraunga, 0, NULL, NULL) == -1 && errno == EAGAIN);
    manatoko(close(종단점) == 0);
    puts("POSIX UDP CHECK PASS");
    return 0;
}
