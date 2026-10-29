// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** RAM Datoteka 64개, 파일당 16384바이트, 서술자 16개. 모든 podaci/정책은 Java에 있다.
 * 호출 도중 양보하지 않으므로 현재의 단일 코어 협력식 작업 사이에서 원자적이다.
 * 디스크 저장이나 POSIX 전체 구현을 뜻하지 않는다. 음수 반환은 GREŠKA 번호다.
 */
public final class Memorija_Datoteke {
    static final int Datoteka_COUNT = 64;
    static int[] Ime = new int[Datoteka_COUNT * 64];
    static int[] 이름길이 = new int[Datoteka_COUNT];
    // Pack four bytes in each Java int, preserving the old content heap budget.
    static int[] Sadržaj_VALUE = new int[Datoteka_COUNT * 4096];
    static int[] 길이 = new int[Datoteka_COUNT];
    static int[] Reference_COUNT = new int[Datoteka_COUNT];
    static int[] uporaba_VALUE = new int[16];
    static int[] cilj = new int[16];
    static int[] Položaj = new int[16];
    static int[] postupak_MODE = new int[16];
    static int[] PUTANJA = new int[64];
    static int 경로길이;

    public static int 파일한도() { return Datoteka_COUNT; }
    static int 자료읽기(int Datoteka, int indeks_položaja) { return (Sadržaj_VALUE[Datoteka * 4096 + indeks_položaja / 4] >>> ((indeks_položaja & 3) * 8)) & 255; }
    static void zapisivanje_podaci(int Datoteka, int indeks_položaja, int VALUE) {
        int 칸 = Datoteka * 4096 + indeks_položaja / 4, pomicati_se_VALUE = (indeks_položaja & 3) * 8;
        Sadržaj_VALUE[칸] = (Sadržaj_VALUE[칸] & ~(255 << pomicati_se_VALUE)) | ((VALUE & 255) << pomicati_se_VALUE);
    }

    public static int put_START(int Veličina) {
        경로길이 = 0;
        if (Veličina < 1 || Veličina > 63) return -36;
        경로길이 = Veličina;
        for (int Loop_INDEX = 0; Loop_INDEX < Veličina; Loop_INDEX++) PUTANJA[Loop_INDEX] = 0;
        return 0;
    }
    public static int put_bajt(int INDEX, int VALUE) {
        if (INDEX < 0 || INDEX >= 경로길이 || VALUE < 1 || VALUE > 255) return -22;
        PUTANJA[INDEX] = VALUE; return 0;
    }
    static int FIND_unos() {
        for (int Datoteka_INDEX = 0; Datoteka_INDEX < Datoteka_COUNT; Datoteka_INDEX++) if (이름길이[Datoteka_INDEX] > 0 && 이름길이[Datoteka_INDEX] == 정규길이 && 접두(Ime, Datoteka_INDEX * 64, 이름길이[Datoteka_INDEX], 정규, 정규길이)) return Datoteka_INDEX;
        return -1;
    }
    public static int Otvori(int 플래그) {
        if (경로길이 == 0 || (플래그 & ~0x6c3) != 0 || (플래그 & 3) == 3) return -22;
        for (int Loop_INDEX = 0; Loop_INDEX < 경로길이; Loop_INDEX++) if (PUTANJA[Loop_INDEX] == 0) return -22;
        if ((플래그 & 0x200) != 0 && (플래그 & 3) == 0) return -22;
        int REZULTAT = normalizirati_VALUE(); if (REZULTAT < 0) return REZULTAT;
        if (FIND_imenik(정규길이) >= 0) return -21;
        REZULTAT = 부모확인(); if (REZULTAT < 0) return REZULTAT;
        int Datoteka = FIND_unos();
        if (Datoteka >= 0 && (플래그 & 0xc0) == 0xc0) return -17;
        if (Datoteka < 0 && (플래그 & 0x40) == 0) return -2;
        int 서술자 = -1;
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (uporaba_VALUE[Loop_INDEX] == 0) { 서술자 = Loop_INDEX; break; }
        if (서술자 < 0) return -24;
        if (Datoteka < 0) {
            for (int Loop_INDEX = 0; Loop_INDEX < Datoteka_COUNT; Loop_INDEX++) if (이름길이[Loop_INDEX] == 0 && Reference_COUNT[Loop_INDEX] == 0) { Datoteka = Loop_INDEX; break; }
            if (Datoteka < 0) return -28;
            이름길이[Datoteka] = 정규길이;
            for (int Loop_INDEX = 0; Loop_INDEX < 정규길이; Loop_INDEX++) Ime[Datoteka * 64 + Loop_INDEX] = 정규[Loop_INDEX];
            길이[Datoteka] = 0;
        }
        if ((플래그 & 0x200) != 0) 길이[Datoteka] = 0;
        uporaba_VALUE[서술자] = 1; cilj[서술자] = Datoteka; Položaj[서술자] = 0; postupak_MODE[서술자] = 플래그;
        Reference_COUNT[Datoteka]++;
        return 서술자 + 3;
    }
    static int provjeriti(int 서술자) {
        return 서술자 >= 3 && 서술자 < 19 && uporaba_VALUE[서술자 - 3] != 0 ? 서술자 - 3 : -1;
    }
    public static int Čitaj(int 서술자) {
        int 칸 = provjeriti(서술자);
        if (칸 < 0 || (postupak_MODE[칸] & 3) == 1) return -9;
        int Datoteka = cilj[칸];
        if (Položaj[칸] >= 길이[Datoteka]) return 256; // EOF와 stvaran_podaci 0x00..0xff 구별
        return 자료읽기(Datoteka, Položaj[칸]++);
    }
    public static int Zapisuj(int 서술자, int VALUE) {
        int 칸 = provjeriti(서술자);
        if (칸 < 0 || (postupak_MODE[칸] & 3) == 0) return -9;
        int Datoteka = cilj[칸];
        if ((postupak_MODE[칸] & 0x400) != 0) Položaj[칸] = 길이[Datoteka];
        if (Položaj[칸] >= 16384) return -28;
        while (길이[Datoteka] < Položaj[칸]) zapisivanje_podaci(Datoteka, 길이[Datoteka]++, 0);
        zapisivanje_podaci(Datoteka, Položaj[칸]++, VALUE);
        if (길이[Datoteka] < Položaj[칸]) 길이[Datoteka] = Položaj[칸];
        return 1;
    }
    public static int tražiti_položaj(int 서술자, int 거리, int akcija_korijen) {
        int 칸 = provjeriti(서술자);
        if (칸 < 0) return -9;
        if (akcija_korijen < 0 || akcija_korijen > 2 || 거리 < -16384 || 거리 > 16384) return -22;
        int 새위치 = 거리 + (akcija_korijen == 0 ? 0 : akcija_korijen == 1 ? Položaj[칸] : 길이[cilj[칸]]);
        if (새위치 < 0 || 새위치 > 16384) return -22;
        Položaj[칸] = 새위치; return 새위치;
    }
    public static int Zatvori(int 서술자) {
        int 칸 = provjeriti(서술자);
        if (칸 < 0) return -9;
        Reference_COUNT[cilj[칸]]--; uporaba_VALUE[칸] = 0; return 0;
    }
    public static int Veličina(int 서술자) {
        int 칸 = provjeriti(서술자); return 칸 < 0 ? -9 : 길이[cilj[칸]];
    }
    public static int 길이정하기(int 서술자, int Veličina) {
        int 칸 = provjeriti(서술자);
        if (칸 < 0 || (postupak_MODE[칸] & 3) == 0) return -9;
        if (Veličina < 0 || Veličina > 16384) return -22;
        int Datoteka = cilj[칸];
        while (길이[Datoteka] < Veličina) zapisivanje_podaci(Datoteka, 길이[Datoteka]++, 0);
        길이[Datoteka] = Veličina; return 0;
    }
    public static int izbrisati_unos() {
        if (경로길이 == 0) return -22;
        int REZULTAT = normalizirati_VALUE(); if (REZULTAT < 0) return REZULTAT;
        if (FIND_imenik(정규길이) >= 0) return -21;
        REZULTAT = 부모확인(); if (REZULTAT < 0) return REZULTAT;
        int Datoteka = FIND_unos();
        if (Datoteka < 0) return -2;
        이름길이[Datoteka] = 0; return 0; // 열려 있는 파일은 마지막 close까지 유지
    }
    static void unos_Popis() {
        put_START(1); put_bajt(0, '.'); 경로목록();
    }
    public static int 공개이름길이(int INDEX) {
        if (INDEX < 0 || INDEX >= Datoteka_COUNT || 이름길이[INDEX] == 0) return 0;
        for (int Loop_INDEX = 0; Loop_INDEX < 이름길이[INDEX]; Loop_INDEX++) if (Ime[INDEX * 64 + Loop_INDEX] == '/') return 0;
        return 이름길이[INDEX];
    }
    public static int 공개이름바이트(int INDEX, int indeks_položaja) {
        return INDEX >= 0 && INDEX < Datoteka_COUNT && indeks_položaja >= 0 && indeks_položaja < 이름길이[INDEX] ? Ime[INDEX * 64 + indeks_položaja] : -22;
    }
    public static int 공개파일크기(int INDEX) { return INDEX >= 0 && INDEX < Datoteka_COUNT ? 길이[INDEX] : -22; }
    static int[] 정규 = new int[64], redovno_artikl = new int[64], imenik_naziv = new int[16 * 64], 폴더길이 = new int[16];
    static int 정규길이, 현재길이;
    static boolean 접두(int[] 이름들, int Pokreni, int put_VALUE, int[] prednja_VALUE, int prored_put) {
        if (put_VALUE < prored_put) return false;
        for (int Loop_INDEX = 0; Loop_INDEX < prored_put; Loop_INDEX++) if (이름들[Pokreni + Loop_INDEX] != prednja_VALUE[Loop_INDEX]) return false;
        return true;
    }
    static int normalizirati_VALUE() {
        if (경로길이 == 0) return -22;
        정규길이 = PUTANJA[0] == '/' ? 0 : 현재길이;
        for (int Loop_INDEX = 0; Loop_INDEX < 정규길이; Loop_INDEX++) 정규[Loop_INDEX] = redovno_artikl[Loop_INDEX];
        int 읽는자리 = 0;
        while (읽는자리 < 경로길이) {
            while (읽는자리 < 경로길이 && PUTANJA[읽는자리] == '/') 읽는자리++;
            int START_položaj = 읽는자리; while (읽는자리 < 경로길이 && PUTANJA[읽는자리] != '/') { if (PUTANJA[읽는자리] == 0) return -22; 읽는자리++; }
            int unos_COUNT = 읽는자리 - START_položaj; if (unos_COUNT == 0 || unos_COUNT == 1 && PUTANJA[START_položaj] == '.') continue;
            if (unos_COUNT == 2 && PUTANJA[START_položaj] == '.' && PUTANJA[START_položaj + 1] == '.') {
                while (정규길이 > 0 && 정규[정규길이 - 1] != '/') 정규길이--;
                if (정규길이 > 0) 정규길이--;
                continue;
            }
            if (정규길이 + unos_COUNT + (정규길이 == 0 ? 0 : 1) > 63) return -36;
            if (정규길이 > 0) 정규[정규길이++] = '/';
            for (int Loop_INDEX = START_položaj; Loop_INDEX < 읽는자리; Loop_INDEX++) 정규[정규길이++] = PUTANJA[Loop_INDEX];
        }
        return 0;
    }
    static int FIND_imenik(int unos_COUNT) {
        if (unos_COUNT == 0) return 0;
        for (int Loop_INDEX = 1; Loop_INDEX < 16; Loop_INDEX++) if (폴더길이[Loop_INDEX] == unos_COUNT && 접두(imenik_naziv, Loop_INDEX * 64, unos_COUNT, 정규, unos_COUNT)) return Loop_INDEX;
        return -1;
    }
    static int 부모확인() {
        int unos_COUNT = 정규길이; while (unos_COUNT > 0 && 정규[unos_COUNT - 1] != '/') unos_COUNT--;
        return FIND_imenik(unos_COUNT == 0 ? 0 : unos_COUNT - 1) < 0 ? -2 : 0;
    }
    public static int Create_imenik() {
        int 처리값 = normalizirati_VALUE(); if (처리값 < 0) return 처리값;
        if (FIND_imenik(정규길이) >= 0 || FIND_unos() >= 0) return -17;
        처리값 = 부모확인(); if (처리값 < 0) return 처리값;
        for (int Loop_INDEX = 1; Loop_INDEX < 16; Loop_INDEX++) if (폴더길이[Loop_INDEX] == 0) {
            폴더길이[Loop_INDEX] = 정규길이; for (int unutarnji_položaj = 0; unutarnji_položaj < 정규길이; unutarnji_položaj++) imenik_naziv[Loop_INDEX * 64 + unutarnji_položaj] = 정규[unutarnji_položaj]; return 0;
        }
        return -28;
    }
    public static int 항목종류() {
        int 처리값 = normalizirati_VALUE(); if (처리값 < 0) return 처리값;
        if (FIND_imenik(정규길이) >= 0) return 2;
        return FIND_unos() >= 0 ? 1 : 0;
    }
    public static int promijeniti_imenik() {
        int 처리값 = normalizirati_VALUE(); if (처리값 < 0) return 처리값;
        if (FIND_imenik(정규길이) < 0) return -2;
        현재길이 = 정규길이; for (int Loop_INDEX = 0; Loop_INDEX < 현재길이; Loop_INDEX++) redovno_artikl[Loop_INDEX] = 정규[Loop_INDEX]; return 0;
    }
    public static int ukloniti_imenik() {
        int 처리값 = normalizirati_VALUE(); if (처리값 < 0) return 처리값;
        int 폴더번호 = FIND_imenik(정규길이); if (폴더번호 < 0) return -2; if (폴더번호 == 0) return -16;
        if (현재길이 == 정규길이 && 접두(redovno_artikl, 0, 현재길이, 정규, 정규길이)) return -16;
        for (int Loop_INDEX = 0; Loop_INDEX < Datoteka_COUNT; Loop_INDEX++) {
            if (이름길이[Loop_INDEX] > 정규길이 && 접두(Ime, Loop_INDEX * 64, 이름길이[Loop_INDEX], 정규, 정규길이) && Ime[Loop_INDEX * 64 + 정규길이] == '/') return -39;
        }
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) {
            if (폴더길이[Loop_INDEX] > 정규길이 && 접두(imenik_naziv, Loop_INDEX * 64, 폴더길이[Loop_INDEX], 정규, 정규길이) && imenik_naziv[Loop_INDEX * 64 + 정규길이] == '/') return -39;
        }
        폴더길이[폴더번호] = 0; return 0;
    }
    public static int Preimenuj_unos(int 원본번호) {
        if (원본번호 < 0 || 원본번호 >= Datoteka_COUNT || 이름길이[원본번호] == 0) return -2;
        int 처리값 = normalizirati_VALUE(); if (처리값 < 0) return 처리값;
        if (FIND_imenik(정규길이) >= 0) return -21;
        처리값 = 부모확인(); if (처리값 < 0) return 처리값;
        int 이전값 = FIND_unos(); if (이전값 == 원본번호) return 0;
        if (이전값 >= 0) 이름길이[이전값] = 0;
        이름길이[원본번호] = 정규길이; for (int Loop_INDEX = 0; Loop_INDEX < 정규길이; Loop_INDEX++) Ime[원본번호 * 64 + Loop_INDEX] = 정규[Loop_INDEX]; return 0;
    }
    static int unos_START(int[] podaci_ARRAY, int 시작점, int unos_COUNT) {
        if (!접두(podaci_ARRAY, 시작점, unos_COUNT, 정규, 정규길이)) return -1;
        int START_položaj = 정규길이;
        if (START_položaj > 0) { if (unos_COUNT <= START_položaj || podaci_ARRAY[시작점 + START_položaj] != '/') return -1; START_položaj++; }
        if (unos_COUNT <= START_položaj) return -1;
        for (int Loop_INDEX = START_položaj; Loop_INDEX < unos_COUNT; Loop_INDEX++) if (podaci_ARRAY[시작점 + Loop_INDEX] == '/') return -1;
        return START_položaj;
    }
    static void redovno_zapisivanje() { 단말.문자('/'); for (int Loop_INDEX = 0; Loop_INDEX < 현재길이; Loop_INDEX++) pano.직렬쓰기(redovno_artikl[Loop_INDEX]); }
    static int 경로목록() {
        int 처리값 = normalizirati_VALUE(); if (처리값 < 0) return 처리값;
        int Datoteka_cilj = FIND_unos();
        if (Datoteka_cilj >= 0) { for (int Loop_INDEX = 0; Loop_INDEX < 정규길이; Loop_INDEX++) pano.직렬쓰기(정규[Loop_INDEX]); 단말.Zapisuj("  "); 단말.수(길이[Datoteka_cilj]); 단말.Zapisuj("bajt_VALUE(주기억 Datoteka)\n"); return 0; }
        if (FIND_imenik(정규길이) < 0) return -2;
        for (int 뒷값 = 1; 뒷값 < 16; 뒷값++) if (폴더길이[뒷값] > 0) {
            int START_položaj = unos_START(imenik_naziv, 뒷값 * 64, 폴더길이[뒷값]); if (START_položaj < 0) continue;
            for (int Loop_INDEX = START_položaj; Loop_INDEX < 폴더길이[뒷값]; Loop_INDEX++) pano.직렬쓰기(imenik_naziv[뒷값 * 64 + Loop_INDEX]); 단말.Zapisuj("/\n");
        }
        for (int Datoteka_INDEX = 0; Datoteka_INDEX < Datoteka_COUNT; Datoteka_INDEX++) if (이름길이[Datoteka_INDEX] > 0) {
            int START_položaj = unos_START(Ime, Datoteka_INDEX * 64, 이름길이[Datoteka_INDEX]); if (START_položaj < 0) continue;
            for (int Loop_INDEX = START_položaj; Loop_INDEX < 이름길이[Datoteka_INDEX]; Loop_INDEX++) pano.직렬쓰기(Ime[Datoteka_INDEX * 64 + Loop_INDEX]);
            단말.Zapisuj("  "); 단말.수(길이[Datoteka_INDEX]); 단말.Zapisuj("bajt_VALUE(주기억 Datoteka)\n");
        }
        return 0;
    }
}
