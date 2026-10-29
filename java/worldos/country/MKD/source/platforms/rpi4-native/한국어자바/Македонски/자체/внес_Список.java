// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Македонски.자체;
import java.util.ArrayList;
/** внес_Список(目錄): 순서가 있는 항목의 모음. 이 판은 низа_VALUE_6ca8363c 목록을 제공한다. */
public final class внес_Список {
    private final ArrayList<String> внес_VALUE = new ArrayList<String>();
    public void 더하기(String VALUE) { внес_VALUE.add(VALUE); }
    public String Читај(int редослед_VALUE) { return внес_VALUE.get(редослед_VALUE); }
    public String замени_VALUE(int редослед_VALUE, String VALUE) { return внес_VALUE.set(редослед_VALUE, VALUE); }
    public String избриши_внес(int редослед_VALUE) { return внес_VALUE.remove(редослед_VALUE); }
    public int Големина() { return внес_VALUE.size(); }
    public boolean информатичка_технологија_празно_VALUE() { return внес_VALUE.isEmpty(); }
    public void исчисти_Содржина() { внес_VALUE.clear(); }
}
