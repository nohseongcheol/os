// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ગુજરાતી.자체;

/** 입력(入力)과 સ્ટ્રીમ_મૂલ્ય: 순서대로 들어오는 바이트를 읽는 ચૅનલ_પ્રવેશ. */
public final class 입력흐름 {
    private final java.io.InputStream 표준흐름;
    입력흐름(java.io.InputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public int વાંચો() throws 입출력예외 {
        try { return 표준흐름.read();
        } catch (java.io.IOException ભૂલ) { throw 예외변환.ઇનપુટ_આઉટપુટ(ભૂલ); }
        catch (RuntimeException ભૂલ) { throw 예외변환.અમલ_કરો_આદેશ(ભૂલ); }
    }
    public int વાંચો(byte[] ડેટા) throws 입출력예외 {
        try { return 표준흐름.read(ડેટા);
        } catch (java.io.IOException ભૂલ) { throw 예외변환.ઇનપુટ_આઉટપુટ(ભૂલ); }
        catch (RuntimeException ભૂલ) { throw 예외변환.અમલ_કરો_આદેશ(ભૂલ); }
    }
    public int વાંચો(byte[] ડેટા, int ચલાવો_2, int લંબાઈ_મૂલ્ય) throws 입출력예외 {
        try { return 표준흐름.read(ડેટા, ચલાવો_2, લંબાઈ_મૂલ્ય);
        } catch (java.io.IOException ભૂલ) { throw 예외변환.ઇનપુટ_આઉટપુટ(ભૂલ); }
        catch (RuntimeException ભૂલ) { throw 예외변환.અમલ_કરો_આદેશ(ભૂલ); }
    }
    public void બંધ_કરો() throws 입출력예외 {
        try { 표준흐름.close();
        } catch (java.io.IOException ભૂલ) { throw 예외변환.ઇનપુટ_આઉટપુટ(ભૂલ); }
        catch (RuntimeException ભૂલ) { throw 예외변환.અમલ_કરો_આદેશ(ભૂલ); }
    }
}
