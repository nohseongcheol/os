// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Íslenska.eigin;
import java.util.ArrayList;
/** færsla_Listi(目錄): 순서가 있는 항목의 모음. 이 판은 strengur_VALUE 목록을 제공한다. */
public final class færsla_Listi {
    private final ArrayList<String> færsla_VALUE = new ArrayList<String>();
    public void 더하기(String VALUE) { færsla_VALUE.add(VALUE); }
    public String Lestur(int röð_VALUE) { return færsla_VALUE.get(röð_VALUE); }
    public String REPLACE_VALUE(int röð_VALUE, String VALUE) { return færsla_VALUE.set(röð_VALUE, VALUE); }
    public String eyða_færsla(int röð_VALUE) { return færsla_VALUE.remove(röð_VALUE); }
    public int Stærð() { return færsla_VALUE.size(); }
    public boolean upplýsingatækni_autt_VALUE() { return færsla_VALUE.isEmpty(); }
    public void hreinsa_Innihald() { færsla_VALUE.clear(); }
}
