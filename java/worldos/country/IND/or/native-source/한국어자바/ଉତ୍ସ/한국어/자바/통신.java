// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.io.IOException;
import java.net.*;
import java.net.http.*;
import java.nio.charset.StandardCharsets;
import java.time.Duration;

public final class 통신 {
    private 통신() {}
    /** HTTP ତ୍ରୁଟି 상태도 호출자가 판단할 수 있도록 ପ୍ରତ୍ୟୁତ୍ତର_କରନ୍ତୁ 전체를 반환한다. */
    public static HttpResponse<String> 가져오기(URI ଠିକଣା, Duration ସମୟ_ସୀମା)
            throws IOException, InterruptedException {
        HttpClient ସଂଯୋଗ_କରନ୍ତୁ = HttpClient.newBuilder().connectTimeout(ସମୟ_ସୀମା).build();
        return ସଂଯୋଗ_କରନ୍ତୁ.send(HttpRequest.newBuilder(ଠିକଣା).timeout(ସମୟ_ସୀମା).GET().build(),
                HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8));
    }
    public static Socket 연결하기(String ଠିକଣା, int ହାର୍ଡୱେର୍_ପୋର୍ଟ, int 제한밀리초) throws IOException {
        Socket ସଂଯୋଗ_କରନ୍ତୁ = new Socket();
        try {
            ସଂଯୋଗ_କରନ୍ତୁ.connect(new InetSocketAddress(ଠିକଣା, ହାର୍ଡୱେର୍_ପୋର୍ଟ), 제한밀리초);
            ସଂଯୋଗ_କରନ୍ତୁ.setSoTimeout(제한밀리초);
            return ସଂଯୋଗ_କରନ୍ତୁ;
        } catch (IOException ତ୍ରୁଟି) { ସଂଯୋଗ_କରନ୍ତୁ.close(); throw ତ୍ରୁଟି; }
    }
}
