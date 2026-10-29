// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.util.ArrayList;
/** унос_списак(目錄): 순서가 있는 항목의 모음. 이 판은 стринг_вриједност 목록을 제공한다. */
public final class унос_списак {
    private final ArrayList<String> унос_вриједност = new ArrayList<String>();
    public void 더하기(String вриједност) { унос_вриједност.add(вриједност); }
    public String 읽기(int редослијед_сортирања_вриједност) { return унос_вриједност.get(редослијед_сортирања_вриједност); }
    public String замијенити_вриједност(int редослијед_сортирања_вриједност, String вриједност) { return унос_вриједност.set(редослијед_сортирања_вриједност, вриједност); }
    public String 지우기(int редослијед_сортирања_вриједност) { return унос_вриједност.remove(редослијед_сортирања_вриједност); }
    public int подесити_величину() { return унос_вриједност.size(); }
    public boolean 비었는가() { return унос_вриједност.isEmpty(); }
    public void избрисати_TOC() { унос_вриједност.clear(); }
}
