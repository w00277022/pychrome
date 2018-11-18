import pychrome

browser = pychrome.Browser('http://127.0.0.1:%d' % 9222)
tab = browser.new_tab()
tab.start()
tab.Runtime.enable()
tab.Page.navigate(url="https://github.com/fate0/pychrome", _timeout=5)
# 设置等待页面加载完成的时间
tab.wait(10)
# 运行js脚本
timing_remote_object = tab.Runtime.evaluate(
    expression='performance.timing'
)
# 获取performance.timing结果数据
timing_properties = tab.Runtime.getProperties(
    objectId=timing_remote_object.get('result').get('objectId')
)
timing = {}
for item in timing_properties.get('result'):
    if item.get('value', {}).get('type') == 'number':
        timing[item.get('name')] = item.get('value').get('value')

timingRes = {}

timingRes['domainLookupTime'] = timing['domainLookupEnd'] - timing['domainLookupStart']
timingRes['TCPConnectTime'] = timing['connectEnd'] - timing['connectStart']
timingRes['ttfb'] = timing['responseStart'] - timing['navigationStart']
timingRes['requestTime'] = timing['responseEnd'] - timing['requestStart']
timingRes['waitTime'] = timing['domLoading'] - timing['navigationStart']
timingRes['renderDomTime'] = timing['domComplete'] - timing['domLoading']
timingRes['loadPageTime'] = timing['loadEventEnd'] - timing['fetchStart']

print(timingRes)

# 获取performance.getEntries()数据
entries_remote_object = tab.Runtime.evaluate(
    expression='performance.getEntries()'
)
entries_properties = tab.Runtime.getProperties(
    objectId=entries_remote_object.get('result').get('objectId')
)
entries_values = []
for item in entries_properties.get('result'):
    if item.get('name').isdigit():
        url_timing_properties = tab.Runtime.getProperties(
            objectId=item.get('value').get('objectId')
        )

        entries_value = {}
        for son_item in url_timing_properties.get('result'):
            if (son_item.get('value', {}).get('type') == 'number' or
                    son_item.get('value', {}).get('type') == 'string'):
                entries_value[son_item.get('name')] = son_item.get('value').get('value')
        entries_values.append(entries_value)
print(entries_values)

# function getTimes()
# # {
# #     var t = performance.timing;
# #     var timing = {
# #         domainLookupTime: t.domainLookupEnd - t.domainLookupStart,
# #         TCPConnectTime: t.connectEnd - t.connectStart,
# #           ttfb: t.responseStart - t.navigationStart,
# #         requestTime: t.responseEnd - t.requestStart,
# #           waitTime: t.domLoading - t.navigationStart,
# #             renderDomTime: t.domComplete - t.domLoading,
# #           loadPageTime: t.loadEventEnd - t.fetchStart
# #         }
# # }
# # getTimes();
