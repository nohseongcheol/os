// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ভারত.JIndOS.ফাইল_পদ্ধতি;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** ELF32 little-endian কার্যকর_করুন_আদেশ 파일의 머리부와 적재 구역을 검증한다. */
public final class 실행파일적재기 {
    public static final class শাখা_মান_366e0bfa {
        private final int 종류;
        private final int নিশান_মান;
        private final int ইমেইল;
        private final int ফাইল_পদ;
        private final int আকার;

        শাখা_মান_366e0bfa(int 종류, int নিশান_মান, int ইমেইল, int ফাইল_পদ, int আকার) {
            this.종류 = 종류;
            this.নিশান_মান = নিশান_মান;
            this.ইমেইল = ইমেইল;
            this.ফাইল_পদ = ফাইল_পদ;
            this.আকার = আকার;
        }

        public int 종류() {
            return 종류;
        }

        public int নিশান_মান() {
            return নিশান_মান;
        }

        public int ইমেইল() {
            return ইমেইল;
        }

        public int ফাইল_পদ() {
            return ফাইল_পদ;
        }

        public int আকার() {
            return আকার;
        }
    }

    public static final class ছবি {
        private final int শুরু_ইমেইল;
        private final List<শাখা_মান_366e0bfa> 구역들;

        ছবি(int শুরু_ইমেইল, List<শাখা_মান_366e0bfa> 구역들) {
            this.শুরু_ইমেইল = শুরু_ইমেইল;
            this.구역들 = Collections.unmodifiableList(구역들);
        }

        public int শুরু_ইমেইল() {
            return শুরু_ইমেইল;
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
        int শুরু_ইমেইল = বিভাজন_করা_পূর্ণসংখ্যা(ডাটা, 24);
        int শাখা_সারণি_পদ = বিভাজন_করা_পূর্ণসংখ্যা(ডাটা, 32);
        int শাখা_ভুক্তি_আয়তন = 짧은정수읽기(ডাটা, 46);
        int 구역수 = 짧은정수읽기(ডাটা, 48);
        if (শাখা_ভুক্তি_আয়তন < 40 || শাখা_সারণি_পদ < 0
                || (long) শাখা_সারণি_পদ + (long) শাখা_ভুক্তি_আয়তন * 구역수 > ডাটা.length) {
            throw new IllegalArgumentException("ELF 구역표 범위가 올바르지 않습니다.");
        }
        List<শাখা_মান_366e0bfa> 구역들 = new ArrayList<শাখা_মান_366e0bfa>();
        for (int সূচি = 0; সূচি < 구역수; সূচি++) {
            int অবস্থান = শাখা_সারণি_পদ + সূচি * শাখা_ভুক্তি_আয়তন;
            int 종류 = বিভাজন_করা_পূর্ণসংখ্যা(ডাটা, অবস্থান + 4);
            int নিশান_মান = বিভাজন_করা_পূর্ণসংখ্যা(ডাটা, অবস্থান + 8);
            int ইমেইল = বিভাজন_করা_পূর্ণসংখ্যা(ডাটা, অবস্থান + 12);
            int ফাইল_পদ = বিভাজন_করা_পূর্ণসংখ্যা(ডাটা, অবস্থান + 16);
            int আকার = বিভাজন_করা_পূর্ণসংখ্যা(ডাটা, অবস্থান + 20);
            if (আকার < 0 || (종류 != 8 && ((long) ফাইল_পদ + আকার > ডাটা.length || ফাইল_পদ < 0))) {
                throw new IllegalArgumentException("ELF শাখা_মান_366e0bfa ডাটা 범위가 올바르지 않습니다.");
            }
            구역들.add(new শাখা_মান_366e0bfa(종류, নিশান_মান, ইমেইল, ফাইল_পদ, আকার));
        }
        return new ছবি(শুরু_ইমেইল, 구역들);
    }

    private int বিভাজন_করা_পূর্ণসংখ্যা(byte[] ডাটা, int অবস্থান) {
        if (অবস্থান < 0 || অবস্থান > ডাটা.length - 4) {
            throw new IllegalArgumentException("ELF পূর্ণসংখ্যা 범위를 벗어났습니다.");
        }
        return (ডাটা[অবস্থান] & 0xff)
                | ((ডাটা[অবস্থান + 1] & 0xff) << 8)
                | ((ডাটা[অবস্থান + 2] & 0xff) << 16)
                | ((ডাটা[অবস্থান + 3] & 0xff) << 24);
    }

    private int 짧은정수읽기(byte[] ডাটা, int অবস্থান) {
        if (অবস্থান < 0 || অবস্থান > ডাটা.length - 2) {
            throw new IllegalArgumentException("ELF 짧은 পূর্ণসংখ্যা 범위를 벗어났습니다.");
        }
        return (ডাটা[অবস্থান] & 0xff) | ((ডাটা[অবস্থান + 1] & 0xff) << 8);
    }
}
