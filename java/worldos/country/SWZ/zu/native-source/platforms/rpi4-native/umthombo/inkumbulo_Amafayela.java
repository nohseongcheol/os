// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** RAM Ihele 64개, 파일당 16384바이트, 서술자 16개. 모든 imininingwane/정책은 Java에 있다.
 * 호출 도중 양보하지 않으므로 현재의 단일 코어 협력식 작업 사이에서 원자적이다.
 * 디스크 저장이나 POSIX 전체 구현을 뜻하지 않는다. 음수 반환은 Iphutha 번호다.
 */
public final class inkumbulo_Amafayela {
    static final int 파일수 = 64;
    static int[] Igama = new int[파일수 * 64];
    static int[] 이름길이 = new int[파일수];
    // Pack four bytes in each Java int, preserving the old content heap budget.
    static int[] Okuqukethwe_inani = new int[파일수 * 4096];
    static int[] ubude_inani = new int[파일수];
    static int[] 참조수 = new int[파일수];
    static int[] 사용 = new int[16];
    static int[] impokophelo = new int[16];
    static int[] 위치 = new int[16];
    static int[] indlela_inqubo = new int[16];
    static int[] Indlela_2 = new int[64];
    static int umzila_ubude;

    public static int 파일한도() { return 파일수; }
    static int 자료읽기(int Ihele, int 자리) { return (Okuqukethwe_inani[Ihele * 4096 + 자리 / 4] >>> ((자리 & 3) * 8)) & 255; }
    static void bhala_imininingwane(int Ihele, int 자리, int inani) {
        int isikhala_okufakwayo = Ihele * 4096 + 자리 / 4, susa_inani = (자리 & 3) * 8;
        Okuqukethwe_inani[isikhala_okufakwayo] = (Okuqukethwe_inani[isikhala_okufakwayo] & ~(255 << susa_inani)) | ((inani & 255) << susa_inani);
    }

    public static int umzila_qala(int Ubungako) {
        umzila_ubude = 0;
        if (Ubungako < 1 || Ubungako > 63) return -36;
        umzila_ubude = Ubungako;
        for (int iluphu_thola_inkomba = 0; iluphu_thola_inkomba < Ubungako; iluphu_thola_inkomba++) Indlela_2[iluphu_thola_inkomba] = 0;
        return 0;
    }
    public static int umzila_ibhayithi(int thola_inkomba, int inani) {
        if (thola_inkomba < 0 || thola_inkomba >= umzila_ubude || inani < 1 || inani > 255) return -22;
        Indlela_2[thola_inkomba] = inani; return 0;
    }
    static int thola_okufakwayo() {
        for (int ifayela_thola_inkomba = 0; ifayela_thola_inkomba < 파일수; ifayela_thola_inkomba++) if (이름길이[ifayela_thola_inkomba] > 0 && 이름길이[ifayela_thola_inkomba] == 정규길이 && 접두(Igama, ifayela_thola_inkomba * 64, 이름길이[ifayela_thola_inkomba], 정규, 정규길이)) return ifayela_thola_inkomba;
        return -1;
    }
    public static int Vula(int 플래그) {
        if (umzila_ubude == 0 || (플래그 & ~0x6c3) != 0 || (플래그 & 3) == 3) return -22;
        for (int iluphu_thola_inkomba = 0; iluphu_thola_inkomba < umzila_ubude; iluphu_thola_inkomba++) if (Indlela_2[iluphu_thola_inkomba] == 0) return -22;
        if ((플래그 & 0x200) != 0 && (플래그 & 3) == 0) return -22;
        int 결과 = beka_kujwayeleke_inani(); if (결과 < 0) return 결과;
        if (thola_umkhombandlela(정규길이) >= 0) return -21;
        결과 = 부모확인(); if (결과 < 0) return 결과;
        int Ihele = thola_okufakwayo();
        if (Ihele >= 0 && (플래그 & 0xc0) == 0xc0) return -17;
        if (Ihele < 0 && (플래그 & 0x40) == 0) return -2;
        int 서술자 = -1;
        for (int iluphu_thola_inkomba = 0; iluphu_thola_inkomba < 16; iluphu_thola_inkomba++) if (사용[iluphu_thola_inkomba] == 0) { 서술자 = iluphu_thola_inkomba; break; }
        if (서술자 < 0) return -24;
        if (Ihele < 0) {
            for (int iluphu_thola_inkomba = 0; iluphu_thola_inkomba < 파일수; iluphu_thola_inkomba++) if (이름길이[iluphu_thola_inkomba] == 0 && 참조수[iluphu_thola_inkomba] == 0) { Ihele = iluphu_thola_inkomba; break; }
            if (Ihele < 0) return -28;
            이름길이[Ihele] = 정규길이;
            for (int iluphu_thola_inkomba = 0; iluphu_thola_inkomba < 정규길이; iluphu_thola_inkomba++) Igama[Ihele * 64 + iluphu_thola_inkomba] = 정규[iluphu_thola_inkomba];
            ubude_inani[Ihele] = 0;
        }
        if ((플래그 & 0x200) != 0) ubude_inani[Ihele] = 0;
        사용[서술자] = 1; impokophelo[서술자] = Ihele; 위치[서술자] = 0; indlela_inqubo[서술자] = 플래그;
        참조수[Ihele]++;
        return 서술자 + 3;
    }
    static int qiniseka(int 서술자) {
        return 서술자 >= 3 && 서술자 < 19 && 사용[서술자 - 3] != 0 ? 서술자 - 3 : -1;
    }
    public static int Funda(int 서술자) {
        int isikhala_okufakwayo = qiniseka(서술자);
        if (isikhala_okufakwayo < 0 || (indlela_inqubo[isikhala_okufakwayo] & 3) == 1) return -9;
        int Ihele = impokophelo[isikhala_okufakwayo];
        if (위치[isikhala_okufakwayo] >= ubude_inani[Ihele]) return 256; // EOF와 ulwazi_ngokwenzekile_imininingwane 0x00..0xff 구별
        return 자료읽기(Ihele, 위치[isikhala_okufakwayo]++);
    }
    public static int Bhala(int 서술자, int inani) {
        int isikhala_okufakwayo = qiniseka(서술자);
        if (isikhala_okufakwayo < 0 || (indlela_inqubo[isikhala_okufakwayo] & 3) == 0) return -9;
        int Ihele = impokophelo[isikhala_okufakwayo];
        if ((indlela_inqubo[isikhala_okufakwayo] & 0x400) != 0) 위치[isikhala_okufakwayo] = ubude_inani[Ihele];
        if (위치[isikhala_okufakwayo] >= 16384) return -28;
        while (ubude_inani[Ihele] < 위치[isikhala_okufakwayo]) bhala_imininingwane(Ihele, ubude_inani[Ihele]++, 0);
        bhala_imininingwane(Ihele, 위치[isikhala_okufakwayo]++, inani);
        if (ubude_inani[Ihele] < 위치[isikhala_okufakwayo]) ubude_inani[Ihele] = 위치[isikhala_okufakwayo];
        return 1;
    }
    public static int 옮기기(int 서술자, int 거리, int 기준) {
        int isikhala_okufakwayo = qiniseka(서술자);
        if (isikhala_okufakwayo < 0) return -9;
        if (기준 < 0 || 기준 > 2 || 거리 < -16384 || 거리 > 16384) return -22;
        int 새위치 = 거리 + (기준 == 0 ? 0 : 기준 == 1 ? 위치[isikhala_okufakwayo] : ubude_inani[impokophelo[isikhala_okufakwayo]]);
        if (새위치 < 0 || 새위치 > 16384) return -22;
        위치[isikhala_okufakwayo] = 새위치; return 새위치;
    }
    public static int Vala(int 서술자) {
        int isikhala_okufakwayo = qiniseka(서술자);
        if (isikhala_okufakwayo < 0) return -9;
        참조수[impokophelo[isikhala_okufakwayo]]--; 사용[isikhala_okufakwayo] = 0; return 0;
    }
    public static int Ubungako(int 서술자) {
        int isikhala_okufakwayo = qiniseka(서술자); return isikhala_okufakwayo < 0 ? -9 : ubude_inani[impokophelo[isikhala_okufakwayo]];
    }
    public static int isethi_ubude(int 서술자, int Ubungako) {
        int isikhala_okufakwayo = qiniseka(서술자);
        if (isikhala_okufakwayo < 0 || (indlela_inqubo[isikhala_okufakwayo] & 3) == 0) return -9;
        if (Ubungako < 0 || Ubungako > 16384) return -22;
        int Ihele = impokophelo[isikhala_okufakwayo];
        while (ubude_inani[Ihele] < Ubungako) bhala_imininingwane(Ihele, ubude_inani[Ihele]++, 0);
        ubude_inani[Ihele] = Ubungako; return 0;
    }
    public static int 지우기() {
        if (umzila_ubude == 0) return -22;
        int 결과 = beka_kujwayeleke_inani(); if (결과 < 0) return 결과;
        if (thola_umkhombandlela(정규길이) >= 0) return -21;
        결과 = 부모확인(); if (결과 < 0) return 결과;
        int Ihele = thola_okufakwayo();
        if (Ihele < 0) return -2;
        이름길이[Ihele] = 0; return 0; // 열려 있는 파일은 마지막 close까지 유지
    }
    static void okufakwayo_Uhlu() {
        umzila_qala(1); umzila_ibhayithi(0, '.'); 경로목록();
    }
    public static int 공개이름길이(int thola_inkomba) {
        if (thola_inkomba < 0 || thola_inkomba >= 파일수 || 이름길이[thola_inkomba] == 0) return 0;
        for (int iluphu_thola_inkomba = 0; iluphu_thola_inkomba < 이름길이[thola_inkomba]; iluphu_thola_inkomba++) if (Igama[thola_inkomba * 64 + iluphu_thola_inkomba] == '/') return 0;
        return 이름길이[thola_inkomba];
    }
    public static int 공개이름바이트(int thola_inkomba, int 자리) {
        return thola_inkomba >= 0 && thola_inkomba < 파일수 && 자리 >= 0 && 자리 < 이름길이[thola_inkomba] ? Igama[thola_inkomba * 64 + 자리] : -22;
    }
    public static int 공개파일크기(int thola_inkomba) { return thola_inkomba >= 0 && thola_inkomba < 파일수 ? ubude_inani[thola_inkomba] : -22; }
    static int[] 정규 = new int[64], 현재 = new int[64], umkhombandlela_igama = new int[16 * 64], umkhombandlela_ubude = new int[16];
    static int 정규길이, 현재길이;
    static boolean 접두(int[] 이름들, int Sebenzisa, int umzila_inani, int[] 앞, int izikhala_umzila) {
        if (umzila_inani < izikhala_umzila) return false;
        for (int iluphu_thola_inkomba = 0; iluphu_thola_inkomba < izikhala_umzila; iluphu_thola_inkomba++) if (이름들[Sebenzisa + iluphu_thola_inkomba] != 앞[iluphu_thola_inkomba]) return false;
        return true;
    }
    static int beka_kujwayeleke_inani() {
        if (umzila_ubude == 0) return -22;
        정규길이 = Indlela_2[0] == '/' ? 0 : 현재길이;
        for (int iluphu_thola_inkomba = 0; iluphu_thola_inkomba < 정규길이; iluphu_thola_inkomba++) 정규[iluphu_thola_inkomba] = 현재[iluphu_thola_inkomba];
        int 읽는자리 = 0;
        while (읽는자리 < umzila_ubude) {
            while (읽는자리 < umzila_ubude && Indlela_2[읽는자리] == '/') 읽는자리++;
            int 시작자리 = 읽는자리; while (읽는자리 < umzila_ubude && Indlela_2[읽는자리] != '/') { if (Indlela_2[읽는자리] == 0) return -22; 읽는자리++; }
            int 항목수 = 읽는자리 - 시작자리; if (항목수 == 0 || 항목수 == 1 && Indlela_2[시작자리] == '.') continue;
            if (항목수 == 2 && Indlela_2[시작자리] == '.' && Indlela_2[시작자리 + 1] == '.') {
                while (정규길이 > 0 && 정규[정규길이 - 1] != '/') 정규길이--;
                if (정규길이 > 0) 정규길이--;
                continue;
            }
            if (정규길이 + 항목수 + (정규길이 == 0 ? 0 : 1) > 63) return -36;
            if (정규길이 > 0) 정규[정규길이++] = '/';
            for (int iluphu_thola_inkomba = 시작자리; iluphu_thola_inkomba < 읽는자리; iluphu_thola_inkomba++) 정규[정규길이++] = Indlela_2[iluphu_thola_inkomba];
        }
        return 0;
    }
    static int thola_umkhombandlela(int 항목수) {
        if (항목수 == 0) return 0;
        for (int iluphu_thola_inkomba = 1; iluphu_thola_inkomba < 16; iluphu_thola_inkomba++) if (umkhombandlela_ubude[iluphu_thola_inkomba] == 항목수 && 접두(umkhombandlela_igama, iluphu_thola_inkomba * 64, 항목수, 정규, 항목수)) return iluphu_thola_inkomba;
        return -1;
    }
    static int 부모확인() {
        int 항목수 = 정규길이; while (항목수 > 0 && 정규[항목수 - 1] != '/') 항목수--;
        return thola_umkhombandlela(항목수 == 0 ? 0 : 항목수 - 1) < 0 ? -2 : 0;
    }
    public static int yakha_umkhombandlela() {
        int 처리값 = beka_kujwayeleke_inani(); if (처리값 < 0) return 처리값;
        if (thola_umkhombandlela(정규길이) >= 0 || thola_okufakwayo() >= 0) return -17;
        처리값 = 부모확인(); if (처리값 < 0) return 처리값;
        for (int iluphu_thola_inkomba = 1; iluphu_thola_inkomba < 16; iluphu_thola_inkomba++) if (umkhombandlela_ubude[iluphu_thola_inkomba] == 0) {
            umkhombandlela_ubude[iluphu_thola_inkomba] = 정규길이; for (int 안쪽자리 = 0; 안쪽자리 < 정규길이; 안쪽자리++) umkhombandlela_igama[iluphu_thola_inkomba * 64 + 안쪽자리] = 정규[안쪽자리]; return 0;
        }
        return -28;
    }
    public static int 항목종류() {
        int 처리값 = beka_kujwayeleke_inani(); if (처리값 < 0) return 처리값;
        if (thola_umkhombandlela(정규길이) >= 0) return 2;
        return thola_okufakwayo() >= 0 ? 1 : 0;
    }
    public static int guqula_umkhombandlela() {
        int 처리값 = beka_kujwayeleke_inani(); if (처리값 < 0) return 처리값;
        if (thola_umkhombandlela(정규길이) < 0) return -2;
        현재길이 = 정규길이; for (int iluphu_thola_inkomba = 0; iluphu_thola_inkomba < 현재길이; iluphu_thola_inkomba++) 현재[iluphu_thola_inkomba] = 정규[iluphu_thola_inkomba]; return 0;
    }
    public static int khipha_umkhombandlela() {
        int 처리값 = beka_kujwayeleke_inani(); if (처리값 < 0) return 처리값;
        int 폴더번호 = thola_umkhombandlela(정규길이); if (폴더번호 < 0) return -2; if (폴더번호 == 0) return -16;
        if (현재길이 == 정규길이 && 접두(현재, 0, 현재길이, 정규, 정규길이)) return -16;
        for (int iluphu_thola_inkomba = 0; iluphu_thola_inkomba < 파일수; iluphu_thola_inkomba++) {
            if (이름길이[iluphu_thola_inkomba] > 정규길이 && 접두(Igama, iluphu_thola_inkomba * 64, 이름길이[iluphu_thola_inkomba], 정규, 정규길이) && Igama[iluphu_thola_inkomba * 64 + 정규길이] == '/') return -39;
        }
        for (int iluphu_thola_inkomba = 0; iluphu_thola_inkomba < 16; iluphu_thola_inkomba++) {
            if (umkhombandlela_ubude[iluphu_thola_inkomba] > 정규길이 && 접두(umkhombandlela_igama, iluphu_thola_inkomba * 64, umkhombandlela_ubude[iluphu_thola_inkomba], 정규, 정규길이) && umkhombandlela_igama[iluphu_thola_inkomba * 64 + 정규길이] == '/') return -39;
        }
        umkhombandlela_ubude[폴더번호] = 0; return 0;
    }
    public static int 이름바꾸기(int 원본번호) {
        if (원본번호 < 0 || 원본번호 >= 파일수 || 이름길이[원본번호] == 0) return -2;
        int 처리값 = beka_kujwayeleke_inani(); if (처리값 < 0) return 처리값;
        if (thola_umkhombandlela(정규길이) >= 0) return -21;
        처리값 = 부모확인(); if (처리값 < 0) return 처리값;
        int 이전값 = thola_okufakwayo(); if (이전값 == 원본번호) return 0;
        if (이전값 >= 0) 이름길이[이전값] = 0;
        이름길이[원본번호] = 정규길이; for (int iluphu_thola_inkomba = 0; iluphu_thola_inkomba < 정규길이; iluphu_thola_inkomba++) Igama[원본번호 * 64 + iluphu_thola_inkomba] = 정규[iluphu_thola_inkomba]; return 0;
    }
    static int okufakwayo_qala(int[] imininingwane_AMALUNGU_AFANAYO, int 시작점, int 항목수) {
        if (!접두(imininingwane_AMALUNGU_AFANAYO, 시작점, 항목수, 정규, 정규길이)) return -1;
        int 시작자리 = 정규길이;
        if (시작자리 > 0) { if (항목수 <= 시작자리 || imininingwane_AMALUNGU_AFANAYO[시작점 + 시작자리] != '/') return -1; 시작자리++; }
        if (항목수 <= 시작자리) return -1;
        for (int iluphu_thola_inkomba = 시작자리; iluphu_thola_inkomba < 항목수; iluphu_thola_inkomba++) if (imininingwane_AMALUNGU_AFANAYO[시작점 + iluphu_thola_inkomba] == '/') return -1;
        return 시작자리;
    }
    static void 현재쓰기() { 단말.문자('/'); for (int iluphu_thola_inkomba = 0; iluphu_thola_inkomba < 현재길이; iluphu_thola_inkomba++) 보드.직렬쓰기(현재[iluphu_thola_inkomba]); }
    static int 경로목록() {
        int 처리값 = beka_kujwayeleke_inani(); if (처리값 < 0) return 처리값;
        int ifayela_impokophelo = thola_okufakwayo();
        if (ifayela_impokophelo >= 0) { for (int iluphu_thola_inkomba = 0; iluphu_thola_inkomba < 정규길이; iluphu_thola_inkomba++) 보드.직렬쓰기(정규[iluphu_thola_inkomba]); 단말.Bhala("  "); 단말.수(ubude_inani[ifayela_impokophelo]); 단말.Bhala("ibhayithi_inani(주기억 Ihele)\n"); return 0; }
        if (thola_umkhombandlela(정규길이) < 0) return -2;
        for (int 뒷값 = 1; 뒷값 < 16; 뒷값++) if (umkhombandlela_ubude[뒷값] > 0) {
            int 시작자리 = okufakwayo_qala(umkhombandlela_igama, 뒷값 * 64, umkhombandlela_ubude[뒷값]); if (시작자리 < 0) continue;
            for (int iluphu_thola_inkomba = 시작자리; iluphu_thola_inkomba < umkhombandlela_ubude[뒷값]; iluphu_thola_inkomba++) 보드.직렬쓰기(umkhombandlela_igama[뒷값 * 64 + iluphu_thola_inkomba]); 단말.Bhala("/\n");
        }
        for (int ifayela_thola_inkomba = 0; ifayela_thola_inkomba < 파일수; ifayela_thola_inkomba++) if (이름길이[ifayela_thola_inkomba] > 0) {
            int 시작자리 = okufakwayo_qala(Igama, ifayela_thola_inkomba * 64, 이름길이[ifayela_thola_inkomba]); if (시작자리 < 0) continue;
            for (int iluphu_thola_inkomba = 시작자리; iluphu_thola_inkomba < 이름길이[ifayela_thola_inkomba]; iluphu_thola_inkomba++) 보드.직렬쓰기(Igama[ifayela_thola_inkomba * 64 + iluphu_thola_inkomba]);
            단말.Bhala("  "); 단말.수(ubude_inani[ifayela_thola_inkomba]); 단말.Bhala("ibhayithi_inani(주기억 Ihele)\n");
        }
        return 0;
    }
}
