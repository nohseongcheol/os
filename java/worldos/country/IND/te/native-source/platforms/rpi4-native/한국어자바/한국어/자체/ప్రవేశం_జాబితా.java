// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.util.ArrayList;
/** ప్రవేశం_జాబితా(目錄): 순서가 있는 항목의 모음. 이 판은 అక్షరసరం_మూల్యం 목록을 제공한다. */
public final class ప్రవేశం_జాబితా {
    private final ArrayList<String> ప్రవేశం_మూల్యం = new ArrayList<String>();
    public void 더하기(String మూల్యం) { ప్రవేశం_మూల్యం.add(మూల్యం); }
    public String చదువు(int క్రమం_మూల్యం) { return ప్రవేశం_మూల్యం.get(క్రమం_మూల్యం); }
    public String మళ్లీ_పెట్టు_మూల్యం(int క్రమం_మూల్యం, String మూల్యం) { return ప్రవేశం_మూల్యం.set(క్రమం_మూల్యం, మూల్యం); }
    public String తుడిచివేయి_ప్రవేశం(int క్రమం_మూల్యం) { return ప్రవేశం_మూల్యం.remove(క్రమం_మూల్యం); }
    public int పరిమాణం() { return ప్రవేశం_మూల్యం.size(); }
    public boolean సమాచార_టెక్నాలజీ_ఖాళీ_మూల్యం() { return ప్రవేశం_మూల్యం.isEmpty(); }
    public void క్లియర్_చేయి_విషయసూచీ() { ప్రవేశం_మూల్యం.clear(); }
}
