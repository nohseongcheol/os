// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package မြန်မာ.ကိုယ်ပိုင်;
import java.util.ArrayList;
/** အစဉ်ရှိသော အချက်များအစု။ ယခုမူသည် စာသားစာရင်းကို ပံ့ပိုးသည်။ */
public final class အချက်စာရင်း {
    private final ArrayList<String> အချက်တန်ဖိုး = new ArrayList<String>();
    public void တန်ဖိုးများထည့်(String တန်ဖိုး) { အချက်တန်ဖိုး.add(တန်ဖိုး); }
    public String ဖတ်(int အစဉ်တန်ဖိုး) { return အချက်တန်ဖိုး.get(အစဉ်တန်ဖိုး); }
    public String တန်ဖိုးအစားထိုး(int အစဉ်တန်ဖိုး, String တန်ဖိုး) { return အချက်တန်ဖိုး.set(အစဉ်တန်ဖိုး, တန်ဖိုး); }
    public String အချက်ဖျက်(int အစဉ်တန်ဖိုး) { return အချက်တန်ဖိုး.remove(အစဉ်တန်ဖိုး); }
    public int အရွယ်() { return အချက်တန်ဖိုး.size(); }
    public boolean ဖြစ်သောအလွတ်တန်ဖိုး() { return အချက်တန်ဖိုး.isEmpty(); }
    public void အကြောင်းအရာရှင်း() { အချက်တန်ဖိုး.clear(); }
}
