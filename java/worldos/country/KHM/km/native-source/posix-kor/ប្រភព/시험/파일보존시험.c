#include <파일규약.h>
#include <stdio.h>
int main(int 개수, char **ការបញ្ចូល_បញ្ជី) {
    (void)개수; (void)ការបញ្ចូល_បញ្ជី;
    int ឯកសារ = បើក_ឯកសារ("stored.txt", អាន_សរសេរ | 없으면만들기 | 내용비우기, 0600);
    if (ឯកសារ < 0 || សរសេរ_ឯកសារ_ទិន្នន័យ(ឯកសារ, "saved-from-C", 12) != 12) return 1;
    if (파일저장확정(ឯកសារ) < 0) return 2;
    if (បិទ_ឯកសារ(ឯកសារ) < 0) return 3;
    puts("POSIX FSYNC PASS");
    return 0;
}
