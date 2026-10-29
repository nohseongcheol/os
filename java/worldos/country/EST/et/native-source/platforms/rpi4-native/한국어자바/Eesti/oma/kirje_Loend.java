// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Eesti.oma;
import java.util.ArrayList;
/** kirje_Loend(目錄): 순서가 있는 항목의 모음. 이 판은 string_VALUE 목록을 제공한다. */
public final class kirje_Loend {
    private final ArrayList<String> kirje_VALUE = new ArrayList<String>();
    public void 더하기(String VALUE) { kirje_VALUE.add(VALUE); }
    public String Lugemine(int tellimus_VALUE) { return kirje_VALUE.get(tellimus_VALUE); }
    public String REPLACE_VALUE(int tellimus_VALUE, String VALUE) { return kirje_VALUE.set(tellimus_VALUE, VALUE); }
    public String kustutama_kirje(int tellimus_VALUE) { return kirje_VALUE.remove(tellimus_VALUE); }
    public int Suurus() { return kirje_VALUE.size(); }
    public boolean 비었는가() { return kirje_VALUE.isEmpty(); }
    public void eemaldama_Sisu() { kirje_VALUE.clear(); }
}
