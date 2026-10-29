// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ગુજરાતી.자체;
import java.io.FileInputStream;
import java.io.FileOutputStream;
/** 파일은 기존 ઉપયોગકર્તા 용어를 보존한다. 현재 저장소는 재부팅 시 사라지는 RAM 파일이다. */
public final class ફાઈલ {
    private ફાઈલ() {}
    public static byte[] 바이트읽기(String નામ) throws 입출력예외 {
        try {
        FileInputStream સ્ટ્રીમ_મૂલ્ય = new FileInputStream(નામ);
        try {
            byte[] 임시 = new byte[16384]; int 수 = 0, મૂલ્ય;
            while ((મૂલ્ય = સ્ટ્રીમ_મૂલ્ય.read()) != -1) { if (수 == 임시.length) throw new 입출력예외("ફાઈલ માપ 제한"); 임시[수++] = (byte)મૂલ્ય; }
            byte[] પરિમાણ = new byte[수]; System.arraycopy(임시, 0, પરિમાણ, 0, 수); return પરિમાણ;
        } finally { સ્ટ્રીમ_મૂલ્ય.close(); }
        } catch (java.io.IOException ભૂલ) { throw 예외변환.ઇનપુટ_આઉટપુટ(ભૂલ); }
        catch (RuntimeException ભૂલ) { throw 예외변환.અમલ_કરો_આદેશ(ભૂલ); }
    }
    public static void લખો_બાઇટ_મૂલ્ય(String નામ, byte[] સામગ્રી_મૂલ્ય) throws 입출력예외 {
        try {
        FileOutputStream સ્ટ્રીમ_મૂલ્ય = new FileOutputStream(નામ);
        try { for (int લૂપ_અનુક્રમણિકા = 0; લૂપ_અનુક્રમણિકા < સામગ્રી_મૂલ્ય.length; લૂપ_અનુક્રમણિકા++) સ્ટ્રીમ_મૂલ્ય.write(સામગ્રી_મૂલ્ય[લૂપ_અનુક્રમણિકા] & 255); } finally { સ્ટ્રીમ_મૂલ્ય.close(); }
        } catch (java.io.IOException ભૂલ) { throw 예외변환.ઇનપુટ_આઉટપુટ(ભૂલ); }
        catch (RuntimeException ભૂલ) { throw 예외변환.અમલ_કરો_આદેશ(ભૂલ); }
    }
    public static String વાંચો(String નામ) throws 입출력예외 {
        try { return 문자.ડિક્રિપ્ટ_કરો_ડેટા(바이트읽기(નામ));
        } catch (java.io.IOException ભૂલ) { throw 예외변환.ઇનપુટ_આઉટપુટ(ભૂલ); }
        catch (RuntimeException ભૂલ) { throw 예외변환.અમલ_કરો_આદેશ(ભૂલ); }
    }
    public static void લખો(String નામ, String સામગ્રી_મૂલ્ય) throws 입출력예외 {
        try { લખો_બાઇટ_મૂલ્ય(નામ, 문자.부호화(સામગ્રી_મૂલ્ય));
        } catch (java.io.IOException ભૂલ) { throw 예외변환.ઇનપુટ_આઉટપુટ(ભૂલ); }
        catch (RuntimeException ભૂલ) { throw 예외변환.અમલ_કરો_આદેશ(ભૂલ); }
    }
}
