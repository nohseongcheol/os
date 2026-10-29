// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package اردو.اپنا;
import java.util.HashMap;
/** لغت(辭典): 찾는 الفاظ_متن(열쇠)에 값을 대응시킨다. */
public final class لغت {
    private final HashMap<String, String> اندراج_قدر = new HashMap<String, String>();
    public String 넣기(String 열쇠, String قدر) { return اندراج_قدر.put(열쇠, قدر); }
    public String ڈھونڈیں_اندراج(String 열쇠) { return اندراج_قدر.get(열쇠); }
    public boolean 있는가(String 열쇠) { return اندراج_قدر.containsKey(열쇠); }
    public String 지우기(String 열쇠) { return اندراج_قدر.remove(열쇠); }
    public int حجم() { return اندراج_قدر.size(); }
    public void صاف_مشمولات() { اندراج_قدر.clear(); }
}
