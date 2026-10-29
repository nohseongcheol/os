// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class test_Rete {
    public static int avvia() {
        int 첫째 = spazio_utente.aperto_rete(45000);
        if (첫째 < 0) { spazio_utente.Scrittura("NETWORK UNAVAILABLE\n"); return 3; }
        int[] dati = new int[8];
        boolean passare_VALORE = spazio_utente.aperto_rete(45000) == -98
            && spazio_utente.ricevere_dati(첫째, dati, 0) == -11
            && spazio_utente.ricevere_dati(첫째, dati, 50) == -110
            && spazio_utente.ricevere_dati(첫째, dati, 3000) == -22
            && spazio_utente.inviare_dati(첫째, 0x0a000202, 9, dati, 9) == -90
            && spazio_utente.ricevere_dati(첫째, null, 0) == -14
            && spazio_utente.Chiudi_rete(첫째) == 0 && spazio_utente.Chiudi_rete(첫째) == -9;
        spazio_utente.Scrittura(passare_VALORE ? "UDP API CHECK PASS\n" : "UDP API CHECK FAIL\n");
        return passare_VALORE ? 0 : 1;
    }
}
