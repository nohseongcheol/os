// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** RAM Fails 64개, 파일당 16384바이트, 서술자 16개. 모든 dati/정책은 Java에 있다.
 * 호출 도중 양보하지 않으므로 현재의 단일 코어 협력식 작업 사이에서 원자적이다.
 * 디스크 저장이나 POSIX 전체 구현을 뜻하지 않는다. 음수 반환은 Kļūda 번호다.
 */
public final class atmiņa_Faili {
    static final int Fails_COUNT = 64;
    static int[] Nosaukums = new int[Fails_COUNT * 64];
    static int[] 이름길이 = new int[Fails_COUNT];
    // Pack four bytes in each Java int, preserving the old content heap budget.
    static int[] Saturs_VALUE = new int[Fails_COUNT * 4096];
    static int[] 길이 = new int[Fails_COUNT];
    static int[] Uzziņas_COUNT = new int[Fails_COUNT];
    static int[] lietot_VALUE = new int[16];
    static int[] mērķis = new int[16];
    static int[] Novietojums = new int[16];
    static int[] metode_MODE = new int[16];
    static int[] CEĻŠ = new int[64];
    static int 경로길이;

    public static int 파일한도() { return Fails_COUNT; }
    static int 자료읽기(int Fails, int pozīcijas_indekss) { return (Saturs_VALUE[Fails * 4096 + pozīcijas_indekss / 4] >>> ((pozīcijas_indekss & 3) * 8)) & 255; }
    static void rakstīšana_dati(int Fails, int pozīcijas_indekss, int VALUE) {
        int 칸 = Fails * 4096 + pozīcijas_indekss / 4, pārvietot_VALUE = (pozīcijas_indekss & 3) * 8;
        Saturs_VALUE[칸] = (Saturs_VALUE[칸] & ~(255 << pārvietot_VALUE)) | ((VALUE & 255) << pārvietot_VALUE);
    }

    public static int ceļš_Sākt(int Izmērs) {
        경로길이 = 0;
        if (Izmērs < 1 || Izmērs > 63) return -36;
        경로길이 = Izmērs;
        for (int Loop_INDEX = 0; Loop_INDEX < Izmērs; Loop_INDEX++) CEĻŠ[Loop_INDEX] = 0;
        return 0;
    }
    public static int ceļš_byte(int INDEX, int VALUE) {
        if (INDEX < 0 || INDEX >= 경로길이 || VALUE < 1 || VALUE > 255) return -22;
        CEĻŠ[INDEX] = VALUE; return 0;
    }
    static int FIND_ievade() {
        for (int Fails_INDEX = 0; Fails_INDEX < Fails_COUNT; Fails_INDEX++) if (이름길이[Fails_INDEX] > 0 && 이름길이[Fails_INDEX] == 정규길이 && 접두(Nosaukums, Fails_INDEX * 64, 이름길이[Fails_INDEX], 정규, 정규길이)) return Fails_INDEX;
        return -1;
    }
    public static int Atvērt(int 플래그) {
        if (경로길이 == 0 || (플래그 & ~0x6c3) != 0 || (플래그 & 3) == 3) return -22;
        for (int Loop_INDEX = 0; Loop_INDEX < 경로길이; Loop_INDEX++) if (CEĻŠ[Loop_INDEX] == 0) return -22;
        if ((플래그 & 0x200) != 0 && (플래그 & 3) == 0) return -22;
        int mērs = normalizēt_VALUE(); if (mērs < 0) return mērs;
        if (FIND_Direktorijs(정규길이) >= 0) return -21;
        mērs = čeks_vecākobjekts(); if (mērs < 0) return mērs;
        int Fails = FIND_ievade();
        if (Fails >= 0 && (플래그 & 0xc0) == 0xc0) return -17;
        if (Fails < 0 && (플래그 & 0x40) == 0) return -2;
        int 서술자 = -1;
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (lietot_VALUE[Loop_INDEX] == 0) { 서술자 = Loop_INDEX; break; }
        if (서술자 < 0) return -24;
        if (Fails < 0) {
            for (int Loop_INDEX = 0; Loop_INDEX < Fails_COUNT; Loop_INDEX++) if (이름길이[Loop_INDEX] == 0 && Uzziņas_COUNT[Loop_INDEX] == 0) { Fails = Loop_INDEX; break; }
            if (Fails < 0) return -28;
            이름길이[Fails] = 정규길이;
            for (int Loop_INDEX = 0; Loop_INDEX < 정규길이; Loop_INDEX++) Nosaukums[Fails * 64 + Loop_INDEX] = 정규[Loop_INDEX];
            길이[Fails] = 0;
        }
        if ((플래그 & 0x200) != 0) 길이[Fails] = 0;
        lietot_VALUE[서술자] = 1; mērķis[서술자] = Fails; Novietojums[서술자] = 0; metode_MODE[서술자] = 플래그;
        Uzziņas_COUNT[Fails]++;
        return 서술자 + 3;
    }
    static int verificēt(int 서술자) {
        return 서술자 >= 3 && 서술자 < 19 && lietot_VALUE[서술자 - 3] != 0 ? 서술자 - 3 : -1;
    }
    public static int Lasīt(int 서술자) {
        int 칸 = verificēt(서술자);
        if (칸 < 0 || (metode_MODE[칸] & 3) == 1) return -9;
        int Fails = mērķis[칸];
        if (Novietojums[칸] >= 길이[Fails]) return 256; // EOF와 faktisks_dati 0x00..0xff 구별
        return 자료읽기(Fails, Novietojums[칸]++);
    }
    public static int Rakstīt(int 서술자, int VALUE) {
        int 칸 = verificēt(서술자);
        if (칸 < 0 || (metode_MODE[칸] & 3) == 0) return -9;
        int Fails = mērķis[칸];
        if ((metode_MODE[칸] & 0x400) != 0) Novietojums[칸] = 길이[Fails];
        if (Novietojums[칸] >= 16384) return -28;
        while (길이[Fails] < Novietojums[칸]) rakstīšana_dati(Fails, 길이[Fails]++, 0);
        rakstīšana_dati(Fails, Novietojums[칸]++, VALUE);
        if (길이[Fails] < Novietojums[칸]) 길이[Fails] = Novietojums[칸];
        return 1;
    }
    public static int meklēt_amats(int 서술자, int 거리, int Project_sakne) {
        int 칸 = verificēt(서술자);
        if (칸 < 0) return -9;
        if (Project_sakne < 0 || Project_sakne > 2 || 거리 < -16384 || 거리 > 16384) return -22;
        int 새위치 = 거리 + (Project_sakne == 0 ? 0 : Project_sakne == 1 ? Novietojums[칸] : 길이[mērķis[칸]]);
        if (새위치 < 0 || 새위치 > 16384) return -22;
        Novietojums[칸] = 새위치; return 새위치;
    }
    public static int Aizvērt(int 서술자) {
        int 칸 = verificēt(서술자);
        if (칸 < 0) return -9;
        Uzziņas_COUNT[mērķis[칸]]--; lietot_VALUE[칸] = 0; return 0;
    }
    public static int Izmērs(int 서술자) {
        int 칸 = verificēt(서술자); return 칸 < 0 ? -9 : 길이[mērķis[칸]];
    }
    public static int 길이정하기(int 서술자, int Izmērs) {
        int 칸 = verificēt(서술자);
        if (칸 < 0 || (metode_MODE[칸] & 3) == 0) return -9;
        if (Izmērs < 0 || Izmērs > 16384) return -22;
        int Fails = mērķis[칸];
        while (길이[Fails] < Izmērs) rakstīšana_dati(Fails, 길이[Fails]++, 0);
        길이[Fails] = Izmērs; return 0;
    }
    public static int dzēst_ievade() {
        if (경로길이 == 0) return -22;
        int mērs = normalizēt_VALUE(); if (mērs < 0) return mērs;
        if (FIND_Direktorijs(정규길이) >= 0) return -21;
        mērs = čeks_vecākobjekts(); if (mērs < 0) return mērs;
        int Fails = FIND_ievade();
        if (Fails < 0) return -2;
        이름길이[Fails] = 0; return 0; // 열려 있는 파일은 마지막 close까지 유지
    }
    static void ievade_Saraksts() {
        ceļš_Sākt(1); ceļš_byte(0, '.'); 경로목록();
    }
    public static int 공개이름길이(int INDEX) {
        if (INDEX < 0 || INDEX >= Fails_COUNT || 이름길이[INDEX] == 0) return 0;
        for (int Loop_INDEX = 0; Loop_INDEX < 이름길이[INDEX]; Loop_INDEX++) if (Nosaukums[INDEX * 64 + Loop_INDEX] == '/') return 0;
        return 이름길이[INDEX];
    }
    public static int 공개이름바이트(int INDEX, int pozīcijas_indekss) {
        return INDEX >= 0 && INDEX < Fails_COUNT && pozīcijas_indekss >= 0 && pozīcijas_indekss < 이름길이[INDEX] ? Nosaukums[INDEX * 64 + pozīcijas_indekss] : -22;
    }
    public static int 공개파일크기(int INDEX) { return INDEX >= 0 && INDEX < Fails_COUNT ? 길이[INDEX] : -22; }
    static int[] 정규 = new int[64], pašreizējais_krājums = new int[64], Direktorijs_nosaukums = new int[16 * 64], 폴더길이 = new int[16];
    static int 정규길이, 현재길이;
    static boolean 접두(int[] 이름들, int Palaist, int ceļš_VALUE, int[] priekšējā_VALUE, int rindstarpa_ceļš) {
        if (ceļš_VALUE < rindstarpa_ceļš) return false;
        for (int Loop_INDEX = 0; Loop_INDEX < rindstarpa_ceļš; Loop_INDEX++) if (이름들[Palaist + Loop_INDEX] != priekšējā_VALUE[Loop_INDEX]) return false;
        return true;
    }
    static int normalizēt_VALUE() {
        if (경로길이 == 0) return -22;
        정규길이 = CEĻŠ[0] == '/' ? 0 : 현재길이;
        for (int Loop_INDEX = 0; Loop_INDEX < 정규길이; Loop_INDEX++) 정규[Loop_INDEX] = pašreizējais_krājums[Loop_INDEX];
        int 읽는자리 = 0;
        while (읽는자리 < 경로길이) {
            while (읽는자리 < 경로길이 && CEĻŠ[읽는자리] == '/') 읽는자리++;
            int Sākt_amats = 읽는자리; while (읽는자리 < 경로길이 && CEĻŠ[읽는자리] != '/') { if (CEĻŠ[읽는자리] == 0) return -22; 읽는자리++; }
            int ievade_COUNT = 읽는자리 - Sākt_amats; if (ievade_COUNT == 0 || ievade_COUNT == 1 && CEĻŠ[Sākt_amats] == '.') continue;
            if (ievade_COUNT == 2 && CEĻŠ[Sākt_amats] == '.' && CEĻŠ[Sākt_amats + 1] == '.') {
                while (정규길이 > 0 && 정규[정규길이 - 1] != '/') 정규길이--;
                if (정규길이 > 0) 정규길이--;
                continue;
            }
            if (정규길이 + ievade_COUNT + (정규길이 == 0 ? 0 : 1) > 63) return -36;
            if (정규길이 > 0) 정규[정규길이++] = '/';
            for (int Loop_INDEX = Sākt_amats; Loop_INDEX < 읽는자리; Loop_INDEX++) 정규[정규길이++] = CEĻŠ[Loop_INDEX];
        }
        return 0;
    }
    static int FIND_Direktorijs(int ievade_COUNT) {
        if (ievade_COUNT == 0) return 0;
        for (int Loop_INDEX = 1; Loop_INDEX < 16; Loop_INDEX++) if (폴더길이[Loop_INDEX] == ievade_COUNT && 접두(Direktorijs_nosaukums, Loop_INDEX * 64, ievade_COUNT, 정규, ievade_COUNT)) return Loop_INDEX;
        return -1;
    }
    static int čeks_vecākobjekts() {
        int ievade_COUNT = 정규길이; while (ievade_COUNT > 0 && 정규[ievade_COUNT - 1] != '/') ievade_COUNT--;
        return FIND_Direktorijs(ievade_COUNT == 0 ? 0 : ievade_COUNT - 1) < 0 ? -2 : 0;
    }
    public static int atvērt_Direktorijs() {
        int 처리값 = normalizēt_VALUE(); if (처리값 < 0) return 처리값;
        if (FIND_Direktorijs(정규길이) >= 0 || FIND_ievade() >= 0) return -17;
        처리값 = čeks_vecākobjekts(); if (처리값 < 0) return 처리값;
        for (int Loop_INDEX = 1; Loop_INDEX < 16; Loop_INDEX++) if (폴더길이[Loop_INDEX] == 0) {
            폴더길이[Loop_INDEX] = 정규길이; for (int iekšējais_amats = 0; iekšējais_amats < 정규길이; iekšējais_amats++) Direktorijs_nosaukums[Loop_INDEX * 64 + iekšējais_amats] = 정규[iekšējais_amats]; return 0;
        }
        return -28;
    }
    public static int 항목종류() {
        int 처리값 = normalizēt_VALUE(); if (처리값 < 0) return 처리값;
        if (FIND_Direktorijs(정규길이) >= 0) return 2;
        return FIND_ievade() >= 0 ? 1 : 0;
    }
    public static int mainīt_Direktorijs() {
        int 처리값 = normalizēt_VALUE(); if (처리값 < 0) return 처리값;
        if (FIND_Direktorijs(정규길이) < 0) return -2;
        현재길이 = 정규길이; for (int Loop_INDEX = 0; Loop_INDEX < 현재길이; Loop_INDEX++) pašreizējais_krājums[Loop_INDEX] = 정규[Loop_INDEX]; return 0;
    }
    public static int noņemt_Direktorijs() {
        int 처리값 = normalizēt_VALUE(); if (처리값 < 0) return 처리값;
        int Direktorijs_numurs = FIND_Direktorijs(정규길이); if (Direktorijs_numurs < 0) return -2; if (Direktorijs_numurs == 0) return -16;
        if (현재길이 == 정규길이 && 접두(pašreizējais_krājums, 0, 현재길이, 정규, 정규길이)) return -16;
        for (int Loop_INDEX = 0; Loop_INDEX < Fails_COUNT; Loop_INDEX++) {
            if (이름길이[Loop_INDEX] > 정규길이 && 접두(Nosaukums, Loop_INDEX * 64, 이름길이[Loop_INDEX], 정규, 정규길이) && Nosaukums[Loop_INDEX * 64 + 정규길이] == '/') return -39;
        }
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) {
            if (폴더길이[Loop_INDEX] > 정규길이 && 접두(Direktorijs_nosaukums, Loop_INDEX * 64, 폴더길이[Loop_INDEX], 정규, 정규길이) && Direktorijs_nosaukums[Loop_INDEX * 64 + 정규길이] == '/') return -39;
        }
        폴더길이[Direktorijs_numurs] = 0; return 0;
    }
    public static int Pārdēvēt_ievade(int 원본번호) {
        if (원본번호 < 0 || 원본번호 >= Fails_COUNT || 이름길이[원본번호] == 0) return -2;
        int 처리값 = normalizēt_VALUE(); if (처리값 < 0) return 처리값;
        if (FIND_Direktorijs(정규길이) >= 0) return -21;
        처리값 = čeks_vecākobjekts(); if (처리값 < 0) return 처리값;
        int 이전값 = FIND_ievade(); if (이전값 == 원본번호) return 0;
        if (이전값 >= 0) 이름길이[이전값] = 0;
        이름길이[원본번호] = 정규길이; for (int Loop_INDEX = 0; Loop_INDEX < 정규길이; Loop_INDEX++) Nosaukums[원본번호 * 64 + Loop_INDEX] = 정규[Loop_INDEX]; return 0;
    }
    static int ievade_Sākt(int[] dati_ARRAY, int 시작점, int ievade_COUNT) {
        if (!접두(dati_ARRAY, 시작점, ievade_COUNT, 정규, 정규길이)) return -1;
        int Sākt_amats = 정규길이;
        if (Sākt_amats > 0) { if (ievade_COUNT <= Sākt_amats || dati_ARRAY[시작점 + Sākt_amats] != '/') return -1; Sākt_amats++; }
        if (ievade_COUNT <= Sākt_amats) return -1;
        for (int Loop_INDEX = Sākt_amats; Loop_INDEX < ievade_COUNT; Loop_INDEX++) if (dati_ARRAY[시작점 + Loop_INDEX] == '/') return -1;
        return Sākt_amats;
    }
    static void pašreizējais_rakstīšana() { 단말.문자('/'); for (int Loop_INDEX = 0; Loop_INDEX < 현재길이; Loop_INDEX++) Panelis.직렬쓰기(pašreizējais_krājums[Loop_INDEX]); }
    static int 경로목록() {
        int 처리값 = normalizēt_VALUE(); if (처리값 < 0) return 처리값;
        int Fails_mērķis = FIND_ievade();
        if (Fails_mērķis >= 0) { for (int Loop_INDEX = 0; Loop_INDEX < 정규길이; Loop_INDEX++) Panelis.직렬쓰기(정규[Loop_INDEX]); 단말.Rakstīt("  "); 단말.numurs(길이[Fails_mērķis]); 단말.Rakstīt("byte_VALUE(주기억 Fails)\n"); return 0; }
        if (FIND_Direktorijs(정규길이) < 0) return -2;
        for (int 뒷값 = 1; 뒷값 < 16; 뒷값++) if (폴더길이[뒷값] > 0) {
            int Sākt_amats = ievade_Sākt(Direktorijs_nosaukums, 뒷값 * 64, 폴더길이[뒷값]); if (Sākt_amats < 0) continue;
            for (int Loop_INDEX = Sākt_amats; Loop_INDEX < 폴더길이[뒷값]; Loop_INDEX++) Panelis.직렬쓰기(Direktorijs_nosaukums[뒷값 * 64 + Loop_INDEX]); 단말.Rakstīt("/\n");
        }
        for (int Fails_INDEX = 0; Fails_INDEX < Fails_COUNT; Fails_INDEX++) if (이름길이[Fails_INDEX] > 0) {
            int Sākt_amats = ievade_Sākt(Nosaukums, Fails_INDEX * 64, 이름길이[Fails_INDEX]); if (Sākt_amats < 0) continue;
            for (int Loop_INDEX = Sākt_amats; Loop_INDEX < 이름길이[Fails_INDEX]; Loop_INDEX++) Panelis.직렬쓰기(Nosaukums[Fails_INDEX * 64 + Loop_INDEX]);
            단말.Rakstīt("  "); 단말.numurs(길이[Fails_INDEX]); 단말.Rakstīt("byte_VALUE(주기억 Fails)\n");
        }
        return 0;
    }
}
