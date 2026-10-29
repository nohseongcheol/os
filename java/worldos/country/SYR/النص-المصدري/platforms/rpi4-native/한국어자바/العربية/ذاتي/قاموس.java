// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package العربية.ذاتي;
import java.util.HashMap;
/** قاموس(辭典): 찾는 الكلمات_نص(열쇠)에 값을 대응시킨다. */
public final class قاموس {
    private final HashMap<String, String> إدخال_قيمة_962f286b = new HashMap<String, String>();
    public String 넣기(String 열쇠, String قيمة) { return إدخال_قيمة_962f286b.put(열쇠, قيمة); }
    public String بحث_إدخال(String 열쇠) { return إدخال_قيمة_962f286b.get(열쇠); }
    public boolean 있는가(String 열쇠) { return إدخال_قيمة_962f286b.containsKey(열쇠); }
    public String مسح_إدخال(String 열쇠) { return إدخال_قيمة_962f286b.remove(열쇠); }
    public int حجم() { return إدخال_قيمة_962f286b.size(); }
    public void مسح_المحتويات() { إدخال_قيمة_962f286b.clear(); }
}
