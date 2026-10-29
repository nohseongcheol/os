// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ভাৰত.JIndOS.ফাইল_ছিষ্টেম;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** ELF32 little-endian নিষ্পাদন_আদেশ 파일의 머리부와 적재 구역을 검증한다. */
public final class 실행파일적재기 {
    public static final class শাখা_মান_366e0bfa {
        private final int 종류;
        private final int পতাকা_মান;
        private final int ঠিকনা;
        private final int ফাইল_স্থান_সলনি_কৰক;
        private final int মাপ;

        শাখা_মান_366e0bfa(int 종류, int পতাকা_মান, int ঠিকনা, int ফাইল_স্থান_সলনি_কৰক, int মাপ) {
            this.종류 = 종류;
            this.পতাকা_মান = পতাকা_মান;
            this.ঠিকনা = ঠিকনা;
            this.ফাইল_স্থান_সলনি_কৰক = ফাইল_স্থান_সলনি_কৰক;
            this.মাপ = মাপ;
        }

        public int 종류() {
            return 종류;
        }

        public int পতাকা_মান() {
            return পতাকা_মান;
        }

        public int ঠিকনা() {
            return ঠিকনা;
        }

        public int ফাইল_স্থান_সলনি_কৰক() {
            return ফাইল_স্থান_সলনি_কৰক;
        }

        public int মাপ() {
            return মাপ;
        }
    }

    public static final class ছবি {
        private final int আৰম্ভ_ঠিকনা;
        private final List<শাখা_মান_366e0bfa> 구역들;

        ছবি(int আৰম্ভ_ঠিকনা, List<শাখা_মান_366e0bfa> 구역들) {
            this.আৰম্ভ_ঠিকনা = আৰম্ভ_ঠিকনা;
            this.구역들 = Collections.unmodifiableList(구역들);
        }

        public int আৰম্ভ_ঠিকনা() {
            return আৰম্ভ_ঠিকনা;
        }

        public List<শাখা_মান_366e0bfa> 구역들() {
            return 구역들;
        }
    }

    public ছবি 검사(byte[] ডাটা) {
        if (ডাটা == null || ডাটা.length < 52
                || ডাটা[0] != 0x7f || ডাটা[1] != 'E' || ডাটা[2] != 'L' || ডাটা[3] != 'F') {
            throw new IllegalArgumentException("ELF 마법값이 올바르지 않습니다.");
        }
        if (ডাটা[4] != 1 || ডাটা[5] != 1) {
            throw new IllegalArgumentException("ELF32 little-endian 형식이 아닙니다.");
        }
        int আৰম্ভ_ঠিকনা = পাৰ্ছ_কৰক_পূর্ণ_সংখ্যা(ডাটা, 24);
        int শাখা_তালিকা_স্থান_সলনি_কৰক = পাৰ্ছ_কৰক_পূর্ণ_সংখ্যা(ডাটা, 32);
        int শাখা_প্রবিষ্ট_আকাৰ_কৰক = 짧은정수읽기(ডাটা, 46);
        int 구역수 = 짧은정수읽기(ডাটা, 48);
        if (শাখা_প্রবিষ্ট_আকাৰ_কৰক < 40 || শাখা_তালিকা_স্থান_সলনি_কৰক < 0
                || (long) শাখা_তালিকা_স্থান_সলনি_কৰক + (long) শাখা_প্রবিষ্ট_আকাৰ_কৰক * 구역수 > ডাটা.length) {
            throw new IllegalArgumentException("ELF 구역표 범위가 올바르지 않습니다.");
        }
        List<শাখা_মান_366e0bfa> 구역들 = new ArrayList<শাখা_মান_366e0bfa>();
        for (int ইনডেক্স = 0; ইনডেক্স < 구역수; ইনডেক্স++) {
            int অৱস্থান = শাখা_তালিকা_স্থান_সলনি_কৰক + ইনডেক্স * শাখা_প্রবিষ্ট_আকাৰ_কৰক;
            int 종류 = পাৰ্ছ_কৰক_পূর্ণ_সংখ্যা(ডাটা, অৱস্থান + 4);
            int পতাকা_মান = পাৰ্ছ_কৰক_পূর্ণ_সংখ্যা(ডাটা, অৱস্থান + 8);
            int ঠিকনা = পাৰ্ছ_কৰক_পূর্ণ_সংখ্যা(ডাটা, অৱস্থান + 12);
            int ফাইল_স্থান_সলনি_কৰক = পাৰ্ছ_কৰক_পূর্ণ_সংখ্যা(ডাটা, অৱস্থান + 16);
            int মাপ = পাৰ্ছ_কৰক_পূর্ণ_সংখ্যা(ডাটা, অৱস্থান + 20);
            if (মাপ < 0 || (종류 != 8 && ((long) ফাইল_স্থান_সলনি_কৰক + মাপ > ডাটা.length || ফাইল_স্থান_সলনি_কৰক < 0))) {
                throw new IllegalArgumentException("ELF শাখা_মান_366e0bfa ডাটা 범위가 올바르지 않습니다.");
            }
            구역들.add(new শাখা_মান_366e0bfa(종류, পতাকা_মান, ঠিকনা, ফাইল_স্থান_সলনি_কৰক, মাপ));
        }
        return new ছবি(আৰম্ভ_ঠিকনা, 구역들);
    }

    private int পাৰ্ছ_কৰক_পূর্ণ_সংখ্যা(byte[] ডাটা, int অৱস্থান) {
        if (অৱস্থান < 0 || অৱস্থান > ডাটা.length - 4) {
            throw new IllegalArgumentException("ELF পূর্ণ_সংখ্যা 범위를 벗어났습니다.");
        }
        return (ডাটা[অৱস্থান] & 0xff)
                | ((ডাটা[অৱস্থান + 1] & 0xff) << 8)
                | ((ডাটা[অৱস্থান + 2] & 0xff) << 16)
                | ((ডাটা[অৱস্থান + 3] & 0xff) << 24);
    }

    private int 짧은정수읽기(byte[] ডাটা, int অৱস্থান) {
        if (অৱস্থান < 0 || অৱস্থান > ডাটা.length - 2) {
            throw new IllegalArgumentException("ELF 짧은 পূর্ণ_সংখ্যা 범위를 벗어났습니다.");
        }
        return (ডাটা[অৱস্থান] & 0xff) | ((ডাটা[অৱস্থান + 1] & 0xff) << 8);
    }
}
