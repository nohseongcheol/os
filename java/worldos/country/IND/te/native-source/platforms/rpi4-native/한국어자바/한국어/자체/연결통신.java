// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.net.*;
public final class 연결통신 {
    private 연결통신() {}
    public static కనెక్షన్ తెరువు(String ఇమెయిల్, int పోర్ట్_సంఖ్య) throws మూ_ఫ_మినహాయింపు {
        try { return కనెక్షన్.తెరువు(ఇమెయిల్, పోర్ట్_సంఖ్య);
        } catch (java.io.IOException దోషం) { throw 예외변환.మూ_ఫ(దోషం); }
        catch (RuntimeException దోషం) { throw 예외변환.అమలు_చేయి_ఆదేశం(దోషం); }
    }
    public static 수신창구 수신열기(int పోర్ట్_సంఖ్య) throws మూ_ఫ_మినహాయింపు {
        try { return 수신창구.తెరువు(పోర్ట్_సంఖ్య);
        } catch (java.io.IOException దోషం) { throw 예외변환.మూ_ఫ(దోషం); }
        catch (RuntimeException దోషం) { throw 예외변환.అమలు_చేయి_ఆదేశం(దోషం); }
    }
    public static Socket కనెక్టుచేయి(String ఇమెయిల్, int పోర్టు_మూల్యం) throws మూ_ఫ_మినహాయింపు {
        try { return new Socket(ఇమెయిల్, పోర్టు_మూల్యం);
        } catch (java.io.IOException దోషం) { throw 예외변환.మూ_ఫ(దోషం); }
        catch (RuntimeException దోషం) { throw 예외변환.అమలు_చేయి_ఆదేశం(దోషం); }
    }
    public static ServerSocket 듣기(int పోర్టు_మూల్యం) throws మూ_ఫ_మినహాయింపు {
        try { return new ServerSocket(పోర్టు_మూల్యం);
        } catch (java.io.IOException దోషం) { throw 예외변환.మూ_ఫ(దోషం); }
        catch (RuntimeException దోషం) { throw 예외변환.అమలు_చేయి_ఆదేశం(దోషం); }
    }
    public static Socket 받기(ServerSocket సర్వర్_మూల్యం) throws మూ_ఫ_మినహాయింపు {
        try { return సర్వర్_మూల్యం.accept();
        } catch (java.io.IOException దోషం) { throw 예외변환.మూ_ఫ(దోషం); }
        catch (RuntimeException దోషం) { throw 예외변환.అమలు_చేయి_ఆదేశం(దోషం); }
    }
}
