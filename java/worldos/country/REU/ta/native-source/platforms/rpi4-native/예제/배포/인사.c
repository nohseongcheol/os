#include <파일규약.h>
#if defined(__linux__) || !defined(__JKOROS__) || __STDC_HOSTED__
#error This sample must be compiled with the native guest cc command.
#endif

int main(int 인수개수, char **மதிப்புரு_பட்டியல்) {
    if (인수개수 < 1 || !மதிப்புரு_பட்டியல்[0]) return 2;
    const char 인사말[] = "자체 커널의 C와 தமிழ் POSIX\n";
    int 문서 = திற_கோப்பு("인사.txt", படிக்க_எழுத | 없으면만들기 | 내용비우기, 0600);
    if (문서 < 0) return 1;
    입출력결과형 நீளம்_மதிப்பு = எழுது_கோப்பு_தரவு(문서, 인사말, sizeof(인사말) - 1);
    மூடு_கோப்பு(문서);
    எழுது_கோப்பு_தரவு(1, 인사말, sizeof(인사말) - 1);
    return நீளம்_மதிப்பு == sizeof(인사말) - 1 ? 0 : 3;
}
