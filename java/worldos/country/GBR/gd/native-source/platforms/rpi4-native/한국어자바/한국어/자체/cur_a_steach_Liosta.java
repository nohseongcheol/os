// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.util.ArrayList;
/** cur_a_steach_Liosta(目錄): 순서가 있는 항목의 모음. 이 판은 sreang_VALUE 목록을 제공한다. */
public final class cur_a_steach_Liosta {
    private final ArrayList<String> cur_a_steach_VALUE = new ArrayList<String>();
    public void 더하기(String VALUE) { cur_a_steach_VALUE.add(VALUE); }
    public String 읽기(int òrdugh_VALUE) { return cur_a_steach_VALUE.get(òrdugh_VALUE); }
    public String REPLACE_VALUE(int òrdugh_VALUE, String VALUE) { return cur_a_steach_VALUE.set(òrdugh_VALUE, VALUE); }
    public String 지우기(int òrdugh_VALUE) { return cur_a_steach_VALUE.remove(òrdugh_VALUE); }
    public int atharraich_am_meud() { return cur_a_steach_VALUE.size(); }
    public boolean 비었는가() { return cur_a_steach_VALUE.isEmpty(); }
    public void glan_susbaint() { cur_a_steach_VALUE.clear(); }
}
