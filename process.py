# import libraries
import re
import random
import csv

# set initial variables
file_num = 1
output = open('./output_files/all_search_queries.html', 'w')
output_csv = csv.writer(open('./output_files/output.csv', 'w'))
logs_parsed = queries_written = num_of_deeps = local_search = advanced = browse = course_reserve = 0

while file_num < 30:
    logfile = open('./access_logs/localhost_access_log.2016-02-{0}.txt'.format(file_num), 'r')
    headers = logfile.readlines()
    for header in headers:
        log = re.search('(^\d+[.]\d+[.]\d+[.]\d+) - - [()[]+(\d+/Feb/2016):(\d+:\d+:\d+)', header)
        query_type = []
        if log:
            ip = log.group(1)
            date = log.group(2)
            time = log.group(3)
            m = re.search('GET (/primo_library/libweb/action/d?l?S?s?earch\.do.*) HTTP/1.1', header)
            if m is not None and ip != '10.14.0.4' and ip != '10.28.0.10':
                m = m.group(1)
                if m.find('ct=facet') == -1 and m.find('ct=Next') == -1 and m.find('fn=showBrowse') == -1 and m.find('&isSerivcesPage=true') == -1 and m.find('%2B') == -1 and m.find('fn=Browse') == -1 and m.find('&fct') == -1 and m.find('tab=cr') == -1 and m.find('VQA') == -1 and (m.find('indx=1') > 0 or m.find('indx') == -1) and (m.find('query=') > 0 or m.find('freeText') > 0):
                    query = ''
                    issn = ''
                    if m.find('query=') > 0:
                        query = re.search('query=any[%2C,]+contains[%2C,]+([a-zA-z+%207]*)', m)
                        if query is not None:
                            query = query.group(1)
                            print(query)
                        else:
                            query = ''
                            issn = ''
                            issn = re.search('query=is[sb]n[%2C,]+[exactcoins]+[%2C,]+([0-9-]*)', m)
                            if issn is not None:
                                issn = issn.group(1)
                    logs_parsed += 1
                    link = 'http://utk-almaprimo.hosted.exlibrisgroup.com' + m
                    if "afterPDS=" not in link and "almaAzSearch=" not in link:
                        if 'dlSearch' in link:
                            query_type.append('Deep Link')
                            num_of_deeps += 1
                        else:
                            query_type.append('Internal Search')
                        if '&tab=local_tab' in link:
                            query_type.append('UT Collections')
                            local_search += 1
                        if '&tab=default_tab' in link:
                            query_type.append('One Search')
                        if 'mode=Advanced' in link:
                            query_type.append('Advanced Search')
                            advanced += 1
                        if '&mode=BrowseSearch' in link:
                            query_type.append('Browse Search')
                            browse += 1
                        if '&tab=cr_tab' in link:
                            query_type.append('Course Reserve')
                            course_reserve += 1
                        output.write('<a href="' + link + '">' + str(logs_parsed) + '</a>&nbsp;&nbsp;&nbsp;Type: ' + str(query_type) + '</b>\n')
                        output_csv.writerow([str(logs_parsed), date, time, query, issn, link])
                        queries_written += 1
    file_num += 1
print("Number of logs parsed: {0}\n".format(logs_parsed))
print("Number of queries written to file: {0}\n".format(queries_written))
print("Number of deep links: {0}\n".format(num_of_deeps))
print("Number of local searches: {0}\n".format(local_search))
print("Number of advanced searches: {0}\n".format(advanced))
print("Number of browse searches: {0}\n".format(browse))
print("Number of course reserve searches: {0}\n".format(course_reserve))

subs = open('./output_files/sample_set_search_queries.html', 'w')
inp2 = open('./output_files/all_search_queries.html', 'r')
subset = random.sample(inp2.readlines(), 100)
subs.write("<br>".join(str(x) for x in subset))
