#include <파일규약.h>
#if defined(__linux__) || !defined(__JKOROS__) || __STDC_HOSTED__
#error This sample must be compiled with the native guest cc command.
#endif

int main(int 인수개수, char **tohenga_Rārangi) {
    if (인수개수 < 1 || !tohenga_Rārangi[0]) return 2;
    const char 인사말[] = "자체 커널의 C와 Reo_Māori POSIX\n";
    int 문서 = tiwhikete_kōnae("인사.txt", 읽고쓰기 | 없으면만들기 | 내용비우기, 0600);
    if (문서 < 0) return 1;
    입출력결과형 roa_uara = tuhi_kōnae_raraunga(문서, 인사말, sizeof(인사말) - 1);
    kati_kōnae(문서);
    tuhi_kōnae_raraunga(1, 인사말, sizeof(인사말) - 1);
    return roa_uara == sizeof(인사말) - 1 ? 0 : 3;
}
