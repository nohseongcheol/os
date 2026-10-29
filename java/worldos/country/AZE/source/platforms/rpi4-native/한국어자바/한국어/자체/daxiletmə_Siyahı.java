// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.util.ArrayList;
/** daxiletmə_Siyahı(目錄): 순서가 있는 항목의 모음. 이 판은 sətir_VALUE 목록을 제공한다. */
public final class daxiletmə_Siyahı {
    private final ArrayList<String> daxiletmə_VALUE = new ArrayList<String>();
    public void 더하기(String VALUE) { daxiletmə_VALUE.add(VALUE); }
    public String Oxuma(int ardıcıllıq_VALUE) { return daxiletmə_VALUE.get(ardıcıllıq_VALUE); }
    public String REPLACE_VALUE(int ardıcıllıq_VALUE, String VALUE) { return daxiletmə_VALUE.set(ardıcıllıq_VALUE, VALUE); }
    public String silmək_daxiletmə_c8dbc399(int ardıcıllıq_VALUE) { return daxiletmə_VALUE.remove(ardıcıllıq_VALUE); }
    public int Böyüklük() { return daxiletmə_VALUE.size(); }
    public boolean 비었는가() { return daxiletmə_VALUE.isEmpty(); }
    public void təmizləmək_TOC() { daxiletmə_VALUE.clear(); }
}
