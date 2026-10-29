"""內建 JVM용 中文 class/JAR와 EL0에 넣을 讀取 전용 class 자료를 만든다."""
from pathlib import Path
import json
import zipfile


def 創建Java庫(根路徑, 執行命令):
    (根路徑 / 'build/user').mkdir(parents=True, exist_ok=True)
    輸出結果 = 根路徑 / 'build/java-library'
    類別路徑 = 輸出結果 / 'classes'
    類別路徑.mkdir(parents=True, exist_ok=True)
    原始碼列表 = sorted((根路徑 / '中文Java').rglob('*.java'))
    執行命令(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', 類別路徑] + 原始碼列表)
    條目列列表 = []
    for 原始地址 in 原始碼列表:
        相對路徑 = 原始地址.relative_to(根路徑 / '中文Java').with_suffix('.class')
        載荷數據資料 = (類別路徑 / 相對路徑).read_bytes()
        名稱 = str(相對路徑).replace('/', '.')
        if len(載荷數據資料) > 16384 or len(名稱.encode('utf-8')) > 511:
            raise ValueError('JVM class/name limit: ' + 名稱)
        條目列列表.append((相對路徑, 名稱, 載荷數據資料))
    標頭值 = ['/* Generated class resources; accessed only within the EL0 JVM. */',
              'typedef struct { const char *名稱; const unsigned char *資料; unsigned 大小; } Java類別資源;']
    for 序數索引, (_, 名稱, 載荷數據資料) in enumerate(條目列列表):
        標頭值.append('static const unsigned char Java類別資料%d[] = {%s};' % (序數索引, ','.join(str(第二值) for 第二值 in 載荷數據資料)))
    標頭值.append('static const Java類別資源 Java類別列表[] = {')
    for 序數索引, (_, 名稱, 載荷數據資料) in enumerate(條目列列表):
        標頭值.append('{%s, Java類別資料%d, %d},' % (json.dumps(名稱, ensure_ascii=False), 序數索引, len(載荷數據資料)))
    標頭值.append('};')
    (根路徑 / 'build/user/java-resources.h').write_text('\n'.join(標頭值) + '\n', encoding='utf-8')
    分發路徑 = 根路徑 / 'dist'; 分發路徑.mkdir(exist_ok=True)
    with zipfile.ZipFile(str(分發路徑 / 'jkoros-native-korean.jar'), 'w', compression=zipfile.ZIP_DEFLATED) as Java捆綁:
        for 相對路徑, _, 載荷數據資料 in 條目列列表:
            系統信息 = zipfile.ZipInfo(str(相對路徑), date_time=(1980, 1, 1, 0, 0, 0)); 系統信息.compress_type = zipfile.ZIP_DEFLATED
            Java捆綁.writestr(系統信息, 載荷數據資料)
    with zipfile.ZipFile(str(分發路徑 / 'jkoros-native-korean-sources.zip'), 'w', compression=zipfile.ZIP_DEFLATED) as 存檔:
        for 原始地址 in 原始碼列表:
            系統信息 = zipfile.ZipInfo(str(原始地址.relative_to(根路徑 / '中文Java')), date_time=(1980, 1, 1, 0, 0, 0)); 系統信息.compress_type = zipfile.ZIP_DEFLATED
            存檔.writestr(系統信息, 原始地址.read_bytes())
