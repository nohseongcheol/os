// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Galego.자체;

/** Conectar(連結)·Canle_introdución(通路): 상대와 이어진 TCP byte_VALOR 흐름의 extremo. */
public final class conexión {
    private final java.net.Socket 표준연결;
    conexión(java.net.Socket 표준연결) { this.표준연결 = 표준연결; }
    public static conexión Abrir(String ENDEREZO, int número_do_porto) throws E_S_excepción {
        try {
            return new conexión(new java.net.Socket(ENDEREZO, número_do_porto));
        } catch (java.io.IOException ERRO) { throw CONVERTER_excepción.E_S(ERRO); }
        catch (RuntimeException ERRO) { throw CONVERTER_excepción.executar_comando(ERRO); }
    }
    public 입력흐름 입력() throws E_S_excepción {
        try { return new 입력흐름(표준연결.getInputStream());
        } catch (java.io.IOException ERRO) { throw CONVERTER_excepción.E_S(ERRO); }
        catch (RuntimeException ERRO) { throw CONVERTER_excepción.executar_comando(ERRO); }
    }
    public 출력흐름 Saída() throws E_S_excepción {
        try { return new 출력흐름(표준연결.getOutputStream());
        } catch (java.io.IOException ERRO) { throw CONVERTER_excepción.E_S(ERRO); }
        catch (RuntimeException ERRO) { throw CONVERTER_excepción.executar_comando(ERRO); }
    }
    public void TIMEOUT(int 밀리초) throws E_S_excepción {
        try { 표준연결.setSoTimeout(밀리초);
        } catch (java.io.IOException ERRO) { throw CONVERTER_excepción.E_S(ERRO); }
        catch (RuntimeException ERRO) { throw CONVERTER_excepción.executar_comando(ERRO); }
    }
    public int número_do_porto() { return 표준연결.getPort(); }
    public int local_número_do_porto() { return 표준연결.getLocalPort(); }
    public boolean 닫힘() { return 표준연결.isClosed(); }
    public boolean 연결됨() { return 표준연결.isConnected(); }
    public void Pechar() throws E_S_excepción {
        try { 표준연결.close();
        } catch (java.io.IOException ERRO) { throw CONVERTER_excepción.E_S(ERRO); }
        catch (RuntimeException ERRO) { throw CONVERTER_excepción.executar_comando(ERRO); }
    }
}
