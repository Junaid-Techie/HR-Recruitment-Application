import textract
import re
from .helpers import _write_to_disk, _read_from_url, _profiles_write_to_disk
import nltk

# nltk.download('maxent_treebank_pos_tagger')
from nameparser.parser import HumanName
from nltk.corpus import wordnet


def from_file(file_path, **kwargs):
    filename = str(file_path.resolve())
    text = textract.process(filename)
    return (filename, text.decode('utf-8'))


def from_stream(stream, ext, **kwargs):
    file_name = _write_to_disk(stream, ext)
    (filename, content )= from_file(file_name)
    return (filename, content )

def _write_stream(stream, ext, _dir, **kwargs):
    file_name = _profiles_write_to_disk(stream, ext, _dir)
    (filename, content )= from_file(file_name)
    return (filename, content )

def from_url(url, mime_type, **kwargs):
    file_name = _write_to_disk(_read_from_url(url), mime_type)
    return from_file(file_name)


def get_human_names(text):
    person_list = []
    tokens = nltk.tokenize.word_tokenize(text)
    pos = nltk.pos_tag(tokens)
    sentence = nltk.ne_chunk(pos, binary=False)

    person = []
    name = ""
    for subtree in sentence.subtrees(filter=lambda t: t.label() == 'PERSON' or t.label() == 'ORGANIZATION'):
        for leaf in subtree.leaves():
            person.append(leaf[0])
        if len(person) > 0:  # avoid grabbing lone surnames
            for part in person:
                name += part + ' '
            if name[:-1] not in person_list:
                person_list.append(name[:-1])
            name = ''
        person = []
    return person_list


def find_email(text):
    emails = re.findall('[a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+', text)
    return [email for email in emails]

def find_postcode(text):
    POSTCODE_REGEX = r"(^[1-9]{1}[0-9]{2}\s{0,1}[0-9]{3}$)"


def find_contact(text):
    phones = re.findall('(?:\+ *)?\d[\d\- ]{7,}\d', text)
    return [phone.replace('-', '').replace(' ', '') for phone in phones]


def find_years_exp(text):
    regex = r"\b(?:\d+\.*\-*\+*\d+ [yY]e|[02-9] [Yy]ears|1 [Yy]ear|[1-9]\d+\+? [Yy]ears)\b"
    matches = re.search(regex, text)
    if matches:
        return matches.group()

def parse_us_resume_format(details):
    parsed_data = {'mobile': '', 'name': '', 'email': '', 'exp': ''}
    next = 0
    for line in details[1:15]:
        if 'name' in line.lower() and 'candidate' in line.lower() and not parsed_data.get('name'):
            parsed_data['name'] = details[next+2]
        if 'exp' in line.lower() :
            parsed_data['exp'] = details[next+3]
        if 'qualif' in line.lower() :
            parsed_data['edu'] = details[next+2]
        next = next + 1
    return parsed_data

def get_required_info(data):
    parsed_data = {'mobile': '', 'name': '', 'email': '', 'exp': ''}
    details = [line.replace('\t', ' ') for line in data.split('\n') if line]
    #names = get_human_names(data)
    parsed_data = parse_us_resume_format(details)
    if parsed_data['name'] is None or parsed_data['name'] == '':
        parsed_data['exp'] = ''
        parsed_data['mobile'] = ''
        parsed_data['email'] = ''
        parsed_data['exp'] = find_years_exp(data)

    cnt = 0


    for i in details:
        # if parsed_data['exp'] == '' and parsed_data['name'] == ''\
        #         and parsed_data['email'] == '' and parsed_data['mobile'] == '':
        #     break

        mobile_number, email, name, exp = ('', '', '', '')
        if not parsed_data.get('mobile'):
            mobile_number = find_contact(i)
        if not parsed_data.get('email'):
            email = find_email(i)
        if not parsed_data.get('name'):
            name = get_human_names(i)

        if (not parsed_data.get('mobile') and mobile_number and len(str(mobile_number[0])) > 9):
            parsed_data['mobile'] = mobile_number[0]
        if (not parsed_data.get('email') and email):
            parsed_data['email'] = email[0]
        if (not parsed_data.get('exp') and exp):
            parsed_data['exp'] = exp

        if (not parsed_data.get('name') and name and cnt <= 5):
            if 'resume' in name[0] or 'curr' in name[0]:  # curr or resume
                parsed_data['name'] = name[-1]
                if len(parsed_data['name']) > 100:
                    parsed_data['name'] = (parsed_data['name'])[0:100]
            else:
                parsed_data['name'] = ' '.join(name)
                if len(parsed_data['name']) > 100:
                    parsed_data['name'] = (parsed_data['name'])[0:100]
        cnt = cnt+1
    return parsed_data
