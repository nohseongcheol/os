// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ဘင်္ဂလားဒေ့ရှ်.JBgdOS.အိမ်ရှင်;

import java.util.HashMap;
import java.util.Map;
import ဘင်္ဂလားဒေ့ရှ်.JBgdOS.အူတိုင်.စက်ပစ္စည်း;

/** ရိုးရိုး JVM တွင် စီမံအူတိုင်ကို ပြန်ထုတ်နိုင်သော ရလဒ်ဖြင့် စမ်းသပ်ရန် စက်ပစ္စည်းအစားထိုး။ */
public final class အိမ်ရှင်စက်ပစ္စည်း implements စက်ပစ္စည်း {
    private final Map<Integer, Integer> စက်ပစ္စည်းဆက်သွယ်ပေါက်တန်ဖိုး = new HashMap<Integer, Integer>();
    private final StringBuilder အစဉ်ဆက်မှတ်တမ်း = new StringBuilder();

    @Override
    public void အစဉ်ဆက်အထွက်(String အကြောင်းအရာတန်ဖိုး) {
        အစဉ်ဆက်မှတ်တမ်း.append(အကြောင်းအရာတန်ဖိုး);
        System.out.print(အကြောင်းအရာတန်ဖိုး);
    }

    @Override
    public int ဆက်သွယ်ပေါက်ဘိုက်ဖတ်(int စက်ပစ္စည်းဆက်သွယ်ပေါက်ကိန်း) {
        Integer တန်ဖိုး = စက်ပစ္စည်းဆက်သွယ်ပေါက်တန်ဖိုး.get(Integer.valueOf(စက်ပစ္စည်းဆက်သွယ်ပေါက်ကိန်း));
        return တန်ဖိုး == null ? 0 : တန်ဖိုး.intValue();
    }

    @Override
    public void ဆက်သွယ်ပေါက်ဘိုက်ရေး(int စက်ပစ္စည်းဆက်သွယ်ပေါက်ကိန်း, int တန်ဖိုး) {
        စက်ပစ္စည်းဆက်သွယ်ပေါက်တန်ဖိုး.put(Integer.valueOf(စက်ပစ္စည်းဆက်သွယ်ပေါက်ကိန်း), Integer.valueOf(တန်ဖိုး & 0xff));
    }

    @Override
    public void CPUရပ်() {
        // အိမ်ရှင်စမ်းသပ်မှုတွင် နောက်ဖြစ်ရပ်ကို မစောင့်ဘဲ ချက်ချင်း ပြန်သည်။
    }

    public String အစဉ်ဆက်မှတ်တမ်း() {
        return အစဉ်ဆက်မှတ်တမ်း.toString();
    }
}

