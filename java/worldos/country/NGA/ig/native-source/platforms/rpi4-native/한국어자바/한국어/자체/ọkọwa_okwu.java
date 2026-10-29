// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.util.HashMap;
/** ọkọwa_okwu(辭典): 찾는 Mkpụrụokwu_SMS(열쇠)에 값을 대응시킨다. */
public final class ọkọwa_okwu {
    private final HashMap<String, String> ndebà_valuu = new HashMap<String, String>();
    public String 넣기(String 열쇠, String valuu) { return ndebà_valuu.put(열쇠, valuu); }
    public String chọta_ndebà(String 열쇠) { return ndebà_valuu.get(열쇠); }
    public boolean 있는가(String 열쇠) { return ndebà_valuu.containsKey(열쇠); }
    public String 지우기(String 열쇠) { return ndebà_valuu.remove(열쇠); }
    public int Ụhara() { return ndebà_valuu.size(); }
    public void hichaa_TOC() { ndebà_valuu.clear(); }
}
