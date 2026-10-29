#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

#define periksa(kondisi) do { if (!(kondisi)) { puts("POSIX UDP CHECK FAILED: " #kondisi); return 1; } } while (0)
int main(int 인수개수, char **argumen_Daftar) {
    periksa(인수개수 == 2);
    int nomor_port = 0;
    for (int slot_entri = 0; argumen_Daftar[1][slot_entri]; slot_entri++) {
        periksa(argumen_Daftar[1][slot_entri] >= '0' && argumen_Daftar[1][slot_entri] <= '9');
        nomor_port = nomor_port * 10 + argumen_Daftar[1][slot_entri] - '0';
        periksa(nomor_port <= 65535);
    }
    int peserta_VALUE = Buat_peserta(AF_INET, SOCK_DGRAM, 0);
    periksa(peserta_VALUE == 3);
    struct sockaddr_in lokal_Cakupan = {0}, serekan_VALUE = {0}, RECEIVED_surel = {0};
    lokal_Cakupan.sin_family = AF_INET;
    socklen_t panjang_VALUE = sizeof lokal_Cakupan;
    periksa(통신주소읽기(peserta_VALUE, (struct sockaddr *)&lokal_Cakupan, &panjang_VALUE) == 0 && lokal_Cakupan.sin_port == 0);
    periksa(ikat_surel(peserta_VALUE, (struct sockaddr *)&lokal_Cakupan, sizeof lokal_Cakupan) == 0);
    periksa(통신주소읽기(peserta_VALUE, (struct sockaddr *)&lokal_Cakupan, &panjang_VALUE) == 0 && ntohs(lokal_Cakupan.sin_port) >= 49152);
    periksa(ikat_surel(peserta_VALUE, (struct sockaddr *)&lokal_Cakupan, sizeof lokal_Cakupan) == -1 && errno == EINVAL);
    int 둘째 = socket(AF_INET, SOCK_DGRAM, 0);
    periksa(bind(둘째, (struct sockaddr *)&lokal_Cakupan, sizeof lokal_Cakupan) == -1 && errno == EADDRINUSE);
    periksa(close(둘째) == 0);
    둘째 = dup(peserta_VALUE);
    periksa(close(peserta_VALUE) == 0); peserta_VALUE = 둘째;
    serekan_VALUE.sin_family = AF_INET; serekan_VALUE.sin_port = 망차례짧은수(nomor_port);
    periksa(urai_jaringan_surel(AF_INET, "10.0.2.2", &serekan_VALUE.sin_addr) == 1);
    struct timeval tunggu_VALUE = {0, 200000};
    periksa(ubah_jaringan_Pengaturan(peserta_VALUE, SOL_SOCKET, SO_RCVTIMEO, &tunggu_VALUE, sizeof tunggu_VALUE) == 0);
    char data[32];
    periksa(자료전문받기(peserta_VALUE, data, sizeof data, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    periksa(자료전문보내기(peserta_VALUE, "posix-udp", 9, 0, (struct sockaddr *)&serekan_VALUE, sizeof serekan_VALUE) == 9);
    panjang_VALUE = sizeof RECEIVED_surel;
    periksa(recvfrom(peserta_VALUE, (void *)0x00100000, 9, 0, NULL, NULL) == -1 && errno == EFAULT);
    periksa(자료전문받기(peserta_VALUE, data, sizeof data, 0, (struct sockaddr *)&RECEIVED_surel, &panjang_VALUE) == 9);
    periksa(memcmp(data, "posix-udp", 9) == 0 && panjang_VALUE == 16);
    periksa(RECEIVED_surel.sin_port == serekan_VALUE.sin_port && RECEIVED_surel.sin_addr.s_addr == serekan_VALUE.sin_addr.s_addr);
    periksa(sendto(peserta_VALUE, "truncate", 8, 0, (struct sockaddr *)&serekan_VALUE, sizeof serekan_VALUE) == 8);
    periksa(recvfrom(peserta_VALUE, data, 3, 0, NULL, NULL) == 3 && memcmp(data, "tru", 3) == 0);
    periksa(recvfrom(peserta_VALUE, data, sizeof data, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    periksa(sendto(peserta_VALUE, NULL, 0, 0, (struct sockaddr *)&serekan_VALUE, sizeof serekan_VALUE) == 0);
    periksa(recvfrom(peserta_VALUE, NULL, 0, 0, NULL, NULL) == 0);
    periksa(recvfrom(peserta_VALUE, data, sizeof data, 0, NULL, NULL) == -1 && errno == EAGAIN);
    periksa(close(peserta_VALUE) == 0);
    puts("POSIX UDP CHECK PASS");
    return 0;
}
