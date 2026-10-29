#include <unistd.h>
#include <fcntl.h>
#include <errno.h>
#include <sys/stat.h>
int __posix_library_test(void);

int main(void)
{
    char bufor_przesyłania_2[16];
    /* USER2 is the ELF fixture installed by the boot harness, not user data. */
    int deskryptor_pliku = Otwórz("/USER2", O_RDONLY);
    struct stat st;
    if (deskryptor_pliku < 0 || fstat(deskryptor_pliku, &st) < 0 || Odczyt(deskryptor_pliku, bufor_przesyłania_2, 4) != 4 ||
        (unsigned char)bufor_przesyłania_2[0] != 0x7f || bufor_przesyłania_2[1] != 'E' || bufor_przesyłania_2[2] != 'L' || bufor_przesyłania_2[3] != 'F' ||
        lseek(deskryptor_pliku, 0, SEEK_SET) != 0 || Zamknij(deskryptor_pliku) < 0 || getpid() <= 0)
        goto failure;
    errno = 0;
    if (Odczyt(-1, bufor_przesyłania_2, 1) != -1 || errno != EBADF)
        goto failure;
    if (__posix_library_test() != 0)
        goto failure;
    if (Zapis(STDOUT_FILENO, "POSIX-NATIVE:PASS\n", 18) != 18)
        goto failure;
    return 0;
failure:
    Zapis(STDOUT_FILENO, "POSIX-NATIVE:FAIL\n", 18);
    return 1;
}
