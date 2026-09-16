/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <unistd.h>
#include <fcntl.h>
#include <errno.h>
#include <அமைப்பு/stat.h>
int __posix_library_test(void);

int main(void)
{
    char பரிமாற்ற_இடையகம்_2[16];
    /* USER2 is the ELF fixture installed by the boot harness, not user data. */
    int கோப்பு_விவரிப்பி = திற("/USER2", O_RDONLY);
    struct கோப்பு_நிலை st;
    if (கோப்பு_விவரிப்பி < 0 || திறந்த_கோப்பின்_நிலையைப்_பெறு(கோப்பு_விவரிப்பி, &st) < 0 || படி(கோப்பு_விவரிப்பி, பரிமாற்ற_இடையகம்_2, 4) != 4 ||
        (unsigned char)பரிமாற்ற_இடையகம்_2[0] != 0x7f || பரிமாற்ற_இடையகம்_2[1] != 'E' || பரிமாற்ற_இடையகம்_2[2] != 'L' || பரிமாற்ற_இடையகம்_2[3] != 'F' ||
        கோப்பின்_படிப்பிடத்தை_நகர்த்து(கோப்பு_விவரிப்பி, 0, SEEK_SET) != 0 || மூடு(கோப்பு_விவரிப்பி) < 0 || செயல்முறை_அடையாளத்தைப்_பெறு() <= 0)
        goto failure;
    errno = 0;
    if (படி(-1, பரிமாற்ற_இடையகம்_2, 1) != -1 || errno != EBADF)
        goto failure;
    if (__posix_library_test() != 0)
        goto failure;
    if (எழுது(STDOUT_FILENO, "POSIX-NATIVE:PASS\n", 18) != 18)
        goto failure;
    return 0;
failure:
    எழுது(STDOUT_FILENO, "POSIX-NATIVE:FAIL\n", 18);
    return 1;
}
