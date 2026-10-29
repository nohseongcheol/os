// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** RAM faili 64개, 파일당 16384바이트, 서술자 16개. 모든 data/정책은 Java에 있다.
 * 호출 도중 양보하지 않으므로 현재의 단일 코어 협력식 작업 사이에서 원자적이다.
 * 디스크 저장이나 POSIX 전체 구현을 뜻하지 않는다. 음수 반환은 kosa 번호다.
 */
public final class kumbukumbu_Faili {
    static final int 파일수 = 64;
    static int[] Jina = new int[파일수 * 64];
    static int[] 이름길이 = new int[파일수];
    // Pack four bytes in each Java int, preserving the old content heap budget.
    static int[] maudhui_thamani = new int[파일수 * 4096];
    static int[] urefu_thamani = new int[파일수];
    static int[] 참조수 = new int[파일수];
    static int[] 사용 = new int[16];
    static int[] lengo = new int[16];
    static int[] 위치 = new int[16];
    static int[] mbinu_hali_tumizi = new int[16];
    static int[] njia = new int[64];
    static int njia_urefu;

    public static int 파일한도() { return 파일수; }
    static int 자료읽기(int faili, int 자리) { return (maudhui_thamani[faili * 4096 + 자리 / 4] >>> ((자리 & 3) * 8)) & 255; }
    static void andika_data(int faili, int 자리, int thamani) {
        int Sloti_ingizo = faili * 4096 + 자리 / 4, hamisha_thamani = (자리 & 3) * 8;
        maudhui_thamani[Sloti_ingizo] = (maudhui_thamani[Sloti_ingizo] & ~(255 << hamisha_thamani)) | ((thamani & 255) << hamisha_thamani);
    }

    public static int njia_Anza(int panga_ukubwa) {
        njia_urefu = 0;
        if (panga_ukubwa < 1 || panga_ukubwa > 63) return -36;
        njia_urefu = panga_ukubwa;
        for (int kitanzi_kielezo = 0; kitanzi_kielezo < panga_ukubwa; kitanzi_kielezo++) njia[kitanzi_kielezo] = 0;
        return 0;
    }
    public static int njia_baiti(int kielezo, int thamani) {
        if (kielezo < 0 || kielezo >= njia_urefu || thamani < 1 || thamani > 255) return -22;
        njia[kielezo] = thamani; return 0;
    }
    static int gundua_ingizo() {
        for (int faili_kielezo = 0; faili_kielezo < 파일수; faili_kielezo++) if (이름길이[faili_kielezo] > 0 && 이름길이[faili_kielezo] == 정규길이 && 접두(Jina, faili_kielezo * 64, 이름길이[faili_kielezo], 정규, 정규길이)) return faili_kielezo;
        return -1;
    }
    public static int unda(int 플래그) {
        if (njia_urefu == 0 || (플래그 & ~0x6c3) != 0 || (플래그 & 3) == 3) return -22;
        for (int kitanzi_kielezo = 0; kitanzi_kielezo < njia_urefu; kitanzi_kielezo++) if (njia[kitanzi_kielezo] == 0) return -22;
        if ((플래그 & 0x200) != 0 && (플래그 & 3) == 0) return -22;
        int 결과 = kawaidisha_thamani(); if (결과 < 0) return 결과;
        if (gundua_Saraka(정규길이) >= 0) return -21;
        결과 = 부모확인(); if (결과 < 0) return 결과;
        int faili = gundua_ingizo();
        if (faili >= 0 && (플래그 & 0xc0) == 0xc0) return -17;
        if (faili < 0 && (플래그 & 0x40) == 0) return -2;
        int 서술자 = -1;
        for (int kitanzi_kielezo = 0; kitanzi_kielezo < 16; kitanzi_kielezo++) if (사용[kitanzi_kielezo] == 0) { 서술자 = kitanzi_kielezo; break; }
        if (서술자 < 0) return -24;
        if (faili < 0) {
            for (int kitanzi_kielezo = 0; kitanzi_kielezo < 파일수; kitanzi_kielezo++) if (이름길이[kitanzi_kielezo] == 0 && 참조수[kitanzi_kielezo] == 0) { faili = kitanzi_kielezo; break; }
            if (faili < 0) return -28;
            이름길이[faili] = 정규길이;
            for (int kitanzi_kielezo = 0; kitanzi_kielezo < 정규길이; kitanzi_kielezo++) Jina[faili * 64 + kitanzi_kielezo] = 정규[kitanzi_kielezo];
            urefu_thamani[faili] = 0;
        }
        if ((플래그 & 0x200) != 0) urefu_thamani[faili] = 0;
        사용[서술자] = 1; lengo[서술자] = faili; 위치[서술자] = 0; mbinu_hali_tumizi[서술자] = 플래그;
        참조수[faili]++;
        return 서술자 + 3;
    }
    static int thibitisha(int 서술자) {
        return 서술자 >= 3 && 서술자 < 19 && 사용[서술자 - 3] != 0 ? 서술자 - 3 : -1;
    }
    public static int 읽기(int 서술자) {
        int Sloti_ingizo = thibitisha(서술자);
        if (Sloti_ingizo < 0 || (mbinu_hali_tumizi[Sloti_ingizo] & 3) == 1) return -9;
        int faili = lengo[Sloti_ingizo];
        if (위치[Sloti_ingizo] >= urefu_thamani[faili]) return 256; // EOF와 halisi_data 0x00..0xff 구별
        return 자료읽기(faili, 위치[Sloti_ingizo]++);
    }
    public static int andika(int 서술자, int thamani) {
        int Sloti_ingizo = thibitisha(서술자);
        if (Sloti_ingizo < 0 || (mbinu_hali_tumizi[Sloti_ingizo] & 3) == 0) return -9;
        int faili = lengo[Sloti_ingizo];
        if ((mbinu_hali_tumizi[Sloti_ingizo] & 0x400) != 0) 위치[Sloti_ingizo] = urefu_thamani[faili];
        if (위치[Sloti_ingizo] >= 16384) return -28;
        while (urefu_thamani[faili] < 위치[Sloti_ingizo]) andika_data(faili, urefu_thamani[faili]++, 0);
        andika_data(faili, 위치[Sloti_ingizo]++, thamani);
        if (urefu_thamani[faili] < 위치[Sloti_ingizo]) urefu_thamani[faili] = 위치[Sloti_ingizo];
        return 1;
    }
    public static int 옮기기(int 서술자, int 거리, int 기준) {
        int Sloti_ingizo = thibitisha(서술자);
        if (Sloti_ingizo < 0) return -9;
        if (기준 < 0 || 기준 > 2 || 거리 < -16384 || 거리 > 16384) return -22;
        int 새위치 = 거리 + (기준 == 0 ? 0 : 기준 == 1 ? 위치[Sloti_ingizo] : urefu_thamani[lengo[Sloti_ingizo]]);
        if (새위치 < 0 || 새위치 > 16384) return -22;
        위치[Sloti_ingizo] = 새위치; return 새위치;
    }
    public static int funga(int 서술자) {
        int Sloti_ingizo = thibitisha(서술자);
        if (Sloti_ingizo < 0) return -9;
        참조수[lengo[Sloti_ingizo]]--; 사용[Sloti_ingizo] = 0; return 0;
    }
    public static int panga_ukubwa(int 서술자) {
        int Sloti_ingizo = thibitisha(서술자); return Sloti_ingizo < 0 ? -9 : urefu_thamani[lengo[Sloti_ingizo]];
    }
    public static int seti_urefu(int 서술자, int panga_ukubwa) {
        int Sloti_ingizo = thibitisha(서술자);
        if (Sloti_ingizo < 0 || (mbinu_hali_tumizi[Sloti_ingizo] & 3) == 0) return -9;
        if (panga_ukubwa < 0 || panga_ukubwa > 16384) return -22;
        int faili = lengo[Sloti_ingizo];
        while (urefu_thamani[faili] < panga_ukubwa) andika_data(faili, urefu_thamani[faili]++, 0);
        urefu_thamani[faili] = panga_ukubwa; return 0;
    }
    public static int futa_ingizo() {
        if (njia_urefu == 0) return -22;
        int 결과 = kawaidisha_thamani(); if (결과 < 0) return 결과;
        if (gundua_Saraka(정규길이) >= 0) return -21;
        결과 = 부모확인(); if (결과 < 0) return 결과;
        int faili = gundua_ingizo();
        if (faili < 0) return -2;
        이름길이[faili] = 0; return 0; // 열려 있는 파일은 마지막 close까지 유지
    }
    static void ingizo_Orodha() {
        njia_Anza(1); njia_baiti(0, '.'); 경로목록();
    }
    public static int 공개이름길이(int kielezo) {
        if (kielezo < 0 || kielezo >= 파일수 || 이름길이[kielezo] == 0) return 0;
        for (int kitanzi_kielezo = 0; kitanzi_kielezo < 이름길이[kielezo]; kitanzi_kielezo++) if (Jina[kielezo * 64 + kitanzi_kielezo] == '/') return 0;
        return 이름길이[kielezo];
    }
    public static int 공개이름바이트(int kielezo, int 자리) {
        return kielezo >= 0 && kielezo < 파일수 && 자리 >= 0 && 자리 < 이름길이[kielezo] ? Jina[kielezo * 64 + 자리] : -22;
    }
    public static int 공개파일크기(int kielezo) { return kielezo >= 0 && kielezo < 파일수 ? urefu_thamani[kielezo] : -22; }
    static int[] 정규 = new int[64], 현재 = new int[64], Saraka_jina = new int[16 * 64], Saraka_urefu = new int[16];
    static int 정규길이, 현재길이;
    static boolean 접두(int[] 이름들, int endesha, int njia_thamani, int[] mbele_thamani, int inayoongoza_njia) {
        if (njia_thamani < inayoongoza_njia) return false;
        for (int kitanzi_kielezo = 0; kitanzi_kielezo < inayoongoza_njia; kitanzi_kielezo++) if (이름들[endesha + kitanzi_kielezo] != mbele_thamani[kitanzi_kielezo]) return false;
        return true;
    }
    static int kawaidisha_thamani() {
        if (njia_urefu == 0) return -22;
        정규길이 = njia[0] == '/' ? 0 : 현재길이;
        for (int kitanzi_kielezo = 0; kitanzi_kielezo < 정규길이; kitanzi_kielezo++) 정규[kitanzi_kielezo] = 현재[kitanzi_kielezo];
        int 읽는자리 = 0;
        while (읽는자리 < njia_urefu) {
            while (읽는자리 < njia_urefu && njia[읽는자리] == '/') 읽는자리++;
            int 시작자리 = 읽는자리; while (읽는자리 < njia_urefu && njia[읽는자리] != '/') { if (njia[읽는자리] == 0) return -22; 읽는자리++; }
            int 항목수 = 읽는자리 - 시작자리; if (항목수 == 0 || 항목수 == 1 && njia[시작자리] == '.') continue;
            if (항목수 == 2 && njia[시작자리] == '.' && njia[시작자리 + 1] == '.') {
                while (정규길이 > 0 && 정규[정규길이 - 1] != '/') 정규길이--;
                if (정규길이 > 0) 정규길이--;
                continue;
            }
            if (정규길이 + 항목수 + (정규길이 == 0 ? 0 : 1) > 63) return -36;
            if (정규길이 > 0) 정규[정규길이++] = '/';
            for (int kitanzi_kielezo = 시작자리; kitanzi_kielezo < 읽는자리; kitanzi_kielezo++) 정규[정규길이++] = njia[kitanzi_kielezo];
        }
        return 0;
    }
    static int gundua_Saraka(int 항목수) {
        if (항목수 == 0) return 0;
        for (int kitanzi_kielezo = 1; kitanzi_kielezo < 16; kitanzi_kielezo++) if (Saraka_urefu[kitanzi_kielezo] == 항목수 && 접두(Saraka_jina, kitanzi_kielezo * 64, 항목수, 정규, 항목수)) return kitanzi_kielezo;
        return -1;
    }
    static int 부모확인() {
        int 항목수 = 정규길이; while (항목수 > 0 && 정규[항목수 - 1] != '/') 항목수--;
        return gundua_Saraka(항목수 == 0 ? 0 : 항목수 - 1) < 0 ? -2 : 0;
    }
    public static int unda_Saraka() {
        int 처리값 = kawaidisha_thamani(); if (처리값 < 0) return 처리값;
        if (gundua_Saraka(정규길이) >= 0 || gundua_ingizo() >= 0) return -17;
        처리값 = 부모확인(); if (처리값 < 0) return 처리값;
        for (int kitanzi_kielezo = 1; kitanzi_kielezo < 16; kitanzi_kielezo++) if (Saraka_urefu[kitanzi_kielezo] == 0) {
            Saraka_urefu[kitanzi_kielezo] = 정규길이; for (int 안쪽자리 = 0; 안쪽자리 < 정규길이; 안쪽자리++) Saraka_jina[kitanzi_kielezo * 64 + 안쪽자리] = 정규[안쪽자리]; return 0;
        }
        return -28;
    }
    public static int 항목종류() {
        int 처리값 = kawaidisha_thamani(); if (처리값 < 0) return 처리값;
        if (gundua_Saraka(정규길이) >= 0) return 2;
        return gundua_ingizo() >= 0 ? 1 : 0;
    }
    public static int badilisha_Saraka() {
        int 처리값 = kawaidisha_thamani(); if (처리값 < 0) return 처리값;
        if (gundua_Saraka(정규길이) < 0) return -2;
        현재길이 = 정규길이; for (int kitanzi_kielezo = 0; kitanzi_kielezo < 현재길이; kitanzi_kielezo++) 현재[kitanzi_kielezo] = 정규[kitanzi_kielezo]; return 0;
    }
    public static int ondoa_Saraka() {
        int 처리값 = kawaidisha_thamani(); if (처리값 < 0) return 처리값;
        int 폴더번호 = gundua_Saraka(정규길이); if (폴더번호 < 0) return -2; if (폴더번호 == 0) return -16;
        if (현재길이 == 정규길이 && 접두(현재, 0, 현재길이, 정규, 정규길이)) return -16;
        for (int kitanzi_kielezo = 0; kitanzi_kielezo < 파일수; kitanzi_kielezo++) {
            if (이름길이[kitanzi_kielezo] > 정규길이 && 접두(Jina, kitanzi_kielezo * 64, 이름길이[kitanzi_kielezo], 정규, 정규길이) && Jina[kitanzi_kielezo * 64 + 정규길이] == '/') return -39;
        }
        for (int kitanzi_kielezo = 0; kitanzi_kielezo < 16; kitanzi_kielezo++) {
            if (Saraka_urefu[kitanzi_kielezo] > 정규길이 && 접두(Saraka_jina, kitanzi_kielezo * 64, Saraka_urefu[kitanzi_kielezo], 정규, 정규길이) && Saraka_jina[kitanzi_kielezo * 64 + 정규길이] == '/') return -39;
        }
        Saraka_urefu[폴더번호] = 0; return 0;
    }
    public static int 이름바꾸기(int 원본번호) {
        if (원본번호 < 0 || 원본번호 >= 파일수 || 이름길이[원본번호] == 0) return -2;
        int 처리값 = kawaidisha_thamani(); if (처리값 < 0) return 처리값;
        if (gundua_Saraka(정규길이) >= 0) return -21;
        처리값 = 부모확인(); if (처리값 < 0) return 처리값;
        int 이전값 = gundua_ingizo(); if (이전값 == 원본번호) return 0;
        if (이전값 >= 0) 이름길이[이전값] = 0;
        이름길이[원본번호] = 정규길이; for (int kitanzi_kielezo = 0; kitanzi_kielezo < 정규길이; kitanzi_kielezo++) Jina[원본번호 * 64 + kitanzi_kielezo] = 정규[kitanzi_kielezo]; return 0;
    }
    static int ingizo_Anza(int[] data_ARRAY, int 시작점, int 항목수) {
        if (!접두(data_ARRAY, 시작점, 항목수, 정규, 정규길이)) return -1;
        int 시작자리 = 정규길이;
        if (시작자리 > 0) { if (항목수 <= 시작자리 || data_ARRAY[시작점 + 시작자리] != '/') return -1; 시작자리++; }
        if (항목수 <= 시작자리) return -1;
        for (int kitanzi_kielezo = 시작자리; kitanzi_kielezo < 항목수; kitanzi_kielezo++) if (data_ARRAY[시작점 + kitanzi_kielezo] == '/') return -1;
        return 시작자리;
    }
    static void 현재쓰기() { 단말.문자('/'); for (int kitanzi_kielezo = 0; kitanzi_kielezo < 현재길이; kitanzi_kielezo++) 보드.직렬쓰기(현재[kitanzi_kielezo]); }
    static int 경로목록() {
        int 처리값 = kawaidisha_thamani(); if (처리값 < 0) return 처리값;
        int faili_lengo = gundua_ingizo();
        if (faili_lengo >= 0) { for (int kitanzi_kielezo = 0; kitanzi_kielezo < 정규길이; kitanzi_kielezo++) 보드.직렬쓰기(정규[kitanzi_kielezo]); 단말.andika("  "); 단말.수(urefu_thamani[faili_lengo]); 단말.andika("baiti_thamani(주기억 faili)\n"); return 0; }
        if (gundua_Saraka(정규길이) < 0) return -2;
        for (int 뒷값 = 1; 뒷값 < 16; 뒷값++) if (Saraka_urefu[뒷값] > 0) {
            int 시작자리 = ingizo_Anza(Saraka_jina, 뒷값 * 64, Saraka_urefu[뒷값]); if (시작자리 < 0) continue;
            for (int kitanzi_kielezo = 시작자리; kitanzi_kielezo < Saraka_urefu[뒷값]; kitanzi_kielezo++) 보드.직렬쓰기(Saraka_jina[뒷값 * 64 + kitanzi_kielezo]); 단말.andika("/\n");
        }
        for (int faili_kielezo = 0; faili_kielezo < 파일수; faili_kielezo++) if (이름길이[faili_kielezo] > 0) {
            int 시작자리 = ingizo_Anza(Jina, faili_kielezo * 64, 이름길이[faili_kielezo]); if (시작자리 < 0) continue;
            for (int kitanzi_kielezo = 시작자리; kitanzi_kielezo < 이름길이[faili_kielezo]; kitanzi_kielezo++) 보드.직렬쓰기(Jina[faili_kielezo * 64 + kitanzi_kielezo]);
            단말.andika("  "); 단말.수(urefu_thamani[faili_kielezo]); 단말.andika("baiti_thamani(주기억 faili)\n");
        }
        return 0;
    }
}
