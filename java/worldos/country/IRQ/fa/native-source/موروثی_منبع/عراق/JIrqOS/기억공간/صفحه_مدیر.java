// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package عراق.JIrqOS.기억공간;

import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

/** 4 KiB صفحه_مقدار 연결과 نوشتن 시 복사를 제공한다. */
public final class صفحه_مدیر {
    public static final int اندازه_صفحه = 4096;

    private static final class صفحه_مقدار {
        private byte[] داده_ها = new byte[اندازه_صفحه];
        private int 참조수 = 1;
        private boolean 쓰기가능 = true;
        private boolean 쓰기시복사;
    }

    public static final class آدرس_فضا {
        private final Map<Integer, صفحه_مقدار> صفحه_جدول = new HashMap<Integer, صفحه_مقدار>();
    }

    public آدرس_فضا 새주소공간() {
        return new آدرس_فضا();
    }

    public void نگاشت_صفحه(آدرس_فضا 공간, int نشانی_مجازی, boolean 쓰기가능) {
        int فهرست = 쪽번호(نشانی_مجازی);
        صفحه_مقدار 새쪽 = new صفحه_مقدار();
        새쪽.쓰기가능 = 쓰기가능;
        공간.صفحه_جدول.put(Integer.valueOf(فهرست), 새쪽);
    }

    public آدرس_فضا 쓰기시복사복제(آدرس_فضا 원본) {
        آدرس_فضا 복제본 = new آدرس_فضا();
        for (Map.Entry<Integer, صفحه_مقدار> ورودی_مقدار : 원본.صفحه_جدول.entrySet()) {
            صفحه_مقدار 공유쪽 = ورودی_مقدار.getValue();
            공유쪽.참조수++;
            if (공유쪽.쓰기가능) {
                공유쪽.쓰기가능 = false;
                공유쪽.쓰기시복사 = true;
            }
            복제본.صفحه_جدول.put(ورودی_مقدار.getKey(), 공유쪽);
        }
        return 복제본;
    }

    public byte 바이트읽기(آدرس_فضا 공간, int نشانی_مجازی) {
        صفحه_مقدار هدف = کشف_صفحه(공간, نشانی_مجازی);
        return هدف.داده_ها[Math.floorMod(نشانی_مجازی, اندازه_صفحه)];
    }

    public void نوشتن_بایت_مقدار(آدرس_فضا 공간, int نشانی_مجازی, byte مقدار) {
        int فهرست = 쪽번호(نشانی_مجازی);
        صفحه_مقدار هدف = کشف_صفحه(공간, نشانی_مجازی);
        if (!هدف.쓰기가능) {
            if (!هدف.쓰기시복사) {
                throw new IllegalStateException("خواندن 전용 쪽입니다.");
            }
            هدف = ایجاد_خصوصی_صفحه(공간, فهرست, هدف);
        }
        هدف.داده_ها[Math.floorMod(نشانی_مجازی, اندازه_صفحه)] = مقدار;
    }

    public void 범위개인쓰기(آدرس_فضا 공간, int شروع_آدرس, int اندازه) {
        if (اندازه < 0) {
            throw new IllegalArgumentException("크기가 음수입니다.");
        }
        int پایان_دادن_آدرس = Math.addExact(شروع_آدرس, اندازه);
        for (int آدرس = شروع_آدرس; آدرس < پایان_دادن_آدرس; آدرس = (쪽번호(آدرس) + 1) * اندازه_صفحه) {
            int فهرست = 쪽번호(آدرس);
            صفحه_مقدار هدف = کشف_صفحه(공간, آدرس);
            if (هدف.쓰기시복사) {
                ایجاد_خصوصی_صفحه(공간, فهرست, هدف);
            } else {
                هدف.쓰기가능 = true;
            }
        }
    }

    public void 범위쓰기(آدرس_فضا 공간, int شروع_آدرس, byte[] داده_ها) {
        for (int فهرست = 0; فهرست < داده_ها.length; فهرست++) {
            نوشتن_بایت_مقدار(공간, شروع_آدرس + فهرست, داده_ها[فهرست]);
        }
    }

    private صفحه_مقدار ایجاد_خصوصی_صفحه(آدرس_فضا 공간, int فهرست, صفحه_مقدار 공유쪽) {
        صفحه_مقدار خصوصی_صفحه = new صفحه_مقدار();
        خصوصی_صفحه.داده_ها = Arrays.copyOf(공유쪽.داده_ها, 공유쪽.داده_ها.length);
        خصوصی_صفحه.쓰기가능 = true;
        خصوصی_صفحه.쓰기시복사 = false;
        공유쪽.참조수--;
        공간.صفحه_جدول.put(Integer.valueOf(فهرست), خصوصی_صفحه);
        return خصوصی_صفحه;
    }

    private صفحه_مقدار کشف_صفحه(آدرس_فضا 공간, int آدرس) {
        صفحه_مقدار هدف = 공간.صفحه_جدول.get(Integer.valueOf(쪽번호(آدرس)));
        if (هدف == null) {
            throw new IllegalStateException("연결되지 않은 가상 주소입니다.");
        }
        return هدف;
    }

    private int 쪽번호(int آدرس) {
        if (آدرس < 0) {
            throw new IllegalArgumentException("주소가 음수입니다.");
        }
        return آدرس / اندازه_صفحه;
    }
}

