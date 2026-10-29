// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Íslenska.eigin;

/** 수신(受信)·gátt_VALUE(窓口): 들어오는 TCP 연결을 받아들이는 곳. */
public final class 수신창구 {
    private final java.net.ServerSocket 표준창구;
    private 수신창구(int tengisnúmer) throws I_Ú_undantekning {
        try { 표준창구 = new java.net.ServerSocket(tengisnúmer);
        } catch (java.io.IOException Villa) { throw CONVERT_undantekning.I_Ú(Villa); }
        catch (RuntimeException Villa) { throw CONVERT_undantekning.keyra_skipun(Villa); }
    }
    public static 수신창구 Opna(int tengisnúmer) throws I_Ú_undantekning {
        try { return new 수신창구(tengisnúmer);
        } catch (java.io.IOException Villa) { throw CONVERT_undantekning.I_Ú(Villa); }
        catch (RuntimeException Villa) { throw CONVERT_undantekning.keyra_skipun(Villa); }
    }
    public tenging 받기() throws I_Ú_undantekning {
        try { return new tenging(표준창구.accept());
        } catch (java.io.IOException Villa) { throw CONVERT_undantekning.I_Ú(Villa); }
        catch (RuntimeException Villa) { throw CONVERT_undantekning.keyra_skipun(Villa); }
    }
    public int tengisnúmer() { return 표준창구.getLocalPort(); }
    public void TIMEOUT(int 밀리초) throws I_Ú_undantekning {
        try { 표준창구.setSoTimeout(밀리초);
        } catch (java.io.IOException Villa) { throw CONVERT_undantekning.I_Ú(Villa); }
        catch (RuntimeException Villa) { throw CONVERT_undantekning.keyra_skipun(Villa); }
    }
    public boolean upplýsingatækni_lokað() { return 표준창구.isClosed(); }
    public void Loka() throws I_Ú_undantekning {
        try { 표준창구.close();
        } catch (java.io.IOException Villa) { throw CONVERT_undantekning.I_Ú(Villa); }
        catch (RuntimeException Villa) { throw CONVERT_undantekning.keyra_skipun(Villa); }
    }
}
