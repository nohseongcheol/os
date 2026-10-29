// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Mooritani.JMrtOS.barabu_boolebdenc_yu_ñu_bennal;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** ELF32 little-endian def_ndigel 파일의 머리부와 적재 구역을 검증한다. */
public final class 실행파일적재기 {
    public static final class dog_xëyma {
        private final int 종류;
        private final int tektalukaay_xëyma;
        private final int dëkkuwaay;
        private final int 파일위치;
        private final int tolluwaay;

        dog_xëyma(int 종류, int tektalukaay_xëyma, int dëkkuwaay, int 파일위치, int tolluwaay) {
            this.종류 = 종류;
            this.tektalukaay_xëyma = tektalukaay_xëyma;
            this.dëkkuwaay = dëkkuwaay;
            this.파일위치 = 파일위치;
            this.tolluwaay = tolluwaay;
        }

        public int 종류() {
            return 종류;
        }

        public int tektalukaay_xëyma() {
            return tektalukaay_xëyma;
        }

        public int dëkkuwaay() {
            return dëkkuwaay;
        }

        public int 파일위치() {
            return 파일위치;
        }

        public int tolluwaay() {
            return tolluwaay;
        }
    }

    public static final class nataal {
        private final int Door_dëkkuwaay;
        private final List<dog_xëyma> 구역들;

        nataal(int Door_dëkkuwaay, List<dog_xëyma> 구역들) {
            this.Door_dëkkuwaay = Door_dëkkuwaay;
            this.구역들 = Collections.unmodifiableList(구역들);
        }

        public int Door_dëkkuwaay() {
            return Door_dëkkuwaay;
        }

        public List<dog_xëyma> 구역들() {
            return 구역들;
        }
    }

    public nataal 검사(byte[] mbir) {
        if (mbir == null || mbir.length < 52
                || mbir[0] != 0x7f || mbir[1] != 'E' || mbir[2] != 'L' || mbir[3] != 'F') {
            throw new IllegalArgumentException("ELF 마법값이 올바르지 않습니다.");
        }
        if (mbir[4] != 1 || mbir[5] != 1) {
            throw new IllegalArgumentException("ELF32 little-endian 형식이 아닙니다.");
        }
        int Door_dëkkuwaay = Segg_lëmm(mbir, 24);
        int 구역표위치 = Segg_lëmm(mbir, 32);
        int dog_dugal_xabaar_tolluwaay = 짧은정수읽기(mbir, 46);
        int 구역수 = 짧은정수읽기(mbir, 48);
        if (dog_dugal_xabaar_tolluwaay < 40 || 구역표위치 < 0
                || (long) 구역표위치 + (long) dog_dugal_xabaar_tolluwaay * 구역수 > mbir.length) {
            throw new IllegalArgumentException("ELF 구역표 범위가 올바르지 않습니다.");
        }
        List<dog_xëyma> 구역들 = new ArrayList<dog_xëyma>();
        for (int àlluwa_tur = 0; àlluwa_tur < 구역수; àlluwa_tur++) {
            int 위치 = 구역표위치 + àlluwa_tur * dog_dugal_xabaar_tolluwaay;
            int 종류 = Segg_lëmm(mbir, 위치 + 4);
            int tektalukaay_xëyma = Segg_lëmm(mbir, 위치 + 8);
            int dëkkuwaay = Segg_lëmm(mbir, 위치 + 12);
            int 파일위치 = Segg_lëmm(mbir, 위치 + 16);
            int tolluwaay = Segg_lëmm(mbir, 위치 + 20);
            if (tolluwaay < 0 || (종류 != 8 && ((long) 파일위치 + tolluwaay > mbir.length || 파일위치 < 0))) {
                throw new IllegalArgumentException("ELF dog_xëyma mbir 범위가 올바르지 않습니다.");
            }
            구역들.add(new dog_xëyma(종류, tektalukaay_xëyma, dëkkuwaay, 파일위치, tolluwaay));
        }
        return new nataal(Door_dëkkuwaay, 구역들);
    }

    private int Segg_lëmm(byte[] mbir, int 위치) {
        if (위치 < 0 || 위치 > mbir.length - 4) {
            throw new IllegalArgumentException("ELF lëmm 범위를 벗어났습니다.");
        }
        return (mbir[위치] & 0xff)
                | ((mbir[위치 + 1] & 0xff) << 8)
                | ((mbir[위치 + 2] & 0xff) << 16)
                | ((mbir[위치 + 3] & 0xff) << 24);
    }

    private int 짧은정수읽기(byte[] mbir, int 위치) {
        if (위치 < 0 || 위치 > mbir.length - 2) {
            throw new IllegalArgumentException("ELF 짧은 lëmm 범위를 벗어났습니다.");
        }
        return (mbir[위치] & 0xff) | ((mbir[위치 + 1] & 0xff) << 8);
    }
}
