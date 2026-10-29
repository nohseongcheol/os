// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Татарча.자체;
import java.util.HashMap;
/** сүзлек(辭典): 찾는 Word_СМС(열쇠)에 값을 대응시킨다. */
public final class сүзлек {
    private final HashMap<String, String> кертү_VALUE = new HashMap<String, String>();
    public String 넣기(String 열쇠, String VALUE) { return кертү_VALUE.put(열쇠, VALUE); }
    public String FIND_кертү(String 열쇠) { return кертү_VALUE.get(열쇠); }
    public boolean 있는가(String 열쇠) { return кертү_VALUE.containsKey(열쇠); }
    public String 지우기(String 열쇠) { return кертү_VALUE.remove(열쇠); }
    public int үлчәмен_үзгәртү() { return кертү_VALUE.size(); }
    public void чистарту_Эчтәлек() { кертү_VALUE.clear(); }
}
