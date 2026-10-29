// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.util.ArrayList;
/** futje_Listë(目錄): 순서가 있는 항목의 모음. 이 판은 varg_VALUE 목록을 제공한다. */
public final class futje_Listë {
    private final ArrayList<String> futje_VALUE = new ArrayList<String>();
    public void 더하기(String VALUE) { futje_VALUE.add(VALUE); }
    public String Leximi(int renditja_VALUE) { return futje_VALUE.get(renditja_VALUE); }
    public String REPLACE_VALUE(int renditja_VALUE, String VALUE) { return futje_VALUE.set(renditja_VALUE, VALUE); }
    public String spastroj_futje(int renditja_VALUE) { return futje_VALUE.remove(renditja_VALUE); }
    public int Madhësi() { return futje_VALUE.size(); }
    public boolean teknologjia_e_informacionit_bosh_VALUE() { return futje_VALUE.isEmpty(); }
    public void pastroj_TOC() { futje_VALUE.clear(); }
}
