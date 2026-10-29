// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** RAM Fil 64개, 파일당 16384바이트, 서술자 16개. 모든 data/정책은 Java에 있다.
 * 호출 도중 양보하지 않으므로 현재의 단일 코어 협력식 작업 사이에서 원자적이다.
 * 디스크 저장이나 POSIX 전체 구현을 뜻하지 않는다. 음수 반환은 fejl 번호다.
 */
public final class Hukommelse_Filer {
    static final int fil_TÆL = 64;
    static int[] Navn = new int[fil_TÆL * 64];
    static int[] 이름길이 = new int[fil_TÆL];
    // Pack four bytes in each Java int, preserving the old content heap budget.
    static int[] Indhold_VÆRDI = new int[fil_TÆL * 4096];
    static int[] varighed_VÆRDI = new int[fil_TÆL];
    static int[] referere_TÆL = new int[fil_TÆL];
    static int[] brug_VÆRDI = new int[16];
    static int[] mål = new int[16];
    static int[] Placering = new int[16];
    static int[] metode_HYPPIGST = new int[16];
    static int[] Sti = new int[64];
    static int sti_varighed;

    public static int 파일한도() { return fil_TÆL; }
    static int 자료읽기(int Fil, int positionsindeks) { return (Indhold_VÆRDI[Fil * 4096 + positionsindeks / 4] >>> ((positionsindeks & 3) * 8)) & 255; }
    static void skrive_data(int Fil, int positionsindeks, int VÆRDI) {
        int udvidelsesstik_post = Fil * 4096 + positionsindeks / 4, flytte_VÆRDI_83b651b8 = (positionsindeks & 3) * 8;
        Indhold_VÆRDI[udvidelsesstik_post] = (Indhold_VÆRDI[udvidelsesstik_post] & ~(255 << flytte_VÆRDI_83b651b8)) | ((VÆRDI & 255) << flytte_VÆRDI_83b651b8);
    }

    public static int sti_START(int Størrelse) {
        sti_varighed = 0;
        if (Størrelse < 1 || Størrelse > 63) return -36;
        sti_varighed = Størrelse;
        for (int Loop_INDEKS = 0; Loop_INDEKS < Størrelse; Loop_INDEKS++) Sti[Loop_INDEKS] = 0;
        return 0;
    }
    public static int sti_byte(int INDEKS, int VÆRDI) {
        if (INDEKS < 0 || INDEKS >= sti_varighed || VÆRDI < 1 || VÆRDI > 255) return -22;
        Sti[INDEKS] = VÆRDI; return 0;
    }
    static int Søg_post() {
        for (int fil_INDEKS = 0; fil_INDEKS < fil_TÆL; fil_INDEKS++) if (이름길이[fil_INDEKS] > 0 && 이름길이[fil_INDEKS] == Canonical_varighed && 접두(Navn, fil_INDEKS * 64, 이름길이[fil_INDEKS], Canonical_VÆRDI, Canonical_varighed)) return fil_INDEKS;
        return -1;
    }
    public static int Åbn(int 플래그) {
        if (sti_varighed == 0 || (플래그 & ~0x6c3) != 0 || (플래그 & 3) == 3) return -22;
        for (int Loop_INDEKS = 0; Loop_INDEKS < sti_varighed; Loop_INDEKS++) if (Sti[Loop_INDEKS] == 0) return -22;
        if ((플래그 & 0x200) != 0 && (플래그 & 3) == 0) return -22;
        int KR = normalisere_VÆRDI(); if (KR < 0) return KR;
        if (Søg_mappe(Canonical_varighed) >= 0) return -21;
        KR = check_overordnet(); if (KR < 0) return KR;
        int Fil = Søg_post();
        if (Fil >= 0 && (플래그 & 0xc0) == 0xc0) return -17;
        if (Fil < 0 && (플래그 & 0x40) == 0) return -2;
        int 서술자 = -1;
        for (int Loop_INDEKS = 0; Loop_INDEKS < 16; Loop_INDEKS++) if (brug_VÆRDI[Loop_INDEKS] == 0) { 서술자 = Loop_INDEKS; break; }
        if (서술자 < 0) return -24;
        if (Fil < 0) {
            for (int Loop_INDEKS = 0; Loop_INDEKS < fil_TÆL; Loop_INDEKS++) if (이름길이[Loop_INDEKS] == 0 && referere_TÆL[Loop_INDEKS] == 0) { Fil = Loop_INDEKS; break; }
            if (Fil < 0) return -28;
            이름길이[Fil] = Canonical_varighed;
            for (int Loop_INDEKS = 0; Loop_INDEKS < Canonical_varighed; Loop_INDEKS++) Navn[Fil * 64 + Loop_INDEKS] = Canonical_VÆRDI[Loop_INDEKS];
            varighed_VÆRDI[Fil] = 0;
        }
        if ((플래그 & 0x200) != 0) varighed_VÆRDI[Fil] = 0;
        brug_VÆRDI[서술자] = 1; mål[서술자] = Fil; Placering[서술자] = 0; metode_HYPPIGST[서술자] = 플래그;
        referere_TÆL[Fil]++;
        return 서술자 + 3;
    }
    static int bekræfte(int 서술자) {
        return 서술자 >= 3 && 서술자 < 19 && brug_VÆRDI[서술자 - 3] != 0 ? 서술자 - 3 : -1;
    }
    public static int Læse(int 서술자) {
        int udvidelsesstik_post = bekræfte(서술자);
        if (udvidelsesstik_post < 0 || (metode_HYPPIGST[udvidelsesstik_post] & 3) == 1) return -9;
        int Fil = mål[udvidelsesstik_post];
        if (Placering[udvidelsesstik_post] >= varighed_VÆRDI[Fil]) return 256; // EOF와 faktisk_data 0x00..0xff 구별
        return 자료읽기(Fil, Placering[udvidelsesstik_post]++);
    }
    public static int Skrive(int 서술자, int VÆRDI) {
        int udvidelsesstik_post = bekræfte(서술자);
        if (udvidelsesstik_post < 0 || (metode_HYPPIGST[udvidelsesstik_post] & 3) == 0) return -9;
        int Fil = mål[udvidelsesstik_post];
        if ((metode_HYPPIGST[udvidelsesstik_post] & 0x400) != 0) Placering[udvidelsesstik_post] = varighed_VÆRDI[Fil];
        if (Placering[udvidelsesstik_post] >= 16384) return -28;
        while (varighed_VÆRDI[Fil] < Placering[udvidelsesstik_post]) skrive_data(Fil, varighed_VÆRDI[Fil]++, 0);
        skrive_data(Fil, Placering[udvidelsesstik_post]++, VÆRDI);
        if (varighed_VÆRDI[Fil] < Placering[udvidelsesstik_post]) varighed_VÆRDI[Fil] = Placering[udvidelsesstik_post];
        return 1;
    }
    public static int søge_placere(int 서술자, int 거리, int To_do_rod) {
        int udvidelsesstik_post = bekræfte(서술자);
        if (udvidelsesstik_post < 0) return -9;
        if (To_do_rod < 0 || To_do_rod > 2 || 거리 < -16384 || 거리 > 16384) return -22;
        int 새위치 = 거리 + (To_do_rod == 0 ? 0 : To_do_rod == 1 ? Placering[udvidelsesstik_post] : varighed_VÆRDI[mål[udvidelsesstik_post]]);
        if (새위치 < 0 || 새위치 > 16384) return -22;
        Placering[udvidelsesstik_post] = 새위치; return 새위치;
    }
    public static int Luk(int 서술자) {
        int udvidelsesstik_post = bekræfte(서술자);
        if (udvidelsesstik_post < 0) return -9;
        referere_TÆL[mål[udvidelsesstik_post]]--; brug_VÆRDI[udvidelsesstik_post] = 0; return 0;
    }
    public static int Størrelse(int 서술자) {
        int udvidelsesstik_post = bekræfte(서술자); return udvidelsesstik_post < 0 ? -9 : varighed_VÆRDI[mål[udvidelsesstik_post]];
    }
    public static int sæt_varighed(int 서술자, int Størrelse) {
        int udvidelsesstik_post = bekræfte(서술자);
        if (udvidelsesstik_post < 0 || (metode_HYPPIGST[udvidelsesstik_post] & 3) == 0) return -9;
        if (Størrelse < 0 || Størrelse > 16384) return -22;
        int Fil = mål[udvidelsesstik_post];
        while (varighed_VÆRDI[Fil] < Størrelse) skrive_data(Fil, varighed_VÆRDI[Fil]++, 0);
        varighed_VÆRDI[Fil] = Størrelse; return 0;
    }
    public static int slette_post() {
        if (sti_varighed == 0) return -22;
        int KR = normalisere_VÆRDI(); if (KR < 0) return KR;
        if (Søg_mappe(Canonical_varighed) >= 0) return -21;
        KR = check_overordnet(); if (KR < 0) return KR;
        int Fil = Søg_post();
        if (Fil < 0) return -2;
        이름길이[Fil] = 0; return 0; // 열려 있는 파일은 마지막 close까지 유지
    }
    static void post_Liste() {
        sti_START(1); sti_byte(0, '.'); 경로목록();
    }
    public static int 공개이름길이(int INDEKS) {
        if (INDEKS < 0 || INDEKS >= fil_TÆL || 이름길이[INDEKS] == 0) return 0;
        for (int Loop_INDEKS = 0; Loop_INDEKS < 이름길이[INDEKS]; Loop_INDEKS++) if (Navn[INDEKS * 64 + Loop_INDEKS] == '/') return 0;
        return 이름길이[INDEKS];
    }
    public static int 공개이름바이트(int INDEKS, int positionsindeks) {
        return INDEKS >= 0 && INDEKS < fil_TÆL && positionsindeks >= 0 && positionsindeks < 이름길이[INDEKS] ? Navn[INDEKS * 64 + positionsindeks] : -22;
    }
    public static int 공개파일크기(int INDEKS) { return INDEKS >= 0 && INDEKS < fil_TÆL ? varighed_VÆRDI[INDEKS] : -22; }
    static int[] Canonical_VÆRDI = new int[64], aktuel_vare = new int[64], mappe_navn = new int[16 * 64], mappe_varighed = new int[16];
    static int Canonical_varighed, aktuel_varighed;
    static boolean 접두(int[] 이름들, int Kør_2, int sti_VÆRDI, int[] frontvendt_VÆRDI, int skydning_sti) {
        if (sti_VÆRDI < skydning_sti) return false;
        for (int Loop_INDEKS = 0; Loop_INDEKS < skydning_sti; Loop_INDEKS++) if (이름들[Kør_2 + Loop_INDEKS] != frontvendt_VÆRDI[Loop_INDEKS]) return false;
        return true;
    }
    static int normalisere_VÆRDI() {
        if (sti_varighed == 0) return -22;
        Canonical_varighed = Sti[0] == '/' ? 0 : aktuel_varighed;
        for (int Loop_INDEKS = 0; Loop_INDEKS < Canonical_varighed; Loop_INDEKS++) Canonical_VÆRDI[Loop_INDEKS] = aktuel_vare[Loop_INDEKS];
        int 읽는자리 = 0;
        while (읽는자리 < sti_varighed) {
            while (읽는자리 < sti_varighed && Sti[읽는자리] == '/') 읽는자리++;
            int START_placere = 읽는자리; while (읽는자리 < sti_varighed && Sti[읽는자리] != '/') { if (Sti[읽는자리] == 0) return -22; 읽는자리++; }
            int post_TÆL_8f7753a1 = 읽는자리 - START_placere; if (post_TÆL_8f7753a1 == 0 || post_TÆL_8f7753a1 == 1 && Sti[START_placere] == '.') continue;
            if (post_TÆL_8f7753a1 == 2 && Sti[START_placere] == '.' && Sti[START_placere + 1] == '.') {
                while (Canonical_varighed > 0 && Canonical_VÆRDI[Canonical_varighed - 1] != '/') Canonical_varighed--;
                if (Canonical_varighed > 0) Canonical_varighed--;
                continue;
            }
            if (Canonical_varighed + post_TÆL_8f7753a1 + (Canonical_varighed == 0 ? 0 : 1) > 63) return -36;
            if (Canonical_varighed > 0) Canonical_VÆRDI[Canonical_varighed++] = '/';
            for (int Loop_INDEKS = START_placere; Loop_INDEKS < 읽는자리; Loop_INDEKS++) Canonical_VÆRDI[Canonical_varighed++] = Sti[Loop_INDEKS];
        }
        return 0;
    }
    static int Søg_mappe(int post_TÆL_8f7753a1) {
        if (post_TÆL_8f7753a1 == 0) return 0;
        for (int Loop_INDEKS = 1; Loop_INDEKS < 16; Loop_INDEKS++) if (mappe_varighed[Loop_INDEKS] == post_TÆL_8f7753a1 && 접두(mappe_navn, Loop_INDEKS * 64, post_TÆL_8f7753a1, Canonical_VÆRDI, post_TÆL_8f7753a1)) return Loop_INDEKS;
        return -1;
    }
    static int check_overordnet() {
        int post_TÆL_8f7753a1 = Canonical_varighed; while (post_TÆL_8f7753a1 > 0 && Canonical_VÆRDI[post_TÆL_8f7753a1 - 1] != '/') post_TÆL_8f7753a1--;
        return Søg_mappe(post_TÆL_8f7753a1 == 0 ? 0 : post_TÆL_8f7753a1 - 1) < 0 ? -2 : 0;
    }
    public static int åbne_mappe() {
        int 처리값 = normalisere_VÆRDI(); if (처리값 < 0) return 처리값;
        if (Søg_mappe(Canonical_varighed) >= 0 || Søg_post() >= 0) return -17;
        처리값 = check_overordnet(); if (처리값 < 0) return 처리값;
        for (int Loop_INDEKS = 1; Loop_INDEKS < 16; Loop_INDEKS++) if (mappe_varighed[Loop_INDEKS] == 0) {
            mappe_varighed[Loop_INDEKS] = Canonical_varighed; for (int indre_placere = 0; indre_placere < Canonical_varighed; indre_placere++) mappe_navn[Loop_INDEKS * 64 + indre_placere] = Canonical_VÆRDI[indre_placere]; return 0;
        }
        return -28;
    }
    public static int 항목종류() {
        int 처리값 = normalisere_VÆRDI(); if (처리값 < 0) return 처리값;
        if (Søg_mappe(Canonical_varighed) >= 0) return 2;
        return Søg_post() >= 0 ? 1 : 0;
    }
    public static int ændre_mappe() {
        int 처리값 = normalisere_VÆRDI(); if (처리값 < 0) return 처리값;
        if (Søg_mappe(Canonical_varighed) < 0) return -2;
        aktuel_varighed = Canonical_varighed; for (int Loop_INDEKS = 0; Loop_INDEKS < aktuel_varighed; Loop_INDEKS++) aktuel_vare[Loop_INDEKS] = Canonical_VÆRDI[Loop_INDEKS]; return 0;
    }
    public static int fjerne_mappe() {
        int 처리값 = normalisere_VÆRDI(); if (처리값 < 0) return 처리값;
        int mappe_tal = Søg_mappe(Canonical_varighed); if (mappe_tal < 0) return -2; if (mappe_tal == 0) return -16;
        if (aktuel_varighed == Canonical_varighed && 접두(aktuel_vare, 0, aktuel_varighed, Canonical_VÆRDI, Canonical_varighed)) return -16;
        for (int Loop_INDEKS = 0; Loop_INDEKS < fil_TÆL; Loop_INDEKS++) {
            if (이름길이[Loop_INDEKS] > Canonical_varighed && 접두(Navn, Loop_INDEKS * 64, 이름길이[Loop_INDEKS], Canonical_VÆRDI, Canonical_varighed) && Navn[Loop_INDEKS * 64 + Canonical_varighed] == '/') return -39;
        }
        for (int Loop_INDEKS = 0; Loop_INDEKS < 16; Loop_INDEKS++) {
            if (mappe_varighed[Loop_INDEKS] > Canonical_varighed && 접두(mappe_navn, Loop_INDEKS * 64, mappe_varighed[Loop_INDEKS], Canonical_VÆRDI, Canonical_varighed) && mappe_navn[Loop_INDEKS * 64 + Canonical_varighed] == '/') return -39;
        }
        mappe_varighed[mappe_tal] = 0; return 0;
    }
    public static int Omdøb_post(int 원본번호) {
        if (원본번호 < 0 || 원본번호 >= fil_TÆL || 이름길이[원본번호] == 0) return -2;
        int 처리값 = normalisere_VÆRDI(); if (처리값 < 0) return 처리값;
        if (Søg_mappe(Canonical_varighed) >= 0) return -21;
        처리값 = check_overordnet(); if (처리값 < 0) return 처리값;
        int Forrige_VÆRDI = Søg_post(); if (Forrige_VÆRDI == 원본번호) return 0;
        if (Forrige_VÆRDI >= 0) 이름길이[Forrige_VÆRDI] = 0;
        이름길이[원본번호] = Canonical_varighed; for (int Loop_INDEKS = 0; Loop_INDEKS < Canonical_varighed; Loop_INDEKS++) Navn[원본번호 * 64 + Loop_INDEKS] = Canonical_VÆRDI[Loop_INDEKS]; return 0;
    }
    static int post_START(int[] data_MATRIX, int 시작점, int post_TÆL_8f7753a1) {
        if (!접두(data_MATRIX, 시작점, post_TÆL_8f7753a1, Canonical_VÆRDI, Canonical_varighed)) return -1;
        int START_placere = Canonical_varighed;
        if (START_placere > 0) { if (post_TÆL_8f7753a1 <= START_placere || data_MATRIX[시작점 + START_placere] != '/') return -1; START_placere++; }
        if (post_TÆL_8f7753a1 <= START_placere) return -1;
        for (int Loop_INDEKS = START_placere; Loop_INDEKS < post_TÆL_8f7753a1; Loop_INDEKS++) if (data_MATRIX[시작점 + Loop_INDEKS] == '/') return -1;
        return START_placere;
    }
    static void aktuel_skrive() { 단말.문자('/'); for (int Loop_INDEKS = 0; Loop_INDEKS < aktuel_varighed; Loop_INDEKS++) Tavle.직렬쓰기(aktuel_vare[Loop_INDEKS]); }
    static int 경로목록() {
        int 처리값 = normalisere_VÆRDI(); if (처리값 < 0) return 처리값;
        int fil_mål = Søg_post();
        if (fil_mål >= 0) { for (int Loop_INDEKS = 0; Loop_INDEKS < Canonical_varighed; Loop_INDEKS++) Tavle.직렬쓰기(Canonical_VÆRDI[Loop_INDEKS]); 단말.Skrive("  "); 단말.tal(varighed_VÆRDI[fil_mål]); 단말.Skrive("byte_VÆRDI(주기억 Fil)\n"); return 0; }
        if (Søg_mappe(Canonical_varighed) < 0) return -2;
        for (int 뒷값 = 1; 뒷값 < 16; 뒷값++) if (mappe_varighed[뒷값] > 0) {
            int START_placere = post_START(mappe_navn, 뒷값 * 64, mappe_varighed[뒷값]); if (START_placere < 0) continue;
            for (int Loop_INDEKS = START_placere; Loop_INDEKS < mappe_varighed[뒷값]; Loop_INDEKS++) Tavle.직렬쓰기(mappe_navn[뒷값 * 64 + Loop_INDEKS]); 단말.Skrive("/\n");
        }
        for (int fil_INDEKS = 0; fil_INDEKS < fil_TÆL; fil_INDEKS++) if (이름길이[fil_INDEKS] > 0) {
            int START_placere = post_START(Navn, fil_INDEKS * 64, 이름길이[fil_INDEKS]); if (START_placere < 0) continue;
            for (int Loop_INDEKS = START_placere; Loop_INDEKS < 이름길이[fil_INDEKS]; Loop_INDEKS++) Tavle.직렬쓰기(Navn[fil_INDEKS * 64 + Loop_INDEKS]);
            단말.Skrive("  "); 단말.tal(varighed_VÆRDI[fil_INDEKS]); 단말.Skrive("byte_VÆRDI(주기억 Fil)\n");
        }
        return 0;
    }
}
