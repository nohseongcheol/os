// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Yr_Ariannin.JArgOS.system_ffeiliau;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** ELF32 little-endian Gweithredu_gorchymyn 파일의 머리부와 적재 구역을 검증한다. */
public final class 실행파일적재기 {
    public static final class adran_VALUE {
        private final int 종류;
        private final int fflag_VALUE;
        private final int ADDRESS;
        private final int ffeil_safle;
        private final int Maint;

        adran_VALUE(int 종류, int fflag_VALUE, int ADDRESS, int ffeil_safle, int Maint) {
            this.종류 = 종류;
            this.fflag_VALUE = fflag_VALUE;
            this.ADDRESS = ADDRESS;
            this.ffeil_safle = ffeil_safle;
            this.Maint = Maint;
        }

        public int 종류() {
            return 종류;
        }

        public int fflag_VALUE() {
            return fflag_VALUE;
        }

        public int ADDRESS() {
            return ADDRESS;
        }

        public int ffeil_safle() {
            return ffeil_safle;
        }

        public int Maint() {
            return Maint;
        }
    }

    public static final class llun {
        private final int cyfeiriad_cychwyn;
        private final List<adran_VALUE> 구역들;

        llun(int cyfeiriad_cychwyn, List<adran_VALUE> 구역들) {
            this.cyfeiriad_cychwyn = cyfeiriad_cychwyn;
            this.구역들 = Collections.unmodifiableList(구역들);
        }

        public int cyfeiriad_cychwyn() {
            return cyfeiriad_cychwyn;
        }

        public List<adran_VALUE> 구역들() {
            return 구역들;
        }
    }

    public llun 검사(byte[] data) {
        if (data == null || data.length < 52
                || data[0] != 0x7f || data[1] != 'E' || data[2] != 'L' || data[3] != 'F') {
            throw new IllegalArgumentException("ELF 마법값이 올바르지 않습니다.");
        }
        if (data[4] != 1 || data[5] != 1) {
            throw new IllegalArgumentException("ELF32 little-endian 형식이 아닙니다.");
        }
        int cyfeiriad_cychwyn = dosrannu_cyfanrif(data, 24);
        int adran_tabl_safle = dosrannu_cyfanrif(data, 32);
        int adran_cofnod_newid_maint = 짧은정수읽기(data, 46);
        int adran_COUNT = 짧은정수읽기(data, 48);
        if (adran_cofnod_newid_maint < 40 || adran_tabl_safle < 0
                || (long) adran_tabl_safle + (long) adran_cofnod_newid_maint * adran_COUNT > data.length) {
            throw new IllegalArgumentException("ELF 구역표 범위가 올바르지 않습니다.");
        }
        List<adran_VALUE> 구역들 = new ArrayList<adran_VALUE>();
        for (int INDEX = 0; INDEX < adran_COUNT; INDEX++) {
            int safle = adran_tabl_safle + INDEX * adran_cofnod_newid_maint;
            int 종류 = dosrannu_cyfanrif(data, safle + 4);
            int fflag_VALUE = dosrannu_cyfanrif(data, safle + 8);
            int ADDRESS = dosrannu_cyfanrif(data, safle + 12);
            int ffeil_safle = dosrannu_cyfanrif(data, safle + 16);
            int Maint = dosrannu_cyfanrif(data, safle + 20);
            if (Maint < 0 || (종류 != 8 && ((long) ffeil_safle + Maint > data.length || ffeil_safle < 0))) {
                throw new IllegalArgumentException("ELF adran_VALUE data 범위가 올바르지 않습니다.");
            }
            구역들.add(new adran_VALUE(종류, fflag_VALUE, ADDRESS, ffeil_safle, Maint));
        }
        return new llun(cyfeiriad_cychwyn, 구역들);
    }

    private int dosrannu_cyfanrif(byte[] data, int safle) {
        if (safle < 0 || safle > data.length - 4) {
            throw new IllegalArgumentException("ELF cyfanrif 범위를 벗어났습니다.");
        }
        return (data[safle] & 0xff)
                | ((data[safle + 1] & 0xff) << 8)
                | ((data[safle + 2] & 0xff) << 16)
                | ((data[safle + 3] & 0xff) << 24);
    }

    private int 짧은정수읽기(byte[] data, int safle) {
        if (safle < 0 || safle > data.length - 2) {
            throw new IllegalArgumentException("ELF 짧은 cyfanrif 범위를 벗어났습니다.");
        }
        return (data[safle] & 0xff) | ((data[safle + 1] & 0xff) << 8);
    }
}
