// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Galego.자체;

/** 수신(受信)·porto_VALOR(窓口): 들어오는 TCP 연결을 받아들이는 곳. */
public final class 수신창구 {
    private final java.net.ServerSocket 표준창구;
    private 수신창구(int número_do_porto) throws E_S_excepción {
        try { 표준창구 = new java.net.ServerSocket(número_do_porto);
        } catch (java.io.IOException ERRO) { throw CONVERTER_excepción.E_S(ERRO); }
        catch (RuntimeException ERRO) { throw CONVERTER_excepción.executar_comando(ERRO); }
    }
    public static 수신창구 Abrir(int número_do_porto) throws E_S_excepción {
        try { return new 수신창구(número_do_porto);
        } catch (java.io.IOException ERRO) { throw CONVERTER_excepción.E_S(ERRO); }
        catch (RuntimeException ERRO) { throw CONVERTER_excepción.executar_comando(ERRO); }
    }
    public conexión 받기() throws E_S_excepción {
        try { return new conexión(표준창구.accept());
        } catch (java.io.IOException ERRO) { throw CONVERTER_excepción.E_S(ERRO); }
        catch (RuntimeException ERRO) { throw CONVERTER_excepción.executar_comando(ERRO); }
    }
    public int número_do_porto() { return 표준창구.getLocalPort(); }
    public void TIMEOUT(int 밀리초) throws E_S_excepción {
        try { 표준창구.setSoTimeout(밀리초);
        } catch (java.io.IOException ERRO) { throw CONVERTER_excepción.E_S(ERRO); }
        catch (RuntimeException ERRO) { throw CONVERTER_excepción.executar_comando(ERRO); }
    }
    public boolean 닫힘() { return 표준창구.isClosed(); }
    public void Pechar() throws E_S_excepción {
        try { 표준창구.close();
        } catch (java.io.IOException ERRO) { throw CONVERTER_excepción.E_S(ERRO); }
        catch (RuntimeException ERRO) { throw CONVERTER_excepción.executar_comando(ERRO); }
    }
}
