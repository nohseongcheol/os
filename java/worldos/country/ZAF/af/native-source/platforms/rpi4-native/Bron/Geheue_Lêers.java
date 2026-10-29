// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** RAM Lêer 64개, 파일당 16384바이트, 서술자 16개. 모든 data/정책은 Java에 있다.
 * 호출 도중 양보하지 않으므로 현재의 단일 코어 협력식 작업 사이에서 원자적이다.
 * 디스크 저장이나 POSIX 전체 구현을 뜻하지 않는다. 음수 반환은 Fout 번호다.
 */
public final class Geheue_Lêers {
    static final int lêer_COUNT = 64;
    static int[] Naam = new int[lêer_COUNT * 64];
    static int[] 이름길이 = new int[lêer_COUNT];
    // Pack four bytes in each Java int, preserving the old content heap budget.
    static int[] Inhoud_VALUE = new int[lêer_COUNT * 4096];
    static int[] lengte_VALUE = new int[lêer_COUNT];
    static int[] Naslaan_COUNT = new int[lêer_COUNT];
    static int[] 사용 = new int[16];
    static int[] teiken = new int[16];
    static int[] Posisie = new int[16];
    static int[] metode_MODE = new int[16];
    static int[] Pad = new int[64];
    static int pad_lengte;

    public static int 파일한도() { return lêer_COUNT; }
    static int 자료읽기(int Lêer, int plaas_INDEX) { return (Inhoud_VALUE[Lêer * 4096 + plaas_INDEX / 4] >>> ((plaas_INDEX & 3) * 8)) & 255; }
    static void skryf_data(int Lêer, int plaas_INDEX, int VALUE) {
        int gleuf_inskrywing = Lêer * 4096 + plaas_INDEX / 4, skuif_VALUE = (plaas_INDEX & 3) * 8;
        Inhoud_VALUE[gleuf_inskrywing] = (Inhoud_VALUE[gleuf_inskrywing] & ~(255 << skuif_VALUE)) | ((VALUE & 255) << skuif_VALUE);
    }

    public static int pad_BEGIN(int Grootte) {
        pad_lengte = 0;
        if (Grootte < 1 || Grootte > 63) return -36;
        pad_lengte = Grootte;
        for (int lus_INDEX = 0; lus_INDEX < Grootte; lus_INDEX++) Pad[lus_INDEX] = 0;
        return 0;
    }
    public static int pad_greep(int INDEX, int VALUE) {
        if (INDEX < 0 || INDEX >= pad_lengte || VALUE < 1 || VALUE > 255) return -22;
        Pad[INDEX] = VALUE; return 0;
    }
    static int FIND_inskrywing() {
        for (int lêer_INDEX = 0; lêer_INDEX < lêer_COUNT; lêer_INDEX++) if (이름길이[lêer_INDEX] > 0 && 이름길이[lêer_INDEX] == 정규길이 && 접두(Naam, lêer_INDEX * 64, 이름길이[lêer_INDEX], 정규, 정규길이)) return lêer_INDEX;
        return -1;
    }
    public static int skep(int 플래그) {
        if (pad_lengte == 0 || (플래그 & ~0x6c3) != 0 || (플래그 & 3) == 3) return -22;
        for (int lus_INDEX = 0; lus_INDEX < pad_lengte; lus_INDEX++) if (Pad[lus_INDEX] == 0) return -22;
        if ((플래그 & 0x200) != 0 && (플래그 & 3) == 0) return -22;
        int maatreël = normaliseer_VALUE(); if (maatreël < 0) return maatreël;
        if (FIND_gids(정규길이) >= 0) return -21;
        maatreël = 부모확인(); if (maatreël < 0) return maatreël;
        int Lêer = FIND_inskrywing();
        if (Lêer >= 0 && (플래그 & 0xc0) == 0xc0) return -17;
        if (Lêer < 0 && (플래그 & 0x40) == 0) return -2;
        int 서술자 = -1;
        for (int lus_INDEX = 0; lus_INDEX < 16; lus_INDEX++) if (사용[lus_INDEX] == 0) { 서술자 = lus_INDEX; break; }
        if (서술자 < 0) return -24;
        if (Lêer < 0) {
            for (int lus_INDEX = 0; lus_INDEX < lêer_COUNT; lus_INDEX++) if (이름길이[lus_INDEX] == 0 && Naslaan_COUNT[lus_INDEX] == 0) { Lêer = lus_INDEX; break; }
            if (Lêer < 0) return -28;
            이름길이[Lêer] = 정규길이;
            for (int lus_INDEX = 0; lus_INDEX < 정규길이; lus_INDEX++) Naam[Lêer * 64 + lus_INDEX] = 정규[lus_INDEX];
            lengte_VALUE[Lêer] = 0;
        }
        if ((플래그 & 0x200) != 0) lengte_VALUE[Lêer] = 0;
        사용[서술자] = 1; teiken[서술자] = Lêer; Posisie[서술자] = 0; metode_MODE[서술자] = 플래그;
        Naslaan_COUNT[Lêer]++;
        return 서술자 + 3;
    }
    static int verifieer(int 서술자) {
        return 서술자 >= 3 && 서술자 < 19 && 사용[서술자 - 3] != 0 ? 서술자 - 3 : -1;
    }
    public static int Lees(int 서술자) {
        int gleuf_inskrywing = verifieer(서술자);
        if (gleuf_inskrywing < 0 || (metode_MODE[gleuf_inskrywing] & 3) == 1) return -9;
        int Lêer = teiken[gleuf_inskrywing];
        if (Posisie[gleuf_inskrywing] >= lengte_VALUE[Lêer]) return 256; // EOF와 werklik_data 0x00..0xff 구별
        return 자료읽기(Lêer, Posisie[gleuf_inskrywing]++);
    }
    public static int Skryf(int 서술자, int VALUE) {
        int gleuf_inskrywing = verifieer(서술자);
        if (gleuf_inskrywing < 0 || (metode_MODE[gleuf_inskrywing] & 3) == 0) return -9;
        int Lêer = teiken[gleuf_inskrywing];
        if ((metode_MODE[gleuf_inskrywing] & 0x400) != 0) Posisie[gleuf_inskrywing] = lengte_VALUE[Lêer];
        if (Posisie[gleuf_inskrywing] >= 16384) return -28;
        while (lengte_VALUE[Lêer] < Posisie[gleuf_inskrywing]) skryf_data(Lêer, lengte_VALUE[Lêer]++, 0);
        skryf_data(Lêer, Posisie[gleuf_inskrywing]++, VALUE);
        if (lengte_VALUE[Lêer] < Posisie[gleuf_inskrywing]) lengte_VALUE[Lêer] = Posisie[gleuf_inskrywing];
        return 1;
    }
    public static int soek_plaas(int 서술자, int 거리, int Project_wortel) {
        int gleuf_inskrywing = verifieer(서술자);
        if (gleuf_inskrywing < 0) return -9;
        if (Project_wortel < 0 || Project_wortel > 2 || 거리 < -16384 || 거리 > 16384) return -22;
        int 새위치 = 거리 + (Project_wortel == 0 ? 0 : Project_wortel == 1 ? Posisie[gleuf_inskrywing] : lengte_VALUE[teiken[gleuf_inskrywing]]);
        if (새위치 < 0 || 새위치 > 16384) return -22;
        Posisie[gleuf_inskrywing] = 새위치; return 새위치;
    }
    public static int Sluit(int 서술자) {
        int gleuf_inskrywing = verifieer(서술자);
        if (gleuf_inskrywing < 0) return -9;
        Naslaan_COUNT[teiken[gleuf_inskrywing]]--; 사용[gleuf_inskrywing] = 0; return 0;
    }
    public static int Grootte(int 서술자) {
        int gleuf_inskrywing = verifieer(서술자); return gleuf_inskrywing < 0 ? -9 : lengte_VALUE[teiken[gleuf_inskrywing]];
    }
    public static int stel_lengte(int 서술자, int Grootte) {
        int gleuf_inskrywing = verifieer(서술자);
        if (gleuf_inskrywing < 0 || (metode_MODE[gleuf_inskrywing] & 3) == 0) return -9;
        if (Grootte < 0 || Grootte > 16384) return -22;
        int Lêer = teiken[gleuf_inskrywing];
        while (lengte_VALUE[Lêer] < Grootte) skryf_data(Lêer, lengte_VALUE[Lêer]++, 0);
        lengte_VALUE[Lêer] = Grootte; return 0;
    }
    public static int vee_uit_inskrywing() {
        if (pad_lengte == 0) return -22;
        int maatreël = normaliseer_VALUE(); if (maatreël < 0) return maatreël;
        if (FIND_gids(정규길이) >= 0) return -21;
        maatreël = 부모확인(); if (maatreël < 0) return maatreël;
        int Lêer = FIND_inskrywing();
        if (Lêer < 0) return -2;
        이름길이[Lêer] = 0; return 0; // 열려 있는 파일은 마지막 close까지 유지
    }
    static void inskrywing_Lys() {
        pad_BEGIN(1); pad_greep(0, '.'); 경로목록();
    }
    public static int 공개이름길이(int INDEX) {
        if (INDEX < 0 || INDEX >= lêer_COUNT || 이름길이[INDEX] == 0) return 0;
        for (int lus_INDEX = 0; lus_INDEX < 이름길이[INDEX]; lus_INDEX++) if (Naam[INDEX * 64 + lus_INDEX] == '/') return 0;
        return 이름길이[INDEX];
    }
    public static int 공개이름바이트(int INDEX, int plaas_INDEX) {
        return INDEX >= 0 && INDEX < lêer_COUNT && plaas_INDEX >= 0 && plaas_INDEX < 이름길이[INDEX] ? Naam[INDEX * 64 + plaas_INDEX] : -22;
    }
    public static int 공개파일크기(int INDEX) { return INDEX >= 0 && INDEX < lêer_COUNT ? lengte_VALUE[INDEX] : -22; }
    static int[] 정규 = new int[64], 현재 = new int[64], gids_naam = new int[16 * 64], gids_lengte = new int[16];
    static int 정규길이, 현재길이;
    static boolean 접두(int[] 이름들, int Loop, int pad_VALUE, int[] voor_VALUE, int reëlspasiëring_pad) {
        if (pad_VALUE < reëlspasiëring_pad) return false;
        for (int lus_INDEX = 0; lus_INDEX < reëlspasiëring_pad; lus_INDEX++) if (이름들[Loop + lus_INDEX] != voor_VALUE[lus_INDEX]) return false;
        return true;
    }
    static int normaliseer_VALUE() {
        if (pad_lengte == 0) return -22;
        정규길이 = Pad[0] == '/' ? 0 : 현재길이;
        for (int lus_INDEX = 0; lus_INDEX < 정규길이; lus_INDEX++) 정규[lus_INDEX] = 현재[lus_INDEX];
        int 읽는자리 = 0;
        while (읽는자리 < pad_lengte) {
            while (읽는자리 < pad_lengte && Pad[읽는자리] == '/') 읽는자리++;
            int BEGIN_plaas = 읽는자리; while (읽는자리 < pad_lengte && Pad[읽는자리] != '/') { if (Pad[읽는자리] == 0) return -22; 읽는자리++; }
            int inskrywing_COUNT = 읽는자리 - BEGIN_plaas; if (inskrywing_COUNT == 0 || inskrywing_COUNT == 1 && Pad[BEGIN_plaas] == '.') continue;
            if (inskrywing_COUNT == 2 && Pad[BEGIN_plaas] == '.' && Pad[BEGIN_plaas + 1] == '.') {
                while (정규길이 > 0 && 정규[정규길이 - 1] != '/') 정규길이--;
                if (정규길이 > 0) 정규길이--;
                continue;
            }
            if (정규길이 + inskrywing_COUNT + (정규길이 == 0 ? 0 : 1) > 63) return -36;
            if (정규길이 > 0) 정규[정규길이++] = '/';
            for (int lus_INDEX = BEGIN_plaas; lus_INDEX < 읽는자리; lus_INDEX++) 정규[정규길이++] = Pad[lus_INDEX];
        }
        return 0;
    }
    static int FIND_gids(int inskrywing_COUNT) {
        if (inskrywing_COUNT == 0) return 0;
        for (int lus_INDEX = 1; lus_INDEX < 16; lus_INDEX++) if (gids_lengte[lus_INDEX] == inskrywing_COUNT && 접두(gids_naam, lus_INDEX * 64, inskrywing_COUNT, 정규, inskrywing_COUNT)) return lus_INDEX;
        return -1;
    }
    static int 부모확인() {
        int inskrywing_COUNT = 정규길이; while (inskrywing_COUNT > 0 && 정규[inskrywing_COUNT - 1] != '/') inskrywing_COUNT--;
        return FIND_gids(inskrywing_COUNT == 0 ? 0 : inskrywing_COUNT - 1) < 0 ? -2 : 0;
    }
    public static int Skep_gids() {
        int 처리값 = normaliseer_VALUE(); if (처리값 < 0) return 처리값;
        if (FIND_gids(정규길이) >= 0 || FIND_inskrywing() >= 0) return -17;
        처리값 = 부모확인(); if (처리값 < 0) return 처리값;
        for (int lus_INDEX = 1; lus_INDEX < 16; lus_INDEX++) if (gids_lengte[lus_INDEX] == 0) {
            gids_lengte[lus_INDEX] = 정규길이; for (int binnebind_plaas = 0; binnebind_plaas < 정규길이; binnebind_plaas++) gids_naam[lus_INDEX * 64 + binnebind_plaas] = 정규[binnebind_plaas]; return 0;
        }
        return -28;
    }
    public static int 항목종류() {
        int 처리값 = normaliseer_VALUE(); if (처리값 < 0) return 처리값;
        if (FIND_gids(정규길이) >= 0) return 2;
        return FIND_inskrywing() >= 0 ? 1 : 0;
    }
    public static int verander_gids() {
        int 처리값 = normaliseer_VALUE(); if (처리값 < 0) return 처리값;
        if (FIND_gids(정규길이) < 0) return -2;
        현재길이 = 정규길이; for (int lus_INDEX = 0; lus_INDEX < 현재길이; lus_INDEX++) 현재[lus_INDEX] = 정규[lus_INDEX]; return 0;
    }
    public static int verwyder_gids() {
        int 처리값 = normaliseer_VALUE(); if (처리값 < 0) return 처리값;
        int 폴더번호 = FIND_gids(정규길이); if (폴더번호 < 0) return -2; if (폴더번호 == 0) return -16;
        if (현재길이 == 정규길이 && 접두(현재, 0, 현재길이, 정규, 정규길이)) return -16;
        for (int lus_INDEX = 0; lus_INDEX < lêer_COUNT; lus_INDEX++) {
            if (이름길이[lus_INDEX] > 정규길이 && 접두(Naam, lus_INDEX * 64, 이름길이[lus_INDEX], 정규, 정규길이) && Naam[lus_INDEX * 64 + 정규길이] == '/') return -39;
        }
        for (int lus_INDEX = 0; lus_INDEX < 16; lus_INDEX++) {
            if (gids_lengte[lus_INDEX] > 정규길이 && 접두(gids_naam, lus_INDEX * 64, gids_lengte[lus_INDEX], 정규, 정규길이) && gids_naam[lus_INDEX * 64 + 정규길이] == '/') return -39;
        }
        gids_lengte[폴더번호] = 0; return 0;
    }
    public static int 이름바꾸기(int 원본번호) {
        if (원본번호 < 0 || 원본번호 >= lêer_COUNT || 이름길이[원본번호] == 0) return -2;
        int 처리값 = normaliseer_VALUE(); if (처리값 < 0) return 처리값;
        if (FIND_gids(정규길이) >= 0) return -21;
        처리값 = 부모확인(); if (처리값 < 0) return 처리값;
        int 이전값 = FIND_inskrywing(); if (이전값 == 원본번호) return 0;
        if (이전값 >= 0) 이름길이[이전값] = 0;
        이름길이[원본번호] = 정규길이; for (int lus_INDEX = 0; lus_INDEX < 정규길이; lus_INDEX++) Naam[원본번호 * 64 + lus_INDEX] = 정규[lus_INDEX]; return 0;
    }
    static int inskrywing_BEGIN(int[] data_ARRAY, int 시작점, int inskrywing_COUNT) {
        if (!접두(data_ARRAY, 시작점, inskrywing_COUNT, 정규, 정규길이)) return -1;
        int BEGIN_plaas = 정규길이;
        if (BEGIN_plaas > 0) { if (inskrywing_COUNT <= BEGIN_plaas || data_ARRAY[시작점 + BEGIN_plaas] != '/') return -1; BEGIN_plaas++; }
        if (inskrywing_COUNT <= BEGIN_plaas) return -1;
        for (int lus_INDEX = BEGIN_plaas; lus_INDEX < inskrywing_COUNT; lus_INDEX++) if (data_ARRAY[시작점 + lus_INDEX] == '/') return -1;
        return BEGIN_plaas;
    }
    static void 현재쓰기() { 단말.문자('/'); for (int lus_INDEX = 0; lus_INDEX < 현재길이; lus_INDEX++) bord.직렬쓰기(현재[lus_INDEX]); }
    static int 경로목록() {
        int 처리값 = normaliseer_VALUE(); if (처리값 < 0) return 처리값;
        int lêer_teiken = FIND_inskrywing();
        if (lêer_teiken >= 0) { for (int lus_INDEX = 0; lus_INDEX < 정규길이; lus_INDEX++) bord.직렬쓰기(정규[lus_INDEX]); 단말.Skryf("  "); 단말.수(lengte_VALUE[lêer_teiken]); 단말.Skryf("greep_VALUE(주기억 Lêer)\n"); return 0; }
        if (FIND_gids(정규길이) < 0) return -2;
        for (int 뒷값 = 1; 뒷값 < 16; 뒷값++) if (gids_lengte[뒷값] > 0) {
            int BEGIN_plaas = inskrywing_BEGIN(gids_naam, 뒷값 * 64, gids_lengte[뒷값]); if (BEGIN_plaas < 0) continue;
            for (int lus_INDEX = BEGIN_plaas; lus_INDEX < gids_lengte[뒷값]; lus_INDEX++) bord.직렬쓰기(gids_naam[뒷값 * 64 + lus_INDEX]); 단말.Skryf("/\n");
        }
        for (int lêer_INDEX = 0; lêer_INDEX < lêer_COUNT; lêer_INDEX++) if (이름길이[lêer_INDEX] > 0) {
            int BEGIN_plaas = inskrywing_BEGIN(Naam, lêer_INDEX * 64, 이름길이[lêer_INDEX]); if (BEGIN_plaas < 0) continue;
            for (int lus_INDEX = BEGIN_plaas; lus_INDEX < 이름길이[lêer_INDEX]; lus_INDEX++) bord.직렬쓰기(Naam[lêer_INDEX * 64 + lus_INDEX]);
            단말.Skryf("  "); 단말.수(lengte_VALUE[lêer_INDEX]); 단말.Skryf("greep_VALUE(주기억 Lêer)\n");
        }
        return 0;
    }
}
