#include "파일규약.h"
int Sākt_lietotājs_programma(int Parametri) {
    (void)Parametri;
    const char 인사말[] = "C에서 한글 이름과 posix-kor 호출\n";
    int 문서 = atvērt_Fails("C인사.txt", 읽고쓰기 | 없으면만들기 | apraut_Satura_rādītājs, 0600);
    if (문서 < 0) return 1;
    입출력결과형 기록한수 = rakstīšana_Fails_dati(문서, 인사말, sizeof(인사말) - 1);
    Aizvērt_Fails(문서);
    rakstīšana_Fails_dati(1, 인사말, sizeof(인사말) - 1);
    return 기록한수 == sizeof(인사말) - 1 ? 0 : 2;
}
