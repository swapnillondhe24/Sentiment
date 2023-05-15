from Scraper.reviews import generate_data

data = generate_data('https://www.amazon.in/Bassbuds-Duo-Headphones-Water-Resistant-Assistance/dp/B09DD9SX9Z/ref=sr_1_1?_encoding=UTF8&_ref=dlx_gate_sd_dcl_tlt_04410e8d_dt&content-id=amzn1.sym.9e4ae409-2145-4395-aa6e-45d7f3e95c3e&pd_rd_r=81b7691e-3f71-41a4-bf8e-549b314a692e&pd_rd_w=D8FkQ&pd_rd_wg=5AAru&pf_rd_p=9e4ae409-2145-4395-aa6e-45d7f3e95c3e&pf_rd_r=KSHN3MBQKSQWTSEM51MT&qid=1684171691&sr=8-1')
print(data)