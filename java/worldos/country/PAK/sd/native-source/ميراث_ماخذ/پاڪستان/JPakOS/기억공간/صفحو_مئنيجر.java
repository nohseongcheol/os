// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package پاڪستان.JPakOS.기억공간;

import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

/** 4 KiB صفحو_قدر 연결과 لکو 시 복사를 제공한다. */
public final class صفحو_مئنيجر {
    public static final int صفحي_جي_ماپ = 4096;

    private static final class صفحو_قدر {
        private byte[] ڪوائف = new byte[صفحي_جي_ماپ];
        private int 참조수 = 1;
        private boolean 쓰기가능 = true;
        private boolean 쓰기시복사;
    }

    public static final class پتو_جڳهه {
        private final Map<Integer, صفحو_قدر> صفحو_جدول = new HashMap<Integer, صفحو_قدر>();
    }

    public پتو_جڳهه 새주소공간() {
        return new پتو_جڳهه();
    }

    public void نقشو_صفحو(پتو_جڳهه 공간, int مجازي_پتو, boolean 쓰기가능) {
        int ابتدائي = 쪽번호(مجازي_پتو);
        صفحو_قدر 새쪽 = new صفحو_قدر();
        새쪽.쓰기가능 = 쓰기가능;
        공간.صفحو_جدول.put(Integer.valueOf(ابتدائي), 새쪽);
    }

    public پتو_جڳهه 쓰기시복사복제(پتو_جڳهه 원본) {
        پتو_جڳهه 복제본 = new پتو_جڳهه();
        for (Map.Entry<Integer, صفحو_قدر> داخلا_قدر : 원본.صفحو_جدول.entrySet()) {
            صفحو_قدر 공유쪽 = داخلا_قدر.getValue();
            공유쪽.참조수++;
            if (공유쪽.쓰기가능) {
                공유쪽.쓰기가능 = false;
                공유쪽.쓰기시복사 = true;
            }
            복제본.صفحو_جدول.put(داخلا_قدر.getKey(), 공유쪽);
        }
        return 복제본;
    }

    public byte 바이트읽기(پتو_جڳهه 공간, int مجازي_پتو) {
        صفحو_قدر هدف = ڳوليو_صفحو(공간, مجازي_پتو);
        return هدف.ڪوائف[Math.floorMod(مجازي_پتو, صفحي_جي_ماپ)];
    }

    public void لکو_بائٽ_قدر(پتو_جڳهه 공간, int مجازي_پتو, byte قدر) {
        int ابتدائي = 쪽번호(مجازي_پتو);
        صفحو_قدر هدف = ڳوليو_صفحو(공간, مجازي_پتو);
        if (!هدف.쓰기가능) {
            if (!هدف.쓰기시복사) {
                throw new IllegalStateException("읽기 전용 쪽입니다.");
            }
            هدف = ٺاھيو_ذاتي_صفحو(공간, ابتدائي, هدف);
        }
        هدف.ڪوائف[Math.floorMod(مجازي_پتو, صفحي_جي_ماپ)] = قدر;
    }

    public void 범위개인쓰기(پتو_جڳهه 공간, int شروع_پتو, int سائيز) {
        if (سائيز < 0) {
            throw new IllegalArgumentException("크기가 음수입니다.");
        }
        int ختم_ڪريو_پتو = Math.addExact(شروع_پتو, سائيز);
        for (int پتو = شروع_پتو; پتو < ختم_ڪريو_پتو; پتو = (쪽번호(پتو) + 1) * صفحي_جي_ماپ) {
            int ابتدائي = 쪽번호(پتو);
            صفحو_قدر هدف = ڳوليو_صفحو(공간, پتو);
            if (هدف.쓰기시복사) {
                ٺاھيو_ذاتي_صفحو(공간, ابتدائي, هدف);
            } else {
                هدف.쓰기가능 = true;
            }
        }
    }

    public void 범위쓰기(پتو_جڳهه 공간, int شروع_پتو, byte[] ڪوائف) {
        for (int ابتدائي = 0; ابتدائي < ڪوائف.length; ابتدائي++) {
            لکو_بائٽ_قدر(공간, شروع_پتو + ابتدائي, ڪوائف[ابتدائي]);
        }
    }

    private صفحو_قدر ٺاھيو_ذاتي_صفحو(پتو_جڳهه 공간, int ابتدائي, صفحو_قدر 공유쪽) {
        صفحو_قدر ذاتي_صفحو = new صفحو_قدر();
        ذاتي_صفحو.ڪوائف = Arrays.copyOf(공유쪽.ڪوائف, 공유쪽.ڪوائف.length);
        ذاتي_صفحو.쓰기가능 = true;
        ذاتي_صفحو.쓰기시복사 = false;
        공유쪽.참조수--;
        공간.صفحو_جدول.put(Integer.valueOf(ابتدائي), ذاتي_صفحو);
        return ذاتي_صفحو;
    }

    private صفحو_قدر ڳوليو_صفحو(پتو_جڳهه 공간, int پتو) {
        صفحو_قدر هدف = 공간.صفحو_جدول.get(Integer.valueOf(쪽번호(پتو)));
        if (هدف == null) {
            throw new IllegalStateException("연결되지 않은 가상 주소입니다.");
        }
        return هدف;
    }

    private int 쪽번호(int پتو) {
        if (پتو < 0) {
            throw new IllegalArgumentException("주소가 음수입니다.");
        }
        return پتو / صفحي_جي_ماپ;
    }
}

