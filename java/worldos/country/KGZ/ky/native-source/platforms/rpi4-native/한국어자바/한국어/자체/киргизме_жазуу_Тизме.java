// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.util.ArrayList;
/** киргизме_жазуу_Тизме(目錄): 순서가 있는 항목의 모음. 이 판은 сап_маани 목록을 제공한다. */
public final class киргизме_жазуу_Тизме {
    private final ArrayList<String> киргизме_жазуу_маани = new ArrayList<String>();
    public void 더하기(String маани) { киргизме_жазуу_маани.add(маани); }
    public String Окуу(int ылгоо_ирети_маани) { return киргизме_жазуу_маани.get(ылгоо_ирети_маани); }
    public String орун_алмаштыруу_маани(int ылгоо_ирети_маани, String маани) { return киргизме_жазуу_маани.set(ылгоо_ирети_маани, маани); }
    public String 지우기(int ылгоо_ирети_маани) { return киргизме_жазуу_маани.remove(ылгоо_ирети_маани); }
    public int Өлчөмү() { return киргизме_жазуу_маани.size(); }
    public boolean 비었는가() { return киргизме_жазуу_маани.isEmpty(); }
    public void тазалоо_мазмуну() { киргизме_жазуу_маани.clear(); }
}
