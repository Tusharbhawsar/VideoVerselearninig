import os 
import pandas as pd 
import csv
rally="/home/link-lap-24/vollyballdeshdata/negative_data_sorted/negative/"
#rally_like="/home/link-lap-24/vollyballdeshdata/rally_data_sorted/rally_like/"

maincsv= pd.read_csv("/home/link-lap-24/vollyballdeshdata/Negative.csv")
new_csv  = "negative_correct.csv"
# os.mkdir(new_csv)
#start_name="https://ai-studio-new.s3-ap-south-1.amazonaws.com/ai-studio/620350ff8a5c7412be56361f/data/"

# csv_all_link=[]
# issue_link=[]
new_link=[]


with open(new_csv, 'w') as csvfile: 
    # creating a csv writer object 
    csvwriter = csv.writer(csvfile) 
        
    # writing the fields 
    csvwriter.writerow(["Source Url"]) 
    
        
    # writing the data rows 
    # csvwriter.writerows(rows)
    
for i in maincsv["Source Url"]:
    imgName = i.split("/")[-1]
    # if not os.path.exists(os.path.join(rally_issue,imgName)) :
    if os.path.exists(os.path.join(rally,imgName)):

        with open(new_csv, 'a') as csvfile: 
            # creating a csv writer object 
            csvwriter = csv.writer(csvfile) 
            
            # writing the fields 
            # csvwriter.writerow(fields) 
                
            # writing the data rows 
            csvwriter.writerows([[i]])
    # for j in os.listdir(rally_issue):
    #     compl_rally_name=start_name+j
    #     print(compl_rally_name)
    # if i != compl_rally_name:
    #     new_link.append(i)
    #     print(len(new_link))

# for i in csv["Source Url"]:
#     for j in os.listdir(rally_issue):
#         compl_rally_name=start_name+j
#         print(compl_rally_name)
#     if i != compl_rally_name:
#         new_link.append(i)
#         print(len(new_link))



        # print(compl_rally_name)
        # issue_link.append(compl_rally_name)

    #     issue_link.append(j)

        
    #     csv_all_link.append(i)
        
    # print(issue_link)
