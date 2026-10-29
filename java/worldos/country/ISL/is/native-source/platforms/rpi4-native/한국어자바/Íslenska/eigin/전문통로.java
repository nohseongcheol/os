// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Íslenska.eigin;

/** 전문(電文)·rás_færsla(通路): 경계를 가진 UDP 자료를 주고받는 endastöð. */
public final class 전문통로 {
    private final java.net.DatagramSocket 표준종단;
    private 전문통로(int tengisnúmer) throws I_Ú_undantekning {
        try { 표준종단 = 통신.Opna(tengisnúmer);
        } catch (java.io.IOException Villa) { throw CONVERT_undantekning.I_Ú(Villa); }
        catch (RuntimeException Villa) { throw CONVERT_undantekning.keyra_skipun(Villa); }
    }
    public static 전문통로 Opna(int tengisnúmer) throws I_Ú_undantekning {
        try { return new 전문통로(tengisnúmer);
        } catch (java.io.IOException Villa) { throw CONVERT_undantekning.I_Ú(Villa); }
        catch (RuntimeException Villa) { throw CONVERT_undantekning.keyra_skipun(Villa); }
    }
    public void senda(String slóð, int tengisnúmer, String gögn) throws I_Ú_undantekning {
        try { 통신.senda(표준종단, slóð, tengisnúmer, gögn);
        } catch (java.io.IOException Villa) { throw CONVERT_undantekning.I_Ú(Villa); }
        catch (RuntimeException Villa) { throw CONVERT_undantekning.keyra_skipun(Villa); }
    }
    public String 받기() throws I_Ú_undantekning {
        try { return 통신.받기(표준종단);
        } catch (java.io.IOException Villa) { throw CONVERT_undantekning.I_Ú(Villa); }
        catch (RuntimeException Villa) { throw CONVERT_undantekning.keyra_skipun(Villa); }
    }
    public void TIMEOUT(int 밀리초) throws I_Ú_undantekning {
        try { 통신.TIMEOUT(표준종단, 밀리초);
        } catch (java.io.IOException Villa) { throw CONVERT_undantekning.I_Ú(Villa); }
        catch (RuntimeException Villa) { throw CONVERT_undantekning.keyra_skipun(Villa); }
    }
    public int tengisnúmer() { return 표준종단.getLocalPort(); }
    public boolean upplýsingatækni_lokað() { return 표준종단.isClosed(); }
    public void Loka() { 통신.Loka(표준종단); }
}
