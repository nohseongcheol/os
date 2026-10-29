// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 검사합과 두 보존본을 사용하는 작은 전용 stor_VALUE format_VALUE. fsync/sync에서만 영구 반영한다. */
public final class 파일보존 {
    static int 현재보존본 = -1, 세대번호 = 0;
    static int[] fail_jadual = new int[1024];
    static int 바이트해시(int VALUE, int data) { return (VALUE ^ data) * 16777619; }
    static void buang_data() {
        for (int INDEX = 0; INDEX < 512; INDEX++) Storan_peranti_hubungan.seksyen_data[INDEX] = 0;
    }
    static int jadual_integer(int Kedudukan) {
        return fail_jadual[Kedudukan] | fail_jadual[Kedudukan + 1] << 8 | fail_jadual[Kedudukan + 2] << 16 | fail_jadual[Kedudukan + 3] << 24;
    }
    static void tulis_jadual_integer(int Kedudukan, int VALUE) {
        for (int INDEX = 0; INDEX < 4; INDEX++) fail_jadual[Kedudukan + INDEX] = (VALUE >>> (INDEX * 8)) & 255;
    }
    static boolean cek_jadual() {
        for (int Fail = 0; Fail < 8; Fail++) {
            int kepanjangan_VALUE = 0;
            for (int 칸 = 0; 칸 < 64; 칸++) Memori_sistem_fail.Nama[칸] = fail_jadual[Fail * 72 + 칸];
            while (kepanjangan_VALUE < 64 && Memori_sistem_fail.Nama[kepanjangan_VALUE] != 0) kepanjangan_VALUE++;
            if (kepanjangan_VALUE == 0) continue;
            if (!Memori_sistem_fail.cek_nama(Memori_sistem_fail.Nama, kepanjangan_VALUE)
                || jadual_integer(Fail * 72 + 64) < 0 || jadual_integer(Fail * 72 + 64) > 16384) return false;
            for (int hadapan_VALUE = 0; hadapan_VALUE < Fail; hadapan_VALUE++) {
                boolean 같음 = fail_jadual[hadapan_VALUE * 72 + kepanjangan_VALUE] == 0;
                for (int 칸 = 0; 칸 < kepanjangan_VALUE; 칸++) if (fail_jadual[hadapan_VALUE * 72 + 칸] != Memori_sistem_fail.Nama[칸]) 같음 = false;
                if (같음) return false;
            }
        }
        return true;
    }
    static int 보존본검사(int 보존본) {
        int Mula_seksyen = 1 + 보존본 * 259;
        if (Storan_peranti_hubungan.Baca(Mula_seksyen) < 0 || Storan_peranti_hubungan.hurai_integer(0) != 0x4a4b534e) return -1;
        int 세대 = Storan_peranti_hubungan.hurai_integer(4), hasil_tambah_semak = Storan_peranti_hubungan.hurai_integer(8);
        if (세대 < 1 || Storan_peranti_hubungan.hurai_integer(12) != (세대 ^ hasil_tambah_semak ^ 0x4a4b534e)) return -1;
        int cincangan_fail = 0x811c9dc5;
        for (int seksyen_VALUE = 0; seksyen_VALUE < 258; seksyen_VALUE++) {
            if (Storan_peranti_hubungan.Baca(Mula_seksyen + 1 + seksyen_VALUE) < 0) return -1;
            for (int 칸 = 0; 칸 < 512; 칸++) {
                int VALUE = Storan_peranti_hubungan.seksyen_data[칸];
                cincangan_fail = 바이트해시(cincangan_fail, VALUE);
                if (seksyen_VALUE < 2) fail_jadual[seksyen_VALUE * 512 + 칸] = VALUE;
            }
        }
        return cincangan_fail == hasil_tambah_semak && cek_jadual() ? 세대 : -1;
    }
    static int Muatan(int 보존본) {
        int Mula_seksyen = 1 + 보존본 * 259;
        for (int seksyen_VALUE = 0; seksyen_VALUE < 2; seksyen_VALUE++) {
            if (Storan_peranti_hubungan.Baca(Mula_seksyen + 1 + seksyen_VALUE) < 0) return -5;
            for (int 칸 = 0; 칸 < 512; 칸++) fail_jadual[seksyen_VALUE * 512 + 칸] = Storan_peranti_hubungan.seksyen_data[칸];
        }
        for (int Fail = 0; Fail < 8; Fail++) {
            for (int 칸 = 0; 칸 < 64; 칸++) Memori_sistem_fail.이름들[Fail * 64 + 칸] = fail_jadual[Fail * 72 + 칸];
            Memori_sistem_fail.saiz_Senarai[Fail] = fail_jadual[Fail * 72] == 0 ? 0 : jadual_integer(Fail * 72 + 64);
            Memori_sistem_fail.허가들[Fail] = jadual_integer(Fail * 72 + 68) & 511;
            for (int seksyen_VALUE = 0; seksyen_VALUE < 32; seksyen_VALUE++) {
                if (Storan_peranti_hubungan.Baca(Mula_seksyen + 3 + Fail * 32 + seksyen_VALUE) < 0) return -5;
                int e_mel = peranti_VALUE.fail_Memori() + Fail * 16384 + seksyen_VALUE * 512;
                for (int 칸 = 0; 칸 < 512; 칸++) peranti_VALUE.tulis_Memori(e_mel + 칸, Storan_peranti_hubungan.seksyen_data[칸]);
            }
        }
        return 0;
    }
    static void Sediakan() {
        if (Storan_peranti_hubungan.Baca(0) < 0 || Storan_peranti_hubungan.hurai_integer(0) != 0x54534b4a
            || Storan_peranti_hubungan.hurai_integer(4) != 0x3145524f || Storan_peranti_hubungan.hurai_integer(8) != 2048
            || Storan_peranti_hubungan.hurai_integer(12) != 0x3153464a) {
            SMS_Terminal.Tulis("STORE RAM only (no JKSTORE1 disk)\n"); return;
        }
        Storan_peranti_hubungan.teknologi_maklumat_Ada_9e72441a = true;
        int 첫째 = 보존본검사(0), 둘째 = 보존본검사(1);
        if (첫째 < 0 && 둘째 < 0) { SMS_Terminal.Tulis("STORE ready; no valid snapshot\n"); return; }
        현재보존본 = 첫째 >= 둘째 ? 0 : 1; 세대번호 = 첫째 >= 둘째 ? 첫째 : 둘째;
        if (Muatan(현재보존본) < 0) {
            SMS_Terminal.Tulis("STORE read failed; halted to preserve files\n"); peranti_VALUE.정지();
        }
        SMS_Terminal.Tulis("STORE restored generation "); SMS_Terminal.수쓰기(세대번호); SMS_Terminal.문자(10);
    }
    static int segerak() {
        if (!Storan_peranti_hubungan.teknologi_maklumat_Ada_9e72441a) return -19;
        if (세대번호 == 2147483647) return -75;
        int Seterusnya_item = 현재보존본 == 0 ? 1 : 0, Mula_seksyen = 1 + Seterusnya_item * 259;
        // 새 본문보다 먼저 이전 commit을 무효화하고 peranti_VALUE 캐시를 비운다.
        buang_data();
        if (Storan_peranti_hubungan.Tulis(Mula_seksyen) < 0 || Storan_peranti_hubungan.밀어쓰기() < 0) return -5;
        for (int 칸 = 0; 칸 < 1024; 칸++) fail_jadual[칸] = 0;
        for (int Fail = 0; Fail < 8; Fail++) if (Memori_sistem_fail.이름들[Fail * 64] != 0) {
            for (int 칸 = 0; 칸 < 64; 칸++) fail_jadual[Fail * 72 + 칸] = Memori_sistem_fail.이름들[Fail * 64 + 칸];
            tulis_jadual_integer(Fail * 72 + 64, Memori_sistem_fail.saiz_Senarai[Fail]);
            tulis_jadual_integer(Fail * 72 + 68, Memori_sistem_fail.허가들[Fail]);
        }
        int cincangan_fail = 0x811c9dc5;
        for (int seksyen_VALUE = 0; seksyen_VALUE < 258; seksyen_VALUE++) {
            for (int 칸 = 0; 칸 < 512; 칸++) {
                int VALUE = 0;
                if (seksyen_VALUE < 2) VALUE = fail_jadual[seksyen_VALUE * 512 + 칸];
                else {
                    int Fail = (seksyen_VALUE - 2) / 32, Kedudukan = (seksyen_VALUE - 2) % 32 * 512 + 칸;
                    if (fail_jadual[Fail * 72] != 0 && Kedudukan < Memori_sistem_fail.saiz_Senarai[Fail])
                        VALUE = peranti_VALUE.기억읽기(peranti_VALUE.fail_Memori() + Fail * 16384 + Kedudukan);
                }
                Storan_peranti_hubungan.seksyen_data[칸] = VALUE; cincangan_fail = 바이트해시(cincangan_fail, VALUE);
            }
            if (Storan_peranti_hubungan.Tulis(Mula_seksyen + 1 + seksyen_VALUE) < 0) return -5;
        }
        if (Storan_peranti_hubungan.밀어쓰기() < 0) return -5;
        buang_data(); Storan_peranti_hubungan.tulis_integer_VALUE(0, 0x4a4b534e);
        Storan_peranti_hubungan.tulis_integer_VALUE(4, 세대번호 + 1); Storan_peranti_hubungan.tulis_integer_VALUE(8, cincangan_fail);
        Storan_peranti_hubungan.tulis_integer_VALUE(12, (세대번호 + 1) ^ cincangan_fail ^ 0x4a4b534e);
        if (Storan_peranti_hubungan.Tulis(Mula_seksyen) < 0 || Storan_peranti_hubungan.밀어쓰기() < 0) return -5;
        현재보존본 = Seterusnya_item; 세대번호++;
        return 0;
    }
}
