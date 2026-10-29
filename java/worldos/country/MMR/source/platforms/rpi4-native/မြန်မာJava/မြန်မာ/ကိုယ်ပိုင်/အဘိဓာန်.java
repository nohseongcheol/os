// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package မြန်မာ.ကိုယ်ပိုင်;
import java.util.HashMap;
/** ရှာဖွေသော သော့စကားလုံးတစ်ခုစီကို တန်ဖိုးတစ်ခုနှင့် တွဲဖက်ပေးသော အဘိဓာန်။ */
public final class အဘိဓာန် {
    private final HashMap<String, String> အချက်တန်ဖိုး = new HashMap<String, String>();
    public String တန်ဖိုးထား(String အဓိကသော့, String တန်ဖိုး) { return အချက်တန်ဖိုး.put(အဓိကသော့, တန်ဖိုး); }
    public String အချက်ရှာ(String အဓိကသော့) { return အချက်တန်ဖိုး.get(အဓိကသော့); }
    public boolean ရှိသလား(String အဓိကသော့) { return အချက်တန်ဖိုး.containsKey(အဓိကသော့); }
    public String အချက်ဖျက်(String အဓိကသော့) { return အချက်တန်ဖိုး.remove(အဓိကသော့); }
    public int အရွယ်() { return အချက်တန်ဖိုး.size(); }
    public void အကြောင်းအရာရှင်း() { အချက်တန်ဖိုး.clear(); }
}
