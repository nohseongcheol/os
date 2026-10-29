// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** CONNECT(連結)·channel_pagpasok(通路): 상대와 이어진 TCP byte_VALUE 흐름의 종단. */
public final class koneksyon {
    private final java.net.Socket 표준연결;
    koneksyon(java.net.Socket 표준연결) { this.표준연결 = 표준연결; }
    public static koneksyon buksan(String email, int numero_ng_port) throws I_O_pagbubukod {
        try {
            return new koneksyon(new java.net.Socket(email, numero_ng_port));
        } catch (java.io.IOException error) { throw CONVERT_pagbubukod.I_O(error); }
        catch (RuntimeException error) { throw CONVERT_pagbubukod.Mag_execute_utos(error); }
    }
    public 입력흐름 입력() throws I_O_pagbubukod {
        try { return new 입력흐름(표준연결.getInputStream());
        } catch (java.io.IOException error) { throw CONVERT_pagbubukod.I_O(error); }
        catch (RuntimeException error) { throw CONVERT_pagbubukod.Mag_execute_utos(error); }
    }
    public 출력흐름 출력() throws I_O_pagbubukod {
        try { return new 출력흐름(표준연결.getOutputStream());
        } catch (java.io.IOException error) { throw CONVERT_pagbubukod.I_O(error); }
        catch (RuntimeException error) { throw CONVERT_pagbubukod.Mag_execute_utos(error); }
    }
    public void TIMEOUT(int 밀리초) throws I_O_pagbubukod {
        try { 표준연결.setSoTimeout(밀리초);
        } catch (java.io.IOException error) { throw CONVERT_pagbubukod.I_O(error); }
        catch (RuntimeException error) { throw CONVERT_pagbubukod.Mag_execute_utos(error); }
    }
    public int numero_ng_port() { return 표준연결.getPort(); }
    public int lokal_numero_ng_port() { return 표준연결.getLocalPort(); }
    public boolean 닫힘() { return 표준연결.isClosed(); }
    public boolean 연결됨() { return 표준연결.isConnected(); }
    public void isara() throws I_O_pagbubukod {
        try { 표준연결.close();
        } catch (java.io.IOException error) { throw CONVERT_pagbubukod.I_O(error); }
        catch (RuntimeException error) { throw CONVERT_pagbubukod.Mag_execute_utos(error); }
    }
}
