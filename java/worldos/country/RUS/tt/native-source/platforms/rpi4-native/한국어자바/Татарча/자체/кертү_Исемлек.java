// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Татарча.자체;
import java.util.ArrayList;
/** кертү_Исемлек(目錄): 순서가 있는 항목의 모음. 이 판은 юл_VALUE_6ca8363c 목록을 제공한다. */
public final class кертү_Исемлек {
    private final ArrayList<String> кертү_VALUE = new ArrayList<String>();
    public void 더하기(String VALUE) { кертү_VALUE.add(VALUE); }
    public String 읽기(int тәртипкә_салу_VALUE) { return кертү_VALUE.get(тәртипкә_салу_VALUE); }
    public String REPLACE_VALUE(int тәртипкә_салу_VALUE, String VALUE) { return кертү_VALUE.set(тәртипкә_салу_VALUE, VALUE); }
    public String 지우기(int тәртипкә_салу_VALUE) { return кертү_VALUE.remove(тәртипкә_салу_VALUE); }
    public int үлчәмен_үзгәртү() { return кертү_VALUE.size(); }
    public boolean 비었는가() { return кертү_VALUE.isEmpty(); }
    public void чистарту_Эчтәлек() { кертү_VALUE.clear(); }
}
