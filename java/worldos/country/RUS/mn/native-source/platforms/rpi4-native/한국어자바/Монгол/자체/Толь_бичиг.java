// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Монгол.자체;
import java.util.HashMap;
/** Толь_бичиг(辭典): 찾는 Үгэн_Бичвэр(열쇠)에 값을 대응시킨다. */
public final class Толь_бичиг {
    private final HashMap<String, String> оролт_утга = new HashMap<String, String>();
    public String 넣기(String 열쇠, String утга) { return оролт_утга.put(열쇠, утга); }
    public String хайх_оролт(String 열쇠) { return оролт_утга.get(열쇠); }
    public boolean 있는가(String 열쇠) { return оролт_утга.containsKey(열쇠); }
    public String 지우기(String 열쇠) { return оролт_утга.remove(열쇠); }
    public int Хэмжээ() { return оролт_утга.size(); }
    public void арилгах_гарчиг() { оролт_утга.clear(); }
}
