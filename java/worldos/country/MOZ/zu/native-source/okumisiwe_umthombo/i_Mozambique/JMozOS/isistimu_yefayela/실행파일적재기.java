// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package i_Mozambique.JMozOS.isistimu_yefayela;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** ELF32 little-endian yenza_umyalo 파일의 머리부와 적재 구역을 검증한다. */
public final class 실행파일적재기 {
    public static final class isigaba_inani {
        private final int 종류;
        private final int iflegi_inani;
        private final int ikheli;
        private final int 파일위치;
        private final int Ubungako;

        isigaba_inani(int 종류, int iflegi_inani, int ikheli, int 파일위치, int Ubungako) {
            this.종류 = 종류;
            this.iflegi_inani = iflegi_inani;
            this.ikheli = ikheli;
            this.파일위치 = 파일위치;
            this.Ubungako = Ubungako;
        }

        public int 종류() {
            return 종류;
        }

        public int iflegi_inani() {
            return iflegi_inani;
        }

        public int ikheli() {
            return ikheli;
        }

        public int 파일위치() {
            return 파일위치;
        }

        public int Ubungako() {
            return Ubungako;
        }
    }

    public static final class isithombe {
        private final int qala_ikheli;
        private final List<isigaba_inani> 구역들;

        isithombe(int qala_ikheli, List<isigaba_inani> 구역들) {
            this.qala_ikheli = qala_ikheli;
            this.구역들 = Collections.unmodifiableList(구역들);
        }

        public int qala_ikheli() {
            return qala_ikheli;
        }

        public List<isigaba_inani> 구역들() {
            return 구역들;
        }
    }

    public isithombe 검사(byte[] imininingwane) {
        if (imininingwane == null || imininingwane.length < 52
                || imininingwane[0] != 0x7f || imininingwane[1] != 'E' || imininingwane[2] != 'L' || imininingwane[3] != 'F') {
            throw new IllegalArgumentException("ELF 마법값이 올바르지 않습니다.");
        }
        if (imininingwane[4] != 1 || imininingwane[5] != 1) {
            throw new IllegalArgumentException("ELF32 little-endian 형식이 아닙니다.");
        }
        int qala_ikheli = zawula_inamba(imininingwane, 24);
        int 구역표위치 = zawula_inamba(imininingwane, 32);
        int isigaba_okufakwayo_linganisa = 짧은정수읽기(imininingwane, 46);
        int 구역수 = 짧은정수읽기(imininingwane, 48);
        if (isigaba_okufakwayo_linganisa < 40 || 구역표위치 < 0
                || (long) 구역표위치 + (long) isigaba_okufakwayo_linganisa * 구역수 > imininingwane.length) {
            throw new IllegalArgumentException("ELF 구역표 범위가 올바르지 않습니다.");
        }
        List<isigaba_inani> 구역들 = new ArrayList<isigaba_inani>();
        for (int thola_inkomba = 0; thola_inkomba < 구역수; thola_inkomba++) {
            int 위치 = 구역표위치 + thola_inkomba * isigaba_okufakwayo_linganisa;
            int 종류 = zawula_inamba(imininingwane, 위치 + 4);
            int iflegi_inani = zawula_inamba(imininingwane, 위치 + 8);
            int ikheli = zawula_inamba(imininingwane, 위치 + 12);
            int 파일위치 = zawula_inamba(imininingwane, 위치 + 16);
            int Ubungako = zawula_inamba(imininingwane, 위치 + 20);
            if (Ubungako < 0 || (종류 != 8 && ((long) 파일위치 + Ubungako > imininingwane.length || 파일위치 < 0))) {
                throw new IllegalArgumentException("ELF isigaba_inani imininingwane 범위가 올바르지 않습니다.");
            }
            구역들.add(new isigaba_inani(종류, iflegi_inani, ikheli, 파일위치, Ubungako));
        }
        return new isithombe(qala_ikheli, 구역들);
    }

    private int zawula_inamba(byte[] imininingwane, int 위치) {
        if (위치 < 0 || 위치 > imininingwane.length - 4) {
            throw new IllegalArgumentException("ELF inamba 범위를 벗어났습니다.");
        }
        return (imininingwane[위치] & 0xff)
                | ((imininingwane[위치 + 1] & 0xff) << 8)
                | ((imininingwane[위치 + 2] & 0xff) << 16)
                | ((imininingwane[위치 + 3] & 0xff) << 24);
    }

    private int 짧은정수읽기(byte[] imininingwane, int 위치) {
        if (위치 < 0 || 위치 > imininingwane.length - 2) {
            throw new IllegalArgumentException("ELF 짧은 inamba 범위를 벗어났습니다.");
        }
        return (imininingwane[위치] & 0xff) | ((imininingwane[위치 + 1] & 0xff) << 8);
    }
}
