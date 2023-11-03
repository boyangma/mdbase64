from PIL import Image
import os
import base64
import re
import sys
from urllib import request, parse
from io import BytesIO
import requests


def local_img_base64(filepath): 
    with open(filepath,"rb") as img:
        img_base64 = base64.b64encode(img.read())
        return str(img_base64)[2:-1]

def web_img_base64(url): 
    buffered = BytesIO(requests.get(url).content)  
    img_base64 = base64.b64encode(buffered.getvalue()) 
    return str(img_base64)[2:-1]

def get_all_md_files(path):
    files = []
    print("Find following md files: ")
    for file in os.listdir(path):
        if file.endswith('md'):
            temp_path = path + '/' + file
            files.append(temp_path)
            print(temp_path)
    print("\n")
    return files

def convert(file_path, output_path):
    filename = os.path.basename(file_path)
    dirname = os.path.dirname(file_path)
    print("Processing the file:")
    print(file_path)
    print("filename: ", filename)
    print("dir: ", dirname)
    print("\n")

    with open(file_path,"r",encoding="utf-8") as md:
        pic_num = 0  
        base64_pic_quote_list = []
        transformed = open(output_path + os.path.sep + filename,"w",encoding="utf-8") 
        for line in md:
            if(re.search(r"!\[[^]]*\].*",line)): 
                img_sents = re.findall(r'!\[[^[\]]*\]\(.+\)$',line.strip())
                for img_sent in img_sents:
                        start_index = img_sent.find('](')
                        end_index = img_sent.rfind(')')
                        raw_img_path = img_sent[start_index+2:end_index]
                raw_img_path = parse.unquote(raw_img_path)
                
                if not(re.match("data",raw_img_path) or re.match("http",raw_img_path)): 
                    print("find local image: ",raw_img_path)
                    pic_num = pic_num + 1
                    pic_name = re.search(r"\[.*?\]",line).group()[1:-1]
                    pic_num_str = "Fig" + str(pic_num)  
                    pic_new_quote = "![" + pic_name + "][" + pic_num_str + "]" 
                    line = re.sub(r"!\[[^]]*\]\([^)]*\)",pic_new_quote,line)  
                    raw_ima_absolute_path = os.path.join(dirname, raw_img_path).replace("\\","/") 
                    base64_pic_quote = "[" + pic_num_str + "]:data:image/png;base64," + local_img_base64(raw_ima_absolute_path) 
                    base64_pic_quote_list.append(base64_pic_quote)                  
                elif(re.match("http",raw_img_path)):
                    print("find web image: ",raw_img_path)
                    pic_num = pic_num + 1
                    pic_name = re.search(r"\[.*?\]",line).group()[1:-1]
                    pic_num_str = "Fig" + str(pic_num) 
                    pic_new_quote = "![" + pic_name + "][" + pic_num_str + "]"  
                    line = re.sub(r"!\[[^]]*\]\([^)]*\)",pic_new_quote,line)  
                    base64_pic_quote = "[" + pic_num_str + "]:data:image/png;base64," + web_img_base64(raw_img_path)                
                    base64_pic_quote_list.append(base64_pic_quote)
                    
            transformed.write(line) 

        for i in range(1,30):
            transformed.write("\n")
       
        for base64_pic_quote in base64_pic_quote_list:
            transformed.write(base64_pic_quote)
            transformed.write("\n")
        
        transformed.close()
        print("\n")

if __name__=="__main__":
    if len(sys.argv) > 2:
        work_path = sys.argv[1]
        output_path = sys.argv[2]
        work_path = work_path.replace("\\","/").rstrip("/")
        if '"' in work_path:
            work_path = eval(work_path)
        output_path = output_path.replace("\\","/").rstrip("/")
        if '"' in output_path:
            output_path = eval(output_path)
        print("work path: ", work_path,"\n")
        print("output path: ",output_path,"\n")
    else:
        print("\n")
        print("missing parameters!")
        print("Please enter \"work path\" & \"output_path\"!\n\n")
        sys.exit()

    if not os.path.exists(output_path):
        os.makedirs(output_path)
    else:
        print("output_path is exist\n\n")

    if os.path.isdir(work_path):
        files = get_all_md_files(work_path)
        for file in files:
            convert(file, output_path)
        print("Done!\n\n")
    elif os.path.isfile(work_path):
        convert(work_path, output_path)
        print("Done!\n\n")
