// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import tiếngViệt.tựThân.*;

public class thửCácNgoạiLệTiếngHàn {
    static void hếtGiờMặcĐịnh() throws java.io.IOException {
        throw new java.net.SocketTimeoutException("원래 ngoạiLệ");
    }
    public static void main(String[] cácĐốiSố) throws NgoạiLệĐầuRaĐầuVào {
        try { throw new NgoạiLệHếtGiờChờ("chờTrạngThái phầnKết"); }
        catch (NgoạiLệHếtGiờChờ lỗi) { ĐầuRa.ghiDòng(lỗi.môTả()); }
        try { throw new NgoạiLệTraCứuĐịaChỉ("địaChỉ giáTrịSựThấtBại"); }
        catch (NgoạiLệĐầuRaĐầuVào lỗi) { ĐầuRa.ghiDòng(lỗi.môTả()); }
        try { throw new NgoạiLệTệpThiếu("Tệp giáTrịSựThấtBại"); }
        catch (java.io.IOException lỗi) { ĐầuRa.ghiDòng("표준 상위 ngoạiLệ 호환"); }
        try { hếtGiờMặcĐịnh(); }
        catch (NgoạiLệHếtGiờChờ saiCáchĐãBắtĐãLà) { ĐầuRa.ghiDòng("잘못된 tênThayThế"); }
        catch (java.io.IOException lỗiNguyênBản) { ĐầuRa.ghiDòng("tiếngViệt 예외의 독립된 loạiMụcKiểu"); }
        try { Tệp.đọc("없는한글파일"); }
        catch (NgoạiLệTệpThiếu lỗi) { ĐầuRa.ghiDòng("Tệp lỗi tiếngViệt chuyểnĐổiGiáTrị"); }
        try { KýTự.phânTíchCúPhápSốNguyên("숫자가아님"); }
        catch (SựThấtBạiĐịnhDạngSố lỗi) { ĐầuRa.ghiDòng("giáTrịChữSố lỗi tiếngViệt chuyểnĐổiGiáTrị"); }
        try { CácPhépKiểmTra.đòiHỏi(false, "CácPhépKiểmTra giáTrịSựThấtBại"); }
        catch (NgoạiLệĐốiSốKhôngHợpLệ lỗi) { ĐầuRa.ghiDòng(lỗi.môTả()); }
        try { throw new NgoạiLệCácCậnMảng("cắtXén giáTrịSựThấtBại"); }
        catch (NgoạiLệCácCận lỗi) { ĐầuRa.ghiDòng(lỗi.môTả()); }
        try { throw new NgoạiLệThamChiếuRỗngThamChiếu("빈 thamChiếu"); }
        catch (java.lang.RuntimeException lỗi) { ĐầuRa.ghiDòng("thựcThiLệnh ngoạiLệ 호환"); }
        try { throw new ngoạiLệ("직접 정의한 môTả"); }
        catch (ngoạiLệ lỗi) { ĐầuRa.ghiDòng(lỗi.môTả()); }
        try { throw new NgoạiLệTrạngTháiLuồngChạy("NgoạiLệTrạngTháiLuồngChạy"); }
        catch (NgoạiLệTrạngTháiLuồngChạy lỗi) { ĐầuRa.ghiDòng(lỗi.môTả()); }
        try { throw new NgoạiLệHếtGiờChờ("NgoạiLệHếtGiờChờ"); }
        catch (NgoạiLệHếtGiờChờ lỗi) { ĐầuRa.ghiDòng(lỗi.môTả()); }
        try { throw new NgoạiLệĐãBịNgắtChờ("NgoạiLệĐãBịNgắtChờ"); }
        catch (NgoạiLệĐãBịNgắtChờ lỗi) { ĐầuRa.ghiDòng(lỗi.môTả()); }
        try { throw new NgoạiLệCácCậnChuỗi("NgoạiLệCácCậnChuỗi"); }
        catch (NgoạiLệCácCậnChuỗi lỗi) { ĐầuRa.ghiDòng(lỗi.môTả()); }
        try { throw new NgoạiLệCácCậnMảng("NgoạiLệCácCậnMảng"); }
        catch (NgoạiLệCácCậnMảng lỗi) { ĐầuRa.ghiDòng(lỗi.môTả()); }
        try { throw new SựThấtBạiCấtMảng("SựThấtBạiCấtMảng"); }
        catch (SựThấtBạiCấtMảng lỗi) { ĐầuRa.ghiDòng(lỗi.môTả()); }
        try { throw new NgoạiLệCácCận("NgoạiLệCácCận"); }
        catch (NgoạiLệCácCận lỗi) { ĐầuRa.ghiDòng(lỗi.môTả()); }
        try { throw new NgoạiLệThamChiếuRỗngThamChiếu("NgoạiLệThamChiếuRỗngThamChiếu"); }
        catch (NgoạiLệThamChiếuRỗngThamChiếu lỗi) { ĐầuRa.ghiDòng(lỗi.môTả()); }
        try { throw new SựThấtBạiSốHọc("SựThấtBạiSốHọc"); }
        catch (SựThấtBạiSốHọc lỗi) { ĐầuRa.ghiDòng(lỗi.môTả()); }
        try { throw new NgoạiLệTrạngThái("NgoạiLệTrạngThái"); }
        catch (NgoạiLệTrạngThái lỗi) { ĐầuRa.ghiDòng(lỗi.môTả()); }
        try { throw new SựThấtBạiĐịnhDạngSố("SựThấtBạiĐịnhDạngSố"); }
        catch (SựThấtBạiĐịnhDạngSố lỗi) { ĐầuRa.ghiDòng(lỗi.môTả()); }
        try { throw new NgoạiLệViệcThựcThi("NgoạiLệViệcThựcThi"); }
        catch (NgoạiLệViệcThựcThi lỗi) { ĐầuRa.ghiDòng(lỗi.môTả()); }
        try { throw new ngoạiLệ("ngoạiLệ"); }
        catch (ngoạiLệ lỗi) { ĐầuRa.ghiDòng(lỗi.môTả()); }
        try { throw new SựThấtBạiCỡMảngÂm("SựThấtBạiCỡMảngÂm"); }
        catch (SựThấtBạiCỡMảngÂm lỗi) { ĐầuRa.ghiDòng(lỗi.môTả()); }
        try { throw new NgoạiLệĐầuRaĐầuVào("NgoạiLệĐầuRaĐầuVào"); }
        catch (NgoạiLệĐầuRaĐầuVào lỗi) { ĐầuRa.ghiDòng(lỗi.môTả()); }
        try { throw new NgoạiLệĐốiSốKhôngHợpLệ("NgoạiLệĐốiSốKhôngHợpLệ"); }
        catch (NgoạiLệĐốiSốKhôngHợpLệ lỗi) { ĐầuRa.ghiDòng(lỗi.môTả()); }
        try { throw new NgoạiLệTraCứuĐịaChỉ("NgoạiLệTraCứuĐịaChỉ"); }
        catch (NgoạiLệTraCứuĐịaChỉ lỗi) { ĐầuRa.ghiDòng(lỗi.môTả()); }
        try { throw new NgoạiLệTruyềnThông("NgoạiLệTruyềnThông"); }
        catch (NgoạiLệTruyềnThông lỗi) { ĐầuRa.ghiDòng(lỗi.môTả()); }
        try { throw new NgoạiLệTệpThiếu("NgoạiLệTệpThiếu"); }
        catch (NgoạiLệTệpThiếu lỗi) { ĐầuRa.ghiDòng(lỗi.môTả()); }
        try { throw new NgoạiLệÉpKiểuKiểu("NgoạiLệÉpKiểuKiểu"); }
        catch (NgoạiLệÉpKiểuKiểu lỗi) { ĐầuRa.ghiDòng(lỗi.môTả()); }
        ĐầuRa.ghiDòng("tiếngViệt ngoạiLệ mụcGiáTrịTiếnTrình làĐầyĐủ");
    }
}
