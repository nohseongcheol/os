// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Ikinyarwanda.자체;
import java.io.FileInputStream;
import java.io.FileOutputStream;
/** 파일은 기존 ukoresha 용어를 보존한다. 현재 저장소는 재부팅 시 사라지는 RAM 파일이다. */
public final class Idosiye {
    private Idosiye() {}
    public static byte[] 바이트읽기(String Izina) throws 입출력예외 {
        try {
        FileInputStream Stream_agaciro = new FileInputStream(Izina);
        try {
            byte[] 임시 = new byte[16384]; int 수 = 0, agaciro;
            while ((agaciro = Stream_agaciro.read()) != -1) { if (수 == 임시.length) throw new 입출력예외("Idosiye Ingano 제한"); 임시[수++] = (byte)agaciro; }
            byte[] 결과 = new byte[수]; System.arraycopy(임시, 0, 결과, 0, 수); return 결과;
        } finally { Stream_agaciro.close(); }
        } catch (java.io.IOException IKOSA) { throw 예외변환.I_O(IKOSA); }
        catch (RuntimeException IKOSA) { throw 예외변환.gukora_ibwiriza(IKOSA); }
    }
    public static void kwandika_bayiti_agaciro(String Izina, byte[] Ibirimo_agaciro) throws 입출력예외 {
        try {
        FileOutputStream Stream_agaciro = new FileOutputStream(Izina);
        try { for (int gukora_mu_matsinda_umugerekashakiro = 0; gukora_mu_matsinda_umugerekashakiro < Ibirimo_agaciro.length; gukora_mu_matsinda_umugerekashakiro++) Stream_agaciro.write(Ibirimo_agaciro[gukora_mu_matsinda_umugerekashakiro] & 255); } finally { Stream_agaciro.close(); }
        } catch (java.io.IOException IKOSA) { throw 예외변환.I_O(IKOSA); }
        catch (RuntimeException IKOSA) { throw 예외변환.gukora_ibwiriza(IKOSA); }
    }
    public static String 읽기(String Izina) throws 입출력예외 {
        try { return 문자.gusobanura_amakurushingiro(바이트읽기(Izina));
        } catch (java.io.IOException IKOSA) { throw 예외변환.I_O(IKOSA); }
        catch (RuntimeException IKOSA) { throw 예외변환.gukora_ibwiriza(IKOSA); }
    }
    public static void kwandika(String Izina, String Ibirimo_agaciro) throws 입출력예외 {
        try { kwandika_bayiti_agaciro(Izina, 문자.부호화(Ibirimo_agaciro));
        } catch (java.io.IOException IKOSA) { throw 예외변환.I_O(IKOSA); }
        catch (RuntimeException IKOSA) { throw 예외변환.gukora_ibwiriza(IKOSA); }
    }
}
