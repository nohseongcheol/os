#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

#define tentu_sahkan(syarat) do { if (!(syarat)) { puts("POSIX UDP CHECK FAILED: " #syarat); return 1; } } while (0)
int main(int 인수개수, char **argumen_Senarai) {
    tentu_sahkan(인수개수 == 2);
    int nombor_port = 0;
    for (int 칸 = 0; argumen_Senarai[1][칸]; 칸++) {
        tentu_sahkan(argumen_Senarai[1][칸] >= '0' && argumen_Senarai[1][칸] <= '9');
        nombor_port = nombor_port * 10 + argumen_Senarai[1][칸] - '0';
        tentu_sahkan(nombor_port <= 65535);
    }
    int peserta_VALUE = cipta_peserta(AF_INET, SOCK_DGRAM, 0);
    tentu_sahkan(peserta_VALUE == 3);
    struct sockaddr_in setempat_Skop = {0}, rakan_VALUE = {0}, RECEIVED_e_mel = {0};
    setempat_Skop.sin_family = AF_INET;
    socklen_t kepanjangan_VALUE = sizeof setempat_Skop;
    tentu_sahkan(통신주소읽기(peserta_VALUE, (struct sockaddr *)&setempat_Skop, &kepanjangan_VALUE) == 0 && setempat_Skop.sin_port == 0);
    tentu_sahkan(ikat_e_mel(peserta_VALUE, (struct sockaddr *)&setempat_Skop, sizeof setempat_Skop) == 0);
    tentu_sahkan(통신주소읽기(peserta_VALUE, (struct sockaddr *)&setempat_Skop, &kepanjangan_VALUE) == 0 && ntohs(setempat_Skop.sin_port) >= 49152);
    tentu_sahkan(ikat_e_mel(peserta_VALUE, (struct sockaddr *)&setempat_Skop, sizeof setempat_Skop) == -1 && errno == EINVAL);
    int 둘째 = socket(AF_INET, SOCK_DGRAM, 0);
    tentu_sahkan(bind(둘째, (struct sockaddr *)&setempat_Skop, sizeof setempat_Skop) == -1 && errno == EADDRINUSE);
    tentu_sahkan(close(둘째) == 0);
    둘째 = dup(peserta_VALUE);
    tentu_sahkan(close(peserta_VALUE) == 0); peserta_VALUE = 둘째;
    rakan_VALUE.sin_family = AF_INET; rakan_VALUE.sin_port = 망차례짧은수(nombor_port);
    tentu_sahkan(hurai_rangkaian_e_mel(AF_INET, "10.0.2.2", &rakan_VALUE.sin_addr) == 1);
    struct timeval tunggu_VALUE = {0, 200000};
    tentu_sahkan(ubah_rangkaian_Seting(peserta_VALUE, SOL_SOCKET, SO_RCVTIMEO, &tunggu_VALUE, sizeof tunggu_VALUE) == 0);
    char data[32];
    tentu_sahkan(자료전문받기(peserta_VALUE, data, sizeof data, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    tentu_sahkan(자료전문보내기(peserta_VALUE, "posix-udp", 9, 0, (struct sockaddr *)&rakan_VALUE, sizeof rakan_VALUE) == 9);
    kepanjangan_VALUE = sizeof RECEIVED_e_mel;
    tentu_sahkan(recvfrom(peserta_VALUE, (void *)0x00100000, 9, 0, NULL, NULL) == -1 && errno == EFAULT);
    tentu_sahkan(자료전문받기(peserta_VALUE, data, sizeof data, 0, (struct sockaddr *)&RECEIVED_e_mel, &kepanjangan_VALUE) == 9);
    tentu_sahkan(memcmp(data, "posix-udp", 9) == 0 && kepanjangan_VALUE == 16);
    tentu_sahkan(RECEIVED_e_mel.sin_port == rakan_VALUE.sin_port && RECEIVED_e_mel.sin_addr.s_addr == rakan_VALUE.sin_addr.s_addr);
    tentu_sahkan(sendto(peserta_VALUE, "truncate", 8, 0, (struct sockaddr *)&rakan_VALUE, sizeof rakan_VALUE) == 8);
    tentu_sahkan(recvfrom(peserta_VALUE, data, 3, 0, NULL, NULL) == 3 && memcmp(data, "tru", 3) == 0);
    tentu_sahkan(recvfrom(peserta_VALUE, data, sizeof data, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    tentu_sahkan(sendto(peserta_VALUE, NULL, 0, 0, (struct sockaddr *)&rakan_VALUE, sizeof rakan_VALUE) == 0);
    tentu_sahkan(recvfrom(peserta_VALUE, NULL, 0, 0, NULL, NULL) == 0);
    tentu_sahkan(recvfrom(peserta_VALUE, data, sizeof data, 0, NULL, NULL) == -1 && errno == EAGAIN);
    tentu_sahkan(close(peserta_VALUE) == 0);
    puts("POSIX UDP CHECK PASS");
    return 0;
}
