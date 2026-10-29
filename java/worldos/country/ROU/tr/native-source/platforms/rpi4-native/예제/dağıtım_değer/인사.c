#include <Dosya_ABI.h>
#if defined(__linux__) || !defined(__JKOROS__) || __STDC_HOSTED__
#error This sample must be compiled with the native guest cc command.
#endif

int main(int 인수개수, char **bağımsız_değişken_Liste) {
    if (인수개수 < 1 || !bağımsız_değişken_Liste[0]) return 2;
    const char 인사말[] = "Öz 커널의 C와 Türkçe POSIX\n";
    int 문서 = açık_Dosya("인사.txt", R_W | 없으면만들기 | kesmek_içindekiler, 0600);
    if (문서 < 0) return 1;
    입출력결과형 süre_değer = yazma_Dosya_veri(문서, 인사말, sizeof(인사말) - 1);
    Kapat_Dosya(문서);
    yazma_Dosya_veri(1, 인사말, sizeof(인사말) - 1);
    return süre_değer == sizeof(인사말) - 1 ? 0 : 3;
}
