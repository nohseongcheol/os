#include <파일규약.h>
#if defined(__linux__) || !defined(__JKOROS__) || __STDC_HOSTED__
#error This sample must be compiled with the native guest cc command.
#endif

int main(int 인수개수, char **ആര്_ഗ്യുമെന്_റ്_ലിസ്റ്റ്) {
    if (인수개수 < 1 || !ആര്_ഗ്യുമെന്_റ്_ലിസ്റ്റ്[0]) return 2;
    const char 인사말[] = "자체 커널의 C와 한국어 POSIX\n";
    int 문서 = തുറക്കുക_ഫയല്("인사.txt", വായനാ_റൈറ്റ് | 없으면만들기 | 내용비우기, 0600);
    if (문서 < 0) return 1;
    입출력결과형 ദൈര്_ഘ്യം_മൂല്യം = റൈറ്റ്_ചെയ്യുക_ഫയല്_ഡാറ്റാ(문서, 인사말, sizeof(인사말) - 1);
    അടയ്ക്കുക_ഫയല്(문서);
    റൈറ്റ്_ചെയ്യുക_ഫയല്_ഡാറ്റാ(1, 인사말, sizeof(인사말) - 1);
    return ദൈര്_ഘ്യം_മൂല്യം == sizeof(인사말) - 1 ? 0 : 3;
}
