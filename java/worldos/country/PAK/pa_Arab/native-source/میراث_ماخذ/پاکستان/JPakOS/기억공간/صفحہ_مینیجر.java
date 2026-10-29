// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package پاکستان.JPakOS.기억공간;

import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

/** 4 KiB صفحہ_قدر 연결과 لکھو 시 복사를 제공한다. */
public final class صفحہ_مینیجر {
    public static final int ورقے_دا_ناپ = 4096;

    private static final class صفحہ_قدر {
        private byte[] کوائف = new byte[ورقے_دا_ناپ];
        private int 참조수 = 1;
        private boolean 쓰기가능 = true;
        private boolean 쓰기시복사;
    }

    public static final class پتا_جگہ {
        private final Map<Integer, صفحہ_قدر> صفحہ_جدول = new HashMap<Integer, صفحہ_قدر>();
    }

    public پتا_جگہ 새주소공간() {
        return new پتا_جگہ();
    }

    public void نقشہ_صفحہ(پتا_جگہ 공간, int مجازی_پتا, boolean 쓰기가능) {
        int اشاریہ = 쪽번호(مجازی_پتا);
        صفحہ_قدر 새쪽 = new صفحہ_قدر();
        새쪽.쓰기가능 = 쓰기가능;
        공간.صفحہ_جدول.put(Integer.valueOf(اشاریہ), 새쪽);
    }

    public پتا_جگہ 쓰기시복사복제(پتا_جگہ 원본) {
        پتا_جگہ 복제본 = new پتا_جگہ();
        for (Map.Entry<Integer, صفحہ_قدر> داخلہ_قدر : 원본.صفحہ_جدول.entrySet()) {
            صفحہ_قدر 공유쪽 = داخلہ_قدر.getValue();
            공유쪽.참조수++;
            if (공유쪽.쓰기가능) {
                공유쪽.쓰기가능 = false;
                공유쪽.쓰기시복사 = true;
            }
            복제본.صفحہ_جدول.put(داخلہ_قدر.getKey(), 공유쪽);
        }
        return 복제본;
    }

    public byte 바이트읽기(پتا_جگہ 공간, int مجازی_پتا) {
        صفحہ_قدر ہدف = ڈھونڈو_صفحہ(공간, مجازی_پتا);
        return ہدف.کوائف[Math.floorMod(مجازی_پتا, ورقے_دا_ناپ)];
    }

    public void لکھو_بائٹ_قدر(پتا_جگہ 공간, int مجازی_پتا, byte قدر) {
        int اشاریہ = 쪽번호(مجازی_پتا);
        صفحہ_قدر ہدف = ڈھونڈو_صفحہ(공간, مجازی_پتا);
        if (!ہدف.쓰기가능) {
            if (!ہدف.쓰기시복사) {
                throw new IllegalStateException("읽기 전용 쪽입니다.");
            }
            ہدف = بنڑاؤ_ذاتی_صفحہ(공간, اشاریہ, ہدف);
        }
        ہدف.کوائف[Math.floorMod(مجازی_پتا, ورقے_دا_ناپ)] = قدر;
    }

    public void 범위개인쓰기(پتا_جگہ 공간, int مکھ_پتا, int سائز) {
        if (سائز < 0) {
            throw new IllegalArgumentException("크기가 음수입니다.");
        }
        int ختم_کرو_پتا = Math.addExact(مکھ_پتا, سائز);
        for (int پتا = مکھ_پتا; پتا < ختم_کرو_پتا; پتا = (쪽번호(پتا) + 1) * ورقے_دا_ناپ) {
            int اشاریہ = 쪽번호(پتا);
            صفحہ_قدر ہدف = ڈھونڈو_صفحہ(공간, پتا);
            if (ہدف.쓰기시복사) {
                بنڑاؤ_ذاتی_صفحہ(공간, اشاریہ, ہدف);
            } else {
                ہدف.쓰기가능 = true;
            }
        }
    }

    public void 범위쓰기(پتا_جگہ 공간, int مکھ_پتا, byte[] کوائف) {
        for (int اشاریہ = 0; اشاریہ < کوائف.length; اشاریہ++) {
            لکھو_بائٹ_قدر(공간, مکھ_پتا + اشاریہ, کوائف[اشاریہ]);
        }
    }

    private صفحہ_قدر بنڑاؤ_ذاتی_صفحہ(پتا_جگہ 공간, int اشاریہ, صفحہ_قدر 공유쪽) {
        صفحہ_قدر ذاتی_صفحہ = new صفحہ_قدر();
        ذاتی_صفحہ.کوائف = Arrays.copyOf(공유쪽.کوائف, 공유쪽.کوائف.length);
        ذاتی_صفحہ.쓰기가능 = true;
        ذاتی_صفحہ.쓰기시복사 = false;
        공유쪽.참조수--;
        공간.صفحہ_جدول.put(Integer.valueOf(اشاریہ), ذاتی_صفحہ);
        return ذاتی_صفحہ;
    }

    private صفحہ_قدر ڈھونڈو_صفحہ(پتا_جگہ 공간, int پتا) {
        صفحہ_قدر ہدف = 공간.صفحہ_جدول.get(Integer.valueOf(쪽번호(پتا)));
        if (ہدف == null) {
            throw new IllegalStateException("연결되지 않은 가상 주소입니다.");
        }
        return ہدف;
    }

    private int 쪽번호(int پتا) {
        if (پتا < 0) {
            throw new IllegalArgumentException("주소가 음수입니다.");
        }
        return پتا / ورقے_دا_ناپ;
    }
}

