// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Republik_Indonesia.JIdnOS.sistem_berkas;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** ELF32 little-endian Jalankan_perintah 파일의 머리부와 적재 구역을 검증한다. */
public final class 실행파일적재기 {
    public static final class seksi_VALUE {
        private final int 종류;
        private final int bendera_VALUE;
        private final int surel;
        private final int file_posisi;
        private final int Ukuran;

        seksi_VALUE(int 종류, int bendera_VALUE, int surel, int file_posisi, int Ukuran) {
            this.종류 = 종류;
            this.bendera_VALUE = bendera_VALUE;
            this.surel = surel;
            this.file_posisi = file_posisi;
            this.Ukuran = Ukuran;
        }

        public int 종류() {
            return 종류;
        }

        public int bendera_VALUE() {
            return bendera_VALUE;
        }

        public int surel() {
            return surel;
        }

        public int file_posisi() {
            return file_posisi;
        }

        public int Ukuran() {
            return Ukuran;
        }
    }

    public static final class foto {
        private final int alamat_permulaan;
        private final List<seksi_VALUE> 구역들;

        foto(int alamat_permulaan, List<seksi_VALUE> 구역들) {
            this.alamat_permulaan = alamat_permulaan;
            this.구역들 = Collections.unmodifiableList(구역들);
        }

        public int alamat_permulaan() {
            return alamat_permulaan;
        }

        public List<seksi_VALUE> 구역들() {
            return 구역들;
        }
    }

    public foto 검사(byte[] data) {
        if (data == null || data.length < 52
                || data[0] != 0x7f || data[1] != 'E' || data[2] != 'L' || data[3] != 'F') {
            throw new IllegalArgumentException("ELF 마법값이 올바르지 않습니다.");
        }
        if (data[4] != 1 || data[5] != 1) {
            throw new IllegalArgumentException("ELF32 little-endian 형식이 아닙니다.");
        }
        int alamat_permulaan = urai_bilangan_bulat(data, 24);
        int seksi_tabel_posisi = urai_bilangan_bulat(data, 32);
        int seksi_entri_ukuran = 짧은정수읽기(data, 46);
        int seksi_COUNT = 짧은정수읽기(data, 48);
        if (seksi_entri_ukuran < 40 || seksi_tabel_posisi < 0
                || (long) seksi_tabel_posisi + (long) seksi_entri_ukuran * seksi_COUNT > data.length) {
            throw new IllegalArgumentException("ELF 구역표 범위가 올바르지 않습니다.");
        }
        List<seksi_VALUE> 구역들 = new ArrayList<seksi_VALUE>();
        for (int INDEX = 0; INDEX < seksi_COUNT; INDEX++) {
            int posisi = seksi_tabel_posisi + INDEX * seksi_entri_ukuran;
            int 종류 = urai_bilangan_bulat(data, posisi + 4);
            int bendera_VALUE = urai_bilangan_bulat(data, posisi + 8);
            int surel = urai_bilangan_bulat(data, posisi + 12);
            int file_posisi = urai_bilangan_bulat(data, posisi + 16);
            int Ukuran = urai_bilangan_bulat(data, posisi + 20);
            if (Ukuran < 0 || (종류 != 8 && ((long) file_posisi + Ukuran > data.length || file_posisi < 0))) {
                throw new IllegalArgumentException("ELF seksi_VALUE data 범위가 올바르지 않습니다.");
            }
            구역들.add(new seksi_VALUE(종류, bendera_VALUE, surel, file_posisi, Ukuran));
        }
        return new foto(alamat_permulaan, 구역들);
    }

    private int urai_bilangan_bulat(byte[] data, int posisi) {
        if (posisi < 0 || posisi > data.length - 4) {
            throw new IllegalArgumentException("ELF bilangan_bulat 범위를 벗어났습니다.");
        }
        return (data[posisi] & 0xff)
                | ((data[posisi + 1] & 0xff) << 8)
                | ((data[posisi + 2] & 0xff) << 16)
                | ((data[posisi + 3] & 0xff) << 24);
    }

    private int 짧은정수읽기(byte[] data, int posisi) {
        if (posisi < 0 || posisi > data.length - 2) {
            throw new IllegalArgumentException("ELF 짧은 bilangan_bulat 범위를 벗어났습니다.");
        }
        return (data[posisi] & 0xff) | ((data[posisi + 1] & 0xff) << 8);
    }
}
