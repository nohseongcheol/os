// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** RAM faidhle 64개, 파일당 16384바이트, 서술자 16개. 모든 dàta/정책은 Java에 있다.
 * 호출 도중 양보하지 않으므로 현재의 단일 코어 협력식 작업 사이에서 원자적이다.
 * 디스크 저장이나 POSIX 전체 구현을 뜻하지 않는다. 음수 반환은 Mearachd 번호다.
 */
public final class cuimhne_faidhlichean {
    static final int faidhle_COUNT = 64;
    static int[] Ainm = new int[faidhle_COUNT * 64];
    static int[] 이름길이 = new int[faidhle_COUNT];
    // Pack four bytes in each Java int, preserving the old content heap budget.
    static int[] susbaint_VALUE = new int[faidhle_COUNT * 4096];
    static int[] faid_VALUE = new int[faidhle_COUNT];
    static int[] fiosrachadh_COUNT = new int[faidhle_COUNT];
    static int[] 사용 = new int[16];
    static int[] targaid = new int[16];
    static int[] suidhich = new int[16];
    static int[] dòigh_MODE = new int[16];
    static int[] Slighe = new int[64];
    static int slighe_faid;

    public static int 파일한도() { return faidhle_COUNT; }
    static int 자료읽기(int faidhle, int suidhich_INDEX) { return (susbaint_VALUE[faidhle * 4096 + suidhich_INDEX / 4] >>> ((suidhich_INDEX & 3) * 8)) & 255; }
    static void sgrìobh_dàta(int faidhle, int suidhich_INDEX, int VALUE) {
        int slot_cur_a_steach = faidhle * 4096 + suidhich_INDEX / 4, gluais_VALUE = (suidhich_INDEX & 3) * 8;
        susbaint_VALUE[slot_cur_a_steach] = (susbaint_VALUE[slot_cur_a_steach] & ~(255 << gluais_VALUE)) | ((VALUE & 255) << gluais_VALUE);
    }

    public static int slighe_Start(int atharraich_am_meud) {
        slighe_faid = 0;
        if (atharraich_am_meud < 1 || atharraich_am_meud > 63) return -36;
        slighe_faid = atharraich_am_meud;
        for (int lùb_INDEX = 0; lùb_INDEX < atharraich_am_meud; lùb_INDEX++) Slighe[lùb_INDEX] = 0;
        return 0;
    }
    public static int slighe_baidht(int INDEX, int VALUE) {
        if (INDEX < 0 || INDEX >= slighe_faid || VALUE < 1 || VALUE > 255) return -22;
        Slighe[INDEX] = VALUE; return 0;
    }
    static int FIND_cur_a_steach() {
        for (int faidhle_INDEX = 0; faidhle_INDEX < faidhle_COUNT; faidhle_INDEX++) if (이름길이[faidhle_INDEX] > 0 && 이름길이[faidhle_INDEX] == 정규길이 && 접두(Ainm, faidhle_INDEX * 64, 이름길이[faidhle_INDEX], 정규, 정규길이)) return faidhle_INDEX;
        return -1;
    }
    public static int fosgail(int 플래그) {
        if (slighe_faid == 0 || (플래그 & ~0x6c3) != 0 || (플래그 & 3) == 3) return -22;
        for (int lùb_INDEX = 0; lùb_INDEX < slighe_faid; lùb_INDEX++) if (Slighe[lùb_INDEX] == 0) return -22;
        if ((플래그 & 0x200) != 0 && (플래그 & 3) == 0) return -22;
        int tomhas = àbhaistich_VALUE(); if (tomhas < 0) return tomhas;
        if (FIND_eòlaire(정규길이) >= 0) return -21;
        tomhas = 부모확인(); if (tomhas < 0) return tomhas;
        int faidhle = FIND_cur_a_steach();
        if (faidhle >= 0 && (플래그 & 0xc0) == 0xc0) return -17;
        if (faidhle < 0 && (플래그 & 0x40) == 0) return -2;
        int 서술자 = -1;
        for (int lùb_INDEX = 0; lùb_INDEX < 16; lùb_INDEX++) if (사용[lùb_INDEX] == 0) { 서술자 = lùb_INDEX; break; }
        if (서술자 < 0) return -24;
        if (faidhle < 0) {
            for (int lùb_INDEX = 0; lùb_INDEX < faidhle_COUNT; lùb_INDEX++) if (이름길이[lùb_INDEX] == 0 && fiosrachadh_COUNT[lùb_INDEX] == 0) { faidhle = lùb_INDEX; break; }
            if (faidhle < 0) return -28;
            이름길이[faidhle] = 정규길이;
            for (int lùb_INDEX = 0; lùb_INDEX < 정규길이; lùb_INDEX++) Ainm[faidhle * 64 + lùb_INDEX] = 정규[lùb_INDEX];
            faid_VALUE[faidhle] = 0;
        }
        if ((플래그 & 0x200) != 0) faid_VALUE[faidhle] = 0;
        사용[서술자] = 1; targaid[서술자] = faidhle; suidhich[서술자] = 0; dòigh_MODE[서술자] = 플래그;
        fiosrachadh_COUNT[faidhle]++;
        return 서술자 + 3;
    }
    static int dearbh(int 서술자) {
        return 서술자 >= 3 && 서술자 < 19 && 사용[서술자 - 3] != 0 ? 서술자 - 3 : -1;
    }
    public static int 읽기(int 서술자) {
        int slot_cur_a_steach = dearbh(서술자);
        if (slot_cur_a_steach < 0 || (dòigh_MODE[slot_cur_a_steach] & 3) == 1) return -9;
        int faidhle = targaid[slot_cur_a_steach];
        if (suidhich[slot_cur_a_steach] >= faid_VALUE[faidhle]) return 256; // EOF와 dearbh_dàta 0x00..0xff 구별
        return 자료읽기(faidhle, suidhich[slot_cur_a_steach]++);
    }
    public static int sgrìobh(int 서술자, int VALUE) {
        int slot_cur_a_steach = dearbh(서술자);
        if (slot_cur_a_steach < 0 || (dòigh_MODE[slot_cur_a_steach] & 3) == 0) return -9;
        int faidhle = targaid[slot_cur_a_steach];
        if ((dòigh_MODE[slot_cur_a_steach] & 0x400) != 0) suidhich[slot_cur_a_steach] = faid_VALUE[faidhle];
        if (suidhich[slot_cur_a_steach] >= 16384) return -28;
        while (faid_VALUE[faidhle] < suidhich[slot_cur_a_steach]) sgrìobh_dàta(faidhle, faid_VALUE[faidhle]++, 0);
        sgrìobh_dàta(faidhle, suidhich[slot_cur_a_steach]++, VALUE);
        if (faid_VALUE[faidhle] < suidhich[slot_cur_a_steach]) faid_VALUE[faidhle] = suidhich[slot_cur_a_steach];
        return 1;
    }
    public static int sir_suidhich(int 서술자, int 거리, int tilg_freumh) {
        int slot_cur_a_steach = dearbh(서술자);
        if (slot_cur_a_steach < 0) return -9;
        if (tilg_freumh < 0 || tilg_freumh > 2 || 거리 < -16384 || 거리 > 16384) return -22;
        int 새위치 = 거리 + (tilg_freumh == 0 ? 0 : tilg_freumh == 1 ? suidhich[slot_cur_a_steach] : faid_VALUE[targaid[slot_cur_a_steach]]);
        if (새위치 < 0 || 새위치 > 16384) return -22;
        suidhich[slot_cur_a_steach] = 새위치; return 새위치;
    }
    public static int dùin(int 서술자) {
        int slot_cur_a_steach = dearbh(서술자);
        if (slot_cur_a_steach < 0) return -9;
        fiosrachadh_COUNT[targaid[slot_cur_a_steach]]--; 사용[slot_cur_a_steach] = 0; return 0;
    }
    public static int atharraich_am_meud(int 서술자) {
        int slot_cur_a_steach = dearbh(서술자); return slot_cur_a_steach < 0 ? -9 : faid_VALUE[targaid[slot_cur_a_steach]];
    }
    public static int seata_faid(int 서술자, int atharraich_am_meud) {
        int slot_cur_a_steach = dearbh(서술자);
        if (slot_cur_a_steach < 0 || (dòigh_MODE[slot_cur_a_steach] & 3) == 0) return -9;
        if (atharraich_am_meud < 0 || atharraich_am_meud > 16384) return -22;
        int faidhle = targaid[slot_cur_a_steach];
        while (faid_VALUE[faidhle] < atharraich_am_meud) sgrìobh_dàta(faidhle, faid_VALUE[faidhle]++, 0);
        faid_VALUE[faidhle] = atharraich_am_meud; return 0;
    }
    public static int 지우기() {
        if (slighe_faid == 0) return -22;
        int tomhas = àbhaistich_VALUE(); if (tomhas < 0) return tomhas;
        if (FIND_eòlaire(정규길이) >= 0) return -21;
        tomhas = 부모확인(); if (tomhas < 0) return tomhas;
        int faidhle = FIND_cur_a_steach();
        if (faidhle < 0) return -2;
        이름길이[faidhle] = 0; return 0; // 열려 있는 파일은 마지막 close까지 유지
    }
    static void cur_a_steach_Liosta() {
        slighe_Start(1); slighe_baidht(0, '.'); 경로목록();
    }
    public static int 공개이름길이(int INDEX) {
        if (INDEX < 0 || INDEX >= faidhle_COUNT || 이름길이[INDEX] == 0) return 0;
        for (int lùb_INDEX = 0; lùb_INDEX < 이름길이[INDEX]; lùb_INDEX++) if (Ainm[INDEX * 64 + lùb_INDEX] == '/') return 0;
        return 이름길이[INDEX];
    }
    public static int 공개이름바이트(int INDEX, int suidhich_INDEX) {
        return INDEX >= 0 && INDEX < faidhle_COUNT && suidhich_INDEX >= 0 && suidhich_INDEX < 이름길이[INDEX] ? Ainm[INDEX * 64 + suidhich_INDEX] : -22;
    }
    public static int 공개파일크기(int INDEX) { return INDEX >= 0 && INDEX < faidhle_COUNT ? faid_VALUE[INDEX] : -22; }
    static int[] 정규 = new int[64], 현재 = new int[64], eòlaire_ainm = new int[16 * 64], eòlaire_faid = new int[16];
    static int 정규길이, 현재길이;
    static boolean 접두(int[] 이름들, int ruith, int slighe_VALUE, int[] 앞, int beàrn_eadar_dà_loidhne_slighe) {
        if (slighe_VALUE < beàrn_eadar_dà_loidhne_slighe) return false;
        for (int lùb_INDEX = 0; lùb_INDEX < beàrn_eadar_dà_loidhne_slighe; lùb_INDEX++) if (이름들[ruith + lùb_INDEX] != 앞[lùb_INDEX]) return false;
        return true;
    }
    static int àbhaistich_VALUE() {
        if (slighe_faid == 0) return -22;
        정규길이 = Slighe[0] == '/' ? 0 : 현재길이;
        for (int lùb_INDEX = 0; lùb_INDEX < 정규길이; lùb_INDEX++) 정규[lùb_INDEX] = 현재[lùb_INDEX];
        int 읽는자리 = 0;
        while (읽는자리 < slighe_faid) {
            while (읽는자리 < slighe_faid && Slighe[읽는자리] == '/') 읽는자리++;
            int Start_suidhich = 읽는자리; while (읽는자리 < slighe_faid && Slighe[읽는자리] != '/') { if (Slighe[읽는자리] == 0) return -22; 읽는자리++; }
            int cur_a_steach_COUNT = 읽는자리 - Start_suidhich; if (cur_a_steach_COUNT == 0 || cur_a_steach_COUNT == 1 && Slighe[Start_suidhich] == '.') continue;
            if (cur_a_steach_COUNT == 2 && Slighe[Start_suidhich] == '.' && Slighe[Start_suidhich + 1] == '.') {
                while (정규길이 > 0 && 정규[정규길이 - 1] != '/') 정규길이--;
                if (정규길이 > 0) 정규길이--;
                continue;
            }
            if (정규길이 + cur_a_steach_COUNT + (정규길이 == 0 ? 0 : 1) > 63) return -36;
            if (정규길이 > 0) 정규[정규길이++] = '/';
            for (int lùb_INDEX = Start_suidhich; lùb_INDEX < 읽는자리; lùb_INDEX++) 정규[정규길이++] = Slighe[lùb_INDEX];
        }
        return 0;
    }
    static int FIND_eòlaire(int cur_a_steach_COUNT) {
        if (cur_a_steach_COUNT == 0) return 0;
        for (int lùb_INDEX = 1; lùb_INDEX < 16; lùb_INDEX++) if (eòlaire_faid[lùb_INDEX] == cur_a_steach_COUNT && 접두(eòlaire_ainm, lùb_INDEX * 64, cur_a_steach_COUNT, 정규, cur_a_steach_COUNT)) return lùb_INDEX;
        return -1;
    }
    static int 부모확인() {
        int cur_a_steach_COUNT = 정규길이; while (cur_a_steach_COUNT > 0 && 정규[cur_a_steach_COUNT - 1] != '/') cur_a_steach_COUNT--;
        return FIND_eòlaire(cur_a_steach_COUNT == 0 ? 0 : cur_a_steach_COUNT - 1) < 0 ? -2 : 0;
    }
    public static int Create_eòlaire() {
        int 처리값 = àbhaistich_VALUE(); if (처리값 < 0) return 처리값;
        if (FIND_eòlaire(정규길이) >= 0 || FIND_cur_a_steach() >= 0) return -17;
        처리값 = 부모확인(); if (처리값 < 0) return 처리값;
        for (int lùb_INDEX = 1; lùb_INDEX < 16; lùb_INDEX++) if (eòlaire_faid[lùb_INDEX] == 0) {
            eòlaire_faid[lùb_INDEX] = 정규길이; for (int Inner_Join_suidhich = 0; Inner_Join_suidhich < 정규길이; Inner_Join_suidhich++) eòlaire_ainm[lùb_INDEX * 64 + Inner_Join_suidhich] = 정규[Inner_Join_suidhich]; return 0;
        }
        return -28;
    }
    public static int 항목종류() {
        int 처리값 = àbhaistich_VALUE(); if (처리값 < 0) return 처리값;
        if (FIND_eòlaire(정규길이) >= 0) return 2;
        return FIND_cur_a_steach() >= 0 ? 1 : 0;
    }
    public static int atharraich_eòlaire() {
        int 처리값 = àbhaistich_VALUE(); if (처리값 < 0) return 처리값;
        if (FIND_eòlaire(정규길이) < 0) return -2;
        현재길이 = 정규길이; for (int lùb_INDEX = 0; lùb_INDEX < 현재길이; lùb_INDEX++) 현재[lùb_INDEX] = 정규[lùb_INDEX]; return 0;
    }
    public static int thoir_air_falbh_eòlaire() {
        int 처리값 = àbhaistich_VALUE(); if (처리값 < 0) return 처리값;
        int 폴더번호 = FIND_eòlaire(정규길이); if (폴더번호 < 0) return -2; if (폴더번호 == 0) return -16;
        if (현재길이 == 정규길이 && 접두(현재, 0, 현재길이, 정규, 정규길이)) return -16;
        for (int lùb_INDEX = 0; lùb_INDEX < faidhle_COUNT; lùb_INDEX++) {
            if (이름길이[lùb_INDEX] > 정규길이 && 접두(Ainm, lùb_INDEX * 64, 이름길이[lùb_INDEX], 정규, 정규길이) && Ainm[lùb_INDEX * 64 + 정규길이] == '/') return -39;
        }
        for (int lùb_INDEX = 0; lùb_INDEX < 16; lùb_INDEX++) {
            if (eòlaire_faid[lùb_INDEX] > 정규길이 && 접두(eòlaire_ainm, lùb_INDEX * 64, eòlaire_faid[lùb_INDEX], 정규, 정규길이) && eòlaire_ainm[lùb_INDEX * 64 + 정규길이] == '/') return -39;
        }
        eòlaire_faid[폴더번호] = 0; return 0;
    }
    public static int 이름바꾸기(int 원본번호) {
        if (원본번호 < 0 || 원본번호 >= faidhle_COUNT || 이름길이[원본번호] == 0) return -2;
        int 처리값 = àbhaistich_VALUE(); if (처리값 < 0) return 처리값;
        if (FIND_eòlaire(정규길이) >= 0) return -21;
        처리값 = 부모확인(); if (처리값 < 0) return 처리값;
        int 이전값 = FIND_cur_a_steach(); if (이전값 == 원본번호) return 0;
        if (이전값 >= 0) 이름길이[이전값] = 0;
        이름길이[원본번호] = 정규길이; for (int lùb_INDEX = 0; lùb_INDEX < 정규길이; lùb_INDEX++) Ainm[원본번호 * 64 + lùb_INDEX] = 정규[lùb_INDEX]; return 0;
    }
    static int cur_a_steach_Start(int[] dàta_ARRAY, int 시작점, int cur_a_steach_COUNT) {
        if (!접두(dàta_ARRAY, 시작점, cur_a_steach_COUNT, 정규, 정규길이)) return -1;
        int Start_suidhich = 정규길이;
        if (Start_suidhich > 0) { if (cur_a_steach_COUNT <= Start_suidhich || dàta_ARRAY[시작점 + Start_suidhich] != '/') return -1; Start_suidhich++; }
        if (cur_a_steach_COUNT <= Start_suidhich) return -1;
        for (int lùb_INDEX = Start_suidhich; lùb_INDEX < cur_a_steach_COUNT; lùb_INDEX++) if (dàta_ARRAY[시작점 + lùb_INDEX] == '/') return -1;
        return Start_suidhich;
    }
    static void 현재쓰기() { 단말.문자('/'); for (int lùb_INDEX = 0; lùb_INDEX < 현재길이; lùb_INDEX++) bòrd.직렬쓰기(현재[lùb_INDEX]); }
    static int 경로목록() {
        int 처리값 = àbhaistich_VALUE(); if (처리값 < 0) return 처리값;
        int faidhle_targaid = FIND_cur_a_steach();
        if (faidhle_targaid >= 0) { for (int lùb_INDEX = 0; lùb_INDEX < 정규길이; lùb_INDEX++) bòrd.직렬쓰기(정규[lùb_INDEX]); 단말.sgrìobh("  "); 단말.수(faid_VALUE[faidhle_targaid]); 단말.sgrìobh("baidht_VALUE(주기억 faidhle)\n"); return 0; }
        if (FIND_eòlaire(정규길이) < 0) return -2;
        for (int 뒷값 = 1; 뒷값 < 16; 뒷값++) if (eòlaire_faid[뒷값] > 0) {
            int Start_suidhich = cur_a_steach_Start(eòlaire_ainm, 뒷값 * 64, eòlaire_faid[뒷값]); if (Start_suidhich < 0) continue;
            for (int lùb_INDEX = Start_suidhich; lùb_INDEX < eòlaire_faid[뒷값]; lùb_INDEX++) bòrd.직렬쓰기(eòlaire_ainm[뒷값 * 64 + lùb_INDEX]); 단말.sgrìobh("/\n");
        }
        for (int faidhle_INDEX = 0; faidhle_INDEX < faidhle_COUNT; faidhle_INDEX++) if (이름길이[faidhle_INDEX] > 0) {
            int Start_suidhich = cur_a_steach_Start(Ainm, faidhle_INDEX * 64, 이름길이[faidhle_INDEX]); if (Start_suidhich < 0) continue;
            for (int lùb_INDEX = Start_suidhich; lùb_INDEX < 이름길이[faidhle_INDEX]; lùb_INDEX++) bòrd.직렬쓰기(Ainm[faidhle_INDEX * 64 + lùb_INDEX]);
            단말.sgrìobh("  "); 단말.수(faid_VALUE[faidhle_INDEX]); 단말.sgrìobh("baidht_VALUE(주기억 faidhle)\n");
        }
        return 0;
    }
}
