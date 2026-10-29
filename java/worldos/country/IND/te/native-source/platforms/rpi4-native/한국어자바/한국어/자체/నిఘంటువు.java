// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.util.HashMap;
/** నిఘంటువు(辭典): 찾는 పదం_పాఠం(열쇠)에 값을 대응시킨다. */
public final class నిఘంటువు {
    private final HashMap<String, String> ప్రవేశం_మూల్యం = new HashMap<String, String>();
    public String 넣기(String 열쇠, String మూల్యం) { return ప్రవేశం_మూల్యం.put(열쇠, మూల్యం); }
    public String వెతుకు_ప్రవేశం(String 열쇠) { return ప్రవేశం_మూల్యం.get(열쇠); }
    public boolean 있는가(String 열쇠) { return ప్రవేశం_మూల్యం.containsKey(열쇠); }
    public String తుడిచివేయి_ప్రవేశం(String 열쇠) { return ప్రవేశం_మూల్యం.remove(열쇠); }
    public int పరిమాణం() { return ప్రవేశం_మూల్యం.size(); }
    public void క్లియర్_చేయి_విషయసూచీ() { ప్రవేశం_మూల్యం.clear(); }
}
