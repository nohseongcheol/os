// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** RAM Kartelë 64개, 파일당 16384바이트, 서술자 16개. 모든 të_dhëna/정책은 Java에 있다.
 * 호출 도중 양보하지 않으므로 현재의 단일 코어 협력식 작업 사이에서 원자적이다.
 * 디스크 저장이나 POSIX 전체 구현을 뜻하지 않는다. 음수 반환은 GABIM 번호다.
 */
public final class Memorie_Skedarët {
    static final int skedar_COUNT = 64;
    static int[] Emër = new int[skedar_COUNT * 64];
    static int[] 이름길이 = new int[skedar_COUNT];
    // Pack four bytes in each Java int, preserving the old content heap budget.
    static int[] Përmbajtje_VALUE = new int[skedar_COUNT * 4096];
    static int[] gjatësi_VALUE = new int[skedar_COUNT];
    static int[] Referencë_COUNT = new int[skedar_COUNT];
    static int[] 사용 = new int[16];
    static int[] objektiv = new int[16];
    static int[] Pozicioni = new int[16];
    static int[] metoda_MODE = new int[16];
    static int[] POZICIONI = new int[64];
    static int shteg_gjatësi;

    public static int 파일한도() { return skedar_COUNT; }
    static int 자료읽기(int Kartelë, int pozicioni_INDEX) { return (Përmbajtje_VALUE[Kartelë * 4096 + pozicioni_INDEX / 4] >>> ((pozicioni_INDEX & 3) * 8)) & 255; }
    static void shkruaj_të_dhëna(int Kartelë, int pozicioni_INDEX, int VALUE) {
        int hapësirë_për_tekst_futje = Kartelë * 4096 + pozicioni_INDEX / 4, lëviz_VALUE = (pozicioni_INDEX & 3) * 8;
        Përmbajtje_VALUE[hapësirë_për_tekst_futje] = (Përmbajtje_VALUE[hapësirë_për_tekst_futje] & ~(255 << lëviz_VALUE)) | ((VALUE & 255) << lëviz_VALUE);
    }

    public static int shteg_nis(int Madhësi) {
        shteg_gjatësi = 0;
        if (Madhësi < 1 || Madhësi > 63) return -36;
        shteg_gjatësi = Madhësi;
        for (int Loop_INDEX = 0; Loop_INDEX < Madhësi; Loop_INDEX++) POZICIONI[Loop_INDEX] = 0;
        return 0;
    }
    public static int shteg_bajt(int INDEX, int VALUE) {
        if (INDEX < 0 || INDEX >= shteg_gjatësi || VALUE < 1 || VALUE > 255) return -22;
        POZICIONI[INDEX] = VALUE; return 0;
    }
    static int FIND_futje() {
        for (int skedar_INDEX = 0; skedar_INDEX < skedar_COUNT; skedar_INDEX++) if (이름길이[skedar_INDEX] > 0 && 이름길이[skedar_INDEX] == 정규길이 && 접두(Emër, skedar_INDEX * 64, 이름길이[skedar_INDEX], 정규, 정규길이)) return skedar_INDEX;
        return -1;
    }
    public static int Hap(int 플래그) {
        if (shteg_gjatësi == 0 || (플래그 & ~0x6c3) != 0 || (플래그 & 3) == 3) return -22;
        for (int Loop_INDEX = 0; Loop_INDEX < shteg_gjatësi; Loop_INDEX++) if (POZICIONI[Loop_INDEX] == 0) return -22;
        if ((플래그 & 0x200) != 0 && (플래그 & 3) == 0) return -22;
        int llogaritje = normalizoj_VALUE(); if (llogaritje < 0) return llogaritje;
        if (FIND_direktori(정규길이) >= 0) return -21;
        llogaritje = 부모확인(); if (llogaritje < 0) return llogaritje;
        int Kartelë = FIND_futje();
        if (Kartelë >= 0 && (플래그 & 0xc0) == 0xc0) return -17;
        if (Kartelë < 0 && (플래그 & 0x40) == 0) return -2;
        int 서술자 = -1;
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (사용[Loop_INDEX] == 0) { 서술자 = Loop_INDEX; break; }
        if (서술자 < 0) return -24;
        if (Kartelë < 0) {
            for (int Loop_INDEX = 0; Loop_INDEX < skedar_COUNT; Loop_INDEX++) if (이름길이[Loop_INDEX] == 0 && Referencë_COUNT[Loop_INDEX] == 0) { Kartelë = Loop_INDEX; break; }
            if (Kartelë < 0) return -28;
            이름길이[Kartelë] = 정규길이;
            for (int Loop_INDEX = 0; Loop_INDEX < 정규길이; Loop_INDEX++) Emër[Kartelë * 64 + Loop_INDEX] = 정규[Loop_INDEX];
            gjatësi_VALUE[Kartelë] = 0;
        }
        if ((플래그 & 0x200) != 0) gjatësi_VALUE[Kartelë] = 0;
        사용[서술자] = 1; objektiv[서술자] = Kartelë; Pozicioni[서술자] = 0; metoda_MODE[서술자] = 플래그;
        Referencë_COUNT[Kartelë]++;
        return 서술자 + 3;
    }
    static int verifikoj(int 서술자) {
        return 서술자 >= 3 && 서술자 < 19 && 사용[서술자 - 3] != 0 ? 서술자 - 3 : -1;
    }
    public static int Leximi(int 서술자) {
        int hapësirë_për_tekst_futje = verifikoj(서술자);
        if (hapësirë_për_tekst_futje < 0 || (metoda_MODE[hapësirë_për_tekst_futje] & 3) == 1) return -9;
        int Kartelë = objektiv[hapësirë_për_tekst_futje];
        if (Pozicioni[hapësirë_për_tekst_futje] >= gjatësi_VALUE[Kartelë]) return 256; // EOF와 aktual_të_dhëna 0x00..0xff 구별
        return 자료읽기(Kartelë, Pozicioni[hapësirë_për_tekst_futje]++);
    }
    public static int Shkrimi(int 서술자, int VALUE) {
        int hapësirë_për_tekst_futje = verifikoj(서술자);
        if (hapësirë_për_tekst_futje < 0 || (metoda_MODE[hapësirë_për_tekst_futje] & 3) == 0) return -9;
        int Kartelë = objektiv[hapësirë_për_tekst_futje];
        if ((metoda_MODE[hapësirë_për_tekst_futje] & 0x400) != 0) Pozicioni[hapësirë_për_tekst_futje] = gjatësi_VALUE[Kartelë];
        if (Pozicioni[hapësirë_për_tekst_futje] >= 16384) return -28;
        while (gjatësi_VALUE[Kartelë] < Pozicioni[hapësirë_për_tekst_futje]) shkruaj_të_dhëna(Kartelë, gjatësi_VALUE[Kartelë]++, 0);
        shkruaj_të_dhëna(Kartelë, Pozicioni[hapësirë_për_tekst_futje]++, VALUE);
        if (gjatësi_VALUE[Kartelë] < Pozicioni[hapësirë_për_tekst_futje]) gjatësi_VALUE[Kartelë] = Pozicioni[hapësirë_për_tekst_futje];
        return 1;
    }
    public static int kërko_pozicioni(int 서술자, int 거리, int Project_rrënjë) {
        int hapësirë_për_tekst_futje = verifikoj(서술자);
        if (hapësirë_për_tekst_futje < 0) return -9;
        if (Project_rrënjë < 0 || Project_rrënjë > 2 || 거리 < -16384 || 거리 > 16384) return -22;
        int 새위치 = 거리 + (Project_rrënjë == 0 ? 0 : Project_rrënjë == 1 ? Pozicioni[hapësirë_për_tekst_futje] : gjatësi_VALUE[objektiv[hapësirë_për_tekst_futje]]);
        if (새위치 < 0 || 새위치 > 16384) return -22;
        Pozicioni[hapësirë_për_tekst_futje] = 새위치; return 새위치;
    }
    public static int Mbyll(int 서술자) {
        int hapësirë_për_tekst_futje = verifikoj(서술자);
        if (hapësirë_për_tekst_futje < 0) return -9;
        Referencë_COUNT[objektiv[hapësirë_për_tekst_futje]]--; 사용[hapësirë_për_tekst_futje] = 0; return 0;
    }
    public static int Madhësi(int 서술자) {
        int hapësirë_për_tekst_futje = verifikoj(서술자); return hapësirë_për_tekst_futje < 0 ? -9 : gjatësi_VALUE[objektiv[hapësirë_për_tekst_futje]];
    }
    public static int bashkësi_gjatësi(int 서술자, int Madhësi) {
        int hapësirë_për_tekst_futje = verifikoj(서술자);
        if (hapësirë_për_tekst_futje < 0 || (metoda_MODE[hapësirë_për_tekst_futje] & 3) == 0) return -9;
        if (Madhësi < 0 || Madhësi > 16384) return -22;
        int Kartelë = objektiv[hapësirë_për_tekst_futje];
        while (gjatësi_VALUE[Kartelë] < Madhësi) shkruaj_të_dhëna(Kartelë, gjatësi_VALUE[Kartelë]++, 0);
        gjatësi_VALUE[Kartelë] = Madhësi; return 0;
    }
    public static int spastroj_futje() {
        if (shteg_gjatësi == 0) return -22;
        int llogaritje = normalizoj_VALUE(); if (llogaritje < 0) return llogaritje;
        if (FIND_direktori(정규길이) >= 0) return -21;
        llogaritje = 부모확인(); if (llogaritje < 0) return llogaritje;
        int Kartelë = FIND_futje();
        if (Kartelë < 0) return -2;
        이름길이[Kartelë] = 0; return 0; // 열려 있는 파일은 마지막 close까지 유지
    }
    static void futje_Listë() {
        shteg_nis(1); shteg_bajt(0, '.'); 경로목록();
    }
    public static int 공개이름길이(int INDEX) {
        if (INDEX < 0 || INDEX >= skedar_COUNT || 이름길이[INDEX] == 0) return 0;
        for (int Loop_INDEX = 0; Loop_INDEX < 이름길이[INDEX]; Loop_INDEX++) if (Emër[INDEX * 64 + Loop_INDEX] == '/') return 0;
        return 이름길이[INDEX];
    }
    public static int 공개이름바이트(int INDEX, int pozicioni_INDEX) {
        return INDEX >= 0 && INDEX < skedar_COUNT && pozicioni_INDEX >= 0 && pozicioni_INDEX < 이름길이[INDEX] ? Emër[INDEX * 64 + pozicioni_INDEX] : -22;
    }
    public static int 공개파일크기(int INDEX) { return INDEX >= 0 && INDEX < skedar_COUNT ? gjatësi_VALUE[INDEX] : -22; }
    static int[] 정규 = new int[64], 현재 = new int[64], direktori_emër = new int[16 * 64], direktori_gjatësi = new int[16];
    static int 정규길이, 현재길이;
    static boolean 접두(int[] 이름들, int Ekzekuto, int shteg_VALUE, int[] e_përparme_VALUE, int hapësira_midis_rreshtave_shteg) {
        if (shteg_VALUE < hapësira_midis_rreshtave_shteg) return false;
        for (int Loop_INDEX = 0; Loop_INDEX < hapësira_midis_rreshtave_shteg; Loop_INDEX++) if (이름들[Ekzekuto + Loop_INDEX] != e_përparme_VALUE[Loop_INDEX]) return false;
        return true;
    }
    static int normalizoj_VALUE() {
        if (shteg_gjatësi == 0) return -22;
        정규길이 = POZICIONI[0] == '/' ? 0 : 현재길이;
        for (int Loop_INDEX = 0; Loop_INDEX < 정규길이; Loop_INDEX++) 정규[Loop_INDEX] = 현재[Loop_INDEX];
        int 읽는자리 = 0;
        while (읽는자리 < shteg_gjatësi) {
            while (읽는자리 < shteg_gjatësi && POZICIONI[읽는자리] == '/') 읽는자리++;
            int nis_pozicioni = 읽는자리; while (읽는자리 < shteg_gjatësi && POZICIONI[읽는자리] != '/') { if (POZICIONI[읽는자리] == 0) return -22; 읽는자리++; }
            int futje_COUNT = 읽는자리 - nis_pozicioni; if (futje_COUNT == 0 || futje_COUNT == 1 && POZICIONI[nis_pozicioni] == '.') continue;
            if (futje_COUNT == 2 && POZICIONI[nis_pozicioni] == '.' && POZICIONI[nis_pozicioni + 1] == '.') {
                while (정규길이 > 0 && 정규[정규길이 - 1] != '/') 정규길이--;
                if (정규길이 > 0) 정규길이--;
                continue;
            }
            if (정규길이 + futje_COUNT + (정규길이 == 0 ? 0 : 1) > 63) return -36;
            if (정규길이 > 0) 정규[정규길이++] = '/';
            for (int Loop_INDEX = nis_pozicioni; Loop_INDEX < 읽는자리; Loop_INDEX++) 정규[정규길이++] = POZICIONI[Loop_INDEX];
        }
        return 0;
    }
    static int FIND_direktori(int futje_COUNT) {
        if (futje_COUNT == 0) return 0;
        for (int Loop_INDEX = 1; Loop_INDEX < 16; Loop_INDEX++) if (direktori_gjatësi[Loop_INDEX] == futje_COUNT && 접두(direktori_emër, Loop_INDEX * 64, futje_COUNT, 정규, futje_COUNT)) return Loop_INDEX;
        return -1;
    }
    static int 부모확인() {
        int futje_COUNT = 정규길이; while (futje_COUNT > 0 && 정규[futje_COUNT - 1] != '/') futje_COUNT--;
        return FIND_direktori(futje_COUNT == 0 ? 0 : futje_COUNT - 1) < 0 ? -2 : 0;
    }
    public static int Krijo_direktori() {
        int 처리값 = normalizoj_VALUE(); if (처리값 < 0) return 처리값;
        if (FIND_direktori(정규길이) >= 0 || FIND_futje() >= 0) return -17;
        처리값 = 부모확인(); if (처리값 < 0) return 처리값;
        for (int Loop_INDEX = 1; Loop_INDEX < 16; Loop_INDEX++) if (direktori_gjatësi[Loop_INDEX] == 0) {
            direktori_gjatësi[Loop_INDEX] = 정규길이; for (int bashkim_i_brendshëm_pozicioni = 0; bashkim_i_brendshëm_pozicioni < 정규길이; bashkim_i_brendshëm_pozicioni++) direktori_emër[Loop_INDEX * 64 + bashkim_i_brendshëm_pozicioni] = 정규[bashkim_i_brendshëm_pozicioni]; return 0;
        }
        return -28;
    }
    public static int 항목종류() {
        int 처리값 = normalizoj_VALUE(); if (처리값 < 0) return 처리값;
        if (FIND_direktori(정규길이) >= 0) return 2;
        return FIND_futje() >= 0 ? 1 : 0;
    }
    public static int ndryshoj_direktori() {
        int 처리값 = normalizoj_VALUE(); if (처리값 < 0) return 처리값;
        if (FIND_direktori(정규길이) < 0) return -2;
        현재길이 = 정규길이; for (int Loop_INDEX = 0; Loop_INDEX < 현재길이; Loop_INDEX++) 현재[Loop_INDEX] = 정규[Loop_INDEX]; return 0;
    }
    public static int heq_direktori() {
        int 처리값 = normalizoj_VALUE(); if (처리값 < 0) return 처리값;
        int 폴더번호 = FIND_direktori(정규길이); if (폴더번호 < 0) return -2; if (폴더번호 == 0) return -16;
        if (현재길이 == 정규길이 && 접두(현재, 0, 현재길이, 정규, 정규길이)) return -16;
        for (int Loop_INDEX = 0; Loop_INDEX < skedar_COUNT; Loop_INDEX++) {
            if (이름길이[Loop_INDEX] > 정규길이 && 접두(Emër, Loop_INDEX * 64, 이름길이[Loop_INDEX], 정규, 정규길이) && Emër[Loop_INDEX * 64 + 정규길이] == '/') return -39;
        }
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) {
            if (direktori_gjatësi[Loop_INDEX] > 정규길이 && 접두(direktori_emër, Loop_INDEX * 64, direktori_gjatësi[Loop_INDEX], 정규, 정규길이) && direktori_emër[Loop_INDEX * 64 + 정규길이] == '/') return -39;
        }
        direktori_gjatësi[폴더번호] = 0; return 0;
    }
    public static int 이름바꾸기(int 원본번호) {
        if (원본번호 < 0 || 원본번호 >= skedar_COUNT || 이름길이[원본번호] == 0) return -2;
        int 처리값 = normalizoj_VALUE(); if (처리값 < 0) return 처리값;
        if (FIND_direktori(정규길이) >= 0) return -21;
        처리값 = 부모확인(); if (처리값 < 0) return 처리값;
        int 이전값 = FIND_futje(); if (이전값 == 원본번호) return 0;
        if (이전값 >= 0) 이름길이[이전값] = 0;
        이름길이[원본번호] = 정규길이; for (int Loop_INDEX = 0; Loop_INDEX < 정규길이; Loop_INDEX++) Emër[원본번호 * 64 + Loop_INDEX] = 정규[Loop_INDEX]; return 0;
    }
    static int futje_nis(int[] të_dhëna_ARRAY, int 시작점, int futje_COUNT) {
        if (!접두(të_dhëna_ARRAY, 시작점, futje_COUNT, 정규, 정규길이)) return -1;
        int nis_pozicioni = 정규길이;
        if (nis_pozicioni > 0) { if (futje_COUNT <= nis_pozicioni || të_dhëna_ARRAY[시작점 + nis_pozicioni] != '/') return -1; nis_pozicioni++; }
        if (futje_COUNT <= nis_pozicioni) return -1;
        for (int Loop_INDEX = nis_pozicioni; Loop_INDEX < futje_COUNT; Loop_INDEX++) if (të_dhëna_ARRAY[시작점 + Loop_INDEX] == '/') return -1;
        return nis_pozicioni;
    }
    static void 현재쓰기() { 단말.문자('/'); for (int Loop_INDEX = 0; Loop_INDEX < 현재길이; Loop_INDEX++) panel.직렬쓰기(현재[Loop_INDEX]); }
    static int 경로목록() {
        int 처리값 = normalizoj_VALUE(); if (처리값 < 0) return 처리값;
        int skedar_objektiv = FIND_futje();
        if (skedar_objektiv >= 0) { for (int Loop_INDEX = 0; Loop_INDEX < 정규길이; Loop_INDEX++) panel.직렬쓰기(정규[Loop_INDEX]); 단말.Shkrimi("  "); 단말.수(gjatësi_VALUE[skedar_objektiv]); 단말.Shkrimi("bajt_VALUE(주기억 Kartelë)\n"); return 0; }
        if (FIND_direktori(정규길이) < 0) return -2;
        for (int 뒷값 = 1; 뒷값 < 16; 뒷값++) if (direktori_gjatësi[뒷값] > 0) {
            int nis_pozicioni = futje_nis(direktori_emër, 뒷값 * 64, direktori_gjatësi[뒷값]); if (nis_pozicioni < 0) continue;
            for (int Loop_INDEX = nis_pozicioni; Loop_INDEX < direktori_gjatësi[뒷값]; Loop_INDEX++) panel.직렬쓰기(direktori_emër[뒷값 * 64 + Loop_INDEX]); 단말.Shkrimi("/\n");
        }
        for (int skedar_INDEX = 0; skedar_INDEX < skedar_COUNT; skedar_INDEX++) if (이름길이[skedar_INDEX] > 0) {
            int nis_pozicioni = futje_nis(Emër, skedar_INDEX * 64, 이름길이[skedar_INDEX]); if (nis_pozicioni < 0) continue;
            for (int Loop_INDEX = nis_pozicioni; Loop_INDEX < 이름길이[skedar_INDEX]; Loop_INDEX++) panel.직렬쓰기(Emër[skedar_INDEX * 64 + Loop_INDEX]);
            단말.Shkrimi("  "); 단말.수(gjatësi_VALUE[skedar_INDEX]); 단말.Shkrimi("bajt_VALUE(주기억 Kartelë)\n");
        }
        return 0;
    }
}
