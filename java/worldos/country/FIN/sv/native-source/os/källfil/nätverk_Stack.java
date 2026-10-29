// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** statisk_värde IPv4/ARP/UDP. 최대 네 통신접속번호와 접속번호마다 한 데이터그램을 보관한다. */
public final class nätverk_Stack {
    static final int 내주소 = 0xc0a80064; /* ip.conf:IP */
    static final int nätverksmask = 0xffffff00; /* ip.conf:NETMASK */
    static final int gateway_värde = 0xc0a80001; /* ip.conf:GATEWAY */
    static int[] indata_ram = new int[1536], utleverans_ram = new int[1536];
    static int[] 접속번호들 = new int[4], BELOPP_längd = new int[4], BELOPP_ADRESS = new int[4], BELOPP_portnummer = new int[4];
    static int[] BELOPP_data = new int[4096], 찾은장치 = new int[6];
    static int 찾을주소 = 0, 찾은주소 = 0, identifierare_värde = 0, 폐기수 = 0;

    static int heltal_16(int[] ram_INDEX, int position) { return (ram_INDEX[position] << 8) | ram_INDEX[position + 1]; }
    static int heltal_32(int[] ram_INDEX, int position) { return (heltal_16(ram_INDEX, position) << 16) | heltal_16(ram_INDEX, position + 2); }
    static void 넣기16(int[] ram_INDEX, int position, int värde) { ram_INDEX[position] = (värde >>> 8) & 255; ram_INDEX[position + 1] = värde & 255; }
    static void 넣기32(int[] ram_INDEX, int position, int värde) { 넣기16(ram_INDEX, position, värde >>> 16); 넣기16(ram_INDEX, position + 2, värde); }
    static int SUM_värde(int[] ram_INDEX, int Kör, int längd_värde, int värde) {
        for (int INDEX = 0; INDEX < längd_värde; INDEX += 2)
            värde += (ram_INDEX[Kör + INDEX] << 8) | (INDEX + 1 < längd_värde ? ram_INDEX[Kör + INDEX + 1] : 0);
        while ((värde >>> 16) != 0) värde = (värde & 65535) + (värde >>> 16);
        return värde;
    }
    static int 가상머리합(int 출발, int 도착, int längd_värde) {
        return (출발 >>> 16) + (출발 & 65535) + (도착 >>> 16) + (도착 & 65535) + 17 + längd_värde;
    }

    static void Rent_Process() {
        for (int INDEX = 0; INDEX < 4; INDEX++) {
            접속번호들[INDEX] = 0; BELOPP_längd[INDEX] = -1; BELOPP_ADRESS[INDEX] = 0; BELOPP_portnummer[INDEX] = 0;
        }
        for (int INDEX = 0; INDEX < 64; INDEX++) if (nätverk_drivrutin.få(indata_ram) == 0) break;
    }
    static int INDEX(int handtag_värde) { return handtag_värde >= 3 && handtag_värde < 7 && 접속번호들[handtag_värde - 3] != 0 ? handtag_värde - 3 : -1; }
    static int Öppna(int portnummer) {
        if (nätverk_drivrutin.입출력기준주소 == 0) return -19;
        if (portnummer < 0 || portnummer > 65535) return -22;
        if (portnummer != 0) for (int INDEX = 0; INDEX < 4; INDEX++) if (접속번호들[INDEX] == portnummer) return -98;
        for (int INDEX = 0; INDEX < 4; INDEX++) if (접속번호들[INDEX] == 0) {
            if (portnummer == 0) {
                portnummer = 49152;
                boolean 겹침 = true;
                while (겹침) {
                    겹침 = false;
                    for (int framåtvänd_värde = 0; framåtvänd_värde < 4; framåtvänd_värde++) if (접속번호들[framåtvänd_värde] == portnummer) 겹침 = true;
                    if (겹침) portnummer++;
                }
            }
            접속번호들[INDEX] = portnummer; BELOPP_längd[INDEX] = -1;
            return INDEX + 3;
        }
        return -24;
    }
    static int Stäng(int handtag_värde) {
        int fack_post = INDEX(handtag_värde);
        if (fack_post < 0) return -9;
        접속번호들[fack_post] = 0; BELOPP_längd[fack_post] = -1;
        return 0;
    }
    static int peer_ADRESS(int handtag_värde) { int fack_post = INDEX(handtag_värde); return fack_post < 0 ? -9 : BELOPP_ADRESS[fack_post]; }
    static int peer_portnummer(int handtag_värde) { int fack_post = INDEX(handtag_värde); return fack_post < 0 ? -9 : BELOPP_portnummer[fack_post]; }

    static void 바깥머리(int variant_värde, boolean sänd_värde) {
        for (int INDEX = 0; INDEX < 6; INDEX++) {
            utleverans_ram[INDEX] = sänd_värde ? 255 : 찾은장치[INDEX];
            utleverans_ram[6 + INDEX] = nätverk_drivrutin.enhet_ADRESS[INDEX];
        }
        넣기16(utleverans_ram, 12, variant_värde);
    }
    static void begäran_ADRESS(int mål_värde) {
        바깥머리(0x0806, true);
        넣기16(utleverans_ram, 14, 1); 넣기16(utleverans_ram, 16, 0x0800);
        utleverans_ram[18] = 6; utleverans_ram[19] = 4; 넣기16(utleverans_ram, 20, 1);
        for (int INDEX = 0; INDEX < 6; INDEX++) {
            utleverans_ram[22 + INDEX] = nätverk_drivrutin.enhet_ADRESS[INDEX]; utleverans_ram[32 + INDEX] = 0;
        }
        넣기32(utleverans_ram, 28, 내주소); 넣기32(utleverans_ram, 38, mål_värde);
        nätverk_drivrutin.skicka(utleverans_ram, 42);
    }
    static void Process_ADRESS(int längd_värde) {
        if (längd_värde < 42 || heltal_16(indata_ram, 14) != 1 || heltal_16(indata_ram, 16) != 0x0800
            || indata_ram[18] != 6 || indata_ram[19] != 4 || heltal_32(indata_ram, 38) != 내주소) { 폐기수++; return; }
        int variant_värde = heltal_16(indata_ram, 20), peer_värde = heltal_32(indata_ram, 28);
        if (variant_värde == 2 && peer_värde == 찾을주소) {
            for (int INDEX = 0; INDEX < 6; INDEX++) {
                if (indata_ram[6 + INDEX] != indata_ram[22 + INDEX] || indata_ram[32 + INDEX] != nätverk_drivrutin.enhet_ADRESS[INDEX]) return;
            }
            for (int INDEX = 0; INDEX < 6; INDEX++) 찾은장치[INDEX] = indata_ram[22 + INDEX];
            찾은주소 = peer_värde;
        } else if (variant_värde == 1) {
            바깥머리(0x0806, false);
            넣기16(utleverans_ram, 14, 1); 넣기16(utleverans_ram, 16, 0x0800);
            utleverans_ram[18] = 6; utleverans_ram[19] = 4; 넣기16(utleverans_ram, 20, 2);
            for (int INDEX = 0; INDEX < 6; INDEX++) {
                utleverans_ram[INDEX] = indata_ram[22 + INDEX]; utleverans_ram[32 + INDEX] = indata_ram[22 + INDEX];
                utleverans_ram[22 + INDEX] = nätverk_drivrutin.enhet_ADRESS[INDEX];
            }
            넣기32(utleverans_ram, 28, 내주소); 넣기32(utleverans_ram, 38, peer_värde);
            nätverk_drivrutin.skicka(utleverans_ram, 42);
        }
    }

    static void Process_ram(int längd_värde) {
        if (längd_värde < 14 || längd_värde > indata_ram.length) { 폐기수++; return; }
        boolean 자기 = true, sänd_värde = true;
        for (int INDEX = 0; INDEX < 6; INDEX++) {
            if (indata_ram[INDEX] != nätverk_drivrutin.enhet_ADRESS[INDEX]) 자기 = false;
            if (indata_ram[INDEX] != 255) sänd_värde = false;
        }
        if (!자기 && !sänd_värde) return;
        if (heltal_16(indata_ram, 12) == 0x0806) { Process_ADRESS(längd_värde); return; }
        if (heltal_16(indata_ram, 12) != 0x0800) return;
        if (längd_värde < 34 || (indata_ram[14] >>> 4) != 4) { 폐기수++; return; }
        int huvud_längd = (indata_ram[14] & 15) * 4, summa_längd = heltal_16(indata_ram, 16);
        if (huvud_längd < 20 || huvud_längd > 60 || summa_längd < huvud_längd + 8 || summa_längd > längd_värde - 14
            || (heltal_16(indata_ram, 20) & 0x3fff) != 0 || indata_ram[23] != 17
            || heltal_32(indata_ram, 30) != 내주소 || SUM_värde(indata_ram, 14, huvud_längd, 0) != 65535) { 폐기수++; return; }
        int Kör = 14 + huvud_längd, data_längd = heltal_16(indata_ram, Kör + 4);
        if (data_längd < 8 || data_längd != summa_längd - huvud_längd || data_längd > 1032) { 폐기수++; return; }
        int 출발 = heltal_32(indata_ram, 26);
        if (heltal_16(indata_ram, Kör + 6) != 0 && SUM_värde(indata_ram, Kör, data_längd, 가상머리합(출발, 내주소, data_längd)) != 65535) {
            폐기수++; return;
        }
        int mål_värde = heltal_16(indata_ram, Kör + 2);
        for (int fack_post = 0; fack_post < 4; fack_post++) if (접속번호들[fack_post] != 0 && 접속번호들[fack_post] == mål_värde) {
            if (BELOPP_längd[fack_post] >= 0) { 폐기수++; return; }
            BELOPP_längd[fack_post] = data_längd - 8; BELOPP_ADRESS[fack_post] = 출발; BELOPP_portnummer[fack_post] = heltal_16(indata_ram, Kör);
            for (int INDEX = 0; INDEX < data_längd - 8; INDEX++) BELOPP_data[fack_post * 1024 + INDEX] = indata_ram[Kör + 8 + INDEX];
            return;
        }
    }

    static void verifiera() {
        for (int INDEX = 0; INDEX < 16; INDEX++) {
            int längd_värde = nätverk_drivrutin.få(indata_ram);
            if (längd_värde == 0) return;
            Process_ram(längd_värde);
        }
    }
    static int Sök_ADRESS(int Adress) {
        if (Adress == 0 || Adress == -1 || (Adress >>> 28) >= 14 || (Adress >>> 24) == 127 || Adress == 내주소) return -101;
        int Nästa_objekt = (Adress & nätverksmask) == (내주소 & nätverksmask) ? Adress : gateway_värde;
        if (Nästa_objekt == 찾은주소) return 0;
        찾을주소 = Nästa_objekt;
        int Kör = enhet_värde.밀리초(), Nästa_begäran = Kör;
        while (enhet_värde.밀리초() - Kör < 1000) {
            if (enhet_värde.밀리초() - Nästa_begäran >= 0) { begäran_ADRESS(Nästa_objekt); Nästa_begäran += 300; }
            verifiera();
            if (찾은주소 == Nästa_objekt) return 0;
            enhet_värde.잠시양보();
        }
        return -110;
    }
    static int skicka(int handtag_värde, int Adress, int portnummer, int[] data, int längd_värde) {
        int fack_post = INDEX(handtag_värde);
        if (fack_post < 0) return -9;
        if (nätverk_drivrutin.입출력기준주소 == 0) return -19;
        if (portnummer < 1 || portnummer > 65535 || längd_värde < 0 || längd_värde > 1024) return -22;
        int RESULTAT = Sök_ADRESS(Adress);
        if (RESULTAT < 0) return RESULTAT;
        바깥머리(0x0800, false);
        utleverans_ram[14] = 0x45; utleverans_ram[15] = 0; 넣기16(utleverans_ram, 16, 28 + längd_värde);
        넣기16(utleverans_ram, 18, identifierare_värde++); 넣기16(utleverans_ram, 20, 0x4000);
        utleverans_ram[22] = 64; utleverans_ram[23] = 17; 넣기16(utleverans_ram, 24, 0);
        넣기32(utleverans_ram, 26, 내주소); 넣기32(utleverans_ram, 30, Adress);
        넣기16(utleverans_ram, 24, ~SUM_värde(utleverans_ram, 14, 20, 0));
        넣기16(utleverans_ram, 34, 접속번호들[fack_post]); 넣기16(utleverans_ram, 36, portnummer);
        넣기16(utleverans_ram, 38, längd_värde + 8); 넣기16(utleverans_ram, 40, 0);
        for (int INDEX = 0; INDEX < längd_värde; INDEX++) utleverans_ram[42 + INDEX] = data[INDEX] & 255;
        int kontrollsumma = (~SUM_värde(utleverans_ram, 34, längd_värde + 8, 가상머리합(내주소, Adress, längd_värde + 8))) & 65535;
        넣기16(utleverans_ram, 40, kontrollsumma == 0 ? 65535 : kontrollsumma);
        RESULTAT = nätverk_drivrutin.skicka(utleverans_ram, längd_värde + 42);
        return RESULTAT < 0 ? RESULTAT : längd_värde;
    }
    static int få(int handtag_värde, int[] data, int kapacitet_värde, int 제한) {
        int fack_post = INDEX(handtag_värde);
        if (fack_post < 0) return -9;
        int Kör = enhet_värde.밀리초();
        while (true) {
            verifiera();
            int längd_värde = BELOPP_längd[fack_post];
            if (längd_värde >= 0) {
                BELOPP_längd[fack_post] = -1;
                if (längd_värde > kapacitet_värde) return -90;
                for (int INDEX = 0; INDEX < längd_värde; INDEX++) data[INDEX] = BELOPP_data[fack_post * 1024 + INDEX];
                return längd_värde;
            }
            if (제한 == 0) return -11;
            if (enhet_värde.밀리초() - Kör >= 제한) return -110;
            enhet_värde.잠시양보();
        }
    }
    static void status_värde() {
        SMS_Terminal.Skriv(nätverk_drivrutin.입출력기준주소 == 0 ? "NET unavailable (RTL8139 required)\n" : "NET RTL8139 192.168.0.100/24 gateway 192.168.0.1 UDP\n");
        SMS_Terminal.Skriv("TX: "); SMS_Terminal.skriva_nummer(nätverk_drivrutin.송신수);
        SMS_Terminal.Skriv(" RX: "); SMS_Terminal.skriva_nummer(nätverk_drivrutin.få_ANTAL);
        SMS_Terminal.Skriv(" DROP: "); SMS_Terminal.skriva_nummer(폐기수);
        SMS_Terminal.Skriv("\n");
    }
}
