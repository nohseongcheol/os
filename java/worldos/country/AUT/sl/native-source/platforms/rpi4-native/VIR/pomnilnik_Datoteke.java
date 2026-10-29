// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** RAM Datoteka 64개, 파일당 16384바이트, 서술자 16개. 모든 podatki/정책은 Java에 있다.
 * 호출 도중 양보하지 않으므로 현재의 단일 코어 협력식 작업 사이에서 원자적이다.
 * 디스크 저장이나 POSIX 전체 구현을 뜻하지 않는다. 음수 반환은 NAPAKA 번호다.
 */
public final class pomnilnik_Datoteke {
    static final int Datoteka_COUNT = 64;
    static int[] Ime = new int[Datoteka_COUNT * 64];
    static int[] 이름길이 = new int[Datoteka_COUNT];
    // Pack four bytes in each Java int, preserving the old content heap budget.
    static int[] vsebina_VALUE = new int[Datoteka_COUNT * 4096];
    static int[] 길이 = new int[Datoteka_COUNT];
    static int[] Gradiva_COUNT = new int[Datoteka_COUNT];
    static int[] uporaba_VALUE = new int[16];
    static int[] tarča = new int[16];
    static int[] Položaj = new int[16];
    static int[] metoda_MODE = new int[16];
    static int[] POT = new int[64];
    static int 경로길이;

    public static int 파일한도() { return Datoteka_COUNT; }
    static int 자료읽기(int Datoteka, int kazalec_mesta) { return (vsebina_VALUE[Datoteka * 4096 + kazalec_mesta / 4] >>> ((kazalec_mesta & 3) * 8)) & 255; }
    static void pisati_podatki(int Datoteka, int kazalec_mesta, int VALUE) {
        int 칸 = Datoteka * 4096 + kazalec_mesta / 4, premikati_VALUE = (kazalec_mesta & 3) * 8;
        vsebina_VALUE[칸] = (vsebina_VALUE[칸] & ~(255 << premikati_VALUE)) | ((VALUE & 255) << premikati_VALUE);
    }

    public static int pot_Start(int Velikost) {
        경로길이 = 0;
        if (Velikost < 1 || Velikost > 63) return -36;
        경로길이 = Velikost;
        for (int Loop_INDEX = 0; Loop_INDEX < Velikost; Loop_INDEX++) POT[Loop_INDEX] = 0;
        return 0;
    }
    public static int pot_bajt(int INDEX, int VALUE) {
        if (INDEX < 0 || INDEX >= 경로길이 || VALUE < 1 || VALUE > 255) return -22;
        POT[INDEX] = VALUE; return 0;
    }
    static int FIND_vnos() {
        for (int Datoteka_INDEX = 0; Datoteka_INDEX < Datoteka_COUNT; Datoteka_INDEX++) if (이름길이[Datoteka_INDEX] > 0 && 이름길이[Datoteka_INDEX] == 정규길이 && 접두(Ime, Datoteka_INDEX * 64, 이름길이[Datoteka_INDEX], 정규, 정규길이)) return Datoteka_INDEX;
        return -1;
    }
    public static int Odpri(int 플래그) {
        if (경로길이 == 0 || (플래그 & ~0x6c3) != 0 || (플래그 & 3) == 3) return -22;
        for (int Loop_INDEX = 0; Loop_INDEX < 경로길이; Loop_INDEX++) if (POT[Loop_INDEX] == 0) return -22;
        if ((플래그 & 0x200) != 0 && (플래그 & 3) == 0) return -22;
        int REZULTAT = normalizirati_VALUE(); if (REZULTAT < 0) return REZULTAT;
        if (FIND_Imenik(정규길이) >= 0) return -21;
        REZULTAT = preveriti_nadrejen(); if (REZULTAT < 0) return REZULTAT;
        int Datoteka = FIND_vnos();
        if (Datoteka >= 0 && (플래그 & 0xc0) == 0xc0) return -17;
        if (Datoteka < 0 && (플래그 & 0x40) == 0) return -2;
        int 서술자 = -1;
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (uporaba_VALUE[Loop_INDEX] == 0) { 서술자 = Loop_INDEX; break; }
        if (서술자 < 0) return -24;
        if (Datoteka < 0) {
            for (int Loop_INDEX = 0; Loop_INDEX < Datoteka_COUNT; Loop_INDEX++) if (이름길이[Loop_INDEX] == 0 && Gradiva_COUNT[Loop_INDEX] == 0) { Datoteka = Loop_INDEX; break; }
            if (Datoteka < 0) return -28;
            이름길이[Datoteka] = 정규길이;
            for (int Loop_INDEX = 0; Loop_INDEX < 정규길이; Loop_INDEX++) Ime[Datoteka * 64 + Loop_INDEX] = 정규[Loop_INDEX];
            길이[Datoteka] = 0;
        }
        if ((플래그 & 0x200) != 0) 길이[Datoteka] = 0;
        uporaba_VALUE[서술자] = 1; tarča[서술자] = Datoteka; Položaj[서술자] = 0; metoda_MODE[서술자] = 플래그;
        Gradiva_COUNT[Datoteka]++;
        return 서술자 + 3;
    }
    static int 확인(int 서술자) {
        return 서술자 >= 3 && 서술자 < 19 && uporaba_VALUE[서술자 - 3] != 0 ? 서술자 - 3 : -1;
    }
    public static int Branje(int 서술자) {
        int 칸 = 확인(서술자);
        if (칸 < 0 || (metoda_MODE[칸] & 3) == 1) return -9;
        int Datoteka = tarča[칸];
        if (Položaj[칸] >= 길이[Datoteka]) return 256; // EOF와 dejanski_podatki 0x00..0xff 구별
        return 자료읽기(Datoteka, Položaj[칸]++);
    }
    public static int Pisanje(int 서술자, int VALUE) {
        int 칸 = 확인(서술자);
        if (칸 < 0 || (metoda_MODE[칸] & 3) == 0) return -9;
        int Datoteka = tarča[칸];
        if ((metoda_MODE[칸] & 0x400) != 0) Položaj[칸] = 길이[Datoteka];
        if (Položaj[칸] >= 16384) return -28;
        while (길이[Datoteka] < Položaj[칸]) pisati_podatki(Datoteka, 길이[Datoteka]++, 0);
        pisati_podatki(Datoteka, Položaj[칸]++, VALUE);
        if (길이[Datoteka] < Položaj[칸]) 길이[Datoteka] = Položaj[칸];
        return 1;
    }
    public static int iskati_položaj(int 서술자, int 거리, int pobuda_koren) {
        int 칸 = 확인(서술자);
        if (칸 < 0) return -9;
        if (pobuda_koren < 0 || pobuda_koren > 2 || 거리 < -16384 || 거리 > 16384) return -22;
        int 새위치 = 거리 + (pobuda_koren == 0 ? 0 : pobuda_koren == 1 ? Položaj[칸] : 길이[tarča[칸]]);
        if (새위치 < 0 || 새위치 > 16384) return -22;
        Položaj[칸] = 새위치; return 새위치;
    }
    public static int Zapri(int 서술자) {
        int 칸 = 확인(서술자);
        if (칸 < 0) return -9;
        Gradiva_COUNT[tarča[칸]]--; uporaba_VALUE[칸] = 0; return 0;
    }
    public static int Velikost(int 서술자) {
        int 칸 = 확인(서술자); return 칸 < 0 ? -9 : 길이[tarča[칸]];
    }
    public static int 길이정하기(int 서술자, int Velikost) {
        int 칸 = 확인(서술자);
        if (칸 < 0 || (metoda_MODE[칸] & 3) == 0) return -9;
        if (Velikost < 0 || Velikost > 16384) return -22;
        int Datoteka = tarča[칸];
        while (길이[Datoteka] < Velikost) pisati_podatki(Datoteka, 길이[Datoteka]++, 0);
        길이[Datoteka] = Velikost; return 0;
    }
    public static int izbrisati_vnos() {
        if (경로길이 == 0) return -22;
        int REZULTAT = normalizirati_VALUE(); if (REZULTAT < 0) return REZULTAT;
        if (FIND_Imenik(정규길이) >= 0) return -21;
        REZULTAT = preveriti_nadrejen(); if (REZULTAT < 0) return REZULTAT;
        int Datoteka = FIND_vnos();
        if (Datoteka < 0) return -2;
        이름길이[Datoteka] = 0; return 0; // 열려 있는 파일은 마지막 close까지 유지
    }
    static void vnos_Seznam() {
        pot_Start(1); pot_bajt(0, '.'); 경로목록();
    }
    public static int 공개이름길이(int INDEX) {
        if (INDEX < 0 || INDEX >= Datoteka_COUNT || 이름길이[INDEX] == 0) return 0;
        for (int Loop_INDEX = 0; Loop_INDEX < 이름길이[INDEX]; Loop_INDEX++) if (Ime[INDEX * 64 + Loop_INDEX] == '/') return 0;
        return 이름길이[INDEX];
    }
    public static int 공개이름바이트(int INDEX, int kazalec_mesta) {
        return INDEX >= 0 && INDEX < Datoteka_COUNT && kazalec_mesta >= 0 && kazalec_mesta < 이름길이[INDEX] ? Ime[INDEX * 64 + kazalec_mesta] : -22;
    }
    public static int 공개파일크기(int INDEX) { return INDEX >= 0 && INDEX < Datoteka_COUNT ? 길이[INDEX] : -22; }
    static int[] 정규 = new int[64], sprotno_element = new int[64], Imenik_ime = new int[16 * 64], 폴더길이 = new int[16];
    static int 정규길이, 현재길이;
    static boolean 접두(int[] 이름들, int Zaženi, int pot_VALUE, int[] sprednja_VALUE, int razmik_vrstic_pot) {
        if (pot_VALUE < razmik_vrstic_pot) return false;
        for (int Loop_INDEX = 0; Loop_INDEX < razmik_vrstic_pot; Loop_INDEX++) if (이름들[Zaženi + Loop_INDEX] != sprednja_VALUE[Loop_INDEX]) return false;
        return true;
    }
    static int normalizirati_VALUE() {
        if (경로길이 == 0) return -22;
        정규길이 = POT[0] == '/' ? 0 : 현재길이;
        for (int Loop_INDEX = 0; Loop_INDEX < 정규길이; Loop_INDEX++) 정규[Loop_INDEX] = sprotno_element[Loop_INDEX];
        int 읽는자리 = 0;
        while (읽는자리 < 경로길이) {
            while (읽는자리 < 경로길이 && POT[읽는자리] == '/') 읽는자리++;
            int Start_položaj = 읽는자리; while (읽는자리 < 경로길이 && POT[읽는자리] != '/') { if (POT[읽는자리] == 0) return -22; 읽는자리++; }
            int vnos_COUNT = 읽는자리 - Start_položaj; if (vnos_COUNT == 0 || vnos_COUNT == 1 && POT[Start_položaj] == '.') continue;
            if (vnos_COUNT == 2 && POT[Start_položaj] == '.' && POT[Start_položaj + 1] == '.') {
                while (정규길이 > 0 && 정규[정규길이 - 1] != '/') 정규길이--;
                if (정규길이 > 0) 정규길이--;
                continue;
            }
            if (정규길이 + vnos_COUNT + (정규길이 == 0 ? 0 : 1) > 63) return -36;
            if (정규길이 > 0) 정규[정규길이++] = '/';
            for (int Loop_INDEX = Start_položaj; Loop_INDEX < 읽는자리; Loop_INDEX++) 정규[정규길이++] = POT[Loop_INDEX];
        }
        return 0;
    }
    static int FIND_Imenik(int vnos_COUNT) {
        if (vnos_COUNT == 0) return 0;
        for (int Loop_INDEX = 1; Loop_INDEX < 16; Loop_INDEX++) if (폴더길이[Loop_INDEX] == vnos_COUNT && 접두(Imenik_ime, Loop_INDEX * 64, vnos_COUNT, 정규, vnos_COUNT)) return Loop_INDEX;
        return -1;
    }
    static int preveriti_nadrejen() {
        int vnos_COUNT = 정규길이; while (vnos_COUNT > 0 && 정규[vnos_COUNT - 1] != '/') vnos_COUNT--;
        return FIND_Imenik(vnos_COUNT == 0 ? 0 : vnos_COUNT - 1) < 0 ? -2 : 0;
    }
    public static int Ustvari_Imenik() {
        int 처리값 = normalizirati_VALUE(); if (처리값 < 0) return 처리값;
        if (FIND_Imenik(정규길이) >= 0 || FIND_vnos() >= 0) return -17;
        처리값 = preveriti_nadrejen(); if (처리값 < 0) return 처리값;
        for (int Loop_INDEX = 1; Loop_INDEX < 16; Loop_INDEX++) if (폴더길이[Loop_INDEX] == 0) {
            폴더길이[Loop_INDEX] = 정규길이; for (int notranje_položaj = 0; notranje_položaj < 정규길이; notranje_položaj++) Imenik_ime[Loop_INDEX * 64 + notranje_položaj] = 정규[notranje_položaj]; return 0;
        }
        return -28;
    }
    public static int 항목종류() {
        int 처리값 = normalizirati_VALUE(); if (처리값 < 0) return 처리값;
        if (FIND_Imenik(정규길이) >= 0) return 2;
        return FIND_vnos() >= 0 ? 1 : 0;
    }
    public static int spremeniti_Imenik() {
        int 처리값 = normalizirati_VALUE(); if (처리값 < 0) return 처리값;
        if (FIND_Imenik(정규길이) < 0) return -2;
        현재길이 = 정규길이; for (int Loop_INDEX = 0; Loop_INDEX < 현재길이; Loop_INDEX++) sprotno_element[Loop_INDEX] = 정규[Loop_INDEX]; return 0;
    }
    public static int odstraniti_Imenik() {
        int 처리값 = normalizirati_VALUE(); if (처리값 < 0) return 처리값;
        int 폴더번호 = FIND_Imenik(정규길이); if (폴더번호 < 0) return -2; if (폴더번호 == 0) return -16;
        if (현재길이 == 정규길이 && 접두(sprotno_element, 0, 현재길이, 정규, 정규길이)) return -16;
        for (int Loop_INDEX = 0; Loop_INDEX < Datoteka_COUNT; Loop_INDEX++) {
            if (이름길이[Loop_INDEX] > 정규길이 && 접두(Ime, Loop_INDEX * 64, 이름길이[Loop_INDEX], 정규, 정규길이) && Ime[Loop_INDEX * 64 + 정규길이] == '/') return -39;
        }
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) {
            if (폴더길이[Loop_INDEX] > 정규길이 && 접두(Imenik_ime, Loop_INDEX * 64, 폴더길이[Loop_INDEX], 정규, 정규길이) && Imenik_ime[Loop_INDEX * 64 + 정규길이] == '/') return -39;
        }
        폴더길이[폴더번호] = 0; return 0;
    }
    public static int Preimenuj_vnos(int 원본번호) {
        if (원본번호 < 0 || 원본번호 >= Datoteka_COUNT || 이름길이[원본번호] == 0) return -2;
        int 처리값 = normalizirati_VALUE(); if (처리값 < 0) return 처리값;
        if (FIND_Imenik(정규길이) >= 0) return -21;
        처리값 = preveriti_nadrejen(); if (처리값 < 0) return 처리값;
        int 이전값 = FIND_vnos(); if (이전값 == 원본번호) return 0;
        if (이전값 >= 0) 이름길이[이전값] = 0;
        이름길이[원본번호] = 정규길이; for (int Loop_INDEX = 0; Loop_INDEX < 정규길이; Loop_INDEX++) Ime[원본번호 * 64 + Loop_INDEX] = 정규[Loop_INDEX]; return 0;
    }
    static int vnos_Start(int[] podatki_ARRAY, int 시작점, int vnos_COUNT) {
        if (!접두(podatki_ARRAY, 시작점, vnos_COUNT, 정규, 정규길이)) return -1;
        int Start_položaj = 정규길이;
        if (Start_položaj > 0) { if (vnos_COUNT <= Start_položaj || podatki_ARRAY[시작점 + Start_položaj] != '/') return -1; Start_položaj++; }
        if (vnos_COUNT <= Start_položaj) return -1;
        for (int Loop_INDEX = Start_položaj; Loop_INDEX < vnos_COUNT; Loop_INDEX++) if (podatki_ARRAY[시작점 + Loop_INDEX] == '/') return -1;
        return Start_položaj;
    }
    static void sprotno_pisati() { 단말.문자('/'); for (int Loop_INDEX = 0; Loop_INDEX < 현재길이; Loop_INDEX++) Tabla.직렬쓰기(sprotno_element[Loop_INDEX]); }
    static int 경로목록() {
        int 처리값 = normalizirati_VALUE(); if (처리값 < 0) return 처리값;
        int Datoteka_tarča = FIND_vnos();
        if (Datoteka_tarča >= 0) { for (int Loop_INDEX = 0; Loop_INDEX < 정규길이; Loop_INDEX++) Tabla.직렬쓰기(정규[Loop_INDEX]); 단말.Pisanje("  "); 단말.수(길이[Datoteka_tarča]); 단말.Pisanje("bajt_VALUE(주기억 Datoteka)\n"); return 0; }
        if (FIND_Imenik(정규길이) < 0) return -2;
        for (int 뒷값 = 1; 뒷값 < 16; 뒷값++) if (폴더길이[뒷값] > 0) {
            int Start_položaj = vnos_Start(Imenik_ime, 뒷값 * 64, 폴더길이[뒷값]); if (Start_položaj < 0) continue;
            for (int Loop_INDEX = Start_položaj; Loop_INDEX < 폴더길이[뒷값]; Loop_INDEX++) Tabla.직렬쓰기(Imenik_ime[뒷값 * 64 + Loop_INDEX]); 단말.Pisanje("/\n");
        }
        for (int Datoteka_INDEX = 0; Datoteka_INDEX < Datoteka_COUNT; Datoteka_INDEX++) if (이름길이[Datoteka_INDEX] > 0) {
            int Start_položaj = vnos_Start(Ime, Datoteka_INDEX * 64, 이름길이[Datoteka_INDEX]); if (Start_položaj < 0) continue;
            for (int Loop_INDEX = Start_položaj; Loop_INDEX < 이름길이[Datoteka_INDEX]; Loop_INDEX++) Tabla.직렬쓰기(Ime[Datoteka_INDEX * 64 + Loop_INDEX]);
            단말.Pisanje("  "); 단말.수(길이[Datoteka_INDEX]); 단말.Pisanje("bajt_VALUE(주기억 Datoteka)\n");
        }
        return 0;
    }
}
