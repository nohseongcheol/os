// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package الجزائر.JDzaOS.جهاز_تخزين;

import java.util.Arrays;

/** ATA 28비트 أمر 계층과 같은 512바이트 논리 قسم_قيمة_366e0bfa 장치다. */
public final class 고급기술결합장치 {
    public static final int قسم_يغير_الحجم = 512;
    private final byte[] بيانات;
    private final boolean للقراءة_فقط_قيمة;

    public 고급기술결합장치(int 구역수, boolean للقراءة_فقط_قيمة) {
        if (구역수 <= 0) {
            throw new IllegalArgumentException("قسم_قيمة_366e0bfa 수가 올바르지 않습니다.");
        }
        بيانات = new byte[Math.multiplyExact(구역수, قسم_يغير_الحجم)];
        this.للقراءة_فقط_قيمة = للقراءة_فقط_قيمة;
    }

    public int 구역수() {
        return بيانات.length / قسم_يغير_الحجم;
    }

    public void قراءة(int قسم_فهرس, byte[] يستلم_وجهة) {
        شيك_نطاق(قسم_فهرس, يستلم_وجهة);
        System.arraycopy(بيانات, قسم_فهرس * قسم_يغير_الحجم, يستلم_وجهة, 0, قسم_يغير_الحجم);
    }

    public void كتابة(int قسم_فهرس, byte[] 쓸자료) {
        if (للقراءة_فقط_قيمة) {
            throw new IllegalStateException("قراءة 전용 장치입니다.");
        }
        شيك_نطاق(قسم_فهرس, 쓸자료);
        System.arraycopy(쓸자료, 0, بيانات, قسم_فهرس * قسم_يغير_الحجم, قسم_يغير_الحجم);
    }

    public void مسح_إدخال() {
        if (للقراءة_فقط_قيمة) {
            throw new IllegalStateException("قراءة 전용 장치입니다.");
        }
        Arrays.fill(بيانات, (byte) 0);
    }

    private void شيك_نطاق(int قسم_فهرس, byte[] 임시공간) {
        if (قسم_فهرس < 0 || قسم_فهرس >= 구역수() || 임시공간.length < قسم_يغير_الحجم) {
            throw new IllegalArgumentException("ATA قسم_قيمة_366e0bfa 범위가 올바르지 않습니다.");
        }
    }
}

