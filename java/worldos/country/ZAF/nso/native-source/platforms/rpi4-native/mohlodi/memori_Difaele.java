// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** RAM Faele 64개, 파일당 16384바이트, 서술자 16개. 모든 data/정책은 Java에 있다.
 * 호출 도중 양보하지 않으므로 현재의 단일 코어 협력식 작업 사이에서 원자적이다.
 * 디스크 저장이나 POSIX 전체 구현을 뜻하지 않는다. 음수 반환은 Phošo 번호다.
 */
public final class memori_Difaele {
    static final int 파일수 = 64;
    static int[] Leina = new int[파일수 * 64];
    static int[] 이름길이 = new int[파일수];
    // Pack four bytes in each Java int, preserving the old content heap budget.
    static int[] Diteng_boleng = new int[파일수 * 4096];
    static int[] botelele_boleng = new int[파일수];
    static int[] 참조수 = new int[파일수];
    static int[] 사용 = new int[16];
    static int[] nepo = new int[16];
    static int[] 위치 = new int[16];
    static int[] mokgwa_mokgwa = new int[16];
    static int[] Tsejana = new int[64];
    static int tsela_botelele;

    public static int 파일한도() { return 파일수; }
    static int 자료읽기(int Faele, int 자리) { return (Diteng_boleng[Faele * 4096 + 자리 / 4] >>> ((자리 & 3) * 8)) & 255; }
    static void ngwala_data(int Faele, int 자리, int boleng) {
        int sekgobana_go_tsenya_tshedimošo = Faele * 4096 + 자리 / 4, šuthiša_boleng = (자리 & 3) * 8;
        Diteng_boleng[sekgobana_go_tsenya_tshedimošo] = (Diteng_boleng[sekgobana_go_tsenya_tshedimošo] & ~(255 << šuthiša_boleng)) | ((boleng & 255) << šuthiša_boleng);
    }

    public static int tsela_Thomišo(int Bogolo) {
        tsela_botelele = 0;
        if (Bogolo < 1 || Bogolo > 63) return -36;
        tsela_botelele = Bogolo;
        for (int ditaelopoeletšwa_lokela = 0; ditaelopoeletšwa_lokela < Bogolo; ditaelopoeletšwa_lokela++) Tsejana[ditaelopoeletšwa_lokela] = 0;
        return 0;
    }
    public static int tsela_paete(int lokela, int boleng) {
        if (lokela < 0 || lokela >= tsela_botelele || boleng < 1 || boleng > 255) return -22;
        Tsejana[lokela] = boleng; return 0;
    }
    static int hwetša_go_tsenya_tshedimošo() {
        for (int faele_lokela = 0; faele_lokela < 파일수; faele_lokela++) if (이름길이[faele_lokela] > 0 && 이름길이[faele_lokela] == 정규길이 && 접두(Leina, faele_lokela * 64, 이름길이[faele_lokela], 정규, 정규길이)) return faele_lokela;
        return -1;
    }
    public static int Bula(int 플래그) {
        if (tsela_botelele == 0 || (플래그 & ~0x6c3) != 0 || (플래그 & 3) == 3) return -22;
        for (int ditaelopoeletšwa_lokela = 0; ditaelopoeletšwa_lokela < tsela_botelele; ditaelopoeletšwa_lokela++) if (Tsejana[ditaelopoeletšwa_lokela] == 0) return -22;
        if ((플래그 & 0x200) != 0 && (플래그 & 3) == 0) return -22;
        int 결과 = fokotša_kopišo_boleng(); if (결과 < 0) return 결과;
        if (hwetša_lelokelelo(정규길이) >= 0) return -21;
        결과 = 부모확인(); if (결과 < 0) return 결과;
        int Faele = hwetša_go_tsenya_tshedimošo();
        if (Faele >= 0 && (플래그 & 0xc0) == 0xc0) return -17;
        if (Faele < 0 && (플래그 & 0x40) == 0) return -2;
        int 서술자 = -1;
        for (int ditaelopoeletšwa_lokela = 0; ditaelopoeletšwa_lokela < 16; ditaelopoeletšwa_lokela++) if (사용[ditaelopoeletšwa_lokela] == 0) { 서술자 = ditaelopoeletšwa_lokela; break; }
        if (서술자 < 0) return -24;
        if (Faele < 0) {
            for (int ditaelopoeletšwa_lokela = 0; ditaelopoeletšwa_lokela < 파일수; ditaelopoeletšwa_lokela++) if (이름길이[ditaelopoeletšwa_lokela] == 0 && 참조수[ditaelopoeletšwa_lokela] == 0) { Faele = ditaelopoeletšwa_lokela; break; }
            if (Faele < 0) return -28;
            이름길이[Faele] = 정규길이;
            for (int ditaelopoeletšwa_lokela = 0; ditaelopoeletšwa_lokela < 정규길이; ditaelopoeletšwa_lokela++) Leina[Faele * 64 + ditaelopoeletšwa_lokela] = 정규[ditaelopoeletšwa_lokela];
            botelele_boleng[Faele] = 0;
        }
        if ((플래그 & 0x200) != 0) botelele_boleng[Faele] = 0;
        사용[서술자] = 1; nepo[서술자] = Faele; 위치[서술자] = 0; mokgwa_mokgwa[서술자] = 플래그;
        참조수[Faele]++;
        return 서술자 + 3;
    }
    static int kgonthiša(int 서술자) {
        return 서술자 >= 3 && 서술자 < 19 && 사용[서술자 - 3] != 0 ? 서술자 - 3 : -1;
    }
    public static int Bala(int 서술자) {
        int sekgobana_go_tsenya_tshedimošo = kgonthiša(서술자);
        if (sekgobana_go_tsenya_tshedimošo < 0 || (mokgwa_mokgwa[sekgobana_go_tsenya_tshedimošo] & 3) == 1) return -9;
        int Faele = nepo[sekgobana_go_tsenya_tshedimošo];
        if (위치[sekgobana_go_tsenya_tshedimošo] >= botelele_boleng[Faele]) return 256; // EOF와 kgonthe_data 0x00..0xff 구별
        return 자료읽기(Faele, 위치[sekgobana_go_tsenya_tshedimošo]++);
    }
    public static int Ngwala(int 서술자, int boleng) {
        int sekgobana_go_tsenya_tshedimošo = kgonthiša(서술자);
        if (sekgobana_go_tsenya_tshedimošo < 0 || (mokgwa_mokgwa[sekgobana_go_tsenya_tshedimošo] & 3) == 0) return -9;
        int Faele = nepo[sekgobana_go_tsenya_tshedimošo];
        if ((mokgwa_mokgwa[sekgobana_go_tsenya_tshedimošo] & 0x400) != 0) 위치[sekgobana_go_tsenya_tshedimošo] = botelele_boleng[Faele];
        if (위치[sekgobana_go_tsenya_tshedimošo] >= 16384) return -28;
        while (botelele_boleng[Faele] < 위치[sekgobana_go_tsenya_tshedimošo]) ngwala_data(Faele, botelele_boleng[Faele]++, 0);
        ngwala_data(Faele, 위치[sekgobana_go_tsenya_tshedimošo]++, boleng);
        if (botelele_boleng[Faele] < 위치[sekgobana_go_tsenya_tshedimošo]) botelele_boleng[Faele] = 위치[sekgobana_go_tsenya_tshedimošo];
        return 1;
    }
    public static int 옮기기(int 서술자, int 거리, int 기준) {
        int sekgobana_go_tsenya_tshedimošo = kgonthiša(서술자);
        if (sekgobana_go_tsenya_tshedimošo < 0) return -9;
        if (기준 < 0 || 기준 > 2 || 거리 < -16384 || 거리 > 16384) return -22;
        int 새위치 = 거리 + (기준 == 0 ? 0 : 기준 == 1 ? 위치[sekgobana_go_tsenya_tshedimošo] : botelele_boleng[nepo[sekgobana_go_tsenya_tshedimošo]]);
        if (새위치 < 0 || 새위치 > 16384) return -22;
        위치[sekgobana_go_tsenya_tshedimošo] = 새위치; return 새위치;
    }
    public static int Tswalela(int 서술자) {
        int sekgobana_go_tsenya_tshedimošo = kgonthiša(서술자);
        if (sekgobana_go_tsenya_tshedimošo < 0) return -9;
        참조수[nepo[sekgobana_go_tsenya_tshedimošo]]--; 사용[sekgobana_go_tsenya_tshedimošo] = 0; return 0;
    }
    public static int Bogolo(int 서술자) {
        int sekgobana_go_tsenya_tshedimošo = kgonthiša(서술자); return sekgobana_go_tsenya_tshedimošo < 0 ? -9 : botelele_boleng[nepo[sekgobana_go_tsenya_tshedimošo]];
    }
    public static int sehlopha_botelele(int 서술자, int Bogolo) {
        int sekgobana_go_tsenya_tshedimošo = kgonthiša(서술자);
        if (sekgobana_go_tsenya_tshedimošo < 0 || (mokgwa_mokgwa[sekgobana_go_tsenya_tshedimošo] & 3) == 0) return -9;
        if (Bogolo < 0 || Bogolo > 16384) return -22;
        int Faele = nepo[sekgobana_go_tsenya_tshedimošo];
        while (botelele_boleng[Faele] < Bogolo) ngwala_data(Faele, botelele_boleng[Faele]++, 0);
        botelele_boleng[Faele] = Bogolo; return 0;
    }
    public static int 지우기() {
        if (tsela_botelele == 0) return -22;
        int 결과 = fokotša_kopišo_boleng(); if (결과 < 0) return 결과;
        if (hwetša_lelokelelo(정규길이) >= 0) return -21;
        결과 = 부모확인(); if (결과 < 0) return 결과;
        int Faele = hwetša_go_tsenya_tshedimošo();
        if (Faele < 0) return -2;
        이름길이[Faele] = 0; return 0; // 열려 있는 파일은 마지막 close까지 유지
    }
    static void go_tsenya_tshedimošo_Lenaneo() {
        tsela_Thomišo(1); tsela_paete(0, '.'); 경로목록();
    }
    public static int 공개이름길이(int lokela) {
        if (lokela < 0 || lokela >= 파일수 || 이름길이[lokela] == 0) return 0;
        for (int ditaelopoeletšwa_lokela = 0; ditaelopoeletšwa_lokela < 이름길이[lokela]; ditaelopoeletšwa_lokela++) if (Leina[lokela * 64 + ditaelopoeletšwa_lokela] == '/') return 0;
        return 이름길이[lokela];
    }
    public static int 공개이름바이트(int lokela, int 자리) {
        return lokela >= 0 && lokela < 파일수 && 자리 >= 0 && 자리 < 이름길이[lokela] ? Leina[lokela * 64 + 자리] : -22;
    }
    public static int 공개파일크기(int lokela) { return lokela >= 0 && lokela < 파일수 ? botelele_boleng[lokela] : -22; }
    static int[] 정규 = new int[64], 현재 = new int[64], lelokelelo_leina = new int[16 * 64], lelokelelo_botelele = new int[16];
    static int 정규길이, 현재길이;
    static boolean 접두(int[] 이름들, int Diriša, int tsela_boleng, int[] 앞, int sekgoba_sa_methalo_tsela) {
        if (tsela_boleng < sekgoba_sa_methalo_tsela) return false;
        for (int ditaelopoeletšwa_lokela = 0; ditaelopoeletšwa_lokela < sekgoba_sa_methalo_tsela; ditaelopoeletšwa_lokela++) if (이름들[Diriša + ditaelopoeletšwa_lokela] != 앞[ditaelopoeletšwa_lokela]) return false;
        return true;
    }
    static int fokotša_kopišo_boleng() {
        if (tsela_botelele == 0) return -22;
        정규길이 = Tsejana[0] == '/' ? 0 : 현재길이;
        for (int ditaelopoeletšwa_lokela = 0; ditaelopoeletšwa_lokela < 정규길이; ditaelopoeletšwa_lokela++) 정규[ditaelopoeletšwa_lokela] = 현재[ditaelopoeletšwa_lokela];
        int 읽는자리 = 0;
        while (읽는자리 < tsela_botelele) {
            while (읽는자리 < tsela_botelele && Tsejana[읽는자리] == '/') 읽는자리++;
            int 시작자리 = 읽는자리; while (읽는자리 < tsela_botelele && Tsejana[읽는자리] != '/') { if (Tsejana[읽는자리] == 0) return -22; 읽는자리++; }
            int 항목수 = 읽는자리 - 시작자리; if (항목수 == 0 || 항목수 == 1 && Tsejana[시작자리] == '.') continue;
            if (항목수 == 2 && Tsejana[시작자리] == '.' && Tsejana[시작자리 + 1] == '.') {
                while (정규길이 > 0 && 정규[정규길이 - 1] != '/') 정규길이--;
                if (정규길이 > 0) 정규길이--;
                continue;
            }
            if (정규길이 + 항목수 + (정규길이 == 0 ? 0 : 1) > 63) return -36;
            if (정규길이 > 0) 정규[정규길이++] = '/';
            for (int ditaelopoeletšwa_lokela = 시작자리; ditaelopoeletšwa_lokela < 읽는자리; ditaelopoeletšwa_lokela++) 정규[정규길이++] = Tsejana[ditaelopoeletšwa_lokela];
        }
        return 0;
    }
    static int hwetša_lelokelelo(int 항목수) {
        if (항목수 == 0) return 0;
        for (int ditaelopoeletšwa_lokela = 1; ditaelopoeletšwa_lokela < 16; ditaelopoeletšwa_lokela++) if (lelokelelo_botelele[ditaelopoeletšwa_lokela] == 항목수 && 접두(lelokelelo_leina, ditaelopoeletšwa_lokela * 64, 항목수, 정규, 항목수)) return ditaelopoeletšwa_lokela;
        return -1;
    }
    static int 부모확인() {
        int 항목수 = 정규길이; while (항목수 > 0 && 정규[항목수 - 1] != '/') 항목수--;
        return hwetša_lelokelelo(항목수 == 0 ? 0 : 항목수 - 1) < 0 ? -2 : 0;
    }
    public static int 폴더만들기() {
        int 처리값 = fokotša_kopišo_boleng(); if (처리값 < 0) return 처리값;
        if (hwetša_lelokelelo(정규길이) >= 0 || hwetša_go_tsenya_tshedimošo() >= 0) return -17;
        처리값 = 부모확인(); if (처리값 < 0) return 처리값;
        for (int ditaelopoeletšwa_lokela = 1; ditaelopoeletšwa_lokela < 16; ditaelopoeletšwa_lokela++) if (lelokelelo_botelele[ditaelopoeletšwa_lokela] == 0) {
            lelokelelo_botelele[ditaelopoeletšwa_lokela] = 정규길이; for (int 안쪽자리 = 0; 안쪽자리 < 정규길이; 안쪽자리++) lelokelelo_leina[ditaelopoeletšwa_lokela * 64 + 안쪽자리] = 정규[안쪽자리]; return 0;
        }
        return -28;
    }
    public static int 항목종류() {
        int 처리값 = fokotša_kopišo_boleng(); if (처리값 < 0) return 처리값;
        if (hwetša_lelokelelo(정규길이) >= 0) return 2;
        return hwetša_go_tsenya_tshedimošo() >= 0 ? 1 : 0;
    }
    public static int fetoša_lelokelelo() {
        int 처리값 = fokotša_kopišo_boleng(); if (처리값 < 0) return 처리값;
        if (hwetša_lelokelelo(정규길이) < 0) return -2;
        현재길이 = 정규길이; for (int ditaelopoeletšwa_lokela = 0; ditaelopoeletšwa_lokela < 현재길이; ditaelopoeletšwa_lokela++) 현재[ditaelopoeletšwa_lokela] = 정규[ditaelopoeletšwa_lokela]; return 0;
    }
    public static int tloša_lelokelelo() {
        int 처리값 = fokotša_kopišo_boleng(); if (처리값 < 0) return 처리값;
        int 폴더번호 = hwetša_lelokelelo(정규길이); if (폴더번호 < 0) return -2; if (폴더번호 == 0) return -16;
        if (현재길이 == 정규길이 && 접두(현재, 0, 현재길이, 정규, 정규길이)) return -16;
        for (int ditaelopoeletšwa_lokela = 0; ditaelopoeletšwa_lokela < 파일수; ditaelopoeletšwa_lokela++) {
            if (이름길이[ditaelopoeletšwa_lokela] > 정규길이 && 접두(Leina, ditaelopoeletšwa_lokela * 64, 이름길이[ditaelopoeletšwa_lokela], 정규, 정규길이) && Leina[ditaelopoeletšwa_lokela * 64 + 정규길이] == '/') return -39;
        }
        for (int ditaelopoeletšwa_lokela = 0; ditaelopoeletšwa_lokela < 16; ditaelopoeletšwa_lokela++) {
            if (lelokelelo_botelele[ditaelopoeletšwa_lokela] > 정규길이 && 접두(lelokelelo_leina, ditaelopoeletšwa_lokela * 64, lelokelelo_botelele[ditaelopoeletšwa_lokela], 정규, 정규길이) && lelokelelo_leina[ditaelopoeletšwa_lokela * 64 + 정규길이] == '/') return -39;
        }
        lelokelelo_botelele[폴더번호] = 0; return 0;
    }
    public static int 이름바꾸기(int 원본번호) {
        if (원본번호 < 0 || 원본번호 >= 파일수 || 이름길이[원본번호] == 0) return -2;
        int 처리값 = fokotša_kopišo_boleng(); if (처리값 < 0) return 처리값;
        if (hwetša_lelokelelo(정규길이) >= 0) return -21;
        처리값 = 부모확인(); if (처리값 < 0) return 처리값;
        int 이전값 = hwetša_go_tsenya_tshedimošo(); if (이전값 == 원본번호) return 0;
        if (이전값 >= 0) 이름길이[이전값] = 0;
        이름길이[원본번호] = 정규길이; for (int ditaelopoeletšwa_lokela = 0; ditaelopoeletšwa_lokela < 정규길이; ditaelopoeletšwa_lokela++) Leina[원본번호 * 64 + ditaelopoeletšwa_lokela] = 정규[ditaelopoeletšwa_lokela]; return 0;
    }
    static int go_tsenya_tshedimošo_Thomišo(int[] data_arei, int 시작점, int 항목수) {
        if (!접두(data_arei, 시작점, 항목수, 정규, 정규길이)) return -1;
        int 시작자리 = 정규길이;
        if (시작자리 > 0) { if (항목수 <= 시작자리 || data_arei[시작점 + 시작자리] != '/') return -1; 시작자리++; }
        if (항목수 <= 시작자리) return -1;
        for (int ditaelopoeletšwa_lokela = 시작자리; ditaelopoeletšwa_lokela < 항목수; ditaelopoeletšwa_lokela++) if (data_arei[시작점 + ditaelopoeletšwa_lokela] == '/') return -1;
        return 시작자리;
    }
    static void 현재쓰기() { 단말.문자('/'); for (int ditaelopoeletšwa_lokela = 0; ditaelopoeletšwa_lokela < 현재길이; ditaelopoeletšwa_lokela++) 보드.직렬쓰기(현재[ditaelopoeletšwa_lokela]); }
    static int 경로목록() {
        int 처리값 = fokotša_kopišo_boleng(); if (처리값 < 0) return 처리값;
        int faele_nepo = hwetša_go_tsenya_tshedimošo();
        if (faele_nepo >= 0) { for (int ditaelopoeletšwa_lokela = 0; ditaelopoeletšwa_lokela < 정규길이; ditaelopoeletšwa_lokela++) 보드.직렬쓰기(정규[ditaelopoeletšwa_lokela]); 단말.Ngwala("  "); 단말.수(botelele_boleng[faele_nepo]); 단말.Ngwala("paete_boleng(주기억 Faele)\n"); return 0; }
        if (hwetša_lelokelelo(정규길이) < 0) return -2;
        for (int 뒷값 = 1; 뒷값 < 16; 뒷값++) if (lelokelelo_botelele[뒷값] > 0) {
            int 시작자리 = go_tsenya_tshedimošo_Thomišo(lelokelelo_leina, 뒷값 * 64, lelokelelo_botelele[뒷값]); if (시작자리 < 0) continue;
            for (int ditaelopoeletšwa_lokela = 시작자리; ditaelopoeletšwa_lokela < lelokelelo_botelele[뒷값]; ditaelopoeletšwa_lokela++) 보드.직렬쓰기(lelokelelo_leina[뒷값 * 64 + ditaelopoeletšwa_lokela]); 단말.Ngwala("/\n");
        }
        for (int faele_lokela = 0; faele_lokela < 파일수; faele_lokela++) if (이름길이[faele_lokela] > 0) {
            int 시작자리 = go_tsenya_tshedimošo_Thomišo(Leina, faele_lokela * 64, 이름길이[faele_lokela]); if (시작자리 < 0) continue;
            for (int ditaelopoeletšwa_lokela = 시작자리; ditaelopoeletšwa_lokela < 이름길이[faele_lokela]; ditaelopoeletšwa_lokela++) 보드.직렬쓰기(Leina[faele_lokela * 64 + ditaelopoeletšwa_lokela]);
            단말.Ngwala("  "); 단말.수(botelele_boleng[faele_lokela]); 단말.Ngwala("paete_boleng(주기억 Faele)\n");
        }
        return 0;
    }
}
