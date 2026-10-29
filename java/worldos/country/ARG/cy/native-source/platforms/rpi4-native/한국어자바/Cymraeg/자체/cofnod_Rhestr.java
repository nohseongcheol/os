// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Cymraeg.자체;
import java.util.ArrayList;
/** cofnod_Rhestr(目錄): 순서가 있는 항목의 모음. 이 판은 testun_VALUE 목록을 제공한다. */
public final class cofnod_Rhestr {
    private final ArrayList<String> cofnod_VALUE = new ArrayList<String>();
    public void 더하기(String VALUE) { cofnod_VALUE.add(VALUE); }
    public String Darllen(int trefn_VALUE) { return cofnod_VALUE.get(trefn_VALUE); }
    public String REPLACE_VALUE(int trefn_VALUE, String VALUE) { return cofnod_VALUE.set(trefn_VALUE, VALUE); }
    public String 지우기(int trefn_VALUE) { return cofnod_VALUE.remove(trefn_VALUE); }
    public int Maint() { return cofnod_VALUE.size(); }
    public boolean technoleg_gwybodaeth_gwag_VALUE() { return cofnod_VALUE.isEmpty(); }
    public void clirio_Cynnwys() { cofnod_VALUE.clear(); }
}
