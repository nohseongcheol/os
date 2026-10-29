// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** RAM Skrá 64개, 파일당 16384바이트, 서술자 16개. 모든 gögn/정책은 Java에 있다.
 * 호출 도중 양보하지 않으므로 현재의 단일 코어 협력식 작업 사이에서 원자적이다.
 * 디스크 저장이나 POSIX 전체 구현을 뜻하지 않는다. 음수 반환은 Villa 번호다.
 */
public final class Minni_Skrár {
    static final int skrá_COUNT = 64;
    static int[] Heiti = new int[skrá_COUNT * 64];
    static int[] 이름길이 = new int[skrá_COUNT];
    // Pack four bytes in each Java int, preserving the old content heap budget.
    static int[] Efni_VALUE = new int[skrá_COUNT * 4096];
    static int[] lengd_VALUE = new int[skrá_COUNT];
    static int[] tilvísun_COUNT = new int[skrá_COUNT];
    static int[] 사용 = new int[16];
    static int[] markmið = new int[16];
    static int[] Staðsetning = new int[16];
    static int[] aðferð_MODE = new int[16];
    static int[] SLÓÐ = new int[64];
    static int slóð_lengd;

    public static int 파일한도() { return skrá_COUNT; }
    static int 자료읽기(int Skrá, int staða_INDEX) { return (Efni_VALUE[Skrá * 4096 + staða_INDEX / 4] >>> ((staða_INDEX & 3) * 8)) & 255; }
    static void skrifa_gögn(int Skrá, int staða_INDEX, int VALUE) {
        int rauf_færsla = Skrá * 4096 + staða_INDEX / 4, færa_VALUE = (staða_INDEX & 3) * 8;
        Efni_VALUE[rauf_færsla] = (Efni_VALUE[rauf_færsla] & ~(255 << færa_VALUE)) | ((VALUE & 255) << færa_VALUE);
    }

    public static int slóð_Opna(int Stærð) {
        slóð_lengd = 0;
        if (Stærð < 1 || Stærð > 63) return -36;
        slóð_lengd = Stærð;
        for (int Loop_INDEX = 0; Loop_INDEX < Stærð; Loop_INDEX++) SLÓÐ[Loop_INDEX] = 0;
        return 0;
    }
    public static int slóð_bæti(int INDEX, int VALUE) {
        if (INDEX < 0 || INDEX >= slóð_lengd || VALUE < 1 || VALUE > 255) return -22;
        SLÓÐ[INDEX] = VALUE; return 0;
    }
    static int FIND_færsla() {
        for (int skrá_INDEX = 0; skrá_INDEX < skrá_COUNT; skrá_INDEX++) if (이름길이[skrá_INDEX] > 0 && 이름길이[skrá_INDEX] == 정규길이 && 접두(Heiti, skrá_INDEX * 64, 이름길이[skrá_INDEX], 정규, 정규길이)) return skrá_INDEX;
        return -1;
    }
    public static int Opna(int 플래그) {
        if (slóð_lengd == 0 || (플래그 & ~0x6c3) != 0 || (플래그 & 3) == 3) return -22;
        for (int Loop_INDEX = 0; Loop_INDEX < slóð_lengd; Loop_INDEX++) if (SLÓÐ[Loop_INDEX] == 0) return -22;
        if ((플래그 & 0x200) != 0 && (플래그 & 3) == 0) return -22;
        int NIÐURSTAÐA = staðla_VALUE(); if (NIÐURSTAÐA < 0) return NIÐURSTAÐA;
        if (FIND_skráasafn(정규길이) >= 0) return -21;
        NIÐURSTAÐA = athuga_yfireining(); if (NIÐURSTAÐA < 0) return NIÐURSTAÐA;
        int Skrá = FIND_færsla();
        if (Skrá >= 0 && (플래그 & 0xc0) == 0xc0) return -17;
        if (Skrá < 0 && (플래그 & 0x40) == 0) return -2;
        int 서술자 = -1;
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (사용[Loop_INDEX] == 0) { 서술자 = Loop_INDEX; break; }
        if (서술자 < 0) return -24;
        if (Skrá < 0) {
            for (int Loop_INDEX = 0; Loop_INDEX < skrá_COUNT; Loop_INDEX++) if (이름길이[Loop_INDEX] == 0 && tilvísun_COUNT[Loop_INDEX] == 0) { Skrá = Loop_INDEX; break; }
            if (Skrá < 0) return -28;
            이름길이[Skrá] = 정규길이;
            for (int Loop_INDEX = 0; Loop_INDEX < 정규길이; Loop_INDEX++) Heiti[Skrá * 64 + Loop_INDEX] = 정규[Loop_INDEX];
            lengd_VALUE[Skrá] = 0;
        }
        if ((플래그 & 0x200) != 0) lengd_VALUE[Skrá] = 0;
        사용[서술자] = 1; markmið[서술자] = Skrá; Staðsetning[서술자] = 0; aðferð_MODE[서술자] = 플래그;
        tilvísun_COUNT[Skrá]++;
        return 서술자 + 3;
    }
    static int sannprófa(int 서술자) {
        return 서술자 >= 3 && 서술자 < 19 && 사용[서술자 - 3] != 0 ? 서술자 - 3 : -1;
    }
    public static int Lestur(int 서술자) {
        int rauf_færsla = sannprófa(서술자);
        if (rauf_færsla < 0 || (aðferð_MODE[rauf_færsla] & 3) == 1) return -9;
        int Skrá = markmið[rauf_færsla];
        if (Staðsetning[rauf_færsla] >= lengd_VALUE[Skrá]) return 256; // EOF와 raun_gögn 0x00..0xff 구별
        return 자료읽기(Skrá, Staðsetning[rauf_færsla]++);
    }
    public static int Skrift(int 서술자, int VALUE) {
        int rauf_færsla = sannprófa(서술자);
        if (rauf_færsla < 0 || (aðferð_MODE[rauf_færsla] & 3) == 0) return -9;
        int Skrá = markmið[rauf_færsla];
        if ((aðferð_MODE[rauf_færsla] & 0x400) != 0) Staðsetning[rauf_færsla] = lengd_VALUE[Skrá];
        if (Staðsetning[rauf_færsla] >= 16384) return -28;
        while (lengd_VALUE[Skrá] < Staðsetning[rauf_færsla]) skrifa_gögn(Skrá, lengd_VALUE[Skrá]++, 0);
        skrifa_gögn(Skrá, Staðsetning[rauf_færsla]++, VALUE);
        if (lengd_VALUE[Skrá] < Staðsetning[rauf_færsla]) lengd_VALUE[Skrá] = Staðsetning[rauf_færsla];
        return 1;
    }
    public static int leita_staða(int 서술자, int 거리, int verk_rót) {
        int rauf_færsla = sannprófa(서술자);
        if (rauf_færsla < 0) return -9;
        if (verk_rót < 0 || verk_rót > 2 || 거리 < -16384 || 거리 > 16384) return -22;
        int 새위치 = 거리 + (verk_rót == 0 ? 0 : verk_rót == 1 ? Staðsetning[rauf_færsla] : lengd_VALUE[markmið[rauf_færsla]]);
        if (새위치 < 0 || 새위치 > 16384) return -22;
        Staðsetning[rauf_færsla] = 새위치; return 새위치;
    }
    public static int Loka(int 서술자) {
        int rauf_færsla = sannprófa(서술자);
        if (rauf_færsla < 0) return -9;
        tilvísun_COUNT[markmið[rauf_færsla]]--; 사용[rauf_færsla] = 0; return 0;
    }
    public static int Stærð(int 서술자) {
        int rauf_færsla = sannprófa(서술자); return rauf_færsla < 0 ? -9 : lengd_VALUE[markmið[rauf_færsla]];
    }
    public static int sett_lengd(int 서술자, int Stærð) {
        int rauf_færsla = sannprófa(서술자);
        if (rauf_færsla < 0 || (aðferð_MODE[rauf_færsla] & 3) == 0) return -9;
        if (Stærð < 0 || Stærð > 16384) return -22;
        int Skrá = markmið[rauf_færsla];
        while (lengd_VALUE[Skrá] < Stærð) skrifa_gögn(Skrá, lengd_VALUE[Skrá]++, 0);
        lengd_VALUE[Skrá] = Stærð; return 0;
    }
    public static int eyða_færsla() {
        if (slóð_lengd == 0) return -22;
        int NIÐURSTAÐA = staðla_VALUE(); if (NIÐURSTAÐA < 0) return NIÐURSTAÐA;
        if (FIND_skráasafn(정규길이) >= 0) return -21;
        NIÐURSTAÐA = athuga_yfireining(); if (NIÐURSTAÐA < 0) return NIÐURSTAÐA;
        int Skrá = FIND_færsla();
        if (Skrá < 0) return -2;
        이름길이[Skrá] = 0; return 0; // 열려 있는 파일은 마지막 close까지 유지
    }
    static void færsla_Listi() {
        slóð_Opna(1); slóð_bæti(0, '.'); 경로목록();
    }
    public static int 공개이름길이(int INDEX) {
        if (INDEX < 0 || INDEX >= skrá_COUNT || 이름길이[INDEX] == 0) return 0;
        for (int Loop_INDEX = 0; Loop_INDEX < 이름길이[INDEX]; Loop_INDEX++) if (Heiti[INDEX * 64 + Loop_INDEX] == '/') return 0;
        return 이름길이[INDEX];
    }
    public static int 공개이름바이트(int INDEX, int staða_INDEX) {
        return INDEX >= 0 && INDEX < skrá_COUNT && staða_INDEX >= 0 && staða_INDEX < 이름길이[INDEX] ? Heiti[INDEX * 64 + staða_INDEX] : -22;
    }
    public static int 공개파일크기(int INDEX) { return INDEX >= 0 && INDEX < skrá_COUNT ? lengd_VALUE[INDEX] : -22; }
    static int[] 정규 = new int[64], 현재 = new int[64], skráasafn_heiti = new int[16 * 64], skráasafn_lengd = new int[16];
    static int 정규길이, 현재길이;
    static boolean 접두(int[] 이름들, int Keyra_2, int slóð_VALUE_d72c8434, int[] myndavél_að_framan_VALUE, int línubil_slóð) {
        if (slóð_VALUE_d72c8434 < línubil_slóð) return false;
        for (int Loop_INDEX = 0; Loop_INDEX < línubil_slóð; Loop_INDEX++) if (이름들[Keyra_2 + Loop_INDEX] != myndavél_að_framan_VALUE[Loop_INDEX]) return false;
        return true;
    }
    static int staðla_VALUE() {
        if (slóð_lengd == 0) return -22;
        정규길이 = SLÓÐ[0] == '/' ? 0 : 현재길이;
        for (int Loop_INDEX = 0; Loop_INDEX < 정규길이; Loop_INDEX++) 정규[Loop_INDEX] = 현재[Loop_INDEX];
        int 읽는자리 = 0;
        while (읽는자리 < slóð_lengd) {
            while (읽는자리 < slóð_lengd && SLÓÐ[읽는자리] == '/') 읽는자리++;
            int Opna_staða = 읽는자리; while (읽는자리 < slóð_lengd && SLÓÐ[읽는자리] != '/') { if (SLÓÐ[읽는자리] == 0) return -22; 읽는자리++; }
            int færsla_COUNT = 읽는자리 - Opna_staða; if (færsla_COUNT == 0 || færsla_COUNT == 1 && SLÓÐ[Opna_staða] == '.') continue;
            if (færsla_COUNT == 2 && SLÓÐ[Opna_staða] == '.' && SLÓÐ[Opna_staða + 1] == '.') {
                while (정규길이 > 0 && 정규[정규길이 - 1] != '/') 정규길이--;
                if (정규길이 > 0) 정규길이--;
                continue;
            }
            if (정규길이 + færsla_COUNT + (정규길이 == 0 ? 0 : 1) > 63) return -36;
            if (정규길이 > 0) 정규[정규길이++] = '/';
            for (int Loop_INDEX = Opna_staða; Loop_INDEX < 읽는자리; Loop_INDEX++) 정규[정규길이++] = SLÓÐ[Loop_INDEX];
        }
        return 0;
    }
    static int FIND_skráasafn(int færsla_COUNT) {
        if (færsla_COUNT == 0) return 0;
        for (int Loop_INDEX = 1; Loop_INDEX < 16; Loop_INDEX++) if (skráasafn_lengd[Loop_INDEX] == færsla_COUNT && 접두(skráasafn_heiti, Loop_INDEX * 64, færsla_COUNT, 정규, færsla_COUNT)) return Loop_INDEX;
        return -1;
    }
    static int athuga_yfireining() {
        int færsla_COUNT = 정규길이; while (færsla_COUNT > 0 && 정규[færsla_COUNT - 1] != '/') færsla_COUNT--;
        return FIND_skráasafn(færsla_COUNT == 0 ? 0 : færsla_COUNT - 1) < 0 ? -2 : 0;
    }
    public static int stofna_skráasafn() {
        int 처리값 = staðla_VALUE(); if (처리값 < 0) return 처리값;
        if (FIND_skráasafn(정규길이) >= 0 || FIND_færsla() >= 0) return -17;
        처리값 = athuga_yfireining(); if (처리값 < 0) return 처리값;
        for (int Loop_INDEX = 1; Loop_INDEX < 16; Loop_INDEX++) if (skráasafn_lengd[Loop_INDEX] == 0) {
            skráasafn_lengd[Loop_INDEX] = 정규길이; for (int innri_samtenging_staða = 0; innri_samtenging_staða < 정규길이; innri_samtenging_staða++) skráasafn_heiti[Loop_INDEX * 64 + innri_samtenging_staða] = 정규[innri_samtenging_staða]; return 0;
        }
        return -28;
    }
    public static int 항목종류() {
        int 처리값 = staðla_VALUE(); if (처리값 < 0) return 처리값;
        if (FIND_skráasafn(정규길이) >= 0) return 2;
        return FIND_færsla() >= 0 ? 1 : 0;
    }
    public static int breyta_skráasafn() {
        int 처리값 = staðla_VALUE(); if (처리값 < 0) return 처리값;
        if (FIND_skráasafn(정규길이) < 0) return -2;
        현재길이 = 정규길이; for (int Loop_INDEX = 0; Loop_INDEX < 현재길이; Loop_INDEX++) 현재[Loop_INDEX] = 정규[Loop_INDEX]; return 0;
    }
    public static int fjarlægja_skráasafn() {
        int 처리값 = staðla_VALUE(); if (처리값 < 0) return 처리값;
        int skráasafn_númer = FIND_skráasafn(정규길이); if (skráasafn_númer < 0) return -2; if (skráasafn_númer == 0) return -16;
        if (현재길이 == 정규길이 && 접두(현재, 0, 현재길이, 정규, 정규길이)) return -16;
        for (int Loop_INDEX = 0; Loop_INDEX < skrá_COUNT; Loop_INDEX++) {
            if (이름길이[Loop_INDEX] > 정규길이 && 접두(Heiti, Loop_INDEX * 64, 이름길이[Loop_INDEX], 정규, 정규길이) && Heiti[Loop_INDEX * 64 + 정규길이] == '/') return -39;
        }
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) {
            if (skráasafn_lengd[Loop_INDEX] > 정규길이 && 접두(skráasafn_heiti, Loop_INDEX * 64, skráasafn_lengd[Loop_INDEX], 정규, 정규길이) && skráasafn_heiti[Loop_INDEX * 64 + 정규길이] == '/') return -39;
        }
        skráasafn_lengd[skráasafn_númer] = 0; return 0;
    }
    public static int 이름바꾸기(int 원본번호) {
        if (원본번호 < 0 || 원본번호 >= skrá_COUNT || 이름길이[원본번호] == 0) return -2;
        int 처리값 = staðla_VALUE(); if (처리값 < 0) return 처리값;
        if (FIND_skráasafn(정규길이) >= 0) return -21;
        처리값 = athuga_yfireining(); if (처리값 < 0) return 처리값;
        int 이전값 = FIND_færsla(); if (이전값 == 원본번호) return 0;
        if (이전값 >= 0) 이름길이[이전값] = 0;
        이름길이[원본번호] = 정규길이; for (int Loop_INDEX = 0; Loop_INDEX < 정규길이; Loop_INDEX++) Heiti[원본번호 * 64 + Loop_INDEX] = 정규[Loop_INDEX]; return 0;
    }
    static int færsla_Opna(int[] gögn_ARRAY, int 시작점, int færsla_COUNT) {
        if (!접두(gögn_ARRAY, 시작점, færsla_COUNT, 정규, 정규길이)) return -1;
        int Opna_staða = 정규길이;
        if (Opna_staða > 0) { if (færsla_COUNT <= Opna_staða || gögn_ARRAY[시작점 + Opna_staða] != '/') return -1; Opna_staða++; }
        if (færsla_COUNT <= Opna_staða) return -1;
        for (int Loop_INDEX = Opna_staða; Loop_INDEX < færsla_COUNT; Loop_INDEX++) if (gögn_ARRAY[시작점 + Loop_INDEX] == '/') return -1;
        return Opna_staða;
    }
    static void 현재쓰기() { 단말.문자('/'); for (int Loop_INDEX = 0; Loop_INDEX < 현재길이; Loop_INDEX++) bretti.직렬쓰기(현재[Loop_INDEX]); }
    static int 경로목록() {
        int 처리값 = staðla_VALUE(); if (처리값 < 0) return 처리값;
        int skrá_markmið = FIND_færsla();
        if (skrá_markmið >= 0) { for (int Loop_INDEX = 0; Loop_INDEX < 정규길이; Loop_INDEX++) bretti.직렬쓰기(정규[Loop_INDEX]); 단말.Skrift("  "); 단말.númer(lengd_VALUE[skrá_markmið]); 단말.Skrift("bæti_VALUE(주기억 Skrá)\n"); return 0; }
        if (FIND_skráasafn(정규길이) < 0) return -2;
        for (int 뒷값 = 1; 뒷값 < 16; 뒷값++) if (skráasafn_lengd[뒷값] > 0) {
            int Opna_staða = færsla_Opna(skráasafn_heiti, 뒷값 * 64, skráasafn_lengd[뒷값]); if (Opna_staða < 0) continue;
            for (int Loop_INDEX = Opna_staða; Loop_INDEX < skráasafn_lengd[뒷값]; Loop_INDEX++) bretti.직렬쓰기(skráasafn_heiti[뒷값 * 64 + Loop_INDEX]); 단말.Skrift("/\n");
        }
        for (int skrá_INDEX = 0; skrá_INDEX < skrá_COUNT; skrá_INDEX++) if (이름길이[skrá_INDEX] > 0) {
            int Opna_staða = færsla_Opna(Heiti, skrá_INDEX * 64, 이름길이[skrá_INDEX]); if (Opna_staða < 0) continue;
            for (int Loop_INDEX = Opna_staða; Loop_INDEX < 이름길이[skrá_INDEX]; Loop_INDEX++) bretti.직렬쓰기(Heiti[skrá_INDEX * 64 + Loop_INDEX]);
            단말.Skrift("  "); 단말.númer(lengd_VALUE[skrá_INDEX]); 단말.Skrift("bæti_VALUE(주기억 Skrá)\n");
        }
        return 0;
    }
}
