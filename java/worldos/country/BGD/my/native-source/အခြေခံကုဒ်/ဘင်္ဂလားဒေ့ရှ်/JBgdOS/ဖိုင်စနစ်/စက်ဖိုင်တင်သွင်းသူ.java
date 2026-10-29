// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ဘင်္ဂလားဒေ့ရှ်.JBgdOS.ဖိုင်စနစ်;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** အနိမ့်ဘိုက်ရှေ့ ELF32 စက်ဖိုင်၏ ခေါင်းစီးနှင့် တင်မည့်နယ်များကို စစ်ဆေးသည်။ */
public final class စက်ဖိုင်တင်သွင်းသူ {
    public static final class ကဏ္ဍတန်ဖိုး {
        private final int အမျိုးအစားတန်ဖိုး;
        private final int အလံတန်ဖိုး;
        private final int လိပ်စာ;
        private final int ဖိုင်နေရာ;
        private final int အရွယ်;

        ကဏ္ဍတန်ဖိုး(int အမျိုးအစားတန်ဖိုး, int အလံတန်ဖိုး, int လိပ်စာ, int ဖိုင်နေရာ, int အရွယ်) {
            this.အမျိုးအစားတန်ဖိုး = အမျိုးအစားတန်ဖိုး;
            this.အလံတန်ဖိုး = အလံတန်ဖိုး;
            this.လိပ်စာ = လိပ်စာ;
            this.ဖိုင်နေရာ = ဖိုင်နေရာ;
            this.အရွယ် = အရွယ်;
        }

        public int အမျိုးအစားတန်ဖိုး() {
            return အမျိုးအစားတန်ဖိုး;
        }

        public int အလံတန်ဖိုး() {
            return အလံတန်ဖိုး;
        }

        public int လိပ်စာ() {
            return လိပ်စာ;
        }

        public int ဖိုင်နေရာ() {
            return ဖိုင်နေရာ;
        }

        public int အရွယ်() {
            return အရွယ်;
        }
    }

    public static final class စက်ကုဒ်ပုံရိပ် {
        private final int စတင်လိပ်စာ;
        private final List<ကဏ္ဍတန်ဖိုး> အပိုင်းကဏ္ဍများ;

        စက်ကုဒ်ပုံရိပ်(int စတင်လိပ်စာ, List<ကဏ္ဍတန်ဖိုး> အပိုင်းကဏ္ဍများ) {
            this.စတင်လိပ်စာ = စတင်လိပ်စာ;
            this.အပိုင်းကဏ္ဍများ = Collections.unmodifiableList(အပိုင်းကဏ္ဍများ);
        }

        public int စတင်လိပ်စာ() {
            return စတင်လိပ်စာ;
        }

        public List<ကဏ္ဍတန်ဖိုး> အပိုင်းကဏ္ဍများ() {
            return အပိုင်းကဏ္ဍများ;
        }
    }

    public စက်ကုဒ်ပုံရိပ် စစ်ဆေးချက်(byte[] ဒေတာ) {
        if (ဒေတာ == null || ဒေတာ.length < 52
                || ဒေတာ[0] != 0x7f || ဒေတာ[1] != 'E' || ဒေတာ[2] != 'L' || ဒေတာ[3] != 'F') {
            throw new IllegalArgumentException("ELF 마법값이 올바르지 않습니다.");
        }
        if (ဒေတာ[4] != 1 || ဒေတာ[5] != 1) {
            throw new IllegalArgumentException("ELF32 little-endian 형식이 아닙니다.");
        }
        int စတင်လိပ်စာ = ကိန်းပြည့်သဒ္ဒါခွဲခြမ်း(ဒေတာ, 24);
        int ကဏ္ဍဇယားနေရာ = ကိန်းပြည့်သဒ္ဒါခွဲခြမ်း(ဒေတာ, 32);
        int ကဏ္ဍအချက်အရွယ် = တိုကိန်းပြည့်ဖတ်(ဒေတာ, 46);
        int ကဏ္ဍအရေအတွက် = တိုကိန်းပြည့်ဖတ်(ဒေတာ, 48);
        if (ကဏ္ဍအချက်အရွယ် < 40 || ကဏ္ဍဇယားနေရာ < 0
                || (long) ကဏ္ဍဇယားနေရာ + (long) ကဏ္ဍအချက်အရွယ် * ကဏ္ဍအရေအတွက် > ဒေတာ.length) {
            throw new IllegalArgumentException("ELF 구역표 범위가 올바르지 않습니다.");
        }
        List<ကဏ္ဍတန်ဖိုး> အပိုင်းကဏ္ဍများ = new ArrayList<ကဏ္ဍတန်ဖိုး>();
        for (int နံပါတ် = 0; နံပါတ် < ကဏ္ဍအရေအတွက်; နံပါတ်++) {
            int နေရာ = ကဏ္ဍဇယားနေရာ + နံပါတ် * ကဏ္ဍအချက်အရွယ်;
            int အမျိုးအစားတန်ဖိုး = ကိန်းပြည့်သဒ္ဒါခွဲခြမ်း(ဒေတာ, နေရာ + 4);
            int အလံတန်ဖိုး = ကိန်းပြည့်သဒ္ဒါခွဲခြမ်း(ဒေတာ, နေရာ + 8);
            int လိပ်စာ = ကိန်းပြည့်သဒ္ဒါခွဲခြမ်း(ဒေတာ, နေရာ + 12);
            int ဖိုင်နေရာ = ကိန်းပြည့်သဒ္ဒါခွဲခြမ်း(ဒေတာ, နေရာ + 16);
            int အရွယ် = ကိန်းပြည့်သဒ္ဒါခွဲခြမ်း(ဒေတာ, နေရာ + 20);
            if (အရွယ် < 0 || (အမျိုးအစားတန်ဖိုး != 8 && ((long) ဖိုင်နေရာ + အရွယ် > ဒေတာ.length || ဖိုင်နေရာ < 0))) {
                throw new IllegalArgumentException("ELF ကဏ္ဍတန်ဖိုး ဒေတာ 범위가 올바르지 않습니다.");
            }
            အပိုင်းကဏ္ဍများ.add(new ကဏ္ဍတန်ဖိုး(အမျိုးအစားတန်ဖိုး, အလံတန်ဖိုး, လိပ်စာ, ဖိုင်နေရာ, အရွယ်));
        }
        return new စက်ကုဒ်ပုံရိပ်(စတင်လိပ်စာ, အပိုင်းကဏ္ဍများ);
    }

    private int ကိန်းပြည့်သဒ္ဒါခွဲခြမ်း(byte[] ဒေတာ, int နေရာ) {
        if (နေရာ < 0 || နေရာ > ဒေတာ.length - 4) {
            throw new IllegalArgumentException("ELF ကိန်းပြည့် 범위를 벗어났습니다.");
        }
        return (ဒေတာ[နေရာ] & 0xff)
                | ((ဒေတာ[နေရာ + 1] & 0xff) << 8)
                | ((ဒေတာ[နေရာ + 2] & 0xff) << 16)
                | ((ဒေတာ[နေရာ + 3] & 0xff) << 24);
    }

    private int တိုကိန်းပြည့်ဖတ်(byte[] ဒေတာ, int နေရာ) {
        if (နေရာ < 0 || နေရာ > ဒေတာ.length - 2) {
            throw new IllegalArgumentException("ELF 짧은 ကိန်းပြည့် 범위를 벗어났습니다.");
        }
        return (ဒေတာ[နေရာ] & 0xff) | ((ဒေတာ[နေရာ + 1] & 0xff) << 8);
    }
}
