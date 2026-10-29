// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** statisch_WAARDE IPv4/ARP/UDP. 최대 네 통신접속번호와 접속번호마다 한 데이터그램을 보관한다. */
public final class net_stack {
    static final int 내주소 = 0xc0a80064; /* ip.conf:IP */
    static final int net_masker = 0xffffff00; /* ip.conf:NETMASK */
    static final int gateway_WAARDE = 0xc0a80001; /* ip.conf:GATEWAY */
    static int[] invoer_frame = new int[1536], uitvoer_frame = new int[1536];
    static int[] 접속번호들 = new int[4], OPBRENGST_tijdsduur = new int[4], OPBRENGST_ADRES = new int[4], OPBRENGST_poortnummer = new int[4];
    static int[] OPBRENGST_gegevens = new int[4096], 찾은장치 = new int[6];
    static int 찾을주소 = 0, 찾은주소 = 0, id_WAARDE = 0, 폐기수 = 0;

    static int geheel_getal_16(int[] frame_INDEX, int positie) { return (frame_INDEX[positie] << 8) | frame_INDEX[positie + 1]; }
    static int geheel_getal_32(int[] frame_INDEX, int positie) { return (geheel_getal_16(frame_INDEX, positie) << 16) | geheel_getal_16(frame_INDEX, positie + 2); }
    static void 넣기16(int[] frame_INDEX, int positie, int WAARDE) { frame_INDEX[positie] = (WAARDE >>> 8) & 255; frame_INDEX[positie + 1] = WAARDE & 255; }
    static void 넣기32(int[] frame_INDEX, int positie, int WAARDE) { 넣기16(frame_INDEX, positie, WAARDE >>> 16); 넣기16(frame_INDEX, positie + 2, WAARDE); }
    static int SOM_WAARDE(int[] frame_INDEX, int starten, int tijdsduur_WAARDE, int WAARDE) {
        for (int INDEX = 0; INDEX < tijdsduur_WAARDE; INDEX += 2)
            WAARDE += (frame_INDEX[starten + INDEX] << 8) | (INDEX + 1 < tijdsduur_WAARDE ? frame_INDEX[starten + INDEX + 1] : 0);
        while ((WAARDE >>> 16) != 0) WAARDE = (WAARDE & 65535) + (WAARDE >>> 16);
        return WAARDE;
    }
    static int 가상머리합(int 출발, int 도착, int tijdsduur_WAARDE) {
        return (출발 >>> 16) + (출발 & 65535) + (도착 >>> 16) + (도착 & 65535) + 17 + tijdsduur_WAARDE;
    }

    static void Verscherpt_Proces() {
        for (int INDEX = 0; INDEX < 4; INDEX++) {
            접속번호들[INDEX] = 0; OPBRENGST_tijdsduur[INDEX] = -1; OPBRENGST_ADRES[INDEX] = 0; OPBRENGST_poortnummer[INDEX] = 0;
        }
        for (int INDEX = 0; INDEX < 64; INDEX++) if (net_stuurprogramma.ontvangen(invoer_frame) == 0) break;
    }
    static int INDEX(int greep_WAARDE) { return greep_WAARDE >= 3 && greep_WAARDE < 7 && 접속번호들[greep_WAARDE - 3] != 0 ? greep_WAARDE - 3 : -1; }
    static int Openen(int poortnummer) {
        if (net_stuurprogramma.입출력기준주소 == 0) return -19;
        if (poortnummer < 0 || poortnummer > 65535) return -22;
        if (poortnummer != 0) for (int INDEX = 0; INDEX < 4; INDEX++) if (접속번호들[INDEX] == poortnummer) return -98;
        for (int INDEX = 0; INDEX < 4; INDEX++) if (접속번호들[INDEX] == 0) {
            if (poortnummer == 0) {
                poortnummer = 49152;
                boolean 겹침 = true;
                while (겹침) {
                    겹침 = false;
                    for (int voorkant_WAARDE = 0; voorkant_WAARDE < 4; voorkant_WAARDE++) if (접속번호들[voorkant_WAARDE] == poortnummer) 겹침 = true;
                    if (겹침) poortnummer++;
                }
            }
            접속번호들[INDEX] = poortnummer; OPBRENGST_tijdsduur[INDEX] = -1;
            return INDEX + 3;
        }
        return -24;
    }
    static int Sluiten(int greep_WAARDE) {
        int sleuf_invoer = INDEX(greep_WAARDE);
        if (sleuf_invoer < 0) return -9;
        접속번호들[sleuf_invoer] = 0; OPBRENGST_tijdsduur[sleuf_invoer] = -1;
        return 0;
    }
    static int peer_ADRES(int greep_WAARDE) { int sleuf_invoer = INDEX(greep_WAARDE); return sleuf_invoer < 0 ? -9 : OPBRENGST_ADRES[sleuf_invoer]; }
    static int peer_poortnummer(int greep_WAARDE) { int sleuf_invoer = INDEX(greep_WAARDE); return sleuf_invoer < 0 ? -9 : OPBRENGST_poortnummer[sleuf_invoer]; }

    static void 바깥머리(int soort_WAARDE, boolean broadcast_WAARDE) {
        for (int INDEX = 0; INDEX < 6; INDEX++) {
            uitvoer_frame[INDEX] = broadcast_WAARDE ? 255 : 찾은장치[INDEX];
            uitvoer_frame[6 + INDEX] = net_stuurprogramma.mobiel_ADRES[INDEX];
        }
        넣기16(uitvoer_frame, 12, soort_WAARDE);
    }
    static void aanvraag_ADRES(int doel_WAARDE) {
        바깥머리(0x0806, true);
        넣기16(uitvoer_frame, 14, 1); 넣기16(uitvoer_frame, 16, 0x0800);
        uitvoer_frame[18] = 6; uitvoer_frame[19] = 4; 넣기16(uitvoer_frame, 20, 1);
        for (int INDEX = 0; INDEX < 6; INDEX++) {
            uitvoer_frame[22 + INDEX] = net_stuurprogramma.mobiel_ADRES[INDEX]; uitvoer_frame[32 + INDEX] = 0;
        }
        넣기32(uitvoer_frame, 28, 내주소); 넣기32(uitvoer_frame, 38, doel_WAARDE);
        net_stuurprogramma.e_mailen(uitvoer_frame, 42);
    }
    static void Proces_ADRES(int tijdsduur_WAARDE) {
        if (tijdsduur_WAARDE < 42 || geheel_getal_16(invoer_frame, 14) != 1 || geheel_getal_16(invoer_frame, 16) != 0x0800
            || invoer_frame[18] != 6 || invoer_frame[19] != 4 || geheel_getal_32(invoer_frame, 38) != 내주소) { 폐기수++; return; }
        int soort_WAARDE = geheel_getal_16(invoer_frame, 20), peer_WAARDE = geheel_getal_32(invoer_frame, 28);
        if (soort_WAARDE == 2 && peer_WAARDE == 찾을주소) {
            for (int INDEX = 0; INDEX < 6; INDEX++) {
                if (invoer_frame[6 + INDEX] != invoer_frame[22 + INDEX] || invoer_frame[32 + INDEX] != net_stuurprogramma.mobiel_ADRES[INDEX]) return;
            }
            for (int INDEX = 0; INDEX < 6; INDEX++) 찾은장치[INDEX] = invoer_frame[22 + INDEX];
            찾은주소 = peer_WAARDE;
        } else if (soort_WAARDE == 1) {
            바깥머리(0x0806, false);
            넣기16(uitvoer_frame, 14, 1); 넣기16(uitvoer_frame, 16, 0x0800);
            uitvoer_frame[18] = 6; uitvoer_frame[19] = 4; 넣기16(uitvoer_frame, 20, 2);
            for (int INDEX = 0; INDEX < 6; INDEX++) {
                uitvoer_frame[INDEX] = invoer_frame[22 + INDEX]; uitvoer_frame[32 + INDEX] = invoer_frame[22 + INDEX];
                uitvoer_frame[22 + INDEX] = net_stuurprogramma.mobiel_ADRES[INDEX];
            }
            넣기32(uitvoer_frame, 28, 내주소); 넣기32(uitvoer_frame, 38, peer_WAARDE);
            net_stuurprogramma.e_mailen(uitvoer_frame, 42);
        }
    }

    static void Proces_frame(int tijdsduur_WAARDE) {
        if (tijdsduur_WAARDE < 14 || tijdsduur_WAARDE > invoer_frame.length) { 폐기수++; return; }
        boolean 자기 = true, broadcast_WAARDE = true;
        for (int INDEX = 0; INDEX < 6; INDEX++) {
            if (invoer_frame[INDEX] != net_stuurprogramma.mobiel_ADRES[INDEX]) 자기 = false;
            if (invoer_frame[INDEX] != 255) broadcast_WAARDE = false;
        }
        if (!자기 && !broadcast_WAARDE) return;
        if (geheel_getal_16(invoer_frame, 12) == 0x0806) { Proces_ADRES(tijdsduur_WAARDE); return; }
        if (geheel_getal_16(invoer_frame, 12) != 0x0800) return;
        if (tijdsduur_WAARDE < 34 || (invoer_frame[14] >>> 4) != 4) { 폐기수++; return; }
        int header_tijdsduur = (invoer_frame[14] & 15) * 4, totaal_tijdsduur = geheel_getal_16(invoer_frame, 16);
        if (header_tijdsduur < 20 || header_tijdsduur > 60 || totaal_tijdsduur < header_tijdsduur + 8 || totaal_tijdsduur > tijdsduur_WAARDE - 14
            || (geheel_getal_16(invoer_frame, 20) & 0x3fff) != 0 || invoer_frame[23] != 17
            || geheel_getal_32(invoer_frame, 30) != 내주소 || SOM_WAARDE(invoer_frame, 14, header_tijdsduur, 0) != 65535) { 폐기수++; return; }
        int starten = 14 + header_tijdsduur, gegevens_tijdsduur = geheel_getal_16(invoer_frame, starten + 4);
        if (gegevens_tijdsduur < 8 || gegevens_tijdsduur != totaal_tijdsduur - header_tijdsduur || gegevens_tijdsduur > 1032) { 폐기수++; return; }
        int 출발 = geheel_getal_32(invoer_frame, 26);
        if (geheel_getal_16(invoer_frame, starten + 6) != 0 && SOM_WAARDE(invoer_frame, starten, gegevens_tijdsduur, 가상머리합(출발, 내주소, gegevens_tijdsduur)) != 65535) {
            폐기수++; return;
        }
        int doel_WAARDE = geheel_getal_16(invoer_frame, starten + 2);
        for (int sleuf_invoer = 0; sleuf_invoer < 4; sleuf_invoer++) if (접속번호들[sleuf_invoer] != 0 && 접속번호들[sleuf_invoer] == doel_WAARDE) {
            if (OPBRENGST_tijdsduur[sleuf_invoer] >= 0) { 폐기수++; return; }
            OPBRENGST_tijdsduur[sleuf_invoer] = gegevens_tijdsduur - 8; OPBRENGST_ADRES[sleuf_invoer] = 출발; OPBRENGST_poortnummer[sleuf_invoer] = geheel_getal_16(invoer_frame, starten);
            for (int INDEX = 0; INDEX < gegevens_tijdsduur - 8; INDEX++) OPBRENGST_gegevens[sleuf_invoer * 1024 + INDEX] = invoer_frame[starten + 8 + INDEX];
            return;
        }
    }

    static void bevestigen() {
        for (int INDEX = 0; INDEX < 16; INDEX++) {
            int tijdsduur_WAARDE = net_stuurprogramma.ontvangen(invoer_frame);
            if (tijdsduur_WAARDE == 0) return;
            Proces_frame(tijdsduur_WAARDE);
        }
    }
    static int Zoeken_ADRES(int ADRES) {
        if (ADRES == 0 || ADRES == -1 || (ADRES >>> 28) >= 14 || (ADRES >>> 24) == 127 || ADRES == 내주소) return -101;
        int Volgende_item = (ADRES & net_masker) == (내주소 & net_masker) ? ADRES : gateway_WAARDE;
        if (Volgende_item == 찾은주소) return 0;
        찾을주소 = Volgende_item;
        int starten = mobiel_WAARDE.밀리초(), Volgende_aanvraag = starten;
        while (mobiel_WAARDE.밀리초() - starten < 1000) {
            if (mobiel_WAARDE.밀리초() - Volgende_aanvraag >= 0) { aanvraag_ADRES(Volgende_item); Volgende_aanvraag += 300; }
            bevestigen();
            if (찾은주소 == Volgende_item) return 0;
            mobiel_WAARDE.잠시양보();
        }
        return -110;
    }
    static int e_mailen(int greep_WAARDE, int ADRES, int poortnummer, int[] gegevens, int tijdsduur_WAARDE) {
        int sleuf_invoer = INDEX(greep_WAARDE);
        if (sleuf_invoer < 0) return -9;
        if (net_stuurprogramma.입출력기준주소 == 0) return -19;
        if (poortnummer < 1 || poortnummer > 65535 || tijdsduur_WAARDE < 0 || tijdsduur_WAARDE > 1024) return -22;
        int resultaat = Zoeken_ADRES(ADRES);
        if (resultaat < 0) return resultaat;
        바깥머리(0x0800, false);
        uitvoer_frame[14] = 0x45; uitvoer_frame[15] = 0; 넣기16(uitvoer_frame, 16, 28 + tijdsduur_WAARDE);
        넣기16(uitvoer_frame, 18, id_WAARDE++); 넣기16(uitvoer_frame, 20, 0x4000);
        uitvoer_frame[22] = 64; uitvoer_frame[23] = 17; 넣기16(uitvoer_frame, 24, 0);
        넣기32(uitvoer_frame, 26, 내주소); 넣기32(uitvoer_frame, 30, ADRES);
        넣기16(uitvoer_frame, 24, ~SOM_WAARDE(uitvoer_frame, 14, 20, 0));
        넣기16(uitvoer_frame, 34, 접속번호들[sleuf_invoer]); 넣기16(uitvoer_frame, 36, poortnummer);
        넣기16(uitvoer_frame, 38, tijdsduur_WAARDE + 8); 넣기16(uitvoer_frame, 40, 0);
        for (int INDEX = 0; INDEX < tijdsduur_WAARDE; INDEX++) uitvoer_frame[42 + INDEX] = gegevens[INDEX] & 255;
        int controlesom = (~SOM_WAARDE(uitvoer_frame, 34, tijdsduur_WAARDE + 8, 가상머리합(내주소, ADRES, tijdsduur_WAARDE + 8))) & 65535;
        넣기16(uitvoer_frame, 40, controlesom == 0 ? 65535 : controlesom);
        resultaat = net_stuurprogramma.e_mailen(uitvoer_frame, tijdsduur_WAARDE + 42);
        return resultaat < 0 ? resultaat : tijdsduur_WAARDE;
    }
    static int ontvangen(int greep_WAARDE, int[] gegevens, int capaciteit_WAARDE, int 제한) {
        int sleuf_invoer = INDEX(greep_WAARDE);
        if (sleuf_invoer < 0) return -9;
        int starten = mobiel_WAARDE.밀리초();
        while (true) {
            bevestigen();
            int tijdsduur_WAARDE = OPBRENGST_tijdsduur[sleuf_invoer];
            if (tijdsduur_WAARDE >= 0) {
                OPBRENGST_tijdsduur[sleuf_invoer] = -1;
                if (tijdsduur_WAARDE > capaciteit_WAARDE) return -90;
                for (int INDEX = 0; INDEX < tijdsduur_WAARDE; INDEX++) gegevens[INDEX] = OPBRENGST_gegevens[sleuf_invoer * 1024 + INDEX];
                return tijdsduur_WAARDE;
            }
            if (제한 == 0) return -11;
            if (mobiel_WAARDE.밀리초() - starten >= 제한) return -110;
            mobiel_WAARDE.잠시양보();
        }
    }
    static void Status_WAARDE() {
        sms_Terminal.Schrijven(net_stuurprogramma.입출력기준주소 == 0 ? "NET unavailable (RTL8139 required)\n" : "NET RTL8139 192.168.0.100/24 gateway 192.168.0.1 UDP\n");
        sms_Terminal.Schrijven("TX: "); sms_Terminal.schrijven_nummer(net_stuurprogramma.송신수);
        sms_Terminal.Schrijven(" RX: "); sms_Terminal.schrijven_nummer(net_stuurprogramma.ontvangen_AANTAL);
        sms_Terminal.Schrijven(" DROP: "); sms_Terminal.schrijven_nummer(폐기수);
        sms_Terminal.Schrijven("\n");
    }
}
