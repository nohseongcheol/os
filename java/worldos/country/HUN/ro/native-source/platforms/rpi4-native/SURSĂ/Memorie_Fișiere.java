// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** RAM Fișier 64개, 파일당 16384바이트, 서술자 16개. 모든 date/정책은 Java에 있다.
 * 호출 도중 양보하지 않으므로 현재의 단일 코어 협력식 작업 사이에서 원자적이다.
 * 디스크 저장이나 POSIX 전체 구현을 뜻하지 않는다. 음수 반환은 eroare 번호다.
 */
public final class Memorie_Fișiere {
    static final int Fișier_COUNT = 64;
    static int[] Nume = new int[Fișier_COUNT * 64];
    static int[] 이름길이 = new int[Fișier_COUNT];
    // Pack four bytes in each Java int, preserving the old content heap budget.
    static int[] Conținut_VALUE = new int[Fișier_COUNT * 4096];
    static int[] lungime_VALUE = new int[Fișier_COUNT];
    static int[] referință_COUNT = new int[Fișier_COUNT];
    static int[] utiliza_VALUE = new int[16];
    static int[] țintă = new int[16];
    static int[] Poziție = new int[16];
    static int[] metodă_mod = new int[16];
    static int[] Cale = new int[64];
    static int cale_lungime;

    public static int 파일한도() { return Fișier_COUNT; }
    static int 자료읽기(int Fișier, int index_de_poziție) { return (Conținut_VALUE[Fișier * 4096 + index_de_poziție / 4] >>> ((index_de_poziție & 3) * 8)) & 255; }
    static void scriere_date(int Fișier, int index_de_poziție, int VALUE) {
        int 칸 = Fișier * 4096 + index_de_poziție / 4, muta_VALUE_83b651b8 = (index_de_poziție & 3) * 8;
        Conținut_VALUE[칸] = (Conținut_VALUE[칸] & ~(255 << muta_VALUE_83b651b8)) | ((VALUE & 255) << muta_VALUE_83b651b8);
    }

    public static int cale_buta(int Mărime) {
        cale_lungime = 0;
        if (Mărime < 1 || Mărime > 63) return -36;
        cale_lungime = Mărime;
        for (int Loop_INDEX = 0; Loop_INDEX < Mărime; Loop_INDEX++) Cale[Loop_INDEX] = 0;
        return 0;
    }
    public static int cale_byte(int INDEX, int VALUE) {
        if (INDEX < 0 || INDEX >= cale_lungime || VALUE < 1 || VALUE > 255) return -22;
        Cale[INDEX] = VALUE; return 0;
    }
    static int FIND_intrare() {
        for (int Fișier_INDEX = 0; Fișier_INDEX < Fișier_COUNT; Fișier_INDEX++) if (이름길이[Fișier_INDEX] > 0 && 이름길이[Fișier_INDEX] == Canonical_lungime && 접두(Nume, Fișier_INDEX * 64, 이름길이[Fișier_INDEX], Canonical_VALUE, Canonical_lungime)) return Fișier_INDEX;
        return -1;
    }
    public static int Deschide(int 플래그) {
        if (cale_lungime == 0 || (플래그 & ~0x6c3) != 0 || (플래그 & 3) == 3) return -22;
        for (int Loop_INDEX = 0; Loop_INDEX < cale_lungime; Loop_INDEX++) if (Cale[Loop_INDEX] == 0) return -22;
        if ((플래그 & 0x200) != 0 && (플래그 & 3) == 0) return -22;
        int KR = normaliza_VALUE(); if (KR < 0) return KR;
        if (FIND_Director(Canonical_lungime) >= 0) return -21;
        KR = verifica_părinte(); if (KR < 0) return KR;
        int Fișier = FIND_intrare();
        if (Fișier >= 0 && (플래그 & 0xc0) == 0xc0) return -17;
        if (Fișier < 0 && (플래그 & 0x40) == 0) return -2;
        int 서술자 = -1;
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (utiliza_VALUE[Loop_INDEX] == 0) { 서술자 = Loop_INDEX; break; }
        if (서술자 < 0) return -24;
        if (Fișier < 0) {
            for (int Loop_INDEX = 0; Loop_INDEX < Fișier_COUNT; Loop_INDEX++) if (이름길이[Loop_INDEX] == 0 && referință_COUNT[Loop_INDEX] == 0) { Fișier = Loop_INDEX; break; }
            if (Fișier < 0) return -28;
            이름길이[Fișier] = Canonical_lungime;
            for (int Loop_INDEX = 0; Loop_INDEX < Canonical_lungime; Loop_INDEX++) Nume[Fișier * 64 + Loop_INDEX] = Canonical_VALUE[Loop_INDEX];
            lungime_VALUE[Fișier] = 0;
        }
        if ((플래그 & 0x200) != 0) lungime_VALUE[Fișier] = 0;
        utiliza_VALUE[서술자] = 1; țintă[서술자] = Fișier; Poziție[서술자] = 0; metodă_mod[서술자] = 플래그;
        referință_COUNT[Fișier]++;
        return 서술자 + 3;
    }
    static int verifica(int 서술자) {
        return 서술자 >= 3 && 서술자 < 19 && utiliza_VALUE[서술자 - 3] != 0 ? 서술자 - 3 : -1;
    }
    public static int Citire(int 서술자) {
        int 칸 = verifica(서술자);
        if (칸 < 0 || (metodă_mod[칸] & 3) == 1) return -9;
        int Fișier = țintă[칸];
        if (Poziție[칸] >= lungime_VALUE[Fișier]) return 256; // EOF와 real_date 0x00..0xff 구별
        return 자료읽기(Fișier, Poziție[칸]++);
    }
    public static int Scriere(int 서술자, int VALUE) {
        int 칸 = verifica(서술자);
        if (칸 < 0 || (metodă_mod[칸] & 3) == 0) return -9;
        int Fișier = țintă[칸];
        if ((metodă_mod[칸] & 0x400) != 0) Poziție[칸] = lungime_VALUE[Fișier];
        if (Poziție[칸] >= 16384) return -28;
        while (lungime_VALUE[Fișier] < Poziție[칸]) scriere_date(Fișier, lungime_VALUE[Fișier]++, 0);
        scriere_date(Fișier, Poziție[칸]++, VALUE);
        if (lungime_VALUE[Fișier] < Poziție[칸]) lungime_VALUE[Fișier] = Poziție[칸];
        return 1;
    }
    public static int căuta_poziție(int 서술자, int 거리, int Project_rădăcină) {
        int 칸 = verifica(서술자);
        if (칸 < 0) return -9;
        if (Project_rădăcină < 0 || Project_rădăcină > 2 || 거리 < -16384 || 거리 > 16384) return -22;
        int 새위치 = 거리 + (Project_rădăcină == 0 ? 0 : Project_rădăcină == 1 ? Poziție[칸] : lungime_VALUE[țintă[칸]]);
        if (새위치 < 0 || 새위치 > 16384) return -22;
        Poziție[칸] = 새위치; return 새위치;
    }
    public static int Închide(int 서술자) {
        int 칸 = verifica(서술자);
        if (칸 < 0) return -9;
        referință_COUNT[țintă[칸]]--; utiliza_VALUE[칸] = 0; return 0;
    }
    public static int Mărime(int 서술자) {
        int 칸 = verifica(서술자); return 칸 < 0 ? -9 : lungime_VALUE[țintă[칸]];
    }
    public static int set_lungime(int 서술자, int Mărime) {
        int 칸 = verifica(서술자);
        if (칸 < 0 || (metodă_mod[칸] & 3) == 0) return -9;
        if (Mărime < 0 || Mărime > 16384) return -22;
        int Fișier = țintă[칸];
        while (lungime_VALUE[Fișier] < Mărime) scriere_date(Fișier, lungime_VALUE[Fișier]++, 0);
        lungime_VALUE[Fișier] = Mărime; return 0;
    }
    public static int șterge_intrare() {
        if (cale_lungime == 0) return -22;
        int KR = normaliza_VALUE(); if (KR < 0) return KR;
        if (FIND_Director(Canonical_lungime) >= 0) return -21;
        KR = verifica_părinte(); if (KR < 0) return KR;
        int Fișier = FIND_intrare();
        if (Fișier < 0) return -2;
        이름길이[Fișier] = 0; return 0; // 열려 있는 파일은 마지막 close까지 유지
    }
    static void intrare_Listă() {
        cale_buta(1); cale_byte(0, '.'); 경로목록();
    }
    public static int 공개이름길이(int INDEX) {
        if (INDEX < 0 || INDEX >= Fișier_COUNT || 이름길이[INDEX] == 0) return 0;
        for (int Loop_INDEX = 0; Loop_INDEX < 이름길이[INDEX]; Loop_INDEX++) if (Nume[INDEX * 64 + Loop_INDEX] == '/') return 0;
        return 이름길이[INDEX];
    }
    public static int 공개이름바이트(int INDEX, int index_de_poziție) {
        return INDEX >= 0 && INDEX < Fișier_COUNT && index_de_poziție >= 0 && index_de_poziție < 이름길이[INDEX] ? Nume[INDEX * 64 + index_de_poziție] : -22;
    }
    public static int 공개파일크기(int INDEX) { return INDEX >= 0 && INDEX < Fișier_COUNT ? lungime_VALUE[INDEX] : -22; }
    static int[] Canonical_VALUE = new int[64], curent_element = new int[64], Director_nume = new int[16 * 64], Director_lungime = new int[16];
    static int Canonical_lungime, curent_lungime;
    static boolean 접두(int[] 이름들, int Pornește, int cale_VALUE, int[] frontală_VALUE, int spațiere_cale) {
        if (cale_VALUE < spațiere_cale) return false;
        for (int Loop_INDEX = 0; Loop_INDEX < spațiere_cale; Loop_INDEX++) if (이름들[Pornește + Loop_INDEX] != frontală_VALUE[Loop_INDEX]) return false;
        return true;
    }
    static int normaliza_VALUE() {
        if (cale_lungime == 0) return -22;
        Canonical_lungime = Cale[0] == '/' ? 0 : curent_lungime;
        for (int Loop_INDEX = 0; Loop_INDEX < Canonical_lungime; Loop_INDEX++) Canonical_VALUE[Loop_INDEX] = curent_element[Loop_INDEX];
        int 읽는자리 = 0;
        while (읽는자리 < cale_lungime) {
            while (읽는자리 < cale_lungime && Cale[읽는자리] == '/') 읽는자리++;
            int buta_poziție = 읽는자리; while (읽는자리 < cale_lungime && Cale[읽는자리] != '/') { if (Cale[읽는자리] == 0) return -22; 읽는자리++; }
            int intrare_COUNT = 읽는자리 - buta_poziție; if (intrare_COUNT == 0 || intrare_COUNT == 1 && Cale[buta_poziție] == '.') continue;
            if (intrare_COUNT == 2 && Cale[buta_poziție] == '.' && Cale[buta_poziție + 1] == '.') {
                while (Canonical_lungime > 0 && Canonical_VALUE[Canonical_lungime - 1] != '/') Canonical_lungime--;
                if (Canonical_lungime > 0) Canonical_lungime--;
                continue;
            }
            if (Canonical_lungime + intrare_COUNT + (Canonical_lungime == 0 ? 0 : 1) > 63) return -36;
            if (Canonical_lungime > 0) Canonical_VALUE[Canonical_lungime++] = '/';
            for (int Loop_INDEX = buta_poziție; Loop_INDEX < 읽는자리; Loop_INDEX++) Canonical_VALUE[Canonical_lungime++] = Cale[Loop_INDEX];
        }
        return 0;
    }
    static int FIND_Director(int intrare_COUNT) {
        if (intrare_COUNT == 0) return 0;
        for (int Loop_INDEX = 1; Loop_INDEX < 16; Loop_INDEX++) if (Director_lungime[Loop_INDEX] == intrare_COUNT && 접두(Director_nume, Loop_INDEX * 64, intrare_COUNT, Canonical_VALUE, intrare_COUNT)) return Loop_INDEX;
        return -1;
    }
    static int verifica_părinte() {
        int intrare_COUNT = Canonical_lungime; while (intrare_COUNT > 0 && Canonical_VALUE[intrare_COUNT - 1] != '/') intrare_COUNT--;
        return FIND_Director(intrare_COUNT == 0 ? 0 : intrare_COUNT - 1) < 0 ? -2 : 0;
    }
    public static int crea_Director() {
        int 처리값 = normaliza_VALUE(); if (처리값 < 0) return 처리값;
        if (FIND_Director(Canonical_lungime) >= 0 || FIND_intrare() >= 0) return -17;
        처리값 = verifica_părinte(); if (처리값 < 0) return 처리값;
        for (int Loop_INDEX = 1; Loop_INDEX < 16; Loop_INDEX++) if (Director_lungime[Loop_INDEX] == 0) {
            Director_lungime[Loop_INDEX] = Canonical_lungime; for (int internă_poziție = 0; internă_poziție < Canonical_lungime; internă_poziție++) Director_nume[Loop_INDEX * 64 + internă_poziție] = Canonical_VALUE[internă_poziție]; return 0;
        }
        return -28;
    }
    public static int 항목종류() {
        int 처리값 = normaliza_VALUE(); if (처리값 < 0) return 처리값;
        if (FIND_Director(Canonical_lungime) >= 0) return 2;
        return FIND_intrare() >= 0 ? 1 : 0;
    }
    public static int schimba_Director() {
        int 처리값 = normaliza_VALUE(); if (처리값 < 0) return 처리값;
        if (FIND_Director(Canonical_lungime) < 0) return -2;
        curent_lungime = Canonical_lungime; for (int Loop_INDEX = 0; Loop_INDEX < curent_lungime; Loop_INDEX++) curent_element[Loop_INDEX] = Canonical_VALUE[Loop_INDEX]; return 0;
    }
    public static int elimina_Director() {
        int 처리값 = normaliza_VALUE(); if (처리값 < 0) return 처리값;
        int 폴더번호 = FIND_Director(Canonical_lungime); if (폴더번호 < 0) return -2; if (폴더번호 == 0) return -16;
        if (curent_lungime == Canonical_lungime && 접두(curent_element, 0, curent_lungime, Canonical_VALUE, Canonical_lungime)) return -16;
        for (int Loop_INDEX = 0; Loop_INDEX < Fișier_COUNT; Loop_INDEX++) {
            if (이름길이[Loop_INDEX] > Canonical_lungime && 접두(Nume, Loop_INDEX * 64, 이름길이[Loop_INDEX], Canonical_VALUE, Canonical_lungime) && Nume[Loop_INDEX * 64 + Canonical_lungime] == '/') return -39;
        }
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) {
            if (Director_lungime[Loop_INDEX] > Canonical_lungime && 접두(Director_nume, Loop_INDEX * 64, Director_lungime[Loop_INDEX], Canonical_VALUE, Canonical_lungime) && Director_nume[Loop_INDEX * 64 + Canonical_lungime] == '/') return -39;
        }
        Director_lungime[폴더번호] = 0; return 0;
    }
    public static int Redenumire_intrare(int 원본번호) {
        if (원본번호 < 0 || 원본번호 >= Fișier_COUNT || 이름길이[원본번호] == 0) return -2;
        int 처리값 = normaliza_VALUE(); if (처리값 < 0) return 처리값;
        if (FIND_Director(Canonical_lungime) >= 0) return -21;
        처리값 = verifica_părinte(); if (처리값 < 0) return 처리값;
        int Anteriorul_VALUE = FIND_intrare(); if (Anteriorul_VALUE == 원본번호) return 0;
        if (Anteriorul_VALUE >= 0) 이름길이[Anteriorul_VALUE] = 0;
        이름길이[원본번호] = Canonical_lungime; for (int Loop_INDEX = 0; Loop_INDEX < Canonical_lungime; Loop_INDEX++) Nume[원본번호 * 64 + Loop_INDEX] = Canonical_VALUE[Loop_INDEX]; return 0;
    }
    static int intrare_buta(int[] date_ARRAY, int 시작점, int intrare_COUNT) {
        if (!접두(date_ARRAY, 시작점, intrare_COUNT, Canonical_VALUE, Canonical_lungime)) return -1;
        int buta_poziție = Canonical_lungime;
        if (buta_poziție > 0) { if (intrare_COUNT <= buta_poziție || date_ARRAY[시작점 + buta_poziție] != '/') return -1; buta_poziție++; }
        if (intrare_COUNT <= buta_poziție) return -1;
        for (int Loop_INDEX = buta_poziție; Loop_INDEX < intrare_COUNT; Loop_INDEX++) if (date_ARRAY[시작점 + Loop_INDEX] == '/') return -1;
        return buta_poziție;
    }
    static void curent_scriere() { 단말.문자('/'); for (int Loop_INDEX = 0; Loop_INDEX < curent_lungime; Loop_INDEX++) Avizier.직렬쓰기(curent_element[Loop_INDEX]); }
    static int 경로목록() {
        int 처리값 = normaliza_VALUE(); if (처리값 < 0) return 처리값;
        int Fișier_țintă = FIND_intrare();
        if (Fișier_țintă >= 0) { for (int Loop_INDEX = 0; Loop_INDEX < Canonical_lungime; Loop_INDEX++) Avizier.직렬쓰기(Canonical_VALUE[Loop_INDEX]); 단말.Scriere("  "); 단말.수(lungime_VALUE[Fișier_țintă]); 단말.Scriere("byte_VALUE(주기억 Fișier)\n"); return 0; }
        if (FIND_Director(Canonical_lungime) < 0) return -2;
        for (int 뒷값 = 1; 뒷값 < 16; 뒷값++) if (Director_lungime[뒷값] > 0) {
            int buta_poziție = intrare_buta(Director_nume, 뒷값 * 64, Director_lungime[뒷값]); if (buta_poziție < 0) continue;
            for (int Loop_INDEX = buta_poziție; Loop_INDEX < Director_lungime[뒷값]; Loop_INDEX++) Avizier.직렬쓰기(Director_nume[뒷값 * 64 + Loop_INDEX]); 단말.Scriere("/\n");
        }
        for (int Fișier_INDEX = 0; Fișier_INDEX < Fișier_COUNT; Fișier_INDEX++) if (이름길이[Fișier_INDEX] > 0) {
            int buta_poziție = intrare_buta(Nume, Fișier_INDEX * 64, 이름길이[Fișier_INDEX]); if (buta_poziție < 0) continue;
            for (int Loop_INDEX = buta_poziție; Loop_INDEX < 이름길이[Fișier_INDEX]; Loop_INDEX++) Avizier.직렬쓰기(Nume[Fișier_INDEX * 64 + Loop_INDEX]);
            단말.Scriere("  "); 단말.수(lungime_VALUE[Fișier_INDEX]); 단말.Scriere("byte_VALUE(주기억 Fișier)\n");
        }
        return 0;
    }
}
