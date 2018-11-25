import re

def main():
    readfilename = "miniproj2-small-data.txt"
    generate_files(readfilename)
    
''' generates the 4 text files (terms.txt, pdates.txt, prices.txt, ads.txt) '''
def generate_files(readfile):
    rfile = open(readfile, "r")
    termfile = open("terms.txt", "w")
    datefile = open("pdates.txt", "w")
    pricefile = open("prices.txt", "w")
    adfile = open("ads.txt", "w")
    
    for line in rfile:
        if line.startswith("<ad>"):
            aid = get_text("aid", line)[0].lower()
            try:
                title = get_text("ti", line)
                write_term(aid, title, termfile)
                desc = get_text("desc", line)
                write_term(aid, desc, termfile)     
            except:
                print("Error when writing terms.txt")
            
            try:
                string = get_text('date', line)[0]+":"+aid+","+get_text("cat", line)[0]+","+get_text("loc", line)[0]+"\n" 
                datefile.write(string)
            except:
                print("Error when writing pdates.txt")
            
            try:
                string = "\t"+get_text('price', line)[0]+":"+aid+","+get_text("cat", line)[0]+","+get_text("loc", line)[0]+"\n" #added tab 
                pricefile.write(string)
            except:
                print("Error when writing prices.txt")
            
            try:
                string = aid+":"+line.lower() #added lower
                adfile.write(string)
            except:
                print("Error when writing ads.txt")

    rfile.close()
    termfile.close()
    datefile.close()
    pricefile.close()
    adfile.close()
    
''' given the tag name, and the line to examine it will return a list of the words between the tags '''
def get_text(tag, line):
    try:
        string = re.search("<"+tag+">"+"(.*)"+"</"+tag+">", line).group(1).lower() #added lower here 
    except:
        print("tag doesn't exist")
        return []
    string = replace(string)
    L = []

    if tag == "ti" or tag == "desc":
        s = 0
        pat = "[0-9a-zA-Z_-]"
        while re.match(pat, string[s]) == None and s<len(string)-1:
            s+=1
        i = s+1
        while i<len(string):
            if i==len(string)-1:
                if re.match("[0-9a-zA-Z_-]", string[i])==None:
                    L.append(string[s:i])
                else:
                    L.append(string[s:i+1])
            else:
                if re.match("[0-9a-zA-Z_-]", string[i])==None:
                    L.append(string[s:i])
                    s=i+1
                    while re.match("[0-9a-zA-Z_-]", string[s])==None and s<len(string)-1:
                        s+=1
                    i=s
            i+=1
    else:
        L = string.split()
    return L

''' replaces &quot, &apos, &amp, and removes special characters of the form &#number'''
def replace(line):
    line = line.replace("&quot", "\"")
    line = line.replace("&apos", "\'")
    line = line.replace("&amp", "&")
    remove = []
    for match in re.finditer("&#", line):
        s = match.start()
        i = match.end()
        while i<len(line) and re.match("[0-9;]", line[i]):
            i+=1
        remove.append(line[s:i])
    for t in remove:
        line = line.replace(t, "")
    return line

''' iterates through each word in the array, checks if it meets the qualifications, 
    and if so it writes the word and aid to the file given. '''
def write_term(aid, array, file):
    for word in array:
        if len(word)>2:
            string = re.sub('[^0-9a-zA-Z_-]', '', word).lower()+":"+aid+"\n" 
            file.write(string)
            
main()
