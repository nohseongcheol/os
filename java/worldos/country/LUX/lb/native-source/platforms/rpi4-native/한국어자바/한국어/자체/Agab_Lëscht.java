// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.util.ArrayList;
/** Agab_Lëscht(目錄): 순서가 있는 항목의 모음. 이 판은 Zeechefolleg_VALUE 목록을 제공한다. */
public final class Agab_Lëscht {
    private final ArrayList<String> Agab_VALUE = new ArrayList<String>();
    public void 더하기(String VALUE) { Agab_VALUE.add(VALUE); }
    public String 읽기(int Reiefolleg_VALUE) { return Agab_VALUE.get(Reiefolleg_VALUE); }
    public String REPLACE_VALUE(int Reiefolleg_VALUE, String VALUE) { return Agab_VALUE.set(Reiefolleg_VALUE, VALUE); }
    public String 지우기(int Reiefolleg_VALUE) { return Agab_VALUE.remove(Reiefolleg_VALUE); }
    public int d_Gréisst_veränneren() { return Agab_VALUE.size(); }
    public boolean 비었는가() { return Agab_VALUE.isEmpty(); }
    public void läschen_Inhalt() { Agab_VALUE.clear(); }
}
