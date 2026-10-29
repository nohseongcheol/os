// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** RAM Faýl 64개, 파일당 16384바이트, 서술자 16개. 모든 maglumat/정책은 Java에 있다.
 * 호출 도중 양보하지 않으므로 현재의 단일 코어 협력식 작업 사이에서 원자적이다.
 * 디스크 저장이나 POSIX 전체 구현을 뜻하지 않는다. 음수 반환은 Hata 번호다.
 */
public final class ýat_Faýllar {
    static final int 파일수 = 64;
    static int[] Ad = new int[파일수 * 64];
    static int[] 이름길이 = new int[파일수];
    // Pack four bytes in each Java int, preserving the old content heap budget.
    static int[] Mazmun_baha = new int[파일수 * 4096];
    static int[] dowamlylyk_baha = new int[파일수];
    static int[] 참조수 = new int[파일수];
    static int[] 사용 = new int[16];
    static int[] niýet = new int[16];
    static int[] 위치 = new int[16];
    static int[] usul_reje = new int[16];
    static int[] Ýol = new int[64];
    static int ýol_dowamlylyk;

    public static int 파일한도() { return 파일수; }
    static int 자료읽기(int Faýl, int 자리) { return (Mazmun_baha[Faýl * 4096 + 자리 / 4] >>> ((자리 & 3) * 8)) & 255; }
    static void ýaz_maglumat(int Faýl, int 자리, int baha) {
        int ýer_girizmeklik = Faýl * 4096 + 자리 / 4, ýerini_üýtget_baha = (자리 & 3) * 8;
        Mazmun_baha[ýer_girizmeklik] = (Mazmun_baha[ýer_girizmeklik] & ~(255 << ýerini_üýtget_baha)) | ((baha & 255) << ýerini_üýtget_baha);
    }

    public static int ýol_başlat(int Ululyk) {
        ýol_dowamlylyk = 0;
        if (Ululyk < 1 || Ululyk > 63) return -36;
        ýol_dowamlylyk = Ululyk;
        for (int sikl_indeks = 0; sikl_indeks < Ululyk; sikl_indeks++) Ýol[sikl_indeks] = 0;
        return 0;
    }
    public static int ýol_baýt(int indeks, int baha) {
        if (indeks < 0 || indeks >= ýol_dowamlylyk || baha < 1 || baha > 255) return -22;
        Ýol[indeks] = baha; return 0;
    }
    static int tap_girizmeklik() {
        for (int faýl_indeks = 0; faýl_indeks < 파일수; faýl_indeks++) if (이름길이[faýl_indeks] > 0 && 이름길이[faýl_indeks] == 정규길이 && 접두(Ad, faýl_indeks * 64, 이름길이[faýl_indeks], 정규, 정규길이)) return faýl_indeks;
        return -1;
    }
    public static int Aç(int 플래그) {
        if (ýol_dowamlylyk == 0 || (플래그 & ~0x6c3) != 0 || (플래그 & 3) == 3) return -22;
        for (int sikl_indeks = 0; sikl_indeks < ýol_dowamlylyk; sikl_indeks++) if (Ýol[sikl_indeks] == 0) return -22;
        if ((플래그 & 0x200) != 0 && (플래그 & 3) == 0) return -22;
        int 결과 = adaty_ýagdaýa_getir_baha(); if (결과 < 0) return 결과;
        if (tap_katalog(정규길이) >= 0) return -21;
        결과 = 부모확인(); if (결과 < 0) return 결과;
        int Faýl = tap_girizmeklik();
        if (Faýl >= 0 && (플래그 & 0xc0) == 0xc0) return -17;
        if (Faýl < 0 && (플래그 & 0x40) == 0) return -2;
        int 서술자 = -1;
        for (int sikl_indeks = 0; sikl_indeks < 16; sikl_indeks++) if (사용[sikl_indeks] == 0) { 서술자 = sikl_indeks; break; }
        if (서술자 < 0) return -24;
        if (Faýl < 0) {
            for (int sikl_indeks = 0; sikl_indeks < 파일수; sikl_indeks++) if (이름길이[sikl_indeks] == 0 && 참조수[sikl_indeks] == 0) { Faýl = sikl_indeks; break; }
            if (Faýl < 0) return -28;
            이름길이[Faýl] = 정규길이;
            for (int sikl_indeks = 0; sikl_indeks < 정규길이; sikl_indeks++) Ad[Faýl * 64 + sikl_indeks] = 정규[sikl_indeks];
            dowamlylyk_baha[Faýl] = 0;
        }
        if ((플래그 & 0x200) != 0) dowamlylyk_baha[Faýl] = 0;
        사용[서술자] = 1; niýet[서술자] = Faýl; 위치[서술자] = 0; usul_reje[서술자] = 플래그;
        참조수[Faýl]++;
        return 서술자 + 3;
    }
    static int barla(int 서술자) {
        return 서술자 >= 3 && 서술자 < 19 && 사용[서술자 - 3] != 0 ? 서술자 - 3 : -1;
    }
    public static int Oka(int 서술자) {
        int ýer_girizmeklik = barla(서술자);
        if (ýer_girizmeklik < 0 || (usul_reje[ýer_girizmeklik] & 3) == 1) return -9;
        int Faýl = niýet[ýer_girizmeklik];
        if (위치[ýer_girizmeklik] >= dowamlylyk_baha[Faýl]) return 256; // EOF와 hakyky_maglumat 0x00..0xff 구별
        return 자료읽기(Faýl, 위치[ýer_girizmeklik]++);
    }
    public static int Ýaz(int 서술자, int baha) {
        int ýer_girizmeklik = barla(서술자);
        if (ýer_girizmeklik < 0 || (usul_reje[ýer_girizmeklik] & 3) == 0) return -9;
        int Faýl = niýet[ýer_girizmeklik];
        if ((usul_reje[ýer_girizmeklik] & 0x400) != 0) 위치[ýer_girizmeklik] = dowamlylyk_baha[Faýl];
        if (위치[ýer_girizmeklik] >= 16384) return -28;
        while (dowamlylyk_baha[Faýl] < 위치[ýer_girizmeklik]) ýaz_maglumat(Faýl, dowamlylyk_baha[Faýl]++, 0);
        ýaz_maglumat(Faýl, 위치[ýer_girizmeklik]++, baha);
        if (dowamlylyk_baha[Faýl] < 위치[ýer_girizmeklik]) dowamlylyk_baha[Faýl] = 위치[ýer_girizmeklik];
        return 1;
    }
    public static int 옮기기(int 서술자, int 거리, int 기준) {
        int ýer_girizmeklik = barla(서술자);
        if (ýer_girizmeklik < 0) return -9;
        if (기준 < 0 || 기준 > 2 || 거리 < -16384 || 거리 > 16384) return -22;
        int 새위치 = 거리 + (기준 == 0 ? 0 : 기준 == 1 ? 위치[ýer_girizmeklik] : dowamlylyk_baha[niýet[ýer_girizmeklik]]);
        if (새위치 < 0 || 새위치 > 16384) return -22;
        위치[ýer_girizmeklik] = 새위치; return 새위치;
    }
    public static int Ýap(int 서술자) {
        int ýer_girizmeklik = barla(서술자);
        if (ýer_girizmeklik < 0) return -9;
        참조수[niýet[ýer_girizmeklik]]--; 사용[ýer_girizmeklik] = 0; return 0;
    }
    public static int Ululyk(int 서술자) {
        int ýer_girizmeklik = barla(서술자); return ýer_girizmeklik < 0 ? -9 : dowamlylyk_baha[niýet[ýer_girizmeklik]];
    }
    public static int köplük_dowamlylyk(int 서술자, int Ululyk) {
        int ýer_girizmeklik = barla(서술자);
        if (ýer_girizmeklik < 0 || (usul_reje[ýer_girizmeklik] & 3) == 0) return -9;
        if (Ululyk < 0 || Ululyk > 16384) return -22;
        int Faýl = niýet[ýer_girizmeklik];
        while (dowamlylyk_baha[Faýl] < Ululyk) ýaz_maglumat(Faýl, dowamlylyk_baha[Faýl]++, 0);
        dowamlylyk_baha[Faýl] = Ululyk; return 0;
    }
    public static int 지우기() {
        if (ýol_dowamlylyk == 0) return -22;
        int 결과 = adaty_ýagdaýa_getir_baha(); if (결과 < 0) return 결과;
        if (tap_katalog(정규길이) >= 0) return -21;
        결과 = 부모확인(); if (결과 < 0) return 결과;
        int Faýl = tap_girizmeklik();
        if (Faýl < 0) return -2;
        이름길이[Faýl] = 0; return 0; // 열려 있는 파일은 마지막 close까지 유지
    }
    static void girizmeklik_Sanaw() {
        ýol_başlat(1); ýol_baýt(0, '.'); 경로목록();
    }
    public static int 공개이름길이(int indeks) {
        if (indeks < 0 || indeks >= 파일수 || 이름길이[indeks] == 0) return 0;
        for (int sikl_indeks = 0; sikl_indeks < 이름길이[indeks]; sikl_indeks++) if (Ad[indeks * 64 + sikl_indeks] == '/') return 0;
        return 이름길이[indeks];
    }
    public static int 공개이름바이트(int indeks, int 자리) {
        return indeks >= 0 && indeks < 파일수 && 자리 >= 0 && 자리 < 이름길이[indeks] ? Ad[indeks * 64 + 자리] : -22;
    }
    public static int 공개파일크기(int indeks) { return indeks >= 0 && indeks < 파일수 ? dowamlylyk_baha[indeks] : -22; }
    static int[] 정규 = new int[64], 현재 = new int[64], katalog_at = new int[16 * 64], katalog_dowamlylyk = new int[16];
    static int 정규길이, 현재길이;
    static boolean 접두(int[] 이름들, int Bitir, int ýol_baha, int[] 앞, int setirara_ýol) {
        if (ýol_baha < setirara_ýol) return false;
        for (int sikl_indeks = 0; sikl_indeks < setirara_ýol; sikl_indeks++) if (이름들[Bitir + sikl_indeks] != 앞[sikl_indeks]) return false;
        return true;
    }
    static int adaty_ýagdaýa_getir_baha() {
        if (ýol_dowamlylyk == 0) return -22;
        정규길이 = Ýol[0] == '/' ? 0 : 현재길이;
        for (int sikl_indeks = 0; sikl_indeks < 정규길이; sikl_indeks++) 정규[sikl_indeks] = 현재[sikl_indeks];
        int 읽는자리 = 0;
        while (읽는자리 < ýol_dowamlylyk) {
            while (읽는자리 < ýol_dowamlylyk && Ýol[읽는자리] == '/') 읽는자리++;
            int 시작자리 = 읽는자리; while (읽는자리 < ýol_dowamlylyk && Ýol[읽는자리] != '/') { if (Ýol[읽는자리] == 0) return -22; 읽는자리++; }
            int 항목수 = 읽는자리 - 시작자리; if (항목수 == 0 || 항목수 == 1 && Ýol[시작자리] == '.') continue;
            if (항목수 == 2 && Ýol[시작자리] == '.' && Ýol[시작자리 + 1] == '.') {
                while (정규길이 > 0 && 정규[정규길이 - 1] != '/') 정규길이--;
                if (정규길이 > 0) 정규길이--;
                continue;
            }
            if (정규길이 + 항목수 + (정규길이 == 0 ? 0 : 1) > 63) return -36;
            if (정규길이 > 0) 정규[정규길이++] = '/';
            for (int sikl_indeks = 시작자리; sikl_indeks < 읽는자리; sikl_indeks++) 정규[정규길이++] = Ýol[sikl_indeks];
        }
        return 0;
    }
    static int tap_katalog(int 항목수) {
        if (항목수 == 0) return 0;
        for (int sikl_indeks = 1; sikl_indeks < 16; sikl_indeks++) if (katalog_dowamlylyk[sikl_indeks] == 항목수 && 접두(katalog_at, sikl_indeks * 64, 항목수, 정규, 항목수)) return sikl_indeks;
        return -1;
    }
    static int 부모확인() {
        int 항목수 = 정규길이; while (항목수 > 0 && 정규[항목수 - 1] != '/') 항목수--;
        return tap_katalog(항목수 == 0 ? 0 : 항목수 - 1) < 0 ? -2 : 0;
    }
    public static int döretmek_katalog() {
        int 처리값 = adaty_ýagdaýa_getir_baha(); if (처리값 < 0) return 처리값;
        if (tap_katalog(정규길이) >= 0 || tap_girizmeklik() >= 0) return -17;
        처리값 = 부모확인(); if (처리값 < 0) return 처리값;
        for (int sikl_indeks = 1; sikl_indeks < 16; sikl_indeks++) if (katalog_dowamlylyk[sikl_indeks] == 0) {
            katalog_dowamlylyk[sikl_indeks] = 정규길이; for (int 안쪽자리 = 0; 안쪽자리 < 정규길이; 안쪽자리++) katalog_at[sikl_indeks * 64 + 안쪽자리] = 정규[안쪽자리]; return 0;
        }
        return -28;
    }
    public static int 항목종류() {
        int 처리값 = adaty_ýagdaýa_getir_baha(); if (처리값 < 0) return 처리값;
        if (tap_katalog(정규길이) >= 0) return 2;
        return tap_girizmeklik() >= 0 ? 1 : 0;
    }
    public static int üýtget_katalog() {
        int 처리값 = adaty_ýagdaýa_getir_baha(); if (처리값 < 0) return 처리값;
        if (tap_katalog(정규길이) < 0) return -2;
        현재길이 = 정규길이; for (int sikl_indeks = 0; sikl_indeks < 현재길이; sikl_indeks++) 현재[sikl_indeks] = 정규[sikl_indeks]; return 0;
    }
    public static int aýyr_katalog() {
        int 처리값 = adaty_ýagdaýa_getir_baha(); if (처리값 < 0) return 처리값;
        int 폴더번호 = tap_katalog(정규길이); if (폴더번호 < 0) return -2; if (폴더번호 == 0) return -16;
        if (현재길이 == 정규길이 && 접두(현재, 0, 현재길이, 정규, 정규길이)) return -16;
        for (int sikl_indeks = 0; sikl_indeks < 파일수; sikl_indeks++) {
            if (이름길이[sikl_indeks] > 정규길이 && 접두(Ad, sikl_indeks * 64, 이름길이[sikl_indeks], 정규, 정규길이) && Ad[sikl_indeks * 64 + 정규길이] == '/') return -39;
        }
        for (int sikl_indeks = 0; sikl_indeks < 16; sikl_indeks++) {
            if (katalog_dowamlylyk[sikl_indeks] > 정규길이 && 접두(katalog_at, sikl_indeks * 64, katalog_dowamlylyk[sikl_indeks], 정규, 정규길이) && katalog_at[sikl_indeks * 64 + 정규길이] == '/') return -39;
        }
        katalog_dowamlylyk[폴더번호] = 0; return 0;
    }
    public static int 이름바꾸기(int 원본번호) {
        if (원본번호 < 0 || 원본번호 >= 파일수 || 이름길이[원본번호] == 0) return -2;
        int 처리값 = adaty_ýagdaýa_getir_baha(); if (처리값 < 0) return 처리값;
        if (tap_katalog(정규길이) >= 0) return -21;
        처리값 = 부모확인(); if (처리값 < 0) return 처리값;
        int 이전값 = tap_girizmeklik(); if (이전값 == 원본번호) return 0;
        if (이전값 >= 0) 이름길이[이전값] = 0;
        이름길이[원본번호] = 정규길이; for (int sikl_indeks = 0; sikl_indeks < 정규길이; sikl_indeks++) Ad[원본번호 * 64 + sikl_indeks] = 정규[sikl_indeks]; return 0;
    }
    static int girizmeklik_başlat(int[] maglumat_ARRAY, int 시작점, int 항목수) {
        if (!접두(maglumat_ARRAY, 시작점, 항목수, 정규, 정규길이)) return -1;
        int 시작자리 = 정규길이;
        if (시작자리 > 0) { if (항목수 <= 시작자리 || maglumat_ARRAY[시작점 + 시작자리] != '/') return -1; 시작자리++; }
        if (항목수 <= 시작자리) return -1;
        for (int sikl_indeks = 시작자리; sikl_indeks < 항목수; sikl_indeks++) if (maglumat_ARRAY[시작점 + sikl_indeks] == '/') return -1;
        return 시작자리;
    }
    static void 현재쓰기() { 단말.문자('/'); for (int sikl_indeks = 0; sikl_indeks < 현재길이; sikl_indeks++) 보드.직렬쓰기(현재[sikl_indeks]); }
    static int 경로목록() {
        int 처리값 = adaty_ýagdaýa_getir_baha(); if (처리값 < 0) return 처리값;
        int faýl_niýet = tap_girizmeklik();
        if (faýl_niýet >= 0) { for (int sikl_indeks = 0; sikl_indeks < 정규길이; sikl_indeks++) 보드.직렬쓰기(정규[sikl_indeks]); 단말.Ýaz("  "); 단말.수(dowamlylyk_baha[faýl_niýet]); 단말.Ýaz("baýt_baha(주기억 Faýl)\n"); return 0; }
        if (tap_katalog(정규길이) < 0) return -2;
        for (int 뒷값 = 1; 뒷값 < 16; 뒷값++) if (katalog_dowamlylyk[뒷값] > 0) {
            int 시작자리 = girizmeklik_başlat(katalog_at, 뒷값 * 64, katalog_dowamlylyk[뒷값]); if (시작자리 < 0) continue;
            for (int sikl_indeks = 시작자리; sikl_indeks < katalog_dowamlylyk[뒷값]; sikl_indeks++) 보드.직렬쓰기(katalog_at[뒷값 * 64 + sikl_indeks]); 단말.Ýaz("/\n");
        }
        for (int faýl_indeks = 0; faýl_indeks < 파일수; faýl_indeks++) if (이름길이[faýl_indeks] > 0) {
            int 시작자리 = girizmeklik_başlat(Ad, faýl_indeks * 64, 이름길이[faýl_indeks]); if (시작자리 < 0) continue;
            for (int sikl_indeks = 시작자리; sikl_indeks < 이름길이[faýl_indeks]; sikl_indeks++) 보드.직렬쓰기(Ad[faýl_indeks * 64 + sikl_indeks]);
            단말.Ýaz("  "); 단말.수(dowamlylyk_baha[faýl_indeks]); 단말.Ýaz("baýt_baha(주기억 Faýl)\n");
        }
        return 0;
    }
}
