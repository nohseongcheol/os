// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package tiếngViệt.tựThân;
import java.net.*;
public final class vậnChuyểnKếtNối {
    private vậnChuyểnKếtNối() {}
    public static KếtNối mở(String địaChỉ, int sốCổng) throws NgoạiLệĐầuRaĐầuVào {
        try { return KếtNối.mở(địaChỉ, sốCổng);
        } catch (java.io.IOException lỗi) { throw chuyểnĐổiNgoạiLệ.đầuRaĐầuVào(lỗi); }
        catch (RuntimeException lỗi) { throw chuyểnĐổiNgoạiLệ.thựcThiLệnh(lỗi); }
    }
    public static nhậnCổng mởBộNhận(int sốCổng) throws NgoạiLệĐầuRaĐầuVào {
        try { return nhậnCổng.mở(sốCổng);
        } catch (java.io.IOException lỗi) { throw chuyểnĐổiNgoạiLệ.đầuRaĐầuVào(lỗi); }
        catch (RuntimeException lỗi) { throw chuyểnĐổiNgoạiLệ.thựcThiLệnh(lỗi); }
    }
    public static Socket nốiKết(String địaChỉ, int giáTrịCổng) throws NgoạiLệĐầuRaĐầuVào {
        try { return new Socket(địaChỉ, giáTrịCổng);
        } catch (java.io.IOException lỗi) { throw chuyểnĐổiNgoạiLệ.đầuRaĐầuVào(lỗi); }
        catch (RuntimeException lỗi) { throw chuyểnĐổiNgoạiLệ.thựcThiLệnh(lỗi); }
    }
    public static ServerSocket lắngNgheĐiểmCuối(int giáTrịCổng) throws NgoạiLệĐầuRaĐầuVào {
        try { return new ServerSocket(giáTrịCổng);
        } catch (java.io.IOException lỗi) { throw chuyểnĐổiNgoạiLệ.đầuRaĐầuVào(lỗi); }
        catch (RuntimeException lỗi) { throw chuyểnĐổiNgoạiLệ.thựcThiLệnh(lỗi); }
    }
    public static Socket nhận(ServerSocket giáTrịMáyChủ) throws NgoạiLệĐầuRaĐầuVào {
        try { return giáTrịMáyChủ.accept();
        } catch (java.io.IOException lỗi) { throw chuyểnĐổiNgoạiLệ.đầuRaĐầuVào(lỗi); }
        catch (RuntimeException lỗi) { throw chuyểnĐổiNgoạiLệ.thựcThiLệnh(lỗi); }
    }
}
