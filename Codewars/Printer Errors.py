import re
def printer_error(s):
    long= len(s)
    over=len(re.findall('[nopqrstuvwxyz]', s))
    
    return (str(over)+"/"+str(long))
