// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ဘင်္ဂလားဒေ့ရှ်.JBgdOS.ကိရိယာ;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** PCI ကိရိယာ ရှာဖွေရလဒ်နှင့် BAR/IRQ တန်ဖိုးများကို စီမံသည်။ */
public final class အရံဒေတာလမ်းစီမံသူ {
    public static final class ကိရိယာ {
        private final int ထုတ်လုပ်သူအမှတ်;
        private final int ကိရိယာသတ်မှတ်နံပါတ်;
        private final int အဝင်အထွက်အခြေ;
        private final int ကြားဖြတ်မှုကိန်း;

        public ကိရိယာ(int ထုတ်လုပ်သူအမှတ်, int ကိရိယာသတ်မှတ်နံပါတ်, int အဝင်အထွက်အခြေ, int ကြားဖြတ်မှုကိန်း) {
            this.ထုတ်လုပ်သူအမှတ် = ထုတ်လုပ်သူအမှတ်;
            this.ကိရိယာသတ်မှတ်နံပါတ် = ကိရိယာသတ်မှတ်နံပါတ်;
            this.အဝင်အထွက်အခြေ = အဝင်အထွက်အခြေ;
            this.ကြားဖြတ်မှုကိန်း = ကြားဖြတ်မှုကိန်း;
        }

        public int ထုတ်လုပ်သူအမှတ်() { return ထုတ်လုပ်သူအမှတ်; }
        public int ကိရိယာသတ်မှတ်နံပါတ်() { return ကိရိယာသတ်မှတ်နံပါတ်; }
        public int အဝင်အထွက်အခြေ() { return အဝင်အထွက်အခြေ; }
        public int ကြားဖြတ်မှုကိန်း() { return ကြားဖြတ်မှုကိန်း; }
    }

    private final List<ကိရိယာ> ကိရိယာများ = new ArrayList<ကိရိယာ>();

    public void ရှာတွေ့မှု(ကိရိယာ ကိရိယာ) {
        ကိရိယာများ.add(ကိရိယာ);
    }

    public List<ကိရိယာ> ကိရိယာများ() {
        return Collections.unmodifiableList(ကိရိယာများ);
    }

    public ကိရိယာ အချက်ရှာ(int ထုတ်လုပ်သူအမှတ်, int ကိရိယာသတ်မှတ်နံပါတ်) {
        for (ကိရိယာ အဆိုပြုချက် : ကိရိယာများ) {
            if (အဆိုပြုချက်.ထုတ်လုပ်သူအမှတ် == ထုတ်လုပ်သူအမှတ် && အဆိုပြုချက်.ကိရိယာသတ်မှတ်နံပါတ် == ကိရိယာသတ်မှတ်နံပါတ်) {
                return အဆိုပြုချက်;
            }
        }
        return null;
    }
}

