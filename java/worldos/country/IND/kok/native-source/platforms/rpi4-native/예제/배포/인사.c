#include <파일규약.h>
#if defined(__linux__) || !defined(__JKOROS__) || __STDC_HOSTED__
#error This sample must be compiled with the native guest cc command.
#endif

int main(int 인수개수, char **युक्तीवाद_सुची) {
    if (인수개수 < 1 || !युक्तीवाद_सुची[0]) return 2;
    const char 인사말[] = "자체 커널의 C와 한국어 POSIX\n";
    int 문서 = उगडचें_फायल("인사.txt", वाचन_बरप | 없으면만들기 | 내용비우기, 0600);
    if (문서 < 0) return 1;
    입출력결과형 लांबाय_मोल = बरोवचें_फायल_डेटा(문서, 인사말, sizeof(인사말) - 1);
    शेवट_फायल(문서);
    बरोवचें_फायल_डेटा(1, 인사말, sizeof(인사말) - 1);
    return लांबाय_मोल == sizeof(인사말) - 1 ? 0 : 3;
}
