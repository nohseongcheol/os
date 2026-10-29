// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Owganystan.JAfgOS.faýl_ulgamy;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** ELF32 little-endian ýerine_ýetir_buýruk 파일의 머리부와 적재 구역을 검증한다. */
public final class 실행파일적재기 {
    public static final class bölüm_baha_366e0bfa {
        private final int 종류;
        private final int alamat_goý_baha;
        private final int salgy;
        private final int 파일위치;
        private final int Ululyk;

        bölüm_baha_366e0bfa(int 종류, int alamat_goý_baha, int salgy, int 파일위치, int Ululyk) {
            this.종류 = 종류;
            this.alamat_goý_baha = alamat_goý_baha;
            this.salgy = salgy;
            this.파일위치 = 파일위치;
            this.Ululyk = Ululyk;
        }

        public int 종류() {
            return 종류;
        }

        public int alamat_goý_baha() {
            return alamat_goý_baha;
        }

        public int salgy() {
            return salgy;
        }

        public int 파일위치() {
            return 파일위치;
        }

        public int Ululyk() {
            return Ululyk;
        }
    }

    public static final class surat {
        private final int başlat_salgy;
        private final List<bölüm_baha_366e0bfa> 구역들;

        surat(int başlat_salgy, List<bölüm_baha_366e0bfa> 구역들) {
            this.başlat_salgy = başlat_salgy;
            this.구역들 = Collections.unmodifiableList(구역들);
        }

        public int başlat_salgy() {
            return başlat_salgy;
        }

        public List<bölüm_baha_366e0bfa> 구역들() {
            return 구역들;
        }
    }

    public surat 검사(byte[] maglumat) {
        if (maglumat == null || maglumat.length < 52
                || maglumat[0] != 0x7f || maglumat[1] != 'E' || maglumat[2] != 'L' || maglumat[3] != 'F') {
            throw new IllegalArgumentException("ELF 마법값이 올바르지 않습니다.");
        }
        if (maglumat[4] != 1 || maglumat[5] != 1) {
            throw new IllegalArgumentException("ELF32 little-endian 형식이 아닙니다.");
        }
        int başlat_salgy = seljer_bitin(maglumat, 24);
        int 구역표위치 = seljer_bitin(maglumat, 32);
        int bölüm_girizmeklik_ölçegi_üýtget = 짧은정수읽기(maglumat, 46);
        int 구역수 = 짧은정수읽기(maglumat, 48);
        if (bölüm_girizmeklik_ölçegi_üýtget < 40 || 구역표위치 < 0
                || (long) 구역표위치 + (long) bölüm_girizmeklik_ölçegi_üýtget * 구역수 > maglumat.length) {
            throw new IllegalArgumentException("ELF 구역표 범위가 올바르지 않습니다.");
        }
        List<bölüm_baha_366e0bfa> 구역들 = new ArrayList<bölüm_baha_366e0bfa>();
        for (int indeks = 0; indeks < 구역수; indeks++) {
            int 위치 = 구역표위치 + indeks * bölüm_girizmeklik_ölçegi_üýtget;
            int 종류 = seljer_bitin(maglumat, 위치 + 4);
            int alamat_goý_baha = seljer_bitin(maglumat, 위치 + 8);
            int salgy = seljer_bitin(maglumat, 위치 + 12);
            int 파일위치 = seljer_bitin(maglumat, 위치 + 16);
            int Ululyk = seljer_bitin(maglumat, 위치 + 20);
            if (Ululyk < 0 || (종류 != 8 && ((long) 파일위치 + Ululyk > maglumat.length || 파일위치 < 0))) {
                throw new IllegalArgumentException("ELF bölüm_baha_366e0bfa maglumat 범위가 올바르지 않습니다.");
            }
            구역들.add(new bölüm_baha_366e0bfa(종류, alamat_goý_baha, salgy, 파일위치, Ululyk));
        }
        return new surat(başlat_salgy, 구역들);
    }

    private int seljer_bitin(byte[] maglumat, int 위치) {
        if (위치 < 0 || 위치 > maglumat.length - 4) {
            throw new IllegalArgumentException("ELF bitin 범위를 벗어났습니다.");
        }
        return (maglumat[위치] & 0xff)
                | ((maglumat[위치 + 1] & 0xff) << 8)
                | ((maglumat[위치 + 2] & 0xff) << 16)
                | ((maglumat[위치 + 3] & 0xff) << 24);
    }

    private int 짧은정수읽기(byte[] maglumat, int 위치) {
        if (위치 < 0 || 위치 > maglumat.length - 2) {
            throw new IllegalArgumentException("ELF 짧은 bitin 범위를 벗어났습니다.");
        }
        return (maglumat[위치] & 0xff) | ((maglumat[위치 + 1] & 0xff) << 8);
    }
}
