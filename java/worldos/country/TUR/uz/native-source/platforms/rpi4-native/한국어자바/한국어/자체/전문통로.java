// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 전문(電文)·kanal_kiritish(通路): 경계를 가진 UDP 자료를 주고받는 종단. */
public final class 전문통로 {
    private final java.net.DatagramSocket 표준종단;
    private 전문통로(int 접속번호) throws I_O_istisno {
        try { 표준종단 = 통신.Ochish(접속번호);
        } catch (java.io.IOException Xato) { throw CONVERT_istisno.I_O(Xato); }
        catch (RuntimeException Xato) { throw CONVERT_istisno.bajarmoq_buyruq(Xato); }
    }
    public static 전문통로 Ochish(int 접속번호) throws I_O_istisno {
        try { return new 전문통로(접속번호);
        } catch (java.io.IOException Xato) { throw CONVERT_istisno.I_O(Xato); }
        catch (RuntimeException Xato) { throw CONVERT_istisno.bajarmoq_buyruq(Xato); }
    }
    public void yuborish(String manzil, int 접속번호, String ma_lumotlar) throws I_O_istisno {
        try { 통신.yuborish(표준종단, manzil, 접속번호, ma_lumotlar);
        } catch (java.io.IOException Xato) { throw CONVERT_istisno.I_O(Xato); }
        catch (RuntimeException Xato) { throw CONVERT_istisno.bajarmoq_buyruq(Xato); }
    }
    public String 받기() throws I_O_istisno {
        try { return 통신.받기(표준종단);
        } catch (java.io.IOException Xato) { throw CONVERT_istisno.I_O(Xato); }
        catch (RuntimeException Xato) { throw CONVERT_istisno.bajarmoq_buyruq(Xato); }
    }
    public void TANAFFUS(int 밀리초) throws I_O_istisno {
        try { 통신.TANAFFUS(표준종단, 밀리초);
        } catch (java.io.IOException Xato) { throw CONVERT_istisno.I_O(Xato); }
        catch (RuntimeException Xato) { throw CONVERT_istisno.bajarmoq_buyruq(Xato); }
    }
    public int 접속번호() { return 표준종단.getLocalPort(); }
    public boolean 닫힘() { return 표준종단.isClosed(); }
    public void Yopish() { 통신.Yopish(표준종단); }
}
