#include <파일규약.h>
#if defined(__linux__) || !defined(__JKOROS__) || __STDC_HOSTED__
#error This sample must be compiled with the native guest cc command.
#endif

int main(int 인수개수, char **ágúmẹ́ntì_Àtòkọ) {
    if (인수개수 < 1 || !ágúmẹ́ntì_Àtòkọ[0]) return 2;
    const char 인사말[] = "자체 커널의 C와 한국어 POSIX\n";
    int 문서 = ṣí_fáìlì("인사.txt", tí_a_lè_kà_tí_a_lè_kọ | 없으면만들기 | 내용비우기, 0600);
    if (문서 < 0) return 1;
    입출력결과형 gígùn_iye = kọ_fáìlì_détà(문서, 인사말, sizeof(인사말) - 1);
    pa_dé_fáìlì(문서);
    kọ_fáìlì_détà(1, 인사말, sizeof(인사말) - 1);
    return gígùn_iye == sizeof(인사말) - 1 ? 0 : 3;
}
