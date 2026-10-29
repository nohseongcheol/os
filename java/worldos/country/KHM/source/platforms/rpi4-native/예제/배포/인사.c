#include <파일규약.h>
#if defined(__linux__) || !defined(__JKOROS__) || __STDC_HOSTED__
#error This sample must be compiled with the native guest cc command.
#endif

int main(int 인수개수, char **អាគុយម៉ង់_បញ្ជី) {
    if (인수개수 < 1 || !អាគុយម៉ង់_បញ្ជី[0]) return 2;
    const char 인사말[] = "자체 커널의 C와 한국어 POSIX\n";
    int 문서 = បើក_ឯកសារ("인사.txt", អាន_សរសេរ | 없으면만들기 | 내용비우기, 0600);
    if (문서 < 0) return 1;
    입출력결과형 ប្រវែង_តំលៃ = សរសេរ_ឯកសារ_ទិន្នន័យ(문서, 인사말, sizeof(인사말) - 1);
    បិទ_ឯកសារ(문서);
    សរសេរ_ឯកសារ_ទិន្នន័យ(1, 인사말, sizeof(인사말) - 1);
    return ប្រវែង_តំលៃ == sizeof(인사말) - 1 ? 0 : 3;
}
