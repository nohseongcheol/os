// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Català.propi;

/** Connecta(連結)·Canal_introducció(通路): 상대와 이어진 TCP byte_VALOR 흐름의 extrem. */
public final class connexió {
    private final java.net.Socket 표준연결;
    connexió(java.net.Socket 표준연결) { this.표준연결 = 표준연결; }
    public static connexió Obre(String Adreça, int número_de_port) throws E_S_excepció {
        try {
            return new connexió(new java.net.Socket(Adreça, número_de_port));
        } catch (java.io.IOException s_ha_produït_un_error) { throw CONVERT_excepció.E_S(s_ha_produït_un_error); }
        catch (RuntimeException s_ha_produït_un_error) { throw CONVERT_excepció.Executa_ordre(s_ha_produït_un_error); }
    }
    public 입력흐름 입력() throws E_S_excepció {
        try { return new 입력흐름(표준연결.getInputStream());
        } catch (java.io.IOException s_ha_produït_un_error) { throw CONVERT_excepció.E_S(s_ha_produït_un_error); }
        catch (RuntimeException s_ha_produït_un_error) { throw CONVERT_excepció.Executa_ordre(s_ha_produït_un_error); }
    }
    public 출력흐름 Sortida() throws E_S_excepció {
        try { return new 출력흐름(표준연결.getOutputStream());
        } catch (java.io.IOException s_ha_produït_un_error) { throw CONVERT_excepció.E_S(s_ha_produït_un_error); }
        catch (RuntimeException s_ha_produït_un_error) { throw CONVERT_excepció.Executa_ordre(s_ha_produït_un_error); }
    }
    public void TIMEOUT(int 밀리초) throws E_S_excepció {
        try { 표준연결.setSoTimeout(밀리초);
        } catch (java.io.IOException s_ha_produït_un_error) { throw CONVERT_excepció.E_S(s_ha_produït_un_error); }
        catch (RuntimeException s_ha_produït_un_error) { throw CONVERT_excepció.Executa_ordre(s_ha_produït_un_error); }
    }
    public int número_de_port() { return 표준연결.getPort(); }
    public int local_número_de_port() { return 표준연결.getLocalPort(); }
    public boolean 닫힘() { return 표준연결.isClosed(); }
    public boolean 연결됨() { return 표준연결.isConnected(); }
    public void Tanca() throws E_S_excepció {
        try { 표준연결.close();
        } catch (java.io.IOException s_ha_produït_un_error) { throw CONVERT_excepció.E_S(s_ha_produït_un_error); }
        catch (RuntimeException s_ha_produït_un_error) { throw CONVERT_excepció.Executa_ordre(s_ha_produït_un_error); }
    }
}
