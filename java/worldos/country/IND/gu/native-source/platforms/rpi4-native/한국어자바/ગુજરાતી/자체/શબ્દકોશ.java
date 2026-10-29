// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ગુજરાતી.자체;
import java.util.HashMap;
/** શબ્દકોશ(辭典): 찾는 શબ્દ_પાઠ(열쇠)에 값을 대응시킨다. */
public final class શબ્દકોશ {
    private final HashMap<String, String> પ્રવેશ_મૂલ્ય = new HashMap<String, String>();
    public String 넣기(String 열쇠, String મૂલ્ય) { return પ્રવેશ_મૂલ્ય.put(열쇠, મૂલ્ય); }
    public String શોધો_પ્રવેશ(String 열쇠) { return પ્રવેશ_મૂલ્ય.get(열쇠); }
    public boolean 있는가(String 열쇠) { return પ્રવેશ_મૂલ્ય.containsKey(열쇠); }
    public String 지우기(String 열쇠) { return પ્રવેશ_મૂલ્ય.remove(열쇠); }
    public int માપ() { return પ્રવેશ_મૂલ્ય.size(); }
    public void 비우기() { પ્રવેશ_મૂલ્ય.clear(); }
}
