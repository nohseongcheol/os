// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** statico_VALORE IPv4/ARP/UDP. 최대 네 통신접속번호와 접속번호마다 한 데이터그램을 보관한다. */
public final class rete_Pila {
    static final int 내주소 = 0xc0a80064; /* ip.conf:IP */
    static final int network_mask = 0xffffff00; /* ip.conf:NETMASK */
    static final int gateway_VALORE = 0xc0a80001; /* ip.conf:GATEWAY */
    static int[] input_frame = new int[1536], output_frame = new int[1536];
    static int[] 접속번호들 = new int[4], RICEV_SCAD_durata = new int[4], RICEV_SCAD_e_mail = new int[4], RICEV_SCAD_numero_di_porta = new int[4];
    static int[] RICEV_SCAD_dati = new int[4096], 찾은장치 = new int[6];
    static int 찾을주소 = 0, 찾은주소 = 0, identificatore_VALORE = 0, 폐기수 = 0;

    static int intero_16(int[] frame_INDICE, int posizione) { return (frame_INDICE[posizione] << 8) | frame_INDICE[posizione + 1]; }
    static int intero_32(int[] frame_INDICE, int posizione) { return (intero_16(frame_INDICE, posizione) << 16) | intero_16(frame_INDICE, posizione + 2); }
    static void 넣기16(int[] frame_INDICE, int posizione, int VALORE) { frame_INDICE[posizione] = (VALORE >>> 8) & 255; frame_INDICE[posizione + 1] = VALORE & 255; }
    static void 넣기32(int[] frame_INDICE, int posizione, int VALORE) { 넣기16(frame_INDICE, posizione, VALORE >>> 16); 넣기16(frame_INDICE, posizione + 2, VALORE); }
    static int SUM_VALORE(int[] frame_INDICE, int avvia, int durata_VALORE, int VALORE) {
        for (int INDICE = 0; INDICE < durata_VALORE; INDICE += 2)
            VALORE += (frame_INDICE[avvia + INDICE] << 8) | (INDICE + 1 < durata_VALORE ? frame_INDICE[avvia + INDICE + 1] : 0);
        while ((VALORE >>> 16) != 0) VALORE = (VALORE & 65535) + (VALORE >>> 16);
        return VALORE;
    }
    static int 가상머리합(int 출발, int 도착, int durata_VALORE) {
        return (출발 >>> 16) + (출발 & 65535) + (도착 >>> 16) + (도착 & 65535) + 17 + durata_VALORE;
    }

    static void LIBERA_Processi() {
        for (int INDICE = 0; INDICE < 4; INDICE++) {
            접속번호들[INDICE] = 0; RICEV_SCAD_durata[INDICE] = -1; RICEV_SCAD_e_mail[INDICE] = 0; RICEV_SCAD_numero_di_porta[INDICE] = 0;
        }
        for (int INDICE = 0; INDICE < 64; INDICE++) if (rete_driver.ricevere(input_frame) == 0) break;
    }
    static int INDICE(int handle_VALORE) { return handle_VALORE >= 3 && handle_VALORE < 7 && 접속번호들[handle_VALORE - 3] != 0 ? handle_VALORE - 3 : -1; }
    static int Apri(int numero_di_porta) {
        if (rete_driver.입출력기준주소 == 0) return -19;
        if (numero_di_porta < 0 || numero_di_porta > 65535) return -22;
        if (numero_di_porta != 0) for (int INDICE = 0; INDICE < 4; INDICE++) if (접속번호들[INDICE] == numero_di_porta) return -98;
        for (int INDICE = 0; INDICE < 4; INDICE++) if (접속번호들[INDICE] == 0) {
            if (numero_di_porta == 0) {
                numero_di_porta = 49152;
                boolean 겹침 = true;
                while (겹침) {
                    겹침 = false;
                    for (int frontale_VALORE = 0; frontale_VALORE < 4; frontale_VALORE++) if (접속번호들[frontale_VALORE] == numero_di_porta) 겹침 = true;
                    if (겹침) numero_di_porta++;
                }
            }
            접속번호들[INDICE] = numero_di_porta; RICEV_SCAD_durata[INDICE] = -1;
            return INDICE + 3;
        }
        return -24;
    }
    static int Chiudi(int handle_VALORE) {
        int slot_voce = INDICE(handle_VALORE);
        if (slot_voce < 0) return -9;
        접속번호들[slot_voce] = 0; RICEV_SCAD_durata[slot_voce] = -1;
        return 0;
    }
    static int peer_e_mail(int handle_VALORE) { int slot_voce = INDICE(handle_VALORE); return slot_voce < 0 ? -9 : RICEV_SCAD_e_mail[slot_voce]; }
    static int peer_numero_di_porta(int handle_VALORE) { int slot_voce = INDICE(handle_VALORE); return slot_voce < 0 ? -9 : RICEV_SCAD_numero_di_porta[slot_voce]; }

    static void 바깥머리(int Kind_VALORE, boolean trasmesso_VALORE) {
        for (int INDICE = 0; INDICE < 6; INDICE++) {
            output_frame[INDICE] = trasmesso_VALORE ? 255 : 찾은장치[INDICE];
            output_frame[6 + INDICE] = rete_driver.cellulare_e_mail[INDICE];
        }
        넣기16(output_frame, 12, Kind_VALORE);
    }
    static void richiesta_e_mail(int meta_VALORE) {
        바깥머리(0x0806, true);
        넣기16(output_frame, 14, 1); 넣기16(output_frame, 16, 0x0800);
        output_frame[18] = 6; output_frame[19] = 4; 넣기16(output_frame, 20, 1);
        for (int INDICE = 0; INDICE < 6; INDICE++) {
            output_frame[22 + INDICE] = rete_driver.cellulare_e_mail[INDICE]; output_frame[32 + INDICE] = 0;
        }
        넣기32(output_frame, 28, 내주소); 넣기32(output_frame, 38, meta_VALORE);
        rete_driver.inviare(output_frame, 42);
    }
    static void Processi_e_mail(int durata_VALORE) {
        if (durata_VALORE < 42 || intero_16(input_frame, 14) != 1 || intero_16(input_frame, 16) != 0x0800
            || input_frame[18] != 6 || input_frame[19] != 4 || intero_32(input_frame, 38) != 내주소) { 폐기수++; return; }
        int Kind_VALORE = intero_16(input_frame, 20), peer_VALORE = intero_32(input_frame, 28);
        if (Kind_VALORE == 2 && peer_VALORE == 찾을주소) {
            for (int INDICE = 0; INDICE < 6; INDICE++) {
                if (input_frame[6 + INDICE] != input_frame[22 + INDICE] || input_frame[32 + INDICE] != rete_driver.cellulare_e_mail[INDICE]) return;
            }
            for (int INDICE = 0; INDICE < 6; INDICE++) 찾은장치[INDICE] = input_frame[22 + INDICE];
            찾은주소 = peer_VALORE;
        } else if (Kind_VALORE == 1) {
            바깥머리(0x0806, false);
            넣기16(output_frame, 14, 1); 넣기16(output_frame, 16, 0x0800);
            output_frame[18] = 6; output_frame[19] = 4; 넣기16(output_frame, 20, 2);
            for (int INDICE = 0; INDICE < 6; INDICE++) {
                output_frame[INDICE] = input_frame[22 + INDICE]; output_frame[32 + INDICE] = input_frame[22 + INDICE];
                output_frame[22 + INDICE] = rete_driver.cellulare_e_mail[INDICE];
            }
            넣기32(output_frame, 28, 내주소); 넣기32(output_frame, 38, peer_VALORE);
            rete_driver.inviare(output_frame, 42);
        }
    }

    static void Processi_frame(int durata_VALORE) {
        if (durata_VALORE < 14 || durata_VALORE > input_frame.length) { 폐기수++; return; }
        boolean 자기 = true, trasmesso_VALORE = true;
        for (int INDICE = 0; INDICE < 6; INDICE++) {
            if (input_frame[INDICE] != rete_driver.cellulare_e_mail[INDICE]) 자기 = false;
            if (input_frame[INDICE] != 255) trasmesso_VALORE = false;
        }
        if (!자기 && !trasmesso_VALORE) return;
        if (intero_16(input_frame, 12) == 0x0806) { Processi_e_mail(durata_VALORE); return; }
        if (intero_16(input_frame, 12) != 0x0800) return;
        if (durata_VALORE < 34 || (input_frame[14] >>> 4) != 4) { 폐기수++; return; }
        int Intestazione_durata = (input_frame[14] & 15) * 4, totale_durata = intero_16(input_frame, 16);
        if (Intestazione_durata < 20 || Intestazione_durata > 60 || totale_durata < Intestazione_durata + 8 || totale_durata > durata_VALORE - 14
            || (intero_16(input_frame, 20) & 0x3fff) != 0 || input_frame[23] != 17
            || intero_32(input_frame, 30) != 내주소 || SUM_VALORE(input_frame, 14, Intestazione_durata, 0) != 65535) { 폐기수++; return; }
        int avvia = 14 + Intestazione_durata, dati_durata = intero_16(input_frame, avvia + 4);
        if (dati_durata < 8 || dati_durata != totale_durata - Intestazione_durata || dati_durata > 1032) { 폐기수++; return; }
        int 출발 = intero_32(input_frame, 26);
        if (intero_16(input_frame, avvia + 6) != 0 && SUM_VALORE(input_frame, avvia, dati_durata, 가상머리합(출발, 내주소, dati_durata)) != 65535) {
            폐기수++; return;
        }
        int meta_VALORE = intero_16(input_frame, avvia + 2);
        for (int slot_voce = 0; slot_voce < 4; slot_voce++) if (접속번호들[slot_voce] != 0 && 접속번호들[slot_voce] == meta_VALORE) {
            if (RICEV_SCAD_durata[slot_voce] >= 0) { 폐기수++; return; }
            RICEV_SCAD_durata[slot_voce] = dati_durata - 8; RICEV_SCAD_e_mail[slot_voce] = 출발; RICEV_SCAD_numero_di_porta[slot_voce] = intero_16(input_frame, avvia);
            for (int INDICE = 0; INDICE < dati_durata - 8; INDICE++) RICEV_SCAD_dati[slot_voce * 1024 + INDICE] = input_frame[avvia + 8 + INDICE];
            return;
        }
    }

    static void verificare() {
        for (int INDICE = 0; INDICE < 16; INDICE++) {
            int durata_VALORE = rete_driver.ricevere(input_frame);
            if (durata_VALORE == 0) return;
            Processi_frame(durata_VALORE);
        }
    }
    static int TROVA_e_mail(int e_mail) {
        if (e_mail == 0 || e_mail == -1 || (e_mail >>> 28) >= 14 || (e_mail >>> 24) == 127 || e_mail == 내주소) return -101;
        int Avanti_articolo = (e_mail & network_mask) == (내주소 & network_mask) ? e_mail : gateway_VALORE;
        if (Avanti_articolo == 찾은주소) return 0;
        찾을주소 = Avanti_articolo;
        int avvia = cellulare_VALORE.밀리초(), Avanti_richiesta = avvia;
        while (cellulare_VALORE.밀리초() - avvia < 1000) {
            if (cellulare_VALORE.밀리초() - Avanti_richiesta >= 0) { richiesta_e_mail(Avanti_articolo); Avanti_richiesta += 300; }
            verificare();
            if (찾은주소 == Avanti_articolo) return 0;
            cellulare_VALORE.잠시양보();
        }
        return -110;
    }
    static int inviare(int handle_VALORE, int e_mail, int numero_di_porta, int[] dati, int durata_VALORE) {
        int slot_voce = INDICE(handle_VALORE);
        if (slot_voce < 0) return -9;
        if (rete_driver.입출력기준주소 == 0) return -19;
        if (numero_di_porta < 1 || numero_di_porta > 65535 || durata_VALORE < 0 || durata_VALORE > 1024) return -22;
        int risultato = TROVA_e_mail(e_mail);
        if (risultato < 0) return risultato;
        바깥머리(0x0800, false);
        output_frame[14] = 0x45; output_frame[15] = 0; 넣기16(output_frame, 16, 28 + durata_VALORE);
        넣기16(output_frame, 18, identificatore_VALORE++); 넣기16(output_frame, 20, 0x4000);
        output_frame[22] = 64; output_frame[23] = 17; 넣기16(output_frame, 24, 0);
        넣기32(output_frame, 26, 내주소); 넣기32(output_frame, 30, e_mail);
        넣기16(output_frame, 24, ~SUM_VALORE(output_frame, 14, 20, 0));
        넣기16(output_frame, 34, 접속번호들[slot_voce]); 넣기16(output_frame, 36, numero_di_porta);
        넣기16(output_frame, 38, durata_VALORE + 8); 넣기16(output_frame, 40, 0);
        for (int INDICE = 0; INDICE < durata_VALORE; INDICE++) output_frame[42 + INDICE] = dati[INDICE] & 255;
        int checksum = (~SUM_VALORE(output_frame, 34, durata_VALORE + 8, 가상머리합(내주소, e_mail, durata_VALORE + 8))) & 65535;
        넣기16(output_frame, 40, checksum == 0 ? 65535 : checksum);
        risultato = rete_driver.inviare(output_frame, durata_VALORE + 42);
        return risultato < 0 ? risultato : durata_VALORE;
    }
    static int ricevere(int handle_VALORE, int[] dati, int capacità_VALORE, int 제한) {
        int slot_voce = INDICE(handle_VALORE);
        if (slot_voce < 0) return -9;
        int avvia = cellulare_VALORE.밀리초();
        while (true) {
            verificare();
            int durata_VALORE = RICEV_SCAD_durata[slot_voce];
            if (durata_VALORE >= 0) {
                RICEV_SCAD_durata[slot_voce] = -1;
                if (durata_VALORE > capacità_VALORE) return -90;
                for (int INDICE = 0; INDICE < durata_VALORE; INDICE++) dati[INDICE] = RICEV_SCAD_dati[slot_voce * 1024 + INDICE];
                return durata_VALORE;
            }
            if (제한 == 0) return -11;
            if (cellulare_VALORE.밀리초() - avvia >= 제한) return -110;
            cellulare_VALORE.잠시양보();
        }
    }
    static void Stato_VALORE() {
        SMS_Terminale.Scrittura(rete_driver.입출력기준주소 == 0 ? "NET unavailable (RTL8139 required)\n" : "NET RTL8139 192.168.0.100/24 gateway 192.168.0.1 UDP\n");
        SMS_Terminale.Scrittura("TX: "); SMS_Terminale.scrivere_numero(rete_driver.trasmettere_CONTA_NUMERI);
        SMS_Terminale.Scrittura(" RX: "); SMS_Terminale.scrivere_numero(rete_driver.ricevere_CONTA_NUMERI);
        SMS_Terminale.Scrittura(" DROP: "); SMS_Terminale.scrivere_numero(폐기수);
        SMS_Terminale.Scrittura("\n");
    }
}
