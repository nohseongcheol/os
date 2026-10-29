// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.io.FileInputStream;
import java.io.FileOutputStream;
/** 파일은 기존 kuutoro 용어를 보존한다. 현재 저장소는 재부팅 시 사라지는 RAM 파일이다. */
public final class fiilde {
    private fiilde() {}
    public static byte[] 바이트읽기(String innde) throws 입출력예외 {
        try {
        FileInputStream waraango_njaru = new FileInputStream(innde);
        try {
            byte[] 임시 = new byte[16384]; int 수 = 0, njaru;
            while ((njaru = waraango_njaru.read()) != -1) { if (수 == 임시.length) throw new 입출력예외("fiilde waylude_etannde 제한"); 임시[수++] = (byte)njaru; }
            byte[] 결과 = new byte[수]; System.arraycopy(임시, 0, 결과, 0, 수); return 결과;
        } finally { waraango_njaru.close(); }
        } catch (java.io.IOException juumre) { throw 예외변환.I_O(juumre); }
        catch (RuntimeException juumre) { throw 예외변환.실행(juumre); }
    }
    public static void winndude_oktee_njaru(String innde, byte[] loowdi_njaru) throws 입출력예외 {
        try {
        FileOutputStream waraango_njaru = new FileOutputStream(innde);
        try { for (int kowal_joopirdu = 0; kowal_joopirdu < loowdi_njaru.length; kowal_joopirdu++) waraango_njaru.write(loowdi_njaru[kowal_joopirdu] & 255); } finally { waraango_njaru.close(); }
        } catch (java.io.IOException juumre) { throw 예외변환.I_O(juumre); }
        catch (RuntimeException juumre) { throw 예외변환.실행(juumre); }
    }
    public static String 읽기(String innde) throws 입출력예외 {
        try { return 문자.dokkitde_keɓe(바이트읽기(innde));
        } catch (java.io.IOException juumre) { throw 예외변환.I_O(juumre); }
        catch (RuntimeException juumre) { throw 예외변환.실행(juumre); }
    }
    public static void winndude(String innde, String loowdi_njaru) throws 입출력예외 {
        try { winndude_oktee_njaru(innde, 문자.부호화(loowdi_njaru));
        } catch (java.io.IOException juumre) { throw 예외변환.I_O(juumre); }
        catch (RuntimeException juumre) { throw 예외변환.실행(juumre); }
    }
}
