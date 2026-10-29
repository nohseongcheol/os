"""tựThân JVM용 tiếngViệt class/JAR와 EL0에 넣을 đọc 전용 class 자료를 만든다."""
from pathlib import Path
import json
import zipfile


def tạoThưViệnJava(đườngDẫnGốcCây, thựcThiLệnh):
    (đườngDẫnGốcCây / 'build/user').mkdir(parents=True, exist_ok=True)
    đầuRa = đườngDẫnGốcCây / 'build/java-library'
    đườngDẫnLớp = đầuRa / 'classes'
    đườngDẫnLớp.mkdir(parents=True, exist_ok=True)
    DanhSáchMãNguồn = sorted((đườngDẫnGốcCây / 'JavaTiếngViệt').rglob('*.java'))
    thựcThiLệnh(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', đườngDẫnLớp] + DanhSáchMãNguồn)
    danhSáchCácMục = []
    for địaChỉNguyênBản in DanhSáchMãNguồn:
        đườngDẫnTươngĐối = địaChỉNguyênBản.relative_to(đườngDẫnGốcCây / 'JavaTiếngViệt').with_suffix('.class')
        dữLiệuNộiTải = (đườngDẫnLớp / đườngDẫnTươngĐối).read_bytes()
        tên = str(đườngDẫnTươngĐối).replace('/', '.')
        if len(dữLiệuNộiTải) > 16384 or len(tên.encode('utf-8')) > 511:
            raise ValueError('JVM class/name limit: ' + tên)
        danhSáchCácMục.append((đườngDẫnTươngĐối, tên, dữLiệuNộiTải))
    giáTrịĐầuMục = ['/* Generated class resources; accessed only within the EL0 JVM. */',
              'typedef struct { const char *tên; const unsigned char *DữLiệu; unsigned cỡ; } TàiNguyênLớpJava;']
    for chỉSốThứBậc, (_, tên, dữLiệuNộiTải) in enumerate(danhSáchCácMục):
        giáTrịĐầuMục.append('static const unsigned char dữLiệuLớpJava%d[] = {%s};' % (chỉSốThứBậc, ','.join(str(giáTrịThứHai) for giáTrịThứHai in dữLiệuNộiTải)))
    giáTrịĐầuMục.append('static const TàiNguyênLớpJava danhSáchLớpJava[] = {')
    for chỉSốThứBậc, (_, tên, dữLiệuNộiTải) in enumerate(danhSáchCácMục):
        giáTrịĐầuMục.append('{%s, dữLiệuLớpJava%d, %d},' % (json.dumps(tên, ensure_ascii=False), chỉSốThứBậc, len(dữLiệuNộiTải)))
    giáTrịĐầuMục.append('};')
    (đườngDẫnGốcCây / 'build/user/java-resources.h').write_text('\n'.join(giáTrịĐầuMục) + '\n', encoding='utf-8')
    đườngDẫnBảnPhânPhối = đườngDẫnGốcCây / 'dist'; đườngDẫnBảnPhânPhối.mkdir(exist_ok=True)
    with zipfile.ZipFile(str(đườngDẫnBảnPhânPhối / 'jkoros-native-korean.jar'), 'w', compression=zipfile.ZIP_DEFLATED) as góiGộpJava:
        for đườngDẫnTươngĐối, _, dữLiệuNộiTải in danhSáchCácMục:
            thôngTinHệThống = zipfile.ZipInfo(str(đườngDẫnTươngĐối), date_time=(1980, 1, 1, 0, 0, 0)); thôngTinHệThống.compress_type = zipfile.ZIP_DEFLATED
            góiGộpJava.writestr(thôngTinHệThống, dữLiệuNộiTải)
    with zipfile.ZipFile(str(đườngDẫnBảnPhânPhối / 'jkoros-native-korean-sources.zip'), 'w', compression=zipfile.ZIP_DEFLATED) as khoLưuTrữ:
        for địaChỉNguyênBản in DanhSáchMãNguồn:
            thôngTinHệThống = zipfile.ZipInfo(str(địaChỉNguyênBản.relative_to(đườngDẫnGốcCây / 'JavaTiếngViệt')), date_time=(1980, 1, 1, 0, 0, 0)); thôngTinHệThống.compress_type = zipfile.ZIP_DEFLATED
            khoLưuTrữ.writestr(thôngTinHệThống, địaChỉNguyênBản.read_bytes())
