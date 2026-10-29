#include <파일규약.h>
#if defined(__linux__) || !defined(__JKOROS__) || __STDC_HOSTED__
#error This sample must be compiled with the native guest cc command.
#endif

int main(int 인수개수, char **არგუმენტი_სია) {
    if (인수개수 < 1 || !არგუმენტი_სია[0]) return 2;
    const char 인사말[] = "자체 커널의 C와 한국어 POSIX\n";
    int 문서 = გახსნა_ფაილი("인사.txt", ჩაწერა_წაკითხვა | 없으면만들기 | 내용비우기, 0600);
    if (문서 < 0) return 1;
    입출력결과형 სიგრძე_მნიშვნელობა = ჩაწერა_ფაილი_მონაცემები(문서, 인사말, sizeof(인사말) - 1);
    დახურვა_ფაილი(문서);
    ჩაწერა_ფაილი_მონაცემები(1, 인사말, sizeof(인사말) - 1);
    return სიგრძე_მნიშვნელობა == sizeof(인사말) - 1 ? 0 : 3;
}
