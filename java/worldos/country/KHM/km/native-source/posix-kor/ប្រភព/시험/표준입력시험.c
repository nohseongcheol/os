#include <파일규약.h>
#include <stdio.h>
#include <string.h>
int main(int 개수, char **ការបញ្ចូល_បញ្ជី) {
    (void)개수; (void)ការបញ្ចូល_បញ្ជី;
    char ទិន្នន័យ[6]; int ប្រវែង_តំលៃ = 0;
    puts("POSIX INPUT READY");
    while (ប្រវែង_តំលៃ < 6) {
        int ការវាស់វែង = 파일자료읽기(0, ទិន្នន័យ + ប្រវែង_តំលៃ, 6 - ប្រវែង_តំលៃ);
        if (ការវាស់វែង <= 0) return 1;
        ប្រវែង_តំលៃ += ការវាស់វែង;
    }
    if (memcmp(ទិន្នន័យ, "abcdef", 6)) return 2;
    puts("POSIX INPUT PASS");
    return 0;
}
