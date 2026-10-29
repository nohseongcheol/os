// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** RAM FAYL 64개, 파일당 16384바이트, 서술자 16개. 모든 verilənlər/정책은 Java에 있다.
 * 호출 도중 양보하지 않으므로 현재의 단일 코어 협력식 작업 사이에서 원자적이다.
 * 디스크 저장이나 POSIX 전체 구현을 뜻하지 않는다. 음수 반환은 XƏTA 번호다.
 */
public final class Yaddaş_Fayllar {
    static final int fayl_COUNT = 64;
    static int[] Ad = new int[fayl_COUNT * 64];
    static int[] 이름길이 = new int[fayl_COUNT];
    // Pack four bytes in each Java int, preserving the old content heap budget.
    static int[] Məzmun_VALUE = new int[fayl_COUNT * 4096];
    static int[] uzunluq_VALUE = new int[fayl_COUNT];
    static int[] İstinad_COUNT = new int[fayl_COUNT];
    static int[] 사용 = new int[16];
    static int[] hədəf = new int[16];
    static int[] yerinə_qoymaq = new int[16];
    static int[] metod_MODE = new int[16];
    static int[] Cığır = new int[64];
    static int yol_uzunluq;

    public static int 파일한도() { return fayl_COUNT; }
    static int 자료읽기(int FAYL, int yerinə_qoymaq_INDEX) { return (Məzmun_VALUE[FAYL * 4096 + yerinə_qoymaq_INDEX / 4] >>> ((yerinə_qoymaq_INDEX & 3) * 8)) & 255; }
    static void yazmaq_verilənlər(int FAYL, int yerinə_qoymaq_INDEX, int VALUE) {
        int slot_daxiletmə = FAYL * 4096 + yerinə_qoymaq_INDEX / 4, hərəkət_etdir_VALUE = (yerinə_qoymaq_INDEX & 3) * 8;
        Məzmun_VALUE[slot_daxiletmə] = (Məzmun_VALUE[slot_daxiletmə] & ~(255 << hərəkət_etdir_VALUE)) | ((VALUE & 255) << hərəkət_etdir_VALUE);
    }

    public static int yol_Başla(int Böyüklük) {
        yol_uzunluq = 0;
        if (Böyüklük < 1 || Böyüklük > 63) return -36;
        yol_uzunluq = Böyüklük;
        for (int Loop_INDEX = 0; Loop_INDEX < Böyüklük; Loop_INDEX++) Cığır[Loop_INDEX] = 0;
        return 0;
    }
    public static int yol_bayt(int INDEX, int VALUE) {
        if (INDEX < 0 || INDEX >= yol_uzunluq || VALUE < 1 || VALUE > 255) return -22;
        Cığır[INDEX] = VALUE; return 0;
    }
    static int FIND_daxiletmə() {
        for (int fayl_INDEX = 0; fayl_INDEX < fayl_COUNT; fayl_INDEX++) if (이름길이[fayl_INDEX] > 0 && 이름길이[fayl_INDEX] == 정규길이 && 접두(Ad, fayl_INDEX * 64, 이름길이[fayl_INDEX], 정규, 정규길이)) return fayl_INDEX;
        return -1;
    }
    public static int Aç(int 플래그) {
        if (yol_uzunluq == 0 || (플래그 & ~0x6c3) != 0 || (플래그 & 3) == 3) return -22;
        for (int Loop_INDEX = 0; Loop_INDEX < yol_uzunluq; Loop_INDEX++) if (Cığır[Loop_INDEX] == 0) return -22;
        if ((플래그 & 0x200) != 0 && (플래그 & 3) == 0) return -22;
        int ölçü = normallaşdırmaq_VALUE(); if (ölçü < 0) return ölçü;
        if (FIND_kataloq(정규길이) >= 0) return -21;
        ölçü = 부모확인(); if (ölçü < 0) return ölçü;
        int FAYL = FIND_daxiletmə();
        if (FAYL >= 0 && (플래그 & 0xc0) == 0xc0) return -17;
        if (FAYL < 0 && (플래그 & 0x40) == 0) return -2;
        int 서술자 = -1;
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (사용[Loop_INDEX] == 0) { 서술자 = Loop_INDEX; break; }
        if (서술자 < 0) return -24;
        if (FAYL < 0) {
            for (int Loop_INDEX = 0; Loop_INDEX < fayl_COUNT; Loop_INDEX++) if (이름길이[Loop_INDEX] == 0 && İstinad_COUNT[Loop_INDEX] == 0) { FAYL = Loop_INDEX; break; }
            if (FAYL < 0) return -28;
            이름길이[FAYL] = 정규길이;
            for (int Loop_INDEX = 0; Loop_INDEX < 정규길이; Loop_INDEX++) Ad[FAYL * 64 + Loop_INDEX] = 정규[Loop_INDEX];
            uzunluq_VALUE[FAYL] = 0;
        }
        if ((플래그 & 0x200) != 0) uzunluq_VALUE[FAYL] = 0;
        사용[서술자] = 1; hədəf[서술자] = FAYL; yerinə_qoymaq[서술자] = 0; metod_MODE[서술자] = 플래그;
        İstinad_COUNT[FAYL]++;
        return 서술자 + 3;
    }
    static int yoxlamaq(int 서술자) {
        return 서술자 >= 3 && 서술자 < 19 && 사용[서술자 - 3] != 0 ? 서술자 - 3 : -1;
    }
    public static int Oxuma(int 서술자) {
        int slot_daxiletmə = yoxlamaq(서술자);
        if (slot_daxiletmə < 0 || (metod_MODE[slot_daxiletmə] & 3) == 1) return -9;
        int FAYL = hədəf[slot_daxiletmə];
        if (yerinə_qoymaq[slot_daxiletmə] >= uzunluq_VALUE[FAYL]) return 256; // EOF와 faktiki_verilənlər 0x00..0xff 구별
        return 자료읽기(FAYL, yerinə_qoymaq[slot_daxiletmə]++);
    }
    public static int Yazma(int 서술자, int VALUE) {
        int slot_daxiletmə = yoxlamaq(서술자);
        if (slot_daxiletmə < 0 || (metod_MODE[slot_daxiletmə] & 3) == 0) return -9;
        int FAYL = hədəf[slot_daxiletmə];
        if ((metod_MODE[slot_daxiletmə] & 0x400) != 0) yerinə_qoymaq[slot_daxiletmə] = uzunluq_VALUE[FAYL];
        if (yerinə_qoymaq[slot_daxiletmə] >= 16384) return -28;
        while (uzunluq_VALUE[FAYL] < yerinə_qoymaq[slot_daxiletmə]) yazmaq_verilənlər(FAYL, uzunluq_VALUE[FAYL]++, 0);
        yazmaq_verilənlər(FAYL, yerinə_qoymaq[slot_daxiletmə]++, VALUE);
        if (uzunluq_VALUE[FAYL] < yerinə_qoymaq[slot_daxiletmə]) uzunluq_VALUE[FAYL] = yerinə_qoymaq[slot_daxiletmə];
        return 1;
    }
    public static int axtarmaq_yerinə_qoymaq(int 서술자, int 거리, int Project_kök) {
        int slot_daxiletmə = yoxlamaq(서술자);
        if (slot_daxiletmə < 0) return -9;
        if (Project_kök < 0 || Project_kök > 2 || 거리 < -16384 || 거리 > 16384) return -22;
        int 새위치 = 거리 + (Project_kök == 0 ? 0 : Project_kök == 1 ? yerinə_qoymaq[slot_daxiletmə] : uzunluq_VALUE[hədəf[slot_daxiletmə]]);
        if (새위치 < 0 || 새위치 > 16384) return -22;
        yerinə_qoymaq[slot_daxiletmə] = 새위치; return 새위치;
    }
    public static int Bağla(int 서술자) {
        int slot_daxiletmə = yoxlamaq(서술자);
        if (slot_daxiletmə < 0) return -9;
        İstinad_COUNT[hədəf[slot_daxiletmə]]--; 사용[slot_daxiletmə] = 0; return 0;
    }
    public static int Böyüklük(int 서술자) {
        int slot_daxiletmə = yoxlamaq(서술자); return slot_daxiletmə < 0 ? -9 : uzunluq_VALUE[hədəf[slot_daxiletmə]];
    }
    public static int Dəst_uzunluq(int 서술자, int Böyüklük) {
        int slot_daxiletmə = yoxlamaq(서술자);
        if (slot_daxiletmə < 0 || (metod_MODE[slot_daxiletmə] & 3) == 0) return -9;
        if (Böyüklük < 0 || Böyüklük > 16384) return -22;
        int FAYL = hədəf[slot_daxiletmə];
        while (uzunluq_VALUE[FAYL] < Böyüklük) yazmaq_verilənlər(FAYL, uzunluq_VALUE[FAYL]++, 0);
        uzunluq_VALUE[FAYL] = Böyüklük; return 0;
    }
    public static int silmək_daxiletmə_c8dbc399() {
        if (yol_uzunluq == 0) return -22;
        int ölçü = normallaşdırmaq_VALUE(); if (ölçü < 0) return ölçü;
        if (FIND_kataloq(정규길이) >= 0) return -21;
        ölçü = 부모확인(); if (ölçü < 0) return ölçü;
        int FAYL = FIND_daxiletmə();
        if (FAYL < 0) return -2;
        이름길이[FAYL] = 0; return 0; // 열려 있는 파일은 마지막 close까지 유지
    }
    static void daxiletmə_Siyahı() {
        yol_Başla(1); yol_bayt(0, '.'); 경로목록();
    }
    public static int 공개이름길이(int INDEX) {
        if (INDEX < 0 || INDEX >= fayl_COUNT || 이름길이[INDEX] == 0) return 0;
        for (int Loop_INDEX = 0; Loop_INDEX < 이름길이[INDEX]; Loop_INDEX++) if (Ad[INDEX * 64 + Loop_INDEX] == '/') return 0;
        return 이름길이[INDEX];
    }
    public static int 공개이름바이트(int INDEX, int yerinə_qoymaq_INDEX) {
        return INDEX >= 0 && INDEX < fayl_COUNT && yerinə_qoymaq_INDEX >= 0 && yerinə_qoymaq_INDEX < 이름길이[INDEX] ? Ad[INDEX * 64 + yerinə_qoymaq_INDEX] : -22;
    }
    public static int 공개파일크기(int INDEX) { return INDEX >= 0 && INDEX < fayl_COUNT ? uzunluq_VALUE[INDEX] : -22; }
    static int[] 정규 = new int[64], 현재 = new int[64], kataloq_ad = new int[16 * 64], kataloq_uzunluq = new int[16];
    static int 정규길이, 현재길이;
    static boolean 접두(int[] 이름들, int İcra_Et, int yol_VALUE, int[] ön_VALUE, int aparıcı_yol) {
        if (yol_VALUE < aparıcı_yol) return false;
        for (int Loop_INDEX = 0; Loop_INDEX < aparıcı_yol; Loop_INDEX++) if (이름들[İcra_Et + Loop_INDEX] != ön_VALUE[Loop_INDEX]) return false;
        return true;
    }
    static int normallaşdırmaq_VALUE() {
        if (yol_uzunluq == 0) return -22;
        정규길이 = Cığır[0] == '/' ? 0 : 현재길이;
        for (int Loop_INDEX = 0; Loop_INDEX < 정규길이; Loop_INDEX++) 정규[Loop_INDEX] = 현재[Loop_INDEX];
        int 읽는자리 = 0;
        while (읽는자리 < yol_uzunluq) {
            while (읽는자리 < yol_uzunluq && Cığır[읽는자리] == '/') 읽는자리++;
            int Başla_yerinə_qoymaq = 읽는자리; while (읽는자리 < yol_uzunluq && Cığır[읽는자리] != '/') { if (Cığır[읽는자리] == 0) return -22; 읽는자리++; }
            int daxiletmə_COUNT = 읽는자리 - Başla_yerinə_qoymaq; if (daxiletmə_COUNT == 0 || daxiletmə_COUNT == 1 && Cığır[Başla_yerinə_qoymaq] == '.') continue;
            if (daxiletmə_COUNT == 2 && Cığır[Başla_yerinə_qoymaq] == '.' && Cığır[Başla_yerinə_qoymaq + 1] == '.') {
                while (정규길이 > 0 && 정규[정규길이 - 1] != '/') 정규길이--;
                if (정규길이 > 0) 정규길이--;
                continue;
            }
            if (정규길이 + daxiletmə_COUNT + (정규길이 == 0 ? 0 : 1) > 63) return -36;
            if (정규길이 > 0) 정규[정규길이++] = '/';
            for (int Loop_INDEX = Başla_yerinə_qoymaq; Loop_INDEX < 읽는자리; Loop_INDEX++) 정규[정규길이++] = Cığır[Loop_INDEX];
        }
        return 0;
    }
    static int FIND_kataloq(int daxiletmə_COUNT) {
        if (daxiletmə_COUNT == 0) return 0;
        for (int Loop_INDEX = 1; Loop_INDEX < 16; Loop_INDEX++) if (kataloq_uzunluq[Loop_INDEX] == daxiletmə_COUNT && 접두(kataloq_ad, Loop_INDEX * 64, daxiletmə_COUNT, 정규, daxiletmə_COUNT)) return Loop_INDEX;
        return -1;
    }
    static int 부모확인() {
        int daxiletmə_COUNT = 정규길이; while (daxiletmə_COUNT > 0 && 정규[daxiletmə_COUNT - 1] != '/') daxiletmə_COUNT--;
        return FIND_kataloq(daxiletmə_COUNT == 0 ? 0 : daxiletmə_COUNT - 1) < 0 ? -2 : 0;
    }
    public static int yarat_kataloq() {
        int 처리값 = normallaşdırmaq_VALUE(); if (처리값 < 0) return 처리값;
        if (FIND_kataloq(정규길이) >= 0 || FIND_daxiletmə() >= 0) return -17;
        처리값 = 부모확인(); if (처리값 < 0) return 처리값;
        for (int Loop_INDEX = 1; Loop_INDEX < 16; Loop_INDEX++) if (kataloq_uzunluq[Loop_INDEX] == 0) {
            kataloq_uzunluq[Loop_INDEX] = 정규길이; for (int daxili_qoşulma_yerinə_qoymaq = 0; daxili_qoşulma_yerinə_qoymaq < 정규길이; daxili_qoşulma_yerinə_qoymaq++) kataloq_ad[Loop_INDEX * 64 + daxili_qoşulma_yerinə_qoymaq] = 정규[daxili_qoşulma_yerinə_qoymaq]; return 0;
        }
        return -28;
    }
    public static int 항목종류() {
        int 처리값 = normallaşdırmaq_VALUE(); if (처리값 < 0) return 처리값;
        if (FIND_kataloq(정규길이) >= 0) return 2;
        return FIND_daxiletmə() >= 0 ? 1 : 0;
    }
    public static int dəyişdirmək_kataloq() {
        int 처리값 = normallaşdırmaq_VALUE(); if (처리값 < 0) return 처리값;
        if (FIND_kataloq(정규길이) < 0) return -2;
        현재길이 = 정규길이; for (int Loop_INDEX = 0; Loop_INDEX < 현재길이; Loop_INDEX++) 현재[Loop_INDEX] = 정규[Loop_INDEX]; return 0;
    }
    public static int silmək_kataloq() {
        int 처리값 = normallaşdırmaq_VALUE(); if (처리값 < 0) return 처리값;
        int 폴더번호 = FIND_kataloq(정규길이); if (폴더번호 < 0) return -2; if (폴더번호 == 0) return -16;
        if (현재길이 == 정규길이 && 접두(현재, 0, 현재길이, 정규, 정규길이)) return -16;
        for (int Loop_INDEX = 0; Loop_INDEX < fayl_COUNT; Loop_INDEX++) {
            if (이름길이[Loop_INDEX] > 정규길이 && 접두(Ad, Loop_INDEX * 64, 이름길이[Loop_INDEX], 정규, 정규길이) && Ad[Loop_INDEX * 64 + 정규길이] == '/') return -39;
        }
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) {
            if (kataloq_uzunluq[Loop_INDEX] > 정규길이 && 접두(kataloq_ad, Loop_INDEX * 64, kataloq_uzunluq[Loop_INDEX], 정규, 정규길이) && kataloq_ad[Loop_INDEX * 64 + 정규길이] == '/') return -39;
        }
        kataloq_uzunluq[폴더번호] = 0; return 0;
    }
    public static int 이름바꾸기(int 원본번호) {
        if (원본번호 < 0 || 원본번호 >= fayl_COUNT || 이름길이[원본번호] == 0) return -2;
        int 처리값 = normallaşdırmaq_VALUE(); if (처리값 < 0) return 처리값;
        if (FIND_kataloq(정규길이) >= 0) return -21;
        처리값 = 부모확인(); if (처리값 < 0) return 처리값;
        int 이전값 = FIND_daxiletmə(); if (이전값 == 원본번호) return 0;
        if (이전값 >= 0) 이름길이[이전값] = 0;
        이름길이[원본번호] = 정규길이; for (int Loop_INDEX = 0; Loop_INDEX < 정규길이; Loop_INDEX++) Ad[원본번호 * 64 + Loop_INDEX] = 정규[Loop_INDEX]; return 0;
    }
    static int daxiletmə_Başla(int[] verilənlər_ARRAY, int 시작점, int daxiletmə_COUNT) {
        if (!접두(verilənlər_ARRAY, 시작점, daxiletmə_COUNT, 정규, 정규길이)) return -1;
        int Başla_yerinə_qoymaq = 정규길이;
        if (Başla_yerinə_qoymaq > 0) { if (daxiletmə_COUNT <= Başla_yerinə_qoymaq || verilənlər_ARRAY[시작점 + Başla_yerinə_qoymaq] != '/') return -1; Başla_yerinə_qoymaq++; }
        if (daxiletmə_COUNT <= Başla_yerinə_qoymaq) return -1;
        for (int Loop_INDEX = Başla_yerinə_qoymaq; Loop_INDEX < daxiletmə_COUNT; Loop_INDEX++) if (verilənlər_ARRAY[시작점 + Loop_INDEX] == '/') return -1;
        return Başla_yerinə_qoymaq;
    }
    static void 현재쓰기() { 단말.문자('/'); for (int Loop_INDEX = 0; Loop_INDEX < 현재길이; Loop_INDEX++) lövhə.직렬쓰기(현재[Loop_INDEX]); }
    static int 경로목록() {
        int 처리값 = normallaşdırmaq_VALUE(); if (처리값 < 0) return 처리값;
        int fayl_hədəf = FIND_daxiletmə();
        if (fayl_hədəf >= 0) { for (int Loop_INDEX = 0; Loop_INDEX < 정규길이; Loop_INDEX++) lövhə.직렬쓰기(정규[Loop_INDEX]); 단말.Yazma("  "); 단말.수(uzunluq_VALUE[fayl_hədəf]); 단말.Yazma("bayt_VALUE(주기억 FAYL)\n"); return 0; }
        if (FIND_kataloq(정규길이) < 0) return -2;
        for (int 뒷값 = 1; 뒷값 < 16; 뒷값++) if (kataloq_uzunluq[뒷값] > 0) {
            int Başla_yerinə_qoymaq = daxiletmə_Başla(kataloq_ad, 뒷값 * 64, kataloq_uzunluq[뒷값]); if (Başla_yerinə_qoymaq < 0) continue;
            for (int Loop_INDEX = Başla_yerinə_qoymaq; Loop_INDEX < kataloq_uzunluq[뒷값]; Loop_INDEX++) lövhə.직렬쓰기(kataloq_ad[뒷값 * 64 + Loop_INDEX]); 단말.Yazma("/\n");
        }
        for (int fayl_INDEX = 0; fayl_INDEX < fayl_COUNT; fayl_INDEX++) if (이름길이[fayl_INDEX] > 0) {
            int Başla_yerinə_qoymaq = daxiletmə_Başla(Ad, fayl_INDEX * 64, 이름길이[fayl_INDEX]); if (Başla_yerinə_qoymaq < 0) continue;
            for (int Loop_INDEX = Başla_yerinə_qoymaq; Loop_INDEX < 이름길이[fayl_INDEX]; Loop_INDEX++) lövhə.직렬쓰기(Ad[fayl_INDEX * 64 + Loop_INDEX]);
            단말.Yazma("  "); 단말.수(uzunluq_VALUE[fayl_INDEX]); 단말.Yazma("bayt_VALUE(주기억 FAYL)\n");
        }
        return 0;
    }
}
