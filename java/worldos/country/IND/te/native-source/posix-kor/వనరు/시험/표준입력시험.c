#include <파일규약.h>
#include <stdio.h>
#include <string.h>
int main(int 개수, char **ప్రవేశం_జాబితా) {
    (void)개수; (void)ప్రవేశం_జాబితా;
    char డేటా[6]; int పొడవు_మూల్యం = 0;
    puts("POSIX INPUT READY");
    while (పొడవు_మూల్యం < 6) {
        int ప్రమాణం = 파일자료읽기(0, డేటా + పొడవు_మూల్యం, 6 - పొడవు_మూల్యం);
        if (ప్రమాణం <= 0) return 1;
        పొడవు_మూల్యం += ప్రమాణం;
    }
    if (memcmp(డేటా, "abcdef", 6)) return 2;
    puts("POSIX INPUT PASS");
    return 0;
}
