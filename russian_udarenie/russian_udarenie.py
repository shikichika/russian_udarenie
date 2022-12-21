import pickle

from natasha import (
    Segmenter,
    NewsEmbedding,
    NewsMorphTagger,
    Doc
)

with open (file="wordforms.dat", mode='rb') as f:
        wordforms = pickle.loads(f.read())




def udarenie(text):

    doc = Doc(text)

    segmenter = Segmenter()
    emb = NewsEmbedding()
    morph_tagger = NewsMorphTagger(emb)


    words_dict = {}

    doc.segment(segmenter)
    doc.tag_morph(morph_tagger)

    for i in range(len(doc.tokens)):

        #featがない場合
        if not doc.tokens[i].feats:
            if doc.tokens[i].text.istitle():
                words_dict[doc.tokens[i].text] = ['', 1]
            else:
                words_dict[doc.tokens[i].text] = ['', 0]
        #featがある場合
        else:

            #Numがある場合
            try:
                #大文字から始まる
                if doc.tokens[i].text.istitle():
                    words_dict[doc.tokens[i].text] = [doc.tokens[i].feats["Number"].lower(), 1]
                #小文字から始まる
                else:
                    words_dict[doc.tokens[i].text] = [doc.tokens[i].feats["Number"].lower(), 0]
            except:
                #大文字から始まる
                if doc.tokens[i].text.istitle():
                    words_dict[doc.tokens[i].text] = ['', 1]
                #小文字から始まる
                else:
                    words_dict[doc.tokens[i].text] = ['', 0]
                

    accent_text = ""

    if text == 'Напишите слова' or text == 'Напиши слова':
        accent_text = "Напиши́те слова́"
    else:
        for word in words_dict.keys():

            try:
            
                try:
                    # wordsformのアクセントの位置が一つの場合
                    if len(wordforms[word]) == 1 : 
                        accent_text += wordforms[word][0]["accentuated"]
                        accent_text += " "
                    # wordsformのアクセントの位置が２つ以上の場合
                    else:
                        for i in range(len(wordforms[word])):
                            if word == 'это':
                                accent_text += 'э́то'
                                accent_text += " "
                                break
                            if word == 'замок':
                                accent_text += 'замо́к/за́мок'
                                accent_text += " "
                                break
                            
                            if words_dict[word][0] in wordforms[word][i]["form"]:
                                accent_text += wordforms[word][i]["accentuated"]
                                accent_text += " "
                                break
                            else:
                                continue
                #wordが小文字でないとwordsformで見つからない場合
                except:
                    # wordsformのアクセントの位置が一つの場合
                    if len(wordforms[word.lower()]) == 1 :
                        #元々wordが大文字始まりだった場合
                        if words_dict[word][1] == 1:
                            accent_text += wordforms[word.lower()][0]["accentuated"].capitalize()
                            accent_text += " "
                        else:
                            accent_text += wordforms[word.lower()][0]["accentuated"]
                            accent_text += " "

                    # wordsformのアクセントの位置が２つ以上の場合
                    else:
                        for i in range(len(wordforms[word.lower()])):
                            if word == 'Это':
                                accent_text += 'Э́то'
                                accent_text += " "
                                break
                            if word == 'Замок':
                                accent_text += 'Замо́к/За́мок'
                                accent_text += " "
                                break
                            if words_dict[word][0] in wordforms[word.lower()][i]["form"]:
                                if words_dict[word][1] == 1:
                                    accent_text += wordforms[word.lower()][i]["accentuated"].capitalize()
                                    accent_text += " " 
                                    break
                                else:
                                    accent_text += wordforms[word.lower()][i]["accentuated"]
                                    accent_text += " " 
                                    break
                            else:
                                continue     
                                
            except:
                accent_text += word
                accent_text += " "
    
    return accent_text


