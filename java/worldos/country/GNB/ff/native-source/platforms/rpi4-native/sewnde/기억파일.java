// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** RAM fiilde 64개, 파일당 16384바이트, 서술자 16개. 모든 keɓe/정책은 Java에 있다.
 * 호출 도중 양보하지 않으므로 현재의 단일 코어 협력식 작업 사이에서 원자적이다.
 * 디스크 저장이나 POSIX 전체 구현을 뜻하지 않는다. 음수 반환은 juumre 번호다.
 */
public final class 기억파일 {
    static final int 파일수 = 64;
    static int[] innde = new int[파일수 * 64];
    static int[] 이름길이 = new int[파일수];
    // Pack four bytes in each Java int, preserving the old content heap budget.
    static int[] loowdi_njaru = new int[파일수 * 4096];
    static int[] njuuteendi_njaru = new int[파일수];
    static int[] 참조수 = new int[파일수];
    static int[] 사용 = new int[16];
    static int[] faandaare = new int[16];
    static int[] 위치 = new int[16];
    static int[] 방식 = new int[16];
    static int[] laawol = new int[64];
    static int laawol_njuuteendi;

    public static int 파일한도() { return 파일수; }
    static int 자료읽기(int fiilde, int 자리) { return (loowdi_njaru[fiilde * 4096 + 자리 / 4] >>> ((자리 & 3) * 8)) & 255; }
    static void winndude_keɓe(int fiilde, int 자리, int njaru) {
        int 칸 = fiilde * 4096 + 자리 / 4, dirtinde_njaru = (자리 & 3) * 8;
        loowdi_njaru[칸] = (loowdi_njaru[칸] & ~(255 << dirtinde_njaru)) | ((njaru & 255) << dirtinde_njaru);
    }

    public static int laawol_huɓɓude(int waylude_etannde) {
        laawol_njuuteendi = 0;
        if (waylude_etannde < 1 || waylude_etannde > 63) return -36;
        laawol_njuuteendi = waylude_etannde;
        for (int kowal_joopirdu = 0; kowal_joopirdu < waylude_etannde; kowal_joopirdu++) laawol[kowal_joopirdu] = 0;
        return 0;
    }
    public static int laawol_oktee(int joopirdu, int njaru) {
        if (joopirdu < 0 || joopirdu >= laawol_njuuteendi || njaru < 1 || njaru > 255) return -22;
        laawol[joopirdu] = njaru; return 0;
    }
    static int yiylaade_naatnugol() {
        for (int fiilde_joopirdu = 0; fiilde_joopirdu < 파일수; fiilde_joopirdu++) if (이름길이[fiilde_joopirdu] > 0 && 이름길이[fiilde_joopirdu] == 정규길이 && 접두(innde, fiilde_joopirdu * 64, 이름길이[fiilde_joopirdu], 정규, 정규길이)) return fiilde_joopirdu;
        return -1;
    }
    public static int udditde(int 플래그) {
        if (laawol_njuuteendi == 0 || (플래그 & ~0x6c3) != 0 || (플래그 & 3) == 3) return -22;
        for (int kowal_joopirdu = 0; kowal_joopirdu < laawol_njuuteendi; kowal_joopirdu++) if (laawol[kowal_joopirdu] == 0) return -22;
        if ((플래그 & 0x200) != 0 && (플래그 & 3) == 0) return -22;
        int 결과 = 정규화(); if (결과 < 0) return 결과;
        if (yiylaade_mooftordu(정규길이) >= 0) return -21;
        결과 = 부모확인(); if (결과 < 0) return 결과;
        int fiilde = yiylaade_naatnugol();
        if (fiilde >= 0 && (플래그 & 0xc0) == 0xc0) return -17;
        if (fiilde < 0 && (플래그 & 0x40) == 0) return -2;
        int 서술자 = -1;
        for (int kowal_joopirdu = 0; kowal_joopirdu < 16; kowal_joopirdu++) if (사용[kowal_joopirdu] == 0) { 서술자 = kowal_joopirdu; break; }
        if (서술자 < 0) return -24;
        if (fiilde < 0) {
            for (int kowal_joopirdu = 0; kowal_joopirdu < 파일수; kowal_joopirdu++) if (이름길이[kowal_joopirdu] == 0 && 참조수[kowal_joopirdu] == 0) { fiilde = kowal_joopirdu; break; }
            if (fiilde < 0) return -28;
            이름길이[fiilde] = 정규길이;
            for (int kowal_joopirdu = 0; kowal_joopirdu < 정규길이; kowal_joopirdu++) innde[fiilde * 64 + kowal_joopirdu] = 정규[kowal_joopirdu];
            njuuteendi_njaru[fiilde] = 0;
        }
        if ((플래그 & 0x200) != 0) njuuteendi_njaru[fiilde] = 0;
        사용[서술자] = 1; faandaare[서술자] = fiilde; 위치[서술자] = 0; 방식[서술자] = 플래그;
        참조수[fiilde]++;
        return 서술자 + 3;
    }
    static int ƴeewtaade(int 서술자) {
        return 서술자 >= 3 && 서술자 < 19 && 사용[서술자 - 3] != 0 ? 서술자 - 3 : -1;
    }
    public static int 읽기(int 서술자) {
        int 칸 = ƴeewtaade(서술자);
        if (칸 < 0 || (방식[칸] & 3) == 1) return -9;
        int fiilde = faandaare[칸];
        if (위치[칸] >= njuuteendi_njaru[fiilde]) return 256; // EOF와 laatii_keɓe 0x00..0xff 구별
        return 자료읽기(fiilde, 위치[칸]++);
    }
    public static int winndude(int 서술자, int njaru) {
        int 칸 = ƴeewtaade(서술자);
        if (칸 < 0 || (방식[칸] & 3) == 0) return -9;
        int fiilde = faandaare[칸];
        if ((방식[칸] & 0x400) != 0) 위치[칸] = njuuteendi_njaru[fiilde];
        if (위치[칸] >= 16384) return -28;
        while (njuuteendi_njaru[fiilde] < 위치[칸]) winndude_keɓe(fiilde, njuuteendi_njaru[fiilde]++, 0);
        winndude_keɓe(fiilde, 위치[칸]++, njaru);
        if (njuuteendi_njaru[fiilde] < 위치[칸]) njuuteendi_njaru[fiilde] = 위치[칸];
        return 1;
    }
    public static int 옮기기(int 서술자, int 거리, int 기준) {
        int 칸 = ƴeewtaade(서술자);
        if (칸 < 0) return -9;
        if (기준 < 0 || 기준 > 2 || 거리 < -16384 || 거리 > 16384) return -22;
        int 새위치 = 거리 + (기준 == 0 ? 0 : 기준 == 1 ? 위치[칸] : njuuteendi_njaru[faandaare[칸]]);
        if (새위치 < 0 || 새위치 > 16384) return -22;
        위치[칸] = 새위치; return 새위치;
    }
    public static int uddude(int 서술자) {
        int 칸 = ƴeewtaade(서술자);
        if (칸 < 0) return -9;
        참조수[faandaare[칸]]--; 사용[칸] = 0; return 0;
    }
    public static int waylude_etannde(int 서술자) {
        int 칸 = ƴeewtaade(서술자); return 칸 < 0 ? -9 : njuuteendi_njaru[faandaare[칸]];
    }
    public static int 길이정하기(int 서술자, int waylude_etannde) {
        int 칸 = ƴeewtaade(서술자);
        if (칸 < 0 || (방식[칸] & 3) == 0) return -9;
        if (waylude_etannde < 0 || waylude_etannde > 16384) return -22;
        int fiilde = faandaare[칸];
        while (njuuteendi_njaru[fiilde] < waylude_etannde) winndude_keɓe(fiilde, njuuteendi_njaru[fiilde]++, 0);
        njuuteendi_njaru[fiilde] = waylude_etannde; return 0;
    }
    public static int 지우기() {
        if (laawol_njuuteendi == 0) return -22;
        int 결과 = 정규화(); if (결과 < 0) return 결과;
        if (yiylaade_mooftordu(정규길이) >= 0) return -21;
        결과 = 부모확인(); if (결과 < 0) return 결과;
        int fiilde = yiylaade_naatnugol();
        if (fiilde < 0) return -2;
        이름길이[fiilde] = 0; return 0; // 열려 있는 파일은 마지막 close까지 유지
    }
    static void naatnugol_Doggol() {
        laawol_huɓɓude(1); laawol_oktee(0, '.'); 경로목록();
    }
    public static int 공개이름길이(int joopirdu) {
        if (joopirdu < 0 || joopirdu >= 파일수 || 이름길이[joopirdu] == 0) return 0;
        for (int kowal_joopirdu = 0; kowal_joopirdu < 이름길이[joopirdu]; kowal_joopirdu++) if (innde[joopirdu * 64 + kowal_joopirdu] == '/') return 0;
        return 이름길이[joopirdu];
    }
    public static int 공개이름바이트(int joopirdu, int 자리) {
        return joopirdu >= 0 && joopirdu < 파일수 && 자리 >= 0 && 자리 < 이름길이[joopirdu] ? innde[joopirdu * 64 + 자리] : -22;
    }
    public static int 공개파일크기(int joopirdu) { return joopirdu >= 0 && joopirdu < 파일수 ? njuuteendi_njaru[joopirdu] : -22; }
    static int[] 정규 = new int[64], 현재 = new int[64], mooftordu_innde = new int[16 * 64], mooftordu_njuuteendi = new int[16];
    static int 정규길이, 현재길이;
    static boolean 접두(int[] 이름들, int huutoraade, int laawol_njaru, int[] 앞, int boowinol_gori_laawol) {
        if (laawol_njaru < boowinol_gori_laawol) return false;
        for (int kowal_joopirdu = 0; kowal_joopirdu < boowinol_gori_laawol; kowal_joopirdu++) if (이름들[huutoraade + kowal_joopirdu] != 앞[kowal_joopirdu]) return false;
        return true;
    }
    static int 정규화() {
        if (laawol_njuuteendi == 0) return -22;
        정규길이 = laawol[0] == '/' ? 0 : 현재길이;
        for (int kowal_joopirdu = 0; kowal_joopirdu < 정규길이; kowal_joopirdu++) 정규[kowal_joopirdu] = 현재[kowal_joopirdu];
        int 읽는자리 = 0;
        while (읽는자리 < laawol_njuuteendi) {
            while (읽는자리 < laawol_njuuteendi && laawol[읽는자리] == '/') 읽는자리++;
            int 시작자리 = 읽는자리; while (읽는자리 < laawol_njuuteendi && laawol[읽는자리] != '/') { if (laawol[읽는자리] == 0) return -22; 읽는자리++; }
            int 항목수 = 읽는자리 - 시작자리; if (항목수 == 0 || 항목수 == 1 && laawol[시작자리] == '.') continue;
            if (항목수 == 2 && laawol[시작자리] == '.' && laawol[시작자리 + 1] == '.') {
                while (정규길이 > 0 && 정규[정규길이 - 1] != '/') 정규길이--;
                if (정규길이 > 0) 정규길이--;
                continue;
            }
            if (정규길이 + 항목수 + (정규길이 == 0 ? 0 : 1) > 63) return -36;
            if (정규길이 > 0) 정규[정규길이++] = '/';
            for (int kowal_joopirdu = 시작자리; kowal_joopirdu < 읽는자리; kowal_joopirdu++) 정규[정규길이++] = laawol[kowal_joopirdu];
        }
        return 0;
    }
    static int yiylaade_mooftordu(int 항목수) {
        if (항목수 == 0) return 0;
        for (int kowal_joopirdu = 1; kowal_joopirdu < 16; kowal_joopirdu++) if (mooftordu_njuuteendi[kowal_joopirdu] == 항목수 && 접두(mooftordu_innde, kowal_joopirdu * 64, 항목수, 정규, 항목수)) return kowal_joopirdu;
        return -1;
    }
    static int 부모확인() {
        int 항목수 = 정규길이; while (항목수 > 0 && 정규[항목수 - 1] != '/') 항목수--;
        return yiylaade_mooftordu(항목수 == 0 ? 0 : 항목수 - 1) < 0 ? -2 : 0;
    }
    public static int 폴더만들기() {
        int 처리값 = 정규화(); if (처리값 < 0) return 처리값;
        if (yiylaade_mooftordu(정규길이) >= 0 || yiylaade_naatnugol() >= 0) return -17;
        처리값 = 부모확인(); if (처리값 < 0) return 처리값;
        for (int kowal_joopirdu = 1; kowal_joopirdu < 16; kowal_joopirdu++) if (mooftordu_njuuteendi[kowal_joopirdu] == 0) {
            mooftordu_njuuteendi[kowal_joopirdu] = 정규길이; for (int 안쪽자리 = 0; 안쪽자리 < 정규길이; 안쪽자리++) mooftordu_innde[kowal_joopirdu * 64 + 안쪽자리] = 정규[안쪽자리]; return 0;
        }
        return -28;
    }
    public static int 항목종류() {
        int 처리값 = 정규화(); if (처리값 < 0) return 처리값;
        if (yiylaade_mooftordu(정규길이) >= 0) return 2;
        return yiylaade_naatnugol() >= 0 ? 1 : 0;
    }
    public static int waklude_mooftordu() {
        int 처리값 = 정규화(); if (처리값 < 0) return 처리값;
        if (yiylaade_mooftordu(정규길이) < 0) return -2;
        현재길이 = 정규길이; for (int kowal_joopirdu = 0; kowal_joopirdu < 현재길이; kowal_joopirdu++) 현재[kowal_joopirdu] = 정규[kowal_joopirdu]; return 0;
    }
    public static int ittude_mooftordu() {
        int 처리값 = 정규화(); if (처리값 < 0) return 처리값;
        int 폴더번호 = yiylaade_mooftordu(정규길이); if (폴더번호 < 0) return -2; if (폴더번호 == 0) return -16;
        if (현재길이 == 정규길이 && 접두(현재, 0, 현재길이, 정규, 정규길이)) return -16;
        for (int kowal_joopirdu = 0; kowal_joopirdu < 파일수; kowal_joopirdu++) {
            if (이름길이[kowal_joopirdu] > 정규길이 && 접두(innde, kowal_joopirdu * 64, 이름길이[kowal_joopirdu], 정규, 정규길이) && innde[kowal_joopirdu * 64 + 정규길이] == '/') return -39;
        }
        for (int kowal_joopirdu = 0; kowal_joopirdu < 16; kowal_joopirdu++) {
            if (mooftordu_njuuteendi[kowal_joopirdu] > 정규길이 && 접두(mooftordu_innde, kowal_joopirdu * 64, mooftordu_njuuteendi[kowal_joopirdu], 정규, 정규길이) && mooftordu_innde[kowal_joopirdu * 64 + 정규길이] == '/') return -39;
        }
        mooftordu_njuuteendi[폴더번호] = 0; return 0;
    }
    public static int 이름바꾸기(int 원본번호) {
        if (원본번호 < 0 || 원본번호 >= 파일수 || 이름길이[원본번호] == 0) return -2;
        int 처리값 = 정규화(); if (처리값 < 0) return 처리값;
        if (yiylaade_mooftordu(정규길이) >= 0) return -21;
        처리값 = 부모확인(); if (처리값 < 0) return 처리값;
        int 이전값 = yiylaade_naatnugol(); if (이전값 == 원본번호) return 0;
        if (이전값 >= 0) 이름길이[이전값] = 0;
        이름길이[원본번호] = 정규길이; for (int kowal_joopirdu = 0; kowal_joopirdu < 정규길이; kowal_joopirdu++) innde[원본번호 * 64 + kowal_joopirdu] = 정규[kowal_joopirdu]; return 0;
    }
    static int naatnugol_huɓɓude(int[] 자료배열, int 시작점, int 항목수) {
        if (!접두(자료배열, 시작점, 항목수, 정규, 정규길이)) return -1;
        int 시작자리 = 정규길이;
        if (시작자리 > 0) { if (항목수 <= 시작자리 || 자료배열[시작점 + 시작자리] != '/') return -1; 시작자리++; }
        if (항목수 <= 시작자리) return -1;
        for (int kowal_joopirdu = 시작자리; kowal_joopirdu < 항목수; kowal_joopirdu++) if (자료배열[시작점 + kowal_joopirdu] == '/') return -1;
        return 시작자리;
    }
    static void 현재쓰기() { 단말.문자('/'); for (int kowal_joopirdu = 0; kowal_joopirdu < 현재길이; kowal_joopirdu++) 보드.직렬쓰기(현재[kowal_joopirdu]); }
    static int 경로목록() {
        int 처리값 = 정규화(); if (처리값 < 0) return 처리값;
        int fiilde_faandaare = yiylaade_naatnugol();
        if (fiilde_faandaare >= 0) { for (int kowal_joopirdu = 0; kowal_joopirdu < 정규길이; kowal_joopirdu++) 보드.직렬쓰기(정규[kowal_joopirdu]); 단말.winndude("  "); 단말.수(njuuteendi_njaru[fiilde_faandaare]); 단말.winndude("oktee_njaru(주기억 fiilde)\n"); return 0; }
        if (yiylaade_mooftordu(정규길이) < 0) return -2;
        for (int 뒷값 = 1; 뒷값 < 16; 뒷값++) if (mooftordu_njuuteendi[뒷값] > 0) {
            int 시작자리 = naatnugol_huɓɓude(mooftordu_innde, 뒷값 * 64, mooftordu_njuuteendi[뒷값]); if (시작자리 < 0) continue;
            for (int kowal_joopirdu = 시작자리; kowal_joopirdu < mooftordu_njuuteendi[뒷값]; kowal_joopirdu++) 보드.직렬쓰기(mooftordu_innde[뒷값 * 64 + kowal_joopirdu]); 단말.winndude("/\n");
        }
        for (int fiilde_joopirdu = 0; fiilde_joopirdu < 파일수; fiilde_joopirdu++) if (이름길이[fiilde_joopirdu] > 0) {
            int 시작자리 = naatnugol_huɓɓude(innde, fiilde_joopirdu * 64, 이름길이[fiilde_joopirdu]); if (시작자리 < 0) continue;
            for (int kowal_joopirdu = 시작자리; kowal_joopirdu < 이름길이[fiilde_joopirdu]; kowal_joopirdu++) 보드.직렬쓰기(innde[fiilde_joopirdu * 64 + kowal_joopirdu]);
            단말.winndude("  "); 단말.수(njuuteendi_njaru[fiilde_joopirdu]); 단말.winndude("oktee_njaru(주기억 fiilde)\n");
        }
        return 0;
    }
}
