// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package မြန်မာ.ကိုယ်ပိုင်;

/** အလုပ်ကိုယ်တိုင် ပြီးဆုံးမှု မဟုတ်ဘဲ အလုပ်ကြိုးကို စောင့်နေသော လုပ်ဆောင်မှု ပြတ်တောက်ခြင်းကို ဖော်ပြသည်။ */
public class စောင့်ဆိုင်းပြတ်ခြွင်းချက် extends java.lang.InterruptedException {
    public စောင့်ဆိုင်းပြတ်ခြွင်းချက်() { super(); }
    public စောင့်ဆိုင်းပြတ်ခြွင်းချက်(String ရှင်းလင်းချက်) { super(ရှင်းလင်းချက်); }
    public String ရှင်းလင်းချက်() { return getMessage(); }
}
