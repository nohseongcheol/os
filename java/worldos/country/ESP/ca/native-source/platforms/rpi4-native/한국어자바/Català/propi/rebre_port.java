// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Català.propi;

/** rebre_VALOR(受信)·port_VALOR(窓口): 들어오는 TCP 연결을 받아들이는 곳. */
public final class rebre_port {
    private final java.net.ServerSocket 표준창구;
    private rebre_port(int número_de_port) throws E_S_excepció {
        try { 표준창구 = new java.net.ServerSocket(número_de_port);
        } catch (java.io.IOException s_ha_produït_un_error) { throw CONVERT_excepció.E_S(s_ha_produït_un_error); }
        catch (RuntimeException s_ha_produït_un_error) { throw CONVERT_excepció.Executa_ordre(s_ha_produït_un_error); }
    }
    public static rebre_port Obre(int número_de_port) throws E_S_excepció {
        try { return new rebre_port(número_de_port);
        } catch (java.io.IOException s_ha_produït_un_error) { throw CONVERT_excepció.E_S(s_ha_produït_un_error); }
        catch (RuntimeException s_ha_produït_un_error) { throw CONVERT_excepció.Executa_ordre(s_ha_produït_un_error); }
    }
    public connexió rebre() throws E_S_excepció {
        try { return new connexió(표준창구.accept());
        } catch (java.io.IOException s_ha_produït_un_error) { throw CONVERT_excepció.E_S(s_ha_produït_un_error); }
        catch (RuntimeException s_ha_produït_un_error) { throw CONVERT_excepció.Executa_ordre(s_ha_produït_un_error); }
    }
    public int número_de_port() { return 표준창구.getLocalPort(); }
    public void TIMEOUT(int 밀리초) throws E_S_excepció {
        try { 표준창구.setSoTimeout(밀리초);
        } catch (java.io.IOException s_ha_produït_un_error) { throw CONVERT_excepció.E_S(s_ha_produït_un_error); }
        catch (RuntimeException s_ha_produït_un_error) { throw CONVERT_excepció.Executa_ordre(s_ha_produït_un_error); }
    }
    public boolean 닫힘() { return 표준창구.isClosed(); }
    public void Tanca() throws E_S_excepció {
        try { 표준창구.close();
        } catch (java.io.IOException s_ha_produït_un_error) { throw CONVERT_excepció.E_S(s_ha_produït_un_error); }
        catch (RuntimeException s_ha_produït_un_error) { throw CONVERT_excepció.Executa_ordre(s_ha_produït_un_error); }
    }
}
