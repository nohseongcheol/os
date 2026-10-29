// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package كينيا.JKenOS.مضيف;

import كينيا.JKenOS.نواة.نواة;

public final class مضيف_بدء_التشغيل {
    private مضيف_بدء_التشغيل() {
    }

    public static void main(String[] معلمة_وسيطة) {
        نواة نواة_قيمة = new نواة(new مضيف_أجهزة());
        نواة_قيمة.تشغيل();
        نواة_قيمة.ينفذ_خطوة();
    }
}

