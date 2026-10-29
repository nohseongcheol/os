// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** RAM Fájl 64개, 파일당 16384바이트, 서술자 16개. 모든 adat/정책은 Java에 있다.
 * 호출 도중 양보하지 않으므로 현재의 단일 코어 협력식 작업 사이에서 원자적이다.
 * 디스크 저장이나 POSIX 전체 구현을 뜻하지 않는다. 음수 반환은 HIBA 번호다.
 */
public final class Memória_Files {
    static final int Fájl_DARAB = 64;
    static int[] Név = new int[Fájl_DARAB * 64];
    static int[] 이름길이 = new int[Fájl_DARAB];
    // Pack four bytes in each Java int, preserving the old content heap budget.
    static int[] Tartalom_ÉRTÉK = new int[Fájl_DARAB * 4096];
    static int[] hossz_ÉRTÉK = new int[Fájl_DARAB];
    static int[] hivatkozik_DARAB = new int[Fájl_DARAB];
    static int[] használ_ÉRTÉK = new int[16];
    static int[] cél = new int[16];
    static int[] Pozíció = new int[16];
    static int[] metódus_mód = new int[16];
    static int[] ÚTVONAL = new int[64];
    static int útvonal_hossz;

    public static int 파일한도() { return Fájl_DARAB; }
    static int 자료읽기(int Fájl, int helyzetindex) { return (Tartalom_ÉRTÉK[Fájl * 4096 + helyzetindex / 4] >>> ((helyzetindex & 3) * 8)) & 255; }
    static void ír_adat(int Fájl, int helyzetindex, int ÉRTÉK) {
        int tárolóhely_bejegyzés = Fájl * 4096 + helyzetindex / 4, áthelyez_ÉRTÉK = (helyzetindex & 3) * 8;
        Tartalom_ÉRTÉK[tárolóhely_bejegyzés] = (Tartalom_ÉRTÉK[tárolóhely_bejegyzés] & ~(255 << áthelyez_ÉRTÉK)) | ((ÉRTÉK & 255) << áthelyez_ÉRTÉK);
    }

    public static int útvonal_START(int Méret) {
        útvonal_hossz = 0;
        if (Méret < 1 || Méret > 63) return -36;
        útvonal_hossz = Méret;
        for (int Loop_INDEX = 0; Loop_INDEX < Méret; Loop_INDEX++) ÚTVONAL[Loop_INDEX] = 0;
        return 0;
    }
    public static int útvonal_bájt(int INDEX, int ÉRTÉK) {
        if (INDEX < 0 || INDEX >= útvonal_hossz || ÉRTÉK < 1 || ÉRTÉK > 255) return -22;
        ÚTVONAL[INDEX] = ÉRTÉK; return 0;
    }
    static int keres_bejegyzés() {
        for (int Fájl_INDEX = 0; Fájl_INDEX < Fájl_DARAB; Fájl_INDEX++) if (이름길이[Fájl_INDEX] > 0 && 이름길이[Fájl_INDEX] == Canonical_hossz && 접두(Név, Fájl_INDEX * 64, 이름길이[Fájl_INDEX], Canonical_ÉRTÉK, Canonical_hossz)) return Fájl_INDEX;
        return -1;
    }
    public static int Megnyitás(int 플래그) {
        if (útvonal_hossz == 0 || (플래그 & ~0x6c3) != 0 || (플래그 & 3) == 3) return -22;
        for (int Loop_INDEX = 0; Loop_INDEX < útvonal_hossz; Loop_INDEX++) if (ÚTVONAL[Loop_INDEX] == 0) return -22;
        if ((플래그 & 0x200) != 0 && (플래그 & 3) == 0) return -22;
        int KR = normalizál_ÉRTÉK(); if (KR < 0) return KR;
        if (keres_címtár(Canonical_hossz) >= 0) return -21;
        KR = csekk_szülő(); if (KR < 0) return KR;
        int Fájl = keres_bejegyzés();
        if (Fájl >= 0 && (플래그 & 0xc0) == 0xc0) return -17;
        if (Fájl < 0 && (플래그 & 0x40) == 0) return -2;
        int 서술자 = -1;
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (használ_ÉRTÉK[Loop_INDEX] == 0) { 서술자 = Loop_INDEX; break; }
        if (서술자 < 0) return -24;
        if (Fájl < 0) {
            for (int Loop_INDEX = 0; Loop_INDEX < Fájl_DARAB; Loop_INDEX++) if (이름길이[Loop_INDEX] == 0 && hivatkozik_DARAB[Loop_INDEX] == 0) { Fájl = Loop_INDEX; break; }
            if (Fájl < 0) return -28;
            이름길이[Fájl] = Canonical_hossz;
            for (int Loop_INDEX = 0; Loop_INDEX < Canonical_hossz; Loop_INDEX++) Név[Fájl * 64 + Loop_INDEX] = Canonical_ÉRTÉK[Loop_INDEX];
            hossz_ÉRTÉK[Fájl] = 0;
        }
        if ((플래그 & 0x200) != 0) hossz_ÉRTÉK[Fájl] = 0;
        használ_ÉRTÉK[서술자] = 1; cél[서술자] = Fájl; Pozíció[서술자] = 0; metódus_mód[서술자] = 플래그;
        hivatkozik_DARAB[Fájl]++;
        return 서술자 + 3;
    }
    static int igazol(int 서술자) {
        return 서술자 >= 3 && 서술자 < 19 && használ_ÉRTÉK[서술자 - 3] != 0 ? 서술자 - 3 : -1;
    }
    public static int Olvasás(int 서술자) {
        int tárolóhely_bejegyzés = igazol(서술자);
        if (tárolóhely_bejegyzés < 0 || (metódus_mód[tárolóhely_bejegyzés] & 3) == 1) return -9;
        int Fájl = cél[tárolóhely_bejegyzés];
        if (Pozíció[tárolóhely_bejegyzés] >= hossz_ÉRTÉK[Fájl]) return 256; // EOF와 tényleges_adat 0x00..0xff 구별
        return 자료읽기(Fájl, Pozíció[tárolóhely_bejegyzés]++);
    }
    public static int Írás(int 서술자, int ÉRTÉK) {
        int tárolóhely_bejegyzés = igazol(서술자);
        if (tárolóhely_bejegyzés < 0 || (metódus_mód[tárolóhely_bejegyzés] & 3) == 0) return -9;
        int Fájl = cél[tárolóhely_bejegyzés];
        if ((metódus_mód[tárolóhely_bejegyzés] & 0x400) != 0) Pozíció[tárolóhely_bejegyzés] = hossz_ÉRTÉK[Fájl];
        if (Pozíció[tárolóhely_bejegyzés] >= 16384) return -28;
        while (hossz_ÉRTÉK[Fájl] < Pozíció[tárolóhely_bejegyzés]) ír_adat(Fájl, hossz_ÉRTÉK[Fájl]++, 0);
        ír_adat(Fájl, Pozíció[tárolóhely_bejegyzés]++, ÉRTÉK);
        if (hossz_ÉRTÉK[Fájl] < Pozíció[tárolóhely_bejegyzés]) hossz_ÉRTÉK[Fájl] = Pozíció[tárolóhely_bejegyzés];
        return 1;
    }
    public static int keres_pozíció(int 서술자, int 거리, int teendő_gyök) {
        int tárolóhely_bejegyzés = igazol(서술자);
        if (tárolóhely_bejegyzés < 0) return -9;
        if (teendő_gyök < 0 || teendő_gyök > 2 || 거리 < -16384 || 거리 > 16384) return -22;
        int 새위치 = 거리 + (teendő_gyök == 0 ? 0 : teendő_gyök == 1 ? Pozíció[tárolóhely_bejegyzés] : hossz_ÉRTÉK[cél[tárolóhely_bejegyzés]]);
        if (새위치 < 0 || 새위치 > 16384) return -22;
        Pozíció[tárolóhely_bejegyzés] = 새위치; return 새위치;
    }
    public static int Bezárás(int 서술자) {
        int tárolóhely_bejegyzés = igazol(서술자);
        if (tárolóhely_bejegyzés < 0) return -9;
        hivatkozik_DARAB[cél[tárolóhely_bejegyzés]]--; használ_ÉRTÉK[tárolóhely_bejegyzés] = 0; return 0;
    }
    public static int Méret(int 서술자) {
        int tárolóhely_bejegyzés = igazol(서술자); return tárolóhely_bejegyzés < 0 ? -9 : hossz_ÉRTÉK[cél[tárolóhely_bejegyzés]];
    }
    public static int halmaz_hossz(int 서술자, int Méret) {
        int tárolóhely_bejegyzés = igazol(서술자);
        if (tárolóhely_bejegyzés < 0 || (metódus_mód[tárolóhely_bejegyzés] & 3) == 0) return -9;
        if (Méret < 0 || Méret > 16384) return -22;
        int Fájl = cél[tárolóhely_bejegyzés];
        while (hossz_ÉRTÉK[Fájl] < Méret) ír_adat(Fájl, hossz_ÉRTÉK[Fájl]++, 0);
        hossz_ÉRTÉK[Fájl] = Méret; return 0;
    }
    public static int töröl_bejegyzés() {
        if (útvonal_hossz == 0) return -22;
        int KR = normalizál_ÉRTÉK(); if (KR < 0) return KR;
        if (keres_címtár(Canonical_hossz) >= 0) return -21;
        KR = csekk_szülő(); if (KR < 0) return KR;
        int Fájl = keres_bejegyzés();
        if (Fájl < 0) return -2;
        이름길이[Fájl] = 0; return 0; // 열려 있는 파일은 마지막 close까지 유지
    }
    static void bejegyzés_Lista() {
        útvonal_START(1); útvonal_bájt(0, '.'); 경로목록();
    }
    public static int 공개이름길이(int INDEX) {
        if (INDEX < 0 || INDEX >= Fájl_DARAB || 이름길이[INDEX] == 0) return 0;
        for (int Loop_INDEX = 0; Loop_INDEX < 이름길이[INDEX]; Loop_INDEX++) if (Név[INDEX * 64 + Loop_INDEX] == '/') return 0;
        return 이름길이[INDEX];
    }
    public static int 공개이름바이트(int INDEX, int helyzetindex) {
        return INDEX >= 0 && INDEX < Fájl_DARAB && helyzetindex >= 0 && helyzetindex < 이름길이[INDEX] ? Név[INDEX * 64 + helyzetindex] : -22;
    }
    public static int 공개파일크기(int INDEX) { return INDEX >= 0 && INDEX < Fájl_DARAB ? hossz_ÉRTÉK[INDEX] : -22; }
    static int[] Canonical_ÉRTÉK = new int[64], aktuális_cikk = new int[64], címtár_név = new int[16 * 64], címtár_hossz = new int[16];
    static int Canonical_hossz, aktuális_hossz;
    static boolean 접두(int[] 이름들, int Futtatás, int útvonal_ÉRTÉK, int[] elülső_kamera_ÉRTÉK, int sorköz_útvonal) {
        if (útvonal_ÉRTÉK < sorköz_útvonal) return false;
        for (int Loop_INDEX = 0; Loop_INDEX < sorköz_útvonal; Loop_INDEX++) if (이름들[Futtatás + Loop_INDEX] != elülső_kamera_ÉRTÉK[Loop_INDEX]) return false;
        return true;
    }
    static int normalizál_ÉRTÉK() {
        if (útvonal_hossz == 0) return -22;
        Canonical_hossz = ÚTVONAL[0] == '/' ? 0 : aktuális_hossz;
        for (int Loop_INDEX = 0; Loop_INDEX < Canonical_hossz; Loop_INDEX++) Canonical_ÉRTÉK[Loop_INDEX] = aktuális_cikk[Loop_INDEX];
        int 읽는자리 = 0;
        while (읽는자리 < útvonal_hossz) {
            while (읽는자리 < útvonal_hossz && ÚTVONAL[읽는자리] == '/') 읽는자리++;
            int START_pozíció = 읽는자리; while (읽는자리 < útvonal_hossz && ÚTVONAL[읽는자리] != '/') { if (ÚTVONAL[읽는자리] == 0) return -22; 읽는자리++; }
            int bejegyzés_DARAB = 읽는자리 - START_pozíció; if (bejegyzés_DARAB == 0 || bejegyzés_DARAB == 1 && ÚTVONAL[START_pozíció] == '.') continue;
            if (bejegyzés_DARAB == 2 && ÚTVONAL[START_pozíció] == '.' && ÚTVONAL[START_pozíció + 1] == '.') {
                while (Canonical_hossz > 0 && Canonical_ÉRTÉK[Canonical_hossz - 1] != '/') Canonical_hossz--;
                if (Canonical_hossz > 0) Canonical_hossz--;
                continue;
            }
            if (Canonical_hossz + bejegyzés_DARAB + (Canonical_hossz == 0 ? 0 : 1) > 63) return -36;
            if (Canonical_hossz > 0) Canonical_ÉRTÉK[Canonical_hossz++] = '/';
            for (int Loop_INDEX = START_pozíció; Loop_INDEX < 읽는자리; Loop_INDEX++) Canonical_ÉRTÉK[Canonical_hossz++] = ÚTVONAL[Loop_INDEX];
        }
        return 0;
    }
    static int keres_címtár(int bejegyzés_DARAB) {
        if (bejegyzés_DARAB == 0) return 0;
        for (int Loop_INDEX = 1; Loop_INDEX < 16; Loop_INDEX++) if (címtár_hossz[Loop_INDEX] == bejegyzés_DARAB && 접두(címtár_név, Loop_INDEX * 64, bejegyzés_DARAB, Canonical_ÉRTÉK, bejegyzés_DARAB)) return Loop_INDEX;
        return -1;
    }
    static int csekk_szülő() {
        int bejegyzés_DARAB = Canonical_hossz; while (bejegyzés_DARAB > 0 && Canonical_ÉRTÉK[bejegyzés_DARAB - 1] != '/') bejegyzés_DARAB--;
        return keres_címtár(bejegyzés_DARAB == 0 ? 0 : bejegyzés_DARAB - 1) < 0 ? -2 : 0;
    }
    public static int készít_címtár() {
        int 처리값 = normalizál_ÉRTÉK(); if (처리값 < 0) return 처리값;
        if (keres_címtár(Canonical_hossz) >= 0 || keres_bejegyzés() >= 0) return -17;
        처리값 = csekk_szülő(); if (처리값 < 0) return 처리값;
        for (int Loop_INDEX = 1; Loop_INDEX < 16; Loop_INDEX++) if (címtár_hossz[Loop_INDEX] == 0) {
            címtár_hossz[Loop_INDEX] = Canonical_hossz; for (int belső_pozíció = 0; belső_pozíció < Canonical_hossz; belső_pozíció++) címtár_név[Loop_INDEX * 64 + belső_pozíció] = Canonical_ÉRTÉK[belső_pozíció]; return 0;
        }
        return -28;
    }
    public static int bejegyzés_Altípus() {
        int 처리값 = normalizál_ÉRTÉK(); if (처리값 < 0) return 처리값;
        if (keres_címtár(Canonical_hossz) >= 0) return 2;
        return keres_bejegyzés() >= 0 ? 1 : 0;
    }
    public static int módosítás_címtár() {
        int 처리값 = normalizál_ÉRTÉK(); if (처리값 < 0) return 처리값;
        if (keres_címtár(Canonical_hossz) < 0) return -2;
        aktuális_hossz = Canonical_hossz; for (int Loop_INDEX = 0; Loop_INDEX < aktuális_hossz; Loop_INDEX++) aktuális_cikk[Loop_INDEX] = Canonical_ÉRTÉK[Loop_INDEX]; return 0;
    }
    public static int eltávolít_címtár() {
        int 처리값 = normalizál_ÉRTÉK(); if (처리값 < 0) return 처리값;
        int címtár_szám = keres_címtár(Canonical_hossz); if (címtár_szám < 0) return -2; if (címtár_szám == 0) return -16;
        if (aktuális_hossz == Canonical_hossz && 접두(aktuális_cikk, 0, aktuális_hossz, Canonical_ÉRTÉK, Canonical_hossz)) return -16;
        for (int Loop_INDEX = 0; Loop_INDEX < Fájl_DARAB; Loop_INDEX++) {
            if (이름길이[Loop_INDEX] > Canonical_hossz && 접두(Név, Loop_INDEX * 64, 이름길이[Loop_INDEX], Canonical_ÉRTÉK, Canonical_hossz) && Név[Loop_INDEX * 64 + Canonical_hossz] == '/') return -39;
        }
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) {
            if (címtár_hossz[Loop_INDEX] > Canonical_hossz && 접두(címtár_név, Loop_INDEX * 64, címtár_hossz[Loop_INDEX], Canonical_ÉRTÉK, Canonical_hossz) && címtár_név[Loop_INDEX * 64 + Canonical_hossz] == '/') return -39;
        }
        címtár_hossz[címtár_szám] = 0; return 0;
    }
    public static int Átnevezés_bejegyzés(int 원본번호) {
        if (원본번호 < 0 || 원본번호 >= Fájl_DARAB || 이름길이[원본번호] == 0) return -2;
        int 처리값 = normalizál_ÉRTÉK(); if (처리값 < 0) return 처리값;
        if (keres_címtár(Canonical_hossz) >= 0) return -21;
        처리값 = csekk_szülő(); if (처리값 < 0) return 처리값;
        int Előző_ÉRTÉK = keres_bejegyzés(); if (Előző_ÉRTÉK == 원본번호) return 0;
        if (Előző_ÉRTÉK >= 0) 이름길이[Előző_ÉRTÉK] = 0;
        이름길이[원본번호] = Canonical_hossz; for (int Loop_INDEX = 0; Loop_INDEX < Canonical_hossz; Loop_INDEX++) Név[원본번호 * 64 + Loop_INDEX] = Canonical_ÉRTÉK[Loop_INDEX]; return 0;
    }
    static int bejegyzés_START(int[] adat_TÖMB, int 시작점, int bejegyzés_DARAB) {
        if (!접두(adat_TÖMB, 시작점, bejegyzés_DARAB, Canonical_ÉRTÉK, Canonical_hossz)) return -1;
        int START_pozíció = Canonical_hossz;
        if (START_pozíció > 0) { if (bejegyzés_DARAB <= START_pozíció || adat_TÖMB[시작점 + START_pozíció] != '/') return -1; START_pozíció++; }
        if (bejegyzés_DARAB <= START_pozíció) return -1;
        for (int Loop_INDEX = START_pozíció; Loop_INDEX < bejegyzés_DARAB; Loop_INDEX++) if (adat_TÖMB[시작점 + Loop_INDEX] == '/') return -1;
        return START_pozíció;
    }
    static void aktuális_ír() { 단말.문자('/'); for (int Loop_INDEX = 0; Loop_INDEX < aktuális_hossz; Loop_INDEX++) fal.직렬쓰기(aktuális_cikk[Loop_INDEX]); }
    static int 경로목록() {
        int 처리값 = normalizál_ÉRTÉK(); if (처리값 < 0) return 처리값;
        int Fájl_cél = keres_bejegyzés();
        if (Fájl_cél >= 0) { for (int Loop_INDEX = 0; Loop_INDEX < Canonical_hossz; Loop_INDEX++) fal.직렬쓰기(Canonical_ÉRTÉK[Loop_INDEX]); 단말.Írás("  "); 단말.szám(hossz_ÉRTÉK[Fájl_cél]); 단말.Írás("bájt_ÉRTÉK(주기억 Fájl)\n"); return 0; }
        if (keres_címtár(Canonical_hossz) < 0) return -2;
        for (int 뒷값 = 1; 뒷값 < 16; 뒷값++) if (címtár_hossz[뒷값] > 0) {
            int START_pozíció = bejegyzés_START(címtár_név, 뒷값 * 64, címtár_hossz[뒷값]); if (START_pozíció < 0) continue;
            for (int Loop_INDEX = START_pozíció; Loop_INDEX < címtár_hossz[뒷값]; Loop_INDEX++) fal.직렬쓰기(címtár_név[뒷값 * 64 + Loop_INDEX]); 단말.Írás("/\n");
        }
        for (int Fájl_INDEX = 0; Fájl_INDEX < Fájl_DARAB; Fájl_INDEX++) if (이름길이[Fájl_INDEX] > 0) {
            int START_pozíció = bejegyzés_START(Név, Fájl_INDEX * 64, 이름길이[Fájl_INDEX]); if (START_pozíció < 0) continue;
            for (int Loop_INDEX = START_pozíció; Loop_INDEX < 이름길이[Fájl_INDEX]; Loop_INDEX++) fal.직렬쓰기(Név[Fájl_INDEX * 64 + Loop_INDEX]);
            단말.Írás("  "); 단말.szám(hossz_ÉRTÉK[Fájl_INDEX]); 단말.Írás("bájt_ÉRTÉK(주기억 Fájl)\n");
        }
        return 0;
    }
}
