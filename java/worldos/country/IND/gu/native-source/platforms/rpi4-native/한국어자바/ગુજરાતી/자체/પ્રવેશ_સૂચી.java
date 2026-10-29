// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ગુજરાતી.자체;
import java.util.ArrayList;
/** પ્રવેશ_સૂચી(目錄): 순서가 있는 항목의 모음. 이 판은 સ્ટ્રિંગ_મૂલ્ય 목록을 제공한다. */
public final class પ્રવેશ_સૂચી {
    private final ArrayList<String> પ્રવેશ_મૂલ્ય = new ArrayList<String>();
    public void 더하기(String મૂલ્ય) { પ્રવેશ_મૂલ્ય.add(મૂલ્ય); }
    public String વાંચો(int ક્રમ_મૂલ્ય) { return પ્રવેશ_મૂલ્ય.get(ક્રમ_મૂલ્ય); }
    public String બદલો_મૂલ્ય(int ક્રમ_મૂલ્ય, String મૂલ્ય) { return પ્રવેશ_મૂલ્ય.set(ક્રમ_મૂલ્ય, મૂલ્ય); }
    public String 지우기(int ક્રમ_મૂલ્ય) { return પ્રવેશ_મૂલ્ય.remove(ક્રમ_મૂલ્ય); }
    public int માપ() { return પ્રવેશ_મૂલ્ય.size(); }
    public boolean ઇન્ટરમિટેંટ_ખાલી_મૂલ્ય() { return પ્રવેશ_મૂલ્ય.isEmpty(); }
    public void 비우기() { પ્રવેશ_મૂલ્ય.clear(); }
}
