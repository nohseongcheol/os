// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package மலேசியா.JMysOS.கோப்பு_முறைமை;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** ELF32 little-endian இயக்கு_கட்டளை 파일의 머리부와 적재 구역을 검증한다. */
public final class 실행파일적재기 {
    public static final class பிரிவு_மதிப்பு {
        private final int 종류;
        private final int குறி_மதிப்பு;
        private final int முகவரி;
        private final int கோப்பு_நிலை_2aa21a9a;
        private final int அளவு;

        பிரிவு_மதிப்பு(int 종류, int குறி_மதிப்பு, int முகவரி, int கோப்பு_நிலை_2aa21a9a, int அளவு) {
            this.종류 = 종류;
            this.குறி_மதிப்பு = குறி_மதிப்பு;
            this.முகவரி = முகவரி;
            this.கோப்பு_நிலை_2aa21a9a = கோப்பு_நிலை_2aa21a9a;
            this.அளவு = அளவு;
        }

        public int 종류() {
            return 종류;
        }

        public int குறி_மதிப்பு() {
            return குறி_மதிப்பு;
        }

        public int முகவரி() {
            return முகவரி;
        }

        public int கோப்பு_நிலை_2aa21a9a() {
            return கோப்பு_நிலை_2aa21a9a;
        }

        public int அளவு() {
            return அளவு;
        }
    }

    public static final class படம் {
        private final int தொடங்கு_முகவரி;
        private final List<பிரிவு_மதிப்பு> 구역들;

        படம்(int தொடங்கு_முகவரி, List<பிரிவு_மதிப்பு> 구역들) {
            this.தொடங்கு_முகவரி = தொடங்கு_முகவரி;
            this.구역들 = Collections.unmodifiableList(구역들);
        }

        public int தொடங்கு_முகவரி() {
            return தொடங்கு_முகவரி;
        }

        public List<பிரிவு_மதிப்பு> 구역들() {
            return 구역들;
        }
    }

    public படம் 검사(byte[] தரவு) {
        if (தரவு == null || தரவு.length < 52
                || தரவு[0] != 0x7f || தரவு[1] != 'E' || தரவு[2] != 'L' || தரவு[3] != 'F') {
            throw new IllegalArgumentException("ELF 마법값이 올바르지 않습니다.");
        }
        if (தரவு[4] != 1 || தரவு[5] != 1) {
            throw new IllegalArgumentException("ELF32 little-endian 형식이 아닙니다.");
        }
        int தொடங்கு_முகவரி = அலகிடு_முழு_எண்(தரவு, 24);
        int பிரிவு_அட்டவணை_நிலை = அலகிடு_முழு_எண்(தரவு, 32);
        int பிரிவு_உள்ளீடு_அளவு = 짧은정수읽기(தரவு, 46);
        int 구역수 = 짧은정수읽기(தரவு, 48);
        if (பிரிவு_உள்ளீடு_அளவு < 40 || பிரிவு_அட்டவணை_நிலை < 0
                || (long) பிரிவு_அட்டவணை_நிலை + (long) பிரிவு_உள்ளீடு_அளவு * 구역수 > தரவு.length) {
            throw new IllegalArgumentException("ELF 구역표 범위가 올바르지 않습니다.");
        }
        List<பிரிவு_மதிப்பு> 구역들 = new ArrayList<பிரிவு_மதிப்பு>();
        for (int அடைவு = 0; அடைவு < 구역수; அடைவு++) {
            int இடம் = பிரிவு_அட்டவணை_நிலை + அடைவு * பிரிவு_உள்ளீடு_அளவு;
            int 종류 = அலகிடு_முழு_எண்(தரவு, இடம் + 4);
            int குறி_மதிப்பு = அலகிடு_முழு_எண்(தரவு, இடம் + 8);
            int முகவரி = அலகிடு_முழு_எண்(தரவு, இடம் + 12);
            int கோப்பு_நிலை_2aa21a9a = அலகிடு_முழு_எண்(தரவு, இடம் + 16);
            int அளவு = அலகிடு_முழு_எண்(தரவு, இடம் + 20);
            if (அளவு < 0 || (종류 != 8 && ((long) கோப்பு_நிலை_2aa21a9a + அளவு > தரவு.length || கோப்பு_நிலை_2aa21a9a < 0))) {
                throw new IllegalArgumentException("ELF பிரிவு_மதிப்பு தரவு 범위가 올바르지 않습니다.");
            }
            구역들.add(new பிரிவு_மதிப்பு(종류, குறி_மதிப்பு, முகவரி, கோப்பு_நிலை_2aa21a9a, அளவு));
        }
        return new படம்(தொடங்கு_முகவரி, 구역들);
    }

    private int அலகிடு_முழு_எண்(byte[] தரவு, int இடம்) {
        if (இடம் < 0 || இடம் > தரவு.length - 4) {
            throw new IllegalArgumentException("ELF முழு_எண் 범위를 벗어났습니다.");
        }
        return (தரவு[இடம்] & 0xff)
                | ((தரவு[இடம் + 1] & 0xff) << 8)
                | ((தரவு[இடம் + 2] & 0xff) << 16)
                | ((தரவு[இடம் + 3] & 0xff) << 24);
    }

    private int 짧은정수읽기(byte[] தரவு, int இடம்) {
        if (இடம் < 0 || இடம் > தரவு.length - 2) {
            throw new IllegalArgumentException("ELF 짧은 முழு_எண் 범위를 벗어났습니다.");
        }
        return (தரவு[இடம்] & 0xff) | ((தரவு[இடம் + 1] & 0xff) << 8);
    }
}
