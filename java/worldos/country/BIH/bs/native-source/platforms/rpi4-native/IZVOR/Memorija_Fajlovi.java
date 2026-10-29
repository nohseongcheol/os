// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** RAM Fajl 64개, 파일당 16384바이트, 서술자 16개. 모든 podaci/정책은 Java에 있다.
 * 호출 도중 양보하지 않으므로 현재의 단일 코어 협력식 작업 사이에서 원자적이다.
 * 디스크 저장이나 POSIX 전체 구현을 뜻하지 않는다. 음수 반환은 GRESKA 번호다.
 */
public final class Memorija_Fajlovi {
    static final int fajl_COUNT = 64;
    static int[] Naziv = new int[fajl_COUNT * 64];
    static int[] 이름길이 = new int[fajl_COUNT];
    // Pack four bytes in each Java int, preserving the old content heap budget.
    static int[] Sadržaj_VALUE = new int[fajl_COUNT * 4096];
    static int[] dužina_VALUE = new int[fajl_COUNT];
    static int[] Reference_COUNT = new int[fajl_COUNT];
    static int[] 사용 = new int[16];
    static int[] cilj = new int[16];
    static int[] Pozicija = new int[16];
    static int[] metoda_mod = new int[16];
    static int[] Putanja = new int[64];
    static int put_dužina;

    public static int 파일한도() { return fajl_COUNT; }
    static int 자료읽기(int Fajl, int položaj_INDEX) { return (Sadržaj_VALUE[Fajl * 4096 + položaj_INDEX / 4] >>> ((položaj_INDEX & 3) * 8)) & 255; }
    static void pisati_podaci(int Fajl, int položaj_INDEX, int VALUE) {
        int prostor_za_unos_unos = Fajl * 4096 + položaj_INDEX / 4, pomaći_VALUE = (položaj_INDEX & 3) * 8;
        Sadržaj_VALUE[prostor_za_unos_unos] = (Sadržaj_VALUE[prostor_za_unos_unos] & ~(255 << pomaći_VALUE)) | ((VALUE & 255) << pomaći_VALUE);
    }

    public static int put_START(int Veličina) {
        put_dužina = 0;
        if (Veličina < 1 || Veličina > 63) return -36;
        put_dužina = Veličina;
        for (int Loop_INDEX = 0; Loop_INDEX < Veličina; Loop_INDEX++) Putanja[Loop_INDEX] = 0;
        return 0;
    }
    public static int put_bajt(int INDEX, int VALUE) {
        if (INDEX < 0 || INDEX >= put_dužina || VALUE < 1 || VALUE > 255) return -22;
        Putanja[INDEX] = VALUE; return 0;
    }
    static int FIND_unos() {
        for (int fajl_INDEX = 0; fajl_INDEX < fajl_COUNT; fajl_INDEX++) if (이름길이[fajl_INDEX] > 0 && 이름길이[fajl_INDEX] == 정규길이 && 접두(Naziv, fajl_INDEX * 64, 이름길이[fajl_INDEX], 정규, 정규길이)) return fajl_INDEX;
        return -1;
    }
    public static int Otvori(int 플래그) {
        if (put_dužina == 0 || (플래그 & ~0x6c3) != 0 || (플래그 & 3) == 3) return -22;
        for (int Loop_INDEX = 0; Loop_INDEX < put_dužina; Loop_INDEX++) if (Putanja[Loop_INDEX] == 0) return -22;
        if ((플래그 & 0x200) != 0 && (플래그 & 3) == 0) return -22;
        int mjera = normalizirati_VALUE(); if (mjera < 0) return mjera;
        if (FIND_Direktorij(정규길이) >= 0) return -21;
        mjera = ček_roditelj(); if (mjera < 0) return mjera;
        int Fajl = FIND_unos();
        if (Fajl >= 0 && (플래그 & 0xc0) == 0xc0) return -17;
        if (Fajl < 0 && (플래그 & 0x40) == 0) return -2;
        int 서술자 = -1;
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (사용[Loop_INDEX] == 0) { 서술자 = Loop_INDEX; break; }
        if (서술자 < 0) return -24;
        if (Fajl < 0) {
            for (int Loop_INDEX = 0; Loop_INDEX < fajl_COUNT; Loop_INDEX++) if (이름길이[Loop_INDEX] == 0 && Reference_COUNT[Loop_INDEX] == 0) { Fajl = Loop_INDEX; break; }
            if (Fajl < 0) return -28;
            이름길이[Fajl] = 정규길이;
            for (int Loop_INDEX = 0; Loop_INDEX < 정규길이; Loop_INDEX++) Naziv[Fajl * 64 + Loop_INDEX] = 정규[Loop_INDEX];
            dužina_VALUE[Fajl] = 0;
        }
        if ((플래그 & 0x200) != 0) dužina_VALUE[Fajl] = 0;
        사용[서술자] = 1; cilj[서술자] = Fajl; Pozicija[서술자] = 0; metoda_mod[서술자] = 플래그;
        Reference_COUNT[Fajl]++;
        return 서술자 + 3;
    }
    static int potvrditi(int 서술자) {
        return 서술자 >= 3 && 서술자 < 19 && 사용[서술자 - 3] != 0 ? 서술자 - 3 : -1;
    }
    public static int Čitaj(int 서술자) {
        int prostor_za_unos_unos = potvrditi(서술자);
        if (prostor_za_unos_unos < 0 || (metoda_mod[prostor_za_unos_unos] & 3) == 1) return -9;
        int Fajl = cilj[prostor_za_unos_unos];
        if (Pozicija[prostor_za_unos_unos] >= dužina_VALUE[Fajl]) return 256; // EOF와 stvaran_podaci 0x00..0xff 구별
        return 자료읽기(Fajl, Pozicija[prostor_za_unos_unos]++);
    }
    public static int Piši(int 서술자, int VALUE) {
        int prostor_za_unos_unos = potvrditi(서술자);
        if (prostor_za_unos_unos < 0 || (metoda_mod[prostor_za_unos_unos] & 3) == 0) return -9;
        int Fajl = cilj[prostor_za_unos_unos];
        if ((metoda_mod[prostor_za_unos_unos] & 0x400) != 0) Pozicija[prostor_za_unos_unos] = dužina_VALUE[Fajl];
        if (Pozicija[prostor_za_unos_unos] >= 16384) return -28;
        while (dužina_VALUE[Fajl] < Pozicija[prostor_za_unos_unos]) pisati_podaci(Fajl, dužina_VALUE[Fajl]++, 0);
        pisati_podaci(Fajl, Pozicija[prostor_za_unos_unos]++, VALUE);
        if (dužina_VALUE[Fajl] < Pozicija[prostor_za_unos_unos]) dužina_VALUE[Fajl] = Pozicija[prostor_za_unos_unos];
        return 1;
    }
    public static int tražiti_položaj(int 서술자, int 거리, int projicirati_koijen) {
        int prostor_za_unos_unos = potvrditi(서술자);
        if (prostor_za_unos_unos < 0) return -9;
        if (projicirati_koijen < 0 || projicirati_koijen > 2 || 거리 < -16384 || 거리 > 16384) return -22;
        int 새위치 = 거리 + (projicirati_koijen == 0 ? 0 : projicirati_koijen == 1 ? Pozicija[prostor_za_unos_unos] : dužina_VALUE[cilj[prostor_za_unos_unos]]);
        if (새위치 < 0 || 새위치 > 16384) return -22;
        Pozicija[prostor_za_unos_unos] = 새위치; return 새위치;
    }
    public static int Zatvori(int 서술자) {
        int prostor_za_unos_unos = potvrditi(서술자);
        if (prostor_za_unos_unos < 0) return -9;
        Reference_COUNT[cilj[prostor_za_unos_unos]]--; 사용[prostor_za_unos_unos] = 0; return 0;
    }
    public static int Veličina(int 서술자) {
        int prostor_za_unos_unos = potvrditi(서술자); return prostor_za_unos_unos < 0 ? -9 : dužina_VALUE[cilj[prostor_za_unos_unos]];
    }
    public static int skup_dužina(int 서술자, int Veličina) {
        int prostor_za_unos_unos = potvrditi(서술자);
        if (prostor_za_unos_unos < 0 || (metoda_mod[prostor_za_unos_unos] & 3) == 0) return -9;
        if (Veličina < 0 || Veličina > 16384) return -22;
        int Fajl = cilj[prostor_za_unos_unos];
        while (dužina_VALUE[Fajl] < Veličina) pisati_podaci(Fajl, dužina_VALUE[Fajl]++, 0);
        dužina_VALUE[Fajl] = Veličina; return 0;
    }
    public static int 지우기() {
        if (put_dužina == 0) return -22;
        int mjera = normalizirati_VALUE(); if (mjera < 0) return mjera;
        if (FIND_Direktorij(정규길이) >= 0) return -21;
        mjera = ček_roditelj(); if (mjera < 0) return mjera;
        int Fajl = FIND_unos();
        if (Fajl < 0) return -2;
        이름길이[Fajl] = 0; return 0; // 열려 있는 파일은 마지막 close까지 유지
    }
    static void unos_spisak() {
        put_START(1); put_bajt(0, '.'); 경로목록();
    }
    public static int 공개이름길이(int INDEX) {
        if (INDEX < 0 || INDEX >= fajl_COUNT || 이름길이[INDEX] == 0) return 0;
        for (int Loop_INDEX = 0; Loop_INDEX < 이름길이[INDEX]; Loop_INDEX++) if (Naziv[INDEX * 64 + Loop_INDEX] == '/') return 0;
        return 이름길이[INDEX];
    }
    public static int 공개이름바이트(int INDEX, int položaj_INDEX) {
        return INDEX >= 0 && INDEX < fajl_COUNT && položaj_INDEX >= 0 && položaj_INDEX < 이름길이[INDEX] ? Naziv[INDEX * 64 + položaj_INDEX] : -22;
    }
    public static int 공개파일크기(int INDEX) { return INDEX >= 0 && INDEX < fajl_COUNT ? dužina_VALUE[INDEX] : -22; }
    static int[] 정규 = new int[64], trenutno_stavka = new int[64], Direktorij_naziv = new int[16 * 64], Direktorij_dužina = new int[16];
    static int 정규길이, trenutno_dužina;
    static boolean 접두(int[] 이름들, int Pokreni, int put_VALUE, int[] 앞, int prored_put) {
        if (put_VALUE < prored_put) return false;
        for (int Loop_INDEX = 0; Loop_INDEX < prored_put; Loop_INDEX++) if (이름들[Pokreni + Loop_INDEX] != 앞[Loop_INDEX]) return false;
        return true;
    }
    static int normalizirati_VALUE() {
        if (put_dužina == 0) return -22;
        정규길이 = Putanja[0] == '/' ? 0 : trenutno_dužina;
        for (int Loop_INDEX = 0; Loop_INDEX < 정규길이; Loop_INDEX++) 정규[Loop_INDEX] = trenutno_stavka[Loop_INDEX];
        int 읽는자리 = 0;
        while (읽는자리 < put_dužina) {
            while (읽는자리 < put_dužina && Putanja[읽는자리] == '/') 읽는자리++;
            int START_položaj = 읽는자리; while (읽는자리 < put_dužina && Putanja[읽는자리] != '/') { if (Putanja[읽는자리] == 0) return -22; 읽는자리++; }
            int unos_COUNT = 읽는자리 - START_položaj; if (unos_COUNT == 0 || unos_COUNT == 1 && Putanja[START_položaj] == '.') continue;
            if (unos_COUNT == 2 && Putanja[START_položaj] == '.' && Putanja[START_položaj + 1] == '.') {
                while (정규길이 > 0 && 정규[정규길이 - 1] != '/') 정규길이--;
                if (정규길이 > 0) 정규길이--;
                continue;
            }
            if (정규길이 + unos_COUNT + (정규길이 == 0 ? 0 : 1) > 63) return -36;
            if (정규길이 > 0) 정규[정규길이++] = '/';
            for (int Loop_INDEX = START_položaj; Loop_INDEX < 읽는자리; Loop_INDEX++) 정규[정규길이++] = Putanja[Loop_INDEX];
        }
        return 0;
    }
    static int FIND_Direktorij(int unos_COUNT) {
        if (unos_COUNT == 0) return 0;
        for (int Loop_INDEX = 1; Loop_INDEX < 16; Loop_INDEX++) if (Direktorij_dužina[Loop_INDEX] == unos_COUNT && 접두(Direktorij_naziv, Loop_INDEX * 64, unos_COUNT, 정규, unos_COUNT)) return Loop_INDEX;
        return -1;
    }
    static int ček_roditelj() {
        int unos_COUNT = 정규길이; while (unos_COUNT > 0 && 정규[unos_COUNT - 1] != '/') unos_COUNT--;
        return FIND_Direktorij(unos_COUNT == 0 ? 0 : unos_COUNT - 1) < 0 ? -2 : 0;
    }
    public static int Create_Direktorij() {
        int 처리값 = normalizirati_VALUE(); if (처리값 < 0) return 처리값;
        if (FIND_Direktorij(정규길이) >= 0 || FIND_unos() >= 0) return -17;
        처리값 = ček_roditelj(); if (처리값 < 0) return 처리값;
        for (int Loop_INDEX = 1; Loop_INDEX < 16; Loop_INDEX++) if (Direktorij_dužina[Loop_INDEX] == 0) {
            Direktorij_dužina[Loop_INDEX] = 정규길이; for (int unutrašnje_spajanje_položaj = 0; unutrašnje_spajanje_položaj < 정규길이; unutrašnje_spajanje_položaj++) Direktorij_naziv[Loop_INDEX * 64 + unutrašnje_spajanje_položaj] = 정규[unutrašnje_spajanje_položaj]; return 0;
        }
        return -28;
    }
    public static int 항목종류() {
        int 처리값 = normalizirati_VALUE(); if (처리값 < 0) return 처리값;
        if (FIND_Direktorij(정규길이) >= 0) return 2;
        return FIND_unos() >= 0 ? 1 : 0;
    }
    public static int promijeniti_Direktorij() {
        int 처리값 = normalizirati_VALUE(); if (처리값 < 0) return 처리값;
        if (FIND_Direktorij(정규길이) < 0) return -2;
        trenutno_dužina = 정규길이; for (int Loop_INDEX = 0; Loop_INDEX < trenutno_dužina; Loop_INDEX++) trenutno_stavka[Loop_INDEX] = 정규[Loop_INDEX]; return 0;
    }
    public static int ukloniti_Direktorij() {
        int 처리값 = normalizirati_VALUE(); if (처리값 < 0) return 처리값;
        int 폴더번호 = FIND_Direktorij(정규길이); if (폴더번호 < 0) return -2; if (폴더번호 == 0) return -16;
        if (trenutno_dužina == 정규길이 && 접두(trenutno_stavka, 0, trenutno_dužina, 정규, 정규길이)) return -16;
        for (int Loop_INDEX = 0; Loop_INDEX < fajl_COUNT; Loop_INDEX++) {
            if (이름길이[Loop_INDEX] > 정규길이 && 접두(Naziv, Loop_INDEX * 64, 이름길이[Loop_INDEX], 정규, 정규길이) && Naziv[Loop_INDEX * 64 + 정규길이] == '/') return -39;
        }
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) {
            if (Direktorij_dužina[Loop_INDEX] > 정규길이 && 접두(Direktorij_naziv, Loop_INDEX * 64, Direktorij_dužina[Loop_INDEX], 정규, 정규길이) && Direktorij_naziv[Loop_INDEX * 64 + 정규길이] == '/') return -39;
        }
        Direktorij_dužina[폴더번호] = 0; return 0;
    }
    public static int 이름바꾸기(int 원본번호) {
        if (원본번호 < 0 || 원본번호 >= fajl_COUNT || 이름길이[원본번호] == 0) return -2;
        int 처리값 = normalizirati_VALUE(); if (처리값 < 0) return 처리값;
        if (FIND_Direktorij(정규길이) >= 0) return -21;
        처리값 = ček_roditelj(); if (처리값 < 0) return 처리값;
        int 이전값 = FIND_unos(); if (이전값 == 원본번호) return 0;
        if (이전값 >= 0) 이름길이[이전값] = 0;
        이름길이[원본번호] = 정규길이; for (int Loop_INDEX = 0; Loop_INDEX < 정규길이; Loop_INDEX++) Naziv[원본번호 * 64 + Loop_INDEX] = 정규[Loop_INDEX]; return 0;
    }
    static int unos_START(int[] podaci_niz, int 시작점, int unos_COUNT) {
        if (!접두(podaci_niz, 시작점, unos_COUNT, 정규, 정규길이)) return -1;
        int START_položaj = 정규길이;
        if (START_položaj > 0) { if (unos_COUNT <= START_položaj || podaci_niz[시작점 + START_položaj] != '/') return -1; START_položaj++; }
        if (unos_COUNT <= START_položaj) return -1;
        for (int Loop_INDEX = START_položaj; Loop_INDEX < unos_COUNT; Loop_INDEX++) if (podaci_niz[시작점 + Loop_INDEX] == '/') return -1;
        return START_položaj;
    }
    static void trenutno_pisati() { 단말.문자('/'); for (int Loop_INDEX = 0; Loop_INDEX < trenutno_dužina; Loop_INDEX++) ploča.직렬쓰기(trenutno_stavka[Loop_INDEX]); }
    static int 경로목록() {
        int 처리값 = normalizirati_VALUE(); if (처리값 < 0) return 처리값;
        int fajl_cilj = FIND_unos();
        if (fajl_cilj >= 0) { for (int Loop_INDEX = 0; Loop_INDEX < 정규길이; Loop_INDEX++) ploča.직렬쓰기(정규[Loop_INDEX]); 단말.Piši("  "); 단말.수(dužina_VALUE[fajl_cilj]); 단말.Piši("bajt_VALUE(주기억 Fajl)\n"); return 0; }
        if (FIND_Direktorij(정규길이) < 0) return -2;
        for (int 뒷값 = 1; 뒷값 < 16; 뒷값++) if (Direktorij_dužina[뒷값] > 0) {
            int START_položaj = unos_START(Direktorij_naziv, 뒷값 * 64, Direktorij_dužina[뒷값]); if (START_položaj < 0) continue;
            for (int Loop_INDEX = START_položaj; Loop_INDEX < Direktorij_dužina[뒷값]; Loop_INDEX++) ploča.직렬쓰기(Direktorij_naziv[뒷값 * 64 + Loop_INDEX]); 단말.Piši("/\n");
        }
        for (int fajl_INDEX = 0; fajl_INDEX < fajl_COUNT; fajl_INDEX++) if (이름길이[fajl_INDEX] > 0) {
            int START_položaj = unos_START(Naziv, fajl_INDEX * 64, 이름길이[fajl_INDEX]); if (START_položaj < 0) continue;
            for (int Loop_INDEX = START_položaj; Loop_INDEX < 이름길이[fajl_INDEX]; Loop_INDEX++) ploča.직렬쓰기(Naziv[fajl_INDEX * 64 + Loop_INDEX]);
            단말.Piši("  "); 단말.수(dužina_VALUE[fajl_INDEX]); 단말.Piši("bajt_VALUE(주기억 Fajl)\n");
        }
        return 0;
    }
}
