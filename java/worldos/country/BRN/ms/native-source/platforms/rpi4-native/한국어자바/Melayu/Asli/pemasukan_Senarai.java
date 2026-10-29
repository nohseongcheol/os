// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Melayu.Asli;
import java.util.ArrayList;
/** pemasukan_Senarai(目錄): 순서가 있는 항목의 모음. 이 판은 rentetan_VALUE 목록을 제공한다. */
public final class pemasukan_Senarai {
    private final ArrayList<String> pemasukan_VALUE = new ArrayList<String>();
    public void 더하기(String VALUE) { pemasukan_VALUE.add(VALUE); }
    public String Baca(int tertib_VALUE) { return pemasukan_VALUE.get(tertib_VALUE); }
    public String ganti_VALUE(int tertib_VALUE, String VALUE) { return pemasukan_VALUE.set(tertib_VALUE, VALUE); }
    public String padam_pemasukan(int tertib_VALUE) { return pemasukan_VALUE.remove(tertib_VALUE); }
    public int Saiz() { return pemasukan_VALUE.size(); }
    public boolean 비었는가() { return pemasukan_VALUE.isEmpty(); }
    public void buang_TOC() { pemasukan_VALUE.clear(); }
}
