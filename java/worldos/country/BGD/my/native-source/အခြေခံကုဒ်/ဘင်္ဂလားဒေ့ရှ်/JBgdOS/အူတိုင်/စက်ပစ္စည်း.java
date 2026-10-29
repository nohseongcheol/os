// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ဘင်္ဂလားဒေ့ရှ်.JBgdOS.အူတိုင်;

/** Java စီမံအူတိုင်နှင့် CPU သီးသန့်ကုဒ်အကြား တစ်ခုတည်းသော နယ်နိမိတ်။ */
public interface စက်ပစ္စည်း {
    void အစဉ်ဆက်အထွက်(String အကြောင်းအရာတန်ဖိုး);

    int ဆက်သွယ်ပေါက်ဘိုက်ဖတ်(int စက်ပစ္စည်းဆက်သွယ်ပေါက်ကိန်း);

    void ဆက်သွယ်ပေါက်ဘိုက်ရေး(int စက်ပစ္စည်းဆက်သွယ်ပေါက်ကိန်း, int တန်ဖိုး);

    void CPUရပ်();
}

