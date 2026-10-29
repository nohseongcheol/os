// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** RAM bara_denc 64개, 파일당 16384바이트, 서술자 16개. 모든 mbir/정책은 Java에 있다.
 * 호출 도중 양보하지 않으므로 현재의 단일 코어 협력식 작업 사이에서 원자적이다.
 * 디스크 저장이나 POSIX 전체 구현을 뜻하지 않는다. 음수 반환은 njumte 번호다.
 */
public final class fatlekookaay_Fisiye_yi {
    static final int 파일수 = 64;
    static int[] tur_253d1510 = new int[파일수 * 64];
    static int[] 이름길이 = new int[파일수];
    // Pack four bytes in each Java int, preserving the old content heap budget.
    static int[] Këmb_xëyma = new int[파일수 * 4096];
    static int[] diir_xëyma = new int[파일수];
    static int[] 참조수 = new int[파일수];
    static int[] 사용 = new int[16];
    static int[] luñu_name = new int[16];
    static int[] 위치 = new int[16];
    static int[] doxalin_anam = new int[16];
    static int[] Yoonu_jëmale = new int[64];
    static int Yoonu_jëmale_diir;

    public static int 파일한도() { return 파일수; }
    static int 자료읽기(int bara_denc, int 자리) { return (Këmb_xëyma[bara_denc * 4096 + 자리 / 4] >>> ((자리 & 3) * 8)) & 255; }
    static void biir_mbir(int bara_denc, int 자리, int xëyma) {
        int xar_xar_dugal_xabaar = bara_denc * 4096 + 자리 / 4, toxal_xëyma = (자리 & 3) * 8;
        Këmb_xëyma[xar_xar_dugal_xabaar] = (Këmb_xëyma[xar_xar_dugal_xabaar] & ~(255 << toxal_xëyma)) | ((xëyma & 255) << toxal_xëyma);
    }

    public static int Yoonu_jëmale_Door(int tolluwaay) {
        Yoonu_jëmale_diir = 0;
        if (tolluwaay < 1 || tolluwaay > 63) return -36;
        Yoonu_jëmale_diir = tolluwaay;
        for (int wërngël_àlluwa_tur = 0; wërngël_àlluwa_tur < tolluwaay; wërngël_àlluwa_tur++) Yoonu_jëmale[wërngël_àlluwa_tur] = 0;
        return 0;
    }
    public static int Yoonu_jëmale_okte(int àlluwa_tur, int xëyma) {
        if (àlluwa_tur < 0 || àlluwa_tur >= Yoonu_jëmale_diir || xëyma < 1 || xëyma > 255) return -22;
        Yoonu_jëmale[àlluwa_tur] = xëyma; return 0;
    }
    static int seet_dugal_xabaar() {
        for (int bara_denc_àlluwa_tur = 0; bara_denc_àlluwa_tur < 파일수; bara_denc_àlluwa_tur++) if (이름길이[bara_denc_àlluwa_tur] > 0 && 이름길이[bara_denc_àlluwa_tur] == 정규길이 && 접두(tur_253d1510, bara_denc_àlluwa_tur * 64, 이름길이[bara_denc_àlluwa_tur], 정규, 정규길이)) return bara_denc_àlluwa_tur;
        return -1;
    }
    public static int sos(int 플래그) {
        if (Yoonu_jëmale_diir == 0 || (플래그 & ~0x6c3) != 0 || (플래그 & 3) == 3) return -22;
        for (int wërngël_àlluwa_tur = 0; wërngël_àlluwa_tur < Yoonu_jëmale_diir; wërngël_àlluwa_tur++) if (Yoonu_jëmale[wërngël_àlluwa_tur] == 0) return -22;
        if ((플래그 & 0x200) != 0 && (플래그 & 3) == 0) return -22;
        int 결과 = yonnal_xëyma(); if (결과 < 0) return 결과;
        if (seet_dàmb(정규길이) >= 0) return -21;
        결과 = 부모확인(); if (결과 < 0) return 결과;
        int bara_denc = seet_dugal_xabaar();
        if (bara_denc >= 0 && (플래그 & 0xc0) == 0xc0) return -17;
        if (bara_denc < 0 && (플래그 & 0x40) == 0) return -2;
        int 서술자 = -1;
        for (int wërngël_àlluwa_tur = 0; wërngël_àlluwa_tur < 16; wërngël_àlluwa_tur++) if (사용[wërngël_àlluwa_tur] == 0) { 서술자 = wërngël_àlluwa_tur; break; }
        if (서술자 < 0) return -24;
        if (bara_denc < 0) {
            for (int wërngël_àlluwa_tur = 0; wërngël_àlluwa_tur < 파일수; wërngël_àlluwa_tur++) if (이름길이[wërngël_àlluwa_tur] == 0 && 참조수[wërngël_àlluwa_tur] == 0) { bara_denc = wërngël_àlluwa_tur; break; }
            if (bara_denc < 0) return -28;
            이름길이[bara_denc] = 정규길이;
            for (int wërngël_àlluwa_tur = 0; wërngël_àlluwa_tur < 정규길이; wërngël_àlluwa_tur++) tur_253d1510[bara_denc * 64 + wërngël_àlluwa_tur] = 정규[wërngël_àlluwa_tur];
            diir_xëyma[bara_denc] = 0;
        }
        if ((플래그 & 0x200) != 0) diir_xëyma[bara_denc] = 0;
        사용[서술자] = 1; luñu_name[서술자] = bara_denc; 위치[서술자] = 0; doxalin_anam[서술자] = 플래그;
        참조수[bara_denc]++;
        return 서술자 + 3;
    }
    static int luñutu(int 서술자) {
        return 서술자 >= 3 && 서술자 < 19 && 사용[서술자 - 3] != 0 ? 서술자 - 3 : -1;
    }
    public static int 읽기(int 서술자) {
        int xar_xar_dugal_xabaar = luñutu(서술자);
        if (xar_xar_dugal_xabaar < 0 || (doxalin_anam[xar_xar_dugal_xabaar] & 3) == 1) return -9;
        int bara_denc = luñu_name[xar_xar_dugal_xabaar];
        if (위치[xar_xar_dugal_xabaar] >= diir_xëyma[bara_denc]) return 256; // EOF와 liteew_mbir 0x00..0xff 구별
        return 자료읽기(bara_denc, 위치[xar_xar_dugal_xabaar]++);
    }
    public static int biir(int 서술자, int xëyma) {
        int xar_xar_dugal_xabaar = luñutu(서술자);
        if (xar_xar_dugal_xabaar < 0 || (doxalin_anam[xar_xar_dugal_xabaar] & 3) == 0) return -9;
        int bara_denc = luñu_name[xar_xar_dugal_xabaar];
        if ((doxalin_anam[xar_xar_dugal_xabaar] & 0x400) != 0) 위치[xar_xar_dugal_xabaar] = diir_xëyma[bara_denc];
        if (위치[xar_xar_dugal_xabaar] >= 16384) return -28;
        while (diir_xëyma[bara_denc] < 위치[xar_xar_dugal_xabaar]) biir_mbir(bara_denc, diir_xëyma[bara_denc]++, 0);
        biir_mbir(bara_denc, 위치[xar_xar_dugal_xabaar]++, xëyma);
        if (diir_xëyma[bara_denc] < 위치[xar_xar_dugal_xabaar]) diir_xëyma[bara_denc] = 위치[xar_xar_dugal_xabaar];
        return 1;
    }
    public static int 옮기기(int 서술자, int 거리, int 기준) {
        int xar_xar_dugal_xabaar = luñutu(서술자);
        if (xar_xar_dugal_xabaar < 0) return -9;
        if (기준 < 0 || 기준 > 2 || 거리 < -16384 || 거리 > 16384) return -22;
        int 새위치 = 거리 + (기준 == 0 ? 0 : 기준 == 1 ? 위치[xar_xar_dugal_xabaar] : diir_xëyma[luñu_name[xar_xar_dugal_xabaar]]);
        if (새위치 < 0 || 새위치 > 16384) return -22;
        위치[xar_xar_dugal_xabaar] = 새위치; return 새위치;
    }
    public static int Tej(int 서술자) {
        int xar_xar_dugal_xabaar = luñutu(서술자);
        if (xar_xar_dugal_xabaar < 0) return -9;
        참조수[luñu_name[xar_xar_dugal_xabaar]]--; 사용[xar_xar_dugal_xabaar] = 0; return 0;
    }
    public static int tolluwaay(int 서술자) {
        int xar_xar_dugal_xabaar = luñutu(서술자); return xar_xar_dugal_xabaar < 0 ? -9 : diir_xëyma[luñu_name[xar_xar_dugal_xabaar]];
    }
    public static int Boole_gi_diir(int 서술자, int tolluwaay) {
        int xar_xar_dugal_xabaar = luñutu(서술자);
        if (xar_xar_dugal_xabaar < 0 || (doxalin_anam[xar_xar_dugal_xabaar] & 3) == 0) return -9;
        if (tolluwaay < 0 || tolluwaay > 16384) return -22;
        int bara_denc = luñu_name[xar_xar_dugal_xabaar];
        while (diir_xëyma[bara_denc] < tolluwaay) biir_mbir(bara_denc, diir_xëyma[bara_denc]++, 0);
        diir_xëyma[bara_denc] = tolluwaay; return 0;
    }
    public static int 지우기() {
        if (Yoonu_jëmale_diir == 0) return -22;
        int 결과 = yonnal_xëyma(); if (결과 < 0) return 결과;
        if (seet_dàmb(정규길이) >= 0) return -21;
        결과 = 부모확인(); if (결과 < 0) return 결과;
        int bara_denc = seet_dugal_xabaar();
        if (bara_denc < 0) return -2;
        이름길이[bara_denc] = 0; return 0; // 열려 있는 파일은 마지막 close까지 유지
    }
    static void dugal_xabaar_lim() {
        Yoonu_jëmale_Door(1); Yoonu_jëmale_okte(0, '.'); 경로목록();
    }
    public static int 공개이름길이(int àlluwa_tur) {
        if (àlluwa_tur < 0 || àlluwa_tur >= 파일수 || 이름길이[àlluwa_tur] == 0) return 0;
        for (int wërngël_àlluwa_tur = 0; wërngël_àlluwa_tur < 이름길이[àlluwa_tur]; wërngël_àlluwa_tur++) if (tur_253d1510[àlluwa_tur * 64 + wërngël_àlluwa_tur] == '/') return 0;
        return 이름길이[àlluwa_tur];
    }
    public static int 공개이름바이트(int àlluwa_tur, int 자리) {
        return àlluwa_tur >= 0 && àlluwa_tur < 파일수 && 자리 >= 0 && 자리 < 이름길이[àlluwa_tur] ? tur_253d1510[àlluwa_tur * 64 + 자리] : -22;
    }
    public static int 공개파일크기(int àlluwa_tur) { return àlluwa_tur >= 0 && àlluwa_tur < 파일수 ? diir_xëyma[àlluwa_tur] : -22; }
    static int[] 정규 = new int[64], 현재 = new int[64], dàmb_tur = new int[16 * 64], dàmb_diir = new int[16];
    static int 정규길이, 현재길이;
    static boolean 접두(int[] 이름들, int daw, int Yoonu_jëmale_xëyma, int[] 앞, int rëddu_xàjji_Yoonu_jëmale) {
        if (Yoonu_jëmale_xëyma < rëddu_xàjji_Yoonu_jëmale) return false;
        for (int wërngël_àlluwa_tur = 0; wërngël_àlluwa_tur < rëddu_xàjji_Yoonu_jëmale; wërngël_àlluwa_tur++) if (이름들[daw + wërngël_àlluwa_tur] != 앞[wërngël_àlluwa_tur]) return false;
        return true;
    }
    static int yonnal_xëyma() {
        if (Yoonu_jëmale_diir == 0) return -22;
        정규길이 = Yoonu_jëmale[0] == '/' ? 0 : 현재길이;
        for (int wërngël_àlluwa_tur = 0; wërngël_àlluwa_tur < 정규길이; wërngël_àlluwa_tur++) 정규[wërngël_àlluwa_tur] = 현재[wërngël_àlluwa_tur];
        int 읽는자리 = 0;
        while (읽는자리 < Yoonu_jëmale_diir) {
            while (읽는자리 < Yoonu_jëmale_diir && Yoonu_jëmale[읽는자리] == '/') 읽는자리++;
            int 시작자리 = 읽는자리; while (읽는자리 < Yoonu_jëmale_diir && Yoonu_jëmale[읽는자리] != '/') { if (Yoonu_jëmale[읽는자리] == 0) return -22; 읽는자리++; }
            int 항목수 = 읽는자리 - 시작자리; if (항목수 == 0 || 항목수 == 1 && Yoonu_jëmale[시작자리] == '.') continue;
            if (항목수 == 2 && Yoonu_jëmale[시작자리] == '.' && Yoonu_jëmale[시작자리 + 1] == '.') {
                while (정규길이 > 0 && 정규[정규길이 - 1] != '/') 정규길이--;
                if (정규길이 > 0) 정규길이--;
                continue;
            }
            if (정규길이 + 항목수 + (정규길이 == 0 ? 0 : 1) > 63) return -36;
            if (정규길이 > 0) 정규[정규길이++] = '/';
            for (int wërngël_àlluwa_tur = 시작자리; wërngël_àlluwa_tur < 읽는자리; wërngël_àlluwa_tur++) 정규[정규길이++] = Yoonu_jëmale[wërngël_àlluwa_tur];
        }
        return 0;
    }
    static int seet_dàmb(int 항목수) {
        if (항목수 == 0) return 0;
        for (int wërngël_àlluwa_tur = 1; wërngël_àlluwa_tur < 16; wërngël_àlluwa_tur++) if (dàmb_diir[wërngël_àlluwa_tur] == 항목수 && 접두(dàmb_tur, wërngël_àlluwa_tur * 64, 항목수, 정규, 항목수)) return wërngël_àlluwa_tur;
        return -1;
    }
    static int 부모확인() {
        int 항목수 = 정규길이; while (항목수 > 0 && 정규[항목수 - 1] != '/') 항목수--;
        return seet_dàmb(항목수 == 0 ? 0 : 항목수 - 1) < 0 ? -2 : 0;
    }
    public static int sos_dàmb() {
        int 처리값 = yonnal_xëyma(); if (처리값 < 0) return 처리값;
        if (seet_dàmb(정규길이) >= 0 || seet_dugal_xabaar() >= 0) return -17;
        처리값 = 부모확인(); if (처리값 < 0) return 처리값;
        for (int wërngël_àlluwa_tur = 1; wërngël_àlluwa_tur < 16; wërngël_àlluwa_tur++) if (dàmb_diir[wërngël_àlluwa_tur] == 0) {
            dàmb_diir[wërngël_àlluwa_tur] = 정규길이; for (int 안쪽자리 = 0; 안쪽자리 < 정규길이; 안쪽자리++) dàmb_tur[wërngël_àlluwa_tur * 64 + 안쪽자리] = 정규[안쪽자리]; return 0;
        }
        return -28;
    }
    public static int 항목종류() {
        int 처리값 = yonnal_xëyma(); if (처리값 < 0) return 처리값;
        if (seet_dàmb(정규길이) >= 0) return 2;
        return seet_dugal_xabaar() >= 0 ? 1 : 0;
    }
    public static int soppi_dàmb() {
        int 처리값 = yonnal_xëyma(); if (처리값 < 0) return 처리값;
        if (seet_dàmb(정규길이) < 0) return -2;
        현재길이 = 정규길이; for (int wërngël_àlluwa_tur = 0; wërngël_àlluwa_tur < 현재길이; wërngël_àlluwa_tur++) 현재[wërngël_àlluwa_tur] = 정규[wërngël_àlluwa_tur]; return 0;
    }
    public static int dandal_dàmb() {
        int 처리값 = yonnal_xëyma(); if (처리값 < 0) return 처리값;
        int 폴더번호 = seet_dàmb(정규길이); if (폴더번호 < 0) return -2; if (폴더번호 == 0) return -16;
        if (현재길이 == 정규길이 && 접두(현재, 0, 현재길이, 정규, 정규길이)) return -16;
        for (int wërngël_àlluwa_tur = 0; wërngël_àlluwa_tur < 파일수; wërngël_àlluwa_tur++) {
            if (이름길이[wërngël_àlluwa_tur] > 정규길이 && 접두(tur_253d1510, wërngël_àlluwa_tur * 64, 이름길이[wërngël_àlluwa_tur], 정규, 정규길이) && tur_253d1510[wërngël_àlluwa_tur * 64 + 정규길이] == '/') return -39;
        }
        for (int wërngël_àlluwa_tur = 0; wërngël_àlluwa_tur < 16; wërngël_àlluwa_tur++) {
            if (dàmb_diir[wërngël_àlluwa_tur] > 정규길이 && 접두(dàmb_tur, wërngël_àlluwa_tur * 64, dàmb_diir[wërngël_àlluwa_tur], 정규, 정규길이) && dàmb_tur[wërngël_àlluwa_tur * 64 + 정규길이] == '/') return -39;
        }
        dàmb_diir[폴더번호] = 0; return 0;
    }
    public static int 이름바꾸기(int 원본번호) {
        if (원본번호 < 0 || 원본번호 >= 파일수 || 이름길이[원본번호] == 0) return -2;
        int 처리값 = yonnal_xëyma(); if (처리값 < 0) return 처리값;
        if (seet_dàmb(정규길이) >= 0) return -21;
        처리값 = 부모확인(); if (처리값 < 0) return 처리값;
        int 이전값 = seet_dugal_xabaar(); if (이전값 == 원본번호) return 0;
        if (이전값 >= 0) 이름길이[이전값] = 0;
        이름길이[원본번호] = 정규길이; for (int wërngël_àlluwa_tur = 0; wërngël_àlluwa_tur < 정규길이; wërngël_àlluwa_tur++) tur_253d1510[원본번호 * 64 + wërngël_àlluwa_tur] = 정규[wërngël_àlluwa_tur]; return 0;
    }
    static int dugal_xabaar_Door(int[] mbir_TABLO, int 시작점, int 항목수) {
        if (!접두(mbir_TABLO, 시작점, 항목수, 정규, 정규길이)) return -1;
        int 시작자리 = 정규길이;
        if (시작자리 > 0) { if (항목수 <= 시작자리 || mbir_TABLO[시작점 + 시작자리] != '/') return -1; 시작자리++; }
        if (항목수 <= 시작자리) return -1;
        for (int wërngël_àlluwa_tur = 시작자리; wërngël_àlluwa_tur < 항목수; wërngël_àlluwa_tur++) if (mbir_TABLO[시작점 + wërngël_àlluwa_tur] == '/') return -1;
        return 시작자리;
    }
    static void 현재쓰기() { 단말.문자('/'); for (int wërngël_àlluwa_tur = 0; wërngël_àlluwa_tur < 현재길이; wërngël_àlluwa_tur++) 보드.직렬쓰기(현재[wërngël_àlluwa_tur]); }
    static int 경로목록() {
        int 처리값 = yonnal_xëyma(); if (처리값 < 0) return 처리값;
        int bara_denc_luñu_name = seet_dugal_xabaar();
        if (bara_denc_luñu_name >= 0) { for (int wërngël_àlluwa_tur = 0; wërngël_àlluwa_tur < 정규길이; wërngël_àlluwa_tur++) 보드.직렬쓰기(정규[wërngël_àlluwa_tur]); 단말.biir("  "); 단말.수(diir_xëyma[bara_denc_luñu_name]); 단말.biir("okte_xëyma(주기억 bara_denc)\n"); return 0; }
        if (seet_dàmb(정규길이) < 0) return -2;
        for (int 뒷값 = 1; 뒷값 < 16; 뒷값++) if (dàmb_diir[뒷값] > 0) {
            int 시작자리 = dugal_xabaar_Door(dàmb_tur, 뒷값 * 64, dàmb_diir[뒷값]); if (시작자리 < 0) continue;
            for (int wërngël_àlluwa_tur = 시작자리; wërngël_àlluwa_tur < dàmb_diir[뒷값]; wërngël_àlluwa_tur++) 보드.직렬쓰기(dàmb_tur[뒷값 * 64 + wërngël_àlluwa_tur]); 단말.biir("/\n");
        }
        for (int bara_denc_àlluwa_tur = 0; bara_denc_àlluwa_tur < 파일수; bara_denc_àlluwa_tur++) if (이름길이[bara_denc_àlluwa_tur] > 0) {
            int 시작자리 = dugal_xabaar_Door(tur_253d1510, bara_denc_àlluwa_tur * 64, 이름길이[bara_denc_àlluwa_tur]); if (시작자리 < 0) continue;
            for (int wërngël_àlluwa_tur = 시작자리; wërngël_àlluwa_tur < 이름길이[bara_denc_àlluwa_tur]; wërngël_àlluwa_tur++) 보드.직렬쓰기(tur_253d1510[bara_denc_àlluwa_tur * 64 + wërngël_àlluwa_tur]);
            단말.biir("  "); 단말.수(diir_xëyma[bara_denc_àlluwa_tur]); 단말.biir("okte_xëyma(주기억 bara_denc)\n");
        }
        return 0;
    }
}
