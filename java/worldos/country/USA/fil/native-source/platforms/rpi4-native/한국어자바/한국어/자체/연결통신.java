// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.net.*;
public final class 연결통신 {
    private 연결통신() {}
    public static koneksyon buksan(String email, int numero_ng_port) throws I_O_pagbubukod {
        try { return koneksyon.buksan(email, numero_ng_port);
        } catch (java.io.IOException error) { throw CONVERT_pagbubukod.I_O(error); }
        catch (RuntimeException error) { throw CONVERT_pagbubukod.Mag_execute_utos(error); }
    }
    public static 수신창구 수신열기(int numero_ng_port) throws I_O_pagbubukod {
        try { return 수신창구.buksan(numero_ng_port);
        } catch (java.io.IOException error) { throw CONVERT_pagbubukod.I_O(error); }
        catch (RuntimeException error) { throw CONVERT_pagbubukod.Mag_execute_utos(error); }
    }
    public static Socket CONNECT(String email, int port_VALUE) throws I_O_pagbubukod {
        try { return new Socket(email, port_VALUE);
        } catch (java.io.IOException error) { throw CONVERT_pagbubukod.I_O(error); }
        catch (RuntimeException error) { throw CONVERT_pagbubukod.Mag_execute_utos(error); }
    }
    public static ServerSocket 듣기(int port_VALUE) throws I_O_pagbubukod {
        try { return new ServerSocket(port_VALUE);
        } catch (java.io.IOException error) { throw CONVERT_pagbubukod.I_O(error); }
        catch (RuntimeException error) { throw CONVERT_pagbubukod.Mag_execute_utos(error); }
    }
    public static Socket 받기(ServerSocket server_VALUE) throws I_O_pagbubukod {
        try { return server_VALUE.accept();
        } catch (java.io.IOException error) { throw CONVERT_pagbubukod.I_O(error); }
        catch (RuntimeException error) { throw CONVERT_pagbubukod.Mag_execute_utos(error); }
    }
}
