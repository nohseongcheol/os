// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** RAM Fitxategia 64개, 파일당 16384바이트, 서술자 16개. 모든 datuak/정책은 Java에 있다.
 * 호출 도중 양보하지 않으므로 현재의 단일 코어 협력식 작업 사이에서 원자적이다.
 * 디스크 저장이나 POSIX 전체 구현을 뜻하지 않는다. 음수 반환은 errorea 번호다.
 */
public final class Memoria_Fitxategiak {
    static final int fitxategi_ZENBATU = 64;
    static int[] Izena = new int[fitxategi_ZENBATU * 64];
    static int[] 이름길이 = new int[fitxategi_ZENBATU];
    // Pack four bytes in each Java int, preserving the old content heap budget.
    static int[] eduki_balio = new int[fitxategi_ZENBATU * 4096];
    static int[] luzera_balio = new int[fitxategi_ZENBATU];
    static int[] Erreferentzia_materiala_ZENBATU = new int[fitxategi_ZENBATU];
    static int[] 사용 = new int[16];
    static int[] helburu_balio = new int[16];
    static int[] Posizioa = new int[16];
    static int[] 방식 = new int[16];
    static int[] Bide_izena = new int[64];
    static int bide_izen_luzera;

    public static int 파일한도() { return fitxategi_ZENBATU; }
    static int 자료읽기(int Fitxategia, int kargu_INDIZE) { return (eduki_balio[Fitxategia * 4096 + kargu_INDIZE / 4] >>> ((kargu_INDIZE & 3) * 8)) & 255; }
    static void idatzi_datuak(int Fitxategia, int kargu_INDIZE, int balio) {
        int 칸 = Fitxategia * 4096 + kargu_INDIZE / 4, eraman_balio = (kargu_INDIZE & 3) * 8;
        eduki_balio[칸] = (eduki_balio[칸] & ~(255 << eraman_balio)) | ((balio & 255) << eraman_balio);
    }

    public static int bide_izen_HASI(int Tamaina) {
        bide_izen_luzera = 0;
        if (Tamaina < 1 || Tamaina > 63) return -36;
        bide_izen_luzera = Tamaina;
        for (int Loop_INDIZE = 0; Loop_INDIZE < Tamaina; Loop_INDIZE++) Bide_izena[Loop_INDIZE] = 0;
        return 0;
    }
    public static int bide_izen_byte(int INDIZE, int balio) {
        if (INDIZE < 0 || INDIZE >= bide_izen_luzera || balio < 1 || balio > 255) return -22;
        Bide_izena[INDIZE] = balio; return 0;
    }
    static int Bilatu_sarrera() {
        for (int fitxategi_INDIZE = 0; fitxategi_INDIZE < fitxategi_ZENBATU; fitxategi_INDIZE++) if (이름길이[fitxategi_INDIZE] > 0 && 이름길이[fitxategi_INDIZE] == 정규길이 && 접두(Izena, fitxategi_INDIZE * 64, 이름길이[fitxategi_INDIZE], 정규, 정규길이)) return fitxategi_INDIZE;
        return -1;
    }
    public static int Ireki(int 플래그) {
        if (bide_izen_luzera == 0 || (플래그 & ~0x6c3) != 0 || (플래그 & 3) == 3) return -22;
        for (int Loop_INDIZE = 0; Loop_INDIZE < bide_izen_luzera; Loop_INDIZE++) if (Bide_izena[Loop_INDIZE] == 0) return -22;
        if ((플래그 & 0x200) != 0 && (플래그 & 3) == 0) return -22;
        int EMAITZA = normalizatu_balio(); if (EMAITZA < 0) return EMAITZA;
        if (Bilatu_direktorio(정규길이) >= 0) return -21;
        EMAITZA = 부모확인(); if (EMAITZA < 0) return EMAITZA;
        int Fitxategia = Bilatu_sarrera();
        if (Fitxategia >= 0 && (플래그 & 0xc0) == 0xc0) return -17;
        if (Fitxategia < 0 && (플래그 & 0x40) == 0) return -2;
        int 서술자 = -1;
        for (int Loop_INDIZE = 0; Loop_INDIZE < 16; Loop_INDIZE++) if (사용[Loop_INDIZE] == 0) { 서술자 = Loop_INDIZE; break; }
        if (서술자 < 0) return -24;
        if (Fitxategia < 0) {
            for (int Loop_INDIZE = 0; Loop_INDIZE < fitxategi_ZENBATU; Loop_INDIZE++) if (이름길이[Loop_INDIZE] == 0 && Erreferentzia_materiala_ZENBATU[Loop_INDIZE] == 0) { Fitxategia = Loop_INDIZE; break; }
            if (Fitxategia < 0) return -28;
            이름길이[Fitxategia] = 정규길이;
            for (int Loop_INDIZE = 0; Loop_INDIZE < 정규길이; Loop_INDIZE++) Izena[Fitxategia * 64 + Loop_INDIZE] = 정규[Loop_INDIZE];
            luzera_balio[Fitxategia] = 0;
        }
        if ((플래그 & 0x200) != 0) luzera_balio[Fitxategia] = 0;
        사용[서술자] = 1; helburu_balio[서술자] = Fitxategia; Posizioa[서술자] = 0; 방식[서술자] = 플래그;
        Erreferentzia_materiala_ZENBATU[Fitxategia]++;
        return 서술자 + 3;
    }
    static int egiaztatu(int 서술자) {
        return 서술자 >= 3 && 서술자 < 19 && 사용[서술자 - 3] != 0 ? 서술자 - 3 : -1;
    }
    public static int Irakurri(int 서술자) {
        int 칸 = egiaztatu(서술자);
        if (칸 < 0 || (방식[칸] & 3) == 1) return -9;
        int Fitxategia = helburu_balio[칸];
        if (Posizioa[칸] >= luzera_balio[Fitxategia]) return 256; // EOF와 benetako_datuak 0x00..0xff 구별
        return 자료읽기(Fitxategia, Posizioa[칸]++);
    }
    public static int Idatzi(int 서술자, int balio) {
        int 칸 = egiaztatu(서술자);
        if (칸 < 0 || (방식[칸] & 3) == 0) return -9;
        int Fitxategia = helburu_balio[칸];
        if ((방식[칸] & 0x400) != 0) Posizioa[칸] = luzera_balio[Fitxategia];
        if (Posizioa[칸] >= 16384) return -28;
        while (luzera_balio[Fitxategia] < Posizioa[칸]) idatzi_datuak(Fitxategia, luzera_balio[Fitxategia]++, 0);
        idatzi_datuak(Fitxategia, Posizioa[칸]++, balio);
        if (luzera_balio[Fitxategia] < Posizioa[칸]) luzera_balio[Fitxategia] = Posizioa[칸];
        return 1;
    }
    public static int bilatu_kargu(int 서술자, int 거리, int Project_erro) {
        int 칸 = egiaztatu(서술자);
        if (칸 < 0) return -9;
        if (Project_erro < 0 || Project_erro > 2 || 거리 < -16384 || 거리 > 16384) return -22;
        int 새위치 = 거리 + (Project_erro == 0 ? 0 : Project_erro == 1 ? Posizioa[칸] : luzera_balio[helburu_balio[칸]]);
        if (새위치 < 0 || 새위치 > 16384) return -22;
        Posizioa[칸] = 새위치; return 새위치;
    }
    public static int Itxi(int 서술자) {
        int 칸 = egiaztatu(서술자);
        if (칸 < 0) return -9;
        Erreferentzia_materiala_ZENBATU[helburu_balio[칸]]--; 사용[칸] = 0; return 0;
    }
    public static int Tamaina(int 서술자) {
        int 칸 = egiaztatu(서술자); return 칸 < 0 ? -9 : luzera_balio[helburu_balio[칸]];
    }
    public static int sorta_luzera(int 서술자, int Tamaina) {
        int 칸 = egiaztatu(서술자);
        if (칸 < 0 || (방식[칸] & 3) == 0) return -9;
        if (Tamaina < 0 || Tamaina > 16384) return -22;
        int Fitxategia = helburu_balio[칸];
        while (luzera_balio[Fitxategia] < Tamaina) idatzi_datuak(Fitxategia, luzera_balio[Fitxategia]++, 0);
        luzera_balio[Fitxategia] = Tamaina; return 0;
    }
    public static int ezabatu_sarrera() {
        if (bide_izen_luzera == 0) return -22;
        int EMAITZA = normalizatu_balio(); if (EMAITZA < 0) return EMAITZA;
        if (Bilatu_direktorio(정규길이) >= 0) return -21;
        EMAITZA = 부모확인(); if (EMAITZA < 0) return EMAITZA;
        int Fitxategia = Bilatu_sarrera();
        if (Fitxategia < 0) return -2;
        이름길이[Fitxategia] = 0; return 0; // 열려 있는 파일은 마지막 close까지 유지
    }
    static void sarrera_Zerrenda() {
        bide_izen_HASI(1); bide_izen_byte(0, '.'); 경로목록();
    }
    public static int 공개이름길이(int INDIZE) {
        if (INDIZE < 0 || INDIZE >= fitxategi_ZENBATU || 이름길이[INDIZE] == 0) return 0;
        for (int Loop_INDIZE = 0; Loop_INDIZE < 이름길이[INDIZE]; Loop_INDIZE++) if (Izena[INDIZE * 64 + Loop_INDIZE] == '/') return 0;
        return 이름길이[INDIZE];
    }
    public static int 공개이름바이트(int INDIZE, int kargu_INDIZE) {
        return INDIZE >= 0 && INDIZE < fitxategi_ZENBATU && kargu_INDIZE >= 0 && kargu_INDIZE < 이름길이[INDIZE] ? Izena[INDIZE * 64 + kargu_INDIZE] : -22;
    }
    public static int 공개파일크기(int INDIZE) { return INDIZE >= 0 && INDIZE < fitxategi_ZENBATU ? luzera_balio[INDIZE] : -22; }
    static int[] 정규 = new int[64], 현재 = new int[64], direktorio_izen = new int[16 * 64], direktorio_luzera = new int[16];
    static int 정규길이, 현재길이;
    static boolean 접두(int[] 이름들, int Exekutatu_2, int bide_izen_balio, int[] aurrekoa_balio, int lerroarte_bide_izen) {
        if (bide_izen_balio < lerroarte_bide_izen) return false;
        for (int Loop_INDIZE = 0; Loop_INDIZE < lerroarte_bide_izen; Loop_INDIZE++) if (이름들[Exekutatu_2 + Loop_INDIZE] != aurrekoa_balio[Loop_INDIZE]) return false;
        return true;
    }
    static int normalizatu_balio() {
        if (bide_izen_luzera == 0) return -22;
        정규길이 = Bide_izena[0] == '/' ? 0 : 현재길이;
        for (int Loop_INDIZE = 0; Loop_INDIZE < 정규길이; Loop_INDIZE++) 정규[Loop_INDIZE] = 현재[Loop_INDIZE];
        int 읽는자리 = 0;
        while (읽는자리 < bide_izen_luzera) {
            while (읽는자리 < bide_izen_luzera && Bide_izena[읽는자리] == '/') 읽는자리++;
            int HASI_kargu = 읽는자리; while (읽는자리 < bide_izen_luzera && Bide_izena[읽는자리] != '/') { if (Bide_izena[읽는자리] == 0) return -22; 읽는자리++; }
            int sarrera_ZENBATU = 읽는자리 - HASI_kargu; if (sarrera_ZENBATU == 0 || sarrera_ZENBATU == 1 && Bide_izena[HASI_kargu] == '.') continue;
            if (sarrera_ZENBATU == 2 && Bide_izena[HASI_kargu] == '.' && Bide_izena[HASI_kargu + 1] == '.') {
                while (정규길이 > 0 && 정규[정규길이 - 1] != '/') 정규길이--;
                if (정규길이 > 0) 정규길이--;
                continue;
            }
            if (정규길이 + sarrera_ZENBATU + (정규길이 == 0 ? 0 : 1) > 63) return -36;
            if (정규길이 > 0) 정규[정규길이++] = '/';
            for (int Loop_INDIZE = HASI_kargu; Loop_INDIZE < 읽는자리; Loop_INDIZE++) 정규[정규길이++] = Bide_izena[Loop_INDIZE];
        }
        return 0;
    }
    static int Bilatu_direktorio(int sarrera_ZENBATU) {
        if (sarrera_ZENBATU == 0) return 0;
        for (int Loop_INDIZE = 1; Loop_INDIZE < 16; Loop_INDIZE++) if (direktorio_luzera[Loop_INDIZE] == sarrera_ZENBATU && 접두(direktorio_izen, Loop_INDIZE * 64, sarrera_ZENBATU, 정규, sarrera_ZENBATU)) return Loop_INDIZE;
        return -1;
    }
    static int 부모확인() {
        int sarrera_ZENBATU = 정규길이; while (sarrera_ZENBATU > 0 && 정규[sarrera_ZENBATU - 1] != '/') sarrera_ZENBATU--;
        return Bilatu_direktorio(sarrera_ZENBATU == 0 ? 0 : sarrera_ZENBATU - 1) < 0 ? -2 : 0;
    }
    public static int sortu_direktorio() {
        int 처리값 = normalizatu_balio(); if (처리값 < 0) return 처리값;
        if (Bilatu_direktorio(정규길이) >= 0 || Bilatu_sarrera() >= 0) return -17;
        처리값 = 부모확인(); if (처리값 < 0) return 처리값;
        for (int Loop_INDIZE = 1; Loop_INDIZE < 16; Loop_INDIZE++) if (direktorio_luzera[Loop_INDIZE] == 0) {
            direktorio_luzera[Loop_INDIZE] = 정규길이; for (int barnekoa_kargu = 0; barnekoa_kargu < 정규길이; barnekoa_kargu++) direktorio_izen[Loop_INDIZE * 64 + barnekoa_kargu] = 정규[barnekoa_kargu]; return 0;
        }
        return -28;
    }
    public static int 항목종류() {
        int 처리값 = normalizatu_balio(); if (처리값 < 0) return 처리값;
        if (Bilatu_direktorio(정규길이) >= 0) return 2;
        return Bilatu_sarrera() >= 0 ? 1 : 0;
    }
    public static int aldatu_direktorio() {
        int 처리값 = normalizatu_balio(); if (처리값 < 0) return 처리값;
        if (Bilatu_direktorio(정규길이) < 0) return -2;
        현재길이 = 정규길이; for (int Loop_INDIZE = 0; Loop_INDIZE < 현재길이; Loop_INDIZE++) 현재[Loop_INDIZE] = 정규[Loop_INDIZE]; return 0;
    }
    public static int kendu_direktorio() {
        int 처리값 = normalizatu_balio(); if (처리값 < 0) return 처리값;
        int 폴더번호 = Bilatu_direktorio(정규길이); if (폴더번호 < 0) return -2; if (폴더번호 == 0) return -16;
        if (현재길이 == 정규길이 && 접두(현재, 0, 현재길이, 정규, 정규길이)) return -16;
        for (int Loop_INDIZE = 0; Loop_INDIZE < fitxategi_ZENBATU; Loop_INDIZE++) {
            if (이름길이[Loop_INDIZE] > 정규길이 && 접두(Izena, Loop_INDIZE * 64, 이름길이[Loop_INDIZE], 정규, 정규길이) && Izena[Loop_INDIZE * 64 + 정규길이] == '/') return -39;
        }
        for (int Loop_INDIZE = 0; Loop_INDIZE < 16; Loop_INDIZE++) {
            if (direktorio_luzera[Loop_INDIZE] > 정규길이 && 접두(direktorio_izen, Loop_INDIZE * 64, direktorio_luzera[Loop_INDIZE], 정규, 정규길이) && direktorio_izen[Loop_INDIZE * 64 + 정규길이] == '/') return -39;
        }
        direktorio_luzera[폴더번호] = 0; return 0;
    }
    public static int 이름바꾸기(int 원본번호) {
        if (원본번호 < 0 || 원본번호 >= fitxategi_ZENBATU || 이름길이[원본번호] == 0) return -2;
        int 처리값 = normalizatu_balio(); if (처리값 < 0) return 처리값;
        if (Bilatu_direktorio(정규길이) >= 0) return -21;
        처리값 = 부모확인(); if (처리값 < 0) return 처리값;
        int 이전값 = Bilatu_sarrera(); if (이전값 == 원본번호) return 0;
        if (이전값 >= 0) 이름길이[이전값] = 0;
        이름길이[원본번호] = 정규길이; for (int Loop_INDIZE = 0; Loop_INDIZE < 정규길이; Loop_INDIZE++) Izena[원본번호 * 64 + Loop_INDIZE] = 정규[Loop_INDIZE]; return 0;
    }
    static int sarrera_HASI(int[] datuak_matrize, int 시작점, int sarrera_ZENBATU) {
        if (!접두(datuak_matrize, 시작점, sarrera_ZENBATU, 정규, 정규길이)) return -1;
        int HASI_kargu = 정규길이;
        if (HASI_kargu > 0) { if (sarrera_ZENBATU <= HASI_kargu || datuak_matrize[시작점 + HASI_kargu] != '/') return -1; HASI_kargu++; }
        if (sarrera_ZENBATU <= HASI_kargu) return -1;
        for (int Loop_INDIZE = HASI_kargu; Loop_INDIZE < sarrera_ZENBATU; Loop_INDIZE++) if (datuak_matrize[시작점 + Loop_INDIZE] == '/') return -1;
        return HASI_kargu;
    }
    static void 현재쓰기() { 단말.문자('/'); for (int Loop_INDIZE = 0; Loop_INDIZE < 현재길이; Loop_INDIZE++) arbel.직렬쓰기(현재[Loop_INDIZE]); }
    static int 경로목록() {
        int 처리값 = normalizatu_balio(); if (처리값 < 0) return 처리값;
        int fitxategi_helburu_balio = Bilatu_sarrera();
        if (fitxategi_helburu_balio >= 0) { for (int Loop_INDIZE = 0; Loop_INDIZE < 정규길이; Loop_INDIZE++) arbel.직렬쓰기(정규[Loop_INDIZE]); 단말.Idatzi("  "); 단말.수(luzera_balio[fitxategi_helburu_balio]); 단말.Idatzi("byte_balio(주기억 Fitxategia)\n"); return 0; }
        if (Bilatu_direktorio(정규길이) < 0) return -2;
        for (int 뒷값 = 1; 뒷값 < 16; 뒷값++) if (direktorio_luzera[뒷값] > 0) {
            int HASI_kargu = sarrera_HASI(direktorio_izen, 뒷값 * 64, direktorio_luzera[뒷값]); if (HASI_kargu < 0) continue;
            for (int Loop_INDIZE = HASI_kargu; Loop_INDIZE < direktorio_luzera[뒷값]; Loop_INDIZE++) arbel.직렬쓰기(direktorio_izen[뒷값 * 64 + Loop_INDIZE]); 단말.Idatzi("/\n");
        }
        for (int fitxategi_INDIZE = 0; fitxategi_INDIZE < fitxategi_ZENBATU; fitxategi_INDIZE++) if (이름길이[fitxategi_INDIZE] > 0) {
            int HASI_kargu = sarrera_HASI(Izena, fitxategi_INDIZE * 64, 이름길이[fitxategi_INDIZE]); if (HASI_kargu < 0) continue;
            for (int Loop_INDIZE = HASI_kargu; Loop_INDIZE < 이름길이[fitxategi_INDIZE]; Loop_INDIZE++) arbel.직렬쓰기(Izena[fitxategi_INDIZE * 64 + Loop_INDIZE]);
            단말.Idatzi("  "); 단말.수(luzera_balio[fitxategi_INDIZE]); 단말.Idatzi("byte_balio(주기억 Fitxategia)\n");
        }
        return 0;
    }
}
