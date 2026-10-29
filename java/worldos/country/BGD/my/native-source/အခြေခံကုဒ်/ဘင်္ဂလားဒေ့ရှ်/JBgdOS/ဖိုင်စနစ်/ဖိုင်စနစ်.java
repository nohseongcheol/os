// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ဘင်္ဂလားဒေ့ရှ်.JBgdOS.ဖိုင်စနစ်;

import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.Locale;
import java.util.Map;

/** engos FAT ဖတ်အလွှာနှင့် တူညီသော ဖတ်ရန်သာ ဖိုင်သိုလှောင်ရာ၏ စီမံပုံစံ။ */
public final class ဖိုင်စနစ် {
    static final class ဖွင့်ထားဖိုင် {
        final byte[] ဒေတာ;
        int နေရာ;
        int ကိုးကားချက်အရေအတွက် = 1;

        ဖွင့်ထားဖိုင်(byte[] ဒေတာ) {
            this.ဒေတာ = ဒေတာ;
        }
    }

    private final Map<String, byte[]> ဖိုင်အချက်များ = new LinkedHashMap<String, byte[]>();

    public void ဖိုင်နောက်တွဲ(String အမည်, byte[] ဒေတာ) {
        ဖိုင်အချက်များ.put(စံအမည်(အမည်), Arrays.copyOf(ဒေတာ, ဒေတာ.length));
    }

    ဖွင့်ထားဖိုင် ဖွင့်(String အမည်) {
        byte[] ဒေတာ = ဖိုင်အချက်များ.get(စံအမည်(အမည်));
        if (ဒေတာ == null) {
            return null;
        }
        return new ဖွင့်ထားဖိုင်(ဒေတာ);
    }

    public boolean တည်ရှိမှု(String အမည်) {
        return ဖိုင်အချက်များ.containsKey(စံအမည်(အမည်));
    }

    public ဖိုင်အချက်အလက် စနစ်သတင်းအချက်အလက်(String အမည်) {
        byte[] ဒေတာ = ဖိုင်အချက်များ.get(စံအမည်(အမည်));
        if (ဒေတာ == null) {
            return null;
        }
        return new ဖိုင်အချက်အလက်(ဒေတာ.length, 0100444);
    }

    private String စံအမည်(String အမည်) {
        if (အမည် == null) {
            throw new NullPointerException("ဖိုင် 이름이 없습니다.");
        }
        String ရလဒ် = အမည်.startsWith("/") ? အမည်.substring(1) : အမည်;
        return ရလဒ်.toUpperCase(Locale.ROOT);
    }
}
