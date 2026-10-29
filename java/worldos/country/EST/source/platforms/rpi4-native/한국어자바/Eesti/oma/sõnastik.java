// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Eesti.oma;
import java.util.HashMap;
/** sõnastik(辭典): 찾는 Word_SMS(열쇠)에 값을 대응시킨다. */
public final class sõnastik {
    private final HashMap<String, String> kirje_VALUE = new HashMap<String, String>();
    public String 넣기(String 열쇠, String VALUE) { return kirje_VALUE.put(열쇠, VALUE); }
    public String FIND_kirje(String 열쇠) { return kirje_VALUE.get(열쇠); }
    public boolean 있는가(String 열쇠) { return kirje_VALUE.containsKey(열쇠); }
    public String kustutama_kirje(String 열쇠) { return kirje_VALUE.remove(열쇠); }
    public int Suurus() { return kirje_VALUE.size(); }
    public void eemaldama_Sisu() { kirje_VALUE.clear(); }
}
