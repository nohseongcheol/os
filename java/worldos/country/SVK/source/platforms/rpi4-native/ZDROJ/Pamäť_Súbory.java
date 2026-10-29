// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** RAM Súbor 64개, 파일당 16384바이트, 서술자 16개. 모든 údaje/정책은 Java에 있다.
 * 호출 도중 양보하지 않으므로 현재의 단일 코어 협력식 작업 사이에서 원자적이다.
 * 디스크 저장이나 POSIX 전체 구현을 뜻하지 않는다. 음수 반환은 chyba 번호다.
 */
public final class Pamäť_Súbory {
    static final int Súbor_COUNT = 64;
    static int[] Názov = new int[Súbor_COUNT * 64];
    static int[] 이름길이 = new int[Súbor_COUNT];
    // Pack four bytes in each Java int, preserving the old content heap budget.
    static int[] obsah_VALUE = new int[Súbor_COUNT * 4096];
    static int[] dĺžka_VALUE = new int[Súbor_COUNT];
    static int[] zdroj_COUNT = new int[Súbor_COUNT];
    static int[] používať_VALUE = new int[16];
    static int[] cieľová_hodnota = new int[16];
    static int[] Pozícia = new int[16];
    static int[] metóda_MODE = new int[16];
    static int[] Cesta = new int[64];
    static int cesta_dĺžka;

    public static int 파일한도() { return Súbor_COUNT; }
    static int 자료읽기(int Súbor, int pozičný_index) { return (obsah_VALUE[Súbor * 4096 + pozičný_index / 4] >>> ((pozičný_index & 3) * 8)) & 255; }
    static void zapísať_údaje(int Súbor, int pozičný_index, int VALUE) {
        int 칸 = Súbor * 4096 + pozičný_index / 4, premiestniť_VALUE = (pozičný_index & 3) * 8;
        obsah_VALUE[칸] = (obsah_VALUE[칸] & ~(255 << premiestniť_VALUE)) | ((VALUE & 255) << premiestniť_VALUE);
    }

    public static int cesta_START(int Veľkosť) {
        cesta_dĺžka = 0;
        if (Veľkosť < 1 || Veľkosť > 63) return -36;
        cesta_dĺžka = Veľkosť;
        for (int Loop_INDEX = 0; Loop_INDEX < Veľkosť; Loop_INDEX++) Cesta[Loop_INDEX] = 0;
        return 0;
    }
    public static int cesta_Byte(int INDEX, int VALUE) {
        if (INDEX < 0 || INDEX >= cesta_dĺžka || VALUE < 1 || VALUE > 255) return -22;
        Cesta[INDEX] = VALUE; return 0;
    }
    static int FIND_položka() {
        for (int Súbor_INDEX = 0; Súbor_INDEX < Súbor_COUNT; Súbor_INDEX++) if (이름길이[Súbor_INDEX] > 0 && 이름길이[Súbor_INDEX] == 정규길이 && 접두(Názov, Súbor_INDEX * 64, 이름길이[Súbor_INDEX], 정규, 정규길이)) return Súbor_INDEX;
        return -1;
    }
    public static int Otvoriť(int 플래그) {
        if (cesta_dĺžka == 0 || (플래그 & ~0x6c3) != 0 || (플래그 & 3) == 3) return -22;
        for (int Loop_INDEX = 0; Loop_INDEX < cesta_dĺžka; Loop_INDEX++) if (Cesta[Loop_INDEX] == 0) return -22;
        if ((플래그 & 0x200) != 0 && (플래그 & 3) == 0) return -22;
        int KR = normalizovať_VALUE(); if (KR < 0) return KR;
        if (FIND_Adresár(정규길이) >= 0) return -21;
        KR = skontrolovať_nadradený(); if (KR < 0) return KR;
        int Súbor = FIND_položka();
        if (Súbor >= 0 && (플래그 & 0xc0) == 0xc0) return -17;
        if (Súbor < 0 && (플래그 & 0x40) == 0) return -2;
        int 서술자 = -1;
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (používať_VALUE[Loop_INDEX] == 0) { 서술자 = Loop_INDEX; break; }
        if (서술자 < 0) return -24;
        if (Súbor < 0) {
            for (int Loop_INDEX = 0; Loop_INDEX < Súbor_COUNT; Loop_INDEX++) if (이름길이[Loop_INDEX] == 0 && zdroj_COUNT[Loop_INDEX] == 0) { Súbor = Loop_INDEX; break; }
            if (Súbor < 0) return -28;
            이름길이[Súbor] = 정규길이;
            for (int Loop_INDEX = 0; Loop_INDEX < 정규길이; Loop_INDEX++) Názov[Súbor * 64 + Loop_INDEX] = 정규[Loop_INDEX];
            dĺžka_VALUE[Súbor] = 0;
        }
        if ((플래그 & 0x200) != 0) dĺžka_VALUE[Súbor] = 0;
        používať_VALUE[서술자] = 1; cieľová_hodnota[서술자] = Súbor; Pozícia[서술자] = 0; metóda_MODE[서술자] = 플래그;
        zdroj_COUNT[Súbor]++;
        return 서술자 + 3;
    }
    static int overiť(int 서술자) {
        return 서술자 >= 3 && 서술자 < 19 && používať_VALUE[서술자 - 3] != 0 ? 서술자 - 3 : -1;
    }
    public static int Čítanie(int 서술자) {
        int 칸 = overiť(서술자);
        if (칸 < 0 || (metóda_MODE[칸] & 3) == 1) return -9;
        int Súbor = cieľová_hodnota[칸];
        if (Pozícia[칸] >= dĺžka_VALUE[Súbor]) return 256; // EOF와 skutočný_údaje 0x00..0xff 구별
        return 자료읽기(Súbor, Pozícia[칸]++);
    }
    public static int Zápis(int 서술자, int VALUE) {
        int 칸 = overiť(서술자);
        if (칸 < 0 || (metóda_MODE[칸] & 3) == 0) return -9;
        int Súbor = cieľová_hodnota[칸];
        if ((metóda_MODE[칸] & 0x400) != 0) Pozícia[칸] = dĺžka_VALUE[Súbor];
        if (Pozícia[칸] >= 16384) return -28;
        while (dĺžka_VALUE[Súbor] < Pozícia[칸]) zapísať_údaje(Súbor, dĺžka_VALUE[Súbor]++, 0);
        zapísať_údaje(Súbor, Pozícia[칸]++, VALUE);
        if (dĺžka_VALUE[Súbor] < Pozícia[칸]) dĺžka_VALUE[Súbor] = Pozícia[칸];
        return 1;
    }
    public static int hľadať_pozícia(int 서술자, int 거리, int akcia_koreň) {
        int 칸 = overiť(서술자);
        if (칸 < 0) return -9;
        if (akcia_koreň < 0 || akcia_koreň > 2 || 거리 < -16384 || 거리 > 16384) return -22;
        int 새위치 = 거리 + (akcia_koreň == 0 ? 0 : akcia_koreň == 1 ? Pozícia[칸] : dĺžka_VALUE[cieľová_hodnota[칸]]);
        if (새위치 < 0 || 새위치 > 16384) return -22;
        Pozícia[칸] = 새위치; return 새위치;
    }
    public static int Zatvoriť(int 서술자) {
        int 칸 = overiť(서술자);
        if (칸 < 0) return -9;
        zdroj_COUNT[cieľová_hodnota[칸]]--; používať_VALUE[칸] = 0; return 0;
    }
    public static int Veľkosť(int 서술자) {
        int 칸 = overiť(서술자); return 칸 < 0 ? -9 : dĺžka_VALUE[cieľová_hodnota[칸]];
    }
    public static int množina_dĺžka(int 서술자, int Veľkosť) {
        int 칸 = overiť(서술자);
        if (칸 < 0 || (metóda_MODE[칸] & 3) == 0) return -9;
        if (Veľkosť < 0 || Veľkosť > 16384) return -22;
        int Súbor = cieľová_hodnota[칸];
        while (dĺžka_VALUE[Súbor] < Veľkosť) zapísať_údaje(Súbor, dĺžka_VALUE[Súbor]++, 0);
        dĺžka_VALUE[Súbor] = Veľkosť; return 0;
    }
    public static int vymazať_položka() {
        if (cesta_dĺžka == 0) return -22;
        int KR = normalizovať_VALUE(); if (KR < 0) return KR;
        if (FIND_Adresár(정규길이) >= 0) return -21;
        KR = skontrolovať_nadradený(); if (KR < 0) return KR;
        int Súbor = FIND_položka();
        if (Súbor < 0) return -2;
        이름길이[Súbor] = 0; return 0; // 열려 있는 파일은 마지막 close까지 유지
    }
    static void položka_Zoznam() {
        cesta_START(1); cesta_Byte(0, '.'); 경로목록();
    }
    public static int 공개이름길이(int INDEX) {
        if (INDEX < 0 || INDEX >= Súbor_COUNT || 이름길이[INDEX] == 0) return 0;
        for (int Loop_INDEX = 0; Loop_INDEX < 이름길이[INDEX]; Loop_INDEX++) if (Názov[INDEX * 64 + Loop_INDEX] == '/') return 0;
        return 이름길이[INDEX];
    }
    public static int 공개이름바이트(int INDEX, int pozičný_index) {
        return INDEX >= 0 && INDEX < Súbor_COUNT && pozičný_index >= 0 && pozičný_index < 이름길이[INDEX] ? Názov[INDEX * 64 + pozičný_index] : -22;
    }
    public static int 공개파일크기(int INDEX) { return INDEX >= 0 && INDEX < Súbor_COUNT ? dĺžka_VALUE[INDEX] : -22; }
    static int[] 정규 = new int[64], v_termíne_splatnosti_položka = new int[64], Adresár_názov = new int[16 * 64], Adresár_dĺžka = new int[16];
    static int 정규길이, v_termíne_splatnosti_dĺžka;
    static boolean 접두(int[] 이름들, int Spustiť_2, int cesta_VALUE, int[] predný_VALUE, int Riadkovanie_cesta) {
        if (cesta_VALUE < Riadkovanie_cesta) return false;
        for (int Loop_INDEX = 0; Loop_INDEX < Riadkovanie_cesta; Loop_INDEX++) if (이름들[Spustiť_2 + Loop_INDEX] != predný_VALUE[Loop_INDEX]) return false;
        return true;
    }
    static int normalizovať_VALUE() {
        if (cesta_dĺžka == 0) return -22;
        정규길이 = Cesta[0] == '/' ? 0 : v_termíne_splatnosti_dĺžka;
        for (int Loop_INDEX = 0; Loop_INDEX < 정규길이; Loop_INDEX++) 정규[Loop_INDEX] = v_termíne_splatnosti_položka[Loop_INDEX];
        int 읽는자리 = 0;
        while (읽는자리 < cesta_dĺžka) {
            while (읽는자리 < cesta_dĺžka && Cesta[읽는자리] == '/') 읽는자리++;
            int START_pozícia = 읽는자리; while (읽는자리 < cesta_dĺžka && Cesta[읽는자리] != '/') { if (Cesta[읽는자리] == 0) return -22; 읽는자리++; }
            int položka_COUNT_8f7753a1 = 읽는자리 - START_pozícia; if (položka_COUNT_8f7753a1 == 0 || položka_COUNT_8f7753a1 == 1 && Cesta[START_pozícia] == '.') continue;
            if (položka_COUNT_8f7753a1 == 2 && Cesta[START_pozícia] == '.' && Cesta[START_pozícia + 1] == '.') {
                while (정규길이 > 0 && 정규[정규길이 - 1] != '/') 정규길이--;
                if (정규길이 > 0) 정규길이--;
                continue;
            }
            if (정규길이 + položka_COUNT_8f7753a1 + (정규길이 == 0 ? 0 : 1) > 63) return -36;
            if (정규길이 > 0) 정규[정규길이++] = '/';
            for (int Loop_INDEX = START_pozícia; Loop_INDEX < 읽는자리; Loop_INDEX++) 정규[정규길이++] = Cesta[Loop_INDEX];
        }
        return 0;
    }
    static int FIND_Adresár(int položka_COUNT_8f7753a1) {
        if (položka_COUNT_8f7753a1 == 0) return 0;
        for (int Loop_INDEX = 1; Loop_INDEX < 16; Loop_INDEX++) if (Adresár_dĺžka[Loop_INDEX] == položka_COUNT_8f7753a1 && 접두(Adresár_názov, Loop_INDEX * 64, položka_COUNT_8f7753a1, 정규, položka_COUNT_8f7753a1)) return Loop_INDEX;
        return -1;
    }
    static int skontrolovať_nadradený() {
        int položka_COUNT_8f7753a1 = 정규길이; while (položka_COUNT_8f7753a1 > 0 && 정규[položka_COUNT_8f7753a1 - 1] != '/') položka_COUNT_8f7753a1--;
        return FIND_Adresár(položka_COUNT_8f7753a1 == 0 ? 0 : položka_COUNT_8f7753a1 - 1) < 0 ? -2 : 0;
    }
    public static int Create_Adresár() {
        int 처리값 = normalizovať_VALUE(); if (처리값 < 0) return 처리값;
        if (FIND_Adresár(정규길이) >= 0 || FIND_položka() >= 0) return -17;
        처리값 = skontrolovať_nadradený(); if (처리값 < 0) return 처리값;
        for (int Loop_INDEX = 1; Loop_INDEX < 16; Loop_INDEX++) if (Adresár_dĺžka[Loop_INDEX] == 0) {
            Adresár_dĺžka[Loop_INDEX] = 정규길이; for (int vnútorné_pozícia = 0; vnútorné_pozícia < 정규길이; vnútorné_pozícia++) Adresár_názov[Loop_INDEX * 64 + vnútorné_pozícia] = 정규[vnútorné_pozícia]; return 0;
        }
        return -28;
    }
    public static int 항목종류() {
        int 처리값 = normalizovať_VALUE(); if (처리값 < 0) return 처리값;
        if (FIND_Adresár(정규길이) >= 0) return 2;
        return FIND_položka() >= 0 ? 1 : 0;
    }
    public static int zmeniť_Adresár() {
        int 처리값 = normalizovať_VALUE(); if (처리값 < 0) return 처리값;
        if (FIND_Adresár(정규길이) < 0) return -2;
        v_termíne_splatnosti_dĺžka = 정규길이; for (int Loop_INDEX = 0; Loop_INDEX < v_termíne_splatnosti_dĺžka; Loop_INDEX++) v_termíne_splatnosti_položka[Loop_INDEX] = 정규[Loop_INDEX]; return 0;
    }
    public static int odobrať_Adresár() {
        int 처리값 = normalizovať_VALUE(); if (처리값 < 0) return 처리값;
        int 폴더번호 = FIND_Adresár(정규길이); if (폴더번호 < 0) return -2; if (폴더번호 == 0) return -16;
        if (v_termíne_splatnosti_dĺžka == 정규길이 && 접두(v_termíne_splatnosti_položka, 0, v_termíne_splatnosti_dĺžka, 정규, 정규길이)) return -16;
        for (int Loop_INDEX = 0; Loop_INDEX < Súbor_COUNT; Loop_INDEX++) {
            if (이름길이[Loop_INDEX] > 정규길이 && 접두(Názov, Loop_INDEX * 64, 이름길이[Loop_INDEX], 정규, 정규길이) && Názov[Loop_INDEX * 64 + 정규길이] == '/') return -39;
        }
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) {
            if (Adresár_dĺžka[Loop_INDEX] > 정규길이 && 접두(Adresár_názov, Loop_INDEX * 64, Adresár_dĺžka[Loop_INDEX], 정규, 정규길이) && Adresár_názov[Loop_INDEX * 64 + 정규길이] == '/') return -39;
        }
        Adresár_dĺžka[폴더번호] = 0; return 0;
    }
    public static int Premenovať_položka(int 원본번호) {
        if (원본번호 < 0 || 원본번호 >= Súbor_COUNT || 이름길이[원본번호] == 0) return -2;
        int 처리값 = normalizovať_VALUE(); if (처리값 < 0) return 처리값;
        if (FIND_Adresár(정규길이) >= 0) return -21;
        처리값 = skontrolovať_nadradený(); if (처리값 < 0) return 처리값;
        int 이전값 = FIND_položka(); if (이전값 == 원본번호) return 0;
        if (이전값 >= 0) 이름길이[이전값] = 0;
        이름길이[원본번호] = 정규길이; for (int Loop_INDEX = 0; Loop_INDEX < 정규길이; Loop_INDEX++) Názov[원본번호 * 64 + Loop_INDEX] = 정규[Loop_INDEX]; return 0;
    }
    static int položka_START(int[] údaje_pole, int 시작점, int položka_COUNT_8f7753a1) {
        if (!접두(údaje_pole, 시작점, položka_COUNT_8f7753a1, 정규, 정규길이)) return -1;
        int START_pozícia = 정규길이;
        if (START_pozícia > 0) { if (položka_COUNT_8f7753a1 <= START_pozícia || údaje_pole[시작점 + START_pozícia] != '/') return -1; START_pozícia++; }
        if (položka_COUNT_8f7753a1 <= START_pozícia) return -1;
        for (int Loop_INDEX = START_pozícia; Loop_INDEX < položka_COUNT_8f7753a1; Loop_INDEX++) if (údaje_pole[시작점 + Loop_INDEX] == '/') return -1;
        return START_pozícia;
    }
    static void v_termíne_splatnosti_zapísať() { 단말.문자('/'); for (int Loop_INDEX = 0; Loop_INDEX < v_termíne_splatnosti_dĺžka; Loop_INDEX++) Panel.직렬쓰기(v_termíne_splatnosti_položka[Loop_INDEX]); }
    static int 경로목록() {
        int 처리값 = normalizovať_VALUE(); if (처리값 < 0) return 처리값;
        int Súbor_cieľová_hodnota = FIND_položka();
        if (Súbor_cieľová_hodnota >= 0) { for (int Loop_INDEX = 0; Loop_INDEX < 정규길이; Loop_INDEX++) Panel.직렬쓰기(정규[Loop_INDEX]); 단말.Zápis("  "); 단말.수(dĺžka_VALUE[Súbor_cieľová_hodnota]); 단말.Zápis("Byte_VALUE(주기억 Súbor)\n"); return 0; }
        if (FIND_Adresár(정규길이) < 0) return -2;
        for (int 뒷값 = 1; 뒷값 < 16; 뒷값++) if (Adresár_dĺžka[뒷값] > 0) {
            int START_pozícia = položka_START(Adresár_názov, 뒷값 * 64, Adresár_dĺžka[뒷값]); if (START_pozícia < 0) continue;
            for (int Loop_INDEX = START_pozícia; Loop_INDEX < Adresár_dĺžka[뒷값]; Loop_INDEX++) Panel.직렬쓰기(Adresár_názov[뒷값 * 64 + Loop_INDEX]); 단말.Zápis("/\n");
        }
        for (int Súbor_INDEX = 0; Súbor_INDEX < Súbor_COUNT; Súbor_INDEX++) if (이름길이[Súbor_INDEX] > 0) {
            int START_pozícia = položka_START(Názov, Súbor_INDEX * 64, 이름길이[Súbor_INDEX]); if (START_pozícia < 0) continue;
            for (int Loop_INDEX = START_pozícia; Loop_INDEX < 이름길이[Súbor_INDEX]; Loop_INDEX++) Panel.직렬쓰기(Názov[Súbor_INDEX * 64 + Loop_INDEX]);
            단말.Zápis("  "); 단말.수(dĺžka_VALUE[Súbor_INDEX]); 단말.Zápis("Byte_VALUE(주기억 Súbor)\n");
        }
        return 0;
    }
}
