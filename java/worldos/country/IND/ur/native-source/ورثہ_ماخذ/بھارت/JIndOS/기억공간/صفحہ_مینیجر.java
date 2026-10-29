// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package بھارت.JIndOS.기억공간;

import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

/** 4 KiB صفحہ_قدر 연결과 لکھیں 시 복사를 제공한다. */
public final class صفحہ_مینیجر {
    public static final int صفحہ_سائز = 4096;

    private static final class صفحہ_قدر {
        private byte[] کوائف = new byte[صفحہ_سائز];
        private int 참조수 = 1;
        private boolean 쓰기가능 = true;
        private boolean 쓰기시복사;
    }

    public static final class پتہ_اسپیس {
        private final Map<Integer, صفحہ_قدر> صفحہ_جدول = new HashMap<Integer, صفحہ_قدر>();
    }

    public پتہ_اسپیس 새주소공간() {
        return new پتہ_اسپیس();
    }

    public void میپ_صفحہ(پتہ_اسپیس 공간, int مجازی_پتہ, boolean 쓰기가능) {
        int اشاریہ = 쪽번호(مجازی_پتہ);
        صفحہ_قدر 새쪽 = new صفحہ_قدر();
        새쪽.쓰기가능 = 쓰기가능;
        공간.صفحہ_جدول.put(Integer.valueOf(اشاریہ), 새쪽);
    }

    public پتہ_اسپیس 쓰기시복사복제(پتہ_اسپیس 원본) {
        پتہ_اسپیس 복제본 = new پتہ_اسپیس();
        for (Map.Entry<Integer, صفحہ_قدر> اندراج_قدر : 원본.صفحہ_جدول.entrySet()) {
            صفحہ_قدر 공유쪽 = اندراج_قدر.getValue();
            공유쪽.참조수++;
            if (공유쪽.쓰기가능) {
                공유쪽.쓰기가능 = false;
                공유쪽.쓰기시복사 = true;
            }
            복제본.صفحہ_جدول.put(اندراج_قدر.getKey(), 공유쪽);
        }
        return 복제본;
    }

    public byte 바이트읽기(پتہ_اسپیس 공간, int مجازی_پتہ) {
        صفحہ_قدر ہدف = ڈھونڈیں_صفحہ(공간, مجازی_پتہ);
        return ہدف.کوائف[Math.floorMod(مجازی_پتہ, صفحہ_سائز)];
    }

    public void لکھیں_بائٹ_قدر(پتہ_اسپیس 공간, int مجازی_پتہ, byte قدر) {
        int اشاریہ = 쪽번호(مجازی_پتہ);
        صفحہ_قدر ہدف = ڈھونڈیں_صفحہ(공간, مجازی_پتہ);
        if (!ہدف.쓰기가능) {
            if (!ہدف.쓰기시복사) {
                throw new IllegalStateException("پڑھیں 전용 쪽입니다.");
            }
            ہدف = بنائیں_نجی_صفحہ(공간, اشاریہ, ہدف);
        }
        ہدف.کوائف[Math.floorMod(مجازی_پتہ, صفحہ_سائز)] = قدر;
    }

    public void 범위개인쓰기(پتہ_اسپیس 공간, int ابتدا_پتہ, int حجم) {
        if (حجم < 0) {
            throw new IllegalArgumentException("크기가 음수입니다.");
        }
        int اختتام_پتہ = Math.addExact(ابتدا_پتہ, حجم);
        for (int پتہ = ابتدا_پتہ; پتہ < اختتام_پتہ; پتہ = (쪽번호(پتہ) + 1) * صفحہ_سائز) {
            int اشاریہ = 쪽번호(پتہ);
            صفحہ_قدر ہدف = ڈھونڈیں_صفحہ(공간, پتہ);
            if (ہدف.쓰기시복사) {
                بنائیں_نجی_صفحہ(공간, اشاریہ, ہدف);
            } else {
                ہدف.쓰기가능 = true;
            }
        }
    }

    public void 범위쓰기(پتہ_اسپیس 공간, int ابتدا_پتہ, byte[] کوائف) {
        for (int اشاریہ = 0; اشاریہ < کوائف.length; اشاریہ++) {
            لکھیں_بائٹ_قدر(공간, ابتدا_پتہ + اشاریہ, کوائف[اشاریہ]);
        }
    }

    private صفحہ_قدر بنائیں_نجی_صفحہ(پتہ_اسپیس 공간, int اشاریہ, صفحہ_قدر 공유쪽) {
        صفحہ_قدر نجی_صفحہ = new صفحہ_قدر();
        نجی_صفحہ.کوائف = Arrays.copyOf(공유쪽.کوائف, 공유쪽.کوائف.length);
        نجی_صفحہ.쓰기가능 = true;
        نجی_صفحہ.쓰기시복사 = false;
        공유쪽.참조수--;
        공간.صفحہ_جدول.put(Integer.valueOf(اشاریہ), نجی_صفحہ);
        return نجی_صفحہ;
    }

    private صفحہ_قدر ڈھونڈیں_صفحہ(پتہ_اسپیس 공간, int پتہ) {
        صفحہ_قدر ہدف = 공간.صفحہ_جدول.get(Integer.valueOf(쪽번호(پتہ)));
        if (ہدف == null) {
            throw new IllegalStateException("연결되지 않은 가상 주소입니다.");
        }
        return ہدف;
    }

    private int 쪽번호(int پتہ) {
        if (پتہ < 0) {
            throw new IllegalArgumentException("주소가 음수입니다.");
        }
        return پتہ / صفحہ_سائز;
    }
}

