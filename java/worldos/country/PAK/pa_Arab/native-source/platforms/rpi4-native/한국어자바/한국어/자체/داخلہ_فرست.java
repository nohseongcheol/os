// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.util.ArrayList;
/** داخلہ_فرست(目錄): 순서가 있는 항목의 모음. 이 판은 سٹرنگ_قدر 목록을 제공한다. */
public final class داخلہ_فرست {
    private final ArrayList<String> داخلہ_قدر = new ArrayList<String>();
    public void 더하기(String قدر) { داخلہ_قدر.add(قدر); }
    public String 읽기(int ترتیب_قدر) { return داخلہ_قدر.get(ترتیب_قدر); }
    public String بدلو_قدر(int ترتیب_قدر, String قدر) { return داخلہ_قدر.set(ترتیب_قدر, قدر); }
    public String 지우기(int ترتیب_قدر) { return داخلہ_قدر.remove(ترتیب_قدر); }
    public int سائز() { return داخلہ_قدر.size(); }
    public boolean 비었는가() { return داخلہ_قدر.isEmpty(); }
    public void صاف_کرو_مواد() { داخلہ_قدر.clear(); }
}
