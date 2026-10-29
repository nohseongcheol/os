// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.io.FileInputStream;
import java.io.FileOutputStream;
/** 파일은 기존 përdorues 용어를 보존한다. 현재 저장소는 재부팅 시 사라지는 RAM 파일이다. */
public final class Kartelë {
    private Kartelë() {}
    public static byte[] 바이트읽기(String Emër) throws I_O_përjashtim {
        try {
        FileInputStream Stream_VALUE = new FileInputStream(Emër);
        try {
            byte[] 임시 = new byte[16384]; int 수 = 0, VALUE;
            while ((VALUE = Stream_VALUE.read()) != -1) { if (수 == 임시.length) throw new I_O_përjashtim("Kartelë Madhësi 제한"); 임시[수++] = (byte)VALUE; }
            byte[] llogaritje = new byte[수]; System.arraycopy(임시, 0, llogaritje, 0, 수); return llogaritje;
        } finally { Stream_VALUE.close(); }
        } catch (java.io.IOException GABIM) { throw CONVERT_përjashtim.I_O(GABIM); }
        catch (RuntimeException GABIM) { throw CONVERT_përjashtim.zbatoj_komandë(GABIM); }
    }
    public static void shkruaj_bajt_VALUE(String Emër, byte[] Përmbajtje_VALUE) throws I_O_përjashtim {
        try {
        FileOutputStream Stream_VALUE = new FileOutputStream(Emër);
        try { for (int Loop_INDEX = 0; Loop_INDEX < Përmbajtje_VALUE.length; Loop_INDEX++) Stream_VALUE.write(Përmbajtje_VALUE[Loop_INDEX] & 255); } finally { Stream_VALUE.close(); }
        } catch (java.io.IOException GABIM) { throw CONVERT_përjashtim.I_O(GABIM); }
        catch (RuntimeException GABIM) { throw CONVERT_përjashtim.zbatoj_komandë(GABIM); }
    }
    public static String Leximi(String Emër) throws I_O_përjashtim {
        try { return 문자.dekriptoj_të_dhëna(바이트읽기(Emër));
        } catch (java.io.IOException GABIM) { throw CONVERT_përjashtim.I_O(GABIM); }
        catch (RuntimeException GABIM) { throw CONVERT_përjashtim.zbatoj_komandë(GABIM); }
    }
    public static void Shkrimi(String Emër, String Përmbajtje_VALUE) throws I_O_përjashtim {
        try { shkruaj_bajt_VALUE(Emër, 문자.부호화(Përmbajtje_VALUE));
        } catch (java.io.IOException GABIM) { throw CONVERT_përjashtim.I_O(GABIM); }
        catch (RuntimeException GABIM) { throw CONVERT_përjashtim.zbatoj_komandë(GABIM); }
    }
}
