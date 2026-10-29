// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.io.FileInputStream;
import java.io.FileOutputStream;
/** 파일은 기존 ᎬᏗᏍᎩ 용어를 보존한다. 현재 저장소는 재부팅 시 사라지는 RAM 파일이다. */
public final class ᎠᏍᏆᏂᎪᏙᏗ {
    private ᎠᏍᏆᏂᎪᏙᏗ() {}
    public static byte[] 바이트읽기(String ᏚᏙᎥᎢ) throws 입출력예외 {
        try {
        FileInputStream ᎤᏪᎬ_ᏧᎬᏩᎶᏗᏯ = new FileInputStream(ᏚᏙᎥᎢ);
        try {
            byte[] 임시 = new byte[16384]; int 수 = 0, ᏧᎬᏩᎶᏗᏯ;
            while ((ᏧᎬᏩᎶᏗᏯ = ᎤᏪᎬ_ᏧᎬᏩᎶᏗᏯ.read()) != -1) { if (수 == 임시.length) throw new 입출력예외("ᎠᏍᏆᏂᎪᏙᏗ ᎢᎩᏓ 제한"); 임시[수++] = (byte)ᏧᎬᏩᎶᏗᏯ; }
            byte[] 결과 = new byte[수]; System.arraycopy(임시, 0, 결과, 0, 수); return 결과;
        } finally { ᎤᏪᎬ_ᏧᎬᏩᎶᏗᏯ.close(); }
        } catch (java.io.IOException ᎦᎵᏓᏍᏔᏅ) { throw 예외변환.I_O(ᎦᎵᏓᏍᏔᏅ); }
        catch (RuntimeException ᎦᎵᏓᏍᏔᏅ) { throw 예외변환.ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ(ᎦᎵᏓᏍᏔᏅ); }
    }
    public static void ᎪᏪᎶᏗ_byte_ᏧᎬᏩᎶᏗᏯ(String ᏚᏙᎥᎢ, byte[] ᎦᎸᏛᎢ_ᏧᎬᏩᎶᏗᏯ) throws 입출력예외 {
        try {
        FileOutputStream ᎤᏪᎬ_ᏧᎬᏩᎶᏗᏯ = new FileOutputStream(ᏚᏙᎥᎢ);
        try { for (int ᎬᎪᏘᎶᏓ_ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ = 0; ᎬᎪᏘᎶᏓ_ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ < ᎦᎸᏛᎢ_ᏧᎬᏩᎶᏗᏯ.length; ᎬᎪᏘᎶᏓ_ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ++) ᎤᏪᎬ_ᏧᎬᏩᎶᏗᏯ.write(ᎦᎸᏛᎢ_ᏧᎬᏩᎶᏗᏯ[ᎬᎪᏘᎶᏓ_ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ] & 255); } finally { ᎤᏪᎬ_ᏧᎬᏩᎶᏗᏯ.close(); }
        } catch (java.io.IOException ᎦᎵᏓᏍᏔᏅ) { throw 예외변환.I_O(ᎦᎵᏓᏍᏔᏅ); }
        catch (RuntimeException ᎦᎵᏓᏍᏔᏅ) { throw 예외변환.ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ(ᎦᎵᏓᏍᏔᏅ); }
    }
    public static String 읽기(String ᏚᏙᎥᎢ) throws 입출력예외 {
        try { return 문자.ᎠᎭᏓᏗᎭ_ᎦᏟᏌᏅᎯ(바이트읽기(ᏚᏙᎥᎢ));
        } catch (java.io.IOException ᎦᎵᏓᏍᏔᏅ) { throw 예외변환.I_O(ᎦᎵᏓᏍᏔᏅ); }
        catch (RuntimeException ᎦᎵᏓᏍᏔᏅ) { throw 예외변환.ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ(ᎦᎵᏓᏍᏔᏅ); }
    }
    public static void ᎪᏪᎶᏗ(String ᏚᏙᎥᎢ, String ᎦᎸᏛᎢ_ᏧᎬᏩᎶᏗᏯ) throws 입출력예외 {
        try { ᎪᏪᎶᏗ_byte_ᏧᎬᏩᎶᏗᏯ(ᏚᏙᎥᎢ, 문자.부호화(ᎦᎸᏛᎢ_ᏧᎬᏩᎶᏗᏯ));
        } catch (java.io.IOException ᎦᎵᏓᏍᏔᏅ) { throw 예외변환.I_O(ᎦᎵᏓᏍᏔᏅ); }
        catch (RuntimeException ᎦᎵᏓᏍᏔᏅ) { throw 예외변환.ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ(ᎦᎵᏓᏍᏔᏅ); }
    }
}
