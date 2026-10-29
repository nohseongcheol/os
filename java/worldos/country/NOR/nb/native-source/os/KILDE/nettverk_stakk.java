// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** statisk_VERDI IPv4/ARP/UDP. 최대 네 통신접속번호와 접속번호마다 한 데이터그램을 보관한다. */
public final class nettverk_stakk {
    static final int 내주소 = 0xc0a80064; /* ip.conf:IP */
    static final int nettverksmaske = 0xffffff00; /* ip.conf:NETMASK */
    static final int gateway_VERDI = 0xc0a80001; /* ip.conf:GATEWAY */
    static int[] inndata_bilde = new int[1536], produksjon_bilde = new int[1536];
    static int[] 접속번호들 = new int[4], MOTTATT_AVKAST_lengde = new int[4], MOTTATT_AVKAST_e_post = new int[4], MOTTATT_AVKAST_portnummer = new int[4];
    static int[] MOTTATT_AVKAST_data = new int[4096], 찾은장치 = new int[6];
    static int 찾을주소 = 0, 찾은주소 = 0, identifikator_VERDI = 0, 폐기수 = 0;

    static int heltall_16(int[] bilde_INDEKS, int Posisjon) { return (bilde_INDEKS[Posisjon] << 8) | bilde_INDEKS[Posisjon + 1]; }
    static int heltall_32(int[] bilde_INDEKS, int Posisjon) { return (heltall_16(bilde_INDEKS, Posisjon) << 16) | heltall_16(bilde_INDEKS, Posisjon + 2); }
    static void 넣기16(int[] bilde_INDEKS, int Posisjon, int VERDI) { bilde_INDEKS[Posisjon] = (VERDI >>> 8) & 255; bilde_INDEKS[Posisjon + 1] = VERDI & 255; }
    static void 넣기32(int[] bilde_INDEKS, int Posisjon, int VERDI) { 넣기16(bilde_INDEKS, Posisjon, VERDI >>> 16); 넣기16(bilde_INDEKS, Posisjon + 2, VERDI); }
    static int SUMMER_VERDI(int[] bilde_INDEKS, int Kjør_2, int lengde_VERDI, int VERDI) {
        for (int INDEKS = 0; INDEKS < lengde_VERDI; INDEKS += 2)
            VERDI += (bilde_INDEKS[Kjør_2 + INDEKS] << 8) | (INDEKS + 1 < lengde_VERDI ? bilde_INDEKS[Kjør_2 + INDEKS + 1] : 0);
        while ((VERDI >>> 16) != 0) VERDI = (VERDI & 65535) + (VERDI >>> 16);
        return VERDI;
    }
    static int 가상머리합(int 출발, int 도착, int lengde_VERDI) {
        return (출발 >>> 16) + (출발 & 65535) + (도착 >>> 16) + (도착 & 65535) + 17 + lengde_VERDI;
    }

    static void RENSK_Prosess() {
        for (int INDEKS = 0; INDEKS < 4; INDEKS++) {
            접속번호들[INDEKS] = 0; MOTTATT_AVKAST_lengde[INDEKS] = -1; MOTTATT_AVKAST_e_post[INDEKS] = 0; MOTTATT_AVKAST_portnummer[INDEKS] = 0;
        }
        for (int INDEKS = 0; INDEKS < 64; INDEKS++) if (nettverk_driver.motta(inndata_bilde) == 0) break;
    }
    static int INDEKS(int håndtak_VERDI) { return håndtak_VERDI >= 3 && håndtak_VERDI < 7 && 접속번호들[håndtak_VERDI - 3] != 0 ? håndtak_VERDI - 3 : -1; }
    static int Åpne(int portnummer) {
        if (nettverk_driver.입출력기준주소 == 0) return -19;
        if (portnummer < 0 || portnummer > 65535) return -22;
        if (portnummer != 0) for (int INDEKS = 0; INDEKS < 4; INDEKS++) if (접속번호들[INDEKS] == portnummer) return -98;
        for (int INDEKS = 0; INDEKS < 4; INDEKS++) if (접속번호들[INDEKS] == 0) {
            if (portnummer == 0) {
                portnummer = 49152;
                boolean 겹침 = true;
                while (겹침) {
                    겹침 = false;
                    for (int frontkamera_VERDI = 0; frontkamera_VERDI < 4; frontkamera_VERDI++) if (접속번호들[frontkamera_VERDI] == portnummer) 겹침 = true;
                    if (겹침) portnummer++;
                }
            }
            접속번호들[INDEKS] = portnummer; MOTTATT_AVKAST_lengde[INDEKS] = -1;
            return INDEKS + 3;
        }
        return -24;
    }
    static int Lukk(int håndtak_VERDI) {
        int åpning_oppføring = INDEKS(håndtak_VERDI);
        if (åpning_oppføring < 0) return -9;
        접속번호들[åpning_oppføring] = 0; MOTTATT_AVKAST_lengde[åpning_oppføring] = -1;
        return 0;
    }
    static int node_e_post(int håndtak_VERDI) { int åpning_oppføring = INDEKS(håndtak_VERDI); return åpning_oppføring < 0 ? -9 : MOTTATT_AVKAST_e_post[åpning_oppføring]; }
    static int node_portnummer(int håndtak_VERDI) { int åpning_oppføring = INDEKS(håndtak_VERDI); return åpning_oppføring < 0 ? -9 : MOTTATT_AVKAST_portnummer[åpning_oppføring]; }

    static void 바깥머리(int 종류, boolean kringkaste_VERDI) {
        for (int INDEKS = 0; INDEKS < 6; INDEKS++) {
            produksjon_bilde[INDEKS] = kringkaste_VERDI ? 255 : 찾은장치[INDEKS];
            produksjon_bilde[6 + INDEKS] = nettverk_driver.enhet_e_post[INDEKS];
        }
        넣기16(produksjon_bilde, 12, 종류);
    }
    static void forespørsel_e_post(int mål_VERDI) {
        바깥머리(0x0806, true);
        넣기16(produksjon_bilde, 14, 1); 넣기16(produksjon_bilde, 16, 0x0800);
        produksjon_bilde[18] = 6; produksjon_bilde[19] = 4; 넣기16(produksjon_bilde, 20, 1);
        for (int INDEKS = 0; INDEKS < 6; INDEKS++) {
            produksjon_bilde[22 + INDEKS] = nettverk_driver.enhet_e_post[INDEKS]; produksjon_bilde[32 + INDEKS] = 0;
        }
        넣기32(produksjon_bilde, 28, 내주소); 넣기32(produksjon_bilde, 38, mål_VERDI);
        nettverk_driver.sende(produksjon_bilde, 42);
    }
    static void Prosess_e_post(int lengde_VERDI) {
        if (lengde_VERDI < 42 || heltall_16(inndata_bilde, 14) != 1 || heltall_16(inndata_bilde, 16) != 0x0800
            || inndata_bilde[18] != 6 || inndata_bilde[19] != 4 || heltall_32(inndata_bilde, 38) != 내주소) { 폐기수++; return; }
        int 종류 = heltall_16(inndata_bilde, 20), node_VERDI_6a3b6fa7 = heltall_32(inndata_bilde, 28);
        if (종류 == 2 && node_VERDI_6a3b6fa7 == 찾을주소) {
            for (int INDEKS = 0; INDEKS < 6; INDEKS++) {
                if (inndata_bilde[6 + INDEKS] != inndata_bilde[22 + INDEKS] || inndata_bilde[32 + INDEKS] != nettverk_driver.enhet_e_post[INDEKS]) return;
            }
            for (int INDEKS = 0; INDEKS < 6; INDEKS++) 찾은장치[INDEKS] = inndata_bilde[22 + INDEKS];
            찾은주소 = node_VERDI_6a3b6fa7;
        } else if (종류 == 1) {
            바깥머리(0x0806, false);
            넣기16(produksjon_bilde, 14, 1); 넣기16(produksjon_bilde, 16, 0x0800);
            produksjon_bilde[18] = 6; produksjon_bilde[19] = 4; 넣기16(produksjon_bilde, 20, 2);
            for (int INDEKS = 0; INDEKS < 6; INDEKS++) {
                produksjon_bilde[INDEKS] = inndata_bilde[22 + INDEKS]; produksjon_bilde[32 + INDEKS] = inndata_bilde[22 + INDEKS];
                produksjon_bilde[22 + INDEKS] = nettverk_driver.enhet_e_post[INDEKS];
            }
            넣기32(produksjon_bilde, 28, 내주소); 넣기32(produksjon_bilde, 38, node_VERDI_6a3b6fa7);
            nettverk_driver.sende(produksjon_bilde, 42);
        }
    }

    static void Prosess_bilde(int lengde_VERDI) {
        if (lengde_VERDI < 14 || lengde_VERDI > inndata_bilde.length) { 폐기수++; return; }
        boolean 자기 = true, kringkaste_VERDI = true;
        for (int INDEKS = 0; INDEKS < 6; INDEKS++) {
            if (inndata_bilde[INDEKS] != nettverk_driver.enhet_e_post[INDEKS]) 자기 = false;
            if (inndata_bilde[INDEKS] != 255) kringkaste_VERDI = false;
        }
        if (!자기 && !kringkaste_VERDI) return;
        if (heltall_16(inndata_bilde, 12) == 0x0806) { Prosess_e_post(lengde_VERDI); return; }
        if (heltall_16(inndata_bilde, 12) != 0x0800) return;
        if (lengde_VERDI < 34 || (inndata_bilde[14] >>> 4) != 4) { 폐기수++; return; }
        int Topptekst_lengde = (inndata_bilde[14] & 15) * 4, total_lengde = heltall_16(inndata_bilde, 16);
        if (Topptekst_lengde < 20 || Topptekst_lengde > 60 || total_lengde < Topptekst_lengde + 8 || total_lengde > lengde_VERDI - 14
            || (heltall_16(inndata_bilde, 20) & 0x3fff) != 0 || inndata_bilde[23] != 17
            || heltall_32(inndata_bilde, 30) != 내주소 || SUMMER_VERDI(inndata_bilde, 14, Topptekst_lengde, 0) != 65535) { 폐기수++; return; }
        int Kjør_2 = 14 + Topptekst_lengde, data_lengde = heltall_16(inndata_bilde, Kjør_2 + 4);
        if (data_lengde < 8 || data_lengde != total_lengde - Topptekst_lengde || data_lengde > 1032) { 폐기수++; return; }
        int 출발 = heltall_32(inndata_bilde, 26);
        if (heltall_16(inndata_bilde, Kjør_2 + 6) != 0 && SUMMER_VERDI(inndata_bilde, Kjør_2, data_lengde, 가상머리합(출발, 내주소, data_lengde)) != 65535) {
            폐기수++; return;
        }
        int mål_VERDI = heltall_16(inndata_bilde, Kjør_2 + 2);
        for (int åpning_oppføring = 0; åpning_oppføring < 4; åpning_oppføring++) if (접속번호들[åpning_oppføring] != 0 && 접속번호들[åpning_oppføring] == mål_VERDI) {
            if (MOTTATT_AVKAST_lengde[åpning_oppføring] >= 0) { 폐기수++; return; }
            MOTTATT_AVKAST_lengde[åpning_oppføring] = data_lengde - 8; MOTTATT_AVKAST_e_post[åpning_oppføring] = 출발; MOTTATT_AVKAST_portnummer[åpning_oppføring] = heltall_16(inndata_bilde, Kjør_2);
            for (int INDEKS = 0; INDEKS < data_lengde - 8; INDEKS++) MOTTATT_AVKAST_data[åpning_oppføring * 1024 + INDEKS] = inndata_bilde[Kjør_2 + 8 + INDEKS];
            return;
        }
    }

    static void bekrefte() {
        for (int INDEKS = 0; INDEKS < 16; INDEKS++) {
            int lengde_VERDI = nettverk_driver.motta(inndata_bilde);
            if (lengde_VERDI == 0) return;
            Prosess_bilde(lengde_VERDI);
        }
    }
    static int Søk_e_post(int e_post) {
        if (e_post == 0 || e_post == -1 || (e_post >>> 28) >= 14 || (e_post >>> 24) == 127 || e_post == 내주소) return -101;
        int Neste_vare = (e_post & nettverksmaske) == (내주소 & nettverksmaske) ? e_post : gateway_VERDI;
        if (Neste_vare == 찾은주소) return 0;
        찾을주소 = Neste_vare;
        int Kjør_2 = enhet_VERDI.밀리초(), Neste_forespørsel = Kjør_2;
        while (enhet_VERDI.밀리초() - Kjør_2 < 1000) {
            if (enhet_VERDI.밀리초() - Neste_forespørsel >= 0) { forespørsel_e_post(Neste_vare); Neste_forespørsel += 300; }
            bekrefte();
            if (찾은주소 == Neste_vare) return 0;
            enhet_VERDI.잠시양보();
        }
        return -110;
    }
    static int sende(int håndtak_VERDI, int e_post, int portnummer, int[] data, int lengde_VERDI) {
        int åpning_oppføring = INDEKS(håndtak_VERDI);
        if (åpning_oppføring < 0) return -9;
        if (nettverk_driver.입출력기준주소 == 0) return -19;
        if (portnummer < 1 || portnummer > 65535 || lengde_VERDI < 0 || lengde_VERDI > 1024) return -22;
        int KR = Søk_e_post(e_post);
        if (KR < 0) return KR;
        바깥머리(0x0800, false);
        produksjon_bilde[14] = 0x45; produksjon_bilde[15] = 0; 넣기16(produksjon_bilde, 16, 28 + lengde_VERDI);
        넣기16(produksjon_bilde, 18, identifikator_VERDI++); 넣기16(produksjon_bilde, 20, 0x4000);
        produksjon_bilde[22] = 64; produksjon_bilde[23] = 17; 넣기16(produksjon_bilde, 24, 0);
        넣기32(produksjon_bilde, 26, 내주소); 넣기32(produksjon_bilde, 30, e_post);
        넣기16(produksjon_bilde, 24, ~SUMMER_VERDI(produksjon_bilde, 14, 20, 0));
        넣기16(produksjon_bilde, 34, 접속번호들[åpning_oppføring]); 넣기16(produksjon_bilde, 36, portnummer);
        넣기16(produksjon_bilde, 38, lengde_VERDI + 8); 넣기16(produksjon_bilde, 40, 0);
        for (int INDEKS = 0; INDEKS < lengde_VERDI; INDEKS++) produksjon_bilde[42 + INDEKS] = data[INDEKS] & 255;
        int kontrollsum = (~SUMMER_VERDI(produksjon_bilde, 34, lengde_VERDI + 8, 가상머리합(내주소, e_post, lengde_VERDI + 8))) & 65535;
        넣기16(produksjon_bilde, 40, kontrollsum == 0 ? 65535 : kontrollsum);
        KR = nettverk_driver.sende(produksjon_bilde, lengde_VERDI + 42);
        return KR < 0 ? KR : lengde_VERDI;
    }
    static int motta(int håndtak_VERDI, int[] data, int kapasitet_VERDI, int 제한) {
        int åpning_oppføring = INDEKS(håndtak_VERDI);
        if (åpning_oppføring < 0) return -9;
        int Kjør_2 = enhet_VERDI.밀리초();
        while (true) {
            bekrefte();
            int lengde_VERDI = MOTTATT_AVKAST_lengde[åpning_oppføring];
            if (lengde_VERDI >= 0) {
                MOTTATT_AVKAST_lengde[åpning_oppføring] = -1;
                if (lengde_VERDI > kapasitet_VERDI) return -90;
                for (int INDEKS = 0; INDEKS < lengde_VERDI; INDEKS++) data[INDEKS] = MOTTATT_AVKAST_data[åpning_oppføring * 1024 + INDEKS];
                return lengde_VERDI;
            }
            if (제한 == 0) return -11;
            if (enhet_VERDI.밀리초() - Kjør_2 >= 제한) return -110;
            enhet_VERDI.잠시양보();
        }
    }
    static void status_VERDI() {
        SMS_Terminal.Skriv(nettverk_driver.입출력기준주소 == 0 ? "NET unavailable (RTL8139 required)\n" : "NET RTL8139 192.168.0.100/24 gateway 192.168.0.1 UDP\n");
        SMS_Terminal.Skriv("TX: "); SMS_Terminal.skrive_nummer(nettverk_driver.송신수);
        SMS_Terminal.Skriv(" RX: "); SMS_Terminal.skrive_nummer(nettverk_driver.motta_ANTALL);
        SMS_Terminal.Skriv(" DROP: "); SMS_Terminal.skrive_nummer(폐기수);
        SMS_Terminal.Skriv("\n");
    }
}
