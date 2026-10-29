// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package اردو.اپنا;
import java.util.ArrayList;
/** اندراج_فہرست(目錄): 순서가 있는 항목의 모음. 이 판은 سلک_قدر 목록을 제공한다. */
public final class اندراج_فہرست {
    private final ArrayList<String> اندراج_قدر = new ArrayList<String>();
    public void 더하기(String قدر) { اندراج_قدر.add(قدر); }
    public String پڑھیں(int ترتیم_قدر) { return اندراج_قدر.get(ترتیم_قدر); }
    public String بدلیں_قدر(int ترتیم_قدر, String قدر) { return اندراج_قدر.set(ترتیم_قدر, قدر); }
    public String 지우기(int ترتیم_قدر) { return اندراج_قدر.remove(ترتیم_قدر); }
    public int حجم() { return اندراج_قدر.size(); }
    public boolean معلومات_ٹیکنالوجی_خالی_قدر() { return اندراج_قدر.isEmpty(); }
    public void صاف_مشمولات() { اندراج_قدر.clear(); }
}
