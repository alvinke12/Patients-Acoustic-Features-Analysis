import csv
import datetime
import os.path

def extract_sleep_episodes(file1):
    day_data=[]
    for line in csv.reader(file1):
        sleep_day = line[0][:10]
        day_session_data=[]
    #some file has no data, so need to jduge     
        if line[2]!='0':
    #total sleep time for one participant per day is given
            sleep_total_hrs = line[2]
    #split sleep episodes to count 
            newline = line[3].replace("[", "").replace("]", "").replace("'", "").split(", ")
    #divide 3 because for each episode contains duration, start time and end time
            cnt_sleep_episodes = len(newline)/3
    #find longest sleep episode and extract datetime
            sleep_length=[]
            sleep_start=[]
            sleep_end=[]
            for i in range(1,len(newline)+1):
                if i%3 == 1:
                    sleep_length.append(float(newline[i-1])-1)
                elif i%3 == 2:
                    date_time1 = datetime.datetime.strptime(newline[i-1],'%Y-%m-%d %H:%M:%S')
                    sleep_start.append(date_time1)
                elif i%3 == 0:    
                    date_time2 = datetime.datetime.strptime(newline[i-1],'%Y-%m-%d %H:%M:%S')
                    sleep_end.append(date_time2)

            longest_sleep_mins = max(sleep_length)

    #find onset and offset
            onset_offset=[]
            for i in range(0,len(sleep_start)):
                diff = (sleep_end[i] - sleep_start[i]).total_seconds()/60
                #find all episodes longer than 20mins 
                if diff >= 20:
                    episodes_20=[sleep_start[i],sleep_end[i]]
                    onset_offset.append(episodes_20)
                else:
                    continue
                
            #judge if no episode is greater than 20mins
            if len(onset_offset)>0:
                onset=onset_offset[0][0]
                offset=onset_offset[-1][1]
            else:
                onset='NA'
                offset='NA'
                
        else:
            sleep_total_hrs='NA'
            cnt_sleep_episodes='NA'
            longest_sleep_mins='NA'
            onset='NA'
            offset='NA'

            
        day_session_data.append(sleep_total_hrs)
        day_session_data.append(cnt_sleep_episodes)
        day_session_data.append(longest_sleep_mins)
        day_session_data.append(sleep_day)
        day_session_data.append(onset)
        day_session_data.append(offset)

        day_data.append(day_session_data)

    #data stored in nested list    
    return day_data

     
def write_results(subject,p_id,data_source,to_path):
    #write features into csv file   
    with open(to_path, mode='w', newline='') as my_csv:
        writer=csv.writer(my_csv)
        writer.writerow(["P_Id","Session_Day","Subject","Total_Sleep_Hour","Count_Sleep_Episodes",
                         "Longest_Sleep_Episode_mins","Onset","Offset"])
        for i in subject:
            for j in p_id:
                #check if file exists
                if os.path.exists(data_source+"\P"+str(j)+"_output_"+i+'.txt')==True:
                    #check if file empty
                    if os.stat(data_source+"\P"+str(j)+"_output_"+i+'.txt').st_size != 0:
                        #call extract_sleep_episodes function
                        file1 = open(data_source+"\P"+str(j)+"_output_"+i+'.txt',"r+")
                        data = extract_sleep_episodes(file1)
                        #write row of csv
                        for element in data:
                            print("For ",i," with id ",j," on",element[3],", the total sleep hour is:",
                              element[0],'; count of sleep episodes is: ', element[1],"; longest sleep time is:",
                              element[2], " minutes; onset is:", element[4]," and offset is:", element[5])
                            writer.writerow([j,element[3],i,element[0],element[1],element[2],element[4],element[5]])
                    else:
                        continue
                else:
                    continue
                
#specify the following:
#the data source                
data_source = r"C:\Users\Alvin\Desktop\UT\fall2019\research project\sleep features"
#the subject you want to extract features 
subject=['mother','baby']
#the start and end+1 id number of text files 
p_id=[]
for i in range(7,66):
    p_id.append(i)
#the path csv is saved to
to_path=r"C:\Users\Alvin\Desktop\UT\fall2019\research project\sleep_mother_baby.csv"

write_results(subject,p_id,data_source,to_path)



