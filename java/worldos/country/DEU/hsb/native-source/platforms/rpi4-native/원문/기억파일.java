// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** RAM Dataja 64개, 파일당 16384바이트, 서술자 16개. 모든 자료/정책은 Java에 있다.
 * 호출 도중 양보하지 않으므로 현재의 단일 코어 협력식 작업 사이에서 원자적이다.
 * 디스크 저장이나 POSIX 전체 구현을 뜻하지 않는다. 음수 반환은 Zmylk 번호다.
 */
public final class 기억파일 {
    static final int 파일수 = 64;
    static int[] Mjeno = new int[파일수 * 64];
    static int[] 이름길이 = new int[파일수];
    // Pack four bytes in each Java int, preserving the old content heap budget.
    static int[] 내용 = new int[파일수 * 4096];
    static int[] 길이 = new int[파일수];
    static int[] 참조수 = new int[파일수];
    static int[] 사용 = new int[16];
    static int[] 대상 = new int[16];
    static int[] 위치 = new int[16];
    static int[] 방식 = new int[16];
    static int[] 경로 = new int[64];
    static int 경로길이;

    public static int 파일한도() { return 파일수; }
    static int 자료읽기(int Dataja, int 자리) { return (내용[Dataja * 4096 + 자리 / 4] >>> ((자리 & 3) * 8)) & 255; }
    static void 자료쓰기(int Dataja, int 자리, int 값) {
        int 칸 = Dataja * 4096 + 자리 / 4, 이동 = (자리 & 3) * 8;
        내용[칸] = (내용[칸] & ~(255 << 이동)) | ((값 & 255) << 이동);
    }

    public static int 경로시작(int 크기) {
        경로길이 = 0;
        if (크기 < 1 || 크기 > 63) return -36;
        경로길이 = 크기;
        for (int 반복자리 = 0; 반복자리 < 크기; 반복자리++) 경로[반복자리] = 0;
        return 0;
    }
    public static int 경로바이트(int 번호, int 값) {
        if (번호 < 0 || 번호 >= 경로길이 || 값 < 1 || 값 > 255) return -22;
        경로[번호] = 값; return 0;
    }
    static int 찾기() {
        for (int 파일번호 = 0; 파일번호 < 파일수; 파일번호++) if (이름길이[파일번호] > 0 && 이름길이[파일번호] == 정규길이 && 접두(Mjeno, 파일번호 * 64, 이름길이[파일번호], 정규, 정규길이)) return 파일번호;
        return -1;
    }
    public static int Wočinić(int 플래그) {
        if (경로길이 == 0 || (플래그 & ~0x6c3) != 0 || (플래그 & 3) == 3) return -22;
        for (int 반복자리 = 0; 반복자리 < 경로길이; 반복자리++) if (경로[반복자리] == 0) return -22;
        if ((플래그 & 0x200) != 0 && (플래그 & 3) == 0) return -22;
        int 결과 = 정규화(); if (결과 < 0) return 결과;
        if (폴더찾기(정규길이) >= 0) return -21;
        결과 = 부모확인(); if (결과 < 0) return 결과;
        int Dataja = 찾기();
        if (Dataja >= 0 && (플래그 & 0xc0) == 0xc0) return -17;
        if (Dataja < 0 && (플래그 & 0x40) == 0) return -2;
        int 서술자 = -1;
        for (int 반복자리 = 0; 반복자리 < 16; 반복자리++) if (사용[반복자리] == 0) { 서술자 = 반복자리; break; }
        if (서술자 < 0) return -24;
        if (Dataja < 0) {
            for (int 반복자리 = 0; 반복자리 < 파일수; 반복자리++) if (이름길이[반복자리] == 0 && 참조수[반복자리] == 0) { Dataja = 반복자리; break; }
            if (Dataja < 0) return -28;
            이름길이[Dataja] = 정규길이;
            for (int 반복자리 = 0; 반복자리 < 정규길이; 반복자리++) Mjeno[Dataja * 64 + 반복자리] = 정규[반복자리];
            길이[Dataja] = 0;
        }
        if ((플래그 & 0x200) != 0) 길이[Dataja] = 0;
        사용[서술자] = 1; 대상[서술자] = Dataja; 위치[서술자] = 0; 방식[서술자] = 플래그;
        참조수[Dataja]++;
        return 서술자 + 3;
    }
    static int 확인(int 서술자) {
        return 서술자 >= 3 && 서술자 < 19 && 사용[서술자 - 3] != 0 ? 서술자 - 3 : -1;
    }
    public static int Čitać(int 서술자) {
        int 칸 = 확인(서술자);
        if (칸 < 0 || (방식[칸] & 3) == 1) return -9;
        int Dataja = 대상[칸];
        if (위치[칸] >= 길이[Dataja]) return 256; // EOF와 실제 0x00..0xff 구별
        return 자료읽기(Dataja, 위치[칸]++);
    }
    public static int Pisać(int 서술자, int 값) {
        int 칸 = 확인(서술자);
        if (칸 < 0 || (방식[칸] & 3) == 0) return -9;
        int Dataja = 대상[칸];
        if ((방식[칸] & 0x400) != 0) 위치[칸] = 길이[Dataja];
        if (위치[칸] >= 16384) return -28;
        while (길이[Dataja] < 위치[칸]) 자료쓰기(Dataja, 길이[Dataja]++, 0);
        자료쓰기(Dataja, 위치[칸]++, 값);
        if (길이[Dataja] < 위치[칸]) 길이[Dataja] = 위치[칸];
        return 1;
    }
    public static int 옮기기(int 서술자, int 거리, int 기준) {
        int 칸 = 확인(서술자);
        if (칸 < 0) return -9;
        if (기준 < 0 || 기준 > 2 || 거리 < -16384 || 거리 > 16384) return -22;
        int 새위치 = 거리 + (기준 == 0 ? 0 : 기준 == 1 ? 위치[칸] : 길이[대상[칸]]);
        if (새위치 < 0 || 새위치 > 16384) return -22;
        위치[칸] = 새위치; return 새위치;
    }
    public static int 닫기(int 서술자) {
        int 칸 = 확인(서술자);
        if (칸 < 0) return -9;
        참조수[대상[칸]]--; 사용[칸] = 0; return 0;
    }
    public static int 크기(int 서술자) {
        int 칸 = 확인(서술자); return 칸 < 0 ? -9 : 길이[대상[칸]];
    }
    public static int 길이정하기(int 서술자, int 크기) {
        int 칸 = 확인(서술자);
        if (칸 < 0 || (방식[칸] & 3) == 0) return -9;
        if (크기 < 0 || 크기 > 16384) return -22;
        int Dataja = 대상[칸];
        while (길이[Dataja] < 크기) 자료쓰기(Dataja, 길이[Dataja]++, 0);
        길이[Dataja] = 크기; return 0;
    }
    public static int 지우기() {
        if (경로길이 == 0) return -22;
        int 결과 = 정규화(); if (결과 < 0) return 결과;
        if (폴더찾기(정규길이) >= 0) return -21;
        결과 = 부모확인(); if (결과 < 0) return 결과;
        int Dataja = 찾기();
        if (Dataja < 0) return -2;
        이름길이[Dataja] = 0; return 0; // 열려 있는 파일은 마지막 close까지 유지
    }
    static void 목록() {
        경로시작(1); 경로바이트(0, '.'); 경로목록();
    }
    public static int 공개이름길이(int 번호) {
        if (번호 < 0 || 번호 >= 파일수 || 이름길이[번호] == 0) return 0;
        for (int 반복자리 = 0; 반복자리 < 이름길이[번호]; 반복자리++) if (Mjeno[번호 * 64 + 반복자리] == '/') return 0;
        return 이름길이[번호];
    }
    public static int 공개이름바이트(int 번호, int 자리) {
        return 번호 >= 0 && 번호 < 파일수 && 자리 >= 0 && 자리 < 이름길이[번호] ? Mjeno[번호 * 64 + 자리] : -22;
    }
    public static int 공개파일크기(int 번호) { return 번호 >= 0 && 번호 < 파일수 ? 길이[번호] : -22; }
    static int[] 정규 = new int[64], 현재 = new int[64], 폴더이름 = new int[16 * 64], 폴더길이 = new int[16];
    static int 정규길이, 현재길이;
    static boolean 접두(int[] 이름들, int 시작, int 길, int[] 앞, int 앞길) {
        if (길 < 앞길) return false;
        for (int 반복자리 = 0; 반복자리 < 앞길; 반복자리++) if (이름들[시작 + 반복자리] != 앞[반복자리]) return false;
        return true;
    }
    static int 정규화() {
        if (경로길이 == 0) return -22;
        정규길이 = 경로[0] == '/' ? 0 : 현재길이;
        for (int 반복자리 = 0; 반복자리 < 정규길이; 반복자리++) 정규[반복자리] = 현재[반복자리];
        int 읽는자리 = 0;
        while (읽는자리 < 경로길이) {
            while (읽는자리 < 경로길이 && 경로[읽는자리] == '/') 읽는자리++;
            int 시작자리 = 읽는자리; while (읽는자리 < 경로길이 && 경로[읽는자리] != '/') { if (경로[읽는자리] == 0) return -22; 읽는자리++; }
            int 항목수 = 읽는자리 - 시작자리; if (항목수 == 0 || 항목수 == 1 && 경로[시작자리] == '.') continue;
            if (항목수 == 2 && 경로[시작자리] == '.' && 경로[시작자리 + 1] == '.') {
                while (정규길이 > 0 && 정규[정규길이 - 1] != '/') 정규길이--;
                if (정규길이 > 0) 정규길이--;
                continue;
            }
            if (정규길이 + 항목수 + (정규길이 == 0 ? 0 : 1) > 63) return -36;
            if (정규길이 > 0) 정규[정규길이++] = '/';
            for (int 반복자리 = 시작자리; 반복자리 < 읽는자리; 반복자리++) 정규[정규길이++] = 경로[반복자리];
        }
        return 0;
    }
    static int 폴더찾기(int 항목수) {
        if (항목수 == 0) return 0;
        for (int 반복자리 = 1; 반복자리 < 16; 반복자리++) if (폴더길이[반복자리] == 항목수 && 접두(폴더이름, 반복자리 * 64, 항목수, 정규, 항목수)) return 반복자리;
        return -1;
    }
    static int 부모확인() {
        int 항목수 = 정규길이; while (항목수 > 0 && 정규[항목수 - 1] != '/') 항목수--;
        return 폴더찾기(항목수 == 0 ? 0 : 항목수 - 1) < 0 ? -2 : 0;
    }
    public static int 폴더만들기() {
        int 처리값 = 정규화(); if (처리값 < 0) return 처리값;
        if (폴더찾기(정규길이) >= 0 || 찾기() >= 0) return -17;
        처리값 = 부모확인(); if (처리값 < 0) return 처리값;
        for (int 반복자리 = 1; 반복자리 < 16; 반복자리++) if (폴더길이[반복자리] == 0) {
            폴더길이[반복자리] = 정규길이; for (int 안쪽자리 = 0; 안쪽자리 < 정규길이; 안쪽자리++) 폴더이름[반복자리 * 64 + 안쪽자리] = 정규[안쪽자리]; return 0;
        }
        return -28;
    }
    public static int 항목종류() {
        int 처리값 = 정규화(); if (처리값 < 0) return 처리값;
        if (폴더찾기(정규길이) >= 0) return 2;
        return 찾기() >= 0 ? 1 : 0;
    }
    public static int 폴더이동() {
        int 처리값 = 정규화(); if (처리값 < 0) return 처리값;
        if (폴더찾기(정규길이) < 0) return -2;
        현재길이 = 정규길이; for (int 반복자리 = 0; 반복자리 < 현재길이; 반복자리++) 현재[반복자리] = 정규[반복자리]; return 0;
    }
    public static int 폴더지우기() {
        int 처리값 = 정규화(); if (처리값 < 0) return 처리값;
        int 폴더번호 = 폴더찾기(정규길이); if (폴더번호 < 0) return -2; if (폴더번호 == 0) return -16;
        if (현재길이 == 정규길이 && 접두(현재, 0, 현재길이, 정규, 정규길이)) return -16;
        for (int 반복자리 = 0; 반복자리 < 파일수; 반복자리++) {
            if (이름길이[반복자리] > 정규길이 && 접두(Mjeno, 반복자리 * 64, 이름길이[반복자리], 정규, 정규길이) && Mjeno[반복자리 * 64 + 정규길이] == '/') return -39;
        }
        for (int 반복자리 = 0; 반복자리 < 16; 반복자리++) {
            if (폴더길이[반복자리] > 정규길이 && 접두(폴더이름, 반복자리 * 64, 폴더길이[반복자리], 정규, 정규길이) && 폴더이름[반복자리 * 64 + 정규길이] == '/') return -39;
        }
        폴더길이[폴더번호] = 0; return 0;
    }
    public static int 이름바꾸기(int 원본번호) {
        if (원본번호 < 0 || 원본번호 >= 파일수 || 이름길이[원본번호] == 0) return -2;
        int 처리값 = 정규화(); if (처리값 < 0) return 처리값;
        if (폴더찾기(정규길이) >= 0) return -21;
        처리값 = 부모확인(); if (처리값 < 0) return 처리값;
        int 이전값 = 찾기(); if (이전값 == 원본번호) return 0;
        if (이전값 >= 0) 이름길이[이전값] = 0;
        이름길이[원본번호] = 정규길이; for (int 반복자리 = 0; 반복자리 < 정규길이; 반복자리++) Mjeno[원본번호 * 64 + 반복자리] = 정규[반복자리]; return 0;
    }
    static int 항목시작(int[] 자료배열, int 시작점, int 항목수) {
        if (!접두(자료배열, 시작점, 항목수, 정규, 정규길이)) return -1;
        int 시작자리 = 정규길이;
        if (시작자리 > 0) { if (항목수 <= 시작자리 || 자료배열[시작점 + 시작자리] != '/') return -1; 시작자리++; }
        if (항목수 <= 시작자리) return -1;
        for (int 반복자리 = 시작자리; 반복자리 < 항목수; 반복자리++) if (자료배열[시작점 + 반복자리] == '/') return -1;
        return 시작자리;
    }
    static void 현재쓰기() { 단말.문자('/'); for (int 반복자리 = 0; 반복자리 < 현재길이; 반복자리++) 보드.직렬쓰기(현재[반복자리]); }
    static int 경로목록() {
        int 처리값 = 정규화(); if (처리값 < 0) return 처리값;
        int 파일대상 = 찾기();
        if (파일대상 >= 0) { for (int 반복자리 = 0; 반복자리 < 정규길이; 반복자리++) 보드.직렬쓰기(정규[반복자리]); 단말.Pisać("  "); 단말.수(길이[파일대상]); 단말.Pisać("바이트(주기억 Dataja)\n"); return 0; }
        if (폴더찾기(정규길이) < 0) return -2;
        for (int 뒷값 = 1; 뒷값 < 16; 뒷값++) if (폴더길이[뒷값] > 0) {
            int 시작자리 = 항목시작(폴더이름, 뒷값 * 64, 폴더길이[뒷값]); if (시작자리 < 0) continue;
            for (int 반복자리 = 시작자리; 반복자리 < 폴더길이[뒷값]; 반복자리++) 보드.직렬쓰기(폴더이름[뒷값 * 64 + 반복자리]); 단말.Pisać("/\n");
        }
        for (int 파일번호 = 0; 파일번호 < 파일수; 파일번호++) if (이름길이[파일번호] > 0) {
            int 시작자리 = 항목시작(Mjeno, 파일번호 * 64, 이름길이[파일번호]); if (시작자리 < 0) continue;
            for (int 반복자리 = 시작자리; 반복자리 < 이름길이[파일번호]; 반복자리++) 보드.직렬쓰기(Mjeno[파일번호 * 64 + 반복자리]);
            단말.Pisać("  "); 단말.수(길이[파일번호]); 단말.Pisać("바이트(주기억 Dataja)\n");
        }
        return 0;
    }
}
