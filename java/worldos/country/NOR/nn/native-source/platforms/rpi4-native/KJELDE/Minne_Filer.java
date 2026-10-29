// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** RAM Fil 64개, 파일당 16384바이트, 서술자 16개. 모든 data/정책은 Java에 있다.
 * 호출 도중 양보하지 않으므로 현재의 단일 코어 협력식 작업 사이에서 원자적이다.
 * 디스크 저장이나 POSIX 전체 구현을 뜻하지 않는다. 음수 반환은 FEIL 번호다.
 */
public final class Minne_Filer {
    static final int fil_COUNT = 64;
    static int[] Namn = new int[fil_COUNT * 64];
    static int[] 이름길이 = new int[fil_COUNT];
    // Pack four bytes in each Java int, preserving the old content heap budget.
    static int[] Innhald_VALUE = new int[fil_COUNT * 4096];
    static int[] lengd_VALUE = new int[fil_COUNT];
    static int[] Oppslagsverk_COUNT = new int[fil_COUNT];
    static int[] 사용 = new int[16];
    static int[] mål = new int[16];
    static int[] Posisjon = new int[16];
    static int[] metode_MODE = new int[16];
    static int[] STIGE = new int[64];
    static int bane_lengd;

    public static int 파일한도() { return fil_COUNT; }
    static int 자료읽기(int Fil, int plassere_INDEX) { return (Innhald_VALUE[Fil * 4096 + plassere_INDEX / 4] >>> ((plassere_INDEX & 3) * 8)) & 255; }
    static void skrive_data(int Fil, int plassere_INDEX, int VALUE) {
        int felt_oppføring = Fil * 4096 + plassere_INDEX / 4, flytte_VALUE = (plassere_INDEX & 3) * 8;
        Innhald_VALUE[felt_oppføring] = (Innhald_VALUE[felt_oppføring] & ~(255 << flytte_VALUE)) | ((VALUE & 255) << flytte_VALUE);
    }

    public static int bane_START(int Storleik) {
        bane_lengd = 0;
        if (Storleik < 1 || Storleik > 63) return -36;
        bane_lengd = Storleik;
        for (int Loop_INDEX = 0; Loop_INDEX < Storleik; Loop_INDEX++) STIGE[Loop_INDEX] = 0;
        return 0;
    }
    public static int bane_byte(int INDEX, int VALUE) {
        if (INDEX < 0 || INDEX >= bane_lengd || VALUE < 1 || VALUE > 255) return -22;
        STIGE[INDEX] = VALUE; return 0;
    }
    static int Søk_oppføring() {
        for (int fil_INDEX = 0; fil_INDEX < fil_COUNT; fil_INDEX++) if (이름길이[fil_INDEX] > 0 && 이름길이[fil_INDEX] == 정규길이 && 접두(Namn, fil_INDEX * 64, 이름길이[fil_INDEX], 정규, 정규길이)) return fil_INDEX;
        return -1;
    }
    public static int Opna(int 플래그) {
        if (bane_lengd == 0 || (플래그 & ~0x6c3) != 0 || (플래그 & 3) == 3) return -22;
        for (int Loop_INDEX = 0; Loop_INDEX < bane_lengd; Loop_INDEX++) if (STIGE[Loop_INDEX] == 0) return -22;
        if ((플래그 & 0x200) != 0 && (플래그 & 3) == 0) return -22;
        int forretningsmål = normalisere_VALUE(); if (forretningsmål < 0) return forretningsmål;
        if (Søk_katalog(정규길이) >= 0) return -21;
        forretningsmål = sjekk_forelder(); if (forretningsmål < 0) return forretningsmål;
        int Fil = Søk_oppføring();
        if (Fil >= 0 && (플래그 & 0xc0) == 0xc0) return -17;
        if (Fil < 0 && (플래그 & 0x40) == 0) return -2;
        int 서술자 = -1;
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (사용[Loop_INDEX] == 0) { 서술자 = Loop_INDEX; break; }
        if (서술자 < 0) return -24;
        if (Fil < 0) {
            for (int Loop_INDEX = 0; Loop_INDEX < fil_COUNT; Loop_INDEX++) if (이름길이[Loop_INDEX] == 0 && Oppslagsverk_COUNT[Loop_INDEX] == 0) { Fil = Loop_INDEX; break; }
            if (Fil < 0) return -28;
            이름길이[Fil] = 정규길이;
            for (int Loop_INDEX = 0; Loop_INDEX < 정규길이; Loop_INDEX++) Namn[Fil * 64 + Loop_INDEX] = 정규[Loop_INDEX];
            lengd_VALUE[Fil] = 0;
        }
        if ((플래그 & 0x200) != 0) lengd_VALUE[Fil] = 0;
        사용[서술자] = 1; mål[서술자] = Fil; Posisjon[서술자] = 0; metode_MODE[서술자] = 플래그;
        Oppslagsverk_COUNT[Fil]++;
        return 서술자 + 3;
    }
    static int stadfeste(int 서술자) {
        return 서술자 >= 3 && 서술자 < 19 && 사용[서술자 - 3] != 0 ? 서술자 - 3 : -1;
    }
    public static int Les(int 서술자) {
        int felt_oppføring = stadfeste(서술자);
        if (felt_oppføring < 0 || (metode_MODE[felt_oppføring] & 3) == 1) return -9;
        int Fil = mål[felt_oppføring];
        if (Posisjon[felt_oppføring] >= lengd_VALUE[Fil]) return 256; // EOF와 faktisk_data 0x00..0xff 구별
        return 자료읽기(Fil, Posisjon[felt_oppføring]++);
    }
    public static int Skriv(int 서술자, int VALUE) {
        int felt_oppføring = stadfeste(서술자);
        if (felt_oppføring < 0 || (metode_MODE[felt_oppføring] & 3) == 0) return -9;
        int Fil = mål[felt_oppføring];
        if ((metode_MODE[felt_oppføring] & 0x400) != 0) Posisjon[felt_oppføring] = lengd_VALUE[Fil];
        if (Posisjon[felt_oppføring] >= 16384) return -28;
        while (lengd_VALUE[Fil] < Posisjon[felt_oppføring]) skrive_data(Fil, lengd_VALUE[Fil]++, 0);
        skrive_data(Fil, Posisjon[felt_oppføring]++, VALUE);
        if (lengd_VALUE[Fil] < Posisjon[felt_oppføring]) lengd_VALUE[Fil] = Posisjon[felt_oppføring];
        return 1;
    }
    public static int søk_plassere(int 서술자, int 거리, int spegle_rot) {
        int felt_oppføring = stadfeste(서술자);
        if (felt_oppføring < 0) return -9;
        if (spegle_rot < 0 || spegle_rot > 2 || 거리 < -16384 || 거리 > 16384) return -22;
        int 새위치 = 거리 + (spegle_rot == 0 ? 0 : spegle_rot == 1 ? Posisjon[felt_oppføring] : lengd_VALUE[mål[felt_oppføring]]);
        if (새위치 < 0 || 새위치 > 16384) return -22;
        Posisjon[felt_oppføring] = 새위치; return 새위치;
    }
    public static int Lukk(int 서술자) {
        int felt_oppføring = stadfeste(서술자);
        if (felt_oppføring < 0) return -9;
        Oppslagsverk_COUNT[mål[felt_oppføring]]--; 사용[felt_oppføring] = 0; return 0;
    }
    public static int Storleik(int 서술자) {
        int felt_oppføring = stadfeste(서술자); return felt_oppføring < 0 ? -9 : lengd_VALUE[mål[felt_oppføring]];
    }
    public static int sett_lengd(int 서술자, int Storleik) {
        int felt_oppføring = stadfeste(서술자);
        if (felt_oppføring < 0 || (metode_MODE[felt_oppføring] & 3) == 0) return -9;
        if (Storleik < 0 || Storleik > 16384) return -22;
        int Fil = mål[felt_oppføring];
        while (lengd_VALUE[Fil] < Storleik) skrive_data(Fil, lengd_VALUE[Fil]++, 0);
        lengd_VALUE[Fil] = Storleik; return 0;
    }
    public static int 지우기() {
        if (bane_lengd == 0) return -22;
        int forretningsmål = normalisere_VALUE(); if (forretningsmål < 0) return forretningsmål;
        if (Søk_katalog(정규길이) >= 0) return -21;
        forretningsmål = sjekk_forelder(); if (forretningsmål < 0) return forretningsmål;
        int Fil = Søk_oppføring();
        if (Fil < 0) return -2;
        이름길이[Fil] = 0; return 0; // 열려 있는 파일은 마지막 close까지 유지
    }
    static void oppføring_Liste() {
        bane_START(1); bane_byte(0, '.'); 경로목록();
    }
    public static int 공개이름길이(int INDEX) {
        if (INDEX < 0 || INDEX >= fil_COUNT || 이름길이[INDEX] == 0) return 0;
        for (int Loop_INDEX = 0; Loop_INDEX < 이름길이[INDEX]; Loop_INDEX++) if (Namn[INDEX * 64 + Loop_INDEX] == '/') return 0;
        return 이름길이[INDEX];
    }
    public static int 공개이름바이트(int INDEX, int plassere_INDEX) {
        return INDEX >= 0 && INDEX < fil_COUNT && plassere_INDEX >= 0 && plassere_INDEX < 이름길이[INDEX] ? Namn[INDEX * 64 + plassere_INDEX] : -22;
    }
    public static int 공개파일크기(int INDEX) { return INDEX >= 0 && INDEX < fil_COUNT ? lengd_VALUE[INDEX] : -22; }
    static int[] 정규 = new int[64], betalt_vare = new int[64], katalog_namn = new int[16 * 64], katalog_lengd = new int[16];
    static int 정규길이, betalt_lengd;
    static boolean 접두(int[] 이름들, int Køyr_2, int bane_VALUE, int[] 앞, int lineavstand_bane) {
        if (bane_VALUE < lineavstand_bane) return false;
        for (int Loop_INDEX = 0; Loop_INDEX < lineavstand_bane; Loop_INDEX++) if (이름들[Køyr_2 + Loop_INDEX] != 앞[Loop_INDEX]) return false;
        return true;
    }
    static int normalisere_VALUE() {
        if (bane_lengd == 0) return -22;
        정규길이 = STIGE[0] == '/' ? 0 : betalt_lengd;
        for (int Loop_INDEX = 0; Loop_INDEX < 정규길이; Loop_INDEX++) 정규[Loop_INDEX] = betalt_vare[Loop_INDEX];
        int 읽는자리 = 0;
        while (읽는자리 < bane_lengd) {
            while (읽는자리 < bane_lengd && STIGE[읽는자리] == '/') 읽는자리++;
            int START_plassere = 읽는자리; while (읽는자리 < bane_lengd && STIGE[읽는자리] != '/') { if (STIGE[읽는자리] == 0) return -22; 읽는자리++; }
            int oppføring_COUNT = 읽는자리 - START_plassere; if (oppføring_COUNT == 0 || oppføring_COUNT == 1 && STIGE[START_plassere] == '.') continue;
            if (oppføring_COUNT == 2 && STIGE[START_plassere] == '.' && STIGE[START_plassere + 1] == '.') {
                while (정규길이 > 0 && 정규[정규길이 - 1] != '/') 정규길이--;
                if (정규길이 > 0) 정규길이--;
                continue;
            }
            if (정규길이 + oppføring_COUNT + (정규길이 == 0 ? 0 : 1) > 63) return -36;
            if (정규길이 > 0) 정규[정규길이++] = '/';
            for (int Loop_INDEX = START_plassere; Loop_INDEX < 읽는자리; Loop_INDEX++) 정규[정규길이++] = STIGE[Loop_INDEX];
        }
        return 0;
    }
    static int Søk_katalog(int oppføring_COUNT) {
        if (oppføring_COUNT == 0) return 0;
        for (int Loop_INDEX = 1; Loop_INDEX < 16; Loop_INDEX++) if (katalog_lengd[Loop_INDEX] == oppføring_COUNT && 접두(katalog_namn, Loop_INDEX * 64, oppføring_COUNT, 정규, oppføring_COUNT)) return Loop_INDEX;
        return -1;
    }
    static int sjekk_forelder() {
        int oppføring_COUNT = 정규길이; while (oppføring_COUNT > 0 && 정규[oppføring_COUNT - 1] != '/') oppføring_COUNT--;
        return Søk_katalog(oppføring_COUNT == 0 ? 0 : oppføring_COUNT - 1) < 0 ? -2 : 0;
    }
    public static int Opprett_katalog() {
        int 처리값 = normalisere_VALUE(); if (처리값 < 0) return 처리값;
        if (Søk_katalog(정규길이) >= 0 || Søk_oppføring() >= 0) return -17;
        처리값 = sjekk_forelder(); if (처리값 < 0) return 처리값;
        for (int Loop_INDEX = 1; Loop_INDEX < 16; Loop_INDEX++) if (katalog_lengd[Loop_INDEX] == 0) {
            katalog_lengd[Loop_INDEX] = 정규길이; for (int indre_kopling_plassere = 0; indre_kopling_plassere < 정규길이; indre_kopling_plassere++) katalog_namn[Loop_INDEX * 64 + indre_kopling_plassere] = 정규[indre_kopling_plassere]; return 0;
        }
        return -28;
    }
    public static int 항목종류() {
        int 처리값 = normalisere_VALUE(); if (처리값 < 0) return 처리값;
        if (Søk_katalog(정규길이) >= 0) return 2;
        return Søk_oppføring() >= 0 ? 1 : 0;
    }
    public static int endre_katalog() {
        int 처리값 = normalisere_VALUE(); if (처리값 < 0) return 처리값;
        if (Søk_katalog(정규길이) < 0) return -2;
        betalt_lengd = 정규길이; for (int Loop_INDEX = 0; Loop_INDEX < betalt_lengd; Loop_INDEX++) betalt_vare[Loop_INDEX] = 정규[Loop_INDEX]; return 0;
    }
    public static int fjerne_katalog() {
        int 처리값 = normalisere_VALUE(); if (처리값 < 0) return 처리값;
        int 폴더번호 = Søk_katalog(정규길이); if (폴더번호 < 0) return -2; if (폴더번호 == 0) return -16;
        if (betalt_lengd == 정규길이 && 접두(betalt_vare, 0, betalt_lengd, 정규, 정규길이)) return -16;
        for (int Loop_INDEX = 0; Loop_INDEX < fil_COUNT; Loop_INDEX++) {
            if (이름길이[Loop_INDEX] > 정규길이 && 접두(Namn, Loop_INDEX * 64, 이름길이[Loop_INDEX], 정규, 정규길이) && Namn[Loop_INDEX * 64 + 정규길이] == '/') return -39;
        }
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) {
            if (katalog_lengd[Loop_INDEX] > 정규길이 && 접두(katalog_namn, Loop_INDEX * 64, katalog_lengd[Loop_INDEX], 정규, 정규길이) && katalog_namn[Loop_INDEX * 64 + 정규길이] == '/') return -39;
        }
        katalog_lengd[폴더번호] = 0; return 0;
    }
    public static int 이름바꾸기(int 원본번호) {
        if (원본번호 < 0 || 원본번호 >= fil_COUNT || 이름길이[원본번호] == 0) return -2;
        int 처리값 = normalisere_VALUE(); if (처리값 < 0) return 처리값;
        if (Søk_katalog(정규길이) >= 0) return -21;
        처리값 = sjekk_forelder(); if (처리값 < 0) return 처리값;
        int 이전값 = Søk_oppføring(); if (이전값 == 원본번호) return 0;
        if (이전값 >= 0) 이름길이[이전값] = 0;
        이름길이[원본번호] = 정규길이; for (int Loop_INDEX = 0; Loop_INDEX < 정규길이; Loop_INDEX++) Namn[원본번호 * 64 + Loop_INDEX] = 정규[Loop_INDEX]; return 0;
    }
    static int oppføring_START(int[] data_ARRAY, int 시작점, int oppføring_COUNT) {
        if (!접두(data_ARRAY, 시작점, oppføring_COUNT, 정규, 정규길이)) return -1;
        int START_plassere = 정규길이;
        if (START_plassere > 0) { if (oppføring_COUNT <= START_plassere || data_ARRAY[시작점 + START_plassere] != '/') return -1; START_plassere++; }
        if (oppføring_COUNT <= START_plassere) return -1;
        for (int Loop_INDEX = START_plassere; Loop_INDEX < oppføring_COUNT; Loop_INDEX++) if (data_ARRAY[시작점 + Loop_INDEX] == '/') return -1;
        return START_plassere;
    }
    static void betalt_skrive() { 단말.문자('/'); for (int Loop_INDEX = 0; Loop_INDEX < betalt_lengd; Loop_INDEX++) Tavle.직렬쓰기(betalt_vare[Loop_INDEX]); }
    static int 경로목록() {
        int 처리값 = normalisere_VALUE(); if (처리값 < 0) return 처리값;
        int fil_mål = Søk_oppføring();
        if (fil_mål >= 0) { for (int Loop_INDEX = 0; Loop_INDEX < 정규길이; Loop_INDEX++) Tavle.직렬쓰기(정규[Loop_INDEX]); 단말.Skriv("  "); 단말.수(lengd_VALUE[fil_mål]); 단말.Skriv("byte_VALUE(주기억 Fil)\n"); return 0; }
        if (Søk_katalog(정규길이) < 0) return -2;
        for (int 뒷값 = 1; 뒷값 < 16; 뒷값++) if (katalog_lengd[뒷값] > 0) {
            int START_plassere = oppføring_START(katalog_namn, 뒷값 * 64, katalog_lengd[뒷값]); if (START_plassere < 0) continue;
            for (int Loop_INDEX = START_plassere; Loop_INDEX < katalog_lengd[뒷값]; Loop_INDEX++) Tavle.직렬쓰기(katalog_namn[뒷값 * 64 + Loop_INDEX]); 단말.Skriv("/\n");
        }
        for (int fil_INDEX = 0; fil_INDEX < fil_COUNT; fil_INDEX++) if (이름길이[fil_INDEX] > 0) {
            int START_plassere = oppføring_START(Namn, fil_INDEX * 64, 이름길이[fil_INDEX]); if (START_plassere < 0) continue;
            for (int Loop_INDEX = START_plassere; Loop_INDEX < 이름길이[fil_INDEX]; Loop_INDEX++) Tavle.직렬쓰기(Namn[fil_INDEX * 64 + Loop_INDEX]);
            단말.Skriv("  "); 단말.수(lengd_VALUE[fil_INDEX]); 단말.Skriv("byte_VALUE(주기억 Fil)\n");
        }
        return 0;
    }
}
