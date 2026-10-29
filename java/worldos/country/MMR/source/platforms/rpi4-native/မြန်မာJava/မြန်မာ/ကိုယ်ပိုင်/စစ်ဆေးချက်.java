// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package မြန်မာ.ကိုယ်ပိုင်;

/** စမ်းသပ်မှုနှင့် လုပ်ဆောင်ဥပမာများတွင် မျှော်လင့်ထားသော အခြေအနေကို စစ်ဆေးသည်။ */
public final class စစ်ဆေးချက် {
    private စစ်ဆေးချက်() {}
    public static void မှန်ကြောင်းစစ်(boolean အခြေအနေစည်းကမ်း, String မူလအကြောင်းရင်း) {
        if (!အခြေအနေစည်းကမ်း) throw new မမှန်ကန်ပေးအချက်ခြွင်းချက်(မူလအကြောင်းရင်း);
    }
}
