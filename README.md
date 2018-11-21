# update_stock_value
Update the value of stock share (total value and net value). Run after every trading day. 

更新个人持仓的股票市值，并计算净值。每个交易日收盘后运行一次

Python 3
需要Tushare
支持A股和港股

使用方法：
1. 在Real_combination_info.xlsx中按照现有的格式输入自己的真实持仓并保存
2. 在Initial_invest.xlsx的price里输入初始本金并保存
3. （可选） 在Currency.xlsx中输入港币汇率
4. 运行脚本（可在这里指定港币汇率）：
Python update_simplified_combination.py (-c 0.88)
