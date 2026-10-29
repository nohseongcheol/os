// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.util.ArrayList;
/** داخلا_فهرست(目錄): 순서가 있는 항목의 모음. 이 판은 اسٽرنگ_قدر 목록을 제공한다. */
public final class داخلا_فهرست {
    private final ArrayList<String> داخلا_قدر = new ArrayList<String>();
    public void 더하기(String قدر) { داخلا_قدر.add(قدر); }
    public String 읽기(int ترتيب_قدر) { return داخلا_قدر.get(ترتيب_قدر); }
    public String بدلو_قدر(int ترتيب_قدر, String قدر) { return داخلا_قدر.set(ترتيب_قدر, قدر); }
    public String 지우기(int ترتيب_قدر) { return داخلا_قدر.remove(ترتيب_قدر); }
    public int سائيز() { return داخلا_قدر.size(); }
    public boolean 비었는가() { return داخلا_قدر.isEmpty(); }
    public void صاف_ڪريو_موادَ() { داخلا_قدر.clear(); }
}
