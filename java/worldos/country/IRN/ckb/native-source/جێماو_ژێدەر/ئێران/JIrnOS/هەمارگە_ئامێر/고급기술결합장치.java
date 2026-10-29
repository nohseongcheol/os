// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ئێران.JIrnOS.هەمارگە_ئامێر;

import java.util.Arrays;

/** ATA 28비트 فەرمان 계층과 같은 512바이트 논리 بەش_نرخ 장치다. */
public final class 고급기술결합장치 {
    public static final int بەش_گۆڕینی_ئەندازە = 512;
    private final byte[] دەیتا;
    private final boolean تەنیا_دەخوێنرێتەوە_نرخ;

    public 고급기술결합장치(int 구역수, boolean تەنیا_دەخوێنرێتەوە_نرخ) {
        if (구역수 <= 0) {
            throw new IllegalArgumentException("بەش_نرخ 수가 올바르지 않습니다.");
        }
        دەیتا = new byte[Math.multiplyExact(구역수, بەش_گۆڕینی_ئەندازە)];
        this.تەنیا_دەخوێنرێتەوە_نرخ = تەنیا_دەخوێنرێتەوە_نرخ;
    }

    public int 구역수() {
        return دەیتا.length / بەش_گۆڕینی_ئەندازە;
    }

    public void 읽기(int بەش_پێرست, byte[] 받을곳) {
        범위확인(بەش_پێرست, 받을곳);
        System.arraycopy(دەیتا, بەش_پێرست * بەش_گۆڕینی_ئەندازە, 받을곳, 0, بەش_گۆڕینی_ئەندازە);
    }

    public void ڕایت_کردن(int بەش_پێرست, byte[] 쓸자료) {
        if (تەنیا_دەخوێنرێتەوە_نرخ) {
            throw new IllegalStateException("읽기 전용 장치입니다.");
        }
        범위확인(بەش_پێرست, 쓸자료);
        System.arraycopy(쓸자료, 0, دەیتا, بەش_پێرست * بەش_گۆڕینی_ئەندازە, بەش_گۆڕینی_ئەندازە);
    }

    public void 지우기() {
        if (تەنیا_دەخوێنرێتەوە_نرخ) {
            throw new IllegalStateException("읽기 전용 장치입니다.");
        }
        Arrays.fill(دەیتا, (byte) 0);
    }

    private void 범위확인(int بەش_پێرست, byte[] 임시공간) {
        if (بەش_پێرست < 0 || بەش_پێرست >= 구역수() || 임시공간.length < بەش_گۆڕینی_ئەندازە) {
            throw new IllegalArgumentException("ATA بەش_نرخ 범위가 올바르지 않습니다.");
        }
    }
}

