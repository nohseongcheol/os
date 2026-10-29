#include <파일규약.h>
#if defined(__linux__) || !defined(__JKOROS__) || __STDC_HOSTED__
#error This sample must be compiled with the native guest cc command.
#endif

int main(int 인수개수, char **isiniki_myalelo_uludwe) {
    if (인수개수 < 1 || !isiniki_myalelo_uludwe[0]) return 2;
    const char 인사말[] = "자체 커널의 C와 isiXhosa POSIX\n";
    int 문서 = vula_ifayile("인사.txt", funda_bhala | 없으면만들기 | 내용비우기, 0600);
    if (문서 < 0) return 1;
    입출력결과형 ubude_ixabiso = bhala_ifayile_iingcombolo(문서, 인사말, sizeof(인사말) - 1);
    vala_ifayile(문서);
    bhala_ifayile_iingcombolo(1, 인사말, sizeof(인사말) - 1);
    return ubude_ixabiso == sizeof(인사말) - 1 ? 0 : 3;
}
