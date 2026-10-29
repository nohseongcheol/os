// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package سوريا.JSyrOS.مقاطعة;

import java.util.Arrays;

/** IDT의 Java 관리 측 처리기 등록과 분배를 담당한다. */
public final class مقاطعة_مدير {
    private final 개입중단처리기[] 처리기들 = new 개입중단처리기[256];
    private boolean نشط;

    public void سجل_إدخال(int فهرس, 개입중단처리기 처리기) {
        يتحقق_رقم(فهرس);
        처리기들[فهرس] = 처리기;
    }

    public void إصدار_تخزين(int فهرس) {
        يتحقق_رقم(فهرس);
        처리기들[فهرس] = null;
    }

    public int يوزع_قيمة(int فهرس, int 저장된쌓임주소) {
        يتحقق_رقم(فهرس);
        if (!نشط) {
            return 저장된쌓임주소;
        }
        개입중단처리기 처리기 = 처리기들[فهرس];
        return 처리기 == null ? 저장된쌓임주소 : 처리기.عملية_قيمة_إدخال(저장된쌓임주소);
    }

    public void يشغل() {
        نشط = true;
    }

    public void إيقاف_نشاط() {
        نشط = false;
    }

    public boolean أنظمة_المعلومات_نشط() {
        return نشط;
    }

    public void 모두해제() {
        Arrays.fill(처리기들, null);
    }

    private void يتحقق_رقم(int فهرس) {
        if (فهرس < 0 || فهرس >= 처리기들.length) {
            throw new IllegalArgumentException("مقاطعة 번호가 올바르지 않습니다.");
        }
    }
}

