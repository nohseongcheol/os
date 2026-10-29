// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package عێراق.JIrqOS.سیستمی_فایل;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** ELF32 little-endian جێبەجێکردن_فەرمان 파일의 머리부와 적재 구역을 검증한다. */
public final class 실행파일적재기 {
    public static final class بەش_نرخ {
        private final int 종류;
        private final int نیشان_نرخ_58846146;
        private final int ناونیشان;
        private final int 파일위치;
        private final int گۆڕینی_ئەندازە;

        بەش_نرخ(int 종류, int نیشان_نرخ_58846146, int ناونیشان, int 파일위치, int گۆڕینی_ئەندازە) {
            this.종류 = 종류;
            this.نیشان_نرخ_58846146 = نیشان_نرخ_58846146;
            this.ناونیشان = ناونیشان;
            this.파일위치 = 파일위치;
            this.گۆڕینی_ئەندازە = گۆڕینی_ئەندازە;
        }

        public int 종류() {
            return 종류;
        }

        public int نیشان_نرخ_58846146() {
            return نیشان_نرخ_58846146;
        }

        public int ناونیشان() {
            return ناونیشان;
        }

        public int 파일위치() {
            return 파일위치;
        }

        public int گۆڕینی_ئەندازە() {
            return گۆڕینی_ئەندازە;
        }
    }

    public static final class وێنە {
        private final int دەستپێك_ناونیشان;
        private final List<بەش_نرخ> 구역들;

        وێنە(int دەستپێك_ناونیشان, List<بەش_نرخ> 구역들) {
            this.دەستپێك_ناونیشان = دەستپێك_ناونیشان;
            this.구역들 = Collections.unmodifiableList(구역들);
        }

        public int دەستپێك_ناونیشان() {
            return دەستپێك_ناونیشان;
        }

        public List<بەش_نرخ> 구역들() {
            return 구역들;
        }
    }

    public وێنە 검사(byte[] دەیتا) {
        if (دەیتا == null || دەیتا.length < 52
                || دەیتا[0] != 0x7f || دەیتا[1] != 'E' || دەیتا[2] != 'L' || دەیتا[3] != 'F') {
            throw new IllegalArgumentException("ELF 마법값이 올바르지 않습니다.");
        }
        if (دەیتا[4] != 1 || دەیتا[5] != 1) {
            throw new IllegalArgumentException("ELF32 little-endian 형식이 아닙니다.");
        }
        int دەستپێك_ناونیشان = 정수읽기(دەیتا, 24);
        int 구역표위치 = 정수읽기(دەیتا, 32);
        int بەش_تێنووسین_گۆڕینی_ئەندازە = 짧은정수읽기(دەیتا, 46);
        int 구역수 = 짧은정수읽기(دەیتا, 48);
        if (بەش_تێنووسین_گۆڕینی_ئەندازە < 40 || 구역표위치 < 0
                || (long) 구역표위치 + (long) بەش_تێنووسین_گۆڕینی_ئەندازە * 구역수 > دەیتا.length) {
            throw new IllegalArgumentException("ELF 구역표 범위가 올바르지 않습니다.");
        }
        List<بەش_نرخ> 구역들 = new ArrayList<بەش_نرخ>();
        for (int پێرست = 0; پێرست < 구역수; پێرست++) {
            int 위치 = 구역표위치 + پێرست * بەش_تێنووسین_گۆڕینی_ئەندازە;
            int 종류 = 정수읽기(دەیتا, 위치 + 4);
            int نیشان_نرخ_58846146 = 정수읽기(دەیتا, 위치 + 8);
            int ناونیشان = 정수읽기(دەیتا, 위치 + 12);
            int 파일위치 = 정수읽기(دەیتا, 위치 + 16);
            int گۆڕینی_ئەندازە = 정수읽기(دەیتا, 위치 + 20);
            if (گۆڕینی_ئەندازە < 0 || (종류 != 8 && ((long) 파일위치 + گۆڕینی_ئەندازە > دەیتا.length || 파일위치 < 0))) {
                throw new IllegalArgumentException("ELF بەش_نرخ دەیتا 범위가 올바르지 않습니다.");
            }
            구역들.add(new بەش_نرخ(종류, نیشان_نرخ_58846146, ناونیشان, 파일위치, گۆڕینی_ئەندازە));
        }
        return new وێنە(دەستپێك_ناونیشان, 구역들);
    }

    private int 정수읽기(byte[] دەیتا, int 위치) {
        if (위치 < 0 || 위치 > دەیتا.length - 4) {
            throw new IllegalArgumentException("ELF ژمارەی_سروشتی 범위를 벗어났습니다.");
        }
        return (دەیتا[위치] & 0xff)
                | ((دەیتا[위치 + 1] & 0xff) << 8)
                | ((دەیتا[위치 + 2] & 0xff) << 16)
                | ((دەیتا[위치 + 3] & 0xff) << 24);
    }

    private int 짧은정수읽기(byte[] دەیتا, int 위치) {
        if (위치 < 0 || 위치 > دەیتا.length - 2) {
            throw new IllegalArgumentException("ELF 짧은 ژمارەی_سروشتی 범위를 벗어났습니다.");
        }
        return (دەیتا[위치] & 0xff) | ((دەیتا[위치 + 1] & 0xff) << 8);
    }
}
