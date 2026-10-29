#include "Dosya_ABI.h"
int Start_kullanıcı_program(int bağımsız_değişkenler) {
    (void)bağımsız_değişkenler;
    const char 인사말[] = "C에서 한글 이름과 posix-kor 호출\n";
    int 문서 = açık_Dosya("C인사.txt", R_W | 없으면만들기 | kesmek_içindekiler, 0600);
    if (문서 < 0) return 1;
    입출력결과형 기록한수 = yazma_Dosya_veri(문서, 인사말, sizeof(인사말) - 1);
    Kapat_Dosya(문서);
    yazma_Dosya_veri(1, 인사말, sizeof(인사말) - 1);
    return 기록한수 == sizeof(인사말) - 1 ? 0 : 2;
}
