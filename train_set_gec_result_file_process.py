import os
import re

import json
from openpyxl import load_workbook
import nltk
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.python.estimator.estimator import Estimator
import yaml
from spacy.lang.en.stop_words import STOP_WORDS
import spacy
import random
import collections


# 处理gec数据，生成josn文件

spacynlp = spacy.load("en_core_web_sm")

def sentence_tokenize(documents):
    """分句函数，将一整段文本进行分句

    Args:
        documents: 待分句的document, string类型

    Returns: 句子组成的list

    """
    # 查看
    locations = [-1]
    locations.extend([item.start() for item in re.finditer(r'[\.\?\!](?=[^ \W\d])', documents)])
    locations.append(len(documents))
    sentences = [documents[locations[i] + 1:locations[i + 1] + 1] for i in range(len(locations) - 1)]
    pre_split_documents = " ".join(sentences)

    sentences = nltk.sent_tokenize(pre_split_documents)
    # print(sentences)
    # for line in sentences:
    #     print(line)
    
    # print(len(sentences))
    # return len(sentences)
    return sentences

# 统计段落数量
def count_para_num(document):
    document = re.sub(r'\s{2,}','\t',document)
    para_list = document.split("\t")
    # for idx, line in enumerate(para_list):
    #     print(idx,line)
    return len(para_list)


with open("config/sys_conf.yaml", encoding="utf-8") as conf_reader:
    sys_conf = yaml.load(conf_reader.read())
    print("加载完成")

# 统计
def define_json():

    # gec_result_json = {}

    asap_csv_file_path = os.path.join(sys_conf["data_dir"], "training_set_rel3.tsv")
    if not os.path.exists(asap_csv_file_path):
        raise ValueError("asap_file_path is invalid.")
    asap_dataset = pd.read_csv(asap_csv_file_path,sep='\t',encoding='iso-8859-15')
    # print(asap_dataset)
    articles_id = list(asap_dataset["essay_id"])
    # print(articles_id)
    articles_set = list(asap_dataset["essay_set"])
    # print(articles_set)
    # print(asap_dataset["essay"])

    articles_eassy = list(asap_dataset["essay"])
    # print(articles_eassy)
    domain1_score = asap_dataset["domain1_score"]
    handmark_scores = dict(zip(articles_id, articles_eassy))
    # print(handmark_scores)
    # print(handmark_scores[key].strip())
    gec_str = ""
    for key,value in handmark_scores.items():
        # print(str(key)+"=="+str(value))
        para_num = count_para_num(value)
        sent_num = len(sentence_tokenize(value))
        sent_list = sentence_tokenize(value)


        


        # gec_result_json = {}
        gec_result_json = collections.OrderedDict()
        gec_result_json['title']=""
        gec_result_json["sent_nums"] = sent_num
        gec_result_json["para_nums"] = para_num
        
        for sent_index in range(int(sent_num)):
            # sentence_josn = {}
            sentence_josn = collections.OrderedDict()
            sentence_josn["orig_sent"] = sent_list[sent_index]
            sentence_josn["sent_type"] = 1
            sentence_josn["err_num"] = random.randint(0,4)

            # edit_json = {}
            edit_json = collections.OrderedDict()
            edit_json["err_type"] = [1,2]
            edit_json["corr_str"] = ""
            edit_json["start_err"] = ""

            for edit_index in range(int(sentence_josn["err_num"])): 
                sentence_josn["edit_"+str(edit_index)] = edit_json
                print("edit_"+str(edit_index))
                print("__________________")
            gec_result_json["sentence_"+str(sent_index)] = sentence_josn


        json_result_str = json.dumps(gec_result_json)
        gec_str += str(key)+"  "+json_result_str+"\n"

    with open("./gec_result.txt","w",encoding="utf-8") as wf:
        wf.write(gec_str)

    print("存取成功")


            




            
                
            


if __name__ == "__main__":
    # sentence_tokenize("I dont think we should not take books, Music, Movies, and Magazines off the shelf gets because we think they are offensive to us. If you think somthing is offensive dont get it I know I would not get somthing that I think is offensive to me.     Their lot's of books in the world that i dont like. One of them is @CAPS1 Books I hate them with all of my heart. The next kind of books that I think is offensive is @CAPS2 Books because their are lots of story that are in their that we dont read. So I think that it is a wast of paper. The last kind of books I think is offensive is @CAPS3 Books because they are hard to read them in @CAPS3.     Their are lot's of music out there I dont like. One of them is @CAPS5. I dont know why I dislike @CAPS5 but I do. The next type @CAPS6- @CAPS7. The singer in todays @CAPS6- @CAPS7 I think are no good. The last type of music is some of todays rap. I think some of todays rap uses to much bad words.     Their are lot's of movies out their I dont like. The first one is @CAPS10 @CAPS11. I did not get the hole plut of that movie. The next one @CAPS12 of the corn. Their was no way I could find out way the @CAPS12 was killing the people over @NUM1 in that town. The last movie that I did not like was ALL the @CAPS13 movies. I just did not like them ok?     I think all of these things are offensive. But I still know that people like them so I would not take them away. There are thing people like but I dont like them. Their things that my friend like but I dont like. Their thing I like and they dont like. But I guess what I am trying to say is in life there are going to be things that you dont like. But you cant get rid of the things you dislike in the world")
    # count_para_num("I dont think we should not take books, Music, Movies, and Magazines off the shelf gets because we think they are offensive to us. If you think somthing is offensive dont get it I know I would not get somthing that I think is offensive to me.     Their lot's of books in the world that i dont like. One of them is @CAPS1 Books I hate them with all of my heart. The next kind of books that I think is offensive is @CAPS2 Books because their are lots of story that are in their that we dont read. So I think that it is a wast of paper. The last kind of books I think is offensive is @CAPS3 Books because they are hard to read them in @CAPS3.     Their are lot's of music out there I dont like. One of them is @CAPS5. I dont know why I dislike @CAPS5 but I do. The next type @CAPS6- @CAPS7. The singer in todays @CAPS6- @CAPS7 I think are no good. The last type of music is some of todays rap. I think some of todays rap uses to much bad words.     Their are lot's of movies out their I dont like. The first one is @CAPS10 @CAPS11. I did not get the hole plut of that movie. The next one @CAPS12 of the corn. Their was no way I could find out way the @CAPS12 was killing the people over @NUM1 in that town. The last movie that I did not like was ALL the @CAPS13 movies. I just did not like them ok?     I think all of these things are offensive. But I still know that people like them so I would not take them away. There are thing people like but I dont like them. Their things that my friend like but I dont like. Their thing I like and they dont like. But I guess what I am trying to say is in life there are going to be things that you dont like. But you cant get rid of the things you dislike in the world")
    # sentence = "Our founding fathers creating amendments for the people.  One of the greatest is the freedom of speech.  Censorship of offessive materials is unnecessary.  Books, music, movies, and magazines @MONTH1 have bad messages or nudity, but that does not give anyone the right to get rid of them.  Book burning happened because of the dislike of people's writing.  People have the right to say how they feel by any medium.  Censorship of anything makes a child more immature.     Book burning is a horrible action by any person.  People used to burn them because of all the sex, drugs, and violence, but doing this destroys people's dreams, theories, and ideas.  In the book @CAPS1 @NUM1, firemen would burn any book seen within a home.  Almost ever single book in the world is not factual, unless it is nonfiction.  The firemen in the novel destroyed any bits of type because it was false and went against the government.  That basically means every kind of book out there.  The causation of such a tragedy was that every citizen befriended their television or video games.  Without books there would be no real sort of entertainment.  Also, the things we read everyday are what make us who we are so there, in fact, should not be less books but more.     Libraries have no right to censor books.  Freedom of speech has been around almost since the beginning of this nation.  Why should it change now?  Stopping obscene literature from being in the reach of the people is stopping writers from speaking out.  They @MONTH1 have already written their ideas, but if nobody reads their work then there is no way that they'll be heard.  Libraries are not there to stop things from reaching little kids' ears but to provide any knowledge a man needs.     Parents have always stopped their precious babies from watching certain shows and movies.  I once knew a woman who would never allow her son to watch the @PERSON1 series because of the use of sorcery.  She believed that he would try to learn witchcraft.  I found that quite ridiculous when I heard about it.  When a kid watches murder mysteries, fantasy shows, or dramas with bits of nudity, it is different to them and they are curious.  After watching these kind of scenes, a parent needs to sit down with their child and talk about what they jus saw.  The child needs to know that killing is wrong and justice is good and magic and dragons don't exist.  Nudity has always been considered a bad thing but penises and boobs are part of the human body.  Kids will be more mature about it the more they see it, but that doesn't the child should watch porn.     Censory has always been taken the wrong way.  People believe if that the offensive material is shown then the watcher or reader will have bad thoughts about what they learned about.  We should not get rid of the obscenity at all.  We should have an understanding of the bad things in life.  Burning books is a bad way to destroy the foundations of the human mind.  Freedom of speech is a law and should be followed.  Censorship is not always a good thing for children or anyone for that matter"
    sentence = "Dear local newspaper, I think effects computers have on people are great learning skills/affects because they give us time to chat with friends/new people, helps us learn about the globe(astronomy) and keeps us out of troble! Thing about! Dont you think so? How would you feel if your teenager is always on the phone with friends! Do you ever time to chat with your friends or buisness partner about things. Well now - there's a new way to chat the computer, theirs plenty of sites on the internet to do so: @ORGANIZATION1, @ORGANIZATION2, @CAPS1, facebook, myspace ect. Just think now while your setting up meeting with your boss on the computer, your teenager is having fun on the phone not rushing to get off cause you want to use it. How did you learn about other countrys/states outside of yours? Well I have by computer/internet, it's a new way to learn about what going on in our time! You might think your child spends a lot of time on the computer, but ask them so question about the economy, sea floor spreading or even about the @DATE1's you'll be surprise at how much he/she knows. Believe it or not the computer is much interesting then in class all day reading out of books. If your child is home on your computer or at a local library, it's better than being out with friends being fresh, or being perpressured to doing something they know isnt right. You might not know where your child is, @CAPS2 forbidde in a hospital bed because of a drive-by. Rather than your child on the computer learning, chatting or just playing games, safe and sound in your home or community place. Now I hope you have reached a point to understand and agree with me, because computers can have great effects on you or child because it gives us time to chat with friends/new people, helps us learn about the globe and believe or not keeps us out of troble. Thank you for listening."
    sentence_num = sentence_tokenize(sentence)
    para_num = count_para_num(sentence)
    # print(sentence_num)
    # print(para_num)

    define_json()
    # with open('./gec_result.txt','r',encoding="utf-8") as rf:
    #     for line in rf:
    #         print(line)
    #         print("____________________________________________")
        