#include "파일규약.h"
int nis_përdorues_program(int Argumente) {
    (void)Argumente;
    const char 인사말[] = "C에서 한글 이름과 posix-kor 호출\n";
    int 문서 = hap_skedar("C인사.txt", lexoj_shkruaj | 없으면만들기 | 내용비우기, 0600);
    if (문서 < 0) return 1;
    입출력결과형 기록한수 = shkruaj_skedar_të_dhëna(문서, 인사말, sizeof(인사말) - 1);
    mbyll_skedar(문서);
    shkruaj_skedar_të_dhëna(1, 인사말, sizeof(인사말) - 1);
    return 기록한수 == sizeof(인사말) - 1 ? 0 : 2;
}
