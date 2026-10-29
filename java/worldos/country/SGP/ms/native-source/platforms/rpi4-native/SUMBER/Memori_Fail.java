// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** RAM Fail 64개, 파일당 16384바이트, 서술자 16개. 모든 data/정책은 Java에 있다.
 * 호출 도중 양보하지 않으므로 현재의 단일 코어 협력식 작업 사이에서 원자적이다.
 * 디스크 저장이나 POSIX 전체 구현을 뜻하지 않는다. 음수 반환은 RALAT 번호다.
 */
public final class Memori_Fail {
    static final int fail_COUNT = 64;
    static int[] Nama = new int[fail_COUNT * 64];
    static int[] 이름길이 = new int[fail_COUNT];
    // Pack four bytes in each Java int, preserving the old content heap budget.
    static int[] Kandungan_VALUE = new int[fail_COUNT * 4096];
    static int[] kepanjangan_VALUE = new int[fail_COUNT];
    static int[] Rujukan_COUNT = new int[fail_COUNT];
    static int[] 사용 = new int[16];
    static int[] sasaran = new int[16];
    static int[] Kedudukan = new int[16];
    static int[] kaedah_mod = new int[16];
    static int[] LALUAN = new int[64];
    static int laluan_kepanjangan;

    public static int 파일한도() { return fail_COUNT; }
    static int 자료읽기(int Fail, int jawatan_INDEX) { return (Kandungan_VALUE[Fail * 4096 + jawatan_INDEX / 4] >>> ((jawatan_INDEX & 3) * 8)) & 255; }
    static void tulis_data(int Fail, int jawatan_INDEX, int VALUE) {
        int 칸 = Fail * 4096 + jawatan_INDEX / 4, alih_VALUE = (jawatan_INDEX & 3) * 8;
        Kandungan_VALUE[칸] = (Kandungan_VALUE[칸] & ~(255 << alih_VALUE)) | ((VALUE & 255) << alih_VALUE);
    }

    public static int laluan_Mula(int Saiz) {
        laluan_kepanjangan = 0;
        if (Saiz < 1 || Saiz > 63) return -36;
        laluan_kepanjangan = Saiz;
        for (int Loop_INDEX = 0; Loop_INDEX < Saiz; Loop_INDEX++) LALUAN[Loop_INDEX] = 0;
        return 0;
    }
    public static int laluan_bait(int INDEX, int VALUE) {
        if (INDEX < 0 || INDEX >= laluan_kepanjangan || VALUE < 1 || VALUE > 255) return -22;
        LALUAN[INDEX] = VALUE; return 0;
    }
    static int Cari_pemasukan() {
        for (int fail_INDEX = 0; fail_INDEX < fail_COUNT; fail_INDEX++) if (이름길이[fail_INDEX] > 0 && 이름길이[fail_INDEX] == 정규길이 && 접두(Nama, fail_INDEX * 64, 이름길이[fail_INDEX], 정규, 정규길이)) return fail_INDEX;
        return -1;
    }
    public static int Buka(int 플래그) {
        if (laluan_kepanjangan == 0 || (플래그 & ~0x6c3) != 0 || (플래그 & 3) == 3) return -22;
        for (int Loop_INDEX = 0; Loop_INDEX < laluan_kepanjangan; Loop_INDEX++) if (LALUAN[Loop_INDEX] == 0) return -22;
        if ((플래그 & 0x200) != 0 && (플래그 & 3) == 0) return -22;
        int ukuran = menormalkan_VALUE(); if (ukuran < 0) return ukuran;
        if (Cari_direktori(정규길이) >= 0) return -21;
        ukuran = 부모확인(); if (ukuran < 0) return ukuran;
        int Fail = Cari_pemasukan();
        if (Fail >= 0 && (플래그 & 0xc0) == 0xc0) return -17;
        if (Fail < 0 && (플래그 & 0x40) == 0) return -2;
        int 서술자 = -1;
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (사용[Loop_INDEX] == 0) { 서술자 = Loop_INDEX; break; }
        if (서술자 < 0) return -24;
        if (Fail < 0) {
            for (int Loop_INDEX = 0; Loop_INDEX < fail_COUNT; Loop_INDEX++) if (이름길이[Loop_INDEX] == 0 && Rujukan_COUNT[Loop_INDEX] == 0) { Fail = Loop_INDEX; break; }
            if (Fail < 0) return -28;
            이름길이[Fail] = 정규길이;
            for (int Loop_INDEX = 0; Loop_INDEX < 정규길이; Loop_INDEX++) Nama[Fail * 64 + Loop_INDEX] = 정규[Loop_INDEX];
            kepanjangan_VALUE[Fail] = 0;
        }
        if ((플래그 & 0x200) != 0) kepanjangan_VALUE[Fail] = 0;
        사용[서술자] = 1; sasaran[서술자] = Fail; Kedudukan[서술자] = 0; kaedah_mod[서술자] = 플래그;
        Rujukan_COUNT[Fail]++;
        return 서술자 + 3;
    }
    static int tentu_sahkan(int 서술자) {
        return 서술자 >= 3 && 서술자 < 19 && 사용[서술자 - 3] != 0 ? 서술자 - 3 : -1;
    }
    public static int Baca(int 서술자) {
        int 칸 = tentu_sahkan(서술자);
        if (칸 < 0 || (kaedah_mod[칸] & 3) == 1) return -9;
        int Fail = sasaran[칸];
        if (Kedudukan[칸] >= kepanjangan_VALUE[Fail]) return 256; // EOF와 sebenar_data 0x00..0xff 구별
        return 자료읽기(Fail, Kedudukan[칸]++);
    }
    public static int Tulis(int 서술자, int VALUE) {
        int 칸 = tentu_sahkan(서술자);
        if (칸 < 0 || (kaedah_mod[칸] & 3) == 0) return -9;
        int Fail = sasaran[칸];
        if ((kaedah_mod[칸] & 0x400) != 0) Kedudukan[칸] = kepanjangan_VALUE[Fail];
        if (Kedudukan[칸] >= 16384) return -28;
        while (kepanjangan_VALUE[Fail] < Kedudukan[칸]) tulis_data(Fail, kepanjangan_VALUE[Fail]++, 0);
        tulis_data(Fail, Kedudukan[칸]++, VALUE);
        if (kepanjangan_VALUE[Fail] < Kedudukan[칸]) kepanjangan_VALUE[Fail] = Kedudukan[칸];
        return 1;
    }
    public static int cari_jawatan(int 서술자, int 거리, int projek_akar) {
        int 칸 = tentu_sahkan(서술자);
        if (칸 < 0) return -9;
        if (projek_akar < 0 || projek_akar > 2 || 거리 < -16384 || 거리 > 16384) return -22;
        int 새위치 = 거리 + (projek_akar == 0 ? 0 : projek_akar == 1 ? Kedudukan[칸] : kepanjangan_VALUE[sasaran[칸]]);
        if (새위치 < 0 || 새위치 > 16384) return -22;
        Kedudukan[칸] = 새위치; return 새위치;
    }
    public static int Tutup(int 서술자) {
        int 칸 = tentu_sahkan(서술자);
        if (칸 < 0) return -9;
        Rujukan_COUNT[sasaran[칸]]--; 사용[칸] = 0; return 0;
    }
    public static int Saiz(int 서술자) {
        int 칸 = tentu_sahkan(서술자); return 칸 < 0 ? -9 : kepanjangan_VALUE[sasaran[칸]];
    }
    public static int set_kepanjangan(int 서술자, int Saiz) {
        int 칸 = tentu_sahkan(서술자);
        if (칸 < 0 || (kaedah_mod[칸] & 3) == 0) return -9;
        if (Saiz < 0 || Saiz > 16384) return -22;
        int Fail = sasaran[칸];
        while (kepanjangan_VALUE[Fail] < Saiz) tulis_data(Fail, kepanjangan_VALUE[Fail]++, 0);
        kepanjangan_VALUE[Fail] = Saiz; return 0;
    }
    public static int padam_pemasukan() {
        if (laluan_kepanjangan == 0) return -22;
        int ukuran = menormalkan_VALUE(); if (ukuran < 0) return ukuran;
        if (Cari_direktori(정규길이) >= 0) return -21;
        ukuran = 부모확인(); if (ukuran < 0) return ukuran;
        int Fail = Cari_pemasukan();
        if (Fail < 0) return -2;
        이름길이[Fail] = 0; return 0; // 열려 있는 파일은 마지막 close까지 유지
    }
    static void pemasukan_Senarai() {
        laluan_Mula(1); laluan_bait(0, '.'); 경로목록();
    }
    public static int 공개이름길이(int INDEX) {
        if (INDEX < 0 || INDEX >= fail_COUNT || 이름길이[INDEX] == 0) return 0;
        for (int Loop_INDEX = 0; Loop_INDEX < 이름길이[INDEX]; Loop_INDEX++) if (Nama[INDEX * 64 + Loop_INDEX] == '/') return 0;
        return 이름길이[INDEX];
    }
    public static int 공개이름바이트(int INDEX, int jawatan_INDEX) {
        return INDEX >= 0 && INDEX < fail_COUNT && jawatan_INDEX >= 0 && jawatan_INDEX < 이름길이[INDEX] ? Nama[INDEX * 64 + jawatan_INDEX] : -22;
    }
    public static int 공개파일크기(int INDEX) { return INDEX >= 0 && INDEX < fail_COUNT ? kepanjangan_VALUE[INDEX] : -22; }
    static int[] 정규 = new int[64], 현재 = new int[64], direktori_nama = new int[16 * 64], direktori_kepanjangan = new int[16];
    static int 정규길이, 현재길이;
    static boolean 접두(int[] 이름들, int Jalan, int laluan_VALUE, int[] hadapan_VALUE, int jarak_baris_laluan) {
        if (laluan_VALUE < jarak_baris_laluan) return false;
        for (int Loop_INDEX = 0; Loop_INDEX < jarak_baris_laluan; Loop_INDEX++) if (이름들[Jalan + Loop_INDEX] != hadapan_VALUE[Loop_INDEX]) return false;
        return true;
    }
    static int menormalkan_VALUE() {
        if (laluan_kepanjangan == 0) return -22;
        정규길이 = LALUAN[0] == '/' ? 0 : 현재길이;
        for (int Loop_INDEX = 0; Loop_INDEX < 정규길이; Loop_INDEX++) 정규[Loop_INDEX] = 현재[Loop_INDEX];
        int 읽는자리 = 0;
        while (읽는자리 < laluan_kepanjangan) {
            while (읽는자리 < laluan_kepanjangan && LALUAN[읽는자리] == '/') 읽는자리++;
            int Mula_jawatan = 읽는자리; while (읽는자리 < laluan_kepanjangan && LALUAN[읽는자리] != '/') { if (LALUAN[읽는자리] == 0) return -22; 읽는자리++; }
            int pemasukan_COUNT = 읽는자리 - Mula_jawatan; if (pemasukan_COUNT == 0 || pemasukan_COUNT == 1 && LALUAN[Mula_jawatan] == '.') continue;
            if (pemasukan_COUNT == 2 && LALUAN[Mula_jawatan] == '.' && LALUAN[Mula_jawatan + 1] == '.') {
                while (정규길이 > 0 && 정규[정규길이 - 1] != '/') 정규길이--;
                if (정규길이 > 0) 정규길이--;
                continue;
            }
            if (정규길이 + pemasukan_COUNT + (정규길이 == 0 ? 0 : 1) > 63) return -36;
            if (정규길이 > 0) 정규[정규길이++] = '/';
            for (int Loop_INDEX = Mula_jawatan; Loop_INDEX < 읽는자리; Loop_INDEX++) 정규[정규길이++] = LALUAN[Loop_INDEX];
        }
        return 0;
    }
    static int Cari_direktori(int pemasukan_COUNT) {
        if (pemasukan_COUNT == 0) return 0;
        for (int Loop_INDEX = 1; Loop_INDEX < 16; Loop_INDEX++) if (direktori_kepanjangan[Loop_INDEX] == pemasukan_COUNT && 접두(direktori_nama, Loop_INDEX * 64, pemasukan_COUNT, 정규, pemasukan_COUNT)) return Loop_INDEX;
        return -1;
    }
    static int 부모확인() {
        int pemasukan_COUNT = 정규길이; while (pemasukan_COUNT > 0 && 정규[pemasukan_COUNT - 1] != '/') pemasukan_COUNT--;
        return Cari_direktori(pemasukan_COUNT == 0 ? 0 : pemasukan_COUNT - 1) < 0 ? -2 : 0;
    }
    public static int cipta_direktori() {
        int 처리값 = menormalkan_VALUE(); if (처리값 < 0) return 처리값;
        if (Cari_direktori(정규길이) >= 0 || Cari_pemasukan() >= 0) return -17;
        처리값 = 부모확인(); if (처리값 < 0) return 처리값;
        for (int Loop_INDEX = 1; Loop_INDEX < 16; Loop_INDEX++) if (direktori_kepanjangan[Loop_INDEX] == 0) {
            direktori_kepanjangan[Loop_INDEX] = 정규길이; for (int dalaman_jawatan = 0; dalaman_jawatan < 정규길이; dalaman_jawatan++) direktori_nama[Loop_INDEX * 64 + dalaman_jawatan] = 정규[dalaman_jawatan]; return 0;
        }
        return -28;
    }
    public static int 항목종류() {
        int 처리값 = menormalkan_VALUE(); if (처리값 < 0) return 처리값;
        if (Cari_direktori(정규길이) >= 0) return 2;
        return Cari_pemasukan() >= 0 ? 1 : 0;
    }
    public static int ubah_direktori() {
        int 처리값 = menormalkan_VALUE(); if (처리값 < 0) return 처리값;
        if (Cari_direktori(정규길이) < 0) return -2;
        현재길이 = 정규길이; for (int Loop_INDEX = 0; Loop_INDEX < 현재길이; Loop_INDEX++) 현재[Loop_INDEX] = 정규[Loop_INDEX]; return 0;
    }
    public static int alih_keluar_direktori() {
        int 처리값 = menormalkan_VALUE(); if (처리값 < 0) return 처리값;
        int 폴더번호 = Cari_direktori(정규길이); if (폴더번호 < 0) return -2; if (폴더번호 == 0) return -16;
        if (현재길이 == 정규길이 && 접두(현재, 0, 현재길이, 정규, 정규길이)) return -16;
        for (int Loop_INDEX = 0; Loop_INDEX < fail_COUNT; Loop_INDEX++) {
            if (이름길이[Loop_INDEX] > 정규길이 && 접두(Nama, Loop_INDEX * 64, 이름길이[Loop_INDEX], 정규, 정규길이) && Nama[Loop_INDEX * 64 + 정규길이] == '/') return -39;
        }
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) {
            if (direktori_kepanjangan[Loop_INDEX] > 정규길이 && 접두(direktori_nama, Loop_INDEX * 64, direktori_kepanjangan[Loop_INDEX], 정규, 정규길이) && direktori_nama[Loop_INDEX * 64 + 정규길이] == '/') return -39;
        }
        direktori_kepanjangan[폴더번호] = 0; return 0;
    }
    public static int 이름바꾸기(int 원본번호) {
        if (원본번호 < 0 || 원본번호 >= fail_COUNT || 이름길이[원본번호] == 0) return -2;
        int 처리값 = menormalkan_VALUE(); if (처리값 < 0) return 처리값;
        if (Cari_direktori(정규길이) >= 0) return -21;
        처리값 = 부모확인(); if (처리값 < 0) return 처리값;
        int 이전값 = Cari_pemasukan(); if (이전값 == 원본번호) return 0;
        if (이전값 >= 0) 이름길이[이전값] = 0;
        이름길이[원본번호] = 정규길이; for (int Loop_INDEX = 0; Loop_INDEX < 정규길이; Loop_INDEX++) Nama[원본번호 * 64 + Loop_INDEX] = 정규[Loop_INDEX]; return 0;
    }
    static int pemasukan_Mula(int[] data_ARRAY, int 시작점, int pemasukan_COUNT) {
        if (!접두(data_ARRAY, 시작점, pemasukan_COUNT, 정규, 정규길이)) return -1;
        int Mula_jawatan = 정규길이;
        if (Mula_jawatan > 0) { if (pemasukan_COUNT <= Mula_jawatan || data_ARRAY[시작점 + Mula_jawatan] != '/') return -1; Mula_jawatan++; }
        if (pemasukan_COUNT <= Mula_jawatan) return -1;
        for (int Loop_INDEX = Mula_jawatan; Loop_INDEX < pemasukan_COUNT; Loop_INDEX++) if (data_ARRAY[시작점 + Loop_INDEX] == '/') return -1;
        return Mula_jawatan;
    }
    static void 현재쓰기() { 단말.문자('/'); for (int Loop_INDEX = 0; Loop_INDEX < 현재길이; Loop_INDEX++) Papan.직렬쓰기(현재[Loop_INDEX]); }
    static int 경로목록() {
        int 처리값 = menormalkan_VALUE(); if (처리값 < 0) return 처리값;
        int fail_sasaran = Cari_pemasukan();
        if (fail_sasaran >= 0) { for (int Loop_INDEX = 0; Loop_INDEX < 정규길이; Loop_INDEX++) Papan.직렬쓰기(정규[Loop_INDEX]); 단말.Tulis("  "); 단말.수(kepanjangan_VALUE[fail_sasaran]); 단말.Tulis("bait_VALUE(주기억 Fail)\n"); return 0; }
        if (Cari_direktori(정규길이) < 0) return -2;
        for (int 뒷값 = 1; 뒷값 < 16; 뒷값++) if (direktori_kepanjangan[뒷값] > 0) {
            int Mula_jawatan = pemasukan_Mula(direktori_nama, 뒷값 * 64, direktori_kepanjangan[뒷값]); if (Mula_jawatan < 0) continue;
            for (int Loop_INDEX = Mula_jawatan; Loop_INDEX < direktori_kepanjangan[뒷값]; Loop_INDEX++) Papan.직렬쓰기(direktori_nama[뒷값 * 64 + Loop_INDEX]); 단말.Tulis("/\n");
        }
        for (int fail_INDEX = 0; fail_INDEX < fail_COUNT; fail_INDEX++) if (이름길이[fail_INDEX] > 0) {
            int Mula_jawatan = pemasukan_Mula(Nama, fail_INDEX * 64, 이름길이[fail_INDEX]); if (Mula_jawatan < 0) continue;
            for (int Loop_INDEX = Mula_jawatan; Loop_INDEX < 이름길이[fail_INDEX]; Loop_INDEX++) Papan.직렬쓰기(Nama[fail_INDEX * 64 + Loop_INDEX]);
            단말.Tulis("  "); 단말.수(kepanjangan_VALUE[fail_INDEX]); 단말.Tulis("bait_VALUE(주기억 Fail)\n");
        }
        return 0;
    }
}
