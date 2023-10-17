import pickle
import math
import numpy as np
import tensorflow as tf
from tensorflow import keras
import argparse
import os

# Import any other necessary libraries

class BanglaSpellChecker:
    def __init__(self, model_path,tokenizer_path,dict_Of_index_Top_Words_path):
        self.model = keras.models.load_model(model_path)
        self.Tokenizer_sen = None  # Load your tokenizer here
        with open(tokenizer_path, 'rb') as handle:
            self.Tokenizer_sen = pickle.load(handle)
        with open(dict_Of_index_Top_Words_path, 'rb') as handle:
            self.dict_Of_index_Top_Words = pickle.load(handle)


    def padding_word(self, dem, length=10):
        dem = dem.strip()
        word = [self.Tokenizer_sen.word_index.get('#')]
        for y in dem:
            value_check = self.Tokenizer_sen.word_index.get(y)
            if value_check is None:
                value_check = len(self.Tokenizer_sen.word_index) + 1
            word.append(value_check)
        word.append(self.Tokenizer_sen.word_index.get('$'))
        flag = 0
        out = []
        if len(word) < 12:
            word_len = len(word)
            dif = 12 - word_len
            flag = 1
            for c in range(0, math.ceil(dif / 2)):
                out.append(0)
            for c in word:
                out.append(c)
            for c in range(0, math.floor(dif / 2)):
                out.append(0)

        if len(word) >= 12 and flag == 0:
            out = word[0:12]
            out[11] = self.Tokenizer_sen.word_index.get('$')
        return out

    def padding_sentence(self, dem):
        c = 0
        if len(dem) < 15:
            x = len(dem)
            pad_sen = []
            dif = 15 - x
            for i in range(0, dif):
                c = c + 1
                pad_sen.append([float(0.0)] * 12)
            for i in dem:
                pad_sen.append(i)
        else:
            pad_sen = dem[0:15]
        pad_sen = np.array(pad_sen)
        return pad_sen, c

    def x_y_generator_model(self, one_sentence):
        words = []
        input_data = []
        for i in one_sentence:
            if i[1] == 1:
                words.append(i[0])
        if len(words) > 15:
            words = words[len(words) - 15:]
        for i in range(len(words)):
            x = words[i]
            for k in x:
                if k == "০" or k == "১" or k == "২" or k == "৩" or k == "৪" or k == "৫" or k == "৬" or k == "৭" or k == "৮" or k == "৯":
                    x = "1111111111"
                    break
            input_data.append(self.padding_word(x, 10))
        input_data, _ = self.padding_sentence(input_data)
        return input_data, words

    def sentence_correction(self, text):
        inputs, without_ending = self.split_ending(text)
        corrected_text = ""
        for i in inputs:
            if len(i) > 2:
                x, words = self.x_y_generator_model(i)
                c = []
                c.append(x)
                x = np.array(c)
                yy = self.model.predict([x])
                yy = np.array(yy)
                check = yy[1][0]
                check = np.array(check)
                result = []
                for k in check:
                    max_value = -1
                    index = -1
                    o = np.array(k)
                    for j in range(len(self.dict_Of_index_Top_Words)):
                        if o[j] > max_value:
                            index = j
                            max_value = o[j]
                    result.append(index)
                index_count = 0
                final_res = []
                for k in result:
                    p = self.dict_Of_index_Top_Words[k]
                    if p != "PAD" and p != "UNK" and p != "1111111111":
                        #index_count = index_count + 1
                        final_res.append(p)
                    if p == "UNK" or p == "1111111111":
                        final_res.append(words[index_count])
                        index_count = index_count + 1
                final_res.reverse()
                xx = i.copy()
                xx.reverse()
                index_check = 0
                for j in xx:
                    if j[1] == 1 and index_check < len(final_res):
                        j[0] = final_res[index_check]
                        index_check = index_check + 1
                xx.reverse()
                for j in xx:
                    if j[0] == "।" or j[0] == "?" or j[0] == "!":
                        corrected_text = corrected_text + j[0]
                    else:
                        corrected_text = corrected_text + " " + j[0]
            else:
                for j in i:
                    corrected_text = corrected_text + " " + j[0]
        for i in without_ending:
            corrected_text = corrected_text + " " + i[0]
        corrected_text = corrected_text.strip()
        corrected_text = corrected_text.replace("<new_line>", "\n")
        return corrected_text

    def split_ending(self,str):
      sentence=""
      for i in str:
        if i =="।" or i=="!" or i=="?" :
          sentence=sentence+" "+i
        elif i=="\n":
          sentence=sentence+" <new_line> "+i
        elif i=='"':
          sentence=sentence+" "+i+" "
        else:
          sentence=sentence+i
      sentence=sentence.split()
      all=[]
      for i in sentence:
        one_bad=0
        temp=""
        for j in i:
          if self.Tokenizer_sen.word_index.get(j)==None :
            one_bad=one_bad+1
            temp=temp+" "+j+" "
          else:
            temp=temp+j
        if one_bad==1 and i=="<new_line>":
          temp=temp.split()
          all=all+temp
        else:
          all=all+[i]
      final=[]
      for j in all:
        bad_char=0
        for i in j:  
          if self.Tokenizer_sen.word_index.get(i) == None and i not in {'০','১','২','৩','৪','৫','৬','৭','৮','৯'} :
            bad_char=bad_char+1

        if bad_char==len(j):
          final.append([j,0])
        else:
          final.append([j,1])
      input_list=[]
      temp=[]
      for i in final: 
        x=i[0]   
        if  x=="।" or x=="!" or x=="?":
          temp.append(i)
          input_list.append(temp)
          temp=[]
        else:
          temp.append(i)
      return input_list,temp
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Bangla Spell Checker")
    parser.add_argument("input_file", help="Input file with error-prone Bengali text")
    parser.add_argument("output_file", help="Output file for corrected text")
    parser.add_argument("tokenizer_path", help="Path of tokenizer")
    parser.add_argument("dict_Of_index_Top_Words_path", help="Path of dict_Of_index_Top_Words")
    parser.add_argument("model_path", help="Path to the saved model")

    args = parser.parse_args()

    spell_checker = BanglaSpellChecker(args.model_path, args.tokenizer_path,
                                       args.dict_Of_index_Top_Words_path)

    with open(args.input_file, 'r', encoding='utf-8') as f:
        input_text = f.read()

    corrected_text = spell_checker.sentence_correction(input_text)

    with open(args.output_file, 'w', encoding='utf-8') as f:
        f.write(corrected_text)

    print(f"Spell checking complete. Corrected text saved to {args.output_file}")
