// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** RAM filnamn 64개, 파일당 16384바이트, 서술자 16개. 모든 data/정책은 Java에 있다.
 * 호출 도중 양보하지 않으므로 현재의 단일 코어 협력식 작업 사이에서 원자적이다.
 * 디스크 저장이나 POSIX 전체 구현을 뜻하지 않는다. 음수 반환은 fel 번호다.
 */
public final class Minne_Filer {
    static final int fil_ANTAL = 64;
    static int[] Namn = new int[fil_ANTAL * 64];
    static int[] 이름길이 = new int[fil_ANTAL];
    // Pack four bytes in each Java int, preserving the old content heap budget.
    static int[] Innehåll_värde = new int[fil_ANTAL * 4096];
    static int[] längd_värde = new int[fil_ANTAL];
    static int[] referens_ANTAL = new int[fil_ANTAL];
    static int[] använda_värde = new int[16];
    static int[] mål = new int[16];
    static int[] position = new int[16];
    static int[] metod_läge = new int[16];
    static int[] sökväg_2 = new int[64];
    static int väg_längd;

    public static int 파일한도() { return fil_ANTAL; }
    static int läsa_data(int filnamn, int positionsindex) { return (Innehåll_värde[filnamn * 4096 + positionsindex / 4] >>> ((positionsindex & 3) * 8)) & 255; }
    static void skriva_data(int filnamn, int positionsindex, int värde) {
        int fack_post = filnamn * 4096 + positionsindex / 4, flytta_värde = (positionsindex & 3) * 8;
        Innehåll_värde[fack_post] = (Innehåll_värde[fack_post] & ~(255 << flytta_värde)) | ((värde & 255) << flytta_värde);
    }

    public static int väg_START(int Storlek) {
        väg_längd = 0;
        if (Storlek < 1 || Storlek > 63) return -36;
        väg_längd = Storlek;
        for (int Loop_INDEX = 0; Loop_INDEX < Storlek; Loop_INDEX++) sökväg_2[Loop_INDEX] = 0;
        return 0;
    }
    public static int väg_byte(int INDEX, int värde) {
        if (INDEX < 0 || INDEX >= väg_längd || värde < 1 || värde > 255) return -22;
        sökväg_2[INDEX] = värde; return 0;
    }
    static int Sök_post() {
        for (int fil_INDEX = 0; fil_INDEX < fil_ANTAL; fil_INDEX++) if (이름길이[fil_INDEX] > 0 && 이름길이[fil_INDEX] == Canonical_längd && 접두(Namn, fil_INDEX * 64, 이름길이[fil_INDEX], Canonical_värde, Canonical_längd)) return fil_INDEX;
        return -1;
    }
    public static int Öppna(int 플래그) {
        if (väg_längd == 0 || (플래그 & ~0x6c3) != 0 || (플래그 & 3) == 3) return -22;
        for (int Loop_INDEX = 0; Loop_INDEX < väg_längd; Loop_INDEX++) if (sökväg_2[Loop_INDEX] == 0) return -22;
        if ((플래그 & 0x200) != 0 && (플래그 & 3) == 0) return -22;
        int RESULTAT = normalisera_värde(); if (RESULTAT < 0) return RESULTAT;
        if (Sök_Katalog(Canonical_längd) >= 0) return -21;
        RESULTAT = check_överordnad(); if (RESULTAT < 0) return RESULTAT;
        int filnamn = Sök_post();
        if (filnamn >= 0 && (플래그 & 0xc0) == 0xc0) return -17;
        if (filnamn < 0 && (플래그 & 0x40) == 0) return -2;
        int 서술자 = -1;
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (använda_värde[Loop_INDEX] == 0) { 서술자 = Loop_INDEX; break; }
        if (서술자 < 0) return -24;
        if (filnamn < 0) {
            for (int Loop_INDEX = 0; Loop_INDEX < fil_ANTAL; Loop_INDEX++) if (이름길이[Loop_INDEX] == 0 && referens_ANTAL[Loop_INDEX] == 0) { filnamn = Loop_INDEX; break; }
            if (filnamn < 0) return -28;
            이름길이[filnamn] = Canonical_längd;
            for (int Loop_INDEX = 0; Loop_INDEX < Canonical_längd; Loop_INDEX++) Namn[filnamn * 64 + Loop_INDEX] = Canonical_värde[Loop_INDEX];
            längd_värde[filnamn] = 0;
        }
        if ((플래그 & 0x200) != 0) längd_värde[filnamn] = 0;
        använda_värde[서술자] = 1; mål[서술자] = filnamn; position[서술자] = 0; metod_läge[서술자] = 플래그;
        referens_ANTAL[filnamn]++;
        return 서술자 + 3;
    }
    static int verifiera(int 서술자) {
        return 서술자 >= 3 && 서술자 < 19 && använda_värde[서술자 - 3] != 0 ? 서술자 - 3 : -1;
    }
    public static int Läs(int 서술자) {
        int fack_post = verifiera(서술자);
        if (fack_post < 0 || (metod_läge[fack_post] & 3) == 1) return -9;
        int filnamn = mål[fack_post];
        if (position[fack_post] >= längd_värde[filnamn]) return 256; // EOF와 verklig_data 0x00..0xff 구별
        return läsa_data(filnamn, position[fack_post]++);
    }
    public static int Skriv(int 서술자, int värde) {
        int fack_post = verifiera(서술자);
        if (fack_post < 0 || (metod_läge[fack_post] & 3) == 0) return -9;
        int filnamn = mål[fack_post];
        if ((metod_läge[fack_post] & 0x400) != 0) position[fack_post] = längd_värde[filnamn];
        if (position[fack_post] >= 16384) return -28;
        while (längd_värde[filnamn] < position[fack_post]) skriva_data(filnamn, längd_värde[filnamn]++, 0);
        skriva_data(filnamn, position[fack_post]++, värde);
        if (längd_värde[filnamn] < position[fack_post]) längd_värde[filnamn] = position[fack_post];
        return 1;
    }
    public static int söka_placera(int 서술자, int 거리, int åtgärd_rot) {
        int fack_post = verifiera(서술자);
        if (fack_post < 0) return -9;
        if (åtgärd_rot < 0 || åtgärd_rot > 2 || 거리 < -16384 || 거리 > 16384) return -22;
        int 새위치 = 거리 + (åtgärd_rot == 0 ? 0 : åtgärd_rot == 1 ? position[fack_post] : längd_värde[mål[fack_post]]);
        if (새위치 < 0 || 새위치 > 16384) return -22;
        position[fack_post] = 새위치; return 새위치;
    }
    public static int Stäng(int 서술자) {
        int fack_post = verifiera(서술자);
        if (fack_post < 0) return -9;
        referens_ANTAL[mål[fack_post]]--; använda_värde[fack_post] = 0; return 0;
    }
    public static int Storlek(int 서술자) {
        int fack_post = verifiera(서술자); return fack_post < 0 ? -9 : längd_värde[mål[fack_post]];
    }
    public static int uppsättning_längd(int 서술자, int Storlek) {
        int fack_post = verifiera(서술자);
        if (fack_post < 0 || (metod_läge[fack_post] & 3) == 0) return -9;
        if (Storlek < 0 || Storlek > 16384) return -22;
        int filnamn = mål[fack_post];
        while (längd_värde[filnamn] < Storlek) skriva_data(filnamn, längd_värde[filnamn]++, 0);
        längd_värde[filnamn] = Storlek; return 0;
    }
    public static int radera_post() {
        if (väg_längd == 0) return -22;
        int RESULTAT = normalisera_värde(); if (RESULTAT < 0) return RESULTAT;
        if (Sök_Katalog(Canonical_längd) >= 0) return -21;
        RESULTAT = check_överordnad(); if (RESULTAT < 0) return RESULTAT;
        int filnamn = Sök_post();
        if (filnamn < 0) return -2;
        이름길이[filnamn] = 0; return 0; // 열려 있는 파일은 마지막 close까지 유지
    }
    static void post_ange() {
        väg_START(1); väg_byte(0, '.'); 경로목록();
    }
    public static int 공개이름길이(int INDEX) {
        if (INDEX < 0 || INDEX >= fil_ANTAL || 이름길이[INDEX] == 0) return 0;
        for (int Loop_INDEX = 0; Loop_INDEX < 이름길이[INDEX]; Loop_INDEX++) if (Namn[INDEX * 64 + Loop_INDEX] == '/') return 0;
        return 이름길이[INDEX];
    }
    public static int 공개이름바이트(int INDEX, int positionsindex) {
        return INDEX >= 0 && INDEX < fil_ANTAL && positionsindex >= 0 && positionsindex < 이름길이[INDEX] ? Namn[INDEX * 64 + positionsindex] : -22;
    }
    public static int 공개파일크기(int INDEX) { return INDEX >= 0 && INDEX < fil_ANTAL ? längd_värde[INDEX] : -22; }
    static int[] Canonical_värde = new int[64], aktuellt_objekt = new int[64], Katalog_namn = new int[16 * 64], Katalog_längd = new int[16];
    static int Canonical_längd, aktuellt_längd;
    static boolean 접두(int[] 이름들, int Kör, int väg_värde, int[] framåtvänd_värde, int avstånd_väg) {
        if (väg_värde < avstånd_väg) return false;
        for (int Loop_INDEX = 0; Loop_INDEX < avstånd_väg; Loop_INDEX++) if (이름들[Kör + Loop_INDEX] != framåtvänd_värde[Loop_INDEX]) return false;
        return true;
    }
    static int normalisera_värde() {
        if (väg_längd == 0) return -22;
        Canonical_längd = sökväg_2[0] == '/' ? 0 : aktuellt_längd;
        for (int Loop_INDEX = 0; Loop_INDEX < Canonical_längd; Loop_INDEX++) Canonical_värde[Loop_INDEX] = aktuellt_objekt[Loop_INDEX];
        int läsa_markör = 0;
        while (läsa_markör < väg_längd) {
            while (läsa_markör < väg_längd && sökväg_2[läsa_markör] == '/') läsa_markör++;
            int START_placera = läsa_markör; while (läsa_markör < väg_längd && sökväg_2[läsa_markör] != '/') { if (sökväg_2[läsa_markör] == 0) return -22; läsa_markör++; }
            int post_ANTAL = läsa_markör - START_placera; if (post_ANTAL == 0 || post_ANTAL == 1 && sökväg_2[START_placera] == '.') continue;
            if (post_ANTAL == 2 && sökväg_2[START_placera] == '.' && sökväg_2[START_placera + 1] == '.') {
                while (Canonical_längd > 0 && Canonical_värde[Canonical_längd - 1] != '/') Canonical_längd--;
                if (Canonical_längd > 0) Canonical_längd--;
                continue;
            }
            if (Canonical_längd + post_ANTAL + (Canonical_längd == 0 ? 0 : 1) > 63) return -36;
            if (Canonical_längd > 0) Canonical_värde[Canonical_längd++] = '/';
            for (int Loop_INDEX = START_placera; Loop_INDEX < läsa_markör; Loop_INDEX++) Canonical_värde[Canonical_längd++] = sökväg_2[Loop_INDEX];
        }
        return 0;
    }
    static int Sök_Katalog(int post_ANTAL) {
        if (post_ANTAL == 0) return 0;
        for (int Loop_INDEX = 1; Loop_INDEX < 16; Loop_INDEX++) if (Katalog_längd[Loop_INDEX] == post_ANTAL && 접두(Katalog_namn, Loop_INDEX * 64, post_ANTAL, Canonical_värde, post_ANTAL)) return Loop_INDEX;
        return -1;
    }
    static int check_överordnad() {
        int post_ANTAL = Canonical_längd; while (post_ANTAL > 0 && Canonical_värde[post_ANTAL - 1] != '/') post_ANTAL--;
        return Sök_Katalog(post_ANTAL == 0 ? 0 : post_ANTAL - 1) < 0 ? -2 : 0;
    }
    public static int Skapa_Katalog() {
        int 처리값 = normalisera_värde(); if (처리값 < 0) return 처리값;
        if (Sök_Katalog(Canonical_längd) >= 0 || Sök_post() >= 0) return -17;
        처리값 = check_överordnad(); if (처리값 < 0) return 처리값;
        for (int Loop_INDEX = 1; Loop_INDEX < 16; Loop_INDEX++) if (Katalog_längd[Loop_INDEX] == 0) {
            Katalog_längd[Loop_INDEX] = Canonical_längd; for (int inre_koppling_placera = 0; inre_koppling_placera < Canonical_längd; inre_koppling_placera++) Katalog_namn[Loop_INDEX * 64 + inre_koppling_placera] = Canonical_värde[inre_koppling_placera]; return 0;
        }
        return -28;
    }
    public static int post_variant() {
        int 처리값 = normalisera_värde(); if (처리값 < 0) return 처리값;
        if (Sök_Katalog(Canonical_längd) >= 0) return 2;
        return Sök_post() >= 0 ? 1 : 0;
    }
    public static int ändra_Katalog() {
        int 처리값 = normalisera_värde(); if (처리값 < 0) return 처리값;
        if (Sök_Katalog(Canonical_längd) < 0) return -2;
        aktuellt_längd = Canonical_längd; for (int Loop_INDEX = 0; Loop_INDEX < aktuellt_längd; Loop_INDEX++) aktuellt_objekt[Loop_INDEX] = Canonical_värde[Loop_INDEX]; return 0;
    }
    public static int ta_bort_Katalog() {
        int 처리값 = normalisera_värde(); if (처리값 < 0) return 처리값;
        int Katalog_nummer = Sök_Katalog(Canonical_längd); if (Katalog_nummer < 0) return -2; if (Katalog_nummer == 0) return -16;
        if (aktuellt_längd == Canonical_längd && 접두(aktuellt_objekt, 0, aktuellt_längd, Canonical_värde, Canonical_längd)) return -16;
        for (int Loop_INDEX = 0; Loop_INDEX < fil_ANTAL; Loop_INDEX++) {
            if (이름길이[Loop_INDEX] > Canonical_längd && 접두(Namn, Loop_INDEX * 64, 이름길이[Loop_INDEX], Canonical_värde, Canonical_längd) && Namn[Loop_INDEX * 64 + Canonical_längd] == '/') return -39;
        }
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) {
            if (Katalog_längd[Loop_INDEX] > Canonical_längd && 접두(Katalog_namn, Loop_INDEX * 64, Katalog_längd[Loop_INDEX], Canonical_värde, Canonical_längd) && Katalog_namn[Loop_INDEX * 64 + Canonical_längd] == '/') return -39;
        }
        Katalog_längd[Katalog_nummer] = 0; return 0;
    }
    public static int Byt_namn_post(int 원본번호) {
        if (원본번호 < 0 || 원본번호 >= fil_ANTAL || 이름길이[원본번호] == 0) return -2;
        int 처리값 = normalisera_värde(); if (처리값 < 0) return 처리값;
        if (Sök_Katalog(Canonical_längd) >= 0) return -21;
        처리값 = check_överordnad(); if (처리값 < 0) return 처리값;
        int Föregående_värde = Sök_post(); if (Föregående_värde == 원본번호) return 0;
        if (Föregående_värde >= 0) 이름길이[Föregående_värde] = 0;
        이름길이[원본번호] = Canonical_längd; for (int Loop_INDEX = 0; Loop_INDEX < Canonical_längd; Loop_INDEX++) Namn[원본번호 * 64 + Loop_INDEX] = Canonical_värde[Loop_INDEX]; return 0;
    }
    static int post_START(int[] data_MATRIS, int 시작점, int post_ANTAL) {
        if (!접두(data_MATRIS, 시작점, post_ANTAL, Canonical_värde, Canonical_längd)) return -1;
        int START_placera = Canonical_längd;
        if (START_placera > 0) { if (post_ANTAL <= START_placera || data_MATRIS[시작점 + START_placera] != '/') return -1; START_placera++; }
        if (post_ANTAL <= START_placera) return -1;
        for (int Loop_INDEX = START_placera; Loop_INDEX < post_ANTAL; Loop_INDEX++) if (data_MATRIS[시작점 + Loop_INDEX] == '/') return -1;
        return START_placera;
    }
    static void aktuellt_skriva() { 단말.문자('/'); for (int Loop_INDEX = 0; Loop_INDEX < aktuellt_längd; Loop_INDEX++) Tavla.직렬쓰기(aktuellt_objekt[Loop_INDEX]); }
    static int 경로목록() {
        int 처리값 = normalisera_värde(); if (처리값 < 0) return 처리값;
        int fil_mål = Sök_post();
        if (fil_mål >= 0) { for (int Loop_INDEX = 0; Loop_INDEX < Canonical_längd; Loop_INDEX++) Tavla.직렬쓰기(Canonical_värde[Loop_INDEX]); 단말.Skriv("  "); 단말.nummer(längd_värde[fil_mål]); 단말.Skriv("byte_värde(주기억 filnamn)\n"); return 0; }
        if (Sök_Katalog(Canonical_längd) < 0) return -2;
        for (int 뒷값 = 1; 뒷값 < 16; 뒷값++) if (Katalog_längd[뒷값] > 0) {
            int START_placera = post_START(Katalog_namn, 뒷값 * 64, Katalog_längd[뒷값]); if (START_placera < 0) continue;
            for (int Loop_INDEX = START_placera; Loop_INDEX < Katalog_längd[뒷값]; Loop_INDEX++) Tavla.직렬쓰기(Katalog_namn[뒷값 * 64 + Loop_INDEX]); 단말.Skriv("/\n");
        }
        for (int fil_INDEX = 0; fil_INDEX < fil_ANTAL; fil_INDEX++) if (이름길이[fil_INDEX] > 0) {
            int START_placera = post_START(Namn, fil_INDEX * 64, 이름길이[fil_INDEX]); if (START_placera < 0) continue;
            for (int Loop_INDEX = START_placera; Loop_INDEX < 이름길이[fil_INDEX]; Loop_INDEX++) Tavla.직렬쓰기(Namn[fil_INDEX * 64 + Loop_INDEX]);
            단말.Skriv("  "); 단말.nummer(längd_värde[fil_INDEX]); 단말.Skriv("byte_värde(주기억 filnamn)\n");
        }
        return 0;
    }
}
