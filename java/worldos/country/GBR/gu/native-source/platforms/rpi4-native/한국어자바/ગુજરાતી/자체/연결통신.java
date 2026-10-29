// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ગુજરાતી.자체;
import java.net.*;
public final class 연결통신 {
    private 연결통신() {}
    public static કનેક્શન ખોલો(String સરનામું, int પોર્ટ_નંબર) throws 입출력예외 {
        try { return કનેક્શન.ખોલો(સરનામું, પોર્ટ_નંબર);
        } catch (java.io.IOException ભૂલ) { throw 예외변환.ઇનપુટ_આઉટપુટ(ભૂલ); }
        catch (RuntimeException ભૂલ) { throw 예외변환.અમલ_કરો_આદેશ(ભૂલ); }
    }
    public static 수신창구 수신열기(int પોર્ટ_નંબર) throws 입출력예외 {
        try { return 수신창구.ખોલો(પોર્ટ_નંબર);
        } catch (java.io.IOException ભૂલ) { throw 예외변환.ઇનપુટ_આઉટપુટ(ભૂલ); }
        catch (RuntimeException ભૂલ) { throw 예외변환.અમલ_કરો_આદેશ(ભૂલ); }
    }
    public static Socket સંપર્ક_કરો(String સરનામું, int પૉર્ટ_મૂલ્ય) throws 입출력예외 {
        try { return new Socket(સરનામું, પૉર્ટ_મૂલ્ય);
        } catch (java.io.IOException ભૂલ) { throw 예외변환.ઇનપુટ_આઉટપુટ(ભૂલ); }
        catch (RuntimeException ભૂલ) { throw 예외변환.અમલ_કરો_આદેશ(ભૂલ); }
    }
    public static ServerSocket 듣기(int પૉર્ટ_મૂલ્ય) throws 입출력예외 {
        try { return new ServerSocket(પૉર્ટ_મૂલ્ય);
        } catch (java.io.IOException ભૂલ) { throw 예외변환.ઇનપુટ_આઉટપુટ(ભૂલ); }
        catch (RuntimeException ભૂલ) { throw 예외변환.અમલ_કરો_આદેશ(ભૂલ); }
    }
    public static Socket 받기(ServerSocket સર્વર_મૂલ્ય) throws 입출력예외 {
        try { return સર્વર_મૂલ્ય.accept();
        } catch (java.io.IOException ભૂલ) { throw 예외변환.ઇનપુટ_આઉટપુટ(ભૂલ); }
        catch (RuntimeException ભૂલ) { throw 예외변환.અમલ_કરો_આદેશ(ભૂલ); }
    }
}
