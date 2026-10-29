// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Malaysia.JMysOS.sistem_fail;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** ELF32 little-endian laksanakan_perintah 파일의 머리부와 적재 구역을 검증한다. */
public final class 실행파일적재기 {
    public static final class seksyen_VALUE {
        private final int 종류;
        private final int bendera_VALUE;
        private final int e_mel;
        private final int fail_jawatan;
        private final int Saiz;

        seksyen_VALUE(int 종류, int bendera_VALUE, int e_mel, int fail_jawatan, int Saiz) {
            this.종류 = 종류;
            this.bendera_VALUE = bendera_VALUE;
            this.e_mel = e_mel;
            this.fail_jawatan = fail_jawatan;
            this.Saiz = Saiz;
        }

        public int 종류() {
            return 종류;
        }

        public int bendera_VALUE() {
            return bendera_VALUE;
        }

        public int e_mel() {
            return e_mel;
        }

        public int fail_jawatan() {
            return fail_jawatan;
        }

        public int Saiz() {
            return Saiz;
        }
    }

    public static final class imej {
        private final int alamat_mula;
        private final List<seksyen_VALUE> 구역들;

        imej(int alamat_mula, List<seksyen_VALUE> 구역들) {
            this.alamat_mula = alamat_mula;
            this.구역들 = Collections.unmodifiableList(구역들);
        }

        public int alamat_mula() {
            return alamat_mula;
        }

        public List<seksyen_VALUE> 구역들() {
            return 구역들;
        }
    }

    public imej 검사(byte[] data) {
        if (data == null || data.length < 52
                || data[0] != 0x7f || data[1] != 'E' || data[2] != 'L' || data[3] != 'F') {
            throw new IllegalArgumentException("ELF 마법값이 올바르지 않습니다.");
        }
        if (data[4] != 1 || data[5] != 1) {
            throw new IllegalArgumentException("ELF32 little-endian 형식이 아닙니다.");
        }
        int alamat_mula = hurai_integer(data, 24);
        int seksyen_jadual_jawatan = hurai_integer(data, 32);
        int seksyen_pemasukan_saiz = 짧은정수읽기(data, 46);
        int seksyen_COUNT = 짧은정수읽기(data, 48);
        if (seksyen_pemasukan_saiz < 40 || seksyen_jadual_jawatan < 0
                || (long) seksyen_jadual_jawatan + (long) seksyen_pemasukan_saiz * seksyen_COUNT > data.length) {
            throw new IllegalArgumentException("ELF 구역표 범위가 올바르지 않습니다.");
        }
        List<seksyen_VALUE> 구역들 = new ArrayList<seksyen_VALUE>();
        for (int INDEX = 0; INDEX < seksyen_COUNT; INDEX++) {
            int Kedudukan = seksyen_jadual_jawatan + INDEX * seksyen_pemasukan_saiz;
            int 종류 = hurai_integer(data, Kedudukan + 4);
            int bendera_VALUE = hurai_integer(data, Kedudukan + 8);
            int e_mel = hurai_integer(data, Kedudukan + 12);
            int fail_jawatan = hurai_integer(data, Kedudukan + 16);
            int Saiz = hurai_integer(data, Kedudukan + 20);
            if (Saiz < 0 || (종류 != 8 && ((long) fail_jawatan + Saiz > data.length || fail_jawatan < 0))) {
                throw new IllegalArgumentException("ELF seksyen_VALUE data 범위가 올바르지 않습니다.");
            }
            구역들.add(new seksyen_VALUE(종류, bendera_VALUE, e_mel, fail_jawatan, Saiz));
        }
        return new imej(alamat_mula, 구역들);
    }

    private int hurai_integer(byte[] data, int Kedudukan) {
        if (Kedudukan < 0 || Kedudukan > data.length - 4) {
            throw new IllegalArgumentException("ELF integer 범위를 벗어났습니다.");
        }
        return (data[Kedudukan] & 0xff)
                | ((data[Kedudukan + 1] & 0xff) << 8)
                | ((data[Kedudukan + 2] & 0xff) << 16)
                | ((data[Kedudukan + 3] & 0xff) << 24);
    }

    private int 짧은정수읽기(byte[] data, int Kedudukan) {
        if (Kedudukan < 0 || Kedudukan > data.length - 2) {
            throw new IllegalArgumentException("ELF 짧은 integer 범위를 벗어났습니다.");
        }
        return (data[Kedudukan] & 0xff) | ((data[Kedudukan + 1] & 0xff) << 8);
    }
}
