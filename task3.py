from collections import Counter
import math

# THIS FUNCTION SPLITS EACH REFERENCE SENTENCE AND MACHINE TRANSLATION(MT)
def splitting(reference_list):
    refer_arr=[]
    for sentence in reference_list:
        sentence=sentence.lower()
        refer_arr.append(sentence.split())
    return refer_arr

# THIS FUNCTION TAKES THE SPLITTED SENTENCES AND CREATES 2 LIST 1 OF REFERNCE AND 1 OF MT
# AND IT STORES THE UNI,BI,TRI AND 4-GRAM SPLITTING IN FORM OF LIST IN 
# CANDIDATE (FOR MT)
# REFERENCE_LIST_FINAL (FOR SPLITTED REFERENCE SENTENCES)
# Then I made 2 counter of n-GRAM SPLITTING 1 OF REFERNCE AND 1 OF MT 

def Splitting_in_n_grams(splitted_reference_sentence,MT,n):
    candidate=[]
    temp_list=[]
    reference_list_final=[]
    MT=MT.lower()
    MT=MT.split()

    for i in range(1,n+1):
        for index in range(len(MT)):
            if index+i<=len(MT):
                temp= ' '.join(MT[index : index+i])
                temp_list.append(temp)
        candidate.append(temp_list)
        temp_list=[]

        for j in range(len(splitted_reference_sentence)):
            for word_index in range(len(splitted_reference_sentence[j])):
                if word_index+i<=len(splitted_reference_sentence[j]):
                    temp=' '.join(splitted_reference_sentence[j][word_index : word_index+i])
                    temp_list.append(temp)
            reference_list_final.append(temp_list)
            temp_list=[]

    counter1=[]
    counter2=[]
    for each in candidate:
        counter1.append(Counter(each))
    for each in reference_list_final:
        counter2.append(Counter(each))

    # print(counter1) 
    # print(counter2)
    
    return candidate,reference_list_final,counter1,counter2


def Bleu_Score(reference_list,MT,n=4):
    count_in_MT=0
    max_count_in_ref=0
    clipped_count=0
    probability=0
    Bleu_Score=0

    splitted_sentence = splitting(reference_list)
    candidate,reference_list_final,counter1,counter2 = Splitting_in_n_grams(splitted_sentence,MT,4)

    # here i ran for loop four times for all 4 grams
    # in  loop it takes 
    # uni-gram of counter of MT for 1 st loop 
    # bi-gram  for 2nd
    # and so on
    # then it loops over all elements in respective spllited n-gram
    # value of max_count_in_ref is obtained with the help of counter
    # for each if it finds same element in reference split it notes its frequency with the help of counter
    # and clipped_count is calculated by adding "min(temp,max_count_in_ref)" to previous value 
    # if clipped_count is ==0 then function returns the value of bleu score as 0
    # else log(probabilty) of nth-gram is added to existing

    for i in range(1,n+1):
        for each_mt in counter1[i-1]:
            temp = counter1[i-1][each_mt]
            count_in_MT += counter1[i-1][each_mt]
            max_count_in_ref=0
            for j in range(len(counter2)):
                for any_word in counter2[j]:
                    if each_mt==any_word:
                        max_count_in_ref = max(counter2[j][any_word],max_count_in_ref)
                        break
            
            clipped_count+=min(temp,max_count_in_ref)

        P=clipped_count/count_in_MT

        if clipped_count==0:
            return 0
        else:
            probability += math.log(P)

        clipped_count=0
        count_in_MT=0
    
        
    r=0
    temp=0
    # this for loop is used to find maximum length of reference line  which is =r 
    for i in range(len(counter2)):
        for each in counter2[i]:
            temp+=counter2[i][each]
        if r<temp:
            r=temp
        temp=0

    c=0
    # this is used to find length of MT line
    for each in counter1[0]:
        c+=counter1[0][each]

    if c>r:
        BP=1
    else:
        BP=math.exp(1-r/c)
    
    w=1/n
    w=w*probability
    w=math.exp(w)

    BLEU=   BP*w
    return BLEU

reference_list = ["It is the practical guide for the army always to heed the directions of the party",
                  "It is the guiding principle which guarantees the military forces always being under the command of the Party",
                  "It is a guide to action that ensures that the military will forever heed Party commands"]

MT1=" It is a guide to action which ensures that the military always obeys the commands of the party"
MT2="It is the to action the troops forever hearing the activity guidebook that party direct"

answer= Bleu_Score(reference_list,MT1,4)
print("BLEU SCORE = ",answer)