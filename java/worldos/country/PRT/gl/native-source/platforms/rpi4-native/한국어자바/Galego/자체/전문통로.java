// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Galego.자체;

/** 전문(電文)·Canle_introdución(通路): 경계를 가진 UDP 자료를 주고받는 extremo. */
public final class 전문통로 {
    private final java.net.DatagramSocket 표준종단;
    private 전문통로(int número_do_porto) throws E_S_excepción {
        try { 표준종단 = 통신.Abrir(número_do_porto);
        } catch (java.io.IOException ERRO) { throw CONVERTER_excepción.E_S(ERRO); }
        catch (RuntimeException ERRO) { throw CONVERTER_excepción.executar_comando(ERRO); }
    }
    public static 전문통로 Abrir(int número_do_porto) throws E_S_excepción {
        try { return new 전문통로(número_do_porto);
        } catch (java.io.IOException ERRO) { throw CONVERTER_excepción.E_S(ERRO); }
        catch (RuntimeException ERRO) { throw CONVERTER_excepción.executar_comando(ERRO); }
    }
    public void enviar(String ENDEREZO, int número_do_porto, String datos) throws E_S_excepción {
        try { 통신.enviar(표준종단, ENDEREZO, número_do_porto, datos);
        } catch (java.io.IOException ERRO) { throw CONVERTER_excepción.E_S(ERRO); }
        catch (RuntimeException ERRO) { throw CONVERTER_excepción.executar_comando(ERRO); }
    }
    public String 받기() throws E_S_excepción {
        try { return 통신.받기(표준종단);
        } catch (java.io.IOException ERRO) { throw CONVERTER_excepción.E_S(ERRO); }
        catch (RuntimeException ERRO) { throw CONVERTER_excepción.executar_comando(ERRO); }
    }
    public void TIMEOUT(int 밀리초) throws E_S_excepción {
        try { 통신.TIMEOUT(표준종단, 밀리초);
        } catch (java.io.IOException ERRO) { throw CONVERTER_excepción.E_S(ERRO); }
        catch (RuntimeException ERRO) { throw CONVERTER_excepción.executar_comando(ERRO); }
    }
    public int número_do_porto() { return 표준종단.getLocalPort(); }
    public boolean 닫힘() { return 표준종단.isClosed(); }
    public void Pechar() { 통신.Pechar(표준종단); }
}
