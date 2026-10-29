// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** RAM Kōnae 64개, 파일당 16384바이트, 서술자 16개. 모든 raraunga/정책은 Java에 있다.
 * 호출 도중 양보하지 않으므로 현재의 단일 코어 협력식 작업 사이에서 원자적이다.
 * 디스크 저장이나 POSIX 전체 구현을 뜻하지 않는다. 음수 반환은 Pōhēhē 번호다.
 */
public final class Pūmahara_Ngā_Kōnae {
    static final int kōnae_COUNT = 64;
    static int[] Ingoa = new int[kōnae_COUNT * 64];
    static int[] 이름길이 = new int[kōnae_COUNT];
    // Pack four bytes in each Java int, preserving the old content heap budget.
    static int[] Ihirangi_uara = new int[kōnae_COUNT * 4096];
    static int[] roa_uara = new int[kōnae_COUNT];
    static int[] Pūranga_kōrero_COUNT = new int[kōnae_COUNT];
    static int[] 사용 = new int[16];
    static int[] ūnga = new int[16];
    static int[] tūranga = new int[16];
    static int[] aratuka_MODE = new int[16];
    static int[] ara = new int[64];
    static int ara_roa;

    public static int 파일한도() { return kōnae_COUNT; }
    static int 자료읽기(int Kōnae, int tūranga_INDEX) { return (Ihirangi_uara[Kōnae * 4096 + tūranga_INDEX / 4] >>> ((tūranga_INDEX & 3) * 8)) & 255; }
    static void tuhi_raraunga(int Kōnae, int tūranga_INDEX, int uara) {
        int kāniwha_tāurunga = Kōnae * 4096 + tūranga_INDEX / 4, nuku_uara = (tūranga_INDEX & 3) * 8;
        Ihirangi_uara[kāniwha_tāurunga] = (Ihirangi_uara[kāniwha_tāurunga] & ~(255 << nuku_uara)) | ((uara & 255) << nuku_uara);
    }

    public static int ara_Start(int rahi) {
        ara_roa = 0;
        if (rahi < 1 || rahi > 63) return -36;
        ara_roa = rahi;
        for (int Loop_INDEX = 0; Loop_INDEX < rahi; Loop_INDEX++) ara[Loop_INDEX] = 0;
        return 0;
    }
    public static int ara_paita(int INDEX, int uara) {
        if (INDEX < 0 || INDEX >= ara_roa || uara < 1 || uara > 255) return -22;
        ara[INDEX] = uara; return 0;
    }
    static int FIND_tāurunga() {
        for (int kōnae_INDEX = 0; kōnae_INDEX < kōnae_COUNT; kōnae_INDEX++) if (이름길이[kōnae_INDEX] > 0 && 이름길이[kōnae_INDEX] == 정규길이 && 접두(Ingoa, kōnae_INDEX * 64, 이름길이[kōnae_INDEX], 정규, 정규길이)) return kōnae_INDEX;
        return -1;
    }
    public static int Huaki(int 플래그) {
        if (ara_roa == 0 || (플래그 & ~0x6c3) != 0 || (플래그 & 3) == 3) return -22;
        for (int Loop_INDEX = 0; Loop_INDEX < ara_roa; Loop_INDEX++) if (ara[Loop_INDEX] == 0) return -22;
        if ((플래그 & 0x200) != 0 && (플래그 & 3) == 0) return -22;
        int mēhua = whakanoa_uara(); if (mēhua < 0) return mēhua;
        if (FIND_whaiaronga(정규길이) >= 0) return -21;
        mēhua = 부모확인(); if (mēhua < 0) return mēhua;
        int Kōnae = FIND_tāurunga();
        if (Kōnae >= 0 && (플래그 & 0xc0) == 0xc0) return -17;
        if (Kōnae < 0 && (플래그 & 0x40) == 0) return -2;
        int 서술자 = -1;
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (사용[Loop_INDEX] == 0) { 서술자 = Loop_INDEX; break; }
        if (서술자 < 0) return -24;
        if (Kōnae < 0) {
            for (int Loop_INDEX = 0; Loop_INDEX < kōnae_COUNT; Loop_INDEX++) if (이름길이[Loop_INDEX] == 0 && Pūranga_kōrero_COUNT[Loop_INDEX] == 0) { Kōnae = Loop_INDEX; break; }
            if (Kōnae < 0) return -28;
            이름길이[Kōnae] = 정규길이;
            for (int Loop_INDEX = 0; Loop_INDEX < 정규길이; Loop_INDEX++) Ingoa[Kōnae * 64 + Loop_INDEX] = 정규[Loop_INDEX];
            roa_uara[Kōnae] = 0;
        }
        if ((플래그 & 0x200) != 0) roa_uara[Kōnae] = 0;
        사용[서술자] = 1; ūnga[서술자] = Kōnae; tūranga[서술자] = 0; aratuka_MODE[서술자] = 플래그;
        Pūranga_kōrero_COUNT[Kōnae]++;
        return 서술자 + 3;
    }
    static int manatoko(int 서술자) {
        return 서술자 >= 3 && 서술자 < 19 && 사용[서술자 - 3] != 0 ? 서술자 - 3 : -1;
    }
    public static int Pānuitia(int 서술자) {
        int kāniwha_tāurunga = manatoko(서술자);
        if (kāniwha_tāurunga < 0 || (aratuka_MODE[kāniwha_tāurunga] & 3) == 1) return -9;
        int Kōnae = ūnga[kāniwha_tāurunga];
        if (tūranga[kāniwha_tāurunga] >= roa_uara[Kōnae]) return 256; // EOF와 tūturu_raraunga 0x00..0xff 구별
        return 자료읽기(Kōnae, tūranga[kāniwha_tāurunga]++);
    }
    public static int Tuhia(int 서술자, int uara) {
        int kāniwha_tāurunga = manatoko(서술자);
        if (kāniwha_tāurunga < 0 || (aratuka_MODE[kāniwha_tāurunga] & 3) == 0) return -9;
        int Kōnae = ūnga[kāniwha_tāurunga];
        if ((aratuka_MODE[kāniwha_tāurunga] & 0x400) != 0) tūranga[kāniwha_tāurunga] = roa_uara[Kōnae];
        if (tūranga[kāniwha_tāurunga] >= 16384) return -28;
        while (roa_uara[Kōnae] < tūranga[kāniwha_tāurunga]) tuhi_raraunga(Kōnae, roa_uara[Kōnae]++, 0);
        tuhi_raraunga(Kōnae, tūranga[kāniwha_tāurunga]++, uara);
        if (roa_uara[Kōnae] < tūranga[kāniwha_tāurunga]) roa_uara[Kōnae] = tūranga[kāniwha_tāurunga];
        return 1;
    }
    public static int kimi_tūranga(int 서술자, int 거리, int whakaatu_pūtake) {
        int kāniwha_tāurunga = manatoko(서술자);
        if (kāniwha_tāurunga < 0) return -9;
        if (whakaatu_pūtake < 0 || whakaatu_pūtake > 2 || 거리 < -16384 || 거리 > 16384) return -22;
        int 새위치 = 거리 + (whakaatu_pūtake == 0 ? 0 : whakaatu_pūtake == 1 ? tūranga[kāniwha_tāurunga] : roa_uara[ūnga[kāniwha_tāurunga]]);
        if (새위치 < 0 || 새위치 > 16384) return -22;
        tūranga[kāniwha_tāurunga] = 새위치; return 새위치;
    }
    public static int Kati(int 서술자) {
        int kāniwha_tāurunga = manatoko(서술자);
        if (kāniwha_tāurunga < 0) return -9;
        Pūranga_kōrero_COUNT[ūnga[kāniwha_tāurunga]]--; 사용[kāniwha_tāurunga] = 0; return 0;
    }
    public static int rahi(int 서술자) {
        int kāniwha_tāurunga = manatoko(서술자); return kāniwha_tāurunga < 0 ? -9 : roa_uara[ūnga[kāniwha_tāurunga]];
    }
    public static int huinga_roa(int 서술자, int rahi) {
        int kāniwha_tāurunga = manatoko(서술자);
        if (kāniwha_tāurunga < 0 || (aratuka_MODE[kāniwha_tāurunga] & 3) == 0) return -9;
        if (rahi < 0 || rahi > 16384) return -22;
        int Kōnae = ūnga[kāniwha_tāurunga];
        while (roa_uara[Kōnae] < rahi) tuhi_raraunga(Kōnae, roa_uara[Kōnae]++, 0);
        roa_uara[Kōnae] = rahi; return 0;
    }
    public static int 지우기() {
        if (ara_roa == 0) return -22;
        int mēhua = whakanoa_uara(); if (mēhua < 0) return mēhua;
        if (FIND_whaiaronga(정규길이) >= 0) return -21;
        mēhua = 부모확인(); if (mēhua < 0) return mēhua;
        int Kōnae = FIND_tāurunga();
        if (Kōnae < 0) return -2;
        이름길이[Kōnae] = 0; return 0; // 열려 있는 파일은 마지막 close까지 유지
    }
    static void tāurunga_Rārangi() {
        ara_Start(1); ara_paita(0, '.'); 경로목록();
    }
    public static int 공개이름길이(int INDEX) {
        if (INDEX < 0 || INDEX >= kōnae_COUNT || 이름길이[INDEX] == 0) return 0;
        for (int Loop_INDEX = 0; Loop_INDEX < 이름길이[INDEX]; Loop_INDEX++) if (Ingoa[INDEX * 64 + Loop_INDEX] == '/') return 0;
        return 이름길이[INDEX];
    }
    public static int 공개이름바이트(int INDEX, int tūranga_INDEX) {
        return INDEX >= 0 && INDEX < kōnae_COUNT && tūranga_INDEX >= 0 && tūranga_INDEX < 이름길이[INDEX] ? Ingoa[INDEX * 64 + tūranga_INDEX] : -22;
    }
    public static int 공개파일크기(int INDEX) { return INDEX >= 0 && INDEX < kōnae_COUNT ? roa_uara[INDEX] : -22; }
    static int[] 정규 = new int[64], 현재 = new int[64], whaiaronga_ingoa = new int[16 * 64], whaiaronga_roa = new int[16];
    static int 정규길이, 현재길이;
    static boolean 접두(int[] 이름들, int whakahaere, int ara_uara, int[] 앞, int mokowā_raina_ara) {
        if (ara_uara < mokowā_raina_ara) return false;
        for (int Loop_INDEX = 0; Loop_INDEX < mokowā_raina_ara; Loop_INDEX++) if (이름들[whakahaere + Loop_INDEX] != 앞[Loop_INDEX]) return false;
        return true;
    }
    static int whakanoa_uara() {
        if (ara_roa == 0) return -22;
        정규길이 = ara[0] == '/' ? 0 : 현재길이;
        for (int Loop_INDEX = 0; Loop_INDEX < 정규길이; Loop_INDEX++) 정규[Loop_INDEX] = 현재[Loop_INDEX];
        int 읽는자리 = 0;
        while (읽는자리 < ara_roa) {
            while (읽는자리 < ara_roa && ara[읽는자리] == '/') 읽는자리++;
            int Start_tūranga = 읽는자리; while (읽는자리 < ara_roa && ara[읽는자리] != '/') { if (ara[읽는자리] == 0) return -22; 읽는자리++; }
            int tāurunga_COUNT = 읽는자리 - Start_tūranga; if (tāurunga_COUNT == 0 || tāurunga_COUNT == 1 && ara[Start_tūranga] == '.') continue;
            if (tāurunga_COUNT == 2 && ara[Start_tūranga] == '.' && ara[Start_tūranga + 1] == '.') {
                while (정규길이 > 0 && 정규[정규길이 - 1] != '/') 정규길이--;
                if (정규길이 > 0) 정규길이--;
                continue;
            }
            if (정규길이 + tāurunga_COUNT + (정규길이 == 0 ? 0 : 1) > 63) return -36;
            if (정규길이 > 0) 정규[정규길이++] = '/';
            for (int Loop_INDEX = Start_tūranga; Loop_INDEX < 읽는자리; Loop_INDEX++) 정규[정규길이++] = ara[Loop_INDEX];
        }
        return 0;
    }
    static int FIND_whaiaronga(int tāurunga_COUNT) {
        if (tāurunga_COUNT == 0) return 0;
        for (int Loop_INDEX = 1; Loop_INDEX < 16; Loop_INDEX++) if (whaiaronga_roa[Loop_INDEX] == tāurunga_COUNT && 접두(whaiaronga_ingoa, Loop_INDEX * 64, tāurunga_COUNT, 정규, tāurunga_COUNT)) return Loop_INDEX;
        return -1;
    }
    static int 부모확인() {
        int tāurunga_COUNT = 정규길이; while (tāurunga_COUNT > 0 && 정규[tāurunga_COUNT - 1] != '/') tāurunga_COUNT--;
        return FIND_whaiaronga(tāurunga_COUNT == 0 ? 0 : tāurunga_COUNT - 1) < 0 ? -2 : 0;
    }
    public static int Waihanga_whaiaronga() {
        int 처리값 = whakanoa_uara(); if (처리값 < 0) return 처리값;
        if (FIND_whaiaronga(정규길이) >= 0 || FIND_tāurunga() >= 0) return -17;
        처리값 = 부모확인(); if (처리값 < 0) return 처리값;
        for (int Loop_INDEX = 1; Loop_INDEX < 16; Loop_INDEX++) if (whaiaronga_roa[Loop_INDEX] == 0) {
            whaiaronga_roa[Loop_INDEX] = 정규길이; for (int hono_roto_tūranga = 0; hono_roto_tūranga < 정규길이; hono_roto_tūranga++) whaiaronga_ingoa[Loop_INDEX * 64 + hono_roto_tūranga] = 정규[hono_roto_tūranga]; return 0;
        }
        return -28;
    }
    public static int 항목종류() {
        int 처리값 = whakanoa_uara(); if (처리값 < 0) return 처리값;
        if (FIND_whaiaronga(정규길이) >= 0) return 2;
        return FIND_tāurunga() >= 0 ? 1 : 0;
    }
    public static int huri_whaiaronga() {
        int 처리값 = whakanoa_uara(); if (처리값 < 0) return 처리값;
        if (FIND_whaiaronga(정규길이) < 0) return -2;
        현재길이 = 정규길이; for (int Loop_INDEX = 0; Loop_INDEX < 현재길이; Loop_INDEX++) 현재[Loop_INDEX] = 정규[Loop_INDEX]; return 0;
    }
    public static int tango_whaiaronga() {
        int 처리값 = whakanoa_uara(); if (처리값 < 0) return 처리값;
        int 폴더번호 = FIND_whaiaronga(정규길이); if (폴더번호 < 0) return -2; if (폴더번호 == 0) return -16;
        if (현재길이 == 정규길이 && 접두(현재, 0, 현재길이, 정규, 정규길이)) return -16;
        for (int Loop_INDEX = 0; Loop_INDEX < kōnae_COUNT; Loop_INDEX++) {
            if (이름길이[Loop_INDEX] > 정규길이 && 접두(Ingoa, Loop_INDEX * 64, 이름길이[Loop_INDEX], 정규, 정규길이) && Ingoa[Loop_INDEX * 64 + 정규길이] == '/') return -39;
        }
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) {
            if (whaiaronga_roa[Loop_INDEX] > 정규길이 && 접두(whaiaronga_ingoa, Loop_INDEX * 64, whaiaronga_roa[Loop_INDEX], 정규, 정규길이) && whaiaronga_ingoa[Loop_INDEX * 64 + 정규길이] == '/') return -39;
        }
        whaiaronga_roa[폴더번호] = 0; return 0;
    }
    public static int 이름바꾸기(int 원본번호) {
        if (원본번호 < 0 || 원본번호 >= kōnae_COUNT || 이름길이[원본번호] == 0) return -2;
        int 처리값 = whakanoa_uara(); if (처리값 < 0) return 처리값;
        if (FIND_whaiaronga(정규길이) >= 0) return -21;
        처리값 = 부모확인(); if (처리값 < 0) return 처리값;
        int 이전값 = FIND_tāurunga(); if (이전값 == 원본번호) return 0;
        if (이전값 >= 0) 이름길이[이전값] = 0;
        이름길이[원본번호] = 정규길이; for (int Loop_INDEX = 0; Loop_INDEX < 정규길이; Loop_INDEX++) Ingoa[원본번호 * 64 + Loop_INDEX] = 정규[Loop_INDEX]; return 0;
    }
    static int tāurunga_Start(int[] raraunga_HUĀNGA, int 시작점, int tāurunga_COUNT) {
        if (!접두(raraunga_HUĀNGA, 시작점, tāurunga_COUNT, 정규, 정규길이)) return -1;
        int Start_tūranga = 정규길이;
        if (Start_tūranga > 0) { if (tāurunga_COUNT <= Start_tūranga || raraunga_HUĀNGA[시작점 + Start_tūranga] != '/') return -1; Start_tūranga++; }
        if (tāurunga_COUNT <= Start_tūranga) return -1;
        for (int Loop_INDEX = Start_tūranga; Loop_INDEX < tāurunga_COUNT; Loop_INDEX++) if (raraunga_HUĀNGA[시작점 + Loop_INDEX] == '/') return -1;
        return Start_tūranga;
    }
    static void 현재쓰기() { 단말.문자('/'); for (int Loop_INDEX = 0; Loop_INDEX < 현재길이; Loop_INDEX++) papa.직렬쓰기(현재[Loop_INDEX]); }
    static int 경로목록() {
        int 처리값 = whakanoa_uara(); if (처리값 < 0) return 처리값;
        int kōnae_ūnga = FIND_tāurunga();
        if (kōnae_ūnga >= 0) { for (int Loop_INDEX = 0; Loop_INDEX < 정규길이; Loop_INDEX++) papa.직렬쓰기(정규[Loop_INDEX]); 단말.Tuhia("  "); 단말.수(roa_uara[kōnae_ūnga]); 단말.Tuhia("paita_uara(주기억 Kōnae)\n"); return 0; }
        if (FIND_whaiaronga(정규길이) < 0) return -2;
        for (int 뒷값 = 1; 뒷값 < 16; 뒷값++) if (whaiaronga_roa[뒷값] > 0) {
            int Start_tūranga = tāurunga_Start(whaiaronga_ingoa, 뒷값 * 64, whaiaronga_roa[뒷값]); if (Start_tūranga < 0) continue;
            for (int Loop_INDEX = Start_tūranga; Loop_INDEX < whaiaronga_roa[뒷값]; Loop_INDEX++) papa.직렬쓰기(whaiaronga_ingoa[뒷값 * 64 + Loop_INDEX]); 단말.Tuhia("/\n");
        }
        for (int kōnae_INDEX = 0; kōnae_INDEX < kōnae_COUNT; kōnae_INDEX++) if (이름길이[kōnae_INDEX] > 0) {
            int Start_tūranga = tāurunga_Start(Ingoa, kōnae_INDEX * 64, 이름길이[kōnae_INDEX]); if (Start_tūranga < 0) continue;
            for (int Loop_INDEX = Start_tūranga; Loop_INDEX < 이름길이[kōnae_INDEX]; Loop_INDEX++) papa.직렬쓰기(Ingoa[kōnae_INDEX * 64 + Loop_INDEX]);
            단말.Tuhia("  "); 단말.수(roa_uara[kōnae_INDEX]); 단말.Tuhia("paita_uara(주기억 Kōnae)\n");
        }
        return 0;
    }
}
