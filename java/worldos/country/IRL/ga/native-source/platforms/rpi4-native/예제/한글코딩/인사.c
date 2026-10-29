#include "파일규약.h"
int Start_úsáideoir_clár(int Argóintí) {
    (void)Argóintí;
    const char 인사말[] = "C에서 한글 이름과 posix-kor 호출\n";
    int 문서 = oscail_comhad("C인사.txt", inléite_inscríofa | 없으면만들기 | 내용비우기, 0600);
    if (문서 < 0) return 1;
    입출력결과형 기록한수 = scríobh_comhad_sonraí(문서, 인사말, sizeof(인사말) - 1);
    dún_comhad(문서);
    scríobh_comhad_sonraí(1, 인사말, sizeof(인사말) - 1);
    return 기록한수 == sizeof(인사말) - 1 ? 0 : 2;
}
