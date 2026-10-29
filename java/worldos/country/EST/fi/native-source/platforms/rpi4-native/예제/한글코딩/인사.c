#include "파일규약.h"
int alku_käyttäjä_ohjelma(int argumentit) {
    (void)argumentit;
    const char 인사말[] = "C에서 한글 이름과 posix-kor 호출\n";
    int 문서 = avata_Tiedosto("C인사.txt", luku_ja_kirjoitus | 없으면만들기 | 내용비우기, 0600);
    if (문서 < 0) return 1;
    입출력결과형 기록한수 = kirjoitus_Tiedosto_data(문서, 인사말, sizeof(인사말) - 1);
    Sulje_Tiedosto(문서);
    kirjoitus_Tiedosto_data(1, 인사말, sizeof(인사말) - 1);
    return 기록한수 == sizeof(인사말) - 1 ? 0 : 2;
}
