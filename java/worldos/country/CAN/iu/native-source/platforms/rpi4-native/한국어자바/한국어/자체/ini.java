// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.io.FileInputStream;
import java.io.FileOutputStream;
/** 파일은 기존 atuqtuq 용어를 보존한다. 현재 저장소는 재부팅 시 사라지는 RAM 파일이다. */
public final class ini {
    private ini() {}
    public static byte[] 바이트읽기(String atiq) throws 입출력예외 {
        try {
        FileInputStream ingirrania_aulataup_atuutilik = new FileInputStream(atiq);
        try {
            byte[] 임시 = new byte[16384]; int 수 = 0, atuutilik;
            while ((atuutilik = ingirrania_aulataup_atuutilik.read()) != -1) { if (수 == 임시.length) throw new 입출력예외("ini anininga 제한"); 임시[수++] = (byte)atuutilik; }
            byte[] 결과 = new byte[수]; System.arraycopy(임시, 0, 결과, 0, 수); return 결과;
        } finally { ingirrania_aulataup_atuutilik.close(); }
        } catch (java.io.IOException tammarniq) { throw 예외변환.I_O(tammarniq); }
        catch (RuntimeException tammarniq) { throw 예외변환.실행(tammarniq); }
    }
    public static void titiraq_byte_atuutilik(String atiq, byte[] Ilulingit_atuutilik) throws 입출력예외 {
        try {
        FileOutputStream ingirrania_aulataup_atuutilik = new FileOutputStream(atiq);
        try { for (int piliqqittaajuq_nalunaiqsimavik = 0; piliqqittaajuq_nalunaiqsimavik < Ilulingit_atuutilik.length; piliqqittaajuq_nalunaiqsimavik++) ingirrania_aulataup_atuutilik.write(Ilulingit_atuutilik[piliqqittaajuq_nalunaiqsimavik] & 255); } finally { ingirrania_aulataup_atuutilik.close(); }
        } catch (java.io.IOException tammarniq) { throw 예외변환.I_O(tammarniq); }
        catch (RuntimeException tammarniq) { throw 예외변환.실행(tammarniq); }
    }
    public static String 읽기(String atiq) throws 입출력예외 {
        try { return 문자.suqquinarunniirlit_titiqqat(바이트읽기(atiq));
        } catch (java.io.IOException tammarniq) { throw 예외변환.I_O(tammarniq); }
        catch (RuntimeException tammarniq) { throw 예외변환.실행(tammarniq); }
    }
    public static void titiraq(String atiq, String Ilulingit_atuutilik) throws 입출력예외 {
        try { titiraq_byte_atuutilik(atiq, 문자.부호화(Ilulingit_atuutilik));
        } catch (java.io.IOException tammarniq) { throw 예외변환.I_O(tammarniq); }
        catch (RuntimeException tammarniq) { throw 예외변환.실행(tammarniq); }
    }
}
