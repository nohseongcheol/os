// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package עברית.עצמי;
import java.util.ArrayList;
/** ערך_רשימה(目錄): 순서가 있는 항목의 모음. 이 판은 מחרוזת_ערך 목록을 제공한다. */
public final class ערך_רשימה {
    private final ArrayList<String> ערך_ערך = new ArrayList<String>();
    public void 더하기(String ערך) { ערך_ערך.add(ערך); }
    public String קרא(int סדר_ערך) { return ערך_ערך.get(סדר_ערך); }
    public String 바꾸기(int סדר_ערך, String ערך) { return ערך_ערך.set(סדר_ערך, ערך); }
    public String מחק_ערך(int סדר_ערך) { return ערך_ערך.remove(סדר_ערך); }
    public int גודל() { return ערך_ערך.size(); }
    public boolean מערכות_מידע_ריק_ערך() { return ערך_ערך.isEmpty(); }
    public void נקה_תוכן() { ערך_ערך.clear(); }
}
