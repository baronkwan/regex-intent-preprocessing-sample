import re
import logging

logging.basicConfig(level=logging.DEBUG, filename='sample_intent_sharing.log', format='%(asctime)s %(levelname)s:%(message)s')

# read input file
f = open('translation.yaml', 'r+')
# create output file
file = open('./test_finished_translation.yaml', 'w')

# two [personName & appName] tasks specific pattern substitutions
def with_personName_pattern_sub(curr_line):
    ### [ with {{$urn:contacts:com.banana.contact.people}}] pattern
    with_pattern = r" with {{\$urn:contacts:com\.banana\.contact\.people}}"
    new_pattern = "同{{$urn:contacts:com.banana.contact.people}}"
    hey_voice_assistant_pattern = r"\- \(喂 Voice Assistant \|voice_assistant{ }\|唔該\)"
    if re.search(with_pattern, curr_line):
        logging.debug("[Found match - with_personName pattern]")
        if re.search(hey_voice_assistant_pattern, curr_line):
            logging.debug("[Found hey voice_assistant pattern@with_personName pattern]")
            logging.debug('performing with_personName & hey_voice_assistant pattern substitution...')
            curr_line = curr_line.replace(' with {{$urn:contacts:com.banana.contact.people}}', '')
            curr_line = re.sub(hey_voice_assistant_pattern, "- (喂 Voice Assistant |voice_assistant{ }|唔該)同{{$urn:contacts:com.banana.contact.people}}", curr_line)
            return curr_line
        else:
            logging.debug('performing with_personName substitution...')
            curr_line = curr_line.replace(' with {{$urn:contacts:com.banana.contact.people}}', '')
            curr_line = curr_line.replace('- (', '- 同{{$urn:contacts:com.banana.contact.people}}(')
            return curr_line
    else:
        logging.debug("[with_personName pattern not found.]")
        return curr_line

def on_using_appName_pattern_sub(curr_line):
    ### [(on|using) {{$urn:appname:com.banana.voice_assistant.applications}}] pattern
    app_pattern = r"用{{\$urn:appname:com\.banana\.voice_assistant\.applications}}"
    new_pattern = "用{{$urn:appname:com.banana.voice_assistant.applications}}"
    hey_voice_assistant_pattern = r"\- \(喂 Voice Assistant \|voice_assistant{ }\|唔該\)"
    if re.search(app_pattern, curr_line):
        logging.debug("[Found match - on_using_appName pattern]")
        if re.search(hey_voice_assistant_pattern, curr_line):
            logging.debug("[Found hey voice_assistant pattern@on_using_appName pattern]")
            logging.debug('performing on_using_appName & hey_voice_assistant pattern substitution...')
            curr_line = curr_line.replace('用{{$urn:appname:com.banana.voice_assistant.applications}}', '')
            curr_line = re.sub(hey_voice_assistant_pattern, "- (喂 Voice Assistant |voice_assistant{ }|唔該)用{{$urn:appname:com.banana.voice_assistant.applications}}", curr_line)
            return curr_line
        else:
            logging.debug('performing on_using_appName pattern substitution...')
            curr_line = curr_line.replace('用{{$urn:appname:com.banana.voice_assistant.applications}}', '')
            curr_line = curr_line.replace('- (', '- 用{{$urn:appname:com.banana.voice_assistant.applications}}(')
            return curr_line
    else:
        logging.debug("[on_using_appName pattern not found.]")
        return curr_line

for line in f.readlines():

    # translate sharingVerb
    line = re.sub(r'\ssend\s', '(send |發送|傳送)',line)
    line = re.sub(r'\sshare\s', '(share |分享)',line)
    line = re.sub(r'\sand say\s', '然後講',line)

    # translate sharingNoun
    ### find sharingNoun where ")" precedes and translate the pattern
    line = re.sub(r"(?<=\))app", '(app |{應用}程式)',line)
    line = re.sub(r"(?<=\))album", '(唱片|專輯|CD{ }|{光}碟)',line)
    line = re.sub(r"(?<=\))book", '書{籍}',line)
    line = re.sub(r"(?<=\))episode", '節目',line)
    line = re.sub(r"(?<=\))\(movie\|film\)", '(電影|影片|戲)',line)
    line = re.sub(r"(?<=\))playlist", '(歌單|播放列表|音樂列表)',line)
    line = re.sub(r"(?<=\))show", '(電視節目|{電視}影集|tv show{ })',line)
    line = re.sub(r"(?<=\))\(webpage\|web page\|website\|site\)", '(網{站}|網址|{網路}連結|url{ }|website{ }|webpage{ }|link{ })',line)

    ### find sharingNoun where "this" precedes and translate the pattern
    line = re.sub(r"this app", '{(呢|嗰|這|那){一}(個|隻)}(app{ }|{應用}程式)',line)
    line = re.sub(r"this album", '{(呢|嗰|這|那){一}(個|隻)}{音樂}(唱片|專輯|CD{ }|{光}碟)',line)
    line = re.sub(r"this book", '{(呢|嗰|這|那){一}(個|本)}書{籍}',line)
    line = re.sub(r"this episode", '{(呢|嗰|這|那){一}(個|隻)}(集|個|輯|套|部)}節目',line)
    line = re.sub(r"this \(movie\|film\)", '{(呢|嗰|這|那){一}(集|個|輯|套|部)}(電影|影片|戲)',line)
    line = re.sub(r"this playlist", '{(呢|嗰|這|那){一}個}(歌單|播放列表|音樂列表)',line)
    line = re.sub(r"this show", '{(呢|嗰|這|那){一}(集|個|輯|套|部)}(電視節目|{電視}影集|tv show{ })',line)
    line = re.sub(r"this \(webpage\|web page\|website\|site\)", '{(呢|嗰|這|那){一}(個|條)}(網{站}|網址|{網路}連結|url{ }|website{ }|webpage{ }|link{ })',line)


    # other translation
    ### replace "hey voice_assistant" to "喂 Voice Assistant "
    line = re.sub(r'hey voice_assistant', '喂 Voice Assistant ',line)
    line = re.sub(r'voice_assistant\|', 'voice_assistant{ }|',line)

    ### replace "please" to "唔該"
    line = re.sub(r'please', '唔該',line)

    # r'\sWORD\s' is a regex expression that select WORD between two whitespaces
    ### replace to & (on|using) with 俾 & 用 respectively
    line = re.sub(r'\sto\s', '俾',line)
    line = re.sub(r"\s\(on\|using\)\s", '用',line)

    # first formatting dislocation due to replacement
    line = line.replace('-(', '- (')
    line = line.replace('|)', ')')

    # perform with_personName & on_using_appName placeholder substitution
    line = with_personName_pattern_sub(line)
    line = on_using_appName_pattern_sub(line)

    # second formatting dislocation due to replacement
    line = line.replace(') (', ')(')
    line = line.replace('} (', '}(')

    logging.debug(line)
    file.write(line)
    f.truncate()
    
# closing r+ & w mode text_io_wrappers respectively
f.close()
file.close()

    

        