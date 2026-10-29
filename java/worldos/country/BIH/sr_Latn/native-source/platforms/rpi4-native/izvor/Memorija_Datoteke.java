// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** RAM Datoteka 64개, 파일당 16384바이트, 서술자 16개. 모든 podaci/정책은 Java에 있다.
 * 호출 도중 양보하지 않으므로 현재의 단일 코어 협력식 작업 사이에서 원자적이다.
 * 디스크 저장이나 POSIX 전체 구현을 뜻하지 않는다. 음수 반환은 greška 번호다.
 */
public final class Memorija_Datoteke {
    static final int Datoteka_COUNT = 64;
    static int[] ime = new int[Datoteka_COUNT * 64];
    static int[] 이름길이 = new int[Datoteka_COUNT];
    // Pack four bytes in each Java int, preserving the old content heap budget.
    static int[] Sadržaj_VALUE = new int[Datoteka_COUNT * 4096];
    static int[] 길이 = new int[Datoteka_COUNT];
    static int[] referenca_COUNT = new int[Datoteka_COUNT];
    static int[] koristiti_VALUE = new int[16];
    static int[] cilj = new int[16];
    static int[] pozicija = new int[16];
    static int[] metod_MODE = new int[16];
    static int[] putanja = new int[64];
    static int 경로길이;

    public static int 파일한도() { return Datoteka_COUNT; }
    static int 자료읽기(int Datoteka, int indeks_pozicije) { return (Sadržaj_VALUE[Datoteka * 4096 + indeks_pozicije / 4] >>> ((indeks_pozicije & 3) * 8)) & 255; }
    static void 자료쓰기(int Datoteka, int indeks_pozicije, int VALUE) {
        int 칸 = Datoteka * 4096 + indeks_pozicije / 4, premestiti_VALUE = (indeks_pozicije & 3) * 8;
        Sadržaj_VALUE[칸] = (Sadržaj_VALUE[칸] & ~(255 << premestiti_VALUE)) | ((VALUE & 255) << premestiti_VALUE);
    }

    public static int putanja_START(int promeniti_veličinu) {
        경로길이 = 0;
        if (promeniti_veličinu < 1 || promeniti_veličinu > 63) return -36;
        경로길이 = promeniti_veličinu;
        for (int Loop_INDEX = 0; Loop_INDEX < promeniti_veličinu; Loop_INDEX++) putanja[Loop_INDEX] = 0;
        return 0;
    }
    public static int putanja_bajt(int INDEX, int VALUE) {
        if (INDEX < 0 || INDEX >= 경로길이 || VALUE < 1 || VALUE > 255) return -22;
        putanja[INDEX] = VALUE; return 0;
    }
    static int FIND_stavka() {
        for (int Datoteka_INDEX = 0; Datoteka_INDEX < Datoteka_COUNT; Datoteka_INDEX++) if (이름길이[Datoteka_INDEX] > 0 && 이름길이[Datoteka_INDEX] == 정규길이 && 접두(ime, Datoteka_INDEX * 64, 이름길이[Datoteka_INDEX], 정규, 정규길이)) return Datoteka_INDEX;
        return -1;
    }
    public static int otvoren(int 플래그) {
        if (경로길이 == 0 || (플래그 & ~0x6c3) != 0 || (플래그 & 3) == 3) return -22;
        for (int Loop_INDEX = 0; Loop_INDEX < 경로길이; Loop_INDEX++) if (putanja[Loop_INDEX] == 0) return -22;
        if ((플래그 & 0x200) != 0 && (플래그 & 3) == 0) return -22;
        int KR = normalizovati_VALUE(); if (KR < 0) return KR;
        if (FIND_Imenik(정규길이) >= 0) return -21;
        KR = proveriti_nadređen(); if (KR < 0) return KR;
        int Datoteka = FIND_stavka();
        if (Datoteka >= 0 && (플래그 & 0xc0) == 0xc0) return -17;
        if (Datoteka < 0 && (플래그 & 0x40) == 0) return -2;
        int 서술자 = -1;
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (koristiti_VALUE[Loop_INDEX] == 0) { 서술자 = Loop_INDEX; break; }
        if (서술자 < 0) return -24;
        if (Datoteka < 0) {
            for (int Loop_INDEX = 0; Loop_INDEX < Datoteka_COUNT; Loop_INDEX++) if (이름길이[Loop_INDEX] == 0 && referenca_COUNT[Loop_INDEX] == 0) { Datoteka = Loop_INDEX; break; }
            if (Datoteka < 0) return -28;
            이름길이[Datoteka] = 정규길이;
            for (int Loop_INDEX = 0; Loop_INDEX < 정규길이; Loop_INDEX++) ime[Datoteka * 64 + Loop_INDEX] = 정규[Loop_INDEX];
            길이[Datoteka] = 0;
        }
        if ((플래그 & 0x200) != 0) 길이[Datoteka] = 0;
        koristiti_VALUE[서술자] = 1; cilj[서술자] = Datoteka; pozicija[서술자] = 0; metod_MODE[서술자] = 플래그;
        referenca_COUNT[Datoteka]++;
        return 서술자 + 3;
    }
    static int verifikovati(int 서술자) {
        return 서술자 >= 3 && 서술자 < 19 && koristiti_VALUE[서술자 - 3] != 0 ? 서술자 - 3 : -1;
    }
    public static int 읽기(int 서술자) {
        int 칸 = verifikovati(서술자);
        if (칸 < 0 || (metod_MODE[칸] & 3) == 1) return -9;
        int Datoteka = cilj[칸];
        if (pozicija[칸] >= 길이[Datoteka]) return 256; // EOF와 stvarni_podaci 0x00..0xff 구별
        return 자료읽기(Datoteka, pozicija[칸]++);
    }
    public static int 쓰기(int 서술자, int VALUE) {
        int 칸 = verifikovati(서술자);
        if (칸 < 0 || (metod_MODE[칸] & 3) == 0) return -9;
        int Datoteka = cilj[칸];
        if ((metod_MODE[칸] & 0x400) != 0) pozicija[칸] = 길이[Datoteka];
        if (pozicija[칸] >= 16384) return -28;
        while (길이[Datoteka] < pozicija[칸]) 자료쓰기(Datoteka, 길이[Datoteka]++, 0);
        자료쓰기(Datoteka, pozicija[칸]++, VALUE);
        if (길이[Datoteka] < pozicija[칸]) 길이[Datoteka] = pozicija[칸];
        return 1;
    }
    public static int tražiti_pozicija(int 서술자, int 거리, int radnja_koren) {
        int 칸 = verifikovati(서술자);
        if (칸 < 0) return -9;
        if (radnja_koren < 0 || radnja_koren > 2 || 거리 < -16384 || 거리 > 16384) return -22;
        int 새위치 = 거리 + (radnja_koren == 0 ? 0 : radnja_koren == 1 ? pozicija[칸] : 길이[cilj[칸]]);
        if (새위치 < 0 || 새위치 > 16384) return -22;
        pozicija[칸] = 새위치; return 새위치;
    }
    public static int Zatvori(int 서술자) {
        int 칸 = verifikovati(서술자);
        if (칸 < 0) return -9;
        referenca_COUNT[cilj[칸]]--; koristiti_VALUE[칸] = 0; return 0;
    }
    public static int promeniti_veličinu(int 서술자) {
        int 칸 = verifikovati(서술자); return 칸 < 0 ? -9 : 길이[cilj[칸]];
    }
    public static int 길이정하기(int 서술자, int promeniti_veličinu) {
        int 칸 = verifikovati(서술자);
        if (칸 < 0 || (metod_MODE[칸] & 3) == 0) return -9;
        if (promeniti_veličinu < 0 || promeniti_veličinu > 16384) return -22;
        int Datoteka = cilj[칸];
        while (길이[Datoteka] < promeniti_veličinu) 자료쓰기(Datoteka, 길이[Datoteka]++, 0);
        길이[Datoteka] = promeniti_veličinu; return 0;
    }
    public static int obrisati_stavka() {
        if (경로길이 == 0) return -22;
        int KR = normalizovati_VALUE(); if (KR < 0) return KR;
        if (FIND_Imenik(정규길이) >= 0) return -21;
        KR = proveriti_nadređen(); if (KR < 0) return KR;
        int Datoteka = FIND_stavka();
        if (Datoteka < 0) return -2;
        이름길이[Datoteka] = 0; return 0; // 열려 있는 파일은 마지막 close까지 유지
    }
    static void stavka_Lista() {
        putanja_START(1); putanja_bajt(0, '.'); 경로목록();
    }
    public static int 공개이름길이(int INDEX) {
        if (INDEX < 0 || INDEX >= Datoteka_COUNT || 이름길이[INDEX] == 0) return 0;
        for (int Loop_INDEX = 0; Loop_INDEX < 이름길이[INDEX]; Loop_INDEX++) if (ime[INDEX * 64 + Loop_INDEX] == '/') return 0;
        return 이름길이[INDEX];
    }
    public static int 공개이름바이트(int INDEX, int indeks_pozicije) {
        return INDEX >= 0 && INDEX < Datoteka_COUNT && indeks_pozicije >= 0 && indeks_pozicije < 이름길이[INDEX] ? ime[INDEX * 64 + indeks_pozicije] : -22;
    }
    public static int 공개파일크기(int INDEX) { return INDEX >= 0 && INDEX < Datoteka_COUNT ? 길이[INDEX] : -22; }
    static int[] 정규 = new int[64], aktuelno_stavka = new int[64], Imenik_ime = new int[16 * 64], 폴더길이 = new int[16];
    static int 정규길이, 현재길이;
    static boolean 접두(int[] 이름들, int koristiti, int putanja_VALUE, int[] čeona_kamera_VALUE, int prored_putanja) {
        if (putanja_VALUE < prored_putanja) return false;
        for (int Loop_INDEX = 0; Loop_INDEX < prored_putanja; Loop_INDEX++) if (이름들[koristiti + Loop_INDEX] != čeona_kamera_VALUE[Loop_INDEX]) return false;
        return true;
    }
    static int normalizovati_VALUE() {
        if (경로길이 == 0) return -22;
        정규길이 = putanja[0] == '/' ? 0 : 현재길이;
        for (int Loop_INDEX = 0; Loop_INDEX < 정규길이; Loop_INDEX++) 정규[Loop_INDEX] = aktuelno_stavka[Loop_INDEX];
        int 읽는자리 = 0;
        while (읽는자리 < 경로길이) {
            while (읽는자리 < 경로길이 && putanja[읽는자리] == '/') 읽는자리++;
            int START_pozicija = 읽는자리; while (읽는자리 < 경로길이 && putanja[읽는자리] != '/') { if (putanja[읽는자리] == 0) return -22; 읽는자리++; }
            int stavka_COUNT_8f7753a1 = 읽는자리 - START_pozicija; if (stavka_COUNT_8f7753a1 == 0 || stavka_COUNT_8f7753a1 == 1 && putanja[START_pozicija] == '.') continue;
            if (stavka_COUNT_8f7753a1 == 2 && putanja[START_pozicija] == '.' && putanja[START_pozicija + 1] == '.') {
                while (정규길이 > 0 && 정규[정규길이 - 1] != '/') 정규길이--;
                if (정규길이 > 0) 정규길이--;
                continue;
            }
            if (정규길이 + stavka_COUNT_8f7753a1 + (정규길이 == 0 ? 0 : 1) > 63) return -36;
            if (정규길이 > 0) 정규[정규길이++] = '/';
            for (int Loop_INDEX = START_pozicija; Loop_INDEX < 읽는자리; Loop_INDEX++) 정규[정규길이++] = putanja[Loop_INDEX];
        }
        return 0;
    }
    static int FIND_Imenik(int stavka_COUNT_8f7753a1) {
        if (stavka_COUNT_8f7753a1 == 0) return 0;
        for (int Loop_INDEX = 1; Loop_INDEX < 16; Loop_INDEX++) if (폴더길이[Loop_INDEX] == stavka_COUNT_8f7753a1 && 접두(Imenik_ime, Loop_INDEX * 64, stavka_COUNT_8f7753a1, 정규, stavka_COUNT_8f7753a1)) return Loop_INDEX;
        return -1;
    }
    static int proveriti_nadređen() {
        int stavka_COUNT_8f7753a1 = 정규길이; while (stavka_COUNT_8f7753a1 > 0 && 정규[stavka_COUNT_8f7753a1 - 1] != '/') stavka_COUNT_8f7753a1--;
        return FIND_Imenik(stavka_COUNT_8f7753a1 == 0 ? 0 : stavka_COUNT_8f7753a1 - 1) < 0 ? -2 : 0;
    }
    public static int Create_Imenik() {
        int 처리값 = normalizovati_VALUE(); if (처리값 < 0) return 처리값;
        if (FIND_Imenik(정규길이) >= 0 || FIND_stavka() >= 0) return -17;
        처리값 = proveriti_nadređen(); if (처리값 < 0) return 처리값;
        for (int Loop_INDEX = 1; Loop_INDEX < 16; Loop_INDEX++) if (폴더길이[Loop_INDEX] == 0) {
            폴더길이[Loop_INDEX] = 정규길이; for (int unutrašnje_pozicija = 0; unutrašnje_pozicija < 정규길이; unutrašnje_pozicija++) Imenik_ime[Loop_INDEX * 64 + unutrašnje_pozicija] = 정규[unutrašnje_pozicija]; return 0;
        }
        return -28;
    }
    public static int 항목종류() {
        int 처리값 = normalizovati_VALUE(); if (처리값 < 0) return 처리값;
        if (FIND_Imenik(정규길이) >= 0) return 2;
        return FIND_stavka() >= 0 ? 1 : 0;
    }
    public static int promeniti_Imenik() {
        int 처리값 = normalizovati_VALUE(); if (처리값 < 0) return 처리값;
        if (FIND_Imenik(정규길이) < 0) return -2;
        현재길이 = 정규길이; for (int Loop_INDEX = 0; Loop_INDEX < 현재길이; Loop_INDEX++) aktuelno_stavka[Loop_INDEX] = 정규[Loop_INDEX]; return 0;
    }
    public static int ukloniti_Imenik() {
        int 처리값 = normalizovati_VALUE(); if (처리값 < 0) return 처리값;
        int 폴더번호 = FIND_Imenik(정규길이); if (폴더번호 < 0) return -2; if (폴더번호 == 0) return -16;
        if (현재길이 == 정규길이 && 접두(aktuelno_stavka, 0, 현재길이, 정규, 정규길이)) return -16;
        for (int Loop_INDEX = 0; Loop_INDEX < Datoteka_COUNT; Loop_INDEX++) {
            if (이름길이[Loop_INDEX] > 정규길이 && 접두(ime, Loop_INDEX * 64, 이름길이[Loop_INDEX], 정규, 정규길이) && ime[Loop_INDEX * 64 + 정규길이] == '/') return -39;
        }
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) {
            if (폴더길이[Loop_INDEX] > 정규길이 && 접두(Imenik_ime, Loop_INDEX * 64, 폴더길이[Loop_INDEX], 정규, 정규길이) && Imenik_ime[Loop_INDEX * 64 + 정규길이] == '/') return -39;
        }
        폴더길이[폴더번호] = 0; return 0;
    }
    public static int Preimenuj_stavka(int 원본번호) {
        if (원본번호 < 0 || 원본번호 >= Datoteka_COUNT || 이름길이[원본번호] == 0) return -2;
        int 처리값 = normalizovati_VALUE(); if (처리값 < 0) return 처리값;
        if (FIND_Imenik(정규길이) >= 0) return -21;
        처리값 = proveriti_nadređen(); if (처리값 < 0) return 처리값;
        int 이전값 = FIND_stavka(); if (이전값 == 원본번호) return 0;
        if (이전값 >= 0) 이름길이[이전값] = 0;
        이름길이[원본번호] = 정규길이; for (int Loop_INDEX = 0; Loop_INDEX < 정규길이; Loop_INDEX++) ime[원본번호 * 64 + Loop_INDEX] = 정규[Loop_INDEX]; return 0;
    }
    static int stavka_START(int[] podaci_niz, int 시작점, int stavka_COUNT_8f7753a1) {
        if (!접두(podaci_niz, 시작점, stavka_COUNT_8f7753a1, 정규, 정규길이)) return -1;
        int START_pozicija = 정규길이;
        if (START_pozicija > 0) { if (stavka_COUNT_8f7753a1 <= START_pozicija || podaci_niz[시작점 + START_pozicija] != '/') return -1; START_pozicija++; }
        if (stavka_COUNT_8f7753a1 <= START_pozicija) return -1;
        for (int Loop_INDEX = START_pozicija; Loop_INDEX < stavka_COUNT_8f7753a1; Loop_INDEX++) if (podaci_niz[시작점 + Loop_INDEX] == '/') return -1;
        return START_pozicija;
    }
    static void 현재쓰기() { 단말.문자('/'); for (int Loop_INDEX = 0; Loop_INDEX < 현재길이; Loop_INDEX++) Tabla.직렬쓰기(aktuelno_stavka[Loop_INDEX]); }
    static int 경로목록() {
        int 처리값 = normalizovati_VALUE(); if (처리값 < 0) return 처리값;
        int Datoteka_cilj = FIND_stavka();
        if (Datoteka_cilj >= 0) { for (int Loop_INDEX = 0; Loop_INDEX < 정규길이; Loop_INDEX++) Tabla.직렬쓰기(정규[Loop_INDEX]); 단말.쓰기("  "); 단말.수(길이[Datoteka_cilj]); 단말.쓰기("bajt_VALUE(주기억 Datoteka)\n"); return 0; }
        if (FIND_Imenik(정규길이) < 0) return -2;
        for (int 뒷값 = 1; 뒷값 < 16; 뒷값++) if (폴더길이[뒷값] > 0) {
            int START_pozicija = stavka_START(Imenik_ime, 뒷값 * 64, 폴더길이[뒷값]); if (START_pozicija < 0) continue;
            for (int Loop_INDEX = START_pozicija; Loop_INDEX < 폴더길이[뒷값]; Loop_INDEX++) Tabla.직렬쓰기(Imenik_ime[뒷값 * 64 + Loop_INDEX]); 단말.쓰기("/\n");
        }
        for (int Datoteka_INDEX = 0; Datoteka_INDEX < Datoteka_COUNT; Datoteka_INDEX++) if (이름길이[Datoteka_INDEX] > 0) {
            int START_pozicija = stavka_START(ime, Datoteka_INDEX * 64, 이름길이[Datoteka_INDEX]); if (START_pozicija < 0) continue;
            for (int Loop_INDEX = START_pozicija; Loop_INDEX < 이름길이[Datoteka_INDEX]; Loop_INDEX++) Tabla.직렬쓰기(ime[Datoteka_INDEX * 64 + Loop_INDEX]);
            단말.쓰기("  "); 단말.수(길이[Datoteka_INDEX]); 단말.쓰기("bajt_VALUE(주기억 Datoteka)\n");
        }
        return 0;
    }
}
