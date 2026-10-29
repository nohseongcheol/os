// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.util.ArrayList;
/** унос_Листа(目錄): 순서가 있는 항목의 모음. 이 판은 ниска_вриједност 목록을 제공한다. */
public final class унос_Листа {
    private final ArrayList<String> унос_вриједност = new ArrayList<String>();
    public void 더하기(String вриједност) { унос_вриједност.add(вриједност); }
    public String Чита(int поредати_вриједност) { return унос_вриједност.get(поредати_вриједност); }
    public String замијенити_вриједност(int поредати_вриједност, String вриједност) { return унос_вриједност.set(поредати_вриједност, вриједност); }
    public String 지우기(int поредати_вриједност) { return унос_вриједност.remove(поредати_вриједност); }
    public int Величина() { return унос_вриједност.size(); }
    public boolean информатичко_одељење_празно_вриједност() { return унос_вриједност.isEmpty(); }
    public void обрисати_Садржај() { унос_вриједност.clear(); }
}
