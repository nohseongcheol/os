// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package فارسی.بومی;
import java.util.ArrayList;
/** ورودی_لیست(目錄): 순서가 있는 항목의 모음. 이 판은 رشته_مقدار_6ca8363c 목록을 제공한다. */
public final class ورودی_لیست {
    private final ArrayList<String> ورودی_مقدار = new ArrayList<String>();
    public void 더하기(String مقدار) { ورودی_مقدار.add(مقدار); }
    public String خواندن(int ترتیب_مقدار) { return ورودی_مقدار.get(ترتیب_مقدار); }
    public String تغییر_مکان_مقدار(int ترتیب_مقدار, String مقدار) { return ورودی_مقدار.set(ترتیب_مقدار, مقدار); }
    public String پاک_کردن_ورودی(int ترتیب_مقدار) { return ورودی_مقدار.remove(ترتیب_مقدار); }
    public int اندازه() { return ورودی_مقدار.size(); }
    public boolean فناوری_اطلاعات_خالی_مقدار() { return ورودی_مقدار.isEmpty(); }
    public void پاک_کردن_مطالب() { ورودی_مقدار.clear(); }
}
