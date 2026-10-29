#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

#define verifizéieren(Bedéngung) do { if (!(Bedéngung)) { puts("POSIX UDP CHECK FAILED: " #Bedéngung); return 1; } } while (0)
int main(int 인수개수, char **Argument_Lëscht) {
    verifizéieren(인수개수 == 2);
    int 접속번호 = 0;
    for (int Slot_Agab = 0; Argument_Lëscht[1][Slot_Agab]; Slot_Agab++) {
        verifizéieren(Argument_Lëscht[1][Slot_Agab] >= '0' && Argument_Lëscht[1][Slot_Agab] <= '9');
        접속번호 = 접속번호 * 10 + Argument_Lëscht[1][Slot_Agab] - '0';
        verifizéieren(접속번호 <= 65535);
    }
    int 종단점 = 통신종단점만들기(AF_INET, SOCK_DGRAM, 0);
    verifizéieren(종단점 == 3);
    struct sockaddr_in lokal_Beräich = {0}, Peer_VALUE = {0}, RECEIVED_Adress = {0};
    lokal_Beräich.sin_family = AF_INET;
    socklen_t Längt_VALUE = sizeof lokal_Beräich;
    verifizéieren(통신주소읽기(종단점, (struct sockaddr *)&lokal_Beräich, &Längt_VALUE) == 0 && lokal_Beräich.sin_port == 0);
    verifizéieren(BANNEN_Adress(종단점, (struct sockaddr *)&lokal_Beräich, sizeof lokal_Beräich) == 0);
    verifizéieren(통신주소읽기(종단점, (struct sockaddr *)&lokal_Beräich, &Längt_VALUE) == 0 && ntohs(lokal_Beräich.sin_port) >= 49152);
    verifizéieren(BANNEN_Adress(종단점, (struct sockaddr *)&lokal_Beräich, sizeof lokal_Beräich) == -1 && errno == EINVAL);
    int 둘째 = socket(AF_INET, SOCK_DGRAM, 0);
    verifizéieren(bind(둘째, (struct sockaddr *)&lokal_Beräich, sizeof lokal_Beräich) == -1 && errno == EADDRINUSE);
    verifizéieren(close(둘째) == 0);
    둘째 = dup(종단점);
    verifizéieren(close(종단점) == 0); 종단점 = 둘째;
    Peer_VALUE.sin_family = AF_INET; Peer_VALUE.sin_port = 망차례짧은수(접속번호);
    verifizéieren(analyséieren_Reseau_Adress(AF_INET, "10.0.2.2", &Peer_VALUE.sin_addr) == 1);
    struct timeval Waart_VALUE = {0, 200000};
    verifizéieren(änneren_Reseau_Astellungen(종단점, SOL_SOCKET, SO_RCVTIMEO, &Waart_VALUE, sizeof Waart_VALUE) == 0);
    char Daten[32];
    verifizéieren(자료전문받기(종단점, Daten, sizeof Daten, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    verifizéieren(자료전문보내기(종단점, "posix-udp", 9, 0, (struct sockaddr *)&Peer_VALUE, sizeof Peer_VALUE) == 9);
    Längt_VALUE = sizeof RECEIVED_Adress;
    verifizéieren(recvfrom(종단점, (void *)0x00100000, 9, 0, NULL, NULL) == -1 && errno == EFAULT);
    verifizéieren(자료전문받기(종단점, Daten, sizeof Daten, 0, (struct sockaddr *)&RECEIVED_Adress, &Längt_VALUE) == 9);
    verifizéieren(memcmp(Daten, "posix-udp", 9) == 0 && Längt_VALUE == 16);
    verifizéieren(RECEIVED_Adress.sin_port == Peer_VALUE.sin_port && RECEIVED_Adress.sin_addr.s_addr == Peer_VALUE.sin_addr.s_addr);
    verifizéieren(sendto(종단점, "truncate", 8, 0, (struct sockaddr *)&Peer_VALUE, sizeof Peer_VALUE) == 8);
    verifizéieren(recvfrom(종단점, Daten, 3, 0, NULL, NULL) == 3 && memcmp(Daten, "tru", 3) == 0);
    verifizéieren(recvfrom(종단점, Daten, sizeof Daten, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    verifizéieren(sendto(종단점, NULL, 0, 0, (struct sockaddr *)&Peer_VALUE, sizeof Peer_VALUE) == 0);
    verifizéieren(recvfrom(종단점, NULL, 0, 0, NULL, NULL) == 0);
    verifizéieren(recvfrom(종단점, Daten, sizeof Daten, 0, NULL, NULL) == -1 && errno == EAGAIN);
    verifizéieren(close(종단점) == 0);
    puts("POSIX UDP CHECK PASS");
    return 0;
}
