import akshare as ak
import pandas as pd
import json
from datetime import date, datetime

def json_serial(obj):
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))

def get_hk_data(symbol="01448"):
    result = {}
    
    # 1. Basic Info & Spot
    try:
        df_spot = ak.stock_hk_spot_em()
        row = df_spot[df_spot['代码'] == symbol]
        if not row.empty:
            result['basic'] = row.to_dict(orient='records')[0]
    except Exception as e:
        result['basic_error'] = str(e)
        
    # 2. Financial Indicators
    try:
        df_ind = ak.stock_hk_financial_indicator_em(symbol=symbol)
        if not df_ind.empty:
            result['indicators'] = df_ind.head(5).to_dict(orient='records')
    except Exception as e:
        result['indicators_error'] = str(e)

    # 3. Financial Reports (to get specific line items for Asset Value and EPV)
    # stock_financial_hk_report_em usually returns a list of reports or specific one
    try:
        # Looking at akshare docs/source, this usually needs indicator like '资产负债表'
        for report_type in ['资产负债表', '利润表', '现金流量表']:
            df = ak.stock_financial_hk_report_em(symbol=symbol, indicator=report_type)
            if not df.empty:
                result[report_type] = df.head(5).to_dict(orient='records')
    except Exception as e:
        result['reports_error'] = str(e)

    return result

if __name__ == "__main__":
    data = get_hk_data("01448")
    print(json.dumps(data, ensure_ascii=False, indent=2, default=json_serial))
