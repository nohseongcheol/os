// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package slovenščina.lastno;
import java.util.ArrayList;
/** vnos_Seznam(目錄): 순서가 있는 항목의 모음. 이 판은 niz_VALUE 목록을 제공한다. */
public final class vnos_Seznam {
    private final ArrayList<String> vnos_VALUE = new ArrayList<String>();
    public void 더하기(String VALUE) { vnos_VALUE.add(VALUE); }
    public String Branje(int naročilo_VALUE) { return vnos_VALUE.get(naročilo_VALUE); }
    public String REPLACE_VALUE(int naročilo_VALUE, String VALUE) { return vnos_VALUE.set(naročilo_VALUE, VALUE); }
    public String izbrisati_vnos(int naročilo_VALUE) { return vnos_VALUE.remove(naročilo_VALUE); }
    public int Velikost() { return vnos_VALUE.size(); }
    public boolean informacijska_tehnologija_prazen_VALUE() { return vnos_VALUE.isEmpty(); }
    public void počistiti_Vsebina() { vnos_VALUE.clear(); }
}
