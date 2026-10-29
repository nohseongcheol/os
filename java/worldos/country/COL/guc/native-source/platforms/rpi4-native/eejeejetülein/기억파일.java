// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** RAM anaajaalaa 64개, 파일당 16384바이트, 서술자 16개. 모든 atijaaya/정책은 Java에 있다.
 * 호출 도중 양보하지 않으므로 현재의 단일 코어 협력식 작업 사이에서 원자적이다.
 * 디스크 저장이나 POSIX 전체 구현을 뜻하지 않는다. 음수 반환은 ajachitia 번호다.
 */
public final class 기억파일 {
    static final int 파일수 = 64;
    static int[] 이름 = new int[파일수 * 64];
    static int[] 이름길이 = new int[파일수];
    // Pack four bytes in each Java int, preserving the old content heap budget.
    static int[] alu_ujatüü_ajutuu = new int[파일수 * 4096];
    static int[] akaliaa_ajutuu = new int[파일수];
    static int[] 참조수 = new int[파일수];
    static int[] 사용 = new int[16];
    static int[] 대상 = new int[16];
    static int[] 위치 = new int[16];
    static int[] 방식 = new int[16];
    static int[] wopu_a_ttaaleemüin = new int[64];
    static int wopu_a_ttaaleemüin_akaliaa;

    public static int 파일한도() { return 파일수; }
    static int 자료읽기(int anaajaalaa, int 자리) { return (alu_ujatüü_ajutuu[anaajaalaa * 4096 + 자리 / 4] >>> ((자리 & 3) * 8)) & 255; }
    static void ashajaa_atijaaya(int anaajaalaa, int 자리, int ajutuu) {
        int 칸 = anaajaalaa * 4096 + 자리 / 4, 이동 = (자리 & 3) * 8;
        alu_ujatüü_ajutuu[칸] = (alu_ujatüü_ajutuu[칸] & ~(255 << 이동)) | ((ajutuu & 255) << 이동);
    }

    public static int wopu_a_ttaaleemüin_achuwalaa(int 크기) {
        wopu_a_ttaaleemüin_akaliaa = 0;
        if (크기 < 1 || 크기 > 63) return -36;
        wopu_a_ttaaleemüin_akaliaa = 크기;
        for (int eitawaakualü_ee_iyatialujuna = 0; eitawaakualü_ee_iyatialujuna < 크기; eitawaakualü_ee_iyatialujuna++) wopu_a_ttaaleemüin[eitawaakualü_ee_iyatialujuna] = 0;
        return 0;
    }
    public static int wopu_a_ttaaleemüin_waai(int ee_iyatialujuna, int ajutuu) {
        if (ee_iyatialujuna < 0 || ee_iyatialujuna >= wopu_a_ttaaleemüin_akaliaa || ajutuu < 1 || ajutuu > 255) return -22;
        wopu_a_ttaaleemüin[ee_iyatialujuna] = ajutuu; return 0;
    }
    static int 찾기() {
        for (int anaajaalaa_ee_iyatialujuna = 0; anaajaalaa_ee_iyatialujuna < 파일수; anaajaalaa_ee_iyatialujuna++) if (이름길이[anaajaalaa_ee_iyatialujuna] > 0 && 이름길이[anaajaalaa_ee_iyatialujuna] == 정규길이 && 접두(이름, anaajaalaa_ee_iyatialujuna * 64, 이름길이[anaajaalaa_ee_iyatialujuna], 정규, 정규길이)) return anaajaalaa_ee_iyatialujuna;
        return -1;
    }
    public static int 열기(int 플래그) {
        if (wopu_a_ttaaleemüin_akaliaa == 0 || (플래그 & ~0x6c3) != 0 || (플래그 & 3) == 3) return -22;
        for (int eitawaakualü_ee_iyatialujuna = 0; eitawaakualü_ee_iyatialujuna < wopu_a_ttaaleemüin_akaliaa; eitawaakualü_ee_iyatialujuna++) if (wopu_a_ttaaleemüin[eitawaakualü_ee_iyatialujuna] == 0) return -22;
        if ((플래그 & 0x200) != 0 && (플래그 & 3) == 0) return -22;
        int 결과 = anaajaa_ajutuu(); if (결과 < 0) return 결과;
        if (폴더찾기(정규길이) >= 0) return -21;
        결과 = 부모확인(); if (결과 < 0) return 결과;
        int anaajaalaa = 찾기();
        if (anaajaalaa >= 0 && (플래그 & 0xc0) == 0xc0) return -17;
        if (anaajaalaa < 0 && (플래그 & 0x40) == 0) return -2;
        int 서술자 = -1;
        for (int eitawaakualü_ee_iyatialujuna = 0; eitawaakualü_ee_iyatialujuna < 16; eitawaakualü_ee_iyatialujuna++) if (사용[eitawaakualü_ee_iyatialujuna] == 0) { 서술자 = eitawaakualü_ee_iyatialujuna; break; }
        if (서술자 < 0) return -24;
        if (anaajaalaa < 0) {
            for (int eitawaakualü_ee_iyatialujuna = 0; eitawaakualü_ee_iyatialujuna < 파일수; eitawaakualü_ee_iyatialujuna++) if (이름길이[eitawaakualü_ee_iyatialujuna] == 0 && 참조수[eitawaakualü_ee_iyatialujuna] == 0) { anaajaalaa = eitawaakualü_ee_iyatialujuna; break; }
            if (anaajaalaa < 0) return -28;
            이름길이[anaajaalaa] = 정규길이;
            for (int eitawaakualü_ee_iyatialujuna = 0; eitawaakualü_ee_iyatialujuna < 정규길이; eitawaakualü_ee_iyatialujuna++) 이름[anaajaalaa * 64 + eitawaakualü_ee_iyatialujuna] = 정규[eitawaakualü_ee_iyatialujuna];
            akaliaa_ajutuu[anaajaalaa] = 0;
        }
        if ((플래그 & 0x200) != 0) akaliaa_ajutuu[anaajaalaa] = 0;
        사용[서술자] = 1; 대상[서술자] = anaajaalaa; 위치[서술자] = 0; 방식[서술자] = 플래그;
        참조수[anaajaalaa]++;
        return 서술자 + 3;
    }
    static int 확인(int 서술자) {
        return 서술자 >= 3 && 서술자 < 19 && 사용[서술자 - 3] != 0 ? 서술자 - 3 : -1;
    }
    public static int 읽기(int 서술자) {
        int 칸 = 확인(서술자);
        if (칸 < 0 || (방식[칸] & 3) == 1) return -9;
        int anaajaalaa = 대상[칸];
        if (위치[칸] >= akaliaa_ajutuu[anaajaalaa]) return 256; // EOF와 실제 0x00..0xff 구별
        return 자료읽기(anaajaalaa, 위치[칸]++);
    }
    public static int ashajaa(int 서술자, int ajutuu) {
        int 칸 = 확인(서술자);
        if (칸 < 0 || (방식[칸] & 3) == 0) return -9;
        int anaajaalaa = 대상[칸];
        if ((방식[칸] & 0x400) != 0) 위치[칸] = akaliaa_ajutuu[anaajaalaa];
        if (위치[칸] >= 16384) return -28;
        while (akaliaa_ajutuu[anaajaalaa] < 위치[칸]) ashajaa_atijaaya(anaajaalaa, akaliaa_ajutuu[anaajaalaa]++, 0);
        ashajaa_atijaaya(anaajaalaa, 위치[칸]++, ajutuu);
        if (akaliaa_ajutuu[anaajaalaa] < 위치[칸]) akaliaa_ajutuu[anaajaalaa] = 위치[칸];
        return 1;
    }
    public static int 옮기기(int 서술자, int 거리, int 기준) {
        int 칸 = 확인(서술자);
        if (칸 < 0) return -9;
        if (기준 < 0 || 기준 > 2 || 거리 < -16384 || 거리 > 16384) return -22;
        int 새위치 = 거리 + (기준 == 0 ? 0 : 기준 == 1 ? 위치[칸] : akaliaa_ajutuu[대상[칸]]);
        if (새위치 < 0 || 새위치 > 16384) return -22;
        위치[칸] = 새위치; return 새위치;
    }
    public static int asürülaa(int 서술자) {
        int 칸 = 확인(서술자);
        if (칸 < 0) return -9;
        참조수[대상[칸]]--; 사용[칸] = 0; return 0;
    }
    public static int 크기(int 서술자) {
        int 칸 = 확인(서술자); return 칸 < 0 ? -9 : akaliaa_ajutuu[대상[칸]];
    }
    public static int 길이정하기(int 서술자, int 크기) {
        int 칸 = 확인(서술자);
        if (칸 < 0 || (방식[칸] & 3) == 0) return -9;
        if (크기 < 0 || 크기 > 16384) return -22;
        int anaajaalaa = 대상[칸];
        while (akaliaa_ajutuu[anaajaalaa] < 크기) ashajaa_atijaaya(anaajaalaa, akaliaa_ajutuu[anaajaalaa]++, 0);
        akaliaa_ajutuu[anaajaalaa] = 크기; return 0;
    }
    public static int 지우기() {
        if (wopu_a_ttaaleemüin_akaliaa == 0) return -22;
        int 결과 = anaajaa_ajutuu(); if (결과 < 0) return 결과;
        if (폴더찾기(정규길이) >= 0) return -21;
        결과 = 부모확인(); if (결과 < 0) return 결과;
        int anaajaalaa = 찾기();
        if (anaajaalaa < 0) return -2;
        이름길이[anaajaalaa] = 0; return 0; // 열려 있는 파일은 마지막 close까지 유지
    }
    static void 목록() {
        wopu_a_ttaaleemüin_achuwalaa(1); wopu_a_ttaaleemüin_waai(0, '.'); 경로목록();
    }
    public static int 공개이름길이(int ee_iyatialujuna) {
        if (ee_iyatialujuna < 0 || ee_iyatialujuna >= 파일수 || 이름길이[ee_iyatialujuna] == 0) return 0;
        for (int eitawaakualü_ee_iyatialujuna = 0; eitawaakualü_ee_iyatialujuna < 이름길이[ee_iyatialujuna]; eitawaakualü_ee_iyatialujuna++) if (이름[ee_iyatialujuna * 64 + eitawaakualü_ee_iyatialujuna] == '/') return 0;
        return 이름길이[ee_iyatialujuna];
    }
    public static int 공개이름바이트(int ee_iyatialujuna, int 자리) {
        return ee_iyatialujuna >= 0 && ee_iyatialujuna < 파일수 && 자리 >= 0 && 자리 < 이름길이[ee_iyatialujuna] ? 이름[ee_iyatialujuna * 64 + 자리] : -22;
    }
    public static int 공개파일크기(int ee_iyatialujuna) { return ee_iyatialujuna >= 0 && ee_iyatialujuna < 파일수 ? akaliaa_ajutuu[ee_iyatialujuna] : -22; }
    static int[] 정규 = new int[64], 현재 = new int[64], 폴더이름 = new int[16 * 64], anaajaalee_akaliaa = new int[16];
    static int 정규길이, 현재길이;
    static boolean 접두(int[] 이름들, int 시작, int wopu_a_ttaaleemüin_ajutuu, int[] 앞, int a_wanajia_liiniakatalia_wopu_a_ttaaleemüin) {
        if (wopu_a_ttaaleemüin_ajutuu < a_wanajia_liiniakatalia_wopu_a_ttaaleemüin) return false;
        for (int eitawaakualü_ee_iyatialujuna = 0; eitawaakualü_ee_iyatialujuna < a_wanajia_liiniakatalia_wopu_a_ttaaleemüin; eitawaakualü_ee_iyatialujuna++) if (이름들[시작 + eitawaakualü_ee_iyatialujuna] != 앞[eitawaakualü_ee_iyatialujuna]) return false;
        return true;
    }
    static int anaajaa_ajutuu() {
        if (wopu_a_ttaaleemüin_akaliaa == 0) return -22;
        정규길이 = wopu_a_ttaaleemüin[0] == '/' ? 0 : 현재길이;
        for (int eitawaakualü_ee_iyatialujuna = 0; eitawaakualü_ee_iyatialujuna < 정규길이; eitawaakualü_ee_iyatialujuna++) 정규[eitawaakualü_ee_iyatialujuna] = 현재[eitawaakualü_ee_iyatialujuna];
        int 읽는자리 = 0;
        while (읽는자리 < wopu_a_ttaaleemüin_akaliaa) {
            while (읽는자리 < wopu_a_ttaaleemüin_akaliaa && wopu_a_ttaaleemüin[읽는자리] == '/') 읽는자리++;
            int 시작자리 = 읽는자리; while (읽는자리 < wopu_a_ttaaleemüin_akaliaa && wopu_a_ttaaleemüin[읽는자리] != '/') { if (wopu_a_ttaaleemüin[읽는자리] == 0) return -22; 읽는자리++; }
            int 항목수 = 읽는자리 - 시작자리; if (항목수 == 0 || 항목수 == 1 && wopu_a_ttaaleemüin[시작자리] == '.') continue;
            if (항목수 == 2 && wopu_a_ttaaleemüin[시작자리] == '.' && wopu_a_ttaaleemüin[시작자리 + 1] == '.') {
                while (정규길이 > 0 && 정규[정규길이 - 1] != '/') 정규길이--;
                if (정규길이 > 0) 정규길이--;
                continue;
            }
            if (정규길이 + 항목수 + (정규길이 == 0 ? 0 : 1) > 63) return -36;
            if (정규길이 > 0) 정규[정규길이++] = '/';
            for (int eitawaakualü_ee_iyatialujuna = 시작자리; eitawaakualü_ee_iyatialujuna < 읽는자리; eitawaakualü_ee_iyatialujuna++) 정규[정규길이++] = wopu_a_ttaaleemüin[eitawaakualü_ee_iyatialujuna];
        }
        return 0;
    }
    static int 폴더찾기(int 항목수) {
        if (항목수 == 0) return 0;
        for (int eitawaakualü_ee_iyatialujuna = 1; eitawaakualü_ee_iyatialujuna < 16; eitawaakualü_ee_iyatialujuna++) if (anaajaalee_akaliaa[eitawaakualü_ee_iyatialujuna] == 항목수 && 접두(폴더이름, eitawaakualü_ee_iyatialujuna * 64, 항목수, 정규, 항목수)) return eitawaakualü_ee_iyatialujuna;
        return -1;
    }
    static int 부모확인() {
        int 항목수 = 정규길이; while (항목수 > 0 && 정규[항목수 - 1] != '/') 항목수--;
        return 폴더찾기(항목수 == 0 ? 0 : 항목수 - 1) < 0 ? -2 : 0;
    }
    public static int 폴더만들기() {
        int 처리값 = anaajaa_ajutuu(); if (처리값 < 0) return 처리값;
        if (폴더찾기(정규길이) >= 0 || 찾기() >= 0) return -17;
        처리값 = 부모확인(); if (처리값 < 0) return 처리값;
        for (int eitawaakualü_ee_iyatialujuna = 1; eitawaakualü_ee_iyatialujuna < 16; eitawaakualü_ee_iyatialujuna++) if (anaajaalee_akaliaa[eitawaakualü_ee_iyatialujuna] == 0) {
            anaajaalee_akaliaa[eitawaakualü_ee_iyatialujuna] = 정규길이; for (int 안쪽자리 = 0; 안쪽자리 < 정규길이; 안쪽자리++) 폴더이름[eitawaakualü_ee_iyatialujuna * 64 + 안쪽자리] = 정규[안쪽자리]; return 0;
        }
        return -28;
    }
    public static int 항목종류() {
        int 처리값 = anaajaa_ajutuu(); if (처리값 < 0) return 처리값;
        if (폴더찾기(정규길이) >= 0) return 2;
        return 찾기() >= 0 ? 1 : 0;
    }
    public static int 폴더이동() {
        int 처리값 = anaajaa_ajutuu(); if (처리값 < 0) return 처리값;
        if (폴더찾기(정규길이) < 0) return -2;
        현재길이 = 정규길이; for (int eitawaakualü_ee_iyatialujuna = 0; eitawaakualü_ee_iyatialujuna < 현재길이; eitawaakualü_ee_iyatialujuna++) 현재[eitawaakualü_ee_iyatialujuna] = 정규[eitawaakualü_ee_iyatialujuna]; return 0;
    }
    public static int 폴더지우기() {
        int 처리값 = anaajaa_ajutuu(); if (처리값 < 0) return 처리값;
        int 폴더번호 = 폴더찾기(정규길이); if (폴더번호 < 0) return -2; if (폴더번호 == 0) return -16;
        if (현재길이 == 정규길이 && 접두(현재, 0, 현재길이, 정규, 정규길이)) return -16;
        for (int eitawaakualü_ee_iyatialujuna = 0; eitawaakualü_ee_iyatialujuna < 파일수; eitawaakualü_ee_iyatialujuna++) {
            if (이름길이[eitawaakualü_ee_iyatialujuna] > 정규길이 && 접두(이름, eitawaakualü_ee_iyatialujuna * 64, 이름길이[eitawaakualü_ee_iyatialujuna], 정규, 정규길이) && 이름[eitawaakualü_ee_iyatialujuna * 64 + 정규길이] == '/') return -39;
        }
        for (int eitawaakualü_ee_iyatialujuna = 0; eitawaakualü_ee_iyatialujuna < 16; eitawaakualü_ee_iyatialujuna++) {
            if (anaajaalee_akaliaa[eitawaakualü_ee_iyatialujuna] > 정규길이 && 접두(폴더이름, eitawaakualü_ee_iyatialujuna * 64, anaajaalee_akaliaa[eitawaakualü_ee_iyatialujuna], 정규, 정규길이) && 폴더이름[eitawaakualü_ee_iyatialujuna * 64 + 정규길이] == '/') return -39;
        }
        anaajaalee_akaliaa[폴더번호] = 0; return 0;
    }
    public static int 이름바꾸기(int 원본번호) {
        if (원본번호 < 0 || 원본번호 >= 파일수 || 이름길이[원본번호] == 0) return -2;
        int 처리값 = anaajaa_ajutuu(); if (처리값 < 0) return 처리값;
        if (폴더찾기(정규길이) >= 0) return -21;
        처리값 = 부모확인(); if (처리값 < 0) return 처리값;
        int 이전값 = 찾기(); if (이전값 == 원본번호) return 0;
        if (이전값 >= 0) 이름길이[이전값] = 0;
        이름길이[원본번호] = 정규길이; for (int eitawaakualü_ee_iyatialujuna = 0; eitawaakualü_ee_iyatialujuna < 정규길이; eitawaakualü_ee_iyatialujuna++) 이름[원본번호 * 64 + eitawaakualü_ee_iyatialujuna] = 정규[eitawaakualü_ee_iyatialujuna]; return 0;
    }
    static int ekeroliaa_achuwalaa(int[] atijaaya_matüriisü, int 시작점, int 항목수) {
        if (!접두(atijaaya_matüriisü, 시작점, 항목수, 정규, 정규길이)) return -1;
        int 시작자리 = 정규길이;
        if (시작자리 > 0) { if (항목수 <= 시작자리 || atijaaya_matüriisü[시작점 + 시작자리] != '/') return -1; 시작자리++; }
        if (항목수 <= 시작자리) return -1;
        for (int eitawaakualü_ee_iyatialujuna = 시작자리; eitawaakualü_ee_iyatialujuna < 항목수; eitawaakualü_ee_iyatialujuna++) if (atijaaya_matüriisü[시작점 + eitawaakualü_ee_iyatialujuna] == '/') return -1;
        return 시작자리;
    }
    static void 현재쓰기() { 단말.문자('/'); for (int eitawaakualü_ee_iyatialujuna = 0; eitawaakualü_ee_iyatialujuna < 현재길이; eitawaakualü_ee_iyatialujuna++) 보드.직렬쓰기(현재[eitawaakualü_ee_iyatialujuna]); }
    static int 경로목록() {
        int 처리값 = anaajaa_ajutuu(); if (처리값 < 0) return 처리값;
        int 파일대상 = 찾기();
        if (파일대상 >= 0) { for (int eitawaakualü_ee_iyatialujuna = 0; eitawaakualü_ee_iyatialujuna < 정규길이; eitawaakualü_ee_iyatialujuna++) 보드.직렬쓰기(정규[eitawaakualü_ee_iyatialujuna]); 단말.ashajaa("  "); 단말.수(akaliaa_ajutuu[파일대상]); 단말.ashajaa("waai_ajutuu(주기억 anaajaalaa)\n"); return 0; }
        if (폴더찾기(정규길이) < 0) return -2;
        for (int 뒷값 = 1; 뒷값 < 16; 뒷값++) if (anaajaalee_akaliaa[뒷값] > 0) {
            int 시작자리 = ekeroliaa_achuwalaa(폴더이름, 뒷값 * 64, anaajaalee_akaliaa[뒷값]); if (시작자리 < 0) continue;
            for (int eitawaakualü_ee_iyatialujuna = 시작자리; eitawaakualü_ee_iyatialujuna < anaajaalee_akaliaa[뒷값]; eitawaakualü_ee_iyatialujuna++) 보드.직렬쓰기(폴더이름[뒷값 * 64 + eitawaakualü_ee_iyatialujuna]); 단말.ashajaa("/\n");
        }
        for (int anaajaalaa_ee_iyatialujuna = 0; anaajaalaa_ee_iyatialujuna < 파일수; anaajaalaa_ee_iyatialujuna++) if (이름길이[anaajaalaa_ee_iyatialujuna] > 0) {
            int 시작자리 = ekeroliaa_achuwalaa(이름, anaajaalaa_ee_iyatialujuna * 64, 이름길이[anaajaalaa_ee_iyatialujuna]); if (시작자리 < 0) continue;
            for (int eitawaakualü_ee_iyatialujuna = 시작자리; eitawaakualü_ee_iyatialujuna < 이름길이[anaajaalaa_ee_iyatialujuna]; eitawaakualü_ee_iyatialujuna++) 보드.직렬쓰기(이름[anaajaalaa_ee_iyatialujuna * 64 + eitawaakualü_ee_iyatialujuna]);
            단말.ashajaa("  "); 단말.수(akaliaa_ajutuu[anaajaalaa_ee_iyatialujuna]); 단말.ashajaa("waai_ajutuu(주기억 anaajaalaa)\n");
        }
        return 0;
    }
}
