// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** RAM Ffeil 64개, 파일당 16384바이트, 서술자 16개. 모든 data/정책은 Java에 있다.
 * 호출 도중 양보하지 않으므로 현재의 단일 코어 협력식 작업 사이에서 원자적이다.
 * 디스크 저장이나 POSIX 전체 구현을 뜻하지 않는다. 음수 반환은 Gwall 번호다.
 */
public final class Cof_Ffeil {
    static final int ffeil_COUNT = 64;
    static int[] Enw = new int[ffeil_COUNT * 64];
    static int[] 이름길이 = new int[ffeil_COUNT];
    // Pack four bytes in each Java int, preserving the old content heap budget.
    static int[] Cynnwys_VALUE = new int[ffeil_COUNT * 4096];
    static int[] hyd_VALUE = new int[ffeil_COUNT];
    static int[] cyfeiriad_COUNT = new int[ffeil_COUNT];
    static int[] 사용 = new int[16];
    static int[] targed = new int[16];
    static int[] safle = new int[16];
    static int[] dull_MODE = new int[16];
    static int[] LLWYBR = new int[64];
    static int llwybr_hyd;

    public static int 파일한도() { return ffeil_COUNT; }
    static int 자료읽기(int Ffeil, int safle_INDEX) { return (Cynnwys_VALUE[Ffeil * 4096 + safle_INDEX / 4] >>> ((safle_INDEX & 3) * 8)) & 255; }
    static void ysgrifennu_data(int Ffeil, int safle_INDEX, int VALUE) {
        int slot_cofnod = Ffeil * 4096 + safle_INDEX / 4, symud_VALUE = (safle_INDEX & 3) * 8;
        Cynnwys_VALUE[slot_cofnod] = (Cynnwys_VALUE[slot_cofnod] & ~(255 << symud_VALUE)) | ((VALUE & 255) << symud_VALUE);
    }

    public static int llwybr_START(int Maint) {
        llwybr_hyd = 0;
        if (Maint < 1 || Maint > 63) return -36;
        llwybr_hyd = Maint;
        for (int Loop_INDEX = 0; Loop_INDEX < Maint; Loop_INDEX++) LLWYBR[Loop_INDEX] = 0;
        return 0;
    }
    public static int llwybr_beit(int INDEX, int VALUE) {
        if (INDEX < 0 || INDEX >= llwybr_hyd || VALUE < 1 || VALUE > 255) return -22;
        LLWYBR[INDEX] = VALUE; return 0;
    }
    static int FIND_cofnod() {
        for (int ffeil_INDEX = 0; ffeil_INDEX < ffeil_COUNT; ffeil_INDEX++) if (이름길이[ffeil_INDEX] > 0 && 이름길이[ffeil_INDEX] == 정규길이 && 접두(Enw, ffeil_INDEX * 64, 이름길이[ffeil_INDEX], 정규, 정규길이)) return ffeil_INDEX;
        return -1;
    }
    public static int Agor(int 플래그) {
        if (llwybr_hyd == 0 || (플래그 & ~0x6c3) != 0 || (플래그 & 3) == 3) return -22;
        for (int Loop_INDEX = 0; Loop_INDEX < llwybr_hyd; Loop_INDEX++) if (LLWYBR[Loop_INDEX] == 0) return -22;
        if ((플래그 & 0x200) != 0 && (플래그 & 3) == 0) return -22;
        int mesur = normaleiddio_VALUE(); if (mesur < 0) return mesur;
        if (FIND_cyfeiriadur(정규길이) >= 0) return -21;
        mesur = 부모확인(); if (mesur < 0) return mesur;
        int Ffeil = FIND_cofnod();
        if (Ffeil >= 0 && (플래그 & 0xc0) == 0xc0) return -17;
        if (Ffeil < 0 && (플래그 & 0x40) == 0) return -2;
        int 서술자 = -1;
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (사용[Loop_INDEX] == 0) { 서술자 = Loop_INDEX; break; }
        if (서술자 < 0) return -24;
        if (Ffeil < 0) {
            for (int Loop_INDEX = 0; Loop_INDEX < ffeil_COUNT; Loop_INDEX++) if (이름길이[Loop_INDEX] == 0 && cyfeiriad_COUNT[Loop_INDEX] == 0) { Ffeil = Loop_INDEX; break; }
            if (Ffeil < 0) return -28;
            이름길이[Ffeil] = 정규길이;
            for (int Loop_INDEX = 0; Loop_INDEX < 정규길이; Loop_INDEX++) Enw[Ffeil * 64 + Loop_INDEX] = 정규[Loop_INDEX];
            hyd_VALUE[Ffeil] = 0;
        }
        if ((플래그 & 0x200) != 0) hyd_VALUE[Ffeil] = 0;
        사용[서술자] = 1; targed[서술자] = Ffeil; safle[서술자] = 0; dull_MODE[서술자] = 플래그;
        cyfeiriad_COUNT[Ffeil]++;
        return 서술자 + 3;
    }
    static int dilysu(int 서술자) {
        return 서술자 >= 3 && 서술자 < 19 && 사용[서술자 - 3] != 0 ? 서술자 - 3 : -1;
    }
    public static int Darllen(int 서술자) {
        int slot_cofnod = dilysu(서술자);
        if (slot_cofnod < 0 || (dull_MODE[slot_cofnod] & 3) == 1) return -9;
        int Ffeil = targed[slot_cofnod];
        if (safle[slot_cofnod] >= hyd_VALUE[Ffeil]) return 256; // EOF와 go_iawn_data 0x00..0xff 구별
        return 자료읽기(Ffeil, safle[slot_cofnod]++);
    }
    public static int Ysgrifennu(int 서술자, int VALUE) {
        int slot_cofnod = dilysu(서술자);
        if (slot_cofnod < 0 || (dull_MODE[slot_cofnod] & 3) == 0) return -9;
        int Ffeil = targed[slot_cofnod];
        if ((dull_MODE[slot_cofnod] & 0x400) != 0) safle[slot_cofnod] = hyd_VALUE[Ffeil];
        if (safle[slot_cofnod] >= 16384) return -28;
        while (hyd_VALUE[Ffeil] < safle[slot_cofnod]) ysgrifennu_data(Ffeil, hyd_VALUE[Ffeil]++, 0);
        ysgrifennu_data(Ffeil, safle[slot_cofnod]++, VALUE);
        if (hyd_VALUE[Ffeil] < safle[slot_cofnod]) hyd_VALUE[Ffeil] = safle[slot_cofnod];
        return 1;
    }
    public static int chwilio_safle(int 서술자, int 거리, int prosiect_gwraidd) {
        int slot_cofnod = dilysu(서술자);
        if (slot_cofnod < 0) return -9;
        if (prosiect_gwraidd < 0 || prosiect_gwraidd > 2 || 거리 < -16384 || 거리 > 16384) return -22;
        int 새위치 = 거리 + (prosiect_gwraidd == 0 ? 0 : prosiect_gwraidd == 1 ? safle[slot_cofnod] : hyd_VALUE[targed[slot_cofnod]]);
        if (새위치 < 0 || 새위치 > 16384) return -22;
        safle[slot_cofnod] = 새위치; return 새위치;
    }
    public static int Cau(int 서술자) {
        int slot_cofnod = dilysu(서술자);
        if (slot_cofnod < 0) return -9;
        cyfeiriad_COUNT[targed[slot_cofnod]]--; 사용[slot_cofnod] = 0; return 0;
    }
    public static int Maint(int 서술자) {
        int slot_cofnod = dilysu(서술자); return slot_cofnod < 0 ? -9 : hyd_VALUE[targed[slot_cofnod]];
    }
    public static int set_hyd(int 서술자, int Maint) {
        int slot_cofnod = dilysu(서술자);
        if (slot_cofnod < 0 || (dull_MODE[slot_cofnod] & 3) == 0) return -9;
        if (Maint < 0 || Maint > 16384) return -22;
        int Ffeil = targed[slot_cofnod];
        while (hyd_VALUE[Ffeil] < Maint) ysgrifennu_data(Ffeil, hyd_VALUE[Ffeil]++, 0);
        hyd_VALUE[Ffeil] = Maint; return 0;
    }
    public static int 지우기() {
        if (llwybr_hyd == 0) return -22;
        int mesur = normaleiddio_VALUE(); if (mesur < 0) return mesur;
        if (FIND_cyfeiriadur(정규길이) >= 0) return -21;
        mesur = 부모확인(); if (mesur < 0) return mesur;
        int Ffeil = FIND_cofnod();
        if (Ffeil < 0) return -2;
        이름길이[Ffeil] = 0; return 0; // 열려 있는 파일은 마지막 close까지 유지
    }
    static void cofnod_Rhestr() {
        llwybr_START(1); llwybr_beit(0, '.'); 경로목록();
    }
    public static int 공개이름길이(int INDEX) {
        if (INDEX < 0 || INDEX >= ffeil_COUNT || 이름길이[INDEX] == 0) return 0;
        for (int Loop_INDEX = 0; Loop_INDEX < 이름길이[INDEX]; Loop_INDEX++) if (Enw[INDEX * 64 + Loop_INDEX] == '/') return 0;
        return 이름길이[INDEX];
    }
    public static int 공개이름바이트(int INDEX, int safle_INDEX) {
        return INDEX >= 0 && INDEX < ffeil_COUNT && safle_INDEX >= 0 && safle_INDEX < 이름길이[INDEX] ? Enw[INDEX * 64 + safle_INDEX] : -22;
    }
    public static int 공개파일크기(int INDEX) { return INDEX >= 0 && INDEX < ffeil_COUNT ? hyd_VALUE[INDEX] : -22; }
    static int[] 정규 = new int[64], 현재 = new int[64], cyfeiriadur_enw = new int[16 * 64], cyfeiriadur_hyd = new int[16];
    static int 정규길이, 현재길이;
    static boolean 접두(int[] 이름들, int Gweithredu_2, int llwybr_VALUE, int[] 앞, int rhynglinellu_llwybr) {
        if (llwybr_VALUE < rhynglinellu_llwybr) return false;
        for (int Loop_INDEX = 0; Loop_INDEX < rhynglinellu_llwybr; Loop_INDEX++) if (이름들[Gweithredu_2 + Loop_INDEX] != 앞[Loop_INDEX]) return false;
        return true;
    }
    static int normaleiddio_VALUE() {
        if (llwybr_hyd == 0) return -22;
        정규길이 = LLWYBR[0] == '/' ? 0 : 현재길이;
        for (int Loop_INDEX = 0; Loop_INDEX < 정규길이; Loop_INDEX++) 정규[Loop_INDEX] = 현재[Loop_INDEX];
        int 읽는자리 = 0;
        while (읽는자리 < llwybr_hyd) {
            while (읽는자리 < llwybr_hyd && LLWYBR[읽는자리] == '/') 읽는자리++;
            int START_safle = 읽는자리; while (읽는자리 < llwybr_hyd && LLWYBR[읽는자리] != '/') { if (LLWYBR[읽는자리] == 0) return -22; 읽는자리++; }
            int cofnod_COUNT = 읽는자리 - START_safle; if (cofnod_COUNT == 0 || cofnod_COUNT == 1 && LLWYBR[START_safle] == '.') continue;
            if (cofnod_COUNT == 2 && LLWYBR[START_safle] == '.' && LLWYBR[START_safle + 1] == '.') {
                while (정규길이 > 0 && 정규[정규길이 - 1] != '/') 정규길이--;
                if (정규길이 > 0) 정규길이--;
                continue;
            }
            if (정규길이 + cofnod_COUNT + (정규길이 == 0 ? 0 : 1) > 63) return -36;
            if (정규길이 > 0) 정규[정규길이++] = '/';
            for (int Loop_INDEX = START_safle; Loop_INDEX < 읽는자리; Loop_INDEX++) 정규[정규길이++] = LLWYBR[Loop_INDEX];
        }
        return 0;
    }
    static int FIND_cyfeiriadur(int cofnod_COUNT) {
        if (cofnod_COUNT == 0) return 0;
        for (int Loop_INDEX = 1; Loop_INDEX < 16; Loop_INDEX++) if (cyfeiriadur_hyd[Loop_INDEX] == cofnod_COUNT && 접두(cyfeiriadur_enw, Loop_INDEX * 64, cofnod_COUNT, 정규, cofnod_COUNT)) return Loop_INDEX;
        return -1;
    }
    static int 부모확인() {
        int cofnod_COUNT = 정규길이; while (cofnod_COUNT > 0 && 정규[cofnod_COUNT - 1] != '/') cofnod_COUNT--;
        return FIND_cyfeiriadur(cofnod_COUNT == 0 ? 0 : cofnod_COUNT - 1) < 0 ? -2 : 0;
    }
    public static int Creu_cyfeiriadur() {
        int 처리값 = normaleiddio_VALUE(); if (처리값 < 0) return 처리값;
        if (FIND_cyfeiriadur(정규길이) >= 0 || FIND_cofnod() >= 0) return -17;
        처리값 = 부모확인(); if (처리값 < 0) return 처리값;
        for (int Loop_INDEX = 1; Loop_INDEX < 16; Loop_INDEX++) if (cyfeiriadur_hyd[Loop_INDEX] == 0) {
            cyfeiriadur_hyd[Loop_INDEX] = 정규길이; for (int uno_mewnol_safle = 0; uno_mewnol_safle < 정규길이; uno_mewnol_safle++) cyfeiriadur_enw[Loop_INDEX * 64 + uno_mewnol_safle] = 정규[uno_mewnol_safle]; return 0;
        }
        return -28;
    }
    public static int 항목종류() {
        int 처리값 = normaleiddio_VALUE(); if (처리값 < 0) return 처리값;
        if (FIND_cyfeiriadur(정규길이) >= 0) return 2;
        return FIND_cofnod() >= 0 ? 1 : 0;
    }
    public static int newid_cyfeiriadur() {
        int 처리값 = normaleiddio_VALUE(); if (처리값 < 0) return 처리값;
        if (FIND_cyfeiriadur(정규길이) < 0) return -2;
        현재길이 = 정규길이; for (int Loop_INDEX = 0; Loop_INDEX < 현재길이; Loop_INDEX++) 현재[Loop_INDEX] = 정규[Loop_INDEX]; return 0;
    }
    public static int tynnu_cyfeiriadur() {
        int 처리값 = normaleiddio_VALUE(); if (처리값 < 0) return 처리값;
        int 폴더번호 = FIND_cyfeiriadur(정규길이); if (폴더번호 < 0) return -2; if (폴더번호 == 0) return -16;
        if (현재길이 == 정규길이 && 접두(현재, 0, 현재길이, 정규, 정규길이)) return -16;
        for (int Loop_INDEX = 0; Loop_INDEX < ffeil_COUNT; Loop_INDEX++) {
            if (이름길이[Loop_INDEX] > 정규길이 && 접두(Enw, Loop_INDEX * 64, 이름길이[Loop_INDEX], 정규, 정규길이) && Enw[Loop_INDEX * 64 + 정규길이] == '/') return -39;
        }
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) {
            if (cyfeiriadur_hyd[Loop_INDEX] > 정규길이 && 접두(cyfeiriadur_enw, Loop_INDEX * 64, cyfeiriadur_hyd[Loop_INDEX], 정규, 정규길이) && cyfeiriadur_enw[Loop_INDEX * 64 + 정규길이] == '/') return -39;
        }
        cyfeiriadur_hyd[폴더번호] = 0; return 0;
    }
    public static int 이름바꾸기(int 원본번호) {
        if (원본번호 < 0 || 원본번호 >= ffeil_COUNT || 이름길이[원본번호] == 0) return -2;
        int 처리값 = normaleiddio_VALUE(); if (처리값 < 0) return 처리값;
        if (FIND_cyfeiriadur(정규길이) >= 0) return -21;
        처리값 = 부모확인(); if (처리값 < 0) return 처리값;
        int 이전값 = FIND_cofnod(); if (이전값 == 원본번호) return 0;
        if (이전값 >= 0) 이름길이[이전값] = 0;
        이름길이[원본번호] = 정규길이; for (int Loop_INDEX = 0; Loop_INDEX < 정규길이; Loop_INDEX++) Enw[원본번호 * 64 + Loop_INDEX] = 정규[Loop_INDEX]; return 0;
    }
    static int cofnod_START(int[] data_ARAE, int 시작점, int cofnod_COUNT) {
        if (!접두(data_ARAE, 시작점, cofnod_COUNT, 정규, 정규길이)) return -1;
        int START_safle = 정규길이;
        if (START_safle > 0) { if (cofnod_COUNT <= START_safle || data_ARAE[시작점 + START_safle] != '/') return -1; START_safle++; }
        if (cofnod_COUNT <= START_safle) return -1;
        for (int Loop_INDEX = START_safle; Loop_INDEX < cofnod_COUNT; Loop_INDEX++) if (data_ARAE[시작점 + Loop_INDEX] == '/') return -1;
        return START_safle;
    }
    static void 현재쓰기() { 단말.문자('/'); for (int Loop_INDEX = 0; Loop_INDEX < 현재길이; Loop_INDEX++) bwrdd.직렬쓰기(현재[Loop_INDEX]); }
    static int 경로목록() {
        int 처리값 = normaleiddio_VALUE(); if (처리값 < 0) return 처리값;
        int ffeil_targed = FIND_cofnod();
        if (ffeil_targed >= 0) { for (int Loop_INDEX = 0; Loop_INDEX < 정규길이; Loop_INDEX++) bwrdd.직렬쓰기(정규[Loop_INDEX]); 단말.Ysgrifennu("  "); 단말.수(hyd_VALUE[ffeil_targed]); 단말.Ysgrifennu("beit_VALUE(주기억 Ffeil)\n"); return 0; }
        if (FIND_cyfeiriadur(정규길이) < 0) return -2;
        for (int 뒷값 = 1; 뒷값 < 16; 뒷값++) if (cyfeiriadur_hyd[뒷값] > 0) {
            int START_safle = cofnod_START(cyfeiriadur_enw, 뒷값 * 64, cyfeiriadur_hyd[뒷값]); if (START_safle < 0) continue;
            for (int Loop_INDEX = START_safle; Loop_INDEX < cyfeiriadur_hyd[뒷값]; Loop_INDEX++) bwrdd.직렬쓰기(cyfeiriadur_enw[뒷값 * 64 + Loop_INDEX]); 단말.Ysgrifennu("/\n");
        }
        for (int ffeil_INDEX = 0; ffeil_INDEX < ffeil_COUNT; ffeil_INDEX++) if (이름길이[ffeil_INDEX] > 0) {
            int START_safle = cofnod_START(Enw, ffeil_INDEX * 64, 이름길이[ffeil_INDEX]); if (START_safle < 0) continue;
            for (int Loop_INDEX = START_safle; Loop_INDEX < 이름길이[ffeil_INDEX]; Loop_INDEX++) bwrdd.직렬쓰기(Enw[ffeil_INDEX * 64 + Loop_INDEX]);
            단말.Ysgrifennu("  "); 단말.수(hyd_VALUE[ffeil_INDEX]); 단말.Ysgrifennu("beit_VALUE(주기억 Ffeil)\n");
        }
        return 0;
    }
}
