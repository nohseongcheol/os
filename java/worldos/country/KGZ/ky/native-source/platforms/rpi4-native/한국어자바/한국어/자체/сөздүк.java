// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.util.HashMap;
/** сөздүк(辭典): 찾는 Сөз_СМС(열쇠)에 값을 대응시킨다. */
public final class сөздүк {
    private final HashMap<String, String> киргизме_жазуу_маани = new HashMap<String, String>();
    public String 넣기(String 열쇠, String маани) { return киргизме_жазуу_маани.put(열쇠, маани); }
    public String табуу_киргизме_жазуу(String 열쇠) { return киргизме_жазуу_маани.get(열쇠); }
    public boolean 있는가(String 열쇠) { return киргизме_жазуу_маани.containsKey(열쇠); }
    public String 지우기(String 열쇠) { return киргизме_жазуу_маани.remove(열쇠); }
    public int Өлчөмү() { return киргизме_жазуу_маани.size(); }
    public void тазалоо_мазмуну() { киргизме_жазуу_маани.clear(); }
}
