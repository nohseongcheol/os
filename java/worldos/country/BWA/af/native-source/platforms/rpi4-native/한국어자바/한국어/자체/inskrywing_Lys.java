// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.util.ArrayList;
/** inskrywing_Lys(目錄): 순서가 있는 항목의 모음. 이 판은 string_VALUE 목록을 제공한다. */
public final class inskrywing_Lys {
    private final ArrayList<String> inskrywing_VALUE = new ArrayList<String>();
    public void 더하기(String VALUE) { inskrywing_VALUE.add(VALUE); }
    public String Lees(int volgorde_VALUE) { return inskrywing_VALUE.get(volgorde_VALUE); }
    public String REPLACE_VALUE(int volgorde_VALUE, String VALUE) { return inskrywing_VALUE.set(volgorde_VALUE, VALUE); }
    public String vee_uit_inskrywing(int volgorde_VALUE) { return inskrywing_VALUE.remove(volgorde_VALUE); }
    public int Grootte() { return inskrywing_VALUE.size(); }
    public boolean 비었는가() { return inskrywing_VALUE.isEmpty(); }
    public void vee_uit_inhoud() { inskrywing_VALUE.clear(); }
}
