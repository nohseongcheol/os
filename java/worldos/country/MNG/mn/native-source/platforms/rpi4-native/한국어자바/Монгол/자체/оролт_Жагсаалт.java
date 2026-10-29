// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Монгол.자체;
import java.util.ArrayList;
/** оролт_Жагсаалт(目錄): 순서가 있는 항목의 모음. 이 판은 мөр_утга_6ca8363c 목록을 제공한다. */
public final class оролт_Жагсаалт {
    private final ArrayList<String> оролт_утга = new ArrayList<String>();
    public void 더하기(String утга) { оролт_утга.add(утга); }
    public String Унших(int дараалал_утга) { return оролт_утга.get(дараалал_утга); }
    public String байрлуулах_утга(int дараалал_утга, String утга) { return оролт_утга.set(дараалал_утга, утга); }
    public String 지우기(int дараалал_утга) { return оролт_утга.remove(дараалал_утга); }
    public int Хэмжээ() { return оролт_утга.size(); }
    public boolean 비었는가() { return оролт_утга.isEmpty(); }
    public void арилгах_гарчиг() { оролт_утга.clear(); }
}
