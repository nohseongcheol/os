// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** RAM iFayili 64개, 파일당 16384바이트, 서술자 16개. 모든 iingcombolo/정책은 Java에 있다.
 * 호출 도중 양보하지 않으므로 현재의 단일 코어 협력식 작업 사이에서 원자적이다.
 * 디스크 저장이나 POSIX 전체 구현을 뜻하지 않는다. 음수 반환은 Impazamo 번호다.
 */
public final class imemori_Iifayile {
    static final int 파일수 = 64;
    static int[] Igama = new int[파일수 * 64];
    static int[] 이름길이 = new int[파일수];
    // Pack four bytes in each Java int, preserving the old content heap budget.
    static int[] Isiqulatho_ixabiso = new int[파일수 * 4096];
    static int[] ubude_ixabiso = new int[파일수];
    static int[] 참조수 = new int[파일수];
    static int[] 사용 = new int[16];
    static int[] ithagethi = new int[16];
    static int[] 위치 = new int[16];
    static int[] imethodi_imo = new int[16];
    static int[] INDLELA = new int[64];
    static int indlela_ubude;

    public static int 파일한도() { return 파일수; }
    static int 자료읽기(int iFayili, int 자리) { return (Isiqulatho_ixabiso[iFayili * 4096 + 자리 / 4] >>> ((자리 & 3) * 8)) & 255; }
    static void bhala_iingcombolo(int iFayili, int 자리, int ixabiso) {
        int isithuba_ufako_nkcukacha = iFayili * 4096 + 자리 / 4, fudusa_ixabiso = (자리 & 3) * 8;
        Isiqulatho_ixabiso[isithuba_ufako_nkcukacha] = (Isiqulatho_ixabiso[isithuba_ufako_nkcukacha] & ~(255 << fudusa_ixabiso)) | ((ixabiso & 255) << fudusa_ixabiso);
    }

    public static int indlela_qala(int Ubukhulu) {
        indlela_ubude = 0;
        if (Ubukhulu < 1 || Ubukhulu > 63) return -36;
        indlela_ubude = Ubukhulu;
        for (int iluphu_indeksa = 0; iluphu_indeksa < Ubukhulu; iluphu_indeksa++) INDLELA[iluphu_indeksa] = 0;
        return 0;
    }
    public static int indlela_ibhayithi(int indeksa, int ixabiso) {
        if (indeksa < 0 || indeksa >= indlela_ubude || ixabiso < 1 || ixabiso > 255) return -22;
        INDLELA[indeksa] = ixabiso; return 0;
    }
    static int fumana_ufako_nkcukacha() {
        for (int ifayile_indeksa = 0; ifayile_indeksa < 파일수; ifayile_indeksa++) if (이름길이[ifayile_indeksa] > 0 && 이름길이[ifayile_indeksa] == 정규길이 && 접두(Igama, ifayile_indeksa * 64, 이름길이[ifayile_indeksa], 정규, 정규길이)) return ifayile_indeksa;
        return -1;
    }
    public static int Vula(int 플래그) {
        if (indlela_ubude == 0 || (플래그 & ~0x6c3) != 0 || (플래그 & 3) == 3) return -22;
        for (int iluphu_indeksa = 0; iluphu_indeksa < indlela_ubude; iluphu_indeksa++) if (INDLELA[iluphu_indeksa] == 0) return -22;
        if ((플래그 & 0x200) != 0 && (플래그 & 3) == 0) return -22;
        int 결과 = qhelekisa_ixabiso(); if (결과 < 0) return 결과;
        if (fumana_isalathisi(정규길이) >= 0) return -21;
        결과 = 부모확인(); if (결과 < 0) return 결과;
        int iFayili = fumana_ufako_nkcukacha();
        if (iFayili >= 0 && (플래그 & 0xc0) == 0xc0) return -17;
        if (iFayili < 0 && (플래그 & 0x40) == 0) return -2;
        int 서술자 = -1;
        for (int iluphu_indeksa = 0; iluphu_indeksa < 16; iluphu_indeksa++) if (사용[iluphu_indeksa] == 0) { 서술자 = iluphu_indeksa; break; }
        if (서술자 < 0) return -24;
        if (iFayili < 0) {
            for (int iluphu_indeksa = 0; iluphu_indeksa < 파일수; iluphu_indeksa++) if (이름길이[iluphu_indeksa] == 0 && 참조수[iluphu_indeksa] == 0) { iFayili = iluphu_indeksa; break; }
            if (iFayili < 0) return -28;
            이름길이[iFayili] = 정규길이;
            for (int iluphu_indeksa = 0; iluphu_indeksa < 정규길이; iluphu_indeksa++) Igama[iFayili * 64 + iluphu_indeksa] = 정규[iluphu_indeksa];
            ubude_ixabiso[iFayili] = 0;
        }
        if ((플래그 & 0x200) != 0) ubude_ixabiso[iFayili] = 0;
        사용[서술자] = 1; ithagethi[서술자] = iFayili; 위치[서술자] = 0; imethodi_imo[서술자] = 플래그;
        참조수[iFayili]++;
        return 서술자 + 3;
    }
    static int ngqinisisa(int 서술자) {
        return 서술자 >= 3 && 서술자 < 19 && 사용[서술자 - 3] != 0 ? 서술자 - 3 : -1;
    }
    public static int Funda(int 서술자) {
        int isithuba_ufako_nkcukacha = ngqinisisa(서술자);
        if (isithuba_ufako_nkcukacha < 0 || (imethodi_imo[isithuba_ufako_nkcukacha] & 3) == 1) return -9;
        int iFayili = ithagethi[isithuba_ufako_nkcukacha];
        if (위치[isithuba_ufako_nkcukacha] >= ubude_ixabiso[iFayili]) return 256; // EOF와 eyona_yenzekileyo_iingcombolo 0x00..0xff 구별
        return 자료읽기(iFayili, 위치[isithuba_ufako_nkcukacha]++);
    }
    public static int Bhala(int 서술자, int ixabiso) {
        int isithuba_ufako_nkcukacha = ngqinisisa(서술자);
        if (isithuba_ufako_nkcukacha < 0 || (imethodi_imo[isithuba_ufako_nkcukacha] & 3) == 0) return -9;
        int iFayili = ithagethi[isithuba_ufako_nkcukacha];
        if ((imethodi_imo[isithuba_ufako_nkcukacha] & 0x400) != 0) 위치[isithuba_ufako_nkcukacha] = ubude_ixabiso[iFayili];
        if (위치[isithuba_ufako_nkcukacha] >= 16384) return -28;
        while (ubude_ixabiso[iFayili] < 위치[isithuba_ufako_nkcukacha]) bhala_iingcombolo(iFayili, ubude_ixabiso[iFayili]++, 0);
        bhala_iingcombolo(iFayili, 위치[isithuba_ufako_nkcukacha]++, ixabiso);
        if (ubude_ixabiso[iFayili] < 위치[isithuba_ufako_nkcukacha]) ubude_ixabiso[iFayili] = 위치[isithuba_ufako_nkcukacha];
        return 1;
    }
    public static int 옮기기(int 서술자, int 거리, int 기준) {
        int isithuba_ufako_nkcukacha = ngqinisisa(서술자);
        if (isithuba_ufako_nkcukacha < 0) return -9;
        if (기준 < 0 || 기준 > 2 || 거리 < -16384 || 거리 > 16384) return -22;
        int 새위치 = 거리 + (기준 == 0 ? 0 : 기준 == 1 ? 위치[isithuba_ufako_nkcukacha] : ubude_ixabiso[ithagethi[isithuba_ufako_nkcukacha]]);
        if (새위치 < 0 || 새위치 > 16384) return -22;
        위치[isithuba_ufako_nkcukacha] = 새위치; return 새위치;
    }
    public static int Vala(int 서술자) {
        int isithuba_ufako_nkcukacha = ngqinisisa(서술자);
        if (isithuba_ufako_nkcukacha < 0) return -9;
        참조수[ithagethi[isithuba_ufako_nkcukacha]]--; 사용[isithuba_ufako_nkcukacha] = 0; return 0;
    }
    public static int Ubukhulu(int 서술자) {
        int isithuba_ufako_nkcukacha = ngqinisisa(서술자); return isithuba_ufako_nkcukacha < 0 ? -9 : ubude_ixabiso[ithagethi[isithuba_ufako_nkcukacha]];
    }
    public static int isethi_ubude(int 서술자, int Ubukhulu) {
        int isithuba_ufako_nkcukacha = ngqinisisa(서술자);
        if (isithuba_ufako_nkcukacha < 0 || (imethodi_imo[isithuba_ufako_nkcukacha] & 3) == 0) return -9;
        if (Ubukhulu < 0 || Ubukhulu > 16384) return -22;
        int iFayili = ithagethi[isithuba_ufako_nkcukacha];
        while (ubude_ixabiso[iFayili] < Ubukhulu) bhala_iingcombolo(iFayili, ubude_ixabiso[iFayili]++, 0);
        ubude_ixabiso[iFayili] = Ubukhulu; return 0;
    }
    public static int 지우기() {
        if (indlela_ubude == 0) return -22;
        int 결과 = qhelekisa_ixabiso(); if (결과 < 0) return 결과;
        if (fumana_isalathisi(정규길이) >= 0) return -21;
        결과 = 부모확인(); if (결과 < 0) return 결과;
        int iFayili = fumana_ufako_nkcukacha();
        if (iFayili < 0) return -2;
        이름길이[iFayili] = 0; return 0; // 열려 있는 파일은 마지막 close까지 유지
    }
    static void ufako_nkcukacha_uludwe() {
        indlela_qala(1); indlela_ibhayithi(0, '.'); 경로목록();
    }
    public static int 공개이름길이(int indeksa) {
        if (indeksa < 0 || indeksa >= 파일수 || 이름길이[indeksa] == 0) return 0;
        for (int iluphu_indeksa = 0; iluphu_indeksa < 이름길이[indeksa]; iluphu_indeksa++) if (Igama[indeksa * 64 + iluphu_indeksa] == '/') return 0;
        return 이름길이[indeksa];
    }
    public static int 공개이름바이트(int indeksa, int 자리) {
        return indeksa >= 0 && indeksa < 파일수 && 자리 >= 0 && 자리 < 이름길이[indeksa] ? Igama[indeksa * 64 + 자리] : -22;
    }
    public static int 공개파일크기(int indeksa) { return indeksa >= 0 && indeksa < 파일수 ? ubude_ixabiso[indeksa] : -22; }
    static int[] 정규 = new int[64], 현재 = new int[64], isalathisi_igama = new int[16 * 64], isalathisi_ubude = new int[16];
    static int 정규길이, 현재길이;
    static boolean 접두(int[] 이름들, int Phumeza, int indlela_ixabiso, int[] 앞, int isikhokeli_indlela) {
        if (indlela_ixabiso < isikhokeli_indlela) return false;
        for (int iluphu_indeksa = 0; iluphu_indeksa < isikhokeli_indlela; iluphu_indeksa++) if (이름들[Phumeza + iluphu_indeksa] != 앞[iluphu_indeksa]) return false;
        return true;
    }
    static int qhelekisa_ixabiso() {
        if (indlela_ubude == 0) return -22;
        정규길이 = INDLELA[0] == '/' ? 0 : 현재길이;
        for (int iluphu_indeksa = 0; iluphu_indeksa < 정규길이; iluphu_indeksa++) 정규[iluphu_indeksa] = 현재[iluphu_indeksa];
        int 읽는자리 = 0;
        while (읽는자리 < indlela_ubude) {
            while (읽는자리 < indlela_ubude && INDLELA[읽는자리] == '/') 읽는자리++;
            int 시작자리 = 읽는자리; while (읽는자리 < indlela_ubude && INDLELA[읽는자리] != '/') { if (INDLELA[읽는자리] == 0) return -22; 읽는자리++; }
            int 항목수 = 읽는자리 - 시작자리; if (항목수 == 0 || 항목수 == 1 && INDLELA[시작자리] == '.') continue;
            if (항목수 == 2 && INDLELA[시작자리] == '.' && INDLELA[시작자리 + 1] == '.') {
                while (정규길이 > 0 && 정규[정규길이 - 1] != '/') 정규길이--;
                if (정규길이 > 0) 정규길이--;
                continue;
            }
            if (정규길이 + 항목수 + (정규길이 == 0 ? 0 : 1) > 63) return -36;
            if (정규길이 > 0) 정규[정규길이++] = '/';
            for (int iluphu_indeksa = 시작자리; iluphu_indeksa < 읽는자리; iluphu_indeksa++) 정규[정규길이++] = INDLELA[iluphu_indeksa];
        }
        return 0;
    }
    static int fumana_isalathisi(int 항목수) {
        if (항목수 == 0) return 0;
        for (int iluphu_indeksa = 1; iluphu_indeksa < 16; iluphu_indeksa++) if (isalathisi_ubude[iluphu_indeksa] == 항목수 && 접두(isalathisi_igama, iluphu_indeksa * 64, 항목수, 정규, 항목수)) return iluphu_indeksa;
        return -1;
    }
    static int 부모확인() {
        int 항목수 = 정규길이; while (항목수 > 0 && 정규[항목수 - 1] != '/') 항목수--;
        return fumana_isalathisi(항목수 == 0 ? 0 : 항목수 - 1) < 0 ? -2 : 0;
    }
    public static int yila_isalathisi() {
        int 처리값 = qhelekisa_ixabiso(); if (처리값 < 0) return 처리값;
        if (fumana_isalathisi(정규길이) >= 0 || fumana_ufako_nkcukacha() >= 0) return -17;
        처리값 = 부모확인(); if (처리값 < 0) return 처리값;
        for (int iluphu_indeksa = 1; iluphu_indeksa < 16; iluphu_indeksa++) if (isalathisi_ubude[iluphu_indeksa] == 0) {
            isalathisi_ubude[iluphu_indeksa] = 정규길이; for (int 안쪽자리 = 0; 안쪽자리 < 정규길이; 안쪽자리++) isalathisi_igama[iluphu_indeksa * 64 + 안쪽자리] = 정규[안쪽자리]; return 0;
        }
        return -28;
    }
    public static int 항목종류() {
        int 처리값 = qhelekisa_ixabiso(); if (처리값 < 0) return 처리값;
        if (fumana_isalathisi(정규길이) >= 0) return 2;
        return fumana_ufako_nkcukacha() >= 0 ? 1 : 0;
    }
    public static int tshintsha_isalathisi() {
        int 처리값 = qhelekisa_ixabiso(); if (처리값 < 0) return 처리값;
        if (fumana_isalathisi(정규길이) < 0) return -2;
        현재길이 = 정규길이; for (int iluphu_indeksa = 0; iluphu_indeksa < 현재길이; iluphu_indeksa++) 현재[iluphu_indeksa] = 정규[iluphu_indeksa]; return 0;
    }
    public static int shenxisa_isalathisi() {
        int 처리값 = qhelekisa_ixabiso(); if (처리값 < 0) return 처리값;
        int 폴더번호 = fumana_isalathisi(정규길이); if (폴더번호 < 0) return -2; if (폴더번호 == 0) return -16;
        if (현재길이 == 정규길이 && 접두(현재, 0, 현재길이, 정규, 정규길이)) return -16;
        for (int iluphu_indeksa = 0; iluphu_indeksa < 파일수; iluphu_indeksa++) {
            if (이름길이[iluphu_indeksa] > 정규길이 && 접두(Igama, iluphu_indeksa * 64, 이름길이[iluphu_indeksa], 정규, 정규길이) && Igama[iluphu_indeksa * 64 + 정규길이] == '/') return -39;
        }
        for (int iluphu_indeksa = 0; iluphu_indeksa < 16; iluphu_indeksa++) {
            if (isalathisi_ubude[iluphu_indeksa] > 정규길이 && 접두(isalathisi_igama, iluphu_indeksa * 64, isalathisi_ubude[iluphu_indeksa], 정규, 정규길이) && isalathisi_igama[iluphu_indeksa * 64 + 정규길이] == '/') return -39;
        }
        isalathisi_ubude[폴더번호] = 0; return 0;
    }
    public static int 이름바꾸기(int 원본번호) {
        if (원본번호 < 0 || 원본번호 >= 파일수 || 이름길이[원본번호] == 0) return -2;
        int 처리값 = qhelekisa_ixabiso(); if (처리값 < 0) return 처리값;
        if (fumana_isalathisi(정규길이) >= 0) return -21;
        처리값 = 부모확인(); if (처리값 < 0) return 처리값;
        int 이전값 = fumana_ufako_nkcukacha(); if (이전값 == 원본번호) return 0;
        if (이전값 >= 0) 이름길이[이전값] = 0;
        이름길이[원본번호] = 정규길이; for (int iluphu_indeksa = 0; iluphu_indeksa < 정규길이; iluphu_indeksa++) Igama[원본번호 * 64 + iluphu_indeksa] = 정규[iluphu_indeksa]; return 0;
    }
    static int ufako_nkcukacha_qala(int[] iingcombolo_ULUHLU, int 시작점, int 항목수) {
        if (!접두(iingcombolo_ULUHLU, 시작점, 항목수, 정규, 정규길이)) return -1;
        int 시작자리 = 정규길이;
        if (시작자리 > 0) { if (항목수 <= 시작자리 || iingcombolo_ULUHLU[시작점 + 시작자리] != '/') return -1; 시작자리++; }
        if (항목수 <= 시작자리) return -1;
        for (int iluphu_indeksa = 시작자리; iluphu_indeksa < 항목수; iluphu_indeksa++) if (iingcombolo_ULUHLU[시작점 + iluphu_indeksa] == '/') return -1;
        return 시작자리;
    }
    static void 현재쓰기() { 단말.문자('/'); for (int iluphu_indeksa = 0; iluphu_indeksa < 현재길이; iluphu_indeksa++) 보드.직렬쓰기(현재[iluphu_indeksa]); }
    static int 경로목록() {
        int 처리값 = qhelekisa_ixabiso(); if (처리값 < 0) return 처리값;
        int ifayile_ithagethi = fumana_ufako_nkcukacha();
        if (ifayile_ithagethi >= 0) { for (int iluphu_indeksa = 0; iluphu_indeksa < 정규길이; iluphu_indeksa++) 보드.직렬쓰기(정규[iluphu_indeksa]); 단말.Bhala("  "); 단말.수(ubude_ixabiso[ifayile_ithagethi]); 단말.Bhala("ibhayithi_ixabiso(주기억 iFayili)\n"); return 0; }
        if (fumana_isalathisi(정규길이) < 0) return -2;
        for (int 뒷값 = 1; 뒷값 < 16; 뒷값++) if (isalathisi_ubude[뒷값] > 0) {
            int 시작자리 = ufako_nkcukacha_qala(isalathisi_igama, 뒷값 * 64, isalathisi_ubude[뒷값]); if (시작자리 < 0) continue;
            for (int iluphu_indeksa = 시작자리; iluphu_indeksa < isalathisi_ubude[뒷값]; iluphu_indeksa++) 보드.직렬쓰기(isalathisi_igama[뒷값 * 64 + iluphu_indeksa]); 단말.Bhala("/\n");
        }
        for (int ifayile_indeksa = 0; ifayile_indeksa < 파일수; ifayile_indeksa++) if (이름길이[ifayile_indeksa] > 0) {
            int 시작자리 = ufako_nkcukacha_qala(Igama, ifayile_indeksa * 64, 이름길이[ifayile_indeksa]); if (시작자리 < 0) continue;
            for (int iluphu_indeksa = 시작자리; iluphu_indeksa < 이름길이[ifayile_indeksa]; iluphu_indeksa++) 보드.직렬쓰기(Igama[ifayile_indeksa * 64 + iluphu_indeksa]);
            단말.Bhala("  "); 단말.수(ubude_ixabiso[ifayile_indeksa]); 단말.Bhala("ibhayithi_ixabiso(주기억 iFayili)\n");
        }
        return 0;
    }
}
