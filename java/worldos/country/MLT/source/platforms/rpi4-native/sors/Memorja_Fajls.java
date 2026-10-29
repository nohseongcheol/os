// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** RAM fajl 64개, 파일당 16384바이트, 서술자 16개. 모든 data/정책은 Java에 있다.
 * 호출 도중 양보하지 않으므로 현재의 단일 코어 협력식 작업 사이에서 원자적이다.
 * 디스크 저장이나 POSIX 전체 구현을 뜻하지 않는다. 음수 반환은 żball 번호다.
 */
public final class Memorja_Fajls {
    static final int fajl_COUNT = 64;
    static int[] isem = new int[fajl_COUNT * 64];
    static int[] 이름길이 = new int[fajl_COUNT];
    // Pack four bytes in each Java int, preserving the old content heap budget.
    static int[] Kontenut_VALUE = new int[fajl_COUNT * 4096];
    static int[] tul_VALUE = new int[fajl_COUNT];
    static int[] Referenza_COUNT = new int[fajl_COUNT];
    static int[] 사용 = new int[16];
    static int[] mira = new int[16];
    static int[] pożizzjoni = new int[16];
    static int[] metodu_MODE = new int[16];
    static int[] mogħdija = new int[64];
    static int mogħdija_tul;

    public static int 파일한도() { return fajl_COUNT; }
    static int 자료읽기(int fajl, int pożizzjoni_INDEX) { return (Kontenut_VALUE[fajl * 4096 + pożizzjoni_INDEX / 4] >>> ((pożizzjoni_INDEX & 3) * 8)) & 255; }
    static void kiteb_data(int fajl, int pożizzjoni_INDEX, int VALUE) {
        int slott_entrata = fajl * 4096 + pożizzjoni_INDEX / 4, mexxi_VALUE = (pożizzjoni_INDEX & 3) * 8;
        Kontenut_VALUE[slott_entrata] = (Kontenut_VALUE[slott_entrata] & ~(255 << mexxi_VALUE)) | ((VALUE & 255) << mexxi_VALUE);
    }

    public static int mogħdija_Bidu(int daqqas) {
        mogħdija_tul = 0;
        if (daqqas < 1 || daqqas > 63) return -36;
        mogħdija_tul = daqqas;
        for (int Loop_INDEX = 0; Loop_INDEX < daqqas; Loop_INDEX++) mogħdija[Loop_INDEX] = 0;
        return 0;
    }
    public static int mogħdija_byte(int INDEX, int VALUE) {
        if (INDEX < 0 || INDEX >= mogħdija_tul || VALUE < 1 || VALUE > 255) return -22;
        mogħdija[INDEX] = VALUE; return 0;
    }
    static int sab_entrata() {
        for (int fajl_INDEX = 0; fajl_INDEX < fajl_COUNT; fajl_INDEX++) if (이름길이[fajl_INDEX] > 0 && 이름길이[fajl_INDEX] == 정규길이 && 접두(isem, fajl_INDEX * 64, 이름길이[fajl_INDEX], 정규, 정규길이)) return fajl_INDEX;
        return -1;
    }
    public static int fetaħ(int 플래그) {
        if (mogħdija_tul == 0 || (플래그 & ~0x6c3) != 0 || (플래그 & 3) == 3) return -22;
        for (int Loop_INDEX = 0; Loop_INDEX < mogħdija_tul; Loop_INDEX++) if (mogħdija[Loop_INDEX] == 0) return -22;
        if ((플래그 & 0x200) != 0 && (플래그 & 3) == 0) return -22;
        int miżura = nnormalizza_VALUE(); if (miżura < 0) return miżura;
        if (sab_direttorju(정규길이) >= 0) return -21;
        miżura = 부모확인(); if (miżura < 0) return miżura;
        int fajl = sab_entrata();
        if (fajl >= 0 && (플래그 & 0xc0) == 0xc0) return -17;
        if (fajl < 0 && (플래그 & 0x40) == 0) return -2;
        int 서술자 = -1;
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (사용[Loop_INDEX] == 0) { 서술자 = Loop_INDEX; break; }
        if (서술자 < 0) return -24;
        if (fajl < 0) {
            for (int Loop_INDEX = 0; Loop_INDEX < fajl_COUNT; Loop_INDEX++) if (이름길이[Loop_INDEX] == 0 && Referenza_COUNT[Loop_INDEX] == 0) { fajl = Loop_INDEX; break; }
            if (fajl < 0) return -28;
            이름길이[fajl] = 정규길이;
            for (int Loop_INDEX = 0; Loop_INDEX < 정규길이; Loop_INDEX++) isem[fajl * 64 + Loop_INDEX] = 정규[Loop_INDEX];
            tul_VALUE[fajl] = 0;
        }
        if ((플래그 & 0x200) != 0) tul_VALUE[fajl] = 0;
        사용[서술자] = 1; mira[서술자] = fajl; pożizzjoni[서술자] = 0; metodu_MODE[서술자] = 플래그;
        Referenza_COUNT[fajl]++;
        return 서술자 + 3;
    }
    static int vverifika(int 서술자) {
        return 서술자 >= 3 && 서술자 < 19 && 사용[서술자 - 3] != 0 ? 서술자 - 3 : -1;
    }
    public static int 읽기(int 서술자) {
        int slott_entrata = vverifika(서술자);
        if (slott_entrata < 0 || (metodu_MODE[slott_entrata] & 3) == 1) return -9;
        int fajl = mira[slott_entrata];
        if (pożizzjoni[slott_entrata] >= tul_VALUE[fajl]) return 256; // EOF와 attwali_data 0x00..0xff 구별
        return 자료읽기(fajl, pożizzjoni[slott_entrata]++);
    }
    public static int kiteb(int 서술자, int VALUE) {
        int slott_entrata = vverifika(서술자);
        if (slott_entrata < 0 || (metodu_MODE[slott_entrata] & 3) == 0) return -9;
        int fajl = mira[slott_entrata];
        if ((metodu_MODE[slott_entrata] & 0x400) != 0) pożizzjoni[slott_entrata] = tul_VALUE[fajl];
        if (pożizzjoni[slott_entrata] >= 16384) return -28;
        while (tul_VALUE[fajl] < pożizzjoni[slott_entrata]) kiteb_data(fajl, tul_VALUE[fajl]++, 0);
        kiteb_data(fajl, pożizzjoni[slott_entrata]++, VALUE);
        if (tul_VALUE[fajl] < pożizzjoni[slott_entrata]) tul_VALUE[fajl] = pożizzjoni[slott_entrata];
        return 1;
    }
    public static int fittex_pożizzjoni(int 서술자, int 거리, int pprojetta_għerq) {
        int slott_entrata = vverifika(서술자);
        if (slott_entrata < 0) return -9;
        if (pprojetta_għerq < 0 || pprojetta_għerq > 2 || 거리 < -16384 || 거리 > 16384) return -22;
        int 새위치 = 거리 + (pprojetta_għerq == 0 ? 0 : pprojetta_għerq == 1 ? pożizzjoni[slott_entrata] : tul_VALUE[mira[slott_entrata]]);
        if (새위치 < 0 || 새위치 > 16384) return -22;
        pożizzjoni[slott_entrata] = 새위치; return 새위치;
    }
    public static int agħlaq(int 서술자) {
        int slott_entrata = vverifika(서술자);
        if (slott_entrata < 0) return -9;
        Referenza_COUNT[mira[slott_entrata]]--; 사용[slott_entrata] = 0; return 0;
    }
    public static int daqqas(int 서술자) {
        int slott_entrata = vverifika(서술자); return slott_entrata < 0 ? -9 : tul_VALUE[mira[slott_entrata]];
    }
    public static int sett_tul(int 서술자, int daqqas) {
        int slott_entrata = vverifika(서술자);
        if (slott_entrata < 0 || (metodu_MODE[slott_entrata] & 3) == 0) return -9;
        if (daqqas < 0 || daqqas > 16384) return -22;
        int fajl = mira[slott_entrata];
        while (tul_VALUE[fajl] < daqqas) kiteb_data(fajl, tul_VALUE[fajl]++, 0);
        tul_VALUE[fajl] = daqqas; return 0;
    }
    public static int 지우기() {
        if (mogħdija_tul == 0) return -22;
        int miżura = nnormalizza_VALUE(); if (miżura < 0) return miżura;
        if (sab_direttorju(정규길이) >= 0) return -21;
        miżura = 부모확인(); if (miżura < 0) return miżura;
        int fajl = sab_entrata();
        if (fajl < 0) return -2;
        이름길이[fajl] = 0; return 0; // 열려 있는 파일은 마지막 close까지 유지
    }
    static void entrata_Lista() {
        mogħdija_Bidu(1); mogħdija_byte(0, '.'); 경로목록();
    }
    public static int 공개이름길이(int INDEX) {
        if (INDEX < 0 || INDEX >= fajl_COUNT || 이름길이[INDEX] == 0) return 0;
        for (int Loop_INDEX = 0; Loop_INDEX < 이름길이[INDEX]; Loop_INDEX++) if (isem[INDEX * 64 + Loop_INDEX] == '/') return 0;
        return 이름길이[INDEX];
    }
    public static int 공개이름바이트(int INDEX, int pożizzjoni_INDEX) {
        return INDEX >= 0 && INDEX < fajl_COUNT && pożizzjoni_INDEX >= 0 && pożizzjoni_INDEX < 이름길이[INDEX] ? isem[INDEX * 64 + pożizzjoni_INDEX] : -22;
    }
    public static int 공개파일크기(int INDEX) { return INDEX >= 0 && INDEX < fajl_COUNT ? tul_VALUE[INDEX] : -22; }
    static int[] 정규 = new int[64], 현재 = new int[64], direttorju_isem = new int[16 * 64], direttorju_tul = new int[16];
    static int 정규길이, 현재길이;
    static boolean 접두(int[] 이름들, int serje, int mogħdija_VALUE, int[] 앞, int leading_mogħdija) {
        if (mogħdija_VALUE < leading_mogħdija) return false;
        for (int Loop_INDEX = 0; Loop_INDEX < leading_mogħdija; Loop_INDEX++) if (이름들[serje + Loop_INDEX] != 앞[Loop_INDEX]) return false;
        return true;
    }
    static int nnormalizza_VALUE() {
        if (mogħdija_tul == 0) return -22;
        정규길이 = mogħdija[0] == '/' ? 0 : 현재길이;
        for (int Loop_INDEX = 0; Loop_INDEX < 정규길이; Loop_INDEX++) 정규[Loop_INDEX] = 현재[Loop_INDEX];
        int 읽는자리 = 0;
        while (읽는자리 < mogħdija_tul) {
            while (읽는자리 < mogħdija_tul && mogħdija[읽는자리] == '/') 읽는자리++;
            int Bidu_pożizzjoni = 읽는자리; while (읽는자리 < mogħdija_tul && mogħdija[읽는자리] != '/') { if (mogħdija[읽는자리] == 0) return -22; 읽는자리++; }
            int entrata_COUNT = 읽는자리 - Bidu_pożizzjoni; if (entrata_COUNT == 0 || entrata_COUNT == 1 && mogħdija[Bidu_pożizzjoni] == '.') continue;
            if (entrata_COUNT == 2 && mogħdija[Bidu_pożizzjoni] == '.' && mogħdija[Bidu_pożizzjoni + 1] == '.') {
                while (정규길이 > 0 && 정규[정규길이 - 1] != '/') 정규길이--;
                if (정규길이 > 0) 정규길이--;
                continue;
            }
            if (정규길이 + entrata_COUNT + (정규길이 == 0 ? 0 : 1) > 63) return -36;
            if (정규길이 > 0) 정규[정규길이++] = '/';
            for (int Loop_INDEX = Bidu_pożizzjoni; Loop_INDEX < 읽는자리; Loop_INDEX++) 정규[정규길이++] = mogħdija[Loop_INDEX];
        }
        return 0;
    }
    static int sab_direttorju(int entrata_COUNT) {
        if (entrata_COUNT == 0) return 0;
        for (int Loop_INDEX = 1; Loop_INDEX < 16; Loop_INDEX++) if (direttorju_tul[Loop_INDEX] == entrata_COUNT && 접두(direttorju_isem, Loop_INDEX * 64, entrata_COUNT, 정규, entrata_COUNT)) return Loop_INDEX;
        return -1;
    }
    static int 부모확인() {
        int entrata_COUNT = 정규길이; while (entrata_COUNT > 0 && 정규[entrata_COUNT - 1] != '/') entrata_COUNT--;
        return sab_direttorju(entrata_COUNT == 0 ? 0 : entrata_COUNT - 1) < 0 ? -2 : 0;
    }
    public static int ħalaq_direttorju() {
        int 처리값 = nnormalizza_VALUE(); if (처리값 < 0) return 처리값;
        if (sab_direttorju(정규길이) >= 0 || sab_entrata() >= 0) return -17;
        처리값 = 부모확인(); if (처리값 < 0) return 처리값;
        for (int Loop_INDEX = 1; Loop_INDEX < 16; Loop_INDEX++) if (direttorju_tul[Loop_INDEX] == 0) {
            direttorju_tul[Loop_INDEX] = 정규길이; for (int inner_join_pożizzjoni = 0; inner_join_pożizzjoni < 정규길이; inner_join_pożizzjoni++) direttorju_isem[Loop_INDEX * 64 + inner_join_pożizzjoni] = 정규[inner_join_pożizzjoni]; return 0;
        }
        return -28;
    }
    public static int 항목종류() {
        int 처리값 = nnormalizza_VALUE(); if (처리값 < 0) return 처리값;
        if (sab_direttorju(정규길이) >= 0) return 2;
        return sab_entrata() >= 0 ? 1 : 0;
    }
    public static int bidel_direttorju() {
        int 처리값 = nnormalizza_VALUE(); if (처리값 < 0) return 처리값;
        if (sab_direttorju(정규길이) < 0) return -2;
        현재길이 = 정규길이; for (int Loop_INDEX = 0; Loop_INDEX < 현재길이; Loop_INDEX++) 현재[Loop_INDEX] = 정규[Loop_INDEX]; return 0;
    }
    public static int neħħa_direttorju() {
        int 처리값 = nnormalizza_VALUE(); if (처리값 < 0) return 처리값;
        int 폴더번호 = sab_direttorju(정규길이); if (폴더번호 < 0) return -2; if (폴더번호 == 0) return -16;
        if (현재길이 == 정규길이 && 접두(현재, 0, 현재길이, 정규, 정규길이)) return -16;
        for (int Loop_INDEX = 0; Loop_INDEX < fajl_COUNT; Loop_INDEX++) {
            if (이름길이[Loop_INDEX] > 정규길이 && 접두(isem, Loop_INDEX * 64, 이름길이[Loop_INDEX], 정규, 정규길이) && isem[Loop_INDEX * 64 + 정규길이] == '/') return -39;
        }
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) {
            if (direttorju_tul[Loop_INDEX] > 정규길이 && 접두(direttorju_isem, Loop_INDEX * 64, direttorju_tul[Loop_INDEX], 정규, 정규길이) && direttorju_isem[Loop_INDEX * 64 + 정규길이] == '/') return -39;
        }
        direttorju_tul[폴더번호] = 0; return 0;
    }
    public static int 이름바꾸기(int 원본번호) {
        if (원본번호 < 0 || 원본번호 >= fajl_COUNT || 이름길이[원본번호] == 0) return -2;
        int 처리값 = nnormalizza_VALUE(); if (처리값 < 0) return 처리값;
        if (sab_direttorju(정규길이) >= 0) return -21;
        처리값 = 부모확인(); if (처리값 < 0) return 처리값;
        int 이전값 = sab_entrata(); if (이전값 == 원본번호) return 0;
        if (이전값 >= 0) 이름길이[이전값] = 0;
        이름길이[원본번호] = 정규길이; for (int Loop_INDEX = 0; Loop_INDEX < 정규길이; Loop_INDEX++) isem[원본번호 * 64 + Loop_INDEX] = 정규[Loop_INDEX]; return 0;
    }
    static int entrata_Bidu(int[] data_ARRAY, int 시작점, int entrata_COUNT) {
        if (!접두(data_ARRAY, 시작점, entrata_COUNT, 정규, 정규길이)) return -1;
        int Bidu_pożizzjoni = 정규길이;
        if (Bidu_pożizzjoni > 0) { if (entrata_COUNT <= Bidu_pożizzjoni || data_ARRAY[시작점 + Bidu_pożizzjoni] != '/') return -1; Bidu_pożizzjoni++; }
        if (entrata_COUNT <= Bidu_pożizzjoni) return -1;
        for (int Loop_INDEX = Bidu_pożizzjoni; Loop_INDEX < entrata_COUNT; Loop_INDEX++) if (data_ARRAY[시작점 + Loop_INDEX] == '/') return -1;
        return Bidu_pożizzjoni;
    }
    static void 현재쓰기() { 단말.문자('/'); for (int Loop_INDEX = 0; Loop_INDEX < 현재길이; Loop_INDEX++) bord.직렬쓰기(현재[Loop_INDEX]); }
    static int 경로목록() {
        int 처리값 = nnormalizza_VALUE(); if (처리값 < 0) return 처리값;
        int fajl_mira = sab_entrata();
        if (fajl_mira >= 0) { for (int Loop_INDEX = 0; Loop_INDEX < 정규길이; Loop_INDEX++) bord.직렬쓰기(정규[Loop_INDEX]); 단말.kiteb("  "); 단말.수(tul_VALUE[fajl_mira]); 단말.kiteb("byte_VALUE(주기억 fajl)\n"); return 0; }
        if (sab_direttorju(정규길이) < 0) return -2;
        for (int 뒷값 = 1; 뒷값 < 16; 뒷값++) if (direttorju_tul[뒷값] > 0) {
            int Bidu_pożizzjoni = entrata_Bidu(direttorju_isem, 뒷값 * 64, direttorju_tul[뒷값]); if (Bidu_pożizzjoni < 0) continue;
            for (int Loop_INDEX = Bidu_pożizzjoni; Loop_INDEX < direttorju_tul[뒷값]; Loop_INDEX++) bord.직렬쓰기(direttorju_isem[뒷값 * 64 + Loop_INDEX]); 단말.kiteb("/\n");
        }
        for (int fajl_INDEX = 0; fajl_INDEX < fajl_COUNT; fajl_INDEX++) if (이름길이[fajl_INDEX] > 0) {
            int Bidu_pożizzjoni = entrata_Bidu(isem, fajl_INDEX * 64, 이름길이[fajl_INDEX]); if (Bidu_pożizzjoni < 0) continue;
            for (int Loop_INDEX = Bidu_pożizzjoni; Loop_INDEX < 이름길이[fajl_INDEX]; Loop_INDEX++) bord.직렬쓰기(isem[fajl_INDEX * 64 + Loop_INDEX]);
            단말.kiteb("  "); 단말.수(tul_VALUE[fajl_INDEX]); 단말.kiteb("byte_VALUE(주기억 fajl)\n");
        }
        return 0;
    }
}
