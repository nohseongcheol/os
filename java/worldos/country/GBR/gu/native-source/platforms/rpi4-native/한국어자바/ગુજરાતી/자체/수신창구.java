// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ગુજરાતી.자체;

/** 수신(受信)·પૉર્ટ_મૂલ્ય(窓口): 들어오는 TCP 연결을 받아들이는 곳. */
public final class 수신창구 {
    private final java.net.ServerSocket 표준창구;
    private 수신창구(int પોર્ટ_નંબર) throws 입출력예외 {
        try { 표준창구 = new java.net.ServerSocket(પોર્ટ_નંબર);
        } catch (java.io.IOException ભૂલ) { throw 예외변환.ઇનપુટ_આઉટપુટ(ભૂલ); }
        catch (RuntimeException ભૂલ) { throw 예외변환.અમલ_કરો_આદેશ(ભૂલ); }
    }
    public static 수신창구 ખોલો(int પોર્ટ_નંબર) throws 입출력예외 {
        try { return new 수신창구(પોર્ટ_નંબર);
        } catch (java.io.IOException ભૂલ) { throw 예외변환.ઇનપુટ_આઉટપુટ(ભૂલ); }
        catch (RuntimeException ભૂલ) { throw 예외변환.અમલ_કરો_આદેશ(ભૂલ); }
    }
    public કનેક્શન 받기() throws 입출력예외 {
        try { return new કનેક્શન(표준창구.accept());
        } catch (java.io.IOException ભૂલ) { throw 예외변환.ઇનપુટ_આઉટપુટ(ભૂલ); }
        catch (RuntimeException ભૂલ) { throw 예외변환.અમલ_કરો_આદેશ(ભૂલ); }
    }
    public int પોર્ટ_નંબર() { return 표준창구.getLocalPort(); }
    public void 대기시간(int 밀리초) throws 입출력예외 {
        try { 표준창구.setSoTimeout(밀리초);
        } catch (java.io.IOException ભૂલ) { throw 예외변환.ઇનપુટ_આઉટપુટ(ભૂલ); }
        catch (RuntimeException ભૂલ) { throw 예외변환.અમલ_કરો_આદેશ(ભૂલ); }
    }
    public boolean 닫힘() { return 표준창구.isClosed(); }
    public void બંધ_કરો() throws 입출력예외 {
        try { 표준창구.close();
        } catch (java.io.IOException ભૂલ) { throw 예외변환.ઇનપુટ_આઉટપુટ(ભૂલ); }
        catch (RuntimeException ભૂલ) { throw 예외변환.અમલ_કરો_આદેશ(ભૂલ); }
    }
}
