// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package አማርኛ.자체;
import java.io.FileInputStream;
import java.io.FileOutputStream;
/** 파일은 기존 ተጠቃሚ 용어를 보존한다. 현재 저장소는 재부팅 시 사라지는 RAM 파일이다. */
public final class ፋይል {
    private ፋይል() {}
    public static byte[] 바이트읽기(String ስም) throws ግቤት_ውጤት_ልዩነት {
        try {
        FileInputStream ልቀቅ_እሴት = new FileInputStream(ስም);
        try {
            byte[] 임시 = new byte[16384]; int 수 = 0, እሴት;
            while ((እሴት = ልቀቅ_እሴት.read()) != -1) { if (수 == 임시.length) throw new ግቤት_ውጤት_ልዩነት("ፋይል መጠን 제한"); 임시[수++] = (byte)እሴት; }
            byte[] ልኬት = new byte[수]; System.arraycopy(임시, 0, ልኬት, 0, 수); return ልኬት;
        } finally { ልቀቅ_እሴት.close(); }
        } catch (java.io.IOException ስህተት) { throw 예외변환.ግቤት_ውጤት(ስህተት); }
        catch (RuntimeException ስህተት) { throw 예외변환.ፈጽም_ትእዛዝ(ስህተት); }
    }
    public static void ጻፍ_ባይት_እሴት(String ስም, byte[] ይዘት_እሴት) throws ግቤት_ውጤት_ልዩነት {
        try {
        FileOutputStream ልቀቅ_እሴት = new FileOutputStream(ስም);
        try { for (int ድግግሞሽ_መረጃ_ጠቆመ = 0; ድግግሞሽ_መረጃ_ጠቆመ < ይዘት_እሴት.length; ድግግሞሽ_መረጃ_ጠቆመ++) ልቀቅ_እሴት.write(ይዘት_እሴት[ድግግሞሽ_መረጃ_ጠቆመ] & 255); } finally { ልቀቅ_እሴት.close(); }
        } catch (java.io.IOException ስህተት) { throw 예외변환.ግቤት_ውጤት(ስህተት); }
        catch (RuntimeException ስህተት) { throw 예외변환.ፈጽም_ትእዛዝ(ስህተት); }
    }
    public static String ማንበቢያ(String ስም) throws ግቤት_ውጤት_ልዩነት {
        try { return 문자.ምስጠራውን_ፍታ_ውሂብ(바이트읽기(ስም));
        } catch (java.io.IOException ስህተት) { throw 예외변환.ግቤት_ውጤት(ስህተት); }
        catch (RuntimeException ስህተት) { throw 예외변환.ፈጽም_ትእዛዝ(ስህተት); }
    }
    public static void መጻፊያ(String ስም, String ይዘት_እሴት) throws ግቤት_ውጤት_ልዩነት {
        try { ጻፍ_ባይት_እሴት(ስም, 문자.부호화(ይዘት_እሴት));
        } catch (java.io.IOException ስህተት) { throw 예외변환.ግቤት_ውጤት(ስህተት); }
        catch (RuntimeException ስህተት) { throw 예외변환.ፈጽም_ትእዛዝ(ስህተት); }
    }
}
