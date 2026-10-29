// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** statisk_VÆRDI IPv4/ARP/UDP. 최대 네 통신접속번호와 접속번호마다 한 데이터그램을 보관한다. */
public final class netværk_Stak {
    static final int 내주소 = 0xc0a80064; /* ip.conf:IP */
    static final int netværksmaske = 0xffffff00; /* ip.conf:NETMASK */
    static final int gateway_VÆRDI = 0xc0a80001; /* ip.conf:GATEWAY */
    static int[] input_ramme = new int[1536], produktoutput_ramme = new int[1536];
    static int[] 접속번호들 = new int[4], MODTAGET_VED_UDLØB_varighed = new int[4], MODTAGET_VED_UDLØB_mail = new int[4], MODTAGET_VED_UDLØB_portnummer = new int[4];
    static int[] MODTAGET_VED_UDLØB_data = new int[4096], 찾은장치 = new int[6];
    static int 찾을주소 = 0, 찾은주소 = 0, identifikator_VÆRDI = 0, 폐기수 = 0;

    static int heltal_16(int[] ramme_INDEKS, int Placering) { return (ramme_INDEKS[Placering] << 8) | ramme_INDEKS[Placering + 1]; }
    static int heltal_32(int[] ramme_INDEKS, int Placering) { return (heltal_16(ramme_INDEKS, Placering) << 16) | heltal_16(ramme_INDEKS, Placering + 2); }
    static void 넣기16(int[] ramme_INDEKS, int Placering, int VÆRDI) { ramme_INDEKS[Placering] = (VÆRDI >>> 8) & 255; ramme_INDEKS[Placering + 1] = VÆRDI & 255; }
    static void 넣기32(int[] ramme_INDEKS, int Placering, int VÆRDI) { 넣기16(ramme_INDEKS, Placering, VÆRDI >>> 16); 넣기16(ramme_INDEKS, Placering + 2, VÆRDI); }
    static int SUM_VÆRDI(int[] ramme_INDEKS, int Kør_2, int varighed_VÆRDI, int VÆRDI) {
        for (int INDEKS = 0; INDEKS < varighed_VÆRDI; INDEKS += 2)
            VÆRDI += (ramme_INDEKS[Kør_2 + INDEKS] << 8) | (INDEKS + 1 < varighed_VÆRDI ? ramme_INDEKS[Kør_2 + INDEKS + 1] : 0);
        while ((VÆRDI >>> 16) != 0) VÆRDI = (VÆRDI & 65535) + (VÆRDI >>> 16);
        return VÆRDI;
    }
    static int 가상머리합(int 출발, int 도착, int varighed_VÆRDI) {
        return (출발 >>> 16) + (출발 & 65535) + (도착 >>> 16) + (도착 & 65535) + 17 + varighed_VÆRDI;
    }

    static void Ren_Proces() {
        for (int INDEKS = 0; INDEKS < 4; INDEKS++) {
            접속번호들[INDEKS] = 0; MODTAGET_VED_UDLØB_varighed[INDEKS] = -1; MODTAGET_VED_UDLØB_mail[INDEKS] = 0; MODTAGET_VED_UDLØB_portnummer[INDEKS] = 0;
        }
        for (int INDEKS = 0; INDEKS < 64; INDEKS++) if (netværk_driver.modtage(input_ramme) == 0) break;
    }
    static int INDEKS(int handle_VÆRDI) { return handle_VÆRDI >= 3 && handle_VÆRDI < 7 && 접속번호들[handle_VÆRDI - 3] != 0 ? handle_VÆRDI - 3 : -1; }
    static int Åbn(int portnummer) {
        if (netværk_driver.입출력기준주소 == 0) return -19;
        if (portnummer < 0 || portnummer > 65535) return -22;
        if (portnummer != 0) for (int INDEKS = 0; INDEKS < 4; INDEKS++) if (접속번호들[INDEKS] == portnummer) return -98;
        for (int INDEKS = 0; INDEKS < 4; INDEKS++) if (접속번호들[INDEKS] == 0) {
            if (portnummer == 0) {
                portnummer = 49152;
                boolean 겹침 = true;
                while (겹침) {
                    겹침 = false;
                    for (int frontvendt_VÆRDI = 0; frontvendt_VÆRDI < 4; frontvendt_VÆRDI++) if (접속번호들[frontvendt_VÆRDI] == portnummer) 겹침 = true;
                    if (겹침) portnummer++;
                }
            }
            접속번호들[INDEKS] = portnummer; MODTAGET_VED_UDLØB_varighed[INDEKS] = -1;
            return INDEKS + 3;
        }
        return -24;
    }
    static int Luk(int handle_VÆRDI) {
        int udvidelsesstik_post = INDEKS(handle_VÆRDI);
        if (udvidelsesstik_post < 0) return -9;
        접속번호들[udvidelsesstik_post] = 0; MODTAGET_VED_UDLØB_varighed[udvidelsesstik_post] = -1;
        return 0;
    }
    static int peer_mail(int handle_VÆRDI) { int udvidelsesstik_post = INDEKS(handle_VÆRDI); return udvidelsesstik_post < 0 ? -9 : MODTAGET_VED_UDLØB_mail[udvidelsesstik_post]; }
    static int peer_portnummer(int handle_VÆRDI) { int udvidelsesstik_post = INDEKS(handle_VÆRDI); return udvidelsesstik_post < 0 ? -9 : MODTAGET_VED_UDLØB_portnummer[udvidelsesstik_post]; }

    static void 바깥머리(int 종류, boolean udsende_VÆRDI) {
        for (int INDEKS = 0; INDEKS < 6; INDEKS++) {
            produktoutput_ramme[INDEKS] = udsende_VÆRDI ? 255 : 찾은장치[INDEKS];
            produktoutput_ramme[6 + INDEKS] = netværk_driver.enhed_mail[INDEKS];
        }
        넣기16(produktoutput_ramme, 12, 종류);
    }
    static void anmodning_mail(int destination_VÆRDI) {
        바깥머리(0x0806, true);
        넣기16(produktoutput_ramme, 14, 1); 넣기16(produktoutput_ramme, 16, 0x0800);
        produktoutput_ramme[18] = 6; produktoutput_ramme[19] = 4; 넣기16(produktoutput_ramme, 20, 1);
        for (int INDEKS = 0; INDEKS < 6; INDEKS++) {
            produktoutput_ramme[22 + INDEKS] = netværk_driver.enhed_mail[INDEKS]; produktoutput_ramme[32 + INDEKS] = 0;
        }
        넣기32(produktoutput_ramme, 28, 내주소); 넣기32(produktoutput_ramme, 38, destination_VÆRDI);
        netværk_driver.maile(produktoutput_ramme, 42);
    }
    static void Proces_mail(int varighed_VÆRDI) {
        if (varighed_VÆRDI < 42 || heltal_16(input_ramme, 14) != 1 || heltal_16(input_ramme, 16) != 0x0800
            || input_ramme[18] != 6 || input_ramme[19] != 4 || heltal_32(input_ramme, 38) != 내주소) { 폐기수++; return; }
        int 종류 = heltal_16(input_ramme, 20), peer_VÆRDI = heltal_32(input_ramme, 28);
        if (종류 == 2 && peer_VÆRDI == 찾을주소) {
            for (int INDEKS = 0; INDEKS < 6; INDEKS++) {
                if (input_ramme[6 + INDEKS] != input_ramme[22 + INDEKS] || input_ramme[32 + INDEKS] != netværk_driver.enhed_mail[INDEKS]) return;
            }
            for (int INDEKS = 0; INDEKS < 6; INDEKS++) 찾은장치[INDEKS] = input_ramme[22 + INDEKS];
            찾은주소 = peer_VÆRDI;
        } else if (종류 == 1) {
            바깥머리(0x0806, false);
            넣기16(produktoutput_ramme, 14, 1); 넣기16(produktoutput_ramme, 16, 0x0800);
            produktoutput_ramme[18] = 6; produktoutput_ramme[19] = 4; 넣기16(produktoutput_ramme, 20, 2);
            for (int INDEKS = 0; INDEKS < 6; INDEKS++) {
                produktoutput_ramme[INDEKS] = input_ramme[22 + INDEKS]; produktoutput_ramme[32 + INDEKS] = input_ramme[22 + INDEKS];
                produktoutput_ramme[22 + INDEKS] = netværk_driver.enhed_mail[INDEKS];
            }
            넣기32(produktoutput_ramme, 28, 내주소); 넣기32(produktoutput_ramme, 38, peer_VÆRDI);
            netværk_driver.maile(produktoutput_ramme, 42);
        }
    }

    static void Proces_ramme(int varighed_VÆRDI) {
        if (varighed_VÆRDI < 14 || varighed_VÆRDI > input_ramme.length) { 폐기수++; return; }
        boolean 자기 = true, udsende_VÆRDI = true;
        for (int INDEKS = 0; INDEKS < 6; INDEKS++) {
            if (input_ramme[INDEKS] != netværk_driver.enhed_mail[INDEKS]) 자기 = false;
            if (input_ramme[INDEKS] != 255) udsende_VÆRDI = false;
        }
        if (!자기 && !udsende_VÆRDI) return;
        if (heltal_16(input_ramme, 12) == 0x0806) { Proces_mail(varighed_VÆRDI); return; }
        if (heltal_16(input_ramme, 12) != 0x0800) return;
        if (varighed_VÆRDI < 34 || (input_ramme[14] >>> 4) != 4) { 폐기수++; return; }
        int Header_varighed = (input_ramme[14] & 15) * 4, i_alt_varighed = heltal_16(input_ramme, 16);
        if (Header_varighed < 20 || Header_varighed > 60 || i_alt_varighed < Header_varighed + 8 || i_alt_varighed > varighed_VÆRDI - 14
            || (heltal_16(input_ramme, 20) & 0x3fff) != 0 || input_ramme[23] != 17
            || heltal_32(input_ramme, 30) != 내주소 || SUM_VÆRDI(input_ramme, 14, Header_varighed, 0) != 65535) { 폐기수++; return; }
        int Kør_2 = 14 + Header_varighed, data_varighed = heltal_16(input_ramme, Kør_2 + 4);
        if (data_varighed < 8 || data_varighed != i_alt_varighed - Header_varighed || data_varighed > 1032) { 폐기수++; return; }
        int 출발 = heltal_32(input_ramme, 26);
        if (heltal_16(input_ramme, Kør_2 + 6) != 0 && SUM_VÆRDI(input_ramme, Kør_2, data_varighed, 가상머리합(출발, 내주소, data_varighed)) != 65535) {
            폐기수++; return;
        }
        int destination_VÆRDI = heltal_16(input_ramme, Kør_2 + 2);
        for (int udvidelsesstik_post = 0; udvidelsesstik_post < 4; udvidelsesstik_post++) if (접속번호들[udvidelsesstik_post] != 0 && 접속번호들[udvidelsesstik_post] == destination_VÆRDI) {
            if (MODTAGET_VED_UDLØB_varighed[udvidelsesstik_post] >= 0) { 폐기수++; return; }
            MODTAGET_VED_UDLØB_varighed[udvidelsesstik_post] = data_varighed - 8; MODTAGET_VED_UDLØB_mail[udvidelsesstik_post] = 출발; MODTAGET_VED_UDLØB_portnummer[udvidelsesstik_post] = heltal_16(input_ramme, Kør_2);
            for (int INDEKS = 0; INDEKS < data_varighed - 8; INDEKS++) MODTAGET_VED_UDLØB_data[udvidelsesstik_post * 1024 + INDEKS] = input_ramme[Kør_2 + 8 + INDEKS];
            return;
        }
    }

    static void bekræfte() {
        for (int INDEKS = 0; INDEKS < 16; INDEKS++) {
            int varighed_VÆRDI = netværk_driver.modtage(input_ramme);
            if (varighed_VÆRDI == 0) return;
            Proces_ramme(varighed_VÆRDI);
        }
    }
    static int Søg_mail(int mail) {
        if (mail == 0 || mail == -1 || (mail >>> 28) >= 14 || (mail >>> 24) == 127 || mail == 내주소) return -101;
        int Næste_vare = (mail & netværksmaske) == (내주소 & netværksmaske) ? mail : gateway_VÆRDI;
        if (Næste_vare == 찾은주소) return 0;
        찾을주소 = Næste_vare;
        int Kør_2 = enhed_VÆRDI.밀리초(), Næste_anmodning = Kør_2;
        while (enhed_VÆRDI.밀리초() - Kør_2 < 1000) {
            if (enhed_VÆRDI.밀리초() - Næste_anmodning >= 0) { anmodning_mail(Næste_vare); Næste_anmodning += 300; }
            bekræfte();
            if (찾은주소 == Næste_vare) return 0;
            enhed_VÆRDI.잠시양보();
        }
        return -110;
    }
    static int maile(int handle_VÆRDI, int mail, int portnummer, int[] data, int varighed_VÆRDI) {
        int udvidelsesstik_post = INDEKS(handle_VÆRDI);
        if (udvidelsesstik_post < 0) return -9;
        if (netværk_driver.입출력기준주소 == 0) return -19;
        if (portnummer < 1 || portnummer > 65535 || varighed_VÆRDI < 0 || varighed_VÆRDI > 1024) return -22;
        int KR = Søg_mail(mail);
        if (KR < 0) return KR;
        바깥머리(0x0800, false);
        produktoutput_ramme[14] = 0x45; produktoutput_ramme[15] = 0; 넣기16(produktoutput_ramme, 16, 28 + varighed_VÆRDI);
        넣기16(produktoutput_ramme, 18, identifikator_VÆRDI++); 넣기16(produktoutput_ramme, 20, 0x4000);
        produktoutput_ramme[22] = 64; produktoutput_ramme[23] = 17; 넣기16(produktoutput_ramme, 24, 0);
        넣기32(produktoutput_ramme, 26, 내주소); 넣기32(produktoutput_ramme, 30, mail);
        넣기16(produktoutput_ramme, 24, ~SUM_VÆRDI(produktoutput_ramme, 14, 20, 0));
        넣기16(produktoutput_ramme, 34, 접속번호들[udvidelsesstik_post]); 넣기16(produktoutput_ramme, 36, portnummer);
        넣기16(produktoutput_ramme, 38, varighed_VÆRDI + 8); 넣기16(produktoutput_ramme, 40, 0);
        for (int INDEKS = 0; INDEKS < varighed_VÆRDI; INDEKS++) produktoutput_ramme[42 + INDEKS] = data[INDEKS] & 255;
        int kontrolsum = (~SUM_VÆRDI(produktoutput_ramme, 34, varighed_VÆRDI + 8, 가상머리합(내주소, mail, varighed_VÆRDI + 8))) & 65535;
        넣기16(produktoutput_ramme, 40, kontrolsum == 0 ? 65535 : kontrolsum);
        KR = netværk_driver.maile(produktoutput_ramme, varighed_VÆRDI + 42);
        return KR < 0 ? KR : varighed_VÆRDI;
    }
    static int modtage(int handle_VÆRDI, int[] data, int kapacitet_VÆRDI, int 제한) {
        int udvidelsesstik_post = INDEKS(handle_VÆRDI);
        if (udvidelsesstik_post < 0) return -9;
        int Kør_2 = enhed_VÆRDI.밀리초();
        while (true) {
            bekræfte();
            int varighed_VÆRDI = MODTAGET_VED_UDLØB_varighed[udvidelsesstik_post];
            if (varighed_VÆRDI >= 0) {
                MODTAGET_VED_UDLØB_varighed[udvidelsesstik_post] = -1;
                if (varighed_VÆRDI > kapacitet_VÆRDI) return -90;
                for (int INDEKS = 0; INDEKS < varighed_VÆRDI; INDEKS++) data[INDEKS] = MODTAGET_VED_UDLØB_data[udvidelsesstik_post * 1024 + INDEKS];
                return varighed_VÆRDI;
            }
            if (제한 == 0) return -11;
            if (enhed_VÆRDI.밀리초() - Kør_2 >= 제한) return -110;
            enhed_VÆRDI.잠시양보();
        }
    }
    static void status_VÆRDI() {
        sms_Terminal.Skrive(netværk_driver.입출력기준주소 == 0 ? "NET unavailable (RTL8139 required)\n" : "NET RTL8139 192.168.0.100/24 gateway 192.168.0.1 UDP\n");
        sms_Terminal.Skrive("TX: "); sms_Terminal.skrive_tal(netværk_driver.송신수);
        sms_Terminal.Skrive(" RX: "); sms_Terminal.skrive_tal(netværk_driver.modtage_TÆL);
        sms_Terminal.Skrive(" DROP: "); sms_Terminal.skrive_tal(폐기수);
        sms_Terminal.Skrive("\n");
    }
}
