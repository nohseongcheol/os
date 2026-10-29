// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** RAM Comhad 64개, 파일당 16384바이트, 서술자 16개. 모든 sonraí/정책은 Java에 있다.
 * 호출 도중 양보하지 않으므로 현재의 단일 코어 협력식 작업 사이에서 원자적이다.
 * 디스크 저장이나 POSIX 전체 구현을 뜻하지 않는다. 음수 반환은 ERREÁID 번호다.
 */
public final class Cuimhne_Comhaid {
    static final int comhad_COUNT = 64;
    static int[] Ainm = new int[comhad_COUNT * 64];
    static int[] 이름길이 = new int[comhad_COUNT];
    // Pack four bytes in each Java int, preserving the old content heap budget.
    static int[] Inneachar_VALUE = new int[comhad_COUNT * 4096];
    static int[] fad_VALUE = new int[comhad_COUNT];
    static int[] Leabhair_thagartha_COUNT = new int[comhad_COUNT];
    static int[] 사용 = new int[16];
    static int[] sprioc = new int[16];
    static int[] suíomh = new int[16];
    static int[] modh_mód = new int[16];
    static int[] CONAIR = new int[64];
    static int cosán_fad;

    public static int 파일한도() { return comhad_COUNT; }
    static int 자료읽기(int Comhad, int suíomh_INDEX) { return (Inneachar_VALUE[Comhad * 4096 + suíomh_INDEX / 4] >>> ((suíomh_INDEX & 3) * 8)) & 255; }
    static void scríobh_sonraí(int Comhad, int suíomh_INDEX, int VALUE) {
        int spás_iontráil = Comhad * 4096 + suíomh_INDEX / 4, bog_VALUE = (suíomh_INDEX & 3) * 8;
        Inneachar_VALUE[spás_iontráil] = (Inneachar_VALUE[spás_iontráil] & ~(255 << bog_VALUE)) | ((VALUE & 255) << bog_VALUE);
    }

    public static int cosán_Start(int Méid) {
        cosán_fad = 0;
        if (Méid < 1 || Méid > 63) return -36;
        cosán_fad = Méid;
        for (int lúb_INDEX = 0; lúb_INDEX < Méid; lúb_INDEX++) CONAIR[lúb_INDEX] = 0;
        return 0;
    }
    public static int cosán_beart(int INDEX, int VALUE) {
        if (INDEX < 0 || INDEX >= cosán_fad || VALUE < 1 || VALUE > 255) return -22;
        CONAIR[INDEX] = VALUE; return 0;
    }
    static int FIND_iontráil() {
        for (int comhad_INDEX = 0; comhad_INDEX < comhad_COUNT; comhad_INDEX++) if (이름길이[comhad_INDEX] > 0 && 이름길이[comhad_INDEX] == 정규길이 && 접두(Ainm, comhad_INDEX * 64, 이름길이[comhad_INDEX], 정규, 정규길이)) return comhad_INDEX;
        return -1;
    }
    public static int Oscail(int 플래그) {
        if (cosán_fad == 0 || (플래그 & ~0x6c3) != 0 || (플래그 & 3) == 3) return -22;
        for (int lúb_INDEX = 0; lúb_INDEX < cosán_fad; lúb_INDEX++) if (CONAIR[lúb_INDEX] == 0) return -22;
        if ((플래그 & 0x200) != 0 && (플래그 & 3) == 0) return -22;
        int tomhas = normalaigh_VALUE(); if (tomhas < 0) return tomhas;
        if (FIND_eolaire(정규길이) >= 0) return -21;
        tomhas = 부모확인(); if (tomhas < 0) return tomhas;
        int Comhad = FIND_iontráil();
        if (Comhad >= 0 && (플래그 & 0xc0) == 0xc0) return -17;
        if (Comhad < 0 && (플래그 & 0x40) == 0) return -2;
        int 서술자 = -1;
        for (int lúb_INDEX = 0; lúb_INDEX < 16; lúb_INDEX++) if (사용[lúb_INDEX] == 0) { 서술자 = lúb_INDEX; break; }
        if (서술자 < 0) return -24;
        if (Comhad < 0) {
            for (int lúb_INDEX = 0; lúb_INDEX < comhad_COUNT; lúb_INDEX++) if (이름길이[lúb_INDEX] == 0 && Leabhair_thagartha_COUNT[lúb_INDEX] == 0) { Comhad = lúb_INDEX; break; }
            if (Comhad < 0) return -28;
            이름길이[Comhad] = 정규길이;
            for (int lúb_INDEX = 0; lúb_INDEX < 정규길이; lúb_INDEX++) Ainm[Comhad * 64 + lúb_INDEX] = 정규[lúb_INDEX];
            fad_VALUE[Comhad] = 0;
        }
        if ((플래그 & 0x200) != 0) fad_VALUE[Comhad] = 0;
        사용[서술자] = 1; sprioc[서술자] = Comhad; suíomh[서술자] = 0; modh_mód[서술자] = 플래그;
        Leabhair_thagartha_COUNT[Comhad]++;
        return 서술자 + 3;
    }
    static int fíoraigh(int 서술자) {
        return 서술자 >= 3 && 서술자 < 19 && 사용[서술자 - 3] != 0 ? 서술자 - 3 : -1;
    }
    public static int Léigh(int 서술자) {
        int spás_iontráil = fíoraigh(서술자);
        if (spás_iontráil < 0 || (modh_mód[spás_iontráil] & 3) == 1) return -9;
        int Comhad = sprioc[spás_iontráil];
        if (suíomh[spás_iontráil] >= fad_VALUE[Comhad]) return 256; // EOF와 iarbhír_sonraí 0x00..0xff 구별
        return 자료읽기(Comhad, suíomh[spás_iontráil]++);
    }
    public static int Scríobh(int 서술자, int VALUE) {
        int spás_iontráil = fíoraigh(서술자);
        if (spás_iontráil < 0 || (modh_mód[spás_iontráil] & 3) == 0) return -9;
        int Comhad = sprioc[spás_iontráil];
        if ((modh_mód[spás_iontráil] & 0x400) != 0) suíomh[spás_iontráil] = fad_VALUE[Comhad];
        if (suíomh[spás_iontráil] >= 16384) return -28;
        while (fad_VALUE[Comhad] < suíomh[spás_iontráil]) scríobh_sonraí(Comhad, fad_VALUE[Comhad]++, 0);
        scríobh_sonraí(Comhad, suíomh[spás_iontráil]++, VALUE);
        if (fad_VALUE[Comhad] < suíomh[spás_iontráil]) fad_VALUE[Comhad] = suíomh[spás_iontráil];
        return 1;
    }
    public static int lorg_suíomh(int 서술자, int 거리, int teilgean_fréamh) {
        int spás_iontráil = fíoraigh(서술자);
        if (spás_iontráil < 0) return -9;
        if (teilgean_fréamh < 0 || teilgean_fréamh > 2 || 거리 < -16384 || 거리 > 16384) return -22;
        int 새위치 = 거리 + (teilgean_fréamh == 0 ? 0 : teilgean_fréamh == 1 ? suíomh[spás_iontráil] : fad_VALUE[sprioc[spás_iontráil]]);
        if (새위치 < 0 || 새위치 > 16384) return -22;
        suíomh[spás_iontráil] = 새위치; return 새위치;
    }
    public static int Dún(int 서술자) {
        int spás_iontráil = fíoraigh(서술자);
        if (spás_iontráil < 0) return -9;
        Leabhair_thagartha_COUNT[sprioc[spás_iontráil]]--; 사용[spás_iontráil] = 0; return 0;
    }
    public static int Méid(int 서술자) {
        int spás_iontráil = fíoraigh(서술자); return spás_iontráil < 0 ? -9 : fad_VALUE[sprioc[spás_iontráil]];
    }
    public static int tacar_fad(int 서술자, int Méid) {
        int spás_iontráil = fíoraigh(서술자);
        if (spás_iontráil < 0 || (modh_mód[spás_iontráil] & 3) == 0) return -9;
        if (Méid < 0 || Méid > 16384) return -22;
        int Comhad = sprioc[spás_iontráil];
        while (fad_VALUE[Comhad] < Méid) scríobh_sonraí(Comhad, fad_VALUE[Comhad]++, 0);
        fad_VALUE[Comhad] = Méid; return 0;
    }
    public static int 지우기() {
        if (cosán_fad == 0) return -22;
        int tomhas = normalaigh_VALUE(); if (tomhas < 0) return tomhas;
        if (FIND_eolaire(정규길이) >= 0) return -21;
        tomhas = 부모확인(); if (tomhas < 0) return tomhas;
        int Comhad = FIND_iontráil();
        if (Comhad < 0) return -2;
        이름길이[Comhad] = 0; return 0; // 열려 있는 파일은 마지막 close까지 유지
    }
    static void iontráil_Liosta() {
        cosán_Start(1); cosán_beart(0, '.'); 경로목록();
    }
    public static int 공개이름길이(int INDEX) {
        if (INDEX < 0 || INDEX >= comhad_COUNT || 이름길이[INDEX] == 0) return 0;
        for (int lúb_INDEX = 0; lúb_INDEX < 이름길이[INDEX]; lúb_INDEX++) if (Ainm[INDEX * 64 + lúb_INDEX] == '/') return 0;
        return 이름길이[INDEX];
    }
    public static int 공개이름바이트(int INDEX, int suíomh_INDEX) {
        return INDEX >= 0 && INDEX < comhad_COUNT && suíomh_INDEX >= 0 && suíomh_INDEX < 이름길이[INDEX] ? Ainm[INDEX * 64 + suíomh_INDEX] : -22;
    }
    public static int 공개파일크기(int INDEX) { return INDEX >= 0 && INDEX < comhad_COUNT ? fad_VALUE[INDEX] : -22; }
    static int[] 정규 = new int[64], 현재 = new int[64], eolaire_ainm = new int[16 * 64], eolaire_fad = new int[16];
    static int 정규길이, 현재길이;
    static boolean 접두(int[] 이름들, int Rith_2, int cosán_VALUE, int[] 앞, int spásáil_línte_cosán) {
        if (cosán_VALUE < spásáil_línte_cosán) return false;
        for (int lúb_INDEX = 0; lúb_INDEX < spásáil_línte_cosán; lúb_INDEX++) if (이름들[Rith_2 + lúb_INDEX] != 앞[lúb_INDEX]) return false;
        return true;
    }
    static int normalaigh_VALUE() {
        if (cosán_fad == 0) return -22;
        정규길이 = CONAIR[0] == '/' ? 0 : 현재길이;
        for (int lúb_INDEX = 0; lúb_INDEX < 정규길이; lúb_INDEX++) 정규[lúb_INDEX] = 현재[lúb_INDEX];
        int 읽는자리 = 0;
        while (읽는자리 < cosán_fad) {
            while (읽는자리 < cosán_fad && CONAIR[읽는자리] == '/') 읽는자리++;
            int Start_suíomh = 읽는자리; while (읽는자리 < cosán_fad && CONAIR[읽는자리] != '/') { if (CONAIR[읽는자리] == 0) return -22; 읽는자리++; }
            int iontráil_COUNT = 읽는자리 - Start_suíomh; if (iontráil_COUNT == 0 || iontráil_COUNT == 1 && CONAIR[Start_suíomh] == '.') continue;
            if (iontráil_COUNT == 2 && CONAIR[Start_suíomh] == '.' && CONAIR[Start_suíomh + 1] == '.') {
                while (정규길이 > 0 && 정규[정규길이 - 1] != '/') 정규길이--;
                if (정규길이 > 0) 정규길이--;
                continue;
            }
            if (정규길이 + iontráil_COUNT + (정규길이 == 0 ? 0 : 1) > 63) return -36;
            if (정규길이 > 0) 정규[정규길이++] = '/';
            for (int lúb_INDEX = Start_suíomh; lúb_INDEX < 읽는자리; lúb_INDEX++) 정규[정규길이++] = CONAIR[lúb_INDEX];
        }
        return 0;
    }
    static int FIND_eolaire(int iontráil_COUNT) {
        if (iontráil_COUNT == 0) return 0;
        for (int lúb_INDEX = 1; lúb_INDEX < 16; lúb_INDEX++) if (eolaire_fad[lúb_INDEX] == iontráil_COUNT && 접두(eolaire_ainm, lúb_INDEX * 64, iontráil_COUNT, 정규, iontráil_COUNT)) return lúb_INDEX;
        return -1;
    }
    static int 부모확인() {
        int iontráil_COUNT = 정규길이; while (iontráil_COUNT > 0 && 정규[iontráil_COUNT - 1] != '/') iontráil_COUNT--;
        return FIND_eolaire(iontráil_COUNT == 0 ? 0 : iontráil_COUNT - 1) < 0 ? -2 : 0;
    }
    public static int Create_eolaire() {
        int 처리값 = normalaigh_VALUE(); if (처리값 < 0) return 처리값;
        if (FIND_eolaire(정규길이) >= 0 || FIND_iontráil() >= 0) return -17;
        처리값 = 부모확인(); if (처리값 < 0) return 처리값;
        for (int lúb_INDEX = 1; lúb_INDEX < 16; lúb_INDEX++) if (eolaire_fad[lúb_INDEX] == 0) {
            eolaire_fad[lúb_INDEX] = 정규길이; for (int comhcheangal_istigh_suíomh = 0; comhcheangal_istigh_suíomh < 정규길이; comhcheangal_istigh_suíomh++) eolaire_ainm[lúb_INDEX * 64 + comhcheangal_istigh_suíomh] = 정규[comhcheangal_istigh_suíomh]; return 0;
        }
        return -28;
    }
    public static int 항목종류() {
        int 처리값 = normalaigh_VALUE(); if (처리값 < 0) return 처리값;
        if (FIND_eolaire(정규길이) >= 0) return 2;
        return FIND_iontráil() >= 0 ? 1 : 0;
    }
    public static int athraigh_eolaire() {
        int 처리값 = normalaigh_VALUE(); if (처리값 < 0) return 처리값;
        if (FIND_eolaire(정규길이) < 0) return -2;
        현재길이 = 정규길이; for (int lúb_INDEX = 0; lúb_INDEX < 현재길이; lúb_INDEX++) 현재[lúb_INDEX] = 정규[lúb_INDEX]; return 0;
    }
    public static int bain_eolaire() {
        int 처리값 = normalaigh_VALUE(); if (처리값 < 0) return 처리값;
        int 폴더번호 = FIND_eolaire(정규길이); if (폴더번호 < 0) return -2; if (폴더번호 == 0) return -16;
        if (현재길이 == 정규길이 && 접두(현재, 0, 현재길이, 정규, 정규길이)) return -16;
        for (int lúb_INDEX = 0; lúb_INDEX < comhad_COUNT; lúb_INDEX++) {
            if (이름길이[lúb_INDEX] > 정규길이 && 접두(Ainm, lúb_INDEX * 64, 이름길이[lúb_INDEX], 정규, 정규길이) && Ainm[lúb_INDEX * 64 + 정규길이] == '/') return -39;
        }
        for (int lúb_INDEX = 0; lúb_INDEX < 16; lúb_INDEX++) {
            if (eolaire_fad[lúb_INDEX] > 정규길이 && 접두(eolaire_ainm, lúb_INDEX * 64, eolaire_fad[lúb_INDEX], 정규, 정규길이) && eolaire_ainm[lúb_INDEX * 64 + 정규길이] == '/') return -39;
        }
        eolaire_fad[폴더번호] = 0; return 0;
    }
    public static int 이름바꾸기(int 원본번호) {
        if (원본번호 < 0 || 원본번호 >= comhad_COUNT || 이름길이[원본번호] == 0) return -2;
        int 처리값 = normalaigh_VALUE(); if (처리값 < 0) return 처리값;
        if (FIND_eolaire(정규길이) >= 0) return -21;
        처리값 = 부모확인(); if (처리값 < 0) return 처리값;
        int 이전값 = FIND_iontráil(); if (이전값 == 원본번호) return 0;
        if (이전값 >= 0) 이름길이[이전값] = 0;
        이름길이[원본번호] = 정규길이; for (int lúb_INDEX = 0; lúb_INDEX < 정규길이; lúb_INDEX++) Ainm[원본번호 * 64 + lúb_INDEX] = 정규[lúb_INDEX]; return 0;
    }
    static int iontráil_Start(int[] sonraí_ARRAY, int 시작점, int iontráil_COUNT) {
        if (!접두(sonraí_ARRAY, 시작점, iontráil_COUNT, 정규, 정규길이)) return -1;
        int Start_suíomh = 정규길이;
        if (Start_suíomh > 0) { if (iontráil_COUNT <= Start_suíomh || sonraí_ARRAY[시작점 + Start_suíomh] != '/') return -1; Start_suíomh++; }
        if (iontráil_COUNT <= Start_suíomh) return -1;
        for (int lúb_INDEX = Start_suíomh; lúb_INDEX < iontráil_COUNT; lúb_INDEX++) if (sonraí_ARRAY[시작점 + lúb_INDEX] == '/') return -1;
        return Start_suíomh;
    }
    static void 현재쓰기() { 단말.문자('/'); for (int lúb_INDEX = 0; lúb_INDEX < 현재길이; lúb_INDEX++) clár.직렬쓰기(현재[lúb_INDEX]); }
    static int 경로목록() {
        int 처리값 = normalaigh_VALUE(); if (처리값 < 0) return 처리값;
        int comhad_sprioc = FIND_iontráil();
        if (comhad_sprioc >= 0) { for (int lúb_INDEX = 0; lúb_INDEX < 정규길이; lúb_INDEX++) clár.직렬쓰기(정규[lúb_INDEX]); 단말.Scríobh("  "); 단말.수(fad_VALUE[comhad_sprioc]); 단말.Scríobh("beart_VALUE(주기억 Comhad)\n"); return 0; }
        if (FIND_eolaire(정규길이) < 0) return -2;
        for (int 뒷값 = 1; 뒷값 < 16; 뒷값++) if (eolaire_fad[뒷값] > 0) {
            int Start_suíomh = iontráil_Start(eolaire_ainm, 뒷값 * 64, eolaire_fad[뒷값]); if (Start_suíomh < 0) continue;
            for (int lúb_INDEX = Start_suíomh; lúb_INDEX < eolaire_fad[뒷값]; lúb_INDEX++) clár.직렬쓰기(eolaire_ainm[뒷값 * 64 + lúb_INDEX]); 단말.Scríobh("/\n");
        }
        for (int comhad_INDEX = 0; comhad_INDEX < comhad_COUNT; comhad_INDEX++) if (이름길이[comhad_INDEX] > 0) {
            int Start_suíomh = iontráil_Start(Ainm, comhad_INDEX * 64, 이름길이[comhad_INDEX]); if (Start_suíomh < 0) continue;
            for (int lúb_INDEX = Start_suíomh; lúb_INDEX < 이름길이[comhad_INDEX]; lúb_INDEX++) clár.직렬쓰기(Ainm[comhad_INDEX * 64 + lúb_INDEX]);
            단말.Scríobh("  "); 단말.수(fad_VALUE[comhad_INDEX]); 단말.Scríobh("beart_VALUE(주기억 Comhad)\n");
        }
        return 0;
    }
}
