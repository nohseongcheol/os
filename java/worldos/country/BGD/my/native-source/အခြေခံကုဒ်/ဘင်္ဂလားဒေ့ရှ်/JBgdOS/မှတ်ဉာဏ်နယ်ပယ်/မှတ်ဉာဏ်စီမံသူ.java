// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ဘင်္ဂလားဒေ့ရှ်.JBgdOS.မှတ်ဉာဏ်နယ်ပယ်;

import java.util.Arrays;
import java.util.Map;
import java.util.TreeMap;

/** ရုပ်ပိုင်းမှတ်ဉာဏ် ချိန်ညှိခွဲဝေမှု၊ လွှတ်မှုနှင့် ပေါင်းစည်းမှုကို တာဝန်ယူသည်။ */
public final class မှတ်ဉာဏ်စီမံသူ {
    private final byte[] မှတ်ဉာဏ်နယ်ပယ်;
    private final TreeMap<Integer, Integer> အလွတ်နယ်ပယ် = new TreeMap<Integer, Integer>();
    private final TreeMap<Integer, Integer> သုံးထားနယ်ပယ် = new TreeMap<Integer, Integer>();

    public မှတ်ဉာဏ်စီမံသူ(int အကုန်စုစုပေါင်းအရွယ်) {
        if (အကုန်စုစုပေါင်းအရွယ် < 8192) {
            throw new IllegalArgumentException("기억공간이 너무 작습니다.");
        }
        မှတ်ဉာဏ်နယ်ပယ် = new byte[အကုန်စုစုပေါင်းအရွယ်];
        အလွတ်နယ်ပယ်.put(Integer.valueOf(4096), Integer.valueOf(အကုန်စုစုပေါင်းအရွယ် - 4096));
    }

    public synchronized int သိုလှောင်ရာခွဲဝေ(int အရွယ်) {
        return ချိန်ညှိခွဲဝေ(အရွယ်, 1);
    }

    public synchronized int ချိန်ညှိခွဲဝေ(int အရွယ်, int ညှိတန်ဖိုး) {
        if (အရွယ် <= 0 || ညှိတန်ဖိုး <= 0 || (ညှိတန်ဖိုး & (ညှိတန်ဖိုး - 1)) != 0) {
            throw new IllegalArgumentException("크기와 정렬이 올바르지 않습니다.");
        }
        for (Map.Entry<Integer, Integer> အချက်တန်ဖိုး : အလွတ်နယ်ပယ်.entrySet()) {
            int လုပ်ဆောင် = အချက်တန်ဖိုး.getKey().intValue();
            int နယ်ပယ်အရွယ် = အချက်တန်ဖိုး.getValue().intValue();
            int ချိန်ညှိစမှတ် = (လုပ်ဆောင် + ညှိတန်ဖိုး - 1) & -ညှိတန်ဖိုး;
            int ရှေ့တန်ဖိုးအရွယ် = ချိန်ညှိစမှတ် - လုပ်ဆောင်;
            int နောက်ဆုံးပိတ်အရွယ် = နယ်ပယ်အရွယ် - ရှေ့တန်ဖိုးအရွယ် - အရွယ်;
            if (နောက်ဆုံးပိတ်အရွယ် < 0) {
                continue;
            }
            အလွတ်နယ်ပယ်.remove(Integer.valueOf(လုပ်ဆောင်));
            if (ရှေ့တန်ဖိုးအရွယ် > 0) {
                အလွတ်နယ်ပယ်.put(Integer.valueOf(လုပ်ဆောင်), Integer.valueOf(ရှေ့တန်ဖိုးအရွယ်));
            }
            if (နောက်ဆုံးပိတ်အရွယ် > 0) {
                အလွတ်နယ်ပယ်.put(Integer.valueOf(ချိန်ညှိစမှတ် + အရွယ်), Integer.valueOf(နောက်ဆုံးပိတ်အရွယ်));
            }
            သုံးထားနယ်ပယ်.put(Integer.valueOf(ချိန်ညှိစမှတ်), Integer.valueOf(အရွယ်));
            Arrays.fill(မှတ်ဉာဏ်နယ်ပယ်, ချိန်ညှိစမှတ်, ချိန်ညှိစမှတ် + အရွယ်, (byte) 0);
            return ချိန်ညှိစမှတ်;
        }
        throw new OutOfMemoryError("물리 기억공간이 부족합니다.");
    }

    public synchronized void သိုလှောင်ရာလွှတ်ပေး(int လိပ်စာ) {
        Integer အရွယ်အရာဝတ္ထု = သုံးထားနယ်ပယ်.remove(Integer.valueOf(လိပ်စာ));
        if (အရွယ်အရာဝတ္ထု == null) {
            throw new IllegalArgumentException("할당되지 않은 주소입니다.");
        }
        int လုပ်ဆောင် = လိပ်စာ;
        int အရွယ် = အရွယ်အရာဝတ္ထု.intValue();
        Map.Entry<Integer, Integer> ရှေ့တန်ဖိုး = အလွတ်နယ်ပယ်.lowerEntry(Integer.valueOf(လုပ်ဆောင်));
        if (ရှေ့တန်ဖိုး != null && ရှေ့တန်ဖိုး.getKey().intValue() + ရှေ့တန်ဖိုး.getValue().intValue() == လုပ်ဆောင်) {
            လုပ်ဆောင် = ရှေ့တန်ဖိုး.getKey().intValue();
            အရွယ် += ရှေ့တန်ဖိုး.getValue().intValue();
            အလွတ်နယ်ပယ်.remove(ရှေ့တန်ဖိုး.getKey());
        }
        Map.Entry<Integer, Integer> နောက်တန်ဖိုး = အလွတ်နယ်ပယ်.ceilingEntry(Integer.valueOf(လုပ်ဆောင်));
        if (နောက်တန်ဖိုး != null && လုပ်ဆောင် + အရွယ် == နောက်တန်ဖိုး.getKey().intValue()) {
            အရွယ် += နောက်တန်ဖိုး.getValue().intValue();
            အလွတ်နယ်ပယ်.remove(နောက်တန်ဖိုး.getKey());
        }
        အလွတ်နယ်ပယ်.put(Integer.valueOf(လုပ်ဆောင်), Integer.valueOf(အရွယ်));
    }

    public synchronized byte ဘိုက်တန်ဖိုးဖတ်(int လိပ်စာ) {
        အပိုင်းအခြားစစ်(လိပ်စာ, 1);
        return မှတ်ဉာဏ်နယ်ပယ်[လိပ်စာ];
    }

    public synchronized void ဘိုက်တန်ဖိုးရေး(int လိပ်စာ, byte တန်ဖိုး) {
        အပိုင်းအခြားစစ်(လိပ်စာ, 1);
        မှတ်ဉာဏ်နယ်ပယ်[လိပ်စာ] = တန်ဖိုး;
    }

    public synchronized int အကုန်စုစုပေါင်းအရွယ်() {
        return မှတ်ဉာဏ်နယ်ပယ်.length;
    }

    public synchronized int သုံးထားအရွယ်() {
        int အကုန်စုစုပေါင်းတန်ဖိုး = 0;
        for (Integer အရွယ် : သုံးထားနယ်ပယ်.values()) {
            အကုန်စုစုပေါင်းတန်ဖိုး += အရွယ်.intValue();
        }
        return အကုန်စုစုပေါင်းတန်ဖိုး;
    }

    private void အပိုင်းအခြားစစ်(int လိပ်စာ, int အရွယ်) {
        if (လိပ်စာ < 0 || အရွယ် < 0 || လိပ်စာ > မှတ်ဉာဏ်နယ်ပယ်.length - အရွယ်) {
            throw new IndexOutOfBoundsException("မှတ်ဉာဏ်နယ်ပယ် 범위를 벗어났습니다.");
        }
    }
}

