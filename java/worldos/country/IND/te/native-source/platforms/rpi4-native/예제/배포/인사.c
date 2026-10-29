#include <파일규약.h>
#if defined(__linux__) || !defined(__JKOROS__) || __STDC_HOSTED__
#error This sample must be compiled with the native guest cc command.
#endif

int main(int 인수개수, char **కారకం_జాబితా) {
    if (인수개수 < 1 || !కారకం_జాబితా[0]) return 2;
    const char 인사말[] = "자체 커널의 C와 한국어 POSIX\n";
    int 문서 = తెరువు_ఫైలు("인사.txt", పఠన_లేఖన | 없으면만들기 | 내용비우기, 0600);
    if (문서 < 0) return 1;
    입출력결과형 పొడవు_మూల్యం = వ్రాయి_ఫైలు_డేటా(문서, 인사말, sizeof(인사말) - 1);
    మూసివేయి_ఫైలు(문서);
    వ్రాయి_ఫైలు_డేటా(1, 인사말, sizeof(인사말) - 1);
    return పొడవు_మూల్యం == sizeof(인사말) - 1 ? 0 : 3;
}
