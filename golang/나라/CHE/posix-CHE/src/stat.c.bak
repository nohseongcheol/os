#include <System/stat.h>
#include <System/Systemkennung.h>
#include <System/syscall.h>

enum { SYS_Dateizustand = 106, SYS_Verknüpfungszustand_ermitteln = 107, SYS_Zustand_offener_Datei_ermitteln = 108, SYS_Systeminformationen_ermitteln = 122 };

int Dateizustand(const char *Pfad, struct Dateizustand *Übertragungspuffer)
{
    return (int)__syscall_result(
        __syscall6(SYS_Dateizustand, (long)Pfad, (long)Übertragungspuffer, 0, 0, 0, 0));
}

int Verknüpfungszustand_ermitteln(const char *Pfad, struct Dateizustand *Übertragungspuffer)
{
    return (int)__syscall_result(
        __syscall6(SYS_Verknüpfungszustand_ermitteln, (long)Pfad, (long)Übertragungspuffer, 0, 0, 0, 0));
}

int Zustand_offener_Datei_ermitteln(int Dateideskriptor, struct Dateizustand *Übertragungspuffer)
{
    return (int)__syscall_result(
        __syscall6(SYS_Zustand_offener_Datei_ermitteln, Dateideskriptor, (long)Übertragungspuffer, 0, 0, 0, 0));
}

int Systeminformationen_ermitteln(struct utsname *Systemidentität)
{
    return (int)__syscall_result(
        __syscall6(SYS_Systeminformationen_ermitteln, (long)Systemidentität, 0, 0, 0, 0, 0));
}
