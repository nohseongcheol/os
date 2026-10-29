// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** RAM Fayl 64개, 파일당 16384바이트, 서술자 16개. 모든 ma_lumotlar/정책은 Java에 있다.
 * 호출 도중 양보하지 않으므로 현재의 단일 코어 협력식 작업 사이에서 원자적이다.
 * 디스크 저장이나 POSIX 전체 구현을 뜻하지 않는다. 음수 반환은 Xato 번호다.
 */
public final class Xotira_Fayllar {
    static final int fayl_COUNT = 64;
    static int[] Nomi = new int[fayl_COUNT * 64];
    static int[] 이름길이 = new int[fayl_COUNT];
    // Pack four bytes in each Java int, preserving the old content heap budget.
    static int[] tarkib_VALUE = new int[fayl_COUNT * 4096];
    static int[] uzunlik_VALUE = new int[fayl_COUNT];
    static int[] Ma_lumotnomalar_COUNT = new int[fayl_COUNT];
    static int[] 사용 = new int[16];
    static int[] nishon = new int[16];
    static int[] Holati = new int[16];
    static int[] uslub_MODE = new int[16];
    static int[] yo_l = new int[64];
    static int yo_l_uzunlik;

    public static int 파일한도() { return fayl_COUNT; }
    static int 자료읽기(int Fayl, int holat_INDEX) { return (tarkib_VALUE[Fayl * 4096 + holat_INDEX / 4] >>> ((holat_INDEX & 3) * 8)) & 255; }
    static void yozmoq_ma_lumotlar(int Fayl, int holat_INDEX, int VALUE) {
        int in_kiritish = Fayl * 4096 + holat_INDEX / 4, ko_chirmoq_VALUE = (holat_INDEX & 3) * 8;
        tarkib_VALUE[in_kiritish] = (tarkib_VALUE[in_kiritish] & ~(255 << ko_chirmoq_VALUE)) | ((VALUE & 255) << ko_chirmoq_VALUE);
    }

    public static int yo_l_Start(int Hajmi) {
        yo_l_uzunlik = 0;
        if (Hajmi < 1 || Hajmi > 63) return -36;
        yo_l_uzunlik = Hajmi;
        for (int Loop_INDEX = 0; Loop_INDEX < Hajmi; Loop_INDEX++) yo_l[Loop_INDEX] = 0;
        return 0;
    }
    public static int yo_l_bayt(int INDEX, int VALUE) {
        if (INDEX < 0 || INDEX >= yo_l_uzunlik || VALUE < 1 || VALUE > 255) return -22;
        yo_l[INDEX] = VALUE; return 0;
    }
    static int FIND_kiritish() {
        for (int fayl_INDEX = 0; fayl_INDEX < fayl_COUNT; fayl_INDEX++) if (이름길이[fayl_INDEX] > 0 && 이름길이[fayl_INDEX] == 정규길이 && 접두(Nomi, fayl_INDEX * 64, 이름길이[fayl_INDEX], 정규, 정규길이)) return fayl_INDEX;
        return -1;
    }
    public static int Ochish(int 플래그) {
        if (yo_l_uzunlik == 0 || (플래그 & ~0x6c3) != 0 || (플래그 & 3) == 3) return -22;
        for (int Loop_INDEX = 0; Loop_INDEX < yo_l_uzunlik; Loop_INDEX++) if (yo_l[Loop_INDEX] == 0) return -22;
        if ((플래그 & 0x200) != 0 && (플래그 & 3) == 0) return -22;
        int o_lchov = normallashtirmoq_VALUE(); if (o_lchov < 0) return o_lchov;
        if (FIND_katalog(정규길이) >= 0) return -21;
        o_lchov = 부모확인(); if (o_lchov < 0) return o_lchov;
        int Fayl = FIND_kiritish();
        if (Fayl >= 0 && (플래그 & 0xc0) == 0xc0) return -17;
        if (Fayl < 0 && (플래그 & 0x40) == 0) return -2;
        int 서술자 = -1;
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (사용[Loop_INDEX] == 0) { 서술자 = Loop_INDEX; break; }
        if (서술자 < 0) return -24;
        if (Fayl < 0) {
            for (int Loop_INDEX = 0; Loop_INDEX < fayl_COUNT; Loop_INDEX++) if (이름길이[Loop_INDEX] == 0 && Ma_lumotnomalar_COUNT[Loop_INDEX] == 0) { Fayl = Loop_INDEX; break; }
            if (Fayl < 0) return -28;
            이름길이[Fayl] = 정규길이;
            for (int Loop_INDEX = 0; Loop_INDEX < 정규길이; Loop_INDEX++) Nomi[Fayl * 64 + Loop_INDEX] = 정규[Loop_INDEX];
            uzunlik_VALUE[Fayl] = 0;
        }
        if ((플래그 & 0x200) != 0) uzunlik_VALUE[Fayl] = 0;
        사용[서술자] = 1; nishon[서술자] = Fayl; Holati[서술자] = 0; uslub_MODE[서술자] = 플래그;
        Ma_lumotnomalar_COUNT[Fayl]++;
        return 서술자 + 3;
    }
    static int tasdiqlamoq(int 서술자) {
        return 서술자 >= 3 && 서술자 < 19 && 사용[서술자 - 3] != 0 ? 서술자 - 3 : -1;
    }
    public static int Oʻqish(int 서술자) {
        int in_kiritish = tasdiqlamoq(서술자);
        if (in_kiritish < 0 || (uslub_MODE[in_kiritish] & 3) == 1) return -9;
        int Fayl = nishon[in_kiritish];
        if (Holati[in_kiritish] >= uzunlik_VALUE[Fayl]) return 256; // EOF와 real_ma_lumotlar 0x00..0xff 구별
        return 자료읽기(Fayl, Holati[in_kiritish]++);
    }
    public static int Yozish(int 서술자, int VALUE) {
        int in_kiritish = tasdiqlamoq(서술자);
        if (in_kiritish < 0 || (uslub_MODE[in_kiritish] & 3) == 0) return -9;
        int Fayl = nishon[in_kiritish];
        if ((uslub_MODE[in_kiritish] & 0x400) != 0) Holati[in_kiritish] = uzunlik_VALUE[Fayl];
        if (Holati[in_kiritish] >= 16384) return -28;
        while (uzunlik_VALUE[Fayl] < Holati[in_kiritish]) yozmoq_ma_lumotlar(Fayl, uzunlik_VALUE[Fayl]++, 0);
        yozmoq_ma_lumotlar(Fayl, Holati[in_kiritish]++, VALUE);
        if (uzunlik_VALUE[Fayl] < Holati[in_kiritish]) uzunlik_VALUE[Fayl] = Holati[in_kiritish];
        return 1;
    }
    public static int izlamoq_holat(int 서술자, int 거리, int Project_ildiz) {
        int in_kiritish = tasdiqlamoq(서술자);
        if (in_kiritish < 0) return -9;
        if (Project_ildiz < 0 || Project_ildiz > 2 || 거리 < -16384 || 거리 > 16384) return -22;
        int 새위치 = 거리 + (Project_ildiz == 0 ? 0 : Project_ildiz == 1 ? Holati[in_kiritish] : uzunlik_VALUE[nishon[in_kiritish]]);
        if (새위치 < 0 || 새위치 > 16384) return -22;
        Holati[in_kiritish] = 새위치; return 새위치;
    }
    public static int Yopish(int 서술자) {
        int in_kiritish = tasdiqlamoq(서술자);
        if (in_kiritish < 0) return -9;
        Ma_lumotnomalar_COUNT[nishon[in_kiritish]]--; 사용[in_kiritish] = 0; return 0;
    }
    public static int Hajmi(int 서술자) {
        int in_kiritish = tasdiqlamoq(서술자); return in_kiritish < 0 ? -9 : uzunlik_VALUE[nishon[in_kiritish]];
    }
    public static int to_plam_uzunlik(int 서술자, int Hajmi) {
        int in_kiritish = tasdiqlamoq(서술자);
        if (in_kiritish < 0 || (uslub_MODE[in_kiritish] & 3) == 0) return -9;
        if (Hajmi < 0 || Hajmi > 16384) return -22;
        int Fayl = nishon[in_kiritish];
        while (uzunlik_VALUE[Fayl] < Hajmi) yozmoq_ma_lumotlar(Fayl, uzunlik_VALUE[Fayl]++, 0);
        uzunlik_VALUE[Fayl] = Hajmi; return 0;
    }
    public static int tozalash_kiritish() {
        if (yo_l_uzunlik == 0) return -22;
        int o_lchov = normallashtirmoq_VALUE(); if (o_lchov < 0) return o_lchov;
        if (FIND_katalog(정규길이) >= 0) return -21;
        o_lchov = 부모확인(); if (o_lchov < 0) return o_lchov;
        int Fayl = FIND_kiritish();
        if (Fayl < 0) return -2;
        이름길이[Fayl] = 0; return 0; // 열려 있는 파일은 마지막 close까지 유지
    }
    static void kiritish_Ro_yxat() {
        yo_l_Start(1); yo_l_bayt(0, '.'); 경로목록();
    }
    public static int 공개이름길이(int INDEX) {
        if (INDEX < 0 || INDEX >= fayl_COUNT || 이름길이[INDEX] == 0) return 0;
        for (int Loop_INDEX = 0; Loop_INDEX < 이름길이[INDEX]; Loop_INDEX++) if (Nomi[INDEX * 64 + Loop_INDEX] == '/') return 0;
        return 이름길이[INDEX];
    }
    public static int 공개이름바이트(int INDEX, int holat_INDEX) {
        return INDEX >= 0 && INDEX < fayl_COUNT && holat_INDEX >= 0 && holat_INDEX < 이름길이[INDEX] ? Nomi[INDEX * 64 + holat_INDEX] : -22;
    }
    public static int 공개파일크기(int INDEX) { return INDEX >= 0 && INDEX < fayl_COUNT ? uzunlik_VALUE[INDEX] : -22; }
    static int[] 정규 = new int[64], 현재 = new int[64], katalog_nom = new int[16 * 64], katalog_uzunlik = new int[16];
    static int 정규길이, 현재길이;
    static boolean 접두(int[] 이름들, int Bajarish, int yo_l_VALUE, int[] old_kamera_VALUE, int yetakchi_yo_l) {
        if (yo_l_VALUE < yetakchi_yo_l) return false;
        for (int Loop_INDEX = 0; Loop_INDEX < yetakchi_yo_l; Loop_INDEX++) if (이름들[Bajarish + Loop_INDEX] != old_kamera_VALUE[Loop_INDEX]) return false;
        return true;
    }
    static int normallashtirmoq_VALUE() {
        if (yo_l_uzunlik == 0) return -22;
        정규길이 = yo_l[0] == '/' ? 0 : 현재길이;
        for (int Loop_INDEX = 0; Loop_INDEX < 정규길이; Loop_INDEX++) 정규[Loop_INDEX] = 현재[Loop_INDEX];
        int 읽는자리 = 0;
        while (읽는자리 < yo_l_uzunlik) {
            while (읽는자리 < yo_l_uzunlik && yo_l[읽는자리] == '/') 읽는자리++;
            int Start_holat = 읽는자리; while (읽는자리 < yo_l_uzunlik && yo_l[읽는자리] != '/') { if (yo_l[읽는자리] == 0) return -22; 읽는자리++; }
            int kiritish_COUNT = 읽는자리 - Start_holat; if (kiritish_COUNT == 0 || kiritish_COUNT == 1 && yo_l[Start_holat] == '.') continue;
            if (kiritish_COUNT == 2 && yo_l[Start_holat] == '.' && yo_l[Start_holat + 1] == '.') {
                while (정규길이 > 0 && 정규[정규길이 - 1] != '/') 정규길이--;
                if (정규길이 > 0) 정규길이--;
                continue;
            }
            if (정규길이 + kiritish_COUNT + (정규길이 == 0 ? 0 : 1) > 63) return -36;
            if (정규길이 > 0) 정규[정규길이++] = '/';
            for (int Loop_INDEX = Start_holat; Loop_INDEX < 읽는자리; Loop_INDEX++) 정규[정규길이++] = yo_l[Loop_INDEX];
        }
        return 0;
    }
    static int FIND_katalog(int kiritish_COUNT) {
        if (kiritish_COUNT == 0) return 0;
        for (int Loop_INDEX = 1; Loop_INDEX < 16; Loop_INDEX++) if (katalog_uzunlik[Loop_INDEX] == kiritish_COUNT && 접두(katalog_nom, Loop_INDEX * 64, kiritish_COUNT, 정규, kiritish_COUNT)) return Loop_INDEX;
        return -1;
    }
    static int 부모확인() {
        int kiritish_COUNT = 정규길이; while (kiritish_COUNT > 0 && 정규[kiritish_COUNT - 1] != '/') kiritish_COUNT--;
        return FIND_katalog(kiritish_COUNT == 0 ? 0 : kiritish_COUNT - 1) < 0 ? -2 : 0;
    }
    public static int Yaratish_katalog() {
        int 처리값 = normallashtirmoq_VALUE(); if (처리값 < 0) return 처리값;
        if (FIND_katalog(정규길이) >= 0 || FIND_kiritish() >= 0) return -17;
        처리값 = 부모확인(); if (처리값 < 0) return 처리값;
        for (int Loop_INDEX = 1; Loop_INDEX < 16; Loop_INDEX++) if (katalog_uzunlik[Loop_INDEX] == 0) {
            katalog_uzunlik[Loop_INDEX] = 정규길이; for (int ichki_qo_shilish_holat = 0; ichki_qo_shilish_holat < 정규길이; ichki_qo_shilish_holat++) katalog_nom[Loop_INDEX * 64 + ichki_qo_shilish_holat] = 정규[ichki_qo_shilish_holat]; return 0;
        }
        return -28;
    }
    public static int 항목종류() {
        int 처리값 = normallashtirmoq_VALUE(); if (처리값 < 0) return 처리값;
        if (FIND_katalog(정규길이) >= 0) return 2;
        return FIND_kiritish() >= 0 ? 1 : 0;
    }
    public static int o_zgartirmoq_katalog() {
        int 처리값 = normallashtirmoq_VALUE(); if (처리값 < 0) return 처리값;
        if (FIND_katalog(정규길이) < 0) return -2;
        현재길이 = 정규길이; for (int Loop_INDEX = 0; Loop_INDEX < 현재길이; Loop_INDEX++) 현재[Loop_INDEX] = 정규[Loop_INDEX]; return 0;
    }
    public static int olib_tashlamoq_katalog() {
        int 처리값 = normallashtirmoq_VALUE(); if (처리값 < 0) return 처리값;
        int 폴더번호 = FIND_katalog(정규길이); if (폴더번호 < 0) return -2; if (폴더번호 == 0) return -16;
        if (현재길이 == 정규길이 && 접두(현재, 0, 현재길이, 정규, 정규길이)) return -16;
        for (int Loop_INDEX = 0; Loop_INDEX < fayl_COUNT; Loop_INDEX++) {
            if (이름길이[Loop_INDEX] > 정규길이 && 접두(Nomi, Loop_INDEX * 64, 이름길이[Loop_INDEX], 정규, 정규길이) && Nomi[Loop_INDEX * 64 + 정규길이] == '/') return -39;
        }
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) {
            if (katalog_uzunlik[Loop_INDEX] > 정규길이 && 접두(katalog_nom, Loop_INDEX * 64, katalog_uzunlik[Loop_INDEX], 정규, 정규길이) && katalog_nom[Loop_INDEX * 64 + 정규길이] == '/') return -39;
        }
        katalog_uzunlik[폴더번호] = 0; return 0;
    }
    public static int 이름바꾸기(int 원본번호) {
        if (원본번호 < 0 || 원본번호 >= fayl_COUNT || 이름길이[원본번호] == 0) return -2;
        int 처리값 = normallashtirmoq_VALUE(); if (처리값 < 0) return 처리값;
        if (FIND_katalog(정규길이) >= 0) return -21;
        처리값 = 부모확인(); if (처리값 < 0) return 처리값;
        int 이전값 = FIND_kiritish(); if (이전값 == 원본번호) return 0;
        if (이전값 >= 0) 이름길이[이전값] = 0;
        이름길이[원본번호] = 정규길이; for (int Loop_INDEX = 0; Loop_INDEX < 정규길이; Loop_INDEX++) Nomi[원본번호 * 64 + Loop_INDEX] = 정규[Loop_INDEX]; return 0;
    }
    static int kiritish_Start(int[] ma_lumotlar_ARRAY, int 시작점, int kiritish_COUNT) {
        if (!접두(ma_lumotlar_ARRAY, 시작점, kiritish_COUNT, 정규, 정규길이)) return -1;
        int Start_holat = 정규길이;
        if (Start_holat > 0) { if (kiritish_COUNT <= Start_holat || ma_lumotlar_ARRAY[시작점 + Start_holat] != '/') return -1; Start_holat++; }
        if (kiritish_COUNT <= Start_holat) return -1;
        for (int Loop_INDEX = Start_holat; Loop_INDEX < kiritish_COUNT; Loop_INDEX++) if (ma_lumotlar_ARRAY[시작점 + Loop_INDEX] == '/') return -1;
        return Start_holat;
    }
    static void 현재쓰기() { 단말.문자('/'); for (int Loop_INDEX = 0; Loop_INDEX < 현재길이; Loop_INDEX++) yozuv_taxtasi.직렬쓰기(현재[Loop_INDEX]); }
    static int 경로목록() {
        int 처리값 = normallashtirmoq_VALUE(); if (처리값 < 0) return 처리값;
        int fayl_nishon = FIND_kiritish();
        if (fayl_nishon >= 0) { for (int Loop_INDEX = 0; Loop_INDEX < 정규길이; Loop_INDEX++) yozuv_taxtasi.직렬쓰기(정규[Loop_INDEX]); 단말.Yozish("  "); 단말.수(uzunlik_VALUE[fayl_nishon]); 단말.Yozish("bayt_VALUE(주기억 Fayl)\n"); return 0; }
        if (FIND_katalog(정규길이) < 0) return -2;
        for (int 뒷값 = 1; 뒷값 < 16; 뒷값++) if (katalog_uzunlik[뒷값] > 0) {
            int Start_holat = kiritish_Start(katalog_nom, 뒷값 * 64, katalog_uzunlik[뒷값]); if (Start_holat < 0) continue;
            for (int Loop_INDEX = Start_holat; Loop_INDEX < katalog_uzunlik[뒷값]; Loop_INDEX++) yozuv_taxtasi.직렬쓰기(katalog_nom[뒷값 * 64 + Loop_INDEX]); 단말.Yozish("/\n");
        }
        for (int fayl_INDEX = 0; fayl_INDEX < fayl_COUNT; fayl_INDEX++) if (이름길이[fayl_INDEX] > 0) {
            int Start_holat = kiritish_Start(Nomi, fayl_INDEX * 64, 이름길이[fayl_INDEX]); if (Start_holat < 0) continue;
            for (int Loop_INDEX = Start_holat; Loop_INDEX < 이름길이[fayl_INDEX]; Loop_INDEX++) yozuv_taxtasi.직렬쓰기(Nomi[fayl_INDEX * 64 + Loop_INDEX]);
            단말.Yozish("  "); 단말.수(uzunlik_VALUE[fayl_INDEX]); 단말.Yozish("bayt_VALUE(주기억 Fayl)\n");
        }
        return 0;
    }
}
