import os
import html

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# 頁面共用 CSS 樣式
STYLE = """
<style>
    body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif; margin: 40px; background: #f8f9fa; color: #333; }
    .container { max-width: 800px; margin: 0 auto; background: #fff; padding: 30px; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.08); }
    h1 { border-bottom: 2px solid #0066cc; padding-bottom: 10px; font-size: 24px; color: #1a1a1a; }
    .breadcrumb { margin-bottom: 20px; font-size: 14px; color: #666; }
    .breadcrumb a { color: #0066cc; text-decoration: none; }
    .breadcrumb a:hover { text-decoration: underline; }
    .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 15px; margin-top: 20px; }
    .card { display: block; padding: 20px; background: #f1f5f9; border-radius: 6px; text-align: center; text-decoration: none; color: #0066cc; font-weight: bold; transition: all 0.2s; border: 1px solid #e2e8f0; }
    .card:hover { background: #0066cc; color: #fff; transform: translateY(-2px); }
    .gallery { display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 20px; margin-top: 20px; }
    .img-card { background: #fff; border: 1px solid #ddd; padding: 10px; border-radius: 6px; text-align: center; }
    .img-card img { max-width: 100%; height: auto; border-radius: 4px; }
</style>
"""

# 名詞對照表（將英文資料夾名轉為中文顯示）
NAME_MAP = {
    "Wind Vector":"Wind Vector",
    "Microwave":"Microwave",
    "Polar Image":"Polar Satellite Imagery",
    "Precipitation Radar":"Precipitation Radar",
    "Science Product":"Science Product",
    "ASCAT":"ASCAT",
    "QuikSCAT":"QuikSCAT",
    "ERS-1&2":"ERS-1&2",
    "WindRAD":"WindRAD",
    "OSCAT":"OSCAT",
    "SMAP":"SMAP",
    "AMSR":"AMSR",
    "SSMI&SSMIS":"SSMI&SSMIS",
    "TMI&GMI":"TMI&GMI",
    "MWRI":"MWRI",
    "MWI":"MWI",
    "MODIS":"MODIS",
    "AVHRR":"AVHRR",
    "VIIRS":"VIIRS",
    "MERSI&VIRR":"MERSI&VIRR",
    "SGLI&GLI":"SGLI&GLI",
    "SLSTR&AATSR&ATSR":"SLSTR&AATSR&ATSR",
    "VIRS":"VIRS",
    "SeaWiFS":"SeaWiFS",
    "OLCI&MERIS":"OLCI&MERIS",
    "EarthCARE":"EarthCARE",
    "METimage":"METimage",
    "TRMM PR":"TRMM-PR",
    "GPM DPR":"GPM-DPR",
    "FY3 PMR":"FY3G-PMR",
    "R34 Measurement":"R34 Measurement",
}

def get_display_name(name):
    return NAME_MAP.get(name, name)

def render_page(title, breadcrumb_html, content_html, output_path):
    full_html = f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{html.escape(title)}</title>
    {STYLE}
</head>
<body>
    <div class="container">
        <div class="breadcrumb">{breadcrumb_html}</div>
        <h1>{html.escape(title)}</h1>
        {content_html}
    </div>
</body>
</html>"""
    
    dir_name = os.path.dirname(output_path)
    if dir_name:  
        os.makedirs(dir_name, exist_ok=True)
        
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(full_html)

def build_multilevel_site(data_root="Data"):
    
    if not os.path.exists(data_root):
        print(f"請先建立 {data_root} 資料夾並放入數據分類！")
        return

    # 第 1 層：首頁 (資料類別)
    categories = [d for d in os.listdir(data_root) if os.path.isdir(os.path.join(data_root, d))]
    cat_cards = "".join([f'<a href="{data_root}/{cat}/index.html" class="card">{get_display_name(cat)}</a>' for cat in categories])
    render_page("Satellite Imagery Archive @Ethan_ku", "Main", f'<div class="grid">{cat_cards}</div>', "index.html")

    for cat in categories:
        cat_dir = os.path.join(data_root, cat)
        instruments = [d for d in os.listdir(cat_dir) if os.path.isdir(os.path.join(cat_dir, d))]
        
        # 第 2 層：儀器分類頁
        inst_cards = "".join([f'<a href="{inst}/index.html" class="card">{get_display_name(inst)}</a>' for inst in instruments])
        bread = f'<a href="../../index.html">Main</a> / {get_display_name(cat)}'
        render_page(f"{get_display_name(cat)}", bread, f'<div class="grid">{inst_cards}</div>', f"{cat_dir}/index.html")

        for inst in instruments:
            inst_dir = os.path.join(cat_dir, inst)
            years = [d for d in os.listdir(inst_dir) if os.path.isdir(os.path.join(inst_dir, d))]
            
            # 第 3 層：時間分類頁
            year_cards = "".join([f'<a href="{y}/index.html" class="card">{y}</a>' for y in sorted(years, reverse=True)])
            bread = f'<a href="../../../index.html">Main</a> / <a href="../index.html">{get_display_name(cat)}</a> / {get_display_name(inst)}'
            render_page(f"{get_display_name(inst)}", bread, f'<div class="grid">{year_cards}</div>', f"{inst_dir}/index.html")

            for y in years:
                year_dir = os.path.join(inst_dir, y)
                cyclones = [d for d in os.listdir(year_dir) if os.path.isdir(os.path.join(year_dir, d))]
                
                # 第 4 層：氣旋系統分類頁
                cyc_cards = "".join([f'<a href="{c}/index.html" class="card">{get_display_name(c)}</a>' for c in cyclones])
                bread = f'<a href="../../../../index.html">Main</a> / <a href="../../index.html">{get_display_name(cat)}</a> / <a href="../index.html">{get_display_name(inst)}</a> / {y}'
                render_page(f"{y}", bread, f'<div class="grid">{cyc_cards}</div>', f"{year_dir}/index.html")

                for c in cyclones:
                    cyc_dir = os.path.join(year_dir, c)
                    dates = [d for d in os.listdir(cyc_dir) if os.path.isdir(os.path.join(cyc_dir, d))]
                    
                    # 第 5 層：日期分類頁
                    date_cards = "".join([f'<a href="{d_name}/index.html" class="card">{d_name}</a>' for d_name in sorted(dates)])
                    bread = f'<a href="../../../../../index.html">Main</a> / <a href="../../../index.html">{get_display_name(cat)}</a> / <a href="../../index.html">{get_display_name(inst)}</a> / <a href="../index.html">{y}</a> / {get_display_name(c)}'
                    render_page(f"{get_display_name(c)}", bread, f'<div class="grid">{date_cards}</div>', f"{cyc_dir}/index.html")

                    for d_name in dates:
                        date_dir = os.path.join(cyc_dir, d_name)
                        files = [f for f in os.listdir(date_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.nc', '.gif'))]
                        
                        # 第 6 層：最終數據/圖片展示頁
                        img_cards = ""
                        for f in files:
                            img_cards += f'''
                            <div class="img-card">
                                <a href="{f}" target="_blank"><img src="{f}" alt="{f}"></a>
                                <p>{f}</p>
                            </div>'''
                        
                        bread = f'<a href="../../../../../../index.html">Main</a> / <a href="../../../../index.html">{get_display_name(cat)}</a> / <a href="../../../index.html">{get_display_name(inst)}</a> / <a href="../../index.html">{y}</a> / <a href="../index.html">{get_display_name(c)}</a> / {d_name}'
                        render_page(f"{d_name}", bread, f'<div class="gallery">{img_cards}</div>', f"{date_dir}/index.html")

    print("✅ 多層級靜態網頁已全部生成完畢！")

if __name__ == "__main__":
    build_multilevel_site()

#git add .
#git commit -m "update"
#git push