// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ગુજરાતી.자체;

/** આઉટપુટ(出力)과 સ્ટ્રીમ_મૂલ્ય: 순서를 보존해 내보내는 바이트의 ચૅનલ_પ્રવેશ. */
public final class 출력흐름 {
    private final java.io.OutputStream 표준흐름;
    출력흐름(java.io.OutputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public void લખો(int મૂલ્ય) throws 입출력예외 {
        try { 표준흐름.write(મૂલ્ય);
        } catch (java.io.IOException ભૂલ) { throw 예외변환.ઇનપુટ_આઉટપુટ(ભૂલ); }
        catch (RuntimeException ભૂલ) { throw 예외변환.અમલ_કરો_આદેશ(ભૂલ); }
    }
    public void લખો(byte[] ડેટા) throws 입출력예외 {
        try { 표준흐름.write(ડેટા);
        } catch (java.io.IOException ભૂલ) { throw 예외변환.ઇનપુટ_આઉટપુટ(ભૂલ); }
        catch (RuntimeException ભૂલ) { throw 예외변환.અમલ_કરો_આદેશ(ભૂલ); }
    }
    public void લખો(byte[] ડેટા, int ચલાવો_2, int લંબાઈ_મૂલ્ય) throws 입출력예외 {
        try { 표준흐름.write(ડેટા, ચલાવો_2, લંબાઈ_મૂલ્ય);
        } catch (java.io.IOException ભૂલ) { throw 예외변환.ઇનપુટ_આઉટપુટ(ભૂલ); }
        catch (RuntimeException ભૂલ) { throw 예외변환.અમલ_કરો_આદેશ(ભૂલ); }
    }
    public void 내보내기() throws 입출력예외 {
        try { 표준흐름.flush();
        } catch (java.io.IOException ભૂલ) { throw 예외변환.ઇનપુટ_આઉટપુટ(ભૂલ); }
        catch (RuntimeException ભૂલ) { throw 예외변환.અમલ_કરો_આદેશ(ભૂલ); }
    }
    public void બંધ_કરો() throws 입출력예외 {
        try { 표준흐름.close();
        } catch (java.io.IOException ભૂલ) { throw 예외변환.ઇનપુટ_આઉટપુટ(ભૂલ); }
        catch (RuntimeException ભૂલ) { throw 예외변환.અમલ_કરો_આદેશ(ભૂલ); }
    }
}
