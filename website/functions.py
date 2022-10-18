
def schedule(time):
    t=60*time
    h=0
    m=0
    timeSchedule=['0 : 0 AM']
    while h<23:
        if t>=60:
            min=t%60
            h+=(t-min)/60
            if m<60:
                m+=min
            else:
                h+=(m-(m-60))/60
                m=(m%60)
            
            if h<=12:
                if m==60:
                    h+=1
                    m=0
                timeSchedule.append(str(int(h))+' : '+str(m)+' AM');    
            else:
                if m==60:
                    h+=1
                    m=0
                timeSchedule.append(str(int(h%12))+' : '+str(int(m))+' PM')
        else:
            m+=t
    return timeSchedule

def court(r):
    court=[]
    for x in range(1,r):
        court.append("Court "+str(x))
    return court