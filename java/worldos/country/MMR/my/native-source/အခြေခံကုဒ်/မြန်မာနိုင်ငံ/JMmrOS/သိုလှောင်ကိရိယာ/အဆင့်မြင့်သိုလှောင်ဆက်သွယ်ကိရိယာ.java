// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package မြန်မာနိုင်ငံ.JMmrOS.သိုလှောင်ကိရိယာ;

import java.util.Arrays;

/** ATA 28 ဘစ် အမိန့်အလွှာနှင့် တူညီသော 512 ဘိုက် ယုတ္တိကဏ္ဍ ကိရိယာ။ */
public final class အဆင့်မြင့်သိုလှောင်ဆက်သွယ်ကိရိယာ {
    public static final int ကဏ္ဍအရွယ် = 512;
    private final byte[] ဒေတာ;
    private final boolean သာတန်ဖိုးဖတ်;

    public အဆင့်မြင့်သိုလှောင်ဆက်သွယ်ကိရိယာ(int ကဏ္ဍအရေအတွက်, boolean သာတန်ဖိုးဖတ်) {
        if (ကဏ္ဍအရေအတွက် <= 0) {
            throw new IllegalArgumentException("ကဏ္ဍတန်ဖိုး 수가 올바르지 않습니다.");
        }
        ဒေတာ = new byte[Math.multiplyExact(ကဏ္ဍအရေအတွက်, ကဏ္ဍအရွယ်)];
        this.သာတန်ဖိုးဖတ် = သာတန်ဖိုးဖတ်;
    }

    public int ကဏ္ဍအရေအတွက်() {
        return ဒေတာ.length / ကဏ္ဍအရွယ်;
    }

    public void ဖတ်(int ကဏ္ဍအညွှန်းကိန်း, byte[] ဦးတည်ရာလက်ခံရယူ) {
        အပိုင်းအခြားစစ်(ကဏ္ဍအညွှန်းကိန်း, ဦးတည်ရာလက်ခံရယူ);
        System.arraycopy(ဒေတာ, ကဏ္ဍအညွှန်းကိန်း * ကဏ္ဍအရွယ်, ဦးတည်ရာလက်ခံရယူ, 0, ကဏ္ဍအရွယ်);
    }

    public void ရေး(int ကဏ္ဍအညွှန်းကိန်း, byte[] ရေးမည့်ဒေတာ) {
        if (သာတန်ဖိုးဖတ်) {
            throw new IllegalStateException("ဖတ် 전용 장치입니다.");
        }
        အပိုင်းအခြားစစ်(ကဏ္ဍအညွှန်းကိန်း, ရေးမည့်ဒေတာ);
        System.arraycopy(ရေးမည့်ဒေတာ, 0, ဒေတာ, ကဏ္ဍအညွှန်းကိန်း * ကဏ္ဍအရွယ်, ကဏ္ဍအရွယ်);
    }

    public void အချက်ဖျက်() {
        if (သာတန်ဖိုးဖတ်) {
            throw new IllegalStateException("ဖတ် 전용 장치입니다.");
        }
        Arrays.fill(ဒေတာ, (byte) 0);
    }

    private void အပိုင်းအခြားစစ်(int ကဏ္ဍအညွှန်းကိန်း, byte[] ယာယီနေရာလပ်) {
        if (ကဏ္ဍအညွှန်းကိန်း < 0 || ကဏ္ဍအညွှန်းကိန်း >= ကဏ္ဍအရေအတွက်() || ယာယီနေရာလပ်.length < ကဏ္ဍအရွယ်) {
            throw new IllegalArgumentException("ATA ကဏ္ဍတန်ဖိုး 범위가 올바르지 않습니다.");
        }
    }
}

