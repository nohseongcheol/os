// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package پاکستان.JPakOS.وقفه;

import java.util.Arrays;

/** IDT의 Java 관리 측 처리기 등록과 분배를 담당한다. */
public final class وقفه_مدیر {
    private final 개입중단처리기[] 처리기들 = new 개입중단처리기[256];
    private boolean فعال;

    public void ثبت_نام_ورودی(int فهرست, 개입중단처리기 처리기) {
        번호확인(فهرست);
        처리기들[فهرست] = 처리기;
    }

    public void انتشار_حافظه_تلفن(int فهرست) {
        번호확인(فهرست);
        처리기들[فهرست] = null;
    }

    public int توزیع_مقدار(int فهرست, int 저장된쌓임주소) {
        번호확인(فهرست);
        if (!فعال) {
            return 저장된쌓임주소;
        }
        개입중단처리기 처리기 = 처리기들[فهرست];
        return 처리기 == null ? 저장된쌓임주소 : 처리기.فرآیند_مقدار_ورودی(저장된쌓임주소);
    }

    public void فعالسازی() {
        فعال = true;
    }

    public void غیرفعال_کردن() {
        فعال = false;
    }

    public boolean فناوری_اطلاعات_فعال() {
        return فعال;
    }

    public void 모두해제() {
        Arrays.fill(처리기들, null);
    }

    private void 번호확인(int فهرست) {
        if (فهرست < 0 || فهرست >= 처리기들.length) {
            throw new IllegalArgumentException("وقفه 번호가 올바르지 않습니다.");
        }
    }
}

