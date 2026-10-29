// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package မြန်မာ.ကိုယ်ပိုင်;

/** မြန်မာ API တွင် ကြေညာ၊ ပစ်ထုတ်၊ ဖမ်းယူနိုင်သော သင်္ချာခြွင်းချက်။ */
public class သင်္ချာခြွင်းချက် extends java.lang.ArithmeticException {
    public သင်္ချာခြွင်းချက်() { super(); }
    public သင်္ချာခြွင်းချက်(String ရှင်းလင်းချက်) { super(ရှင်းလင်းချက်); }
    public String ရှင်းလင်းချက်() { return getMessage(); }
}
