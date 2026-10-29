// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** RAM bestand 64개, 파일당 16384바이트, 서술자 16개. 모든 gegevens/정책은 Java에 있다.
 * 호출 도중 양보하지 않으므로 현재의 단일 코어 협력식 작업 사이에서 원자적이다.
 * 디스크 저장이나 POSIX 전체 구현을 뜻하지 않는다. 음수 반환은 fout 번호다.
 */
public final class GeheugenBestanden {
    static final int Bestand_AANTAL = 64;
    static int[] Naam = new int[Bestand_AANTAL * 64];
    static int[] 이름길이 = new int[Bestand_AANTAL];
    // Pack four bytes in each Java int, preserving the old content heap budget.
    static int[] Inhoud_WAARDE = new int[Bestand_AANTAL * 4096];
    static int[] tijdsduur_WAARDE = new int[Bestand_AANTAL];
    static int[] verwijzen_AANTAL = new int[Bestand_AANTAL];
    static int[] gebruik_WAARDE = new int[16];
    static int[] doel = new int[16];
    static int[] positie = new int[16];
    static int[] methode_MODUS = new int[16];
    static int[] pad = new int[64];
    static int pad_tijdsduur;

    public static int 파일한도() { return Bestand_AANTAL; }
    static int 자료읽기(int bestand, int plaatsingsindex) { return (Inhoud_WAARDE[bestand * 4096 + plaatsingsindex / 4] >>> ((plaatsingsindex & 3) * 8)) & 255; }
    static void schrijven_gegevens(int bestand, int plaatsingsindex, int WAARDE) {
        int sleuf_invoer = bestand * 4096 + plaatsingsindex / 4, verplaatsen_WAARDE_83b651b8 = (plaatsingsindex & 3) * 8;
        Inhoud_WAARDE[sleuf_invoer] = (Inhoud_WAARDE[sleuf_invoer] & ~(255 << verplaatsen_WAARDE_83b651b8)) | ((WAARDE & 255) << verplaatsen_WAARDE_83b651b8);
    }

    public static int pad_START(int Grootte) {
        pad_tijdsduur = 0;
        if (Grootte < 1 || Grootte > 63) return -36;
        pad_tijdsduur = Grootte;
        for (int lus_INDEX = 0; lus_INDEX < Grootte; lus_INDEX++) pad[lus_INDEX] = 0;
        return 0;
    }
    public static int pad_byte(int INDEX, int WAARDE) {
        if (INDEX < 0 || INDEX >= pad_tijdsduur || WAARDE < 1 || WAARDE > 255) return -22;
        pad[INDEX] = WAARDE; return 0;
    }
    static int Zoeken_invoer() {
        for (int Bestand_INDEX = 0; Bestand_INDEX < Bestand_AANTAL; Bestand_INDEX++) if (이름길이[Bestand_INDEX] > 0 && 이름길이[Bestand_INDEX] == Canonical_tijdsduur && 접두(Naam, Bestand_INDEX * 64, 이름길이[Bestand_INDEX], Canonical_WAARDE, Canonical_tijdsduur)) return Bestand_INDEX;
        return -1;
    }
    public static int Openen(int 플래그) {
        if (pad_tijdsduur == 0 || (플래그 & ~0x6c3) != 0 || (플래그 & 3) == 3) return -22;
        for (int lus_INDEX = 0; lus_INDEX < pad_tijdsduur; lus_INDEX++) if (pad[lus_INDEX] == 0) return -22;
        if ((플래그 & 0x200) != 0 && (플래그 & 3) == 0) return -22;
        int resultaat = normaliseren_WAARDE(); if (resultaat < 0) return resultaat;
        if (Zoeken_map(Canonical_tijdsduur) >= 0) return -21;
        resultaat = cheque_bovenliggend(); if (resultaat < 0) return resultaat;
        int bestand = Zoeken_invoer();
        if (bestand >= 0 && (플래그 & 0xc0) == 0xc0) return -17;
        if (bestand < 0 && (플래그 & 0x40) == 0) return -2;
        int 서술자 = -1;
        for (int lus_INDEX = 0; lus_INDEX < 16; lus_INDEX++) if (gebruik_WAARDE[lus_INDEX] == 0) { 서술자 = lus_INDEX; break; }
        if (서술자 < 0) return -24;
        if (bestand < 0) {
            for (int lus_INDEX = 0; lus_INDEX < Bestand_AANTAL; lus_INDEX++) if (이름길이[lus_INDEX] == 0 && verwijzen_AANTAL[lus_INDEX] == 0) { bestand = lus_INDEX; break; }
            if (bestand < 0) return -28;
            이름길이[bestand] = Canonical_tijdsduur;
            for (int lus_INDEX = 0; lus_INDEX < Canonical_tijdsduur; lus_INDEX++) Naam[bestand * 64 + lus_INDEX] = Canonical_WAARDE[lus_INDEX];
            tijdsduur_WAARDE[bestand] = 0;
        }
        if ((플래그 & 0x200) != 0) tijdsduur_WAARDE[bestand] = 0;
        gebruik_WAARDE[서술자] = 1; doel[서술자] = bestand; positie[서술자] = 0; methode_MODUS[서술자] = 플래그;
        verwijzen_AANTAL[bestand]++;
        return 서술자 + 3;
    }
    static int bevestigen(int 서술자) {
        return 서술자 >= 3 && 서술자 < 19 && gebruik_WAARDE[서술자 - 3] != 0 ? 서술자 - 3 : -1;
    }
    public static int Lezen(int 서술자) {
        int sleuf_invoer = bevestigen(서술자);
        if (sleuf_invoer < 0 || (methode_MODUS[sleuf_invoer] & 3) == 1) return -9;
        int bestand = doel[sleuf_invoer];
        if (positie[sleuf_invoer] >= tijdsduur_WAARDE[bestand]) return 256; // EOF와 werkelijk_gegevens 0x00..0xff 구별
        return 자료읽기(bestand, positie[sleuf_invoer]++);
    }
    public static int Schrijven(int 서술자, int WAARDE) {
        int sleuf_invoer = bevestigen(서술자);
        if (sleuf_invoer < 0 || (methode_MODUS[sleuf_invoer] & 3) == 0) return -9;
        int bestand = doel[sleuf_invoer];
        if ((methode_MODUS[sleuf_invoer] & 0x400) != 0) positie[sleuf_invoer] = tijdsduur_WAARDE[bestand];
        if (positie[sleuf_invoer] >= 16384) return -28;
        while (tijdsduur_WAARDE[bestand] < positie[sleuf_invoer]) schrijven_gegevens(bestand, tijdsduur_WAARDE[bestand]++, 0);
        schrijven_gegevens(bestand, positie[sleuf_invoer]++, WAARDE);
        if (tijdsduur_WAARDE[bestand] < positie[sleuf_invoer]) tijdsduur_WAARDE[bestand] = positie[sleuf_invoer];
        return 1;
    }
    public static int zoeken_functie(int 서술자, int 거리, int Taken_wortel) {
        int sleuf_invoer = bevestigen(서술자);
        if (sleuf_invoer < 0) return -9;
        if (Taken_wortel < 0 || Taken_wortel > 2 || 거리 < -16384 || 거리 > 16384) return -22;
        int 새위치 = 거리 + (Taken_wortel == 0 ? 0 : Taken_wortel == 1 ? positie[sleuf_invoer] : tijdsduur_WAARDE[doel[sleuf_invoer]]);
        if (새위치 < 0 || 새위치 > 16384) return -22;
        positie[sleuf_invoer] = 새위치; return 새위치;
    }
    public static int Sluiten(int 서술자) {
        int sleuf_invoer = bevestigen(서술자);
        if (sleuf_invoer < 0) return -9;
        verwijzen_AANTAL[doel[sleuf_invoer]]--; gebruik_WAARDE[sleuf_invoer] = 0; return 0;
    }
    public static int Grootte(int 서술자) {
        int sleuf_invoer = bevestigen(서술자); return sleuf_invoer < 0 ? -9 : tijdsduur_WAARDE[doel[sleuf_invoer]];
    }
    public static int set_tijdsduur(int 서술자, int Grootte) {
        int sleuf_invoer = bevestigen(서술자);
        if (sleuf_invoer < 0 || (methode_MODUS[sleuf_invoer] & 3) == 0) return -9;
        if (Grootte < 0 || Grootte > 16384) return -22;
        int bestand = doel[sleuf_invoer];
        while (tijdsduur_WAARDE[bestand] < Grootte) schrijven_gegevens(bestand, tijdsduur_WAARDE[bestand]++, 0);
        tijdsduur_WAARDE[bestand] = Grootte; return 0;
    }
    public static int wissen_invoer() {
        if (pad_tijdsduur == 0) return -22;
        int resultaat = normaliseren_WAARDE(); if (resultaat < 0) return resultaat;
        if (Zoeken_map(Canonical_tijdsduur) >= 0) return -21;
        resultaat = cheque_bovenliggend(); if (resultaat < 0) return resultaat;
        int bestand = Zoeken_invoer();
        if (bestand < 0) return -2;
        이름길이[bestand] = 0; return 0; // 열려 있는 파일은 마지막 close까지 behouden_WAARDE
    }
    static void invoer_Lijst_f07b3200() {
        pad_START(1); pad_byte(0, '.'); 경로목록();
    }
    public static int 공개이름길이(int INDEX) {
        if (INDEX < 0 || INDEX >= Bestand_AANTAL || 이름길이[INDEX] == 0) return 0;
        for (int lus_INDEX = 0; lus_INDEX < 이름길이[INDEX]; lus_INDEX++) if (Naam[INDEX * 64 + lus_INDEX] == '/') return 0;
        return 이름길이[INDEX];
    }
    public static int 공개이름바이트(int INDEX, int plaatsingsindex) {
        return INDEX >= 0 && INDEX < Bestand_AANTAL && plaatsingsindex >= 0 && plaatsingsindex < 이름길이[INDEX] ? Naam[INDEX * 64 + plaatsingsindex] : -22;
    }
    public static int 공개파일크기(int INDEX) { return INDEX >= 0 && INDEX < Bestand_AANTAL ? tijdsduur_WAARDE[INDEX] : -22; }
    static int[] Canonical_WAARDE = new int[64], actueel_item = new int[64], map_naam = new int[16 * 64], map_tijdsduur = new int[16];
    static int Canonical_tijdsduur, actueel_tijdsduur;
    static boolean 접두(int[] 이름들, int starten, int pad_WAARDE, int[] voorkant_WAARDE, int interlinie_pad) {
        if (pad_WAARDE < interlinie_pad) return false;
        for (int lus_INDEX = 0; lus_INDEX < interlinie_pad; lus_INDEX++) if (이름들[starten + lus_INDEX] != voorkant_WAARDE[lus_INDEX]) return false;
        return true;
    }
    static int normaliseren_WAARDE() {
        if (pad_tijdsduur == 0) return -22;
        Canonical_tijdsduur = pad[0] == '/' ? 0 : actueel_tijdsduur;
        for (int lus_INDEX = 0; lus_INDEX < Canonical_tijdsduur; lus_INDEX++) Canonical_WAARDE[lus_INDEX] = actueel_item[lus_INDEX];
        int 읽는자리 = 0;
        while (읽는자리 < pad_tijdsduur) {
            while (읽는자리 < pad_tijdsduur && pad[읽는자리] == '/') 읽는자리++;
            int START_functie = 읽는자리; while (읽는자리 < pad_tijdsduur && pad[읽는자리] != '/') { if (pad[읽는자리] == 0) return -22; 읽는자리++; }
            int invoer_AANTAL_8f7753a1 = 읽는자리 - START_functie; if (invoer_AANTAL_8f7753a1 == 0 || invoer_AANTAL_8f7753a1 == 1 && pad[START_functie] == '.') continue;
            if (invoer_AANTAL_8f7753a1 == 2 && pad[START_functie] == '.' && pad[START_functie + 1] == '.') {
                while (Canonical_tijdsduur > 0 && Canonical_WAARDE[Canonical_tijdsduur - 1] != '/') Canonical_tijdsduur--;
                if (Canonical_tijdsduur > 0) Canonical_tijdsduur--;
                continue;
            }
            if (Canonical_tijdsduur + invoer_AANTAL_8f7753a1 + (Canonical_tijdsduur == 0 ? 0 : 1) > 63) return -36;
            if (Canonical_tijdsduur > 0) Canonical_WAARDE[Canonical_tijdsduur++] = '/';
            for (int lus_INDEX = START_functie; lus_INDEX < 읽는자리; lus_INDEX++) Canonical_WAARDE[Canonical_tijdsduur++] = pad[lus_INDEX];
        }
        return 0;
    }
    static int Zoeken_map(int invoer_AANTAL_8f7753a1) {
        if (invoer_AANTAL_8f7753a1 == 0) return 0;
        for (int lus_INDEX = 1; lus_INDEX < 16; lus_INDEX++) if (map_tijdsduur[lus_INDEX] == invoer_AANTAL_8f7753a1 && 접두(map_naam, lus_INDEX * 64, invoer_AANTAL_8f7753a1, Canonical_WAARDE, invoer_AANTAL_8f7753a1)) return lus_INDEX;
        return -1;
    }
    static int cheque_bovenliggend() {
        int invoer_AANTAL_8f7753a1 = Canonical_tijdsduur; while (invoer_AANTAL_8f7753a1 > 0 && Canonical_WAARDE[invoer_AANTAL_8f7753a1 - 1] != '/') invoer_AANTAL_8f7753a1--;
        return Zoeken_map(invoer_AANTAL_8f7753a1 == 0 ? 0 : invoer_AANTAL_8f7753a1 - 1) < 0 ? -2 : 0;
    }
    public static int maken_map() {
        int 처리값 = normaliseren_WAARDE(); if (처리값 < 0) return 처리값;
        if (Zoeken_map(Canonical_tijdsduur) >= 0 || Zoeken_invoer() >= 0) return -17;
        처리값 = cheque_bovenliggend(); if (처리값 < 0) return 처리값;
        for (int lus_INDEX = 1; lus_INDEX < 16; lus_INDEX++) if (map_tijdsduur[lus_INDEX] == 0) {
            map_tijdsduur[lus_INDEX] = Canonical_tijdsduur; for (int inner_functie = 0; inner_functie < Canonical_tijdsduur; inner_functie++) map_naam[lus_INDEX * 64 + inner_functie] = Canonical_WAARDE[inner_functie]; return 0;
        }
        return -28;
    }
    public static int invoer_soort() {
        int 처리값 = normaliseren_WAARDE(); if (처리값 < 0) return 처리값;
        if (Zoeken_map(Canonical_tijdsduur) >= 0) return 2;
        return Zoeken_invoer() >= 0 ? 1 : 0;
    }
    public static int wijzigen_map() {
        int 처리값 = normaliseren_WAARDE(); if (처리값 < 0) return 처리값;
        if (Zoeken_map(Canonical_tijdsduur) < 0) return -2;
        actueel_tijdsduur = Canonical_tijdsduur; for (int lus_INDEX = 0; lus_INDEX < actueel_tijdsduur; lus_INDEX++) actueel_item[lus_INDEX] = Canonical_WAARDE[lus_INDEX]; return 0;
    }
    public static int verwijderen_map() {
        int 처리값 = normaliseren_WAARDE(); if (처리값 < 0) return 처리값;
        int map_nummer = Zoeken_map(Canonical_tijdsduur); if (map_nummer < 0) return -2; if (map_nummer == 0) return -16;
        if (actueel_tijdsduur == Canonical_tijdsduur && 접두(actueel_item, 0, actueel_tijdsduur, Canonical_WAARDE, Canonical_tijdsduur)) return -16;
        for (int lus_INDEX = 0; lus_INDEX < Bestand_AANTAL; lus_INDEX++) {
            if (이름길이[lus_INDEX] > Canonical_tijdsduur && 접두(Naam, lus_INDEX * 64, 이름길이[lus_INDEX], Canonical_WAARDE, Canonical_tijdsduur) && Naam[lus_INDEX * 64 + Canonical_tijdsduur] == '/') return -39;
        }
        for (int lus_INDEX = 0; lus_INDEX < 16; lus_INDEX++) {
            if (map_tijdsduur[lus_INDEX] > Canonical_tijdsduur && 접두(map_naam, lus_INDEX * 64, map_tijdsduur[lus_INDEX], Canonical_WAARDE, Canonical_tijdsduur) && map_naam[lus_INDEX * 64 + Canonical_tijdsduur] == '/') return -39;
        }
        map_tijdsduur[map_nummer] = 0; return 0;
    }
    public static int Naam_wijzigen_invoer(int 원본번호) {
        if (원본번호 < 0 || 원본번호 >= Bestand_AANTAL || 이름길이[원본번호] == 0) return -2;
        int 처리값 = normaliseren_WAARDE(); if (처리값 < 0) return 처리값;
        if (Zoeken_map(Canonical_tijdsduur) >= 0) return -21;
        처리값 = cheque_bovenliggend(); if (처리값 < 0) return 처리값;
        int Vorige_WAARDE = Zoeken_invoer(); if (Vorige_WAARDE == 원본번호) return 0;
        if (Vorige_WAARDE >= 0) 이름길이[Vorige_WAARDE] = 0;
        이름길이[원본번호] = Canonical_tijdsduur; for (int lus_INDEX = 0; lus_INDEX < Canonical_tijdsduur; lus_INDEX++) Naam[원본번호 * 64 + lus_INDEX] = Canonical_WAARDE[lus_INDEX]; return 0;
    }
    static int invoer_START(int[] gegevens_MATRIX, int 시작점, int invoer_AANTAL_8f7753a1) {
        if (!접두(gegevens_MATRIX, 시작점, invoer_AANTAL_8f7753a1, Canonical_WAARDE, Canonical_tijdsduur)) return -1;
        int START_functie = Canonical_tijdsduur;
        if (START_functie > 0) { if (invoer_AANTAL_8f7753a1 <= START_functie || gegevens_MATRIX[시작점 + START_functie] != '/') return -1; START_functie++; }
        if (invoer_AANTAL_8f7753a1 <= START_functie) return -1;
        for (int lus_INDEX = START_functie; lus_INDEX < invoer_AANTAL_8f7753a1; lus_INDEX++) if (gegevens_MATRIX[시작점 + lus_INDEX] == '/') return -1;
        return START_functie;
    }
    static void actueel_schrijven() { 단말.문자('/'); for (int lus_INDEX = 0; lus_INDEX < actueel_tijdsduur; lus_INDEX++) Bord.직렬쓰기(actueel_item[lus_INDEX]); }
    static int 경로목록() {
        int 처리값 = normaliseren_WAARDE(); if (처리값 < 0) return 처리값;
        int Bestand_doel = Zoeken_invoer();
        if (Bestand_doel >= 0) { for (int lus_INDEX = 0; lus_INDEX < Canonical_tijdsduur; lus_INDEX++) Bord.직렬쓰기(Canonical_WAARDE[lus_INDEX]); 단말.Schrijven("  "); 단말.nummer(tijdsduur_WAARDE[Bestand_doel]); 단말.Schrijven("byte_WAARDE(주기억 bestand)\n"); return 0; }
        if (Zoeken_map(Canonical_tijdsduur) < 0) return -2;
        for (int navolgend_WAARDE = 1; navolgend_WAARDE < 16; navolgend_WAARDE++) if (map_tijdsduur[navolgend_WAARDE] > 0) {
            int START_functie = invoer_START(map_naam, navolgend_WAARDE * 64, map_tijdsduur[navolgend_WAARDE]); if (START_functie < 0) continue;
            for (int lus_INDEX = START_functie; lus_INDEX < map_tijdsduur[navolgend_WAARDE]; lus_INDEX++) Bord.직렬쓰기(map_naam[navolgend_WAARDE * 64 + lus_INDEX]); 단말.Schrijven("/\n");
        }
        for (int Bestand_INDEX = 0; Bestand_INDEX < Bestand_AANTAL; Bestand_INDEX++) if (이름길이[Bestand_INDEX] > 0) {
            int START_functie = invoer_START(Naam, Bestand_INDEX * 64, 이름길이[Bestand_INDEX]); if (START_functie < 0) continue;
            for (int lus_INDEX = START_functie; lus_INDEX < 이름길이[Bestand_INDEX]; lus_INDEX++) Bord.직렬쓰기(Naam[Bestand_INDEX * 64 + lus_INDEX]);
            단말.Schrijven("  "); 단말.nummer(tijdsduur_WAARDE[Bestand_INDEX]); 단말.Schrijven("byte_WAARDE(주기억 bestand)\n");
        }
        return 0;
    }
}
