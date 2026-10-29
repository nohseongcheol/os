// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package tiếngViệt.Java;

import java.io.IOException;
import java.net.*;
import java.net.http.*;
import java.nio.charset.StandardCharsets;
import java.time.Duration;

public final class TruyềnThông {
    private TruyềnThông() {}
    /** Trả toàn bộ phản hồi để bên gọi cũng đánh giá được mã trạng thái lỗi HTTP. */
    public static HttpResponse<String> giáTrịThu(URI địaChỉ, Duration giớiHạnThờiGian)
            throws IOException, InterruptedException {
        HttpClient nốiKết = HttpClient.newBuilder().connectTimeout(giớiHạnThờiGian).build();
        return nốiKết.send(HttpRequest.newBuilder(địaChỉ).timeout(giớiHạnThờiGian).GET().build(),
                HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8));
    }
    public static Socket kếtNốiĐiểmCuối(String địaChỉ, int cổngPhầnCứng, int miliGiâyGiớiHạn) throws IOException {
        Socket nốiKết = new Socket();
        try {
            nốiKết.connect(new InetSocketAddress(địaChỉ, cổngPhầnCứng), miliGiâyGiớiHạn);
            nốiKết.setSoTimeout(miliGiâyGiớiHạn);
            return nốiKết;
        } catch (IOException lỗi) { nốiKết.close(); throw lỗi; }
    }
}
