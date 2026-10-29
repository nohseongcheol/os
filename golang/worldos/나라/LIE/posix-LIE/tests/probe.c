#include <unistd.h>
#include <fcntl.h>
#include <errno.h>
#include <System/stat.h>
int __posix_library_test(void);

int main(void)
{
    char Übertragungspuffer_2[16];
    /* USER2 is the ELF fixture installed by the boot harness, not user data. */
    int Dateideskriptor = öffnen("/USER2", O_RDONLY);
    struct Dateizustand st;
    if (Dateideskriptor < 0 || Zustand_offener_Datei_ermitteln(Dateideskriptor, &st) < 0 || lesen(Dateideskriptor, Übertragungspuffer_2, 4) != 4 ||
        (unsigned char)Übertragungspuffer_2[0] != 0x7f || Übertragungspuffer_2[1] != 'E' || Übertragungspuffer_2[2] != 'L' || Übertragungspuffer_2[3] != 'F' ||
        Dateiposition_verschieben(Dateideskriptor, 0, SEEK_SET) != 0 || schließen(Dateideskriptor) < 0 || Prozesskennung_ermitteln() <= 0)
        goto failure;
    errno = 0;
    if (lesen(-1, Übertragungspuffer_2, 1) != -1 || errno != EBADF)
        goto failure;
    if (__posix_library_test() != 0)
        goto failure;
    if (schreiben(STDOUT_FILENO, "POSIX-NATIVE:PASS\n", 18) != 18)
        goto failure;
    return 0;
failure:
    schreiben(STDOUT_FILENO, "POSIX-NATIVE:FAIL\n", 18);
    return 1;
}
