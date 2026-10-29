#include <파일규약.h>
#include <stdio.h>
int main(int item_AANTAL, char **invoer_Lijst_f07b3200) {
    (void)item_AANTAL; (void)invoer_Lijst_f07b3200;
    int bestand = open_Bestand("stored.txt", lezen_schrijven | 없으면만들기 | afkappen_Inhoud, 0600);
    if (bestand < 0 || schrijven_Bestand_gegevens(bestand, "saved-from-C", 12) != 12) return 1;
    if (doorvoeren_Files(bestand) < 0) return 2;
    if (Sluiten_Bestand(bestand) < 0) return 3;
    puts("POSIX FSYNC PASS");
    return 0;
}
