// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class messaggio_di_saluto_ae353e94 {
    public static int avvia() {
        spazio_utente.Scrittura("Hello from a separate Java ELF!\n");
        spazio_utente.Scrittura(spazio_utente.esecuzione_privilegio() == 3 ? "USER MODE ring 3\n" : "WRONG PRIVILEGE\n");
        for (int INDICE = 0; INDICE < spazio_utente.인수개수(); INDICE++) {
            spazio_utente.Scrittura("arg: "); spazio_utente.Scrittura(spazio_utente.argomenti(INDICE)); spazio_utente.Scrittura("\n");
        }
        return spazio_utente.esecuzione_privilegio() == 3 ? 0 : 1;
    }
}
