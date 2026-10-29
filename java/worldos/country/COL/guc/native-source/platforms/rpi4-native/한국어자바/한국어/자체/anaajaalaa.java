// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.io.FileInputStream;
import java.io.FileOutputStream;
/** 파일은 기존 ka_yataayakalü 용어를 보존한다. 현재 저장소는 재부팅 시 사라지는 RAM 파일이다. */
public final class anaajaalaa {
    private anaajaalaa() {}
    public static byte[] 바이트읽기(String 이름) throws 입출력예외 {
        try {
        FileInputStream palantüsü_ajutuu = new FileInputStream(이름);
        try {
            byte[] 임시 = new byte[16384]; int 수 = 0, ajutuu;
            while ((ajutuu = palantüsü_ajutuu.read()) != -1) { if (수 == 임시.length) throw new 입출력예외("anaajaalaa 크기 제한"); 임시[수++] = (byte)ajutuu; }
            byte[] 결과 = new byte[수]; System.arraycopy(임시, 0, 결과, 0, 수); return 결과;
        } finally { palantüsü_ajutuu.close(); }
        } catch (java.io.IOException ajachitia) { throw 예외변환.E_A(ajachitia); }
        catch (RuntimeException ajachitia) { throw 예외변환.실행(ajachitia); }
    }
    public static void ashajaa_waai_ajutuu(String 이름, byte[] alu_ujatüü_ajutuu) throws 입출력예외 {
        try {
        FileOutputStream palantüsü_ajutuu = new FileOutputStream(이름);
        try { for (int eitawaakualü_ee_iyatialujuna = 0; eitawaakualü_ee_iyatialujuna < alu_ujatüü_ajutuu.length; eitawaakualü_ee_iyatialujuna++) palantüsü_ajutuu.write(alu_ujatüü_ajutuu[eitawaakualü_ee_iyatialujuna] & 255); } finally { palantüsü_ajutuu.close(); }
        } catch (java.io.IOException ajachitia) { throw 예외변환.E_A(ajachitia); }
        catch (RuntimeException ajachitia) { throw 예외변환.실행(ajachitia); }
    }
    public static String 읽기(String 이름) throws 입출력예외 {
        try { return 문자.ale_ejiraa_amoutuushi_atijaaya(바이트읽기(이름));
        } catch (java.io.IOException ajachitia) { throw 예외변환.E_A(ajachitia); }
        catch (RuntimeException ajachitia) { throw 예외변환.실행(ajachitia); }
    }
    public static void ashajaa(String 이름, String alu_ujatüü_ajutuu) throws 입출력예외 {
        try { ashajaa_waai_ajutuu(이름, 문자.부호화(alu_ujatüü_ajutuu));
        } catch (java.io.IOException ajachitia) { throw 예외변환.E_A(ajachitia); }
        catch (RuntimeException ajachitia) { throw 예외변환.실행(ajachitia); }
    }
}
