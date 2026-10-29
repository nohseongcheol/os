// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** RAM faele 64개, 파일당 16384바이트, 서술자 16개. 모든 tshedimosetso/정책은 Java에 있다.
 * 호출 도중 양보하지 않으므로 현재의 단일 코어 협력식 작업 사이에서 원자적이다.
 * 디스크 저장이나 POSIX 전체 구현을 뜻하지 않는다. 음수 반환은 phoso 번호다.
 */
public final class memori_Difaele {
    static final int 파일수 = 64;
    static int[] leina = new int[파일수 * 64];
    static int[] 이름길이 = new int[파일수];
    // Pack four bytes in each Java int, preserving the old content heap budget.
    static int[] Diteng_Boleng = new int[파일수 * 4096];
    static int[] boleele_Boleng = new int[파일수];
    static int[] 참조수 = new int[파일수];
    static int[] 사용 = new int[16];
    static int[] setotwa = new int[16];
    static int[] 위치 = new int[16];
    static int[] mokgwa_mokgwa = new int[16];
    static int[] tsela = new int[64];
    static int tsela_boleele;

    public static int 파일한도() { return 파일수; }
    static int 자료읽기(int faele, int 자리) { return (Diteng_Boleng[faele * 4096 + 자리 / 4] >>> ((자리 & 3) * 8)) & 255; }
    static void kwala_tshedimosetso(int faele, int 자리, int Boleng) {
        int sebaka_tsenyo = faele * 4096 + 자리 / 4, sutisa_Boleng = (자리 & 3) * 8;
        Diteng_Boleng[sebaka_tsenyo] = (Diteng_Boleng[sebaka_tsenyo] & ~(255 << sutisa_Boleng)) | ((Boleng & 255) << sutisa_Boleng);
    }

    public static int tsela_simolola(int lekanya) {
        tsela_boleele = 0;
        if (lekanya < 1 || lekanya > 63) return -36;
        tsela_boleele = lekanya;
        for (int lupu_tshupane = 0; lupu_tshupane < lekanya; lupu_tshupane++) tsela[lupu_tshupane] = 0;
        return 0;
    }
    public static int tsela_baete(int tshupane, int Boleng) {
        if (tshupane < 0 || tshupane >= tsela_boleele || Boleng < 1 || Boleng > 255) return -22;
        tsela[tshupane] = Boleng; return 0;
    }
    static int batla_tsenyo() {
        for (int faele_tshupane = 0; faele_tshupane < 파일수; faele_tshupane++) if (이름길이[faele_tshupane] > 0 && 이름길이[faele_tshupane] == 정규길이 && 접두(leina, faele_tshupane * 64, 이름길이[faele_tshupane], 정규, 정규길이)) return faele_tshupane;
        return -1;
    }
    public static int bula(int 플래그) {
        if (tsela_boleele == 0 || (플래그 & ~0x6c3) != 0 || (플래그 & 3) == 3) return -22;
        for (int lupu_tshupane = 0; lupu_tshupane < tsela_boleele; lupu_tshupane++) if (tsela[lupu_tshupane] == 0) return -22;
        if ((플래그 & 0x200) != 0 && (플래그 & 3) == 0) return -22;
        int 결과 = fokotsa_ntsifatso_Boleng(); if (결과 < 0) return 결과;
        if (batla_Lenaneofaele(정규길이) >= 0) return -21;
        결과 = 부모확인(); if (결과 < 0) return 결과;
        int faele = batla_tsenyo();
        if (faele >= 0 && (플래그 & 0xc0) == 0xc0) return -17;
        if (faele < 0 && (플래그 & 0x40) == 0) return -2;
        int 서술자 = -1;
        for (int lupu_tshupane = 0; lupu_tshupane < 16; lupu_tshupane++) if (사용[lupu_tshupane] == 0) { 서술자 = lupu_tshupane; break; }
        if (서술자 < 0) return -24;
        if (faele < 0) {
            for (int lupu_tshupane = 0; lupu_tshupane < 파일수; lupu_tshupane++) if (이름길이[lupu_tshupane] == 0 && 참조수[lupu_tshupane] == 0) { faele = lupu_tshupane; break; }
            if (faele < 0) return -28;
            이름길이[faele] = 정규길이;
            for (int lupu_tshupane = 0; lupu_tshupane < 정규길이; lupu_tshupane++) leina[faele * 64 + lupu_tshupane] = 정규[lupu_tshupane];
            boleele_Boleng[faele] = 0;
        }
        if ((플래그 & 0x200) != 0) boleele_Boleng[faele] = 0;
        사용[서술자] = 1; setotwa[서술자] = faele; 위치[서술자] = 0; mokgwa_mokgwa[서술자] = 플래그;
        참조수[faele]++;
        return 서술자 + 3;
    }
    static int netefatsa(int 서술자) {
        return 서술자 >= 3 && 서술자 < 19 && 사용[서술자 - 3] != 0 ? 서술자 - 3 : -1;
    }
    public static int 읽기(int 서술자) {
        int sebaka_tsenyo = netefatsa(서술자);
        if (sebaka_tsenyo < 0 || (mokgwa_mokgwa[sebaka_tsenyo] & 3) == 1) return -9;
        int faele = setotwa[sebaka_tsenyo];
        if (위치[sebaka_tsenyo] >= boleele_Boleng[faele]) return 256; // EOF와 tota_tshedimosetso 0x00..0xff 구별
        return 자료읽기(faele, 위치[sebaka_tsenyo]++);
    }
    public static int kwala(int 서술자, int Boleng) {
        int sebaka_tsenyo = netefatsa(서술자);
        if (sebaka_tsenyo < 0 || (mokgwa_mokgwa[sebaka_tsenyo] & 3) == 0) return -9;
        int faele = setotwa[sebaka_tsenyo];
        if ((mokgwa_mokgwa[sebaka_tsenyo] & 0x400) != 0) 위치[sebaka_tsenyo] = boleele_Boleng[faele];
        if (위치[sebaka_tsenyo] >= 16384) return -28;
        while (boleele_Boleng[faele] < 위치[sebaka_tsenyo]) kwala_tshedimosetso(faele, boleele_Boleng[faele]++, 0);
        kwala_tshedimosetso(faele, 위치[sebaka_tsenyo]++, Boleng);
        if (boleele_Boleng[faele] < 위치[sebaka_tsenyo]) boleele_Boleng[faele] = 위치[sebaka_tsenyo];
        return 1;
    }
    public static int 옮기기(int 서술자, int 거리, int 기준) {
        int sebaka_tsenyo = netefatsa(서술자);
        if (sebaka_tsenyo < 0) return -9;
        if (기준 < 0 || 기준 > 2 || 거리 < -16384 || 거리 > 16384) return -22;
        int 새위치 = 거리 + (기준 == 0 ? 0 : 기준 == 1 ? 위치[sebaka_tsenyo] : boleele_Boleng[setotwa[sebaka_tsenyo]]);
        if (새위치 < 0 || 새위치 > 16384) return -22;
        위치[sebaka_tsenyo] = 새위치; return 새위치;
    }
    public static int tswala(int 서술자) {
        int sebaka_tsenyo = netefatsa(서술자);
        if (sebaka_tsenyo < 0) return -9;
        참조수[setotwa[sebaka_tsenyo]]--; 사용[sebaka_tsenyo] = 0; return 0;
    }
    public static int lekanya(int 서술자) {
        int sebaka_tsenyo = netefatsa(서술자); return sebaka_tsenyo < 0 ? -9 : boleele_Boleng[setotwa[sebaka_tsenyo]];
    }
    public static int sete_boleele(int 서술자, int lekanya) {
        int sebaka_tsenyo = netefatsa(서술자);
        if (sebaka_tsenyo < 0 || (mokgwa_mokgwa[sebaka_tsenyo] & 3) == 0) return -9;
        if (lekanya < 0 || lekanya > 16384) return -22;
        int faele = setotwa[sebaka_tsenyo];
        while (boleele_Boleng[faele] < lekanya) kwala_tshedimosetso(faele, boleele_Boleng[faele]++, 0);
        boleele_Boleng[faele] = lekanya; return 0;
    }
    public static int 지우기() {
        if (tsela_boleele == 0) return -22;
        int 결과 = fokotsa_ntsifatso_Boleng(); if (결과 < 0) return 결과;
        if (batla_Lenaneofaele(정규길이) >= 0) return -21;
        결과 = 부모확인(); if (결과 < 0) return 결과;
        int faele = batla_tsenyo();
        if (faele < 0) return -2;
        이름길이[faele] = 0; return 0; // 열려 있는 파일은 마지막 close까지 유지
    }
    static void tsenyo_lenaane() {
        tsela_simolola(1); tsela_baete(0, '.'); 경로목록();
    }
    public static int 공개이름길이(int tshupane) {
        if (tshupane < 0 || tshupane >= 파일수 || 이름길이[tshupane] == 0) return 0;
        for (int lupu_tshupane = 0; lupu_tshupane < 이름길이[tshupane]; lupu_tshupane++) if (leina[tshupane * 64 + lupu_tshupane] == '/') return 0;
        return 이름길이[tshupane];
    }
    public static int 공개이름바이트(int tshupane, int 자리) {
        return tshupane >= 0 && tshupane < 파일수 && 자리 >= 0 && 자리 < 이름길이[tshupane] ? leina[tshupane * 64 + 자리] : -22;
    }
    public static int 공개파일크기(int tshupane) { return tshupane >= 0 && tshupane < 파일수 ? boleele_Boleng[tshupane] : -22; }
    static int[] 정규 = new int[64], ga_jaana_selwana = new int[64], Lenaneofaele_leina = new int[16 * 64], Lenaneofaele_boleele = new int[16];
    static int 정규길이, ga_jaana_boleele;
    static boolean 접두(int[] 이름들, int dirisa, int tsela_Boleng, int[] 앞, int kgaoganyomela_tsela) {
        if (tsela_Boleng < kgaoganyomela_tsela) return false;
        for (int lupu_tshupane = 0; lupu_tshupane < kgaoganyomela_tsela; lupu_tshupane++) if (이름들[dirisa + lupu_tshupane] != 앞[lupu_tshupane]) return false;
        return true;
    }
    static int fokotsa_ntsifatso_Boleng() {
        if (tsela_boleele == 0) return -22;
        정규길이 = tsela[0] == '/' ? 0 : ga_jaana_boleele;
        for (int lupu_tshupane = 0; lupu_tshupane < 정규길이; lupu_tshupane++) 정규[lupu_tshupane] = ga_jaana_selwana[lupu_tshupane];
        int 읽는자리 = 0;
        while (읽는자리 < tsela_boleele) {
            while (읽는자리 < tsela_boleele && tsela[읽는자리] == '/') 읽는자리++;
            int 시작자리 = 읽는자리; while (읽는자리 < tsela_boleele && tsela[읽는자리] != '/') { if (tsela[읽는자리] == 0) return -22; 읽는자리++; }
            int 항목수 = 읽는자리 - 시작자리; if (항목수 == 0 || 항목수 == 1 && tsela[시작자리] == '.') continue;
            if (항목수 == 2 && tsela[시작자리] == '.' && tsela[시작자리 + 1] == '.') {
                while (정규길이 > 0 && 정규[정규길이 - 1] != '/') 정규길이--;
                if (정규길이 > 0) 정규길이--;
                continue;
            }
            if (정규길이 + 항목수 + (정규길이 == 0 ? 0 : 1) > 63) return -36;
            if (정규길이 > 0) 정규[정규길이++] = '/';
            for (int lupu_tshupane = 시작자리; lupu_tshupane < 읽는자리; lupu_tshupane++) 정규[정규길이++] = tsela[lupu_tshupane];
        }
        return 0;
    }
    static int batla_Lenaneofaele(int 항목수) {
        if (항목수 == 0) return 0;
        for (int lupu_tshupane = 1; lupu_tshupane < 16; lupu_tshupane++) if (Lenaneofaele_boleele[lupu_tshupane] == 항목수 && 접두(Lenaneofaele_leina, lupu_tshupane * 64, 항목수, 정규, 항목수)) return lupu_tshupane;
        return -1;
    }
    static int 부모확인() {
        int 항목수 = 정규길이; while (항목수 > 0 && 정규[항목수 - 1] != '/') 항목수--;
        return batla_Lenaneofaele(항목수 == 0 ? 0 : 항목수 - 1) < 0 ? -2 : 0;
    }
    public static int tlhama_Lenaneofaele() {
        int 처리값 = fokotsa_ntsifatso_Boleng(); if (처리값 < 0) return 처리값;
        if (batla_Lenaneofaele(정규길이) >= 0 || batla_tsenyo() >= 0) return -17;
        처리값 = 부모확인(); if (처리값 < 0) return 처리값;
        for (int lupu_tshupane = 1; lupu_tshupane < 16; lupu_tshupane++) if (Lenaneofaele_boleele[lupu_tshupane] == 0) {
            Lenaneofaele_boleele[lupu_tshupane] = 정규길이; for (int 안쪽자리 = 0; 안쪽자리 < 정규길이; 안쪽자리++) Lenaneofaele_leina[lupu_tshupane * 64 + 안쪽자리] = 정규[안쪽자리]; return 0;
        }
        return -28;
    }
    public static int 항목종류() {
        int 처리값 = fokotsa_ntsifatso_Boleng(); if (처리값 < 0) return 처리값;
        if (batla_Lenaneofaele(정규길이) >= 0) return 2;
        return batla_tsenyo() >= 0 ? 1 : 0;
    }
    public static int fetola_Lenaneofaele() {
        int 처리값 = fokotsa_ntsifatso_Boleng(); if (처리값 < 0) return 처리값;
        if (batla_Lenaneofaele(정규길이) < 0) return -2;
        ga_jaana_boleele = 정규길이; for (int lupu_tshupane = 0; lupu_tshupane < ga_jaana_boleele; lupu_tshupane++) ga_jaana_selwana[lupu_tshupane] = 정규[lupu_tshupane]; return 0;
    }
    public static int tlosa_Lenaneofaele() {
        int 처리값 = fokotsa_ntsifatso_Boleng(); if (처리값 < 0) return 처리값;
        int 폴더번호 = batla_Lenaneofaele(정규길이); if (폴더번호 < 0) return -2; if (폴더번호 == 0) return -16;
        if (ga_jaana_boleele == 정규길이 && 접두(ga_jaana_selwana, 0, ga_jaana_boleele, 정규, 정규길이)) return -16;
        for (int lupu_tshupane = 0; lupu_tshupane < 파일수; lupu_tshupane++) {
            if (이름길이[lupu_tshupane] > 정규길이 && 접두(leina, lupu_tshupane * 64, 이름길이[lupu_tshupane], 정규, 정규길이) && leina[lupu_tshupane * 64 + 정규길이] == '/') return -39;
        }
        for (int lupu_tshupane = 0; lupu_tshupane < 16; lupu_tshupane++) {
            if (Lenaneofaele_boleele[lupu_tshupane] > 정규길이 && 접두(Lenaneofaele_leina, lupu_tshupane * 64, Lenaneofaele_boleele[lupu_tshupane], 정규, 정규길이) && Lenaneofaele_leina[lupu_tshupane * 64 + 정규길이] == '/') return -39;
        }
        Lenaneofaele_boleele[폴더번호] = 0; return 0;
    }
    public static int 이름바꾸기(int 원본번호) {
        if (원본번호 < 0 || 원본번호 >= 파일수 || 이름길이[원본번호] == 0) return -2;
        int 처리값 = fokotsa_ntsifatso_Boleng(); if (처리값 < 0) return 처리값;
        if (batla_Lenaneofaele(정규길이) >= 0) return -21;
        처리값 = 부모확인(); if (처리값 < 0) return 처리값;
        int 이전값 = batla_tsenyo(); if (이전값 == 원본번호) return 0;
        if (이전값 >= 0) 이름길이[이전값] = 0;
        이름길이[원본번호] = 정규길이; for (int lupu_tshupane = 0; lupu_tshupane < 정규길이; lupu_tshupane++) leina[원본번호 * 64 + lupu_tshupane] = 정규[lupu_tshupane]; return 0;
    }
    static int tsenyo_simolola(int[] tshedimosetso_setlhopha, int 시작점, int 항목수) {
        if (!접두(tshedimosetso_setlhopha, 시작점, 항목수, 정규, 정규길이)) return -1;
        int 시작자리 = 정규길이;
        if (시작자리 > 0) { if (항목수 <= 시작자리 || tshedimosetso_setlhopha[시작점 + 시작자리] != '/') return -1; 시작자리++; }
        if (항목수 <= 시작자리) return -1;
        for (int lupu_tshupane = 시작자리; lupu_tshupane < 항목수; lupu_tshupane++) if (tshedimosetso_setlhopha[시작점 + lupu_tshupane] == '/') return -1;
        return 시작자리;
    }
    static void ga_jaana_kwala() { 단말.문자('/'); for (int lupu_tshupane = 0; lupu_tshupane < ga_jaana_boleele; lupu_tshupane++) 보드.직렬쓰기(ga_jaana_selwana[lupu_tshupane]); }
    static int 경로목록() {
        int 처리값 = fokotsa_ntsifatso_Boleng(); if (처리값 < 0) return 처리값;
        int faele_setotwa = batla_tsenyo();
        if (faele_setotwa >= 0) { for (int lupu_tshupane = 0; lupu_tshupane < 정규길이; lupu_tshupane++) 보드.직렬쓰기(정규[lupu_tshupane]); 단말.kwala("  "); 단말.수(boleele_Boleng[faele_setotwa]); 단말.kwala("baete_Boleng(주기억 faele)\n"); return 0; }
        if (batla_Lenaneofaele(정규길이) < 0) return -2;
        for (int 뒷값 = 1; 뒷값 < 16; 뒷값++) if (Lenaneofaele_boleele[뒷값] > 0) {
            int 시작자리 = tsenyo_simolola(Lenaneofaele_leina, 뒷값 * 64, Lenaneofaele_boleele[뒷값]); if (시작자리 < 0) continue;
            for (int lupu_tshupane = 시작자리; lupu_tshupane < Lenaneofaele_boleele[뒷값]; lupu_tshupane++) 보드.직렬쓰기(Lenaneofaele_leina[뒷값 * 64 + lupu_tshupane]); 단말.kwala("/\n");
        }
        for (int faele_tshupane = 0; faele_tshupane < 파일수; faele_tshupane++) if (이름길이[faele_tshupane] > 0) {
            int 시작자리 = tsenyo_simolola(leina, faele_tshupane * 64, 이름길이[faele_tshupane]); if (시작자리 < 0) continue;
            for (int lupu_tshupane = 시작자리; lupu_tshupane < 이름길이[faele_tshupane]; lupu_tshupane++) 보드.직렬쓰기(leina[faele_tshupane * 64 + lupu_tshupane]);
            단말.kwala("  "); 단말.수(boleele_Boleng[faele_tshupane]); 단말.kwala("baete_Boleng(주기억 faele)\n");
        }
        return 0;
    }
}
