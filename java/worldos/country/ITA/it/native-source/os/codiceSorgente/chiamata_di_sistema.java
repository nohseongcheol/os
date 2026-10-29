// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** int 0x80 게이트가 호출한다. 모든 spazio_utente puntatore/길이는 accesso_voce 전에 검사한다. */
public final class chiamata_di_sistema {
    static int[] 임시자료 = new int[1024];

    static int array_durata(int e_mail) {
        if (!esecuzione_manager.ritagliare(e_mail, 4)) return -14;
        int durata_VALORE = esecuzione_manager.numero(e_mail);
        if (durata_VALORE < 0 || durata_VALORE > (esecuzione_manager.USER_chiudere - e_mail - 4) / 4) return -14;
        return durata_VALORE;
    }

    public static int Processi_VALORE_voce(int INDICE, int 가, int SECONDO_operando, int 다, int 라, int 마) {
        if (INDICE == 30) return File_descrittore_manager.aperto_File(가, SECONDO_operando, 다);
        if (INDICE == 31) return File_descrittore_manager.파일읽기(가, SECONDO_operando, 다);
        if (INDICE == 32) return File_descrittore_manager.scrivere_File(가, SECONDO_operando, 다);
        if (INDICE == 33) return File_descrittore_manager.Chiudi_File(가);
        if (INDICE == 34) return File_descrittore_manager.cercare_File(가, SECONDO_operando, 다);
        if (INDICE == 35) return File_descrittore_manager.Duplica_descrittore(가, 0, false, 0);
        if (INDICE == 36) return File_descrittore_manager.Duplica_descrittore(가, SECONDO_operando, true, 0);
        if (INDICE == 37) return File_descrittore_manager.파일상태읽기(가, SECONDO_operando);
        if (INDICE == 38) return File_descrittore_manager.rimuovere_File_voce_nome(가);
        if (INDICE == 39) return File_descrittore_manager.set_File_durata(가, SECONDO_operando);
        if (INDICE == 40) return File_descrittore_manager.controllo_descrittore(가, SECONDO_operando, 다);
        if (INDICE == 41) return File_descrittore_manager.Crea_endpoint(가, SECONDO_operando, 다);
        if (INDICE == 42) return File_descrittore_manager.BIND_e_mail(가, SECONDO_operando, 다);
        if (INDICE == 43) return File_descrittore_manager.inviare_datagramma_dati(가, SECONDO_operando, 다, 라, 마);
        if (INDICE == 44) return File_descrittore_manager.ricevere_datagramma_dati(가, SECONDO_operando, 다, 라, 마);
        if (INDICE == 45) return File_descrittore_manager.통신주소읽기(가, SECONDO_operando, 다);
        if (INDICE == 46) return File_descrittore_manager.set_ricevere_TIMEOUT(가, SECONDO_operando);
        if (INDICE == 47) {
            int descrittore_VALORE = File_descrittore_manager.TROVA_descrittore(가);
            if (descrittore_VALORE < 0) return -9;
            if (File_descrittore_manager.Kind_VALORE[descrittore_VALORE] != 2) return -22;
            return 파일보존.sincronizzare();
        }
        if (INDICE == 1) {
            int durata_VALORE = array_durata(가);
            if (durata_VALORE < 0) return durata_VALORE;
            if (durata_VALORE > 4096) return -90;
            for (int carattere_VALORE = 0; carattere_VALORE < durata_VALORE; carattere_VALORE++) SMS_Terminale.문자(esecuzione_manager.numero(가 + 4 + carattere_VALORE * 4) & 65535);
            return durata_VALORE;
        }
        if (INDICE == 2) return esecuzione_manager.argomento_CONTA_NUMERI;
        if (INDICE == 3) return 가 >= 0 && 가 < esecuzione_manager.argomento_CONTA_NUMERI ? esecuzione_manager.argomento_e_mail[가] : 0;
        if (INDICE == 10) return rete_Pila.Apri(가);
        if (INDICE == 11) {
            int durata_VALORE = array_durata(라);
            if (durata_VALORE < 0) return durata_VALORE;
            if (마 < 0 || 마 > durata_VALORE || 마 > 1024) return -90;
            for (int posizione = 0; posizione < 마; posizione++) 임시자료[posizione] = esecuzione_manager.numero(라 + 4 + posizione * 4) & 255;
            return rete_Pila.inviare(가, SECONDO_operando, 다, 임시자료, 마);
        }
        if (INDICE == 12) {
            int durata_VALORE = array_durata(SECONDO_operando);
            if (durata_VALORE < 0) return durata_VALORE;
            if (다 < 0 || 다 > 2000) return -22;
            int risultato = rete_Pila.ricevere(가, 임시자료, durata_VALORE < 1024 ? durata_VALORE : 1024, 다);
            if (risultato >= 0) for (int posizione = 0; posizione < risultato; posizione++) esecuzione_manager.scrivere_numero(SECONDO_operando + 4 + posizione * 4, 임시자료[posizione]);
            return risultato;
        }
        if (INDICE == 13) return rete_Pila.Chiudi(가);
        if (INDICE == 14) return rete_Pila.내주소;
        if (INDICE == 15) return rete_Pila.peer_e_mail(가);
        if (INDICE == 16) return rete_Pila.peer_numero_di_porta(가);
        if (INDICE == 22) {
            if (가 < 0 || 가 > 65535) return -22;
            SMS_Terminale.문자(가); return 1;
        }
        if (INDICE == 20 || INDICE == 21) {
            int nome_ridimensionare = array_durata(가), dati_ridimensionare = array_durata(SECONDO_operando);
            if (nome_ridimensionare < 0 || dati_ridimensionare < 0) return -14;
            if (nome_ridimensionare < 1 || nome_ridimensionare > 64) return -22;
            int durata_VALORE = 0;
            while (durata_VALORE < nome_ridimensionare && esecuzione_manager.numero(가 + 4 + durata_VALORE * 4) != 0) {
                Memoria_file_system.Nome[durata_VALORE] = esecuzione_manager.numero(가 + 4 + durata_VALORE * 4);
                durata_VALORE++;
            }
            if (!Memoria_file_system.assegno_nome(Memoria_file_system.Nome, durata_VALORE)) return -22;
            if (INDICE == 20) {
                int file = Memoria_file_system.TROVA_voce(Memoria_file_system.Nome, durata_VALORE);
                if (file < 0) return file;
                int Dimensione = Memoria_file_system.ridimensionare_elenco[file];
                if (Dimensione > dati_ridimensionare) return -90;
                int e_mail = cellulare_VALORE.File_Memoria() + file * Memoria_file_system.최대크기;
                for (int numero = 0; numero < Dimensione; numero++) esecuzione_manager.scrivere_numero(SECONDO_operando + 4 + numero * 4, cellulare_VALORE.기억읽기(e_mail + numero));
                return Dimensione;
            }
            if (다 < 0 || 다 > dati_ridimensionare) return -22;
            if (다 > Memoria_file_system.최대크기) return -90;
            for (int numero = 0; numero < 다; numero++) Memoria_file_system.Modifica_VALORE[numero] = esecuzione_manager.numero(SECONDO_operando + 4 + numero * 4) & 255;
            return Memoria_file_system.Store_VALORE(Memoria_file_system.Nome, durata_VALORE, Memoria_file_system.Modifica_VALORE, 다);
        }
        return -38;
    }
}
