// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.io.FileInputStream;
import java.io.FileOutputStream;
/** 파일은 기존 వినియోగదారు 용어를 보존한다. 현재 저장소는 재부팅 시 사라지는 RAM 파일이다. */
public final class దస్త్రం {
    private దస్త్రం() {}
    public static byte[] 바이트읽기(String పేరు) throws మూ_ఫ_మినహాయింపు {
        try {
        FileInputStream ధార_మూల్యం = new FileInputStream(పేరు);
        try {
            byte[] 임시 = new byte[16384]; int 수 = 0, మూల్యం;
            while ((మూల్యం = ధార_మూల్యం.read()) != -1) { if (수 == 임시.length) throw new మూ_ఫ_మినహాయింపు("దస్త్రం పరిమాణం 제한"); 임시[수++] = (byte)మూల్యం; }
            byte[] ప్రమాణం = new byte[수]; System.arraycopy(임시, 0, ప్రమాణం, 0, 수); return ప్రమాణం;
        } finally { ధార_మూల్యం.close(); }
        } catch (java.io.IOException దోషం) { throw 예외변환.మూ_ఫ(దోషం); }
        catch (RuntimeException దోషం) { throw 예외변환.అమలు_చేయి_ఆదేశం(దోషం); }
    }
    public static void వ్రాయి_బైట్_మూల్యం(String పేరు, byte[] విషయం_మూల్యం) throws మూ_ఫ_మినహాయింపు {
        try {
        FileOutputStream ధార_మూల్యం = new FileOutputStream(పేరు);
        try { for (int లూప్_సూచీ = 0; లూప్_సూచీ < విషయం_మూల్యం.length; లూప్_సూచీ++) ధార_మూల్యం.write(విషయం_మూల్యం[లూప్_సూచీ] & 255); } finally { ధార_మూల్యం.close(); }
        } catch (java.io.IOException దోషం) { throw 예외변환.మూ_ఫ(దోషం); }
        catch (RuntimeException దోషం) { throw 예외변환.అమలు_చేయి_ఆదేశం(దోషం); }
    }
    public static String చదువు(String పేరు) throws మూ_ఫ_మినహాయింపు {
        try { return 문자.వ్యక్తపరుచు_డేటా(바이트읽기(పేరు));
        } catch (java.io.IOException దోషం) { throw 예외변환.మూ_ఫ(దోషం); }
        catch (RuntimeException దోషం) { throw 예외변환.అమలు_చేయి_ఆదేశం(దోషం); }
    }
    public static void వ్రాయుము(String పేరు, String విషయం_మూల్యం) throws మూ_ఫ_మినహాయింపు {
        try { వ్రాయి_బైట్_మూల్యం(పేరు, 문자.부호화(విషయం_మూల్యం));
        } catch (java.io.IOException దోషం) { throw 예외변환.మూ_ఫ(దోషం); }
        catch (RuntimeException దోషం) { throw 예외변환.అమలు_చేయి_ఆదేశం(దోషం); }
    }
}
