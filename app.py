#!/usr/bin/env python
# coding: utf-8

# ## 알파벳으로 한글 쓰기 
# 

# In[32]:


import itertools 
import pandas as pd
import streamlit as st
import webbrowser

def onset(char):
    code = ord(char)
    if 0xac00 <= code <= 0xd7b0:
        return (code - 0xac00) // 588
    return -1


def nucleus(char):
    code = ord(char)
    if 0xac00 <= code <= 0xd7b0:
        x = (code - 0xac00) % 588
        return x // 28
    return -1


def coda(char):
    code = ord(char)
    if 0xac00 <= code <= 0xd7b0:
        return (code - 0xac00) % 28
    return -1


def compose(onset, nucleus, coda):
    return chr(0xac00 + onset * 588 + nucleus * 28 + coda)

onsets=["ㄱ","ㄲ","ㄴ","ㄷ","ㄸ","ㄹ","ㅁ","ㅂ","ㅃ","ㅅ","ㅆ","ㅇ","ㅈ","ㅉ","ㅊ","ㅋ","ㅌ","ㅍ","ㅎ"] # 19개
nuclei=["ㅏ","ㅐ","ㅑ","ㅒ","ㅓ","ㅔ","ㅕ","ㅖ","ㅗ","ㅘ","ㅙ","ㅚ","ㅛ","ㅜ","ㅝ","ㅞ","ㅟ","ㅠ","ㅡ","ㅢ","ㅣ"] # 21개
codas=["","ㄱ","ㄲ","ㄳ","ㄴ","ㄵ","ㄶ","ㄷ","ㄹ","ㄺ","ㄻ","ㄼ","ㄽ","ㄾ","ㄿ","ㅀ","ㅁ","ㅂ","ㅄ","ㅅ","ㅆ","ㅇ","ㅈ","ㅊ","ㅋ","ㅌ","ㅍ","ㅎ"]  # 28개


# In[31]:


# 'key' : [[있는 그대로의 형태], [왼쪽으로 90도 회전한 형태], [오른쪽으로 90도 회전한 형태], [180도 회전한 형태]]
onset_dict = {
'ㄱ': [['7'], ['r'], ['_l'], ['L']],
'ㄲ': [['77'], ['F'], [], []],
'ㄴ': [['L', 'l_'], ['J', 'v', 'V', 'j', '_l'], ['r'], ['7']],
'ㄷ': [['C', 'c', '<'], ['u', 'U'], ['n'], []],
'ㄸ': [['CC', 'cc', '<<'], [], ['fl', 'Fl'], ['>>']],
'ㄹ': [['2', 'z'], ['N', 'W', 'w', 'ru'], ['ru'], ['z', 'Z']],
'ㅁ': [['17', '12', 'D'], ['D'], ['D'], ['D']],
'ㅂ' : [['ld'], [], [], ['fl', 'Fl']],
'ㅃ': [['ldld'], [], [], []],
'ㅅ': [['^', 'x'], ['<', 'c', 'x','X', 'T'], ['>', 'T', '7'], ['v',' V', 'y', 'x']],
'ㅆ': [['^^', 'xx'], [], [], ['vv', 'VV', 'yy', 'xx']],
'ㅇ': [['0', 'o', 'O'], ['0', 'o', 'O'], ['0', 'o', 'O'], ['0', 'o', 'O']],
'ㅈ' : [['z', 'Z'], ['K', 'k'], [], []],
'ㅉ': [['zz', 'ZZ'], [], [], []],
'ㅊ': [[], ['lk', 'lK'], [], []],
'ㅋ': [[], ['lr'], ['_ll'], []],
'ㅌ': [['E'], [], ['rn'], ['3']],
'ㅍ': [[], ['lxl'], ['lxl'], []],
'ㅎ': [['6'], ['lb', 'lp', 'lo', '1o', '|o', 'llo'], ['ql', 'or', 'dl', 'ol', 'o1', 'o|', 'oll'], ['e', 'g']] }

nucleus_dict = {
'ㅏ': [['r', 'l-'], [], [], ['-l']],
'ㅐ': [['H', 'rl', 'h'], [], [], ['rl', 'H']],
'ㅑ': [['f', 'F'], [], [], ['xl', 'Xl', 'zl', 'Zl' ]],
'ㅒ': [['lxl', 'kl', 'tl', 'fl'], [], [], ['lxl', 'kl', 'tl', 'fl']],
'ㅓ': [['-l'], [], [], ['r', 'L']],
'ㅔ': [['7l'], [], [], ['lr', 'lL']],
'ㅕ': [['xl', 'Xl', 'zl', 'Zl'], [], [], ['f', 'k']],
'ㅖ': [['xl'], [], [], ['lk', 'lf', 'lt']],
'ㅗ' : [[], ['J', '-l'], ['r'], []],
'ㅘ': [['Lr'], [], [], []],
'ㅙ': [['LH'], [], [], ['HT']],
'ㅚ': [['Ll'], [], [], ['lT']],
'ㅛ': [[], ['zl', 'Zl', '3l'], ['k', 'K', 'f', 'F'], []],
'ㅜ': [[], ['r',  'l-'], ['y', '-l'], []],
'ㅝ': [[], ['rT'], [], []],
'ㅞ': [[], [], [], []],
'ㅟ': [['7l'], [], [], []],
'ㅠ': [[], ['F', 'f', 'k', 'K'], ['zl', 'Zl', '3l'], []],
'ㅡ' : [['-'], ['l', '1', '|'], ['l', '1', '|'], ['-']],
'ㅣ' : [['l', '1', '|'], ['-'], ['_',], ['l', '1', '|']],
'ㅢ': [['-l'], ['T'], ['L'], ['l-']] }


coda_dict = {
'ㄱ': [['7'], ['r'], ['_l'], ['L']],
'ㄲ': [['77'], ['F'], [], []],
'ㄳ': [[], [], [], []],
'ㄴ': [['L', 'l_'], ['J', 'v', 'V', 'j', '_l'], ['r'], ['7']],
'ㄵ': [[], [], [], []],
'ㄶ': [[], [], [], []],
'ㄷ': [['C', 'c', '<'], ['u', 'U'], ['n'], []],
'ㄹ': [['2', 'z'], ['N', 'W', 'w', 'ru'], ['ru'], ['z', 'Z']],
'ㄺ': [['27', 'z7'], [], [], ['LZ', 'Lz']],
'ㄻ': [['212', '2D'], [], [], ['Dz', 'DZ']],
'ㄼ': [['2ld', 'zld'], [], [], ['flz', 'FlZ']],
'ㄽ': [['zx', '2X'], [], [], ['vz', 'VZ', 'yz', 'xz']],
'ㄾ': [['zE', 'ZE', '2E'], [], [], ['3z', '3Z']],
'ㄿ': [[], [], [], []],
'ㅀ': [['z6'], [], [], ['ez', 'gz']],
'ㅁ': [['17', '12', 'D'], ['D'], ['D'], ['D']],
'ㅂ': [['ld'], [], [], ['fl', 'Fl']],
'ㅄ': [['ldx'], [], [], ['vfl', 'VFl']],
'ㅅ': [['^', 'x'], ['<', 'c', 'x','X', 'T'], ['>', 'T', '7'], ['v',' V', 'y', 'x']],
'ㅆ': [['^^', 'xx'], [], [], ['vv', 'VV', 'yy', 'xx']],
'ㅇ': [['0', 'o', 'O'], ['0', 'o', 'O'], ['0', 'o', 'O'], ['0', 'o', 'O']],
'ㅈ': [['z', 'Z'], ['K', 'k'], [], []],
'ㅊ': [[], ['lk', 'lK'], [], []],
'ㅋ': [[], ['lr'], ['_ll'], []],
'ㅌ': [['E'], [], ['rn'], ['3']],
'ㅍ': [[], ['lxl'], ['lxl'], []],
'ㅎ': [['6'], ['lb', 'lp', 'lo', '1o', '|o', 'llo'], ['ql', 'or', 'dl', 'ol', 'o1', 'o|', 'oll'], ['e', 'g']] }


# In[33]:


# 음소(자,모음) 하나 -> 알파벳 상형 변환 
def phon_to_alphabet(phon):
    if phon in onset_dict.keys():
        # flatten list 
        return [item for sublist in onset_dict[phon] for item in sublist]
    elif phon in nucleus_dict.keys():
        return [item for sublist in nucleus_dict[phon] for item in sublist]
    else:
        return [item for sublist in coda_dict[phon] for item in sublist]


# In[35]:



# In[135]:


# 한 음절 -> 알파벳 상형 변환
def syl_to_alphabet(syl, explain=False):
    result = []
    explanation = []
    
    explain_dict = {0: '있는 그대로의 형태', 1:'왼쪽으로 90도 회전한 형태', 2:'오른쪽으로 90도 회전한 형태', 3:'180도 회전한 형태'}
        
    # 받침 없는 경우 
    if coda(syl) == 0:
        on = onsets[onset(syl)] 
        nu = nuclei[nucleus(syl)] 

        # i==0 : 초성, 중성 모두 있는 그대로의 형태로 표현 가능한 경우
        # i==1 : 초성, 중성 모두 왼쪽으로 90도 회전한 형태로 표현 가능한 경우
        # i==2 : 초성, 중성 모두 오른쪽으로 90도 회전한 형태로 표현 가능한 경우
        # i==3 : 초성, 중성 모두 180도 회전한 형태로 표현 가능한 경우
        for i in range(4):
            if onset_dict[on][i] != [] and nucleus_dict[nu][i] != [ ]:
                for x in range(len(onset_dict[on][i])):
                    for y in range(len(nucleus_dict[nu][i])):
                        if i in [0,1]:
                            result.append(onset_dict[on][i][x] + nucleus_dict[nu][i][y])
                            explanation.append(explain_dict[i])
                        # 오른쪽으로 90도 / 180도 회전한 경우 초성, 중성 순서 바뀌어야 함
                        else:
                            result.append(nucleus_dict[nu][i][y] + onset_dict[on][i][x])
                            explanation.append(explain_dict[i])

    # 받침 있는 경우    
    else:
        on = onsets[onset(syl)] 
        nu = nuclei[nucleus(syl)] 
        co = codas[coda(syl)]
        
        exception = [['ㅓ', 'ㅇ', 'a'], ['ㅣ', 'ㄴ', 'L'], ['ㅕ', 'ㅇ', 'zb'], ['ㅏ', 'ㅇ', '6'], ['ㅕ', 'ㄴ', '_t'],                     ['l', 'ㅁ', 'b'], ['ㅓ', 'ㄴ', 'z']]

        
        for exc in range(len(exception)):
            if nu == exception[exc][0] and co == exception[exc][1] and onset_dict[on][0] != []:
                for e in range(len(onset_dict[on][0])):
                    result.append(onset_dict[on][0][e] + exception[exc][2])
                    explanation.append(explain_dict[0])
        

        # i==0 : 초성, 중성 모두 있는 그대로의 형태로 표현 가능한 경우
        # i==1 : 초성, 중성 모두 왼쪽으로 90도 회전한 형태로 표현 가능한 경우
        # i==2 : 초성, 중성 모두 오른쪽으로 90도 회전한 형태로 표현 가능한 경우
        # 받침 있으면 180도 회전 불가 
        for i in range(3):
            if onset_dict[on][i] != [] and nucleus_dict[nu][i] != [ ] and coda_dict[co][i] != [ ]:
                for x in range(len(onset_dict[on][i])):
                    for y in range(len(nucleus_dict[nu][i])):
                        for z in range(len(coda_dict[co][i])):
                            if i != 2:
                                result.append(onset_dict[on][i][x] + nucleus_dict[nu][i][y] + coda_dict[co][i][z])
                                explanation.append(explain_dict[i])
                            # 오른쪽으로 90도 회전한 경우 초성, 종성, 종성 순서 바뀌어야 함 
                            else:
                                result.append(coda_dict[co][i][z] + nucleus_dict[nu][i][y] + onset_dict[on][i][x])
                                explanation.append(explain_dict[i])

    
    if explain:
        return pd.DataFrame(zip(result, explanation), columns=[syl, 'explanation'])
    
    else:
        return result




# In[137]:


def word_to_alphabet(word):
    syls = []
    for i in range(len(word)):
        df = syl_to_alphabet(word[i], explain=True)
        syls.append(df.iloc[:,0].tolist())
    
    result = []
    
    for i in map(''.join, list(itertools.product(*syls))):
        result.append(i)
    
    return result        




# In[155]:


st.title("알파벳으로 한글 쓰기 ^^-7l")

st.write('알파벳 및 특수문자로 한글의 모양을 본떠 표현합니다. 상형하기 힘든 일부 자모는 회전한 형태로 나타날 수 있습니다. 결과물이 이해되지 않으면 아래 대응표를 확인해주세요.')
st.write('[예시1] 아이디 → 0r0lCl')
st.write('[예시2] 우주 → 0rKr (왼쪽으로 90도 회전한 형태)')

user_input = st.text_input("변환하고 싶은 한글을 입력하세요: ")
st.write(word_to_alphabet(user_input))


with st.beta_expander("각 자모의 대응표 확인하기"):
    st.write('[초성 대응표]')
    st.write(pd.DataFrame.from_dict(onset_dict, orient='index',
                                    columns=['있는 그대로의 형태', '왼쪽으로 90도 회전한 형태', '오른쪽으로 90도 회전한 형태', '180도 회전한 형태']))

    st.write('[중성 대응표]')
    st.write(pd.DataFrame.from_dict(nucleus_dict, orient='index',
                                    columns=['있는 그대로의 형태', '왼쪽으로 90도 회전한 형태', '오른쪽으로 90도 회전한 형태', '180도 회전한 형태']))

    st.write('[종성 대응표]')
    st.write(pd.DataFrame.from_dict(coda_dict, orient='index',
                                    columns=['있는 그대로의 형태', '왼쪽으로 90도 회전한 형태', '오른쪽으로 90도 회전한 형태', '180도 회전한 형태']))

url = 'https://github.com/yeounyi/write_hangul_w_alphabet'
if st.button('Github'):
    webbrowser.open_new_tab(url)




