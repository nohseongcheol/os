// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Cymraeg.자체;
import java.net.*;
public final class 연결통신 {
    private 연결통신() {}
    public static cyswllt Agor(String ADDRESS, int rhif_porth) throws I_O_eithriad {
        try { return cyswllt.Agor(ADDRESS, rhif_porth);
        } catch (java.io.IOException Gwall) { throw CONVERT_eithriad.I_O(Gwall); }
        catch (RuntimeException Gwall) { throw CONVERT_eithriad.Gweithredu_gorchymyn(Gwall); }
    }
    public static 수신창구 수신열기(int rhif_porth) throws I_O_eithriad {
        try { return 수신창구.Agor(rhif_porth);
        } catch (java.io.IOException Gwall) { throw CONVERT_eithriad.I_O(Gwall); }
        catch (RuntimeException Gwall) { throw CONVERT_eithriad.Gweithredu_gorchymyn(Gwall); }
    }
    public static Socket Cysylltu(String ADDRESS, int porth_VALUE) throws I_O_eithriad {
        try { return new Socket(ADDRESS, porth_VALUE);
        } catch (java.io.IOException Gwall) { throw CONVERT_eithriad.I_O(Gwall); }
        catch (RuntimeException Gwall) { throw CONVERT_eithriad.Gweithredu_gorchymyn(Gwall); }
    }
    public static ServerSocket 듣기(int porth_VALUE) throws I_O_eithriad {
        try { return new ServerSocket(porth_VALUE);
        } catch (java.io.IOException Gwall) { throw CONVERT_eithriad.I_O(Gwall); }
        catch (RuntimeException Gwall) { throw CONVERT_eithriad.Gweithredu_gorchymyn(Gwall); }
    }
    public static Socket 받기(ServerSocket gweinydd_VALUE) throws I_O_eithriad {
        try { return gweinydd_VALUE.accept();
        } catch (java.io.IOException Gwall) { throw CONVERT_eithriad.I_O(Gwall); }
        catch (RuntimeException Gwall) { throw CONVERT_eithriad.Gweithredu_gorchymyn(Gwall); }
    }
}
