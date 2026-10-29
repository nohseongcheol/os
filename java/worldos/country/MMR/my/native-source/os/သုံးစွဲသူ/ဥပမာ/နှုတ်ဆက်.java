// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class နှုတ်ဆက် {
    public static int လုပ်ဆောင်() {
        သုံးစွဲသူ.ရေး("Hello from a separate Java ELF!\n");
        သုံးစွဲသူ.ရေး(သုံးစွဲသူ.လုပ်ဆောင်မှုခွင့်ပြုချက်() == 3 ? "USER MODE ring 3\n" : "WRONG PRIVILEGE\n");
        for (int နံပါတ် = 0; နံပါတ် < သုံးစွဲသူ.ပေးအချက်များအရေအတွက်(); နံပါတ်++) {
            သုံးစွဲသူ.ရေး("arg: "); သုံးစွဲသူ.ရေး(သုံးစွဲသူ.အချက်များ(နံပါတ်)); သုံးစွဲသူ.ရေး("\n");
        }
        return သုံးစွဲသူ.လုပ်ဆောင်မှုခွင့်ပြုချက်() == 3 ? 0 : 1;
    }
}
