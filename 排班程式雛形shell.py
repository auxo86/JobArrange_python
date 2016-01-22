import sqlite3
from prettytable import PrettyTable

def rows_to_list(rows, x=0):
    return [r[x] for r in rows]

def read_source(c):
    c.execute('select job_name from job where monday_job = 1 order by job_order' )
    job_rec_set = rows_to_list(c.fetchall())
    #job_rec_set.append(['-------------'])
    c.execute('select name from member_array where by_pass = 0 and discount = 0 order by arrange_order')
    routine_member_rec_set = rows_to_list(c.fetchall())
    #routine_member_rec_set.append(['-------------'])
    c.execute('select name from member_array where by_pass = 0 and discount = 1 order by arrange_order')
    discount_member_rec_set = rows_to_list(c.fetchall())
    #discount_member_rec_set.append(['-------------'])
    return job_rec_set, routine_member_rec_set, discount_member_rec_set

def do_proc(head_line, body):
    if len(body) % len(head_line) != 0:
        n = len(head_line) - len(body) % len(head_line)
        body.extend(['',]*n)
    it = iter(body)
    body_lines = zip(*[it,]*len(head_line))
    return body_lines

def print_out(head_line, body_lines):
    pt = PrettyTable(head_line)
    for line in body_lines:
        pt.add_row(line)
    print(pt)

def main():
    conn = sqlite3.connect('job_arrange.db')
    c = conn.cursor()
    try:
        job_rec_set, routine_member_rec_set, discount_member_rec_set = read_source(c)
    finally:
        conn.close()

    head_line = job_rec_set
    body = routine_member_rec_set + discount_member_rec_set
    body_lines = do_proc(head_line, body)
    print_out(head_line, body_lines)

if __name__ == '__main__': main()

# for x in list_array:
#     i=0
#     for y in x:
#         print(y[0], end='\t')
#         i+=1
#         if i%12 == 0:
#             print()
#     print()



##print('禮拜一的工作點:')
##for x in job_rec_set:
##    print (x[0])
##print('照排的人員:')
##for x in routine_member_rec_set:
##    print (x[0])
##print('折扣的人員:')
##for x in discount_member_rec_set:
##    print (x[0])
