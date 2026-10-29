// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Íslenska.eigin;
import java.net.*;
public final class tenging_flutningur {
    private tenging_flutningur() {}
    public static tenging Opna(String slóð, int tengisnúmer) throws I_Ú_undantekning {
        try { return tenging.Opna(slóð, tengisnúmer);
        } catch (java.io.IOException Villa) { throw CONVERT_undantekning.I_Ú(Villa); }
        catch (RuntimeException Villa) { throw CONVERT_undantekning.keyra_skipun(Villa); }
    }
    public static 수신창구 수신열기(int tengisnúmer) throws I_Ú_undantekning {
        try { return 수신창구.Opna(tengisnúmer);
        } catch (java.io.IOException Villa) { throw CONVERT_undantekning.I_Ú(Villa); }
        catch (RuntimeException Villa) { throw CONVERT_undantekning.keyra_skipun(Villa); }
    }
    public static Socket Tengjast(String slóð, int gátt_VALUE) throws I_Ú_undantekning {
        try { return new Socket(slóð, gátt_VALUE);
        } catch (java.io.IOException Villa) { throw CONVERT_undantekning.I_Ú(Villa); }
        catch (RuntimeException Villa) { throw CONVERT_undantekning.keyra_skipun(Villa); }
    }
    public static ServerSocket hlusta_endastöð(int gátt_VALUE) throws I_Ú_undantekning {
        try { return new ServerSocket(gátt_VALUE);
        } catch (java.io.IOException Villa) { throw CONVERT_undantekning.I_Ú(Villa); }
        catch (RuntimeException Villa) { throw CONVERT_undantekning.keyra_skipun(Villa); }
    }
    public static Socket 받기(ServerSocket þjónn_VALUE) throws I_Ú_undantekning {
        try { return þjónn_VALUE.accept();
        } catch (java.io.IOException Villa) { throw CONVERT_undantekning.I_Ú(Villa); }
        catch (RuntimeException Villa) { throw CONVERT_undantekning.keyra_skipun(Villa); }
    }
}
