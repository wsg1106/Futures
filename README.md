

<!---
wsg1106/wsg1106 is a ✨ special ✨ repository because its `README.md` (this file) appears on your GitHub profile.
You can click the Preview link to take a look at your changes.
--->
里面包含4个文件，都经过测试可以正常运行。
第一个：qh5min-csv.py   是由通达信期货通中的五分钟数据下载文件，转换为格式csv文件。
第二个：qh5-15min.py  是把上述的5分钟csv格式文件 转换为周期15分钟的csv文件。
第三个：qh15-30min.py 是把上述15分钟csv格式文件 转换为周期30分钟的csv文件。
第四个：qh15-60min.py 是把上述15分钟csv格式文件转换为周期60分钟的csv文件。

其中第一个文件是基于网上 “python处理通达信 5分钟数据 .lc5文件处理，生成csv文件，期货回测” 这篇文章中代码测试而得。
第二个文件是基于网上“python通达信5分钟转，10分钟，15分钟，30分钟，60分钟，量化交易，K线” 代码改写而得（源代码无法正常运行，缺少一个库）。
第三个文件是根据第二个文件的框架改编。由于用resample函数只能实现整时间段的时间统计，无法达到通达信软件上面那种跨时间周期的K线方法，所以自己改写了该代码。
第四个文件跟上述原因一样。
