// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** RAM Fail 64개, 파일당 16384바이트, 서술자 16개. 모든 andmed/정책은 Java에 있다.
 * 호출 도중 양보하지 않으므로 현재의 단일 코어 협력식 작업 사이에서 원자적이다.
 * 디스크 저장이나 POSIX 전체 구현을 뜻하지 않는다. 음수 반환은 VIGA 번호다.
 */
public final class Mälu_Failid {
    static final int Fail_COUNT = 64;
    static int[] Nimi_2 = new int[Fail_COUNT * 64];
    static int[] 이름길이 = new int[Fail_COUNT];
    // Pack four bytes in each Java int, preserving the old content heap budget.
    static int[] Sisu_VALUE = new int[Fail_COUNT * 4096];
    static int[] 길이 = new int[Fail_COUNT];
    static int[] viide_COUNT = new int[Fail_COUNT];
    static int[] kasutus_VALUE = new int[16];
    static int[] siht = new int[16];
    static int[] Asukoht = new int[16];
    static int[] meetod_MODE = new int[16];
    static int[] RADA = new int[64];
    static int 경로길이;

    public static int 파일한도() { return Fail_COUNT; }
    static int 자료읽기(int Fail, int asukohaindeks) { return (Sisu_VALUE[Fail * 4096 + asukohaindeks / 4] >>> ((asukohaindeks & 3) * 8)) & 255; }
    static void kirjutamine_andmed(int Fail, int asukohaindeks, int VALUE) {
        int 칸 = Fail * 4096 + asukohaindeks / 4, liigutama_VALUE = (asukohaindeks & 3) * 8;
        Sisu_VALUE[칸] = (Sisu_VALUE[칸] & ~(255 << liigutama_VALUE)) | ((VALUE & 255) << liigutama_VALUE);
    }

    public static int tee_START(int Suurus) {
        경로길이 = 0;
        if (Suurus < 1 || Suurus > 63) return -36;
        경로길이 = Suurus;
        for (int Loop_INDEX = 0; Loop_INDEX < Suurus; Loop_INDEX++) RADA[Loop_INDEX] = 0;
        return 0;
    }
    public static int tee_bait(int INDEX, int VALUE) {
        if (INDEX < 0 || INDEX >= 경로길이 || VALUE < 1 || VALUE > 255) return -22;
        RADA[INDEX] = VALUE; return 0;
    }
    static int FIND_kirje() {
        for (int Fail_INDEX = 0; Fail_INDEX < Fail_COUNT; Fail_INDEX++) if (이름길이[Fail_INDEX] > 0 && 이름길이[Fail_INDEX] == 정규길이 && 접두(Nimi_2, Fail_INDEX * 64, 이름길이[Fail_INDEX], 정규, 정규길이)) return Fail_INDEX;
        return -1;
    }
    public static int Ava(int 플래그) {
        if (경로길이 == 0 || (플래그 & ~0x6c3) != 0 || (플래그 & 3) == 3) return -22;
        for (int Loop_INDEX = 0; Loop_INDEX < 경로길이; Loop_INDEX++) if (RADA[Loop_INDEX] == 0) return -22;
        if ((플래그 & 0x200) != 0 && (플래그 & 3) == 0) return -22;
        int TULEMUS = normaliseerima_VALUE(); if (TULEMUS < 0) return TULEMUS;
        if (FIND_kaust(정규길이) >= 0) return -21;
        TULEMUS = tšekk_ema(); if (TULEMUS < 0) return TULEMUS;
        int Fail = FIND_kirje();
        if (Fail >= 0 && (플래그 & 0xc0) == 0xc0) return -17;
        if (Fail < 0 && (플래그 & 0x40) == 0) return -2;
        int 서술자 = -1;
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (kasutus_VALUE[Loop_INDEX] == 0) { 서술자 = Loop_INDEX; break; }
        if (서술자 < 0) return -24;
        if (Fail < 0) {
            for (int Loop_INDEX = 0; Loop_INDEX < Fail_COUNT; Loop_INDEX++) if (이름길이[Loop_INDEX] == 0 && viide_COUNT[Loop_INDEX] == 0) { Fail = Loop_INDEX; break; }
            if (Fail < 0) return -28;
            이름길이[Fail] = 정규길이;
            for (int Loop_INDEX = 0; Loop_INDEX < 정규길이; Loop_INDEX++) Nimi_2[Fail * 64 + Loop_INDEX] = 정규[Loop_INDEX];
            길이[Fail] = 0;
        }
        if ((플래그 & 0x200) != 0) 길이[Fail] = 0;
        kasutus_VALUE[서술자] = 1; siht[서술자] = Fail; Asukoht[서술자] = 0; meetod_MODE[서술자] = 플래그;
        viide_COUNT[Fail]++;
        return 서술자 + 3;
    }
    static int kinnitama(int 서술자) {
        return 서술자 >= 3 && 서술자 < 19 && kasutus_VALUE[서술자 - 3] != 0 ? 서술자 - 3 : -1;
    }
    public static int Lugemine(int 서술자) {
        int 칸 = kinnitama(서술자);
        if (칸 < 0 || (meetod_MODE[칸] & 3) == 1) return -9;
        int Fail = siht[칸];
        if (Asukoht[칸] >= 길이[Fail]) return 256; // EOF와 tegelik_andmed 0x00..0xff 구별
        return 자료읽기(Fail, Asukoht[칸]++);
    }
    public static int Kirjutamine(int 서술자, int VALUE) {
        int 칸 = kinnitama(서술자);
        if (칸 < 0 || (meetod_MODE[칸] & 3) == 0) return -9;
        int Fail = siht[칸];
        if ((meetod_MODE[칸] & 0x400) != 0) Asukoht[칸] = 길이[Fail];
        if (Asukoht[칸] >= 16384) return -28;
        while (길이[Fail] < Asukoht[칸]) kirjutamine_andmed(Fail, 길이[Fail]++, 0);
        kirjutamine_andmed(Fail, Asukoht[칸]++, VALUE);
        if (길이[Fail] < Asukoht[칸]) 길이[Fail] = Asukoht[칸];
        return 1;
    }
    public static int otsima_ametikoht(int 서술자, int 거리, int Project_juur) {
        int 칸 = kinnitama(서술자);
        if (칸 < 0) return -9;
        if (Project_juur < 0 || Project_juur > 2 || 거리 < -16384 || 거리 > 16384) return -22;
        int 새위치 = 거리 + (Project_juur == 0 ? 0 : Project_juur == 1 ? Asukoht[칸] : 길이[siht[칸]]);
        if (새위치 < 0 || 새위치 > 16384) return -22;
        Asukoht[칸] = 새위치; return 새위치;
    }
    public static int Suletud(int 서술자) {
        int 칸 = kinnitama(서술자);
        if (칸 < 0) return -9;
        viide_COUNT[siht[칸]]--; kasutus_VALUE[칸] = 0; return 0;
    }
    public static int Suurus(int 서술자) {
        int 칸 = kinnitama(서술자); return 칸 < 0 ? -9 : 길이[siht[칸]];
    }
    public static int 길이정하기(int 서술자, int Suurus) {
        int 칸 = kinnitama(서술자);
        if (칸 < 0 || (meetod_MODE[칸] & 3) == 0) return -9;
        if (Suurus < 0 || Suurus > 16384) return -22;
        int Fail = siht[칸];
        while (길이[Fail] < Suurus) kirjutamine_andmed(Fail, 길이[Fail]++, 0);
        길이[Fail] = Suurus; return 0;
    }
    public static int kustutama_kirje() {
        if (경로길이 == 0) return -22;
        int TULEMUS = normaliseerima_VALUE(); if (TULEMUS < 0) return TULEMUS;
        if (FIND_kaust(정규길이) >= 0) return -21;
        TULEMUS = tšekk_ema(); if (TULEMUS < 0) return TULEMUS;
        int Fail = FIND_kirje();
        if (Fail < 0) return -2;
        이름길이[Fail] = 0; return 0; // 열려 있는 파일은 마지막 close까지 유지
    }
    static void kirje_Loend() {
        tee_START(1); tee_bait(0, '.'); 경로목록();
    }
    public static int 공개이름길이(int INDEX) {
        if (INDEX < 0 || INDEX >= Fail_COUNT || 이름길이[INDEX] == 0) return 0;
        for (int Loop_INDEX = 0; Loop_INDEX < 이름길이[INDEX]; Loop_INDEX++) if (Nimi_2[INDEX * 64 + Loop_INDEX] == '/') return 0;
        return 이름길이[INDEX];
    }
    public static int 공개이름바이트(int INDEX, int asukohaindeks) {
        return INDEX >= 0 && INDEX < Fail_COUNT && asukohaindeks >= 0 && asukohaindeks < 이름길이[INDEX] ? Nimi_2[INDEX * 64 + asukohaindeks] : -22;
    }
    public static int 공개파일크기(int INDEX) { return INDEX >= 0 && INDEX < Fail_COUNT ? 길이[INDEX] : -22; }
    static int[] 정규 = new int[64], tähtaja_piires_kaup = new int[64], kaust_nimetus = new int[16 * 64], 폴더길이 = new int[16];
    static int 정규길이, 현재길이;
    static boolean 접두(int[] 이름들, int Käivita_2, int tee_VALUE, int[] esikaamera_VALUE, int reasamm_tee) {
        if (tee_VALUE < reasamm_tee) return false;
        for (int Loop_INDEX = 0; Loop_INDEX < reasamm_tee; Loop_INDEX++) if (이름들[Käivita_2 + Loop_INDEX] != esikaamera_VALUE[Loop_INDEX]) return false;
        return true;
    }
    static int normaliseerima_VALUE() {
        if (경로길이 == 0) return -22;
        정규길이 = RADA[0] == '/' ? 0 : 현재길이;
        for (int Loop_INDEX = 0; Loop_INDEX < 정규길이; Loop_INDEX++) 정규[Loop_INDEX] = tähtaja_piires_kaup[Loop_INDEX];
        int 읽는자리 = 0;
        while (읽는자리 < 경로길이) {
            while (읽는자리 < 경로길이 && RADA[읽는자리] == '/') 읽는자리++;
            int START_ametikoht = 읽는자리; while (읽는자리 < 경로길이 && RADA[읽는자리] != '/') { if (RADA[읽는자리] == 0) return -22; 읽는자리++; }
            int kirje_COUNT = 읽는자리 - START_ametikoht; if (kirje_COUNT == 0 || kirje_COUNT == 1 && RADA[START_ametikoht] == '.') continue;
            if (kirje_COUNT == 2 && RADA[START_ametikoht] == '.' && RADA[START_ametikoht + 1] == '.') {
                while (정규길이 > 0 && 정규[정규길이 - 1] != '/') 정규길이--;
                if (정규길이 > 0) 정규길이--;
                continue;
            }
            if (정규길이 + kirje_COUNT + (정규길이 == 0 ? 0 : 1) > 63) return -36;
            if (정규길이 > 0) 정규[정규길이++] = '/';
            for (int Loop_INDEX = START_ametikoht; Loop_INDEX < 읽는자리; Loop_INDEX++) 정규[정규길이++] = RADA[Loop_INDEX];
        }
        return 0;
    }
    static int FIND_kaust(int kirje_COUNT) {
        if (kirje_COUNT == 0) return 0;
        for (int Loop_INDEX = 1; Loop_INDEX < 16; Loop_INDEX++) if (폴더길이[Loop_INDEX] == kirje_COUNT && 접두(kaust_nimetus, Loop_INDEX * 64, kirje_COUNT, 정규, kirje_COUNT)) return Loop_INDEX;
        return -1;
    }
    static int tšekk_ema() {
        int kirje_COUNT = 정규길이; while (kirje_COUNT > 0 && 정규[kirje_COUNT - 1] != '/') kirje_COUNT--;
        return FIND_kaust(kirje_COUNT == 0 ? 0 : kirje_COUNT - 1) < 0 ? -2 : 0;
    }
    public static int avama_kaust() {
        int 처리값 = normaliseerima_VALUE(); if (처리값 < 0) return 처리값;
        if (FIND_kaust(정규길이) >= 0 || FIND_kirje() >= 0) return -17;
        처리값 = tšekk_ema(); if (처리값 < 0) return 처리값;
        for (int Loop_INDEX = 1; Loop_INDEX < 16; Loop_INDEX++) if (폴더길이[Loop_INDEX] == 0) {
            폴더길이[Loop_INDEX] = 정규길이; for (int sisemine_ametikoht = 0; sisemine_ametikoht < 정규길이; sisemine_ametikoht++) kaust_nimetus[Loop_INDEX * 64 + sisemine_ametikoht] = 정규[sisemine_ametikoht]; return 0;
        }
        return -28;
    }
    public static int 항목종류() {
        int 처리값 = normaliseerima_VALUE(); if (처리값 < 0) return 처리값;
        if (FIND_kaust(정규길이) >= 0) return 2;
        return FIND_kirje() >= 0 ? 1 : 0;
    }
    public static int muutma_kaust() {
        int 처리값 = normaliseerima_VALUE(); if (처리값 < 0) return 처리값;
        if (FIND_kaust(정규길이) < 0) return -2;
        현재길이 = 정규길이; for (int Loop_INDEX = 0; Loop_INDEX < 현재길이; Loop_INDEX++) tähtaja_piires_kaup[Loop_INDEX] = 정규[Loop_INDEX]; return 0;
    }
    public static int eemaldama_kaust() {
        int 처리값 = normaliseerima_VALUE(); if (처리값 < 0) return 처리값;
        int kaust_number = FIND_kaust(정규길이); if (kaust_number < 0) return -2; if (kaust_number == 0) return -16;
        if (현재길이 == 정규길이 && 접두(tähtaja_piires_kaup, 0, 현재길이, 정규, 정규길이)) return -16;
        for (int Loop_INDEX = 0; Loop_INDEX < Fail_COUNT; Loop_INDEX++) {
            if (이름길이[Loop_INDEX] > 정규길이 && 접두(Nimi_2, Loop_INDEX * 64, 이름길이[Loop_INDEX], 정규, 정규길이) && Nimi_2[Loop_INDEX * 64 + 정규길이] == '/') return -39;
        }
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) {
            if (폴더길이[Loop_INDEX] > 정규길이 && 접두(kaust_nimetus, Loop_INDEX * 64, 폴더길이[Loop_INDEX], 정규, 정규길이) && kaust_nimetus[Loop_INDEX * 64 + 정규길이] == '/') return -39;
        }
        폴더길이[kaust_number] = 0; return 0;
    }
    public static int Nimeta_ümber_kirje(int 원본번호) {
        if (원본번호 < 0 || 원본번호 >= Fail_COUNT || 이름길이[원본번호] == 0) return -2;
        int 처리값 = normaliseerima_VALUE(); if (처리값 < 0) return 처리값;
        if (FIND_kaust(정규길이) >= 0) return -21;
        처리값 = tšekk_ema(); if (처리값 < 0) return 처리값;
        int 이전값 = FIND_kirje(); if (이전값 == 원본번호) return 0;
        if (이전값 >= 0) 이름길이[이전값] = 0;
        이름길이[원본번호] = 정규길이; for (int Loop_INDEX = 0; Loop_INDEX < 정규길이; Loop_INDEX++) Nimi_2[원본번호 * 64 + Loop_INDEX] = 정규[Loop_INDEX]; return 0;
    }
    static int kirje_START(int[] andmed_ARRAY, int 시작점, int kirje_COUNT) {
        if (!접두(andmed_ARRAY, 시작점, kirje_COUNT, 정규, 정규길이)) return -1;
        int START_ametikoht = 정규길이;
        if (START_ametikoht > 0) { if (kirje_COUNT <= START_ametikoht || andmed_ARRAY[시작점 + START_ametikoht] != '/') return -1; START_ametikoht++; }
        if (kirje_COUNT <= START_ametikoht) return -1;
        for (int Loop_INDEX = START_ametikoht; Loop_INDEX < kirje_COUNT; Loop_INDEX++) if (andmed_ARRAY[시작점 + Loop_INDEX] == '/') return -1;
        return START_ametikoht;
    }
    static void tähtaja_piires_kirjutamine() { 단말.문자('/'); for (int Loop_INDEX = 0; Loop_INDEX < 현재길이; Loop_INDEX++) Tahvel.직렬쓰기(tähtaja_piires_kaup[Loop_INDEX]); }
    static int 경로목록() {
        int 처리값 = normaliseerima_VALUE(); if (처리값 < 0) return 처리값;
        int Fail_siht = FIND_kirje();
        if (Fail_siht >= 0) { for (int Loop_INDEX = 0; Loop_INDEX < 정규길이; Loop_INDEX++) Tahvel.직렬쓰기(정규[Loop_INDEX]); 단말.Kirjutamine("  "); 단말.number(길이[Fail_siht]); 단말.Kirjutamine("bait_VALUE(주기억 Fail)\n"); return 0; }
        if (FIND_kaust(정규길이) < 0) return -2;
        for (int 뒷값 = 1; 뒷값 < 16; 뒷값++) if (폴더길이[뒷값] > 0) {
            int START_ametikoht = kirje_START(kaust_nimetus, 뒷값 * 64, 폴더길이[뒷값]); if (START_ametikoht < 0) continue;
            for (int Loop_INDEX = START_ametikoht; Loop_INDEX < 폴더길이[뒷값]; Loop_INDEX++) Tahvel.직렬쓰기(kaust_nimetus[뒷값 * 64 + Loop_INDEX]); 단말.Kirjutamine("/\n");
        }
        for (int Fail_INDEX = 0; Fail_INDEX < Fail_COUNT; Fail_INDEX++) if (이름길이[Fail_INDEX] > 0) {
            int START_ametikoht = kirje_START(Nimi_2, Fail_INDEX * 64, 이름길이[Fail_INDEX]); if (START_ametikoht < 0) continue;
            for (int Loop_INDEX = START_ametikoht; Loop_INDEX < 이름길이[Fail_INDEX]; Loop_INDEX++) Tahvel.직렬쓰기(Nimi_2[Fail_INDEX * 64 + Loop_INDEX]);
            단말.Kirjutamine("  "); 단말.number(길이[Fail_INDEX]); 단말.Kirjutamine("bait_VALUE(주기억 Fail)\n");
        }
        return 0;
    }
}
