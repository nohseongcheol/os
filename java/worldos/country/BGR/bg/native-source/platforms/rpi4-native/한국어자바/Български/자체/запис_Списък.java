// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Български.자체;
import java.util.ArrayList;
/** запис_Списък(目錄): 순서가 있는 항목의 모음. 이 판은 низ_стойност 목록을 제공한다. */
public final class запис_Списък {
    private final ArrayList<String> запис_стойност = new ArrayList<String>();
    public void 더하기(String стойност) { запис_стойност.add(стойност); }
    public String Четене(int ред_стойност) { return запис_стойност.get(ред_стойност); }
    public String 바꾸기(int ред_стойност, String стойност) { return запис_стойност.set(ред_стойност, стойност); }
    public String изтривам_запис(int ред_стойност) { return запис_стойност.remove(ред_стойност); }
    public int Размер() { return запис_стойност.size(); }
    public boolean 비었는가() { return запис_стойност.isEmpty(); }
    public void изчиствам_Съдържание() { запис_стойност.clear(); }
}
