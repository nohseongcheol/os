// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ଭାରତ.JIndOS.ଫାଇଲ୍_ସିଷ୍ଟମ୍;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** ELF32 little-endian ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ 파일의 머리부와 적재 구역을 검증한다. */
public final class 실행파일적재기 {
    public static final class ବିଭାଗ_ମୂଲ୍ୟ {
        private final int 종류;
        private final int ପତାକା_ମୂଲ୍ୟ;
        private final int ଠିକଣା;
        private final int ଫାଇଲ୍_ସ୍ଥିତି_2aa21a9a;
        private final int ଆକାର;

        ବିଭାଗ_ମୂଲ୍ୟ(int 종류, int ପତାକା_ମୂଲ୍ୟ, int ଠିକଣା, int ଫାଇଲ୍_ସ୍ଥିତି_2aa21a9a, int ଆକାର) {
            this.종류 = 종류;
            this.ପତାକା_ମୂଲ୍ୟ = ପତାକା_ମୂଲ୍ୟ;
            this.ଠିକଣା = ଠିକଣା;
            this.ଫାଇଲ୍_ସ୍ଥିତି_2aa21a9a = ଫାଇଲ୍_ସ୍ଥିତି_2aa21a9a;
            this.ଆକାର = ଆକାର;
        }

        public int 종류() {
            return 종류;
        }

        public int ପତାକା_ମୂଲ୍ୟ() {
            return ପତାକା_ମୂଲ୍ୟ;
        }

        public int ଠିକଣା() {
            return ଠିକଣା;
        }

        public int ଫାଇଲ୍_ସ୍ଥିତି_2aa21a9a() {
            return ଫାଇଲ୍_ସ୍ଥିତି_2aa21a9a;
        }

        public int ଆକାର() {
            return ଆକାର;
        }
    }

    public static final class ଚିତ୍ର {
        private final int ଆରମ୍ଭ_ଠିକଣା;
        private final List<ବିଭାଗ_ମୂଲ୍ୟ> 구역들;

        ଚିତ୍ର(int ଆରମ୍ଭ_ଠିକଣା, List<ବିଭାଗ_ମୂଲ୍ୟ> 구역들) {
            this.ଆରମ୍ଭ_ଠିକଣା = ଆରମ୍ଭ_ଠିକଣା;
            this.구역들 = Collections.unmodifiableList(구역들);
        }

        public int ଆରମ୍ଭ_ଠିକଣା() {
            return ଆରମ୍ଭ_ଠିକଣା;
        }

        public List<ବିଭାଗ_ମୂଲ୍ୟ> 구역들() {
            return 구역들;
        }
    }

    public ଚିତ୍ର 검사(byte[] ଡାଟା) {
        if (ଡାଟା == null || ଡାଟା.length < 52
                || ଡାଟା[0] != 0x7f || ଡାଟା[1] != 'E' || ଡାଟା[2] != 'L' || ଡାଟା[3] != 'F') {
            throw new IllegalArgumentException("ELF 마법값이 올바르지 않습니다.");
        }
        if (ଡାଟା[4] != 1 || ଡାଟା[5] != 1) {
            throw new IllegalArgumentException("ELF32 little-endian 형식이 아닙니다.");
        }
        int ଆରମ୍ଭ_ଠିକଣା = ପାର୍ସ_ଇଣ୍ଟିଜର(ଡାଟା, 24);
        int ବିଭାଗ_ସାରଣୀ_ସ୍ଥିତି = ପାର୍ସ_ଇଣ୍ଟିଜର(ଡାଟା, 32);
        int ବିଭାଗ_ଏଣ୍ଟ୍ରି_ଅକାର = 짧은정수읽기(ଡାଟା, 46);
        int 구역수 = 짧은정수읽기(ଡାଟା, 48);
        if (ବିଭାଗ_ଏଣ୍ଟ୍ରି_ଅକାର < 40 || ବିଭାଗ_ସାରଣୀ_ସ୍ଥିତି < 0
                || (long) ବିଭାଗ_ସାରଣୀ_ସ୍ଥିତି + (long) ବିଭାଗ_ଏଣ୍ଟ୍ରି_ଅକାର * 구역수 > ଡାଟା.length) {
            throw new IllegalArgumentException("ELF 구역표 범위가 올바르지 않습니다.");
        }
        List<ବିଭାଗ_ମୂଲ୍ୟ> 구역들 = new ArrayList<ବିଭାଗ_ମୂଲ୍ୟ>();
        for (int ଅନୁକ୍ରମଣିକା = 0; ଅନୁକ୍ରମଣିକା < 구역수; ଅନୁକ୍ରମଣିକା++) {
            int ଅବସ୍ଥାନ = ବିଭାଗ_ସାରଣୀ_ସ୍ଥିତି + ଅନୁକ୍ରମଣିକା * ବିଭାଗ_ଏଣ୍ଟ୍ରି_ଅକାର;
            int 종류 = ପାର୍ସ_ଇଣ୍ଟିଜର(ଡାଟା, ଅବସ୍ଥାନ + 4);
            int ପତାକା_ମୂଲ୍ୟ = ପାର୍ସ_ଇଣ୍ଟିଜର(ଡାଟା, ଅବସ୍ଥାନ + 8);
            int ଠିକଣା = ପାର୍ସ_ଇଣ୍ଟିଜର(ଡାଟା, ଅବସ୍ଥାନ + 12);
            int ଫାଇଲ୍_ସ୍ଥିତି_2aa21a9a = ପାର୍ସ_ଇଣ୍ଟିଜର(ଡାଟା, ଅବସ୍ଥାନ + 16);
            int ଆକାର = ପାର୍ସ_ଇଣ୍ଟିଜର(ଡାଟା, ଅବସ୍ଥାନ + 20);
            if (ଆକାର < 0 || (종류 != 8 && ((long) ଫାଇଲ୍_ସ୍ଥିତି_2aa21a9a + ଆକାର > ଡାଟା.length || ଫାଇଲ୍_ସ୍ଥିତି_2aa21a9a < 0))) {
                throw new IllegalArgumentException("ELF ବିଭାଗ_ମୂଲ୍ୟ ଡାଟା 범위가 올바르지 않습니다.");
            }
            구역들.add(new ବିଭାଗ_ମୂଲ୍ୟ(종류, ପତାକା_ମୂଲ୍ୟ, ଠିକଣା, ଫାଇଲ୍_ସ୍ଥିତି_2aa21a9a, ଆକାର));
        }
        return new ଚିତ୍ର(ଆରମ୍ଭ_ଠିକଣା, 구역들);
    }

    private int ପାର୍ସ_ଇଣ୍ଟିଜର(byte[] ଡାଟା, int ଅବସ୍ଥାନ) {
        if (ଅବସ୍ଥାନ < 0 || ଅବସ୍ଥାନ > ଡାଟା.length - 4) {
            throw new IllegalArgumentException("ELF ଇଣ୍ଟିଜର 범위를 벗어났습니다.");
        }
        return (ଡାଟା[ଅବସ୍ଥାନ] & 0xff)
                | ((ଡାଟା[ଅବସ୍ଥାନ + 1] & 0xff) << 8)
                | ((ଡାଟା[ଅବସ୍ଥାନ + 2] & 0xff) << 16)
                | ((ଡାଟା[ଅବସ୍ଥାନ + 3] & 0xff) << 24);
    }

    private int 짧은정수읽기(byte[] ଡାଟା, int ଅବସ୍ଥାନ) {
        if (ଅବସ୍ଥାନ < 0 || ଅବସ୍ଥାନ > ଡାଟା.length - 2) {
            throw new IllegalArgumentException("ELF 짧은 ଇଣ୍ଟିଜର 범위를 벗어났습니다.");
        }
        return (ଡାଟା[ଅବସ୍ଥାନ] & 0xff) | ((ଡାଟା[ଅବସ୍ଥାନ + 1] & 0xff) << 8);
    }
}
