// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.io.IOException;
import java.net.*;
import java.net.http.*;
import java.nio.charset.StandardCharsets;
import java.time.Duration;

public final class 통신 {
    private 통신() {}
    /** HTTP പിശക് 상태도 호출자가 판단할 수 있도록 മറുപടി_നൽകുക 전체를 반환한다. */
    public static HttpResponse<String> 가져오기(URI ഇമെയിൽ, Duration സമയ_പരിധി)
            throws IOException, InterruptedException {
        HttpClient കണക്ടു്_ചെയ്യുക = HttpClient.newBuilder().connectTimeout(സമയ_പരിധി).build();
        return കണക്ടു്_ചെയ്യുക.send(HttpRequest.newBuilder(ഇമെയിൽ).timeout(സമയ_പരിധി).GET().build(),
                HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8));
    }
    public static Socket കണക്റ്റ്_അവസാനബിന്ദു(String ഇമെയിൽ, int 포트, int 제한밀리초) throws IOException {
        Socket കണക്ടു്_ചെയ്യുക = new Socket();
        try {
            കണക്ടു്_ചെയ്യുക.connect(new InetSocketAddress(ഇമെയിൽ, 포트), 제한밀리초);
            കണക്ടു്_ചെയ്യുക.setSoTimeout(제한밀리초);
            return കണക്ടു്_ചെയ്യുക;
        } catch (IOException പിശക്) { കണക്ടു്_ചെയ്യുക.close(); throw പിശക്; }
    }
}
