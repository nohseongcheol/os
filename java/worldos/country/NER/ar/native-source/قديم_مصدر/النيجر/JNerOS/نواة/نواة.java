// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package النيجر.JNerOS.نواة;

import النيجر.JNerOS.ذاكرة_منطقة.ذاكرة_مدير;
import النيجر.JNerOS.ذاكرة_منطقة.صفحة_مدير;
import النيجر.JNerOS.إدخال_قيمة.إدخال_مدير;
import النيجر.JNerOS.작업.عملية_قيمة;
import النيجر.JNerOS.작업.المجدوِل;
import النيجر.JNerOS.نداء_النظام.نداء_النظام;
import النيجر.JNerOS.نظام_الملفات.파일서술자표;
import النيجر.JNerOS.نظام_الملفات.نظام_الملفات;

/** Java 관리 커널의 조립과 시작을 담당한다. */
public final class نواة {
    private final أجهزة_قيمة جهاز_قيمة;
    private final ذاكرة_مدير ذاكرة_منطقة = new ذاكرة_مدير(32 * 1024 * 1024);
    private final صفحة_مدير 쪽관리 = new صفحة_مدير();
    private final نظام_الملفات نظام_الملفات = new نظام_الملفات();
    private final المجدوِل المجدوِل = new المجدوِل(쪽관리);
    private final إدخال_مدير 입력관리 = new إدخال_مدير(256);
    private final عملية_قيمة 첫과정;
    private final نداء_النظام نداء_النظام;

    public نواة(أجهزة_قيمة جهاز_قيمة) {
        this.جهاز_قيمة = جهاز_قيمة;
        첫과정 = المجدوِل.첫과정(new 파일서술자표(نظام_الملفات));
        نداء_النظام = new نداء_النظام(نظام_الملفات, 쪽관리, المجدوِل, جهاز_قيمة, 입력관리);
    }

    public void تشغيل() {
        جهاز_قيمة.직렬출력("=== JNerOS 관리 نواة_قيمة ===\n");
    }

    public void ينفذ_خطوة() {
        جهاز_قيمة.중앙처리장치멈춤();
    }

    public ذاكرة_مدير ذاكرة_منطقة() {
        return ذاكرة_منطقة;
    }

    public صفحة_مدير 쪽관리() {
        return 쪽관리;
    }

    public نظام_الملفات نظام_الملفات() {
        return نظام_الملفات;
    }

    public المجدوِل المجدوِل() {
        return المجدوِل;
    }

    public إدخال_مدير 입력관리() {
        return 입력관리;
    }

    public عملية_قيمة 첫과정() {
        return 첫과정;
    }

    public نداء_النظام نداء_النظام() {
        return نداء_النظام;
    }
}
