// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** RAM název_souboru 64개, 파일당 16384바이트, popisovač_položka 16개. 모든 data/정책은 Java에 있다.
 * 호출 도중 양보하지 않으므로 현재의 단일 코어 협력식 작업 사이에서 원자적이다.
 * 디스크 저장이나 POSIX 전체 구현을 뜻하지 않는다. 음수 반환은 chyba 번호다.
 */
public final class Paměť_Files {
    static final int Soubor_POČET = 64;
    static int[] Název = new int[Soubor_POČET * 64];
    static int[] 이름길이 = new int[Soubor_POČET];
    // Pack four bytes in each Java int, preserving the old content heap budget.
    static int[] Obsah_HODNOTA = new int[Soubor_POČET * 4096];
    static int[] délka_HODNOTA = new int[Soubor_POČET];
    static int[] odkaz_POČET = new int[Soubor_POČET];
    static int[] použít_HODNOTA = new int[16];
    static int[] cílová_úroveň = new int[16];
    static int[] pozice = new int[16];
    static int[] metoda_MODE = new int[16];
    static int[] cesta_2 = new int[64];
    static int cesta_délka;

    public static int 파일한도() { return Soubor_POČET; }
    static int 자료읽기(int název_souboru, int poziční_index) { return (Obsah_HODNOTA[název_souboru * 4096 + poziční_index / 4] >>> ((poziční_index & 3) * 8)) & 255; }
    static void zápis_data(int název_souboru, int poziční_index, int HODNOTA) {
        int přihrádka_položka = název_souboru * 4096 + poziční_index / 4, přesunout_HODNOTA = (poziční_index & 3) * 8;
        Obsah_HODNOTA[přihrádka_položka] = (Obsah_HODNOTA[přihrádka_položka] & ~(255 << přesunout_HODNOTA)) | ((HODNOTA & 255) << přesunout_HODNOTA);
    }

    public static int cesta_START(int Velikost) {
        cesta_délka = 0;
        if (Velikost < 1 || Velikost > 63) return -36;
        cesta_délka = Velikost;
        for (int Loop_INDEX = 0; Loop_INDEX < Velikost; Loop_INDEX++) cesta_2[Loop_INDEX] = 0;
        return 0;
    }
    public static int cesta_bajt(int INDEX, int HODNOTA) {
        if (INDEX < 0 || INDEX >= cesta_délka || HODNOTA < 1 || HODNOTA > 255) return -22;
        cesta_2[INDEX] = HODNOTA; return 0;
    }
    static int NAJÍT_položka() {
        for (int Soubor_INDEX = 0; Soubor_INDEX < Soubor_POČET; Soubor_INDEX++) if (이름길이[Soubor_INDEX] > 0 && 이름길이[Soubor_INDEX] == Canonical_délka && 접두(Název, Soubor_INDEX * 64, 이름길이[Soubor_INDEX], Canonical_HODNOTA, Canonical_délka)) return Soubor_INDEX;
        return -1;
    }
    public static int Otevřít(int 플래그) {
        if (cesta_délka == 0 || (플래그 & ~0x6c3) != 0 || (플래그 & 3) == 3) return -22;
        for (int Loop_INDEX = 0; Loop_INDEX < cesta_délka; Loop_INDEX++) if (cesta_2[Loop_INDEX] == 0) return -22;
        if ((플래그 & 0x200) != 0 && (플래그 & 3) == 0) return -22;
        int VÝSLEDEK = normalizovat_HODNOTA(); if (VÝSLEDEK < 0) return VÝSLEDEK;
        if (NAJÍT_Adresář(Canonical_délka) >= 0) return -21;
        VÝSLEDEK = šek_nadřazený(); if (VÝSLEDEK < 0) return VÝSLEDEK;
        int název_souboru = NAJÍT_položka();
        if (název_souboru >= 0 && (플래그 & 0xc0) == 0xc0) return -17;
        if (název_souboru < 0 && (플래그 & 0x40) == 0) return -2;
        int popisovač_položka = -1;
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (použít_HODNOTA[Loop_INDEX] == 0) { popisovač_položka = Loop_INDEX; break; }
        if (popisovač_položka < 0) return -24;
        if (název_souboru < 0) {
            for (int Loop_INDEX = 0; Loop_INDEX < Soubor_POČET; Loop_INDEX++) if (이름길이[Loop_INDEX] == 0 && odkaz_POČET[Loop_INDEX] == 0) { název_souboru = Loop_INDEX; break; }
            if (název_souboru < 0) return -28;
            이름길이[název_souboru] = Canonical_délka;
            for (int Loop_INDEX = 0; Loop_INDEX < Canonical_délka; Loop_INDEX++) Název[název_souboru * 64 + Loop_INDEX] = Canonical_HODNOTA[Loop_INDEX];
            délka_HODNOTA[název_souboru] = 0;
        }
        if ((플래그 & 0x200) != 0) délka_HODNOTA[název_souboru] = 0;
        použít_HODNOTA[popisovač_položka] = 1; cílová_úroveň[popisovač_položka] = název_souboru; pozice[popisovač_položka] = 0; metoda_MODE[popisovač_položka] = 플래그;
        odkaz_POČET[název_souboru]++;
        return popisovač_položka + 3;
    }
    static int ověřit(int popisovač_položka) {
        return popisovač_položka >= 3 && popisovač_položka < 19 && použít_HODNOTA[popisovač_položka - 3] != 0 ? popisovač_položka - 3 : -1;
    }
    public static int Čtení(int popisovač_položka) {
        int přihrádka_položka = ověřit(popisovač_položka);
        if (přihrádka_položka < 0 || (metoda_MODE[přihrádka_položka] & 3) == 1) return -9;
        int název_souboru = cílová_úroveň[přihrádka_položka];
        if (pozice[přihrádka_položka] >= délka_HODNOTA[název_souboru]) return 256; // EOF와 skutečný_data 0x00..0xff 구별
        return 자료읽기(název_souboru, pozice[přihrádka_položka]++);
    }
    public static int Zápis(int popisovač_položka, int HODNOTA) {
        int přihrádka_položka = ověřit(popisovač_položka);
        if (přihrádka_položka < 0 || (metoda_MODE[přihrádka_položka] & 3) == 0) return -9;
        int název_souboru = cílová_úroveň[přihrádka_položka];
        if ((metoda_MODE[přihrádka_položka] & 0x400) != 0) pozice[přihrádka_položka] = délka_HODNOTA[název_souboru];
        if (pozice[přihrádka_položka] >= 16384) return -28;
        while (délka_HODNOTA[název_souboru] < pozice[přihrádka_položka]) zápis_data(název_souboru, délka_HODNOTA[název_souboru]++, 0);
        zápis_data(název_souboru, pozice[přihrádka_položka]++, HODNOTA);
        if (délka_HODNOTA[název_souboru] < pozice[přihrádka_položka]) délka_HODNOTA[název_souboru] = pozice[přihrádka_položka];
        return 1;
    }
    public static int hledat_pozice(int popisovač_položka, int 거리, int akce_kořen) {
        int přihrádka_položka = ověřit(popisovač_položka);
        if (přihrádka_položka < 0) return -9;
        if (akce_kořen < 0 || akce_kořen > 2 || 거리 < -16384 || 거리 > 16384) return -22;
        int 새위치 = 거리 + (akce_kořen == 0 ? 0 : akce_kořen == 1 ? pozice[přihrádka_položka] : délka_HODNOTA[cílová_úroveň[přihrádka_položka]]);
        if (새위치 < 0 || 새위치 > 16384) return -22;
        pozice[přihrádka_položka] = 새위치; return 새위치;
    }
    public static int Zavřené(int popisovač_položka) {
        int přihrádka_položka = ověřit(popisovač_položka);
        if (přihrádka_položka < 0) return -9;
        odkaz_POČET[cílová_úroveň[přihrádka_položka]]--; použít_HODNOTA[přihrádka_položka] = 0; return 0;
    }
    public static int Velikost(int popisovač_položka) {
        int přihrádka_položka = ověřit(popisovač_položka); return přihrádka_položka < 0 ? -9 : délka_HODNOTA[cílová_úroveň[přihrádka_položka]];
    }
    public static int sada_délka(int popisovač_položka, int Velikost) {
        int přihrádka_položka = ověřit(popisovač_položka);
        if (přihrádka_položka < 0 || (metoda_MODE[přihrádka_položka] & 3) == 0) return -9;
        if (Velikost < 0 || Velikost > 16384) return -22;
        int název_souboru = cílová_úroveň[přihrádka_položka];
        while (délka_HODNOTA[název_souboru] < Velikost) zápis_data(název_souboru, délka_HODNOTA[název_souboru]++, 0);
        délka_HODNOTA[název_souboru] = Velikost; return 0;
    }
    public static int vymazat_položka() {
        if (cesta_délka == 0) return -22;
        int VÝSLEDEK = normalizovat_HODNOTA(); if (VÝSLEDEK < 0) return VÝSLEDEK;
        if (NAJÍT_Adresář(Canonical_délka) >= 0) return -21;
        VÝSLEDEK = šek_nadřazený(); if (VÝSLEDEK < 0) return VÝSLEDEK;
        int název_souboru = NAJÍT_položka();
        if (název_souboru < 0) return -2;
        이름길이[název_souboru] = 0; return 0; // 열려 있는 파일은 마지막 close까지 유지
    }
    static void položka_Seznam() {
        cesta_START(1); cesta_bajt(0, '.'); 경로목록();
    }
    public static int 공개이름길이(int INDEX) {
        if (INDEX < 0 || INDEX >= Soubor_POČET || 이름길이[INDEX] == 0) return 0;
        for (int Loop_INDEX = 0; Loop_INDEX < 이름길이[INDEX]; Loop_INDEX++) if (Název[INDEX * 64 + Loop_INDEX] == '/') return 0;
        return 이름길이[INDEX];
    }
    public static int 공개이름바이트(int INDEX, int poziční_index) {
        return INDEX >= 0 && INDEX < Soubor_POČET && poziční_index >= 0 && poziční_index < 이름길이[INDEX] ? Název[INDEX * 64 + poziční_index] : -22;
    }
    public static int 공개파일크기(int INDEX) { return INDEX >= 0 && INDEX < Soubor_POČET ? délka_HODNOTA[INDEX] : -22; }
    static int[] Canonical_HODNOTA = new int[64], dobrá_zboží = new int[64], Adresář_název = new int[16 * 64], Adresář_délka = new int[16];
    static int Canonical_délka, dobrá_délka;
    static boolean 접두(int[] 이름들, int Spustit_2, int cesta_HODNOTA, int[] přední_fotoaparát_HODNOTA, int řádkování_cesta) {
        if (cesta_HODNOTA < řádkování_cesta) return false;
        for (int Loop_INDEX = 0; Loop_INDEX < řádkování_cesta; Loop_INDEX++) if (이름들[Spustit_2 + Loop_INDEX] != přední_fotoaparát_HODNOTA[Loop_INDEX]) return false;
        return true;
    }
    static int normalizovat_HODNOTA() {
        if (cesta_délka == 0) return -22;
        Canonical_délka = cesta_2[0] == '/' ? 0 : dobrá_délka;
        for (int Loop_INDEX = 0; Loop_INDEX < Canonical_délka; Loop_INDEX++) Canonical_HODNOTA[Loop_INDEX] = dobrá_zboží[Loop_INDEX];
        int 읽는자리 = 0;
        while (읽는자리 < cesta_délka) {
            while (읽는자리 < cesta_délka && cesta_2[읽는자리] == '/') 읽는자리++;
            int START_pozice = 읽는자리; while (읽는자리 < cesta_délka && cesta_2[읽는자리] != '/') { if (cesta_2[읽는자리] == 0) return -22; 읽는자리++; }
            int položka_POČET = 읽는자리 - START_pozice; if (položka_POČET == 0 || položka_POČET == 1 && cesta_2[START_pozice] == '.') continue;
            if (položka_POČET == 2 && cesta_2[START_pozice] == '.' && cesta_2[START_pozice + 1] == '.') {
                while (Canonical_délka > 0 && Canonical_HODNOTA[Canonical_délka - 1] != '/') Canonical_délka--;
                if (Canonical_délka > 0) Canonical_délka--;
                continue;
            }
            if (Canonical_délka + položka_POČET + (Canonical_délka == 0 ? 0 : 1) > 63) return -36;
            if (Canonical_délka > 0) Canonical_HODNOTA[Canonical_délka++] = '/';
            for (int Loop_INDEX = START_pozice; Loop_INDEX < 읽는자리; Loop_INDEX++) Canonical_HODNOTA[Canonical_délka++] = cesta_2[Loop_INDEX];
        }
        return 0;
    }
    static int NAJÍT_Adresář(int položka_POČET) {
        if (položka_POČET == 0) return 0;
        for (int Loop_INDEX = 1; Loop_INDEX < 16; Loop_INDEX++) if (Adresář_délka[Loop_INDEX] == položka_POČET && 접두(Adresář_název, Loop_INDEX * 64, položka_POČET, Canonical_HODNOTA, položka_POČET)) return Loop_INDEX;
        return -1;
    }
    static int šek_nadřazený() {
        int položka_POČET = Canonical_délka; while (položka_POČET > 0 && Canonical_HODNOTA[položka_POČET - 1] != '/') položka_POČET--;
        return NAJÍT_Adresář(položka_POČET == 0 ? 0 : položka_POČET - 1) < 0 ? -2 : 0;
    }
    public static int Create_Adresář() {
        int 처리값 = normalizovat_HODNOTA(); if (처리값 < 0) return 처리값;
        if (NAJÍT_Adresář(Canonical_délka) >= 0 || NAJÍT_položka() >= 0) return -17;
        처리값 = šek_nadřazený(); if (처리값 < 0) return 처리값;
        for (int Loop_INDEX = 1; Loop_INDEX < 16; Loop_INDEX++) if (Adresář_délka[Loop_INDEX] == 0) {
            Adresář_délka[Loop_INDEX] = Canonical_délka; for (int vnitřní_pozice = 0; vnitřní_pozice < Canonical_délka; vnitřní_pozice++) Adresář_název[Loop_INDEX * 64 + vnitřní_pozice] = Canonical_HODNOTA[vnitřní_pozice]; return 0;
        }
        return -28;
    }
    public static int položka_Druh() {
        int 처리값 = normalizovat_HODNOTA(); if (처리값 < 0) return 처리값;
        if (NAJÍT_Adresář(Canonical_délka) >= 0) return 2;
        return NAJÍT_položka() >= 0 ? 1 : 0;
    }
    public static int změnit_Adresář() {
        int 처리값 = normalizovat_HODNOTA(); if (처리값 < 0) return 처리값;
        if (NAJÍT_Adresář(Canonical_délka) < 0) return -2;
        dobrá_délka = Canonical_délka; for (int Loop_INDEX = 0; Loop_INDEX < dobrá_délka; Loop_INDEX++) dobrá_zboží[Loop_INDEX] = Canonical_HODNOTA[Loop_INDEX]; return 0;
    }
    public static int odebrat_Adresář() {
        int 처리값 = normalizovat_HODNOTA(); if (처리값 < 0) return 처리값;
        int Adresář_číslo = NAJÍT_Adresář(Canonical_délka); if (Adresář_číslo < 0) return -2; if (Adresář_číslo == 0) return -16;
        if (dobrá_délka == Canonical_délka && 접두(dobrá_zboží, 0, dobrá_délka, Canonical_HODNOTA, Canonical_délka)) return -16;
        for (int Loop_INDEX = 0; Loop_INDEX < Soubor_POČET; Loop_INDEX++) {
            if (이름길이[Loop_INDEX] > Canonical_délka && 접두(Název, Loop_INDEX * 64, 이름길이[Loop_INDEX], Canonical_HODNOTA, Canonical_délka) && Název[Loop_INDEX * 64 + Canonical_délka] == '/') return -39;
        }
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) {
            if (Adresář_délka[Loop_INDEX] > Canonical_délka && 접두(Adresář_název, Loop_INDEX * 64, Adresář_délka[Loop_INDEX], Canonical_HODNOTA, Canonical_délka) && Adresář_název[Loop_INDEX * 64 + Canonical_délka] == '/') return -39;
        }
        Adresář_délka[Adresář_číslo] = 0; return 0;
    }
    public static int Odebrat_položka(int 원본번호) {
        if (원본번호 < 0 || 원본번호 >= Soubor_POČET || 이름길이[원본번호] == 0) return -2;
        int 처리값 = normalizovat_HODNOTA(); if (처리값 < 0) return 처리값;
        if (NAJÍT_Adresář(Canonical_délka) >= 0) return -21;
        처리값 = šek_nadřazený(); if (처리값 < 0) return 처리값;
        int Předchozí_HODNOTA = NAJÍT_položka(); if (Předchozí_HODNOTA == 원본번호) return 0;
        if (Předchozí_HODNOTA >= 0) 이름길이[Předchozí_HODNOTA] = 0;
        이름길이[원본번호] = Canonical_délka; for (int Loop_INDEX = 0; Loop_INDEX < Canonical_délka; Loop_INDEX++) Název[원본번호 * 64 + Loop_INDEX] = Canonical_HODNOTA[Loop_INDEX]; return 0;
    }
    static int položka_START(int[] data_pole, int 시작점, int položka_POČET) {
        if (!접두(data_pole, 시작점, položka_POČET, Canonical_HODNOTA, Canonical_délka)) return -1;
        int START_pozice = Canonical_délka;
        if (START_pozice > 0) { if (položka_POČET <= START_pozice || data_pole[시작점 + START_pozice] != '/') return -1; START_pozice++; }
        if (položka_POČET <= START_pozice) return -1;
        for (int Loop_INDEX = START_pozice; Loop_INDEX < položka_POČET; Loop_INDEX++) if (data_pole[시작점 + Loop_INDEX] == '/') return -1;
        return START_pozice;
    }
    static void dobrá_zápis() { 단말.문자('/'); for (int Loop_INDEX = 0; Loop_INDEX < dobrá_délka; Loop_INDEX++) Panel.직렬쓰기(dobrá_zboží[Loop_INDEX]); }
    static int 경로목록() {
        int 처리값 = normalizovat_HODNOTA(); if (처리값 < 0) return 처리값;
        int Soubor_cílová_úroveň = NAJÍT_položka();
        if (Soubor_cílová_úroveň >= 0) { for (int Loop_INDEX = 0; Loop_INDEX < Canonical_délka; Loop_INDEX++) Panel.직렬쓰기(Canonical_HODNOTA[Loop_INDEX]); 단말.Zápis("  "); 단말.číslo(délka_HODNOTA[Soubor_cílová_úroveň]); 단말.Zápis("bajt_HODNOTA(주기억 název_souboru)\n"); return 0; }
        if (NAJÍT_Adresář(Canonical_délka) < 0) return -2;
        for (int 뒷값 = 1; 뒷값 < 16; 뒷값++) if (Adresář_délka[뒷값] > 0) {
            int START_pozice = položka_START(Adresář_název, 뒷값 * 64, Adresář_délka[뒷값]); if (START_pozice < 0) continue;
            for (int Loop_INDEX = START_pozice; Loop_INDEX < Adresář_délka[뒷값]; Loop_INDEX++) Panel.직렬쓰기(Adresář_název[뒷값 * 64 + Loop_INDEX]); 단말.Zápis("/\n");
        }
        for (int Soubor_INDEX = 0; Soubor_INDEX < Soubor_POČET; Soubor_INDEX++) if (이름길이[Soubor_INDEX] > 0) {
            int START_pozice = položka_START(Název, Soubor_INDEX * 64, 이름길이[Soubor_INDEX]); if (START_pozice < 0) continue;
            for (int Loop_INDEX = START_pozice; Loop_INDEX < 이름길이[Soubor_INDEX]; Loop_INDEX++) Panel.직렬쓰기(Název[Soubor_INDEX * 64 + Loop_INDEX]);
            단말.Zápis("  "); 단말.číslo(délka_HODNOTA[Soubor_INDEX]); 단말.Zápis("bajt_HODNOTA(주기억 název_souboru)\n");
        }
        return 0;
    }
}
