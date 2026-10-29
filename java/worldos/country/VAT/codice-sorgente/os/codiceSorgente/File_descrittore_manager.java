// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 단일 spazio_utente 과정의 파일서술자와 열린 file 기술을 분리한다. 호출 번호는 POSIX ABI 문서에 기록한다. */
public final class File_descrittore_manager {
    static final int 서술자한도 = 32;
    static final int in_lettura_scrittura_flag = 2, Crea_voce = 64, 독점생성 = 128, liquidare_Sommario = 512;
    static final int 이어쓰기 = 1024, 기다리지않기 = 2048, 실행시닫기 = 524288;
    static int[] aperto_handle = new int[서술자한도], set_descrittore = new int[서술자한도];
    static int[] Kind_VALORE = new int[서술자한도], target = new int[서술자한도];
    static int[] File_funzione = new int[서술자한도], aperto_Impostazioni = new int[서술자한도], fonti_CONTA_NUMERI = new int[서술자한도];
    static int[] rete_handle = new int[서술자한도], 수신대기밀리초 = new int[서술자한도];
    static int[] percorso_nome = new int[64], trasferire_dati = new int[1024];

    static int TROVA_descrittore(int File_descrittore) {
        if (File_descrittore < 0 || File_descrittore >= 서술자한도) return -9;
        return aperto_handle[File_descrittore] - 1;
    }
    static int vuota_descrittore(int avvia) {
        for (int INDICE = avvia; INDICE < 서술자한도; INDICE++) if (aperto_handle[INDICE] == 0) return INDICE;
        return -24;
    }
    static int vuota_handle() {
        for (int INDICE = 0; INDICE < 서술자한도; INDICE++) if (fonti_CONTA_NUMERI[INDICE] == 0) return INDICE;
        return -24;
    }
    static int Connetti(int descrittore_voce, int descrittore_VALORE, int File_Kind, int File_target, int Impostazioni) {
        aperto_handle[descrittore_voce] = descrittore_VALORE + 1; set_descrittore[descrittore_voce] = (Impostazioni & 실행시닫기) != 0 ? 1 : 0;
        Kind_VALORE[descrittore_VALORE] = File_Kind; target[descrittore_VALORE] = File_target; fonti_CONTA_NUMERI[descrittore_VALORE] = 1;
        aperto_Impostazioni[descrittore_VALORE] = Impostazioni & (3 | 이어쓰기 | 기다리지않기); File_funzione[descrittore_VALORE] = 0;
        rete_handle[descrittore_VALORE] = 0; 수신대기밀리초[descrittore_VALORE] = 0;
        return descrittore_voce;
    }
    static void START_Processi() {
        LIBERA_Processi();
        for (int INDICE = 0; INDICE < 3; INDICE++) Connetti(INDICE, INDICE, 1, INDICE, INDICE == 0 ? 0 : 1);
    }
    static void LIBERA_Processi() {
        for (int INDICE = 0; INDICE < 서술자한도; INDICE++) if (aperto_handle[INDICE] != 0) Chiudi_File(INDICE);
    }
    static int Chiudi_File(int descrittore_voce) {
        int descrittore_VALORE = TROVA_descrittore(descrittore_voce);
        if (descrittore_VALORE < 0) return -9;
        aperto_handle[descrittore_voce] = 0; set_descrittore[descrittore_voce] = 0;
        fonti_CONTA_NUMERI[descrittore_VALORE]--;
        if (fonti_CONTA_NUMERI[descrittore_VALORE] == 0) {
            if (Kind_VALORE[descrittore_VALORE] == 2) Memoria_file_system.aperto_CONTA_NUMERI[target[descrittore_VALORE]]--;
            if (Kind_VALORE[descrittore_VALORE] == 3 && rete_handle[descrittore_VALORE] != 0) rete_Pila.Chiudi(rete_handle[descrittore_VALORE]);
            Kind_VALORE[descrittore_VALORE] = 0;
        }
        return 0;
    }
    // C 경로는 NUL 끝 byte_VALORE 문자열이다. 루트의 한 이름만 지원한다.
    static int 경로읽기(int e_mail) {
        if (!esecuzione_manager.ritagliare(e_mail, 1)) return -14;
        int posizione = cellulare_VALORE.기억읽기(e_mail) == '/' ? 1 : 0;
        for (int durata_VALORE = 0; durata_VALORE < 64; durata_VALORE++) {
            if (!esecuzione_manager.ritagliare(e_mail + posizione + durata_VALORE, 1)) return -14;
            int VALORE = cellulare_VALORE.기억읽기(e_mail + posizione + durata_VALORE);
            percorso_nome[durata_VALORE] = VALORE;
            if (VALORE == 0) return durata_VALORE == 0 ? -2 : (Memoria_file_system.assegno_nome(percorso_nome, durata_VALORE) ? durata_VALORE : -22);
            if (VALORE == '/') return -20;
        }
        return -36;
    }
    static int aperto_File(int nome_e_mail, int Impostazioni, int concessione_privilegio) {
        int durata_VALORE = 경로읽기(nome_e_mail);
        if (durata_VALORE < 0) return durata_VALORE;
        if ((Impostazioni & ~(3 | Crea_voce | 독점생성 | liquidare_Sommario | 이어쓰기 | 기다리지않기 | 실행시닫기)) != 0) return -95;
        if ((Impostazioni & 3) == 3 || ((Impostazioni & liquidare_Sommario) != 0 && (Impostazioni & 3) == 0)) return -22;
        int file = Memoria_file_system.TROVA_voce(percorso_nome, durata_VALORE);
        if (file >= 0 && (Impostazioni & (Crea_voce | 독점생성)) == (Crea_voce | 독점생성)) return -17;
        if (file == -2 && (Impostazioni & Crea_voce) == 0) return -2;
        int descrittore_voce = vuota_descrittore(0), descrittore_VALORE = vuota_handle();
        if (descrittore_voce < 0 || descrittore_VALORE < 0) return -24;
        if (file == -2) {
            int risultato = Memoria_file_system.Store_VALORE(percorso_nome, durata_VALORE, percorso_nome, 0);
            if (risultato < 0) return risultato;
            file = Memoria_file_system.TROVA_voce(percorso_nome, durata_VALORE);
            Memoria_file_system.허가들[file] = concessione_privilegio & 511;
        }
        if (file < 0) return file;
        if ((Impostazioni & liquidare_Sommario) != 0) Memoria_file_system.ridimensionare_elenco[file] = 0;
        Memoria_file_system.aperto_CONTA_NUMERI[file]++;
        return Connetti(descrittore_voce, descrittore_VALORE, 2, file, Impostazioni);
    }
    static int 파일읽기(int descrittore_voce, int dati_e_mail, int durata_VALORE) {
        int descrittore_VALORE = TROVA_descrittore(descrittore_voce);
        if (descrittore_VALORE < 0 || (aperto_Impostazioni[descrittore_VALORE] & 3) == 1) return -9;
        if (durata_VALORE < 0) return -22;
        if (durata_VALORE == 0) return 0;
        if (!esecuzione_manager.ritagliare(dati_e_mail, durata_VALORE)) return -14;
        if (Kind_VALORE[descrittore_VALORE] == 3) return ricevere_datagramma_dati(descrittore_voce, dati_e_mail, durata_VALORE, 0, 0);
        if (Kind_VALORE[descrittore_VALORE] == 1) {
            int RICEV_SCAD_CONTA_NUMERI = 0;
            while (RICEV_SCAD_CONTA_NUMERI < durata_VALORE) {
                int VALORE = SMS_Terminale.직렬읽기();
                if (VALORE < 0) VALORE = tastiera.Lettura();
                if (VALORE < 0) {
                    if (RICEV_SCAD_CONTA_NUMERI > 0) return RICEV_SCAD_CONTA_NUMERI;
                    if ((aperto_Impostazioni[descrittore_VALORE] & 기다리지않기) != 0) return -11;
                    if (cellulare_VALORE.사용자남은밀리초() <= 10) return -11;
                    rete_Pila.verificare(); cellulare_VALORE.잠시양보();
                } else {
                    cellulare_VALORE.scrivere_Memoria(dati_e_mail + RICEV_SCAD_CONTA_NUMERI, VALORE); RICEV_SCAD_CONTA_NUMERI++;
                }
            }
            return RICEV_SCAD_CONTA_NUMERI;
        }
        int file = target[descrittore_VALORE], posizione = File_funzione[descrittore_VALORE];
        if (posizione >= Memoria_file_system.ridimensionare_elenco[file]) return 0;
        if (durata_VALORE > Memoria_file_system.ridimensionare_elenco[file] - posizione) durata_VALORE = Memoria_file_system.ridimensionare_elenco[file] - posizione;
        int 원본주소 = cellulare_VALORE.File_Memoria() + file * Memoria_file_system.최대크기 + posizione;
        for (int INDICE = 0; INDICE < durata_VALORE; INDICE++) cellulare_VALORE.scrivere_Memoria(dati_e_mail + INDICE, cellulare_VALORE.기억읽기(원본주소 + INDICE));
        File_funzione[descrittore_VALORE] += durata_VALORE;
        return durata_VALORE;
    }
    static int scrivere_File(int descrittore_voce, int dati_e_mail, int durata_VALORE) {
        int descrittore_VALORE = TROVA_descrittore(descrittore_voce);
        if (descrittore_VALORE < 0 || (aperto_Impostazioni[descrittore_VALORE] & 3) == 0) return -9;
        if (durata_VALORE < 0) return -22;
        if (durata_VALORE == 0) return 0;
        if (!esecuzione_manager.ritagliare(dati_e_mail, durata_VALORE)) return -14;
        if (Kind_VALORE[descrittore_VALORE] == 3) return -89; // 연결하지 않은 자료전문 종단점에는 meta_VALORE 주소가 필요하다.
        if (Kind_VALORE[descrittore_VALORE] == 1) {
            if (durata_VALORE > 16384) durata_VALORE = 16384;
            for (int INDICE = 0; INDICE < durata_VALORE; INDICE++) {
                int VALORE = cellulare_VALORE.기억읽기(dati_e_mail + INDICE);
                SMS_Terminale.seriale_byte(VALORE); SMS_Terminale.schermata_carattere(VALORE);
            }
            return durata_VALORE;
        }
        int file = target[descrittore_VALORE], Dimensione = Memoria_file_system.ridimensionare_elenco[file];
        int posizione = (aperto_Impostazioni[descrittore_VALORE] & 이어쓰기) != 0 ? Dimensione : File_funzione[descrittore_VALORE];
        if (posizione >= Memoria_file_system.최대크기) return -27;
        if (durata_VALORE > Memoria_file_system.최대크기 - posizione) durata_VALORE = Memoria_file_system.최대크기 - posizione;
        int meta_e_mail = cellulare_VALORE.File_Memoria() + file * Memoria_file_system.최대크기;
        for (int INDICE = Dimensione; INDICE < posizione; INDICE++) cellulare_VALORE.scrivere_Memoria(meta_e_mail + INDICE, 0);
        for (int INDICE = 0; INDICE < durata_VALORE; INDICE++) cellulare_VALORE.scrivere_Memoria(meta_e_mail + posizione + INDICE, cellulare_VALORE.기억읽기(dati_e_mail + INDICE));
        File_funzione[descrittore_VALORE] = posizione + durata_VALORE;
        if (posizione + durata_VALORE > Dimensione) Memoria_file_system.ridimensionare_elenco[file] = posizione + durata_VALORE;
        return durata_VALORE;
    }
    static int cercare_File(int descrittore_voce, int SCARTO_VALORE, int azione_radice) {
        int descrittore_VALORE = TROVA_descrittore(descrittore_voce);
        if (descrittore_VALORE < 0) return -9;
        if (Kind_VALORE[descrittore_VALORE] != 2) return -29;
        if (azione_radice < 0 || azione_radice > 2) return -22;
        int sfondo_VALORE = azione_radice == 0 ? 0 : (azione_radice == 1 ? File_funzione[descrittore_VALORE] : Memoria_file_system.ridimensionare_elenco[target[descrittore_VALORE]]);
        if (SCARTO_VALORE > 0 && sfondo_VALORE > 2147483647 - SCARTO_VALORE) return -75;
        if (SCARTO_VALORE < 0 && SCARTO_VALORE < -sfondo_VALORE) return -22;
        File_funzione[descrittore_VALORE] = sfondo_VALORE + SCARTO_VALORE;
        return File_funzione[descrittore_VALORE];
    }
    static int Duplica_descrittore(int descrittore_voce, int 새서술자, boolean Assegna_VALORE, int Impostazioni) {
        int descrittore_VALORE = TROVA_descrittore(descrittore_voce);
        if (descrittore_VALORE < 0) return -9;
        if (새서술자 < 0 || 새서술자 >= 서술자한도) return Assegna_VALORE ? -9 : -22;
        if (Assegna_VALORE && descrittore_voce == 새서술자) return 새서술자;
        if (Assegna_VALORE) { if (aperto_handle[새서술자] != 0) Chiudi_File(새서술자); }
        else { 새서술자 = vuota_descrittore(새서술자); if (새서술자 < 0) return 새서술자; }
        aperto_handle[새서술자] = descrittore_VALORE + 1; set_descrittore[새서술자] = Impostazioni; fonti_CONTA_NUMERI[descrittore_VALORE]++;
        return 새서술자;
    }
    static int rimuovere_File_voce_nome(int nome_e_mail) {
        int durata_VALORE = 경로읽기(nome_e_mail);
        if (durata_VALORE < 0) return durata_VALORE;
        int file = Memoria_file_system.TROVA_voce(percorso_nome, durata_VALORE);
        if (file < 0) return file;
        Memoria_file_system.이름들[file * 64] = 0;
        return 0;
    }
    static int set_File_durata(int descrittore_voce, int durata_VALORE) {
        int descrittore_VALORE = TROVA_descrittore(descrittore_voce);
        if (descrittore_VALORE < 0) return -9;
        if (Kind_VALORE[descrittore_VALORE] != 2 || (aperto_Impostazioni[descrittore_VALORE] & 3) == 0 || durata_VALORE < 0) return -22;
        if (durata_VALORE > Memoria_file_system.최대크기) return -27;
        int file = target[descrittore_VALORE], e_mail = cellulare_VALORE.File_Memoria() + file * Memoria_file_system.최대크기;
        for (int INDICE = Memoria_file_system.ridimensionare_elenco[file]; INDICE < durata_VALORE; INDICE++) cellulare_VALORE.scrivere_Memoria(e_mail + INDICE, 0);
        Memoria_file_system.ridimensionare_elenco[file] = durata_VALORE;
        return 0;
    }
    static int 파일상태읽기(int descrittore_voce, int e_mail) {
        int descrittore_VALORE = TROVA_descrittore(descrittore_voce);
        if (descrittore_VALORE < 0) return -9;
        if (!esecuzione_manager.ritagliare(e_mail, 48)) return -14;
        for (int INDICE = 0; INDICE < 12; INDICE++) esecuzione_manager.scrivere_numero(e_mail + INDICE * 4, 0);
        int file = target[descrittore_VALORE], Dimensione = Kind_VALORE[descrittore_VALORE] == 2 ? Memoria_file_system.ridimensionare_elenco[file] : 0;
        int concessione_privilegio = Kind_VALORE[descrittore_VALORE] == 2 ? Memoria_file_system.허가들[file] : 438;
        esecuzione_manager.scrivere_numero(e_mail, 1);
        esecuzione_manager.scrivere_numero(e_mail + 4, Kind_VALORE[descrittore_VALORE] == 2 ? file + 1 : 100 + descrittore_VALORE);
        esecuzione_manager.scrivere_numero(e_mail + 8, (Kind_VALORE[descrittore_VALORE] == 2 ? 32768 : (Kind_VALORE[descrittore_VALORE] == 1 ? 8192 : 49152)) | concessione_privilegio);
        esecuzione_manager.scrivere_numero(e_mail + 12, Kind_VALORE[descrittore_VALORE] == 2 && Memoria_file_system.이름들[file * 64] == 0 ? 0 : 1);
        esecuzione_manager.scrivere_numero(e_mail + 28, Dimensione); esecuzione_manager.scrivere_numero(e_mail + 32, 512);
        esecuzione_manager.scrivere_numero(e_mail + 36, (Dimensione + 511) / 512);
        return 0;
    }
    static int controllo_descrittore(int descrittore_voce, int comando, int VALORE) {
        int descrittore_VALORE = TROVA_descrittore(descrittore_voce);
        if (descrittore_VALORE < 0) return -9;
        if (comando == 0 || comando == 1030) return Duplica_descrittore(descrittore_voce, VALORE, false, comando == 1030 ? 1 : 0);
        if (comando == 1) return set_descrittore[descrittore_voce];
        if (comando == 2) { if ((VALORE & ~1) != 0) return -22; set_descrittore[descrittore_voce] = VALORE; return 0; }
        if (comando == 3) return aperto_Impostazioni[descrittore_VALORE];
        if (comando == 4) {
            if ((VALORE & ~(3 | 이어쓰기 | 기다리지않기)) != 0) return -95;
            aperto_Impostazioni[descrittore_VALORE] = (aperto_Impostazioni[descrittore_VALORE] & 3) | (VALORE & (이어쓰기 | 기다리지않기)); return 0;
        }
        return -95;
    }
    static int Crea_endpoint(int 주소체계, int rete_Kind, int caso_numero) {
        if (주소체계 != 2) return -97;
        if (rete_Kind != 2) return -93;
        if (caso_numero != 0 && caso_numero != 17) return -93;
        int descrittore_voce = vuota_descrittore(0), descrittore_VALORE = vuota_handle();
        if (descrittore_voce < 0 || descrittore_VALORE < 0) return -24;
        return Connetti(descrittore_voce, descrittore_VALORE, 3, 0, in_lettura_scrittura_flag);
    }
    static int endpoint_descrittore(int descrittore_voce) {
        int descrittore_VALORE = TROVA_descrittore(descrittore_voce);
        if (descrittore_VALORE < 0) return -9;
        return Kind_VALORE[descrittore_VALORE] == 3 ? descrittore_VALORE : -88;
    }
    static int e_mail_32(int e_mail) {
        return cellulare_VALORE.기억읽기(e_mail) << 24 | cellulare_VALORE.기억읽기(e_mail + 1) << 16
            | cellulare_VALORE.기억읽기(e_mail + 2) << 8 | cellulare_VALORE.기억읽기(e_mail + 3);
    }
    static int assegno_e_mail(int e_mail, int durata_VALORE) {
        if (durata_VALORE < 16) return -22;
        if (!esecuzione_manager.ritagliare(e_mail, 16)) return -14;
        return esecuzione_manager.짧은수(e_mail) == 2 ? 0 : -97;
    }
    static int BIND_e_mail(int descrittore_voce, int e_mail, int durata_VALORE) {
        int descrittore_VALORE = endpoint_descrittore(descrittore_voce);
        if (descrittore_VALORE < 0) return descrittore_VALORE;
        int risultato = assegno_e_mail(e_mail, durata_VALORE);
        if (risultato < 0) return risultato;
        if (rete_handle[descrittore_VALORE] != 0) return -22;
        int ID_rete = e_mail_32(e_mail + 4);
        if (ID_rete != 0 && ID_rete != rete_Pila.내주소) return -99;
        int numero_di_porta = cellulare_VALORE.기억읽기(e_mail + 2) << 8 | cellulare_VALORE.기억읽기(e_mail + 3);
        risultato = rete_Pila.Apri(numero_di_porta);
        if (risultato < 0) return risultato;
        rete_handle[descrittore_VALORE] = risultato; target[descrittore_VALORE] = ID_rete;
        return 0;
    }
    static int Auto_BIND(int descrittore_VALORE) {
        if (rete_handle[descrittore_VALORE] != 0) return 0;
        int risultato = rete_Pila.Apri(0);
        if (risultato < 0) return risultato;
        rete_handle[descrittore_VALORE] = risultato;
        return 0;
    }
    // sendto/recvfrom의 마지막 두 인자는 8바이트 richiesta 구조체로 전달한다.
    static int inviare_datagramma_dati(int descrittore_voce, int dati_e_mail, int durata_VALORE, int Impostazioni, int richiesto_e_mail) {
        int descrittore_VALORE = endpoint_descrittore(descrittore_voce);
        if (descrittore_VALORE < 0) return descrittore_VALORE;
        if (Impostazioni != 0) return -95;
        if (durata_VALORE < 0 || durata_VALORE > 1024) return -90;
        if (durata_VALORE != 0 && !esecuzione_manager.ritagliare(dati_e_mail, durata_VALORE)) return -14;
        if (!esecuzione_manager.ritagliare(richiesto_e_mail, 8)) return -14;
        int e_mail = esecuzione_manager.numero(richiesto_e_mail);
        int risultato = assegno_e_mail(e_mail, esecuzione_manager.numero(richiesto_e_mail + 4));
        if (risultato < 0) return risultato;
        int numero_di_porta = cellulare_VALORE.기억읽기(e_mail + 2) << 8 | cellulare_VALORE.기억읽기(e_mail + 3);
        if (numero_di_porta == 0) return -22;
        risultato = Auto_BIND(descrittore_VALORE);
        if (risultato < 0) return risultato;
        for (int INDICE = 0; INDICE < durata_VALORE; INDICE++) trasferire_dati[INDICE] = cellulare_VALORE.기억읽기(dati_e_mail + INDICE);
        return rete_Pila.inviare(rete_handle[descrittore_VALORE], e_mail_32(e_mail + 4), numero_di_porta, trasferire_dati, durata_VALORE);
    }
    static void scrivere_e_mail(int e_mail, int durata_VALORE, int ID_rete, int numero_di_porta) {
        for (int INDICE = 0; INDICE < durata_VALORE && INDICE < 16; INDICE++) {
            int VALORE = 0;
            if (INDICE == 0) VALORE = 2;
            if (INDICE == 2) VALORE = numero_di_porta >>> 8;
            if (INDICE == 3) VALORE = numero_di_porta;
            if (INDICE >= 4 && INDICE < 8) VALORE = ID_rete >>> (56 - INDICE * 8);
            cellulare_VALORE.scrivere_Memoria(e_mail + INDICE, VALORE & 255);
        }
    }
    static int ricevere_datagramma_dati(int descrittore_voce, int dati_e_mail, int durata_VALORE, int Impostazioni, int richiesto_e_mail) {
        int descrittore_VALORE = endpoint_descrittore(descrittore_voce);
        if (descrittore_VALORE < 0) return descrittore_VALORE;
        if ((Impostazioni & ~64) != 0) return -95;
        if (durata_VALORE < 0) return -22;
        if (durata_VALORE != 0 && !esecuzione_manager.ritagliare(dati_e_mail, durata_VALORE)) return -14;
        int e_mail = 0, e_mail_durata_e_mail = 0, e_mail_durata = 0;
        if (richiesto_e_mail != 0) {
            if (!esecuzione_manager.ritagliare(richiesto_e_mail, 8)) return -14;
            e_mail = esecuzione_manager.numero(richiesto_e_mail); e_mail_durata_e_mail = esecuzione_manager.numero(richiesto_e_mail + 4);
            if (e_mail != 0) {
                if (!esecuzione_manager.ritagliare(e_mail_durata_e_mail, 4)) return -14;
                e_mail_durata = esecuzione_manager.numero(e_mail_durata_e_mail);
                if (e_mail_durata < 0) return -22;
                if (!esecuzione_manager.ritagliare(e_mail, e_mail_durata < 16 ? e_mail_durata : 16)) return -14;
            }
        }
        int risultato = Auto_BIND(descrittore_VALORE);
        if (risultato < 0) return risultato;
        int avvia = cellulare_VALORE.밀리초();
        while (true) {
            risultato = rete_Pila.ricevere(rete_handle[descrittore_VALORE], trasferire_dati, 1024, 0);
            if (risultato != -11) break;
            if ((Impostazioni & 64) != 0 || (aperto_Impostazioni[descrittore_VALORE] & 기다리지않기) != 0) return -11;
            if (수신대기밀리초[descrittore_VALORE] > 0 && cellulare_VALORE.밀리초() - avvia >= 수신대기밀리초[descrittore_VALORE]) return -11;
            if (cellulare_VALORE.사용자남은밀리초() <= 10) return -11;
            cellulare_VALORE.잠시양보();
        }
        if (risultato < 0) return risultato;
        if (risultato > durata_VALORE) risultato = durata_VALORE;
        for (int INDICE = 0; INDICE < risultato; INDICE++) cellulare_VALORE.scrivere_Memoria(dati_e_mail + INDICE, trasferire_dati[INDICE]);
        if (e_mail != 0) {
            scrivere_e_mail(e_mail, e_mail_durata, rete_Pila.peer_e_mail(rete_handle[descrittore_VALORE]), rete_Pila.peer_numero_di_porta(rete_handle[descrittore_VALORE]));
            esecuzione_manager.scrivere_numero(e_mail_durata_e_mail, 16);
        }
        return risultato;
    }
    static int 통신주소읽기(int descrittore_voce, int e_mail, int durata_e_mail) {
        int descrittore_VALORE = endpoint_descrittore(descrittore_voce);
        if (descrittore_VALORE < 0) return descrittore_VALORE;
        if (!esecuzione_manager.ritagliare(durata_e_mail, 4)) return -14;
        int durata_VALORE = esecuzione_manager.numero(durata_e_mail);
        if (durata_VALORE < 0) return -22;
        if (!esecuzione_manager.ritagliare(e_mail, durata_VALORE < 16 ? durata_VALORE : 16)) return -14;
        int slot_voce = rete_Pila.INDICE(rete_handle[descrittore_VALORE]);
        scrivere_e_mail(e_mail, durata_VALORE, target[descrittore_VALORE], slot_voce < 0 ? 0 : rete_Pila.접속번호들[slot_voce]);
        esecuzione_manager.scrivere_numero(durata_e_mail, 16);
        return 0;
    }
    static int set_ricevere_TIMEOUT(int descrittore_voce, int 밀리초) {
        int descrittore_VALORE = endpoint_descrittore(descrittore_voce);
        if (descrittore_VALORE < 0) return descrittore_VALORE;
        if (밀리초 < 0 || 밀리초 > 2000) return -22;
        수신대기밀리초[descrittore_VALORE] = 밀리초;
        return 0;
    }
}
