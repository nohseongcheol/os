#include <unistd.h>
#include <fcntl.h>
#include <errno.h>
#include <प्रणाली/stat.h>
int __posix_library_test(void);

int main(void)
{
    char स्थानांतरण_का_अस्थायी_भंडार_2[16];
    /* USER2 is the ELF fixture installed by the boot harness, not user data. */
    int संचिका_विवरणक = खोलना("/USER2", O_RDONLY);
    struct संचिका_स्थिति st;
    if (संचिका_विवरणक < 0 || खुली_संचिका_स्थिति_पाना(संचिका_विवरणक, &st) < 0 || पढ़ना(संचिका_विवरणक, स्थानांतरण_का_अस्थायी_भंडार_2, 4) != 4 ||
        (unsigned char)स्थानांतरण_का_अस्थायी_भंडार_2[0] != 0x7f || स्थानांतरण_का_अस्थायी_भंडार_2[1] != 'E' || स्थानांतरण_का_अस्थायी_भंडार_2[2] != 'L' || स्थानांतरण_का_अस्थायी_भंडार_2[3] != 'F' ||
        पठन_लेखन_स्थिति_बदलना(संचिका_विवरणक, 0, SEEK_SET) != 0 || बंद_करना(संचिका_विवरणक) < 0 || प्रक्रिया_पहचान_पाना() <= 0)
        goto failure;
    errno = 0;
    if (पढ़ना(-1, स्थानांतरण_का_अस्थायी_भंडार_2, 1) != -1 || errno != EBADF)
        goto failure;
    if (__posix_library_test() != 0)
        goto failure;
    if (लिखना(STDOUT_FILENO, "POSIX-NATIVE:PASS\n", 18) != 18)
        goto failure;
    return 0;
failure:
    लिखना(STDOUT_FILENO, "POSIX-NATIVE:FAIL\n", 18);
    return 1;
}
