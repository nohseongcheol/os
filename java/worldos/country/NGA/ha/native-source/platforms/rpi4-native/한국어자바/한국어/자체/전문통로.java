// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 전문(電文)·tasha_Mashigar_bayanai(通路): 경계를 가진 UDP 자료를 주고받는 종단. */
public final class 전문통로 {
    private final java.net.DatagramSocket 표준종단;
    private 전문통로(int lambar_kafa) throws I_O_banbanchi {
        try { 표준종단 = 통신.Buɗe(lambar_kafa);
        } catch (java.io.IOException Kuskure) { throw 예외변환.I_O(Kuskure); }
        catch (RuntimeException Kuskure) { throw 예외변환.gudanar_Umarni(Kuskure); }
    }
    public static 전문통로 Buɗe(int lambar_kafa) throws I_O_banbanchi {
        try { return new 전문통로(lambar_kafa);
        } catch (java.io.IOException Kuskure) { throw 예외변환.I_O(Kuskure); }
        catch (RuntimeException Kuskure) { throw 예외변환.gudanar_Umarni(Kuskure); }
    }
    public void Aika(String imel, int lambar_kafa, String Tarin_bayani) throws I_O_banbanchi {
        try { 통신.Aika(표준종단, imel, lambar_kafa, Tarin_bayani);
        } catch (java.io.IOException Kuskure) { throw 예외변환.I_O(Kuskure); }
        catch (RuntimeException Kuskure) { throw 예외변환.gudanar_Umarni(Kuskure); }
    }
    public String 받기() throws I_O_banbanchi {
        try { return 통신.받기(표준종단);
        } catch (java.io.IOException Kuskure) { throw 예외변환.I_O(Kuskure); }
        catch (RuntimeException Kuskure) { throw 예외변환.gudanar_Umarni(Kuskure); }
    }
    public void 대기시간(int 밀리초) throws I_O_banbanchi {
        try { 통신.대기시간(표준종단, 밀리초);
        } catch (java.io.IOException Kuskure) { throw 예외변환.I_O(Kuskure); }
        catch (RuntimeException Kuskure) { throw 예외변환.gudanar_Umarni(Kuskure); }
    }
    public int lambar_kafa() { return 표준종단.getLocalPort(); }
    public boolean 닫힘() { return 표준종단.isClosed(); }
    public void Rufe() { 통신.Rufe(표준종단); }
}
