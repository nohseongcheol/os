#include <Dosya_ABI.h>
#include <ağ_ABI.h>
#include <string.h>
#include <stdio.h>

#define doğrulamak(koşul) do { if (!(koşul)) { puts("POSIX UDP CHECK FAILED: " #koşul); return 1; } } while (0)
int main(int 인수개수, char **bağımsız_değişken_Liste) {
    doğrulamak(인수개수 == 2);
    int bağlantı_noktası_numarası = 0;
    for (int yuva_girdi = 0; bağımsız_değişken_Liste[1][yuva_girdi]; yuva_girdi++) {
        doğrulamak(bağımsız_değişken_Liste[1][yuva_girdi] >= '0' && bağımsız_değişken_Liste[1][yuva_girdi] <= '9');
        bağlantı_noktası_numarası = bağlantı_noktası_numarası * 10 + bağımsız_değişken_Liste[1][yuva_girdi] - '0';
        doğrulamak(bağlantı_noktası_numarası <= 65535);
    }
    int uç_nokta_değer = açmak_uç_nokta(AF_INET, SOCK_DGRAM, 0);
    doğrulamak(uç_nokta_değer == 3);
    struct sockaddr_in yerel_Scope = {0}, eş_değer = {0}, GETİRİ_ADRES = {0};
    yerel_Scope.sin_family = AF_INET;
    socklen_t süre_değer = sizeof yerel_Scope;
    doğrulamak(통신주소읽기(uç_nokta_değer, (struct sockaddr *)&yerel_Scope, &süre_değer) == 0 && yerel_Scope.sin_port == 0);
    doğrulamak(BIND_ADRES(uç_nokta_değer, (struct sockaddr *)&yerel_Scope, sizeof yerel_Scope) == 0);
    doğrulamak(통신주소읽기(uç_nokta_değer, (struct sockaddr *)&yerel_Scope, &süre_değer) == 0 && ntohs(yerel_Scope.sin_port) >= 49152);
    doğrulamak(BIND_ADRES(uç_nokta_değer, (struct sockaddr *)&yerel_Scope, sizeof yerel_Scope) == -1 && errno == EINVAL);
    int 둘째 = socket(AF_INET, SOCK_DGRAM, 0);
    doğrulamak(bind(둘째, (struct sockaddr *)&yerel_Scope, sizeof yerel_Scope) == -1 && errno == EADDRINUSE);
    doğrulamak(close(둘째) == 0);
    둘째 = dup(uç_nokta_değer);
    doğrulamak(close(uç_nokta_değer) == 0); uç_nokta_değer = 둘째;
    eş_değer.sin_family = AF_INET; eş_değer.sin_port = 망차례짧은수(bağlantı_noktası_numarası);
    doğrulamak(ayrıştırmak_ağ_kimliği(AF_INET, "10.0.2.2", &eş_değer.sin_addr) == 1);
    struct timeval bekle_değer = {0, 200000};
    doğrulamak(değiştirmek_ağ_Ayarlar(uç_nokta_değer, SOL_SOCKET, SO_RCVTIMEO, &bekle_değer, sizeof bekle_değer) == 0);
    char veri[32];
    doğrulamak(almak_veri_birimi_veri(uç_nokta_değer, veri, sizeof veri, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    doğrulamak(göndermek_veri_birimi_veri(uç_nokta_değer, "posix-udp", 9, 0, (struct sockaddr *)&eş_değer, sizeof eş_değer) == 9);
    süre_değer = sizeof GETİRİ_ADRES;
    doğrulamak(recvfrom(uç_nokta_değer, (void *)0x00100000, 9, 0, NULL, NULL) == -1 && errno == EFAULT);
    doğrulamak(almak_veri_birimi_veri(uç_nokta_değer, veri, sizeof veri, 0, (struct sockaddr *)&GETİRİ_ADRES, &süre_değer) == 9);
    doğrulamak(memcmp(veri, "posix-udp", 9) == 0 && süre_değer == 16);
    doğrulamak(GETİRİ_ADRES.sin_port == eş_değer.sin_port && GETİRİ_ADRES.sin_addr.s_addr == eş_değer.sin_addr.s_addr);
    doğrulamak(sendto(uç_nokta_değer, "truncate", 8, 0, (struct sockaddr *)&eş_değer, sizeof eş_değer) == 8);
    doğrulamak(recvfrom(uç_nokta_değer, veri, 3, 0, NULL, NULL) == 3 && memcmp(veri, "tru", 3) == 0);
    doğrulamak(recvfrom(uç_nokta_değer, veri, sizeof veri, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    doğrulamak(sendto(uç_nokta_değer, NULL, 0, 0, (struct sockaddr *)&eş_değer, sizeof eş_değer) == 0);
    doğrulamak(recvfrom(uç_nokta_değer, NULL, 0, 0, NULL, NULL) == 0);
    doğrulamak(recvfrom(uç_nokta_değer, veri, sizeof veri, 0, NULL, NULL) == -1 && errno == EAGAIN);
    doğrulamak(close(uç_nokta_değer) == 0);
    puts("POSIX UDP CHECK PASS");
    return 0;
}
