// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Български.자체;
import java.util.HashMap;
/** речник(辭典): 찾는 Игри_с_думи_Текст(열쇠)에 값을 대응시킨다. */
public final class речник {
    private final HashMap<String, String> запис_стойност = new HashMap<String, String>();
    public String 넣기(String 열쇠, String стойност) { return запис_стойност.put(열쇠, стойност); }
    public String Търсене_запис(String 열쇠) { return запис_стойност.get(열쇠); }
    public boolean 있는가(String 열쇠) { return запис_стойност.containsKey(열쇠); }
    public String изтривам_запис(String 열쇠) { return запис_стойност.remove(열쇠); }
    public int Размер() { return запис_стойност.size(); }
    public void изчиствам_Съдържание() { запис_стойност.clear(); }
}
