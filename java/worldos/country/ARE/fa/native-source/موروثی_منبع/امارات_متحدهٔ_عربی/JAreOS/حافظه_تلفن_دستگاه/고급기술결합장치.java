// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package امارات_متحدهٔ_عربی.JAreOS.حافظه_تلفن_دستگاه;

import java.util.Arrays;

/** ATA 28비트 فرمان 계층과 같은 512바이트 논리 قسمت_مقدار 장치다. */
public final class 고급기술결합장치 {
    public static final int قسمت_اندازه_کردن = 512;
    private final byte[] داده_ها;
    private final boolean فقط_خواندنی_مقدار;

    public 고급기술결합장치(int 구역수, boolean فقط_خواندنی_مقدار) {
        if (구역수 <= 0) {
            throw new IllegalArgumentException("قسمت_مقدار 수가 올바르지 않습니다.");
        }
        داده_ها = new byte[Math.multiplyExact(구역수, قسمت_اندازه_کردن)];
        this.فقط_خواندنی_مقدار = فقط_خواندنی_مقدار;
    }

    public int 구역수() {
        return داده_ها.length / قسمت_اندازه_کردن;
    }

    public void خواندن(int قسمت_فهرست, byte[] 받을곳) {
        범위확인(قسمت_فهرست, 받을곳);
        System.arraycopy(داده_ها, قسمت_فهرست * قسمت_اندازه_کردن, 받을곳, 0, قسمت_اندازه_کردن);
    }

    public void نوشتن(int قسمت_فهرست, byte[] 쓸자료) {
        if (فقط_خواندنی_مقدار) {
            throw new IllegalStateException("خواندن 전용 장치입니다.");
        }
        범위확인(قسمت_فهرست, 쓸자료);
        System.arraycopy(쓸자료, 0, داده_ها, قسمت_فهرست * قسمت_اندازه_کردن, قسمت_اندازه_کردن);
    }

    public void پاک_کردن_ورودی() {
        if (فقط_خواندنی_مقدار) {
            throw new IllegalStateException("خواندن 전용 장치입니다.");
        }
        Arrays.fill(داده_ها, (byte) 0);
    }

    private void 범위확인(int قسمت_فهرست, byte[] 임시공간) {
        if (قسمت_فهرست < 0 || قسمت_فهرست >= 구역수() || 임시공간.length < قسمت_اندازه_کردن) {
            throw new IllegalArgumentException("ATA قسمت_مقدار 범위가 올바르지 않습니다.");
        }
    }
}

