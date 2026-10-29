#include <파일규약.h>
#include <stdio.h>
int main(int 개수, char **உள்ளீடு_பட்டியல்) {
    (void)개수; (void)உள்ளீடு_பட்டியல்;
    int கோப்பின்_பெயர் = திற_கோப்பு("stored.txt", படிக்க_எழுத | 없으면만들기 | 내용비우기, 0600);
    if (கோப்பின்_பெயர் < 0 || எழுது_கோப்பு_தரவு(கோப்பின்_பெயர், "saved-from-C", 12) != 12) return 1;
    if (파일저장확정(கோப்பின்_பெயர்) < 0) return 2;
    if (மூடு_கோப்பு(கோப்பின்_பெயர்) < 0) return 3;
    puts("POSIX FSYNC PASS");
    return 0;
}
