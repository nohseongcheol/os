// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package فارسی.بومی;
import java.util.HashMap;
/** لغت_نامه(辭典): 찾는 کلمات_متن(열쇠)에 값을 대응시킨다. */
public final class لغت_نامه {
    private final HashMap<String, String> ورودی_مقدار = new HashMap<String, String>();
    public String 넣기(String 열쇠, String مقدار) { return ورودی_مقدار.put(열쇠, مقدار); }
    public String کشف_ورودی(String 열쇠) { return ورودی_مقدار.get(열쇠); }
    public boolean 있는가(String 열쇠) { return ورودی_مقدار.containsKey(열쇠); }
    public String پاک_کردن_ورودی(String 열쇠) { return ورودی_مقدار.remove(열쇠); }
    public int اندازه() { return ورودی_مقدار.size(); }
    public void پاک_کردن_مطالب() { ورودی_مقدار.clear(); }
}
