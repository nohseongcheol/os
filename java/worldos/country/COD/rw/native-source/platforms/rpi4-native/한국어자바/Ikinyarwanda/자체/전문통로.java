// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Ikinyarwanda.자체;

/** 전문(電文)·umurongo_icyinjizwa(通路): 경계를 가진 UDP 자료를 주고받는 종단. */
public final class 전문통로 {
    private final java.net.DatagramSocket 표준종단;
    private 전문통로(int 접속번호) throws 입출력예외 {
        try { 표준종단 = 통신.Gufungura(접속번호);
        } catch (java.io.IOException IKOSA) { throw 예외변환.I_O(IKOSA); }
        catch (RuntimeException IKOSA) { throw 예외변환.gukora_ibwiriza(IKOSA); }
    }
    public static 전문통로 Gufungura(int 접속번호) throws 입출력예외 {
        try { return new 전문통로(접속번호);
        } catch (java.io.IOException IKOSA) { throw 예외변환.I_O(IKOSA); }
        catch (RuntimeException IKOSA) { throw 예외변환.gukora_ibwiriza(IKOSA); }
    }
    public void kohereza(String aderesi, int 접속번호, String amakurushingiro) throws 입출력예외 {
        try { 통신.kohereza(표준종단, aderesi, 접속번호, amakurushingiro);
        } catch (java.io.IOException IKOSA) { throw 예외변환.I_O(IKOSA); }
        catch (RuntimeException IKOSA) { throw 예외변환.gukora_ibwiriza(IKOSA); }
    }
    public String 받기() throws 입출력예외 {
        try { return 통신.받기(표준종단);
        } catch (java.io.IOException IKOSA) { throw 예외변환.I_O(IKOSA); }
        catch (RuntimeException IKOSA) { throw 예외변환.gukora_ibwiriza(IKOSA); }
    }
    public void 대기시간(int 밀리초) throws 입출력예외 {
        try { 통신.대기시간(표준종단, 밀리초);
        } catch (java.io.IOException IKOSA) { throw 예외변환.I_O(IKOSA); }
        catch (RuntimeException IKOSA) { throw 예외변환.gukora_ibwiriza(IKOSA); }
    }
    public int 접속번호() { return 표준종단.getLocalPort(); }
    public boolean 닫힘() { return 표준종단.isClosed(); }
    public void Gufunga() { 통신.Gufunga(표준종단); }
}
