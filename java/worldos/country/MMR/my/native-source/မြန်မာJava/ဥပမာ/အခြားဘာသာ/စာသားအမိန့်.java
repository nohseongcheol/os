// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import မြန်မာ.Java.အက္ခရာ;

/** အခြားဘာသာများက စံအထွက်မှ ရလဒ်ယူနိုင်သော သေးငယ်သည့် Java ဝင်ခွင့်။ */
public final class စာသားအမိန့် {
    public static void main(String[] အချက်များ) {
        if (အချက်များ.length != 1) {
            System.err.println("사용법: စာသားအမိန့် အက္ခရာစဉ်");
            System.exit(2);
        }
        System.out.println(အက္ခရာ.ကုဒ်အမှတ်တစ်ခုအရေအတွက်(အချက်များ[0]));
    }
}
