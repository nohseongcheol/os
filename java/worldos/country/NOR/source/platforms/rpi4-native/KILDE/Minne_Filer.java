// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** RAM Fil 64개, 파일당 16384바이트, 서술자 16개. 모든 data/정책은 Java에 있다.
 * 호출 도중 양보하지 않으므로 현재의 단일 코어 협력식 작업 사이에서 원자적이다.
 * 디스크 저장이나 POSIX 전체 구현을 뜻하지 않는다. 음수 반환은 feil 번호다.
 */
public final class Minne_Filer {
    static final int Fil_ANTALL = 64;
    static int[] Navn = new int[Fil_ANTALL * 64];
    static int[] 이름길이 = new int[Fil_ANTALL];
    // Pack four bytes in each Java int, preserving the old content heap budget.
    static int[] Innhold_VERDI = new int[Fil_ANTALL * 4096];
    static int[] lengde_VERDI = new int[Fil_ANTALL];
    static int[] referere_ANTALL = new int[Fil_ANTALL];
    static int[] bruk_VERDI = new int[16];
    static int[] mål = new int[16];
    static int[] Posisjon = new int[16];
    static int[] metode_MODUS = new int[16];
    static int[] Sti = new int[64];
    static int bane_lengde;

    public static int 파일한도() { return Fil_ANTALL; }
    static int 자료읽기(int Fil, int posisjonsindeks) { return (Innhold_VERDI[Fil * 4096 + posisjonsindeks / 4] >>> ((posisjonsindeks & 3) * 8)) & 255; }
    static void skrive_data(int Fil, int posisjonsindeks, int VERDI) {
        int åpning_oppføring = Fil * 4096 + posisjonsindeks / 4, flytte_VERDI_83b651b8 = (posisjonsindeks & 3) * 8;
        Innhold_VERDI[åpning_oppføring] = (Innhold_VERDI[åpning_oppføring] & ~(255 << flytte_VERDI_83b651b8)) | ((VERDI & 255) << flytte_VERDI_83b651b8);
    }

    public static int bane_START(int Størrelse) {
        bane_lengde = 0;
        if (Størrelse < 1 || Størrelse > 63) return -36;
        bane_lengde = Størrelse;
        for (int Loop_INDEKS = 0; Loop_INDEKS < Størrelse; Loop_INDEKS++) Sti[Loop_INDEKS] = 0;
        return 0;
    }
    public static int bane_byte(int INDEKS, int VERDI) {
        if (INDEKS < 0 || INDEKS >= bane_lengde || VERDI < 1 || VERDI > 255) return -22;
        Sti[INDEKS] = VERDI; return 0;
    }
    static int Søk_oppføring() {
        for (int Fil_INDEKS = 0; Fil_INDEKS < Fil_ANTALL; Fil_INDEKS++) if (이름길이[Fil_INDEKS] > 0 && 이름길이[Fil_INDEKS] == Canonical_lengde && 접두(Navn, Fil_INDEKS * 64, 이름길이[Fil_INDEKS], Canonical_VERDI, Canonical_lengde)) return Fil_INDEKS;
        return -1;
    }
    public static int Åpne(int 플래그) {
        if (bane_lengde == 0 || (플래그 & ~0x6c3) != 0 || (플래그 & 3) == 3) return -22;
        for (int Loop_INDEKS = 0; Loop_INDEKS < bane_lengde; Loop_INDEKS++) if (Sti[Loop_INDEKS] == 0) return -22;
        if ((플래그 & 0x200) != 0 && (플래그 & 3) == 0) return -22;
        int KR = normalisere_VERDI(); if (KR < 0) return KR;
        if (Søk_katalog(Canonical_lengde) >= 0) return -21;
        KR = sjekk_overordnet(); if (KR < 0) return KR;
        int Fil = Søk_oppføring();
        if (Fil >= 0 && (플래그 & 0xc0) == 0xc0) return -17;
        if (Fil < 0 && (플래그 & 0x40) == 0) return -2;
        int 서술자 = -1;
        for (int Loop_INDEKS = 0; Loop_INDEKS < 16; Loop_INDEKS++) if (bruk_VERDI[Loop_INDEKS] == 0) { 서술자 = Loop_INDEKS; break; }
        if (서술자 < 0) return -24;
        if (Fil < 0) {
            for (int Loop_INDEKS = 0; Loop_INDEKS < Fil_ANTALL; Loop_INDEKS++) if (이름길이[Loop_INDEKS] == 0 && referere_ANTALL[Loop_INDEKS] == 0) { Fil = Loop_INDEKS; break; }
            if (Fil < 0) return -28;
            이름길이[Fil] = Canonical_lengde;
            for (int Loop_INDEKS = 0; Loop_INDEKS < Canonical_lengde; Loop_INDEKS++) Navn[Fil * 64 + Loop_INDEKS] = Canonical_VERDI[Loop_INDEKS];
            lengde_VERDI[Fil] = 0;
        }
        if ((플래그 & 0x200) != 0) lengde_VERDI[Fil] = 0;
        bruk_VERDI[서술자] = 1; mål[서술자] = Fil; Posisjon[서술자] = 0; metode_MODUS[서술자] = 플래그;
        referere_ANTALL[Fil]++;
        return 서술자 + 3;
    }
    static int bekrefte(int 서술자) {
        return 서술자 >= 3 && 서술자 < 19 && bruk_VERDI[서술자 - 3] != 0 ? 서술자 - 3 : -1;
    }
    public static int Les(int 서술자) {
        int åpning_oppføring = bekrefte(서술자);
        if (åpning_oppføring < 0 || (metode_MODUS[åpning_oppføring] & 3) == 1) return -9;
        int Fil = mål[åpning_oppføring];
        if (Posisjon[åpning_oppføring] >= lengde_VERDI[Fil]) return 256; // EOF와 faktisk_data 0x00..0xff 구별
        return 자료읽기(Fil, Posisjon[åpning_oppføring]++);
    }
    public static int Skriv(int 서술자, int VERDI) {
        int åpning_oppføring = bekrefte(서술자);
        if (åpning_oppføring < 0 || (metode_MODUS[åpning_oppføring] & 3) == 0) return -9;
        int Fil = mål[åpning_oppføring];
        if ((metode_MODUS[åpning_oppføring] & 0x400) != 0) Posisjon[åpning_oppføring] = lengde_VERDI[Fil];
        if (Posisjon[åpning_oppføring] >= 16384) return -28;
        while (lengde_VERDI[Fil] < Posisjon[åpning_oppføring]) skrive_data(Fil, lengde_VERDI[Fil]++, 0);
        skrive_data(Fil, Posisjon[åpning_oppføring]++, VERDI);
        if (lengde_VERDI[Fil] < Posisjon[åpning_oppføring]) lengde_VERDI[Fil] = Posisjon[åpning_oppføring];
        return 1;
    }
    public static int søk_plassere(int 서술자, int 거리, int speile_rot) {
        int åpning_oppføring = bekrefte(서술자);
        if (åpning_oppføring < 0) return -9;
        if (speile_rot < 0 || speile_rot > 2 || 거리 < -16384 || 거리 > 16384) return -22;
        int 새위치 = 거리 + (speile_rot == 0 ? 0 : speile_rot == 1 ? Posisjon[åpning_oppføring] : lengde_VERDI[mål[åpning_oppføring]]);
        if (새위치 < 0 || 새위치 > 16384) return -22;
        Posisjon[åpning_oppføring] = 새위치; return 새위치;
    }
    public static int Lukk(int 서술자) {
        int åpning_oppføring = bekrefte(서술자);
        if (åpning_oppføring < 0) return -9;
        referere_ANTALL[mål[åpning_oppføring]]--; bruk_VERDI[åpning_oppføring] = 0; return 0;
    }
    public static int Størrelse(int 서술자) {
        int åpning_oppføring = bekrefte(서술자); return åpning_oppføring < 0 ? -9 : lengde_VERDI[mål[åpning_oppføring]];
    }
    public static int sett_lengde(int 서술자, int Størrelse) {
        int åpning_oppføring = bekrefte(서술자);
        if (åpning_oppføring < 0 || (metode_MODUS[åpning_oppføring] & 3) == 0) return -9;
        if (Størrelse < 0 || Størrelse > 16384) return -22;
        int Fil = mål[åpning_oppføring];
        while (lengde_VERDI[Fil] < Størrelse) skrive_data(Fil, lengde_VERDI[Fil]++, 0);
        lengde_VERDI[Fil] = Størrelse; return 0;
    }
    public static int slette_oppføring() {
        if (bane_lengde == 0) return -22;
        int KR = normalisere_VERDI(); if (KR < 0) return KR;
        if (Søk_katalog(Canonical_lengde) >= 0) return -21;
        KR = sjekk_overordnet(); if (KR < 0) return KR;
        int Fil = Søk_oppføring();
        if (Fil < 0) return -2;
        이름길이[Fil] = 0; return 0; // 열려 있는 파일은 마지막 close까지 유지
    }
    static void oppføring_Liste() {
        bane_START(1); bane_byte(0, '.'); 경로목록();
    }
    public static int 공개이름길이(int INDEKS) {
        if (INDEKS < 0 || INDEKS >= Fil_ANTALL || 이름길이[INDEKS] == 0) return 0;
        for (int Loop_INDEKS = 0; Loop_INDEKS < 이름길이[INDEKS]; Loop_INDEKS++) if (Navn[INDEKS * 64 + Loop_INDEKS] == '/') return 0;
        return 이름길이[INDEKS];
    }
    public static int 공개이름바이트(int INDEKS, int posisjonsindeks) {
        return INDEKS >= 0 && INDEKS < Fil_ANTALL && posisjonsindeks >= 0 && posisjonsindeks < 이름길이[INDEKS] ? Navn[INDEKS * 64 + posisjonsindeks] : -22;
    }
    public static int 공개파일크기(int INDEKS) { return INDEKS >= 0 && INDEKS < Fil_ANTALL ? lengde_VERDI[INDEKS] : -22; }
    static int[] Canonical_VERDI = new int[64], betalt_vare = new int[64], katalog_navn = new int[16 * 64], katalog_lengde = new int[16];
    static int Canonical_lengde, betalt_lengde;
    static boolean 접두(int[] 이름들, int Kjør_2, int bane_VERDI, int[] frontkamera_VERDI, int linjeavstand_bane) {
        if (bane_VERDI < linjeavstand_bane) return false;
        for (int Loop_INDEKS = 0; Loop_INDEKS < linjeavstand_bane; Loop_INDEKS++) if (이름들[Kjør_2 + Loop_INDEKS] != frontkamera_VERDI[Loop_INDEKS]) return false;
        return true;
    }
    static int normalisere_VERDI() {
        if (bane_lengde == 0) return -22;
        Canonical_lengde = Sti[0] == '/' ? 0 : betalt_lengde;
        for (int Loop_INDEKS = 0; Loop_INDEKS < Canonical_lengde; Loop_INDEKS++) Canonical_VERDI[Loop_INDEKS] = betalt_vare[Loop_INDEKS];
        int 읽는자리 = 0;
        while (읽는자리 < bane_lengde) {
            while (읽는자리 < bane_lengde && Sti[읽는자리] == '/') 읽는자리++;
            int START_plassere = 읽는자리; while (읽는자리 < bane_lengde && Sti[읽는자리] != '/') { if (Sti[읽는자리] == 0) return -22; 읽는자리++; }
            int oppføring_ANTALL = 읽는자리 - START_plassere; if (oppføring_ANTALL == 0 || oppføring_ANTALL == 1 && Sti[START_plassere] == '.') continue;
            if (oppføring_ANTALL == 2 && Sti[START_plassere] == '.' && Sti[START_plassere + 1] == '.') {
                while (Canonical_lengde > 0 && Canonical_VERDI[Canonical_lengde - 1] != '/') Canonical_lengde--;
                if (Canonical_lengde > 0) Canonical_lengde--;
                continue;
            }
            if (Canonical_lengde + oppføring_ANTALL + (Canonical_lengde == 0 ? 0 : 1) > 63) return -36;
            if (Canonical_lengde > 0) Canonical_VERDI[Canonical_lengde++] = '/';
            for (int Loop_INDEKS = START_plassere; Loop_INDEKS < 읽는자리; Loop_INDEKS++) Canonical_VERDI[Canonical_lengde++] = Sti[Loop_INDEKS];
        }
        return 0;
    }
    static int Søk_katalog(int oppføring_ANTALL) {
        if (oppføring_ANTALL == 0) return 0;
        for (int Loop_INDEKS = 1; Loop_INDEKS < 16; Loop_INDEKS++) if (katalog_lengde[Loop_INDEKS] == oppføring_ANTALL && 접두(katalog_navn, Loop_INDEKS * 64, oppføring_ANTALL, Canonical_VERDI, oppføring_ANTALL)) return Loop_INDEKS;
        return -1;
    }
    static int sjekk_overordnet() {
        int oppføring_ANTALL = Canonical_lengde; while (oppføring_ANTALL > 0 && Canonical_VERDI[oppføring_ANTALL - 1] != '/') oppføring_ANTALL--;
        return Søk_katalog(oppføring_ANTALL == 0 ? 0 : oppføring_ANTALL - 1) < 0 ? -2 : 0;
    }
    public static int åpne_katalog() {
        int 처리값 = normalisere_VERDI(); if (처리값 < 0) return 처리값;
        if (Søk_katalog(Canonical_lengde) >= 0 || Søk_oppføring() >= 0) return -17;
        처리값 = sjekk_overordnet(); if (처리값 < 0) return 처리값;
        for (int Loop_INDEKS = 1; Loop_INDEKS < 16; Loop_INDEKS++) if (katalog_lengde[Loop_INDEKS] == 0) {
            katalog_lengde[Loop_INDEKS] = Canonical_lengde; for (int indre_kobling_plassere = 0; indre_kobling_plassere < Canonical_lengde; indre_kobling_plassere++) katalog_navn[Loop_INDEKS * 64 + indre_kobling_plassere] = Canonical_VERDI[indre_kobling_plassere]; return 0;
        }
        return -28;
    }
    public static int 항목종류() {
        int 처리값 = normalisere_VERDI(); if (처리값 < 0) return 처리값;
        if (Søk_katalog(Canonical_lengde) >= 0) return 2;
        return Søk_oppføring() >= 0 ? 1 : 0;
    }
    public static int endre_katalog() {
        int 처리값 = normalisere_VERDI(); if (처리값 < 0) return 처리값;
        if (Søk_katalog(Canonical_lengde) < 0) return -2;
        betalt_lengde = Canonical_lengde; for (int Loop_INDEKS = 0; Loop_INDEKS < betalt_lengde; Loop_INDEKS++) betalt_vare[Loop_INDEKS] = Canonical_VERDI[Loop_INDEKS]; return 0;
    }
    public static int fjerne_katalog() {
        int 처리값 = normalisere_VERDI(); if (처리값 < 0) return 처리값;
        int katalog_nummer = Søk_katalog(Canonical_lengde); if (katalog_nummer < 0) return -2; if (katalog_nummer == 0) return -16;
        if (betalt_lengde == Canonical_lengde && 접두(betalt_vare, 0, betalt_lengde, Canonical_VERDI, Canonical_lengde)) return -16;
        for (int Loop_INDEKS = 0; Loop_INDEKS < Fil_ANTALL; Loop_INDEKS++) {
            if (이름길이[Loop_INDEKS] > Canonical_lengde && 접두(Navn, Loop_INDEKS * 64, 이름길이[Loop_INDEKS], Canonical_VERDI, Canonical_lengde) && Navn[Loop_INDEKS * 64 + Canonical_lengde] == '/') return -39;
        }
        for (int Loop_INDEKS = 0; Loop_INDEKS < 16; Loop_INDEKS++) {
            if (katalog_lengde[Loop_INDEKS] > Canonical_lengde && 접두(katalog_navn, Loop_INDEKS * 64, katalog_lengde[Loop_INDEKS], Canonical_VERDI, Canonical_lengde) && katalog_navn[Loop_INDEKS * 64 + Canonical_lengde] == '/') return -39;
        }
        katalog_lengde[katalog_nummer] = 0; return 0;
    }
    public static int Gi_nytt_navn_oppføring(int 원본번호) {
        if (원본번호 < 0 || 원본번호 >= Fil_ANTALL || 이름길이[원본번호] == 0) return -2;
        int 처리값 = normalisere_VERDI(); if (처리값 < 0) return 처리값;
        if (Søk_katalog(Canonical_lengde) >= 0) return -21;
        처리값 = sjekk_overordnet(); if (처리값 < 0) return 처리값;
        int Forrige_VERDI = Søk_oppføring(); if (Forrige_VERDI == 원본번호) return 0;
        if (Forrige_VERDI >= 0) 이름길이[Forrige_VERDI] = 0;
        이름길이[원본번호] = Canonical_lengde; for (int Loop_INDEKS = 0; Loop_INDEKS < Canonical_lengde; Loop_INDEKS++) Navn[원본번호 * 64 + Loop_INDEKS] = Canonical_VERDI[Loop_INDEKS]; return 0;
    }
    static int oppføring_START(int[] data_MATRISE, int 시작점, int oppføring_ANTALL) {
        if (!접두(data_MATRISE, 시작점, oppføring_ANTALL, Canonical_VERDI, Canonical_lengde)) return -1;
        int START_plassere = Canonical_lengde;
        if (START_plassere > 0) { if (oppføring_ANTALL <= START_plassere || data_MATRISE[시작점 + START_plassere] != '/') return -1; START_plassere++; }
        if (oppføring_ANTALL <= START_plassere) return -1;
        for (int Loop_INDEKS = START_plassere; Loop_INDEKS < oppføring_ANTALL; Loop_INDEKS++) if (data_MATRISE[시작점 + Loop_INDEKS] == '/') return -1;
        return START_plassere;
    }
    static void betalt_skrive() { 단말.문자('/'); for (int Loop_INDEKS = 0; Loop_INDEKS < betalt_lengde; Loop_INDEKS++) Tavle.직렬쓰기(betalt_vare[Loop_INDEKS]); }
    static int 경로목록() {
        int 처리값 = normalisere_VERDI(); if (처리값 < 0) return 처리값;
        int Fil_mål = Søk_oppføring();
        if (Fil_mål >= 0) { for (int Loop_INDEKS = 0; Loop_INDEKS < Canonical_lengde; Loop_INDEKS++) Tavle.직렬쓰기(Canonical_VERDI[Loop_INDEKS]); 단말.Skriv("  "); 단말.nummer(lengde_VERDI[Fil_mål]); 단말.Skriv("byte_VERDI(주기억 Fil)\n"); return 0; }
        if (Søk_katalog(Canonical_lengde) < 0) return -2;
        for (int 뒷값 = 1; 뒷값 < 16; 뒷값++) if (katalog_lengde[뒷값] > 0) {
            int START_plassere = oppføring_START(katalog_navn, 뒷값 * 64, katalog_lengde[뒷값]); if (START_plassere < 0) continue;
            for (int Loop_INDEKS = START_plassere; Loop_INDEKS < katalog_lengde[뒷값]; Loop_INDEKS++) Tavle.직렬쓰기(katalog_navn[뒷값 * 64 + Loop_INDEKS]); 단말.Skriv("/\n");
        }
        for (int Fil_INDEKS = 0; Fil_INDEKS < Fil_ANTALL; Fil_INDEKS++) if (이름길이[Fil_INDEKS] > 0) {
            int START_plassere = oppføring_START(Navn, Fil_INDEKS * 64, 이름길이[Fil_INDEKS]); if (START_plassere < 0) continue;
            for (int Loop_INDEKS = START_plassere; Loop_INDEKS < 이름길이[Fil_INDEKS]; Loop_INDEKS++) Tavle.직렬쓰기(Navn[Fil_INDEKS * 64 + Loop_INDEKS]);
            단말.Skriv("  "); 단말.nummer(lengde_VERDI[Fil_INDEKS]); 단말.Skriv("byte_VERDI(주기억 Fil)\n");
        }
        return 0;
    }
}
