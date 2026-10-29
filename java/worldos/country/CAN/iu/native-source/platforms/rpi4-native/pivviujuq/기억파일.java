// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** RAM ini 64개, 파일당 16384바이트, 서술자 16개. 모든 titiqqat/정책은 Java에 있다.
 * 호출 도중 양보하지 않으므로 현재의 단일 코어 협력식 작업 사이에서 원자적이다.
 * 디스크 저장이나 POSIX 전체 구현을 뜻하지 않는다. 음수 반환은 tammarniq 번호다.
 */
public final class 기억파일 {
    static final int 파일수 = 64;
    static int[] atiq = new int[파일수 * 64];
    static int[] 이름길이 = new int[파일수];
    // Pack four bytes in each Java int, preserving the old content heap budget.
    static int[] Ilulingit_atuutilik = new int[파일수 * 4096];
    static int[] takininga_atuutilik = new int[파일수];
    static int[] 참조수 = new int[파일수];
    static int[] 사용 = new int[16];
    static int[] turaagaq = new int[16];
    static int[] 위치 = new int[16];
    static int[] 방식 = new int[16];
    static int[] aqqut = new int[64];
    static int aqqut_takininga;

    public static int 파일한도() { return 파일수; }
    static int 자료읽기(int ini, int 자리) { return (Ilulingit_atuutilik[ini * 4096 + 자리 / 4] >>> ((자리 & 3) * 8)) & 255; }
    static void titiraq_titiqqat(int ini, int 자리, int atuutilik) {
        int 칸 = ini * 4096 + 자리 / 4, nuulli_atuutilik = (자리 & 3) * 8;
        Ilulingit_atuutilik[칸] = (Ilulingit_atuutilik[칸] & ~(255 << nuulli_atuutilik)) | ((atuutilik & 255) << nuulli_atuutilik);
    }

    public static int aqqut_pigiarli(int anininga) {
        aqqut_takininga = 0;
        if (anininga < 1 || anininga > 63) return -36;
        aqqut_takininga = anininga;
        for (int piliqqittaajuq_nalunaiqsimavik = 0; piliqqittaajuq_nalunaiqsimavik < anininga; piliqqittaajuq_nalunaiqsimavik++) aqqut[piliqqittaajuq_nalunaiqsimavik] = 0;
        return 0;
    }
    public static int aqqut_byte(int nalunaiqsimavik, int atuutilik) {
        if (nalunaiqsimavik < 0 || nalunaiqsimavik >= aqqut_takininga || atuutilik < 1 || atuutilik > 255) return -22;
        aqqut[nalunaiqsimavik] = atuutilik; return 0;
    }
    static int nanili_Iliniku() {
        for (int ini_nalunaiqsimavik = 0; ini_nalunaiqsimavik < 파일수; ini_nalunaiqsimavik++) if (이름길이[ini_nalunaiqsimavik] > 0 && 이름길이[ini_nalunaiqsimavik] == 정규길이 && 접두(atiq, ini_nalunaiqsimavik * 64, 이름길이[ini_nalunaiqsimavik], 정규, 정규길이)) return ini_nalunaiqsimavik;
        return -1;
    }
    public static int matuirli(int 플래그) {
        if (aqqut_takininga == 0 || (플래그 & ~0x6c3) != 0 || (플래그 & 3) == 3) return -22;
        for (int piliqqittaajuq_nalunaiqsimavik = 0; piliqqittaajuq_nalunaiqsimavik < aqqut_takininga; piliqqittaajuq_nalunaiqsimavik++) if (aqqut[piliqqittaajuq_nalunaiqsimavik] == 0) return -22;
        if ((플래그 & 0x200) != 0 && (플래그 & 3) == 0) return -22;
        int 결과 = naammasitilli_atuutilik(); if (결과 < 0) return 결과;
        if (nanili_tukimuagutiit(정규길이) >= 0) return -21;
        결과 = 부모확인(); if (결과 < 0) return 결과;
        int ini = nanili_Iliniku();
        if (ini >= 0 && (플래그 & 0xc0) == 0xc0) return -17;
        if (ini < 0 && (플래그 & 0x40) == 0) return -2;
        int 서술자 = -1;
        for (int piliqqittaajuq_nalunaiqsimavik = 0; piliqqittaajuq_nalunaiqsimavik < 16; piliqqittaajuq_nalunaiqsimavik++) if (사용[piliqqittaajuq_nalunaiqsimavik] == 0) { 서술자 = piliqqittaajuq_nalunaiqsimavik; break; }
        if (서술자 < 0) return -24;
        if (ini < 0) {
            for (int piliqqittaajuq_nalunaiqsimavik = 0; piliqqittaajuq_nalunaiqsimavik < 파일수; piliqqittaajuq_nalunaiqsimavik++) if (이름길이[piliqqittaajuq_nalunaiqsimavik] == 0 && 참조수[piliqqittaajuq_nalunaiqsimavik] == 0) { ini = piliqqittaajuq_nalunaiqsimavik; break; }
            if (ini < 0) return -28;
            이름길이[ini] = 정규길이;
            for (int piliqqittaajuq_nalunaiqsimavik = 0; piliqqittaajuq_nalunaiqsimavik < 정규길이; piliqqittaajuq_nalunaiqsimavik++) atiq[ini * 64 + piliqqittaajuq_nalunaiqsimavik] = 정규[piliqqittaajuq_nalunaiqsimavik];
            takininga_atuutilik[ini] = 0;
        }
        if ((플래그 & 0x200) != 0) takininga_atuutilik[ini] = 0;
        사용[서술자] = 1; turaagaq[서술자] = ini; 위치[서술자] = 0; 방식[서술자] = 플래그;
        참조수[ini]++;
        return 서술자 + 3;
    }
    static int nalunairli_1aacb54c(int 서술자) {
        return 서술자 >= 3 && 서술자 < 19 && 사용[서술자 - 3] != 0 ? 서술자 - 3 : -1;
    }
    public static int 읽기(int 서술자) {
        int 칸 = nalunairli_1aacb54c(서술자);
        if (칸 < 0 || (방식[칸] & 3) == 1) return -9;
        int ini = turaagaq[칸];
        if (위치[칸] >= takininga_atuutilik[ini]) return 256; // EOF와 taannallarik_titiqqat 0x00..0xff 구별
        return 자료읽기(ini, 위치[칸]++);
    }
    public static int titiraq(int 서술자, int atuutilik) {
        int 칸 = nalunairli_1aacb54c(서술자);
        if (칸 < 0 || (방식[칸] & 3) == 0) return -9;
        int ini = turaagaq[칸];
        if ((방식[칸] & 0x400) != 0) 위치[칸] = takininga_atuutilik[ini];
        if (위치[칸] >= 16384) return -28;
        while (takininga_atuutilik[ini] < 위치[칸]) titiraq_titiqqat(ini, takininga_atuutilik[ini]++, 0);
        titiraq_titiqqat(ini, 위치[칸]++, atuutilik);
        if (takininga_atuutilik[ini] < 위치[칸]) takininga_atuutilik[ini] = 위치[칸];
        return 1;
    }
    public static int 옮기기(int 서술자, int 거리, int 기준) {
        int 칸 = nalunairli_1aacb54c(서술자);
        if (칸 < 0) return -9;
        if (기준 < 0 || 기준 > 2 || 거리 < -16384 || 거리 > 16384) return -22;
        int 새위치 = 거리 + (기준 == 0 ? 0 : 기준 == 1 ? 위치[칸] : takininga_atuutilik[turaagaq[칸]]);
        if (새위치 < 0 || 새위치 > 16384) return -22;
        위치[칸] = 새위치; return 새위치;
    }
    public static int matuli(int 서술자) {
        int 칸 = nalunairli_1aacb54c(서술자);
        if (칸 < 0) return -9;
        참조수[turaagaq[칸]]--; 사용[칸] = 0; return 0;
    }
    public static int anininga(int 서술자) {
        int 칸 = nalunairli_1aacb54c(서술자); return 칸 < 0 ? -9 : takininga_atuutilik[turaagaq[칸]];
    }
    public static int attiqsimaniit_takininga(int 서술자, int anininga) {
        int 칸 = nalunairli_1aacb54c(서술자);
        if (칸 < 0 || (방식[칸] & 3) == 0) return -9;
        if (anininga < 0 || anininga > 16384) return -22;
        int ini = turaagaq[칸];
        while (takininga_atuutilik[ini] < anininga) titiraq_titiqqat(ini, takininga_atuutilik[ini]++, 0);
        takininga_atuutilik[ini] = anininga; return 0;
    }
    public static int 지우기() {
        if (aqqut_takininga == 0) return -22;
        int 결과 = naammasitilli_atuutilik(); if (결과 < 0) return 결과;
        if (nanili_tukimuagutiit(정규길이) >= 0) return -21;
        결과 = 부모확인(); if (결과 < 0) return 결과;
        int ini = nanili_Iliniku();
        if (ini < 0) return -2;
        이름길이[ini] = 0; return 0; // 열려 있는 파일은 마지막 close까지 유지
    }
    static void Iliniku_Titiqpalliagaq() {
        aqqut_pigiarli(1); aqqut_byte(0, '.'); 경로목록();
    }
    public static int 공개이름길이(int nalunaiqsimavik) {
        if (nalunaiqsimavik < 0 || nalunaiqsimavik >= 파일수 || 이름길이[nalunaiqsimavik] == 0) return 0;
        for (int piliqqittaajuq_nalunaiqsimavik = 0; piliqqittaajuq_nalunaiqsimavik < 이름길이[nalunaiqsimavik]; piliqqittaajuq_nalunaiqsimavik++) if (atiq[nalunaiqsimavik * 64 + piliqqittaajuq_nalunaiqsimavik] == '/') return 0;
        return 이름길이[nalunaiqsimavik];
    }
    public static int 공개이름바이트(int nalunaiqsimavik, int 자리) {
        return nalunaiqsimavik >= 0 && nalunaiqsimavik < 파일수 && 자리 >= 0 && 자리 < 이름길이[nalunaiqsimavik] ? atiq[nalunaiqsimavik * 64 + 자리] : -22;
    }
    public static int 공개파일크기(int nalunaiqsimavik) { return nalunaiqsimavik >= 0 && nalunaiqsimavik < 파일수 ? takininga_atuutilik[nalunaiqsimavik] : -22; }
    static int[] 정규 = new int[64], 현재 = new int[64], tukimuagutiit_atiq = new int[16 * 64], tukimuagutiit_takininga = new int[16];
    static int 정규길이, 현재길이;
    static boolean 접두(int[] 이름들, int 시작, int aqqut_atuutilik, int[] 앞, int titikutaat_akunningit_aqqut) {
        if (aqqut_atuutilik < titikutaat_akunningit_aqqut) return false;
        for (int piliqqittaajuq_nalunaiqsimavik = 0; piliqqittaajuq_nalunaiqsimavik < titikutaat_akunningit_aqqut; piliqqittaajuq_nalunaiqsimavik++) if (이름들[시작 + piliqqittaajuq_nalunaiqsimavik] != 앞[piliqqittaajuq_nalunaiqsimavik]) return false;
        return true;
    }
    static int naammasitilli_atuutilik() {
        if (aqqut_takininga == 0) return -22;
        정규길이 = aqqut[0] == '/' ? 0 : 현재길이;
        for (int piliqqittaajuq_nalunaiqsimavik = 0; piliqqittaajuq_nalunaiqsimavik < 정규길이; piliqqittaajuq_nalunaiqsimavik++) 정규[piliqqittaajuq_nalunaiqsimavik] = 현재[piliqqittaajuq_nalunaiqsimavik];
        int 읽는자리 = 0;
        while (읽는자리 < aqqut_takininga) {
            while (읽는자리 < aqqut_takininga && aqqut[읽는자리] == '/') 읽는자리++;
            int 시작자리 = 읽는자리; while (읽는자리 < aqqut_takininga && aqqut[읽는자리] != '/') { if (aqqut[읽는자리] == 0) return -22; 읽는자리++; }
            int 항목수 = 읽는자리 - 시작자리; if (항목수 == 0 || 항목수 == 1 && aqqut[시작자리] == '.') continue;
            if (항목수 == 2 && aqqut[시작자리] == '.' && aqqut[시작자리 + 1] == '.') {
                while (정규길이 > 0 && 정규[정규길이 - 1] != '/') 정규길이--;
                if (정규길이 > 0) 정규길이--;
                continue;
            }
            if (정규길이 + 항목수 + (정규길이 == 0 ? 0 : 1) > 63) return -36;
            if (정규길이 > 0) 정규[정규길이++] = '/';
            for (int piliqqittaajuq_nalunaiqsimavik = 시작자리; piliqqittaajuq_nalunaiqsimavik < 읽는자리; piliqqittaajuq_nalunaiqsimavik++) 정규[정규길이++] = aqqut[piliqqittaajuq_nalunaiqsimavik];
        }
        return 0;
    }
    static int nanili_tukimuagutiit(int 항목수) {
        if (항목수 == 0) return 0;
        for (int piliqqittaajuq_nalunaiqsimavik = 1; piliqqittaajuq_nalunaiqsimavik < 16; piliqqittaajuq_nalunaiqsimavik++) if (tukimuagutiit_takininga[piliqqittaajuq_nalunaiqsimavik] == 항목수 && 접두(tukimuagutiit_atiq, piliqqittaajuq_nalunaiqsimavik * 64, 항목수, 정규, 항목수)) return piliqqittaajuq_nalunaiqsimavik;
        return -1;
    }
    static int 부모확인() {
        int 항목수 = 정규길이; while (항목수 > 0 && 정규[항목수 - 1] != '/') 항목수--;
        return nanili_tukimuagutiit(항목수 == 0 ? 0 : 항목수 - 1) < 0 ? -2 : 0;
    }
    public static int 폴더만들기() {
        int 처리값 = naammasitilli_atuutilik(); if (처리값 < 0) return 처리값;
        if (nanili_tukimuagutiit(정규길이) >= 0 || nanili_Iliniku() >= 0) return -17;
        처리값 = 부모확인(); if (처리값 < 0) return 처리값;
        for (int piliqqittaajuq_nalunaiqsimavik = 1; piliqqittaajuq_nalunaiqsimavik < 16; piliqqittaajuq_nalunaiqsimavik++) if (tukimuagutiit_takininga[piliqqittaajuq_nalunaiqsimavik] == 0) {
            tukimuagutiit_takininga[piliqqittaajuq_nalunaiqsimavik] = 정규길이; for (int 안쪽자리 = 0; 안쪽자리 < 정규길이; 안쪽자리++) tukimuagutiit_atiq[piliqqittaajuq_nalunaiqsimavik * 64 + 안쪽자리] = 정규[안쪽자리]; return 0;
        }
        return -28;
    }
    public static int 항목종류() {
        int 처리값 = naammasitilli_atuutilik(); if (처리값 < 0) return 처리값;
        if (nanili_tukimuagutiit(정규길이) >= 0) return 2;
        return nanili_Iliniku() >= 0 ? 1 : 0;
    }
    public static int asijjirli_tukimuagutiit() {
        int 처리값 = naammasitilli_atuutilik(); if (처리값 < 0) return 처리값;
        if (nanili_tukimuagutiit(정규길이) < 0) return -2;
        현재길이 = 정규길이; for (int piliqqittaajuq_nalunaiqsimavik = 0; piliqqittaajuq_nalunaiqsimavik < 현재길이; piliqqittaajuq_nalunaiqsimavik++) 현재[piliqqittaajuq_nalunaiqsimavik] = 정규[piliqqittaajuq_nalunaiqsimavik]; return 0;
    }
    public static int sanirvalli_tukimuagutiit() {
        int 처리값 = naammasitilli_atuutilik(); if (처리값 < 0) return 처리값;
        int 폴더번호 = nanili_tukimuagutiit(정규길이); if (폴더번호 < 0) return -2; if (폴더번호 == 0) return -16;
        if (현재길이 == 정규길이 && 접두(현재, 0, 현재길이, 정규, 정규길이)) return -16;
        for (int piliqqittaajuq_nalunaiqsimavik = 0; piliqqittaajuq_nalunaiqsimavik < 파일수; piliqqittaajuq_nalunaiqsimavik++) {
            if (이름길이[piliqqittaajuq_nalunaiqsimavik] > 정규길이 && 접두(atiq, piliqqittaajuq_nalunaiqsimavik * 64, 이름길이[piliqqittaajuq_nalunaiqsimavik], 정규, 정규길이) && atiq[piliqqittaajuq_nalunaiqsimavik * 64 + 정규길이] == '/') return -39;
        }
        for (int piliqqittaajuq_nalunaiqsimavik = 0; piliqqittaajuq_nalunaiqsimavik < 16; piliqqittaajuq_nalunaiqsimavik++) {
            if (tukimuagutiit_takininga[piliqqittaajuq_nalunaiqsimavik] > 정규길이 && 접두(tukimuagutiit_atiq, piliqqittaajuq_nalunaiqsimavik * 64, tukimuagutiit_takininga[piliqqittaajuq_nalunaiqsimavik], 정규, 정규길이) && tukimuagutiit_atiq[piliqqittaajuq_nalunaiqsimavik * 64 + 정규길이] == '/') return -39;
        }
        tukimuagutiit_takininga[폴더번호] = 0; return 0;
    }
    public static int 이름바꾸기(int 원본번호) {
        if (원본번호 < 0 || 원본번호 >= 파일수 || 이름길이[원본번호] == 0) return -2;
        int 처리값 = naammasitilli_atuutilik(); if (처리값 < 0) return 처리값;
        if (nanili_tukimuagutiit(정규길이) >= 0) return -21;
        처리값 = 부모확인(); if (처리값 < 0) return 처리값;
        int 이전값 = nanili_Iliniku(); if (이전값 == 원본번호) return 0;
        if (이전값 >= 0) 이름길이[이전값] = 0;
        이름길이[원본번호] = 정규길이; for (int piliqqittaajuq_nalunaiqsimavik = 0; piliqqittaajuq_nalunaiqsimavik < 정규길이; piliqqittaajuq_nalunaiqsimavik++) atiq[원본번호 * 64 + piliqqittaajuq_nalunaiqsimavik] = 정규[piliqqittaajuq_nalunaiqsimavik]; return 0;
    }
    static int Iliniku_pigiarli(int[] titiqqat_array, int 시작점, int 항목수) {
        if (!접두(titiqqat_array, 시작점, 항목수, 정규, 정규길이)) return -1;
        int 시작자리 = 정규길이;
        if (시작자리 > 0) { if (항목수 <= 시작자리 || titiqqat_array[시작점 + 시작자리] != '/') return -1; 시작자리++; }
        if (항목수 <= 시작자리) return -1;
        for (int piliqqittaajuq_nalunaiqsimavik = 시작자리; piliqqittaajuq_nalunaiqsimavik < 항목수; piliqqittaajuq_nalunaiqsimavik++) if (titiqqat_array[시작점 + piliqqittaajuq_nalunaiqsimavik] == '/') return -1;
        return 시작자리;
    }
    static void 현재쓰기() { 단말.문자('/'); for (int piliqqittaajuq_nalunaiqsimavik = 0; piliqqittaajuq_nalunaiqsimavik < 현재길이; piliqqittaajuq_nalunaiqsimavik++) 보드.직렬쓰기(현재[piliqqittaajuq_nalunaiqsimavik]); }
    static int 경로목록() {
        int 처리값 = naammasitilli_atuutilik(); if (처리값 < 0) return 처리값;
        int ini_turaagaq = nanili_Iliniku();
        if (ini_turaagaq >= 0) { for (int piliqqittaajuq_nalunaiqsimavik = 0; piliqqittaajuq_nalunaiqsimavik < 정규길이; piliqqittaajuq_nalunaiqsimavik++) 보드.직렬쓰기(정규[piliqqittaajuq_nalunaiqsimavik]); 단말.titiraq("  "); 단말.수(takininga_atuutilik[ini_turaagaq]); 단말.titiraq("byte_atuutilik(주기억 ini)\n"); return 0; }
        if (nanili_tukimuagutiit(정규길이) < 0) return -2;
        for (int 뒷값 = 1; 뒷값 < 16; 뒷값++) if (tukimuagutiit_takininga[뒷값] > 0) {
            int 시작자리 = Iliniku_pigiarli(tukimuagutiit_atiq, 뒷값 * 64, tukimuagutiit_takininga[뒷값]); if (시작자리 < 0) continue;
            for (int piliqqittaajuq_nalunaiqsimavik = 시작자리; piliqqittaajuq_nalunaiqsimavik < tukimuagutiit_takininga[뒷값]; piliqqittaajuq_nalunaiqsimavik++) 보드.직렬쓰기(tukimuagutiit_atiq[뒷값 * 64 + piliqqittaajuq_nalunaiqsimavik]); 단말.titiraq("/\n");
        }
        for (int ini_nalunaiqsimavik = 0; ini_nalunaiqsimavik < 파일수; ini_nalunaiqsimavik++) if (이름길이[ini_nalunaiqsimavik] > 0) {
            int 시작자리 = Iliniku_pigiarli(atiq, ini_nalunaiqsimavik * 64, 이름길이[ini_nalunaiqsimavik]); if (시작자리 < 0) continue;
            for (int piliqqittaajuq_nalunaiqsimavik = 시작자리; piliqqittaajuq_nalunaiqsimavik < 이름길이[ini_nalunaiqsimavik]; piliqqittaajuq_nalunaiqsimavik++) 보드.직렬쓰기(atiq[ini_nalunaiqsimavik * 64 + piliqqittaajuq_nalunaiqsimavik]);
            단말.titiraq("  "); 단말.수(takininga_atuutilik[ini_nalunaiqsimavik]); 단말.titiraq("byte_atuutilik(주기억 ini)\n");
        }
        return 0;
    }
}
