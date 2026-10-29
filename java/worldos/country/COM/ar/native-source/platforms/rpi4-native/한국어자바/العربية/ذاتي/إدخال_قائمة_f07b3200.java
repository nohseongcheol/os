// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package العربية.ذاتي;
import java.util.ArrayList;
/** إدخال_قائمة_f07b3200(目錄): 순서가 있는 항목의 모음. 이 판은 سلسلة_قيمة 목록을 제공한다. */
public final class إدخال_قائمة_f07b3200 {
    private final ArrayList<String> إدخال_قيمة_962f286b = new ArrayList<String>();
    public void 더하기(String قيمة) { إدخال_قيمة_962f286b.add(قيمة); }
    public String قراءة(int أمر_قيمة) { return إدخال_قيمة_962f286b.get(أمر_قيمة); }
    public String 바꾸기(int أمر_قيمة, String قيمة) { return إدخال_قيمة_962f286b.set(أمر_قيمة, قيمة); }
    public String مسح_إدخال(int أمر_قيمة) { return إدخال_قيمة_962f286b.remove(أمر_قيمة); }
    public int حجم() { return إدخال_قيمة_962f286b.size(); }
    public boolean أنظمة_المعلومات_فارغ_قيمة() { return إدخال_قيمة_962f286b.isEmpty(); }
    public void مسح_المحتويات() { إدخال_قيمة_962f286b.clear(); }
}
