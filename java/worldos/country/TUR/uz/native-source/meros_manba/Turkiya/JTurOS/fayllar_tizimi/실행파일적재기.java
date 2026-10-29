// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Turkiya.JTurOS.fayllar_tizimi;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** ELF32 little-endian bajarmoq_buyruq 파일의 머리부와 적재 구역을 검증한다. */
public final class 실행파일적재기 {
    public static final class bo_lim_VALUE_366e0bfa {
        private final int 종류;
        private final int bayroq_VALUE;
        private final int manzil;
        private final int fayl_holat_2aa21a9a;
        private final int Hajmi;

        bo_lim_VALUE_366e0bfa(int 종류, int bayroq_VALUE, int manzil, int fayl_holat_2aa21a9a, int Hajmi) {
            this.종류 = 종류;
            this.bayroq_VALUE = bayroq_VALUE;
            this.manzil = manzil;
            this.fayl_holat_2aa21a9a = fayl_holat_2aa21a9a;
            this.Hajmi = Hajmi;
        }

        public int 종류() {
            return 종류;
        }

        public int bayroq_VALUE() {
            return bayroq_VALUE;
        }

        public int manzil() {
            return manzil;
        }

        public int fayl_holat_2aa21a9a() {
            return fayl_holat_2aa21a9a;
        }

        public int Hajmi() {
            return Hajmi;
        }
    }

    public static final class rasm {
        private final int Start_manzil;
        private final List<bo_lim_VALUE_366e0bfa> 구역들;

        rasm(int Start_manzil, List<bo_lim_VALUE_366e0bfa> 구역들) {
            this.Start_manzil = Start_manzil;
            this.구역들 = Collections.unmodifiableList(구역들);
        }

        public int Start_manzil() {
            return Start_manzil;
        }

        public List<bo_lim_VALUE_366e0bfa> 구역들() {
            return 구역들;
        }
    }

    public rasm 검사(byte[] ma_lumotlar) {
        if (ma_lumotlar == null || ma_lumotlar.length < 52
                || ma_lumotlar[0] != 0x7f || ma_lumotlar[1] != 'E' || ma_lumotlar[2] != 'L' || ma_lumotlar[3] != 'F') {
            throw new IllegalArgumentException("ELF 마법값이 올바르지 않습니다.");
        }
        if (ma_lumotlar[4] != 1 || ma_lumotlar[5] != 1) {
            throw new IllegalArgumentException("ELF32 little-endian 형식이 아닙니다.");
        }
        int Start_manzil = tahlil_qilmoq_butun_son(ma_lumotlar, 24);
        int bo_lim_jadval_holat = tahlil_qilmoq_butun_son(ma_lumotlar, 32);
        int bo_lim_kiritish_o_lcham = 짧은정수읽기(ma_lumotlar, 46);
        int bo_lim_COUNT = 짧은정수읽기(ma_lumotlar, 48);
        if (bo_lim_kiritish_o_lcham < 40 || bo_lim_jadval_holat < 0
                || (long) bo_lim_jadval_holat + (long) bo_lim_kiritish_o_lcham * bo_lim_COUNT > ma_lumotlar.length) {
            throw new IllegalArgumentException("ELF 구역표 범위가 올바르지 않습니다.");
        }
        List<bo_lim_VALUE_366e0bfa> 구역들 = new ArrayList<bo_lim_VALUE_366e0bfa>();
        for (int INDEX = 0; INDEX < bo_lim_COUNT; INDEX++) {
            int Holati = bo_lim_jadval_holat + INDEX * bo_lim_kiritish_o_lcham;
            int 종류 = tahlil_qilmoq_butun_son(ma_lumotlar, Holati + 4);
            int bayroq_VALUE = tahlil_qilmoq_butun_son(ma_lumotlar, Holati + 8);
            int manzil = tahlil_qilmoq_butun_son(ma_lumotlar, Holati + 12);
            int fayl_holat_2aa21a9a = tahlil_qilmoq_butun_son(ma_lumotlar, Holati + 16);
            int Hajmi = tahlil_qilmoq_butun_son(ma_lumotlar, Holati + 20);
            if (Hajmi < 0 || (종류 != 8 && ((long) fayl_holat_2aa21a9a + Hajmi > ma_lumotlar.length || fayl_holat_2aa21a9a < 0))) {
                throw new IllegalArgumentException("ELF bo_lim_VALUE_366e0bfa ma_lumotlar 범위가 올바르지 않습니다.");
            }
            구역들.add(new bo_lim_VALUE_366e0bfa(종류, bayroq_VALUE, manzil, fayl_holat_2aa21a9a, Hajmi));
        }
        return new rasm(Start_manzil, 구역들);
    }

    private int tahlil_qilmoq_butun_son(byte[] ma_lumotlar, int Holati) {
        if (Holati < 0 || Holati > ma_lumotlar.length - 4) {
            throw new IllegalArgumentException("ELF butun_son 범위를 벗어났습니다.");
        }
        return (ma_lumotlar[Holati] & 0xff)
                | ((ma_lumotlar[Holati + 1] & 0xff) << 8)
                | ((ma_lumotlar[Holati + 2] & 0xff) << 16)
                | ((ma_lumotlar[Holati + 3] & 0xff) << 24);
    }

    private int 짧은정수읽기(byte[] ma_lumotlar, int Holati) {
        if (Holati < 0 || Holati > ma_lumotlar.length - 2) {
            throw new IllegalArgumentException("ELF 짧은 butun_son 범위를 벗어났습니다.");
        }
        return (ma_lumotlar[Holati] & 0xff) | ((ma_lumotlar[Holati + 1] & 0xff) << 8);
    }
}
