#include <unistd.h>
#include <fcntl.h>
#include <errno.h>
#include <النظام/stat.h>
int __posix_library_test(void);

int main(void)
{
    char مخزن_النقل_المؤقت_2[16];
    /* USER2 is the ELF fixture installed by the boot harness, not user data. */
    int واصف_الملف = فتح("/USER2", O_RDONLY);
    struct حالة_الملف st;
    if (واصف_الملف < 0 || جلب_حالة_الملف_المفتوح(واصف_الملف, &st) < 0 || قراءة(واصف_الملف, مخزن_النقل_المؤقت_2, 4) != 4 ||
        (unsigned char)مخزن_النقل_المؤقت_2[0] != 0x7f || مخزن_النقل_المؤقت_2[1] != 'E' || مخزن_النقل_المؤقت_2[2] != 'L' || مخزن_النقل_المؤقت_2[3] != 'F' ||
        نقل_موضع_الملف(واصف_الملف, 0, SEEK_SET) != 0 || إغلاق(واصف_الملف) < 0 || جلب_معرف_العملية() <= 0)
        goto failure;
    errno = 0;
    if (قراءة(-1, مخزن_النقل_المؤقت_2, 1) != -1 || errno != EBADF)
        goto failure;
    if (__posix_library_test() != 0)
        goto failure;
    if (كتابة(STDOUT_FILENO, "POSIX-NATIVE:PASS\n", 18) != 18)
        goto failure;
    return 0;
failure:
    كتابة(STDOUT_FILENO, "POSIX-NATIVE:FAIL\n", 18);
    return 1;
}
