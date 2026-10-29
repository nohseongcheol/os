// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ဘင်္ဂလားဒေ့ရှ်.JBgdOS.ဖိုင်စနစ်;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** DOS MBR ၏ အဓိကအပိုင်းခြားလေးခုကို ဖတ်သည်။ */
public final class အဓိကအပိုင်းခြားမှုဇယား {
    public static final class အပိုင်းခြားမှုတန်ဖိုး {
        private final int အမျိုးအစားတန်ဖိုး;
        private final long ကဏ္ဍစတင်;
        private final long ကဏ္ဍအရေအတွက်;

        အပိုင်းခြားမှုတန်ဖိုး(int အမျိုးအစားတန်ဖိုး, long ကဏ္ဍစတင်, long ကဏ္ဍအရေအတွက်) {
            this.အမျိုးအစားတန်ဖိုး = အမျိုးအစားတန်ဖိုး;
            this.ကဏ္ဍစတင် = ကဏ္ဍစတင်;
            this.ကဏ္ဍအရေအတွက် = ကဏ္ဍအရေအတွက်;
        }

        public int အမျိုးအစားတန်ဖိုး() { return အမျိုးအစားတန်ဖိုး; }
        public long ကဏ္ဍစတင်() { return ကဏ္ဍစတင်; }
        public long ကဏ္ဍအရေအတွက်() { return ကဏ္ဍအရေအတွက်; }
    }

    public List<အပိုင်းခြားမှုတန်ဖိုး> ဖတ်(byte[] ပထမကဏ္ဍ) {
        if (ပထမကဏ္ဍ == null || ပထမကဏ္ဍ.length < 512
                || (ပထမကဏ္ဍ[510] & 0xff) != 0x55 || (ပထမကဏ္ဍ[511] & 0xff) != 0xaa) {
            throw new IllegalArgumentException("올바른 MBR이 아닙니다.");
        }
        List<အပိုင်းခြားမှုတန်ဖိုး> ရလဒ် = new ArrayList<အပိုင်းခြားမှုတန်ဖိုး>();
        for (int နံပါတ် = 0; နံပါတ် < 4; နံပါတ်++) {
            int နေရာ = 446 + နံပါတ် * 16;
            int အမျိုးအစားတန်ဖိုး = ပထမကဏ္ဍ[နေရာ + 4] & 0xff;
            long လုပ်ဆောင် = အနိမ့်ဘိုက်ရှေ့ကိန်းပြည့်(ပထမကဏ္ဍ, နေရာ + 8);
            long အရွယ် = အနိမ့်ဘိုက်ရှေ့ကိန်းပြည့်(ပထမကဏ္ဍ, နေရာ + 12);
            if (အမျိုးအစားတန်ဖိုး != 0 && အရွယ် != 0) {
                ရလဒ်.add(new အပိုင်းခြားမှုတန်ဖိုး(အမျိုးအစားတန်ဖိုး, လုပ်ဆောင်, အရွယ်));
            }
        }
        return Collections.unmodifiableList(ရလဒ်);
    }

    private long အနိမ့်ဘိုက်ရှေ့ကိန်းပြည့်(byte[] ဒေတာ, int နေရာ) {
        return (ဒေတာ[နေရာ] & 0xffL)
                | ((ဒေတာ[နေရာ + 1] & 0xffL) << 8)
                | ((ဒေတာ[နေရာ + 2] & 0xffL) << 16)
                | ((ဒေတာ[နေရာ + 3] & 0xffL) << 24);
    }
}

